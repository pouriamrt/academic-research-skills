"""Validate consistency between handoff schema definitions and agent file references.

Parses shared/handoff_schemas.md for schema definitions (1-15), scans all
agent files (*/agents/*.md) and SKILL.md files for schema references, and
checks for orphaned schemas, undefined references, producer/consumer mismatches,
cross-reference integrity, and required-field coverage.

Usage:
    python tools/validate_schemas.py          # from repo root
    python tools/validate_schemas.py --verbose  # show per-file detail
"""

from __future__ import annotations

import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import NamedTuple


# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------


@dataclass
class SchemaDefinition:
    """A single schema parsed from handoff_schemas.md."""

    number: int
    name: str
    producer_agents: list[str] = field(default_factory=list)
    consumer_agents: list[str] = field(default_factory=list)
    required_fields: list[str] = field(default_factory=list)
    optional_fields: list[str] = field(default_factory=list)


class AgentRef(NamedTuple):
    """A reference to a schema found inside an agent or SKILL file."""

    file_path: str  # relative to repo root
    schema_number: int
    line_number: int
    line_text: str


class CheckResult(NamedTuple):
    """Result of a single validation check."""

    status: str  # PASS, WARN, FAIL
    title: str
    details: list[str]


# ---------------------------------------------------------------------------
# Parsing helpers
# ---------------------------------------------------------------------------

REPO_ROOT = Path(__file__).resolve().parent.parent


def _normalise_agent_path(raw: str) -> str:
    """Turn a producer/consumer string like
    `deep-research/research_question_agent` into a normalised form that can be
    compared with file-derived agent identifiers.

    The convention in handoff_schemas.md is ``skill/agent_name`` (without the
    ``agents/`` directory component and without the ``.md`` extension).

    Handles trailing annotations like:
        `academic-paper/draft_writer_agent` (revision mode)
        `experiment-designer/protocol_compiler_agent` (only when Schema 10 ...)
    """
    cleaned = raw.strip()
    # Strip backtick-delimited portion and any trailing parenthetical note
    # Pattern: `skill/agent` (optional note) or `skill/agent`
    m = re.match(r"`([^`]+)`(?:\s*\(.*\))?\s*$", cleaned)
    if m:
        return m.group(1).strip()
    # Fallback: strip backticks and parenthetical
    cleaned = cleaned.strip("`")
    cleaned = re.sub(r"\s*\(.*\)\s*$", "", cleaned)
    return cleaned.strip()


def parse_schemas(schemas_path: Path) -> dict[int, SchemaDefinition]:
    """Parse all schema definitions from handoff_schemas.md."""

    text = schemas_path.read_text(encoding="utf-8")
    schemas: dict[int, SchemaDefinition] = {}

    # Split on Schema headers: "## Schema N: <Name>"
    header_pattern = re.compile(
        r"^## Schema (\d+):\s*(.+?)(?:\s*\(.*\))?\s*$", re.MULTILINE
    )
    matches = list(header_pattern.finditer(text))

    for idx, m in enumerate(matches):
        num = int(m.group(1))
        name = m.group(2).strip()
        # Extract the block between this header and the next (or EOF)
        start = m.end()
        end = matches[idx + 1].start() if idx + 1 < len(matches) else len(text)
        block = text[start:end]

        schema = SchemaDefinition(number=num, name=name)

        # --- Producers / Consumers ---
        # Lines like: **Producer**: `skill/agent` | `skill/agent`
        # or          **Consumer**: `skill/agent` | `skill/agent`
        prod_match = re.search(r"\*\*Producer\*\*:\s*(.+?)$", block, re.MULTILINE)
        if prod_match:
            raw = prod_match.group(1)
            schema.producer_agents = [
                _normalise_agent_path(p)
                for p in re.split(r"\s*\|\s*", raw)
                if p.strip()
            ]

        cons_match = re.search(r"\*\*Consumer\*\*:\s*(.+?)$", block, re.MULTILINE)
        if cons_match:
            raw = cons_match.group(1)
            schema.consumer_agents = [
                _normalise_agent_path(c)
                for c in re.split(r"\s*\|\s*", raw)
                if c.strip()
            ]

        # --- Required Fields ---
        # Look for "### Required Fields" followed by a Markdown table.
        req_section = re.search(
            r"### Required Fields\s*\n(.*?)(?=\n### |\n## |\n---|\Z)",
            block,
            re.DOTALL,
        )
        if req_section:
            for row in re.finditer(
                r"^\|\s*`([^`]+)`\s*\|", req_section.group(1), re.MULTILINE
            ):
                schema.required_fields.append(row.group(1))

        # --- Optional Fields ---
        opt_section = re.search(
            r"### Optional Fields\s*\n(.*?)(?=\n### |\n## |\n---|\Z)",
            block,
            re.DOTALL,
        )
        if opt_section:
            for row in re.finditer(
                r"^\|\s*`([^`]+)`\s*\|", opt_section.group(1), re.MULTILINE
            ):
                schema.optional_fields.append(row.group(1))

        schemas[num] = schema

    return schemas


def scan_agent_files(root: Path) -> list[AgentRef]:
    """Scan */agents/*.md for all 'Schema N' references."""

    refs: list[AgentRef] = []
    pattern = re.compile(r"Schema\s+(\d+)")

    for md_file in sorted(root.glob("*/agents/*.md")):
        rel = md_file.relative_to(root).as_posix()
        for line_no, line in enumerate(
            md_file.read_text(encoding="utf-8").splitlines(), start=1
        ):
            for m in pattern.finditer(line):
                refs.append(AgentRef(rel, int(m.group(1)), line_no, line.strip()))

    return refs


def scan_skill_files(root: Path) -> list[AgentRef]:
    """Scan */SKILL.md for all 'Schema N' references."""

    refs: list[AgentRef] = []
    pattern = re.compile(r"Schema\s+(\d+)")

    for md_file in sorted(root.glob("*/SKILL.md")):
        rel = md_file.relative_to(root).as_posix()
        for line_no, line in enumerate(
            md_file.read_text(encoding="utf-8").splitlines(), start=1
        ):
            for m in pattern.finditer(line):
                refs.append(AgentRef(rel, int(m.group(1)), line_no, line.strip()))

    return refs


def _agent_id_from_path(rel_path: str) -> str:
    """Convert 'deep-research/agents/bibliography_agent.md'
    -> 'deep-research/bibliography_agent' to match schema notation."""

    parts = Path(rel_path).parts
    # Expected: (<skill>, "agents", <agent>.md)
    if len(parts) >= 3 and parts[1] == "agents":
        skill = parts[0]
        agent = Path(parts[2]).stem  # drop .md
        return f"{skill}/{agent}"
    return rel_path


# ---------------------------------------------------------------------------
# Validation checks
# ---------------------------------------------------------------------------


def check_orphaned_schemas(
    schemas: dict[int, SchemaDefinition],
    agent_refs: list[AgentRef],
    skill_refs: list[AgentRef],
) -> CheckResult:
    """Schemas defined in handoff_schemas.md but never referenced elsewhere."""

    referenced_nums = {r.schema_number for r in agent_refs} | {
        r.schema_number for r in skill_refs
    }
    orphaned = sorted(n for n in schemas if n not in referenced_nums)
    if orphaned:
        details = [
            f"Schema {n} ({schemas[n].name}) — defined but never referenced in any agent or SKILL file"
            for n in orphaned
        ]
        return CheckResult("WARN", "Orphaned schemas", details)
    return CheckResult("PASS", "Orphaned schemas", ["All schemas are referenced."])


def check_undefined_references(
    schemas: dict[int, SchemaDefinition],
    agent_refs: list[AgentRef],
    skill_refs: list[AgentRef],
) -> CheckResult:
    """References to schema numbers that don't exist in handoff_schemas.md."""

    all_refs = agent_refs + skill_refs
    undefined: list[str] = []
    seen: set[tuple[str, int]] = set()
    for ref in all_refs:
        key = (ref.file_path, ref.schema_number)
        if key in seen:
            continue
        seen.add(key)
        if ref.schema_number not in schemas:
            undefined.append(
                f"{ref.file_path}:L{ref.line_number} references undefined Schema {ref.schema_number}"
            )

    if undefined:
        return CheckResult("FAIL", "Undefined schema references", undefined)
    return CheckResult(
        "PASS",
        "Undefined schema references",
        ["All references point to defined schemas."],
    )


def check_producer_consumer_mismatch(
    schemas: dict[int, SchemaDefinition],
    agent_refs: list[AgentRef],
) -> CheckResult:
    """For each schema, verify that its declared producers/consumers actually
    reference that schema in their agent file."""

    # Build a mapping: agent_id -> set of schema numbers referenced
    agent_schema_map: dict[str, set[int]] = {}
    for ref in agent_refs:
        aid = _agent_id_from_path(ref.file_path)
        agent_schema_map.setdefault(aid, set()).add(ref.schema_number)

    issues: list[str] = []

    for num, schema in sorted(schemas.items()):
        # Check producers
        for producer in schema.producer_agents:
            # Wildcard producers like `academic-paper-reviewer/*` match any
            # agent in that skill
            if producer.endswith("/*"):
                skill_prefix = producer[:-2]  # e.g. "academic-paper-reviewer"
                found = any(
                    aid.startswith(skill_prefix + "/") and num in snums
                    for aid, snums in agent_schema_map.items()
                )
                if not found:
                    issues.append(
                        f"Schema {num} ({schema.name}): declared producer "
                        f"'{producer}' — no agent file under {skill_prefix}/ "
                        f"references Schema {num}"
                    )
            else:
                if producer not in agent_schema_map:
                    issues.append(
                        f"Schema {num} ({schema.name}): declared producer "
                        f"'{producer}' has no agent file or no Schema {num} reference"
                    )
                elif num not in agent_schema_map[producer]:
                    issues.append(
                        f"Schema {num} ({schema.name}): declared producer "
                        f"'{producer}' exists but does not reference Schema {num}"
                    )

        # Check consumers
        for consumer in schema.consumer_agents:
            if consumer.endswith("/*"):
                skill_prefix = consumer[:-2]
                found = any(
                    aid.startswith(skill_prefix + "/") and num in snums
                    for aid, snums in agent_schema_map.items()
                )
                if not found:
                    issues.append(
                        f"Schema {num} ({schema.name}): declared consumer "
                        f"'{consumer}' — no agent file under {skill_prefix}/ "
                        f"references Schema {num}"
                    )
            else:
                if consumer not in agent_schema_map:
                    issues.append(
                        f"Schema {num} ({schema.name}): declared consumer "
                        f"'{consumer}' exists but does not reference Schema {num}"
                    )
                elif num not in agent_schema_map[consumer]:
                    issues.append(
                        f"Schema {num} ({schema.name}): declared consumer "
                        f"'{consumer}' exists but does not reference Schema {num}"
                    )

    if issues:
        return CheckResult("WARN", "Producer/Consumer mismatch", issues)
    return CheckResult(
        "PASS",
        "Producer/Consumer mismatch",
        ["All declared producers and consumers reference their schemas."],
    )


def check_skill_crossref(
    schemas: dict[int, SchemaDefinition],
    skill_refs: list[AgentRef],
) -> CheckResult:
    """Verify that all schema IDs used in SKILL.md files match definitions."""

    issues: list[str] = []
    seen: set[tuple[str, int]] = set()
    for ref in skill_refs:
        key = (ref.file_path, ref.schema_number)
        if key in seen:
            continue
        seen.add(key)
        if ref.schema_number not in schemas:
            issues.append(
                f"{ref.file_path}:L{ref.line_number} references undefined "
                f"Schema {ref.schema_number}"
            )

    if issues:
        return CheckResult("FAIL", "SKILL.md cross-reference integrity", issues)
    return CheckResult(
        "PASS",
        "SKILL.md cross-reference integrity",
        ["All SKILL.md schema references match definitions."],
    )


def check_required_field_coverage(
    schemas: dict[int, SchemaDefinition],
    agent_refs: list[AgentRef],
) -> CheckResult:
    """Heuristic: for each schema's declared producers, check whether the
    producer's agent file mentions the required field names."""

    issues: list[str] = []

    # Pre-load agent file contents for producers
    file_contents: dict[str, str] = {}
    for ref in agent_refs:
        if ref.file_path not in file_contents:
            full_path = REPO_ROOT / ref.file_path
            if full_path.exists():
                file_contents[ref.file_path] = full_path.read_text(
                    encoding="utf-8"
                ).lower()

    # Build reverse map: agent_id -> file_path
    agent_to_file: dict[str, str] = {}
    for ref in agent_refs:
        aid = _agent_id_from_path(ref.file_path)
        agent_to_file[aid] = ref.file_path

    for num, schema in sorted(schemas.items()):
        if not schema.required_fields:
            continue

        for producer in schema.producer_agents:
            if producer.endswith("/*"):
                # Skip wildcard producers for field coverage
                continue

            file_path = agent_to_file.get(producer)
            if not file_path:
                continue  # already reported in mismatch check

            content = file_contents.get(file_path, "")
            if not content:
                continue

            missing_fields: list[str] = []
            for field_name in schema.required_fields:
                # Heuristic: check if the field name (with underscores or
                # spaces or camelCase splits) appears in the file
                variants = [
                    field_name.lower(),
                    field_name.replace("_", " ").lower(),
                    field_name.replace("_", "-").lower(),
                ]
                found = any(v in content for v in variants)
                if not found:
                    missing_fields.append(field_name)

            if missing_fields:
                pct = (
                    (len(schema.required_fields) - len(missing_fields))
                    / len(schema.required_fields)
                    * 100
                )
                issues.append(
                    f"Schema {num} ({schema.name}), producer '{producer}': "
                    f"{len(missing_fields)}/{len(schema.required_fields)} required "
                    f"fields not mentioned ({pct:.0f}% coverage). "
                    f"Missing: {', '.join(missing_fields)}"
                )

    if issues:
        return CheckResult("WARN", "Required field coverage (heuristic)", issues)
    return CheckResult(
        "PASS",
        "Required field coverage (heuristic)",
        ["All producer agents mention their schemas' required fields."],
    )


# ---------------------------------------------------------------------------
# Report output
# ---------------------------------------------------------------------------

_STATUS_SYMBOL = {"PASS": "[PASS]", "WARN": "[WARN]", "FAIL": "[FAIL]"}


def print_report(
    schemas: dict[int, SchemaDefinition],
    agent_refs: list[AgentRef],
    skill_refs: list[AgentRef],
    results: list[CheckResult],
    verbose: bool = False,
) -> None:
    """Print a structured report to stdout."""

    # --- Summary ---
    unique_agent_files = {r.file_path for r in agent_refs}
    unique_skill_files = {r.file_path for r in skill_refs}
    total_refs = len(agent_refs) + len(skill_refs)

    print("=" * 64)
    print("  Handoff Schema Validation Report")
    print("=" * 64)
    print()
    print("Summary:")
    print(f"  Schemas defined:    {len(schemas)}")
    print(f"  Agent files scanned: {len(unique_agent_files)}")
    print(f"  SKILL files scanned: {len(unique_skill_files)}")
    print(f"  Total references:    {total_refs}")
    print()

    # --- Per-schema overview ---
    print("-" * 64)
    print("  Schema Overview")
    print("-" * 64)
    for num in sorted(schemas):
        s = schemas[num]
        agent_ref_count = sum(1 for r in agent_refs if r.schema_number == num)
        skill_ref_count = sum(1 for r in skill_refs if r.schema_number == num)
        print(
            f"  Schema {num:2d}: {s.name:<45s} "
            f"refs: {agent_ref_count + skill_ref_count:3d} "
            f"(agents: {agent_ref_count}, skills: {skill_ref_count})"
        )
    print()

    # --- Check results ---
    print("-" * 64)
    print("  Validation Checks")
    print("-" * 64)
    for result in results:
        symbol = _STATUS_SYMBOL[result.status]
        print(f"\n  {symbol} {result.title}")
        for detail in result.details:
            print(f"    - {detail}")

    # --- Verbose per-file detail ---
    if verbose:
        print()
        print("-" * 64)
        print("  Per-File Schema References")
        print("-" * 64)
        all_refs = sorted(
            agent_refs + skill_refs, key=lambda r: (r.file_path, r.line_number)
        )
        current_file = ""
        for ref in all_refs:
            if ref.file_path != current_file:
                current_file = ref.file_path
                print(f"\n  {current_file}")
            print(f"    L{ref.line_number:4d}: Schema {ref.schema_number}")

    # --- Final verdict ---
    statuses = [r.status for r in results]
    if "FAIL" in statuses:
        verdict = "FAIL"
    elif "WARN" in statuses:
        verdict = "WARN"
    else:
        verdict = "PASS"

    print()
    print("=" * 64)
    print(f"  Overall: {_STATUS_SYMBOL[verdict]}")
    warn_count = statuses.count("WARN")
    fail_count = statuses.count("FAIL")
    pass_count = statuses.count("PASS")
    print(f"  {pass_count} passed, {warn_count} warnings, {fail_count} failures")
    print("=" * 64)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> int:
    """Run all validation checks and return the exit code."""

    verbose = "--verbose" in sys.argv or "-v" in sys.argv

    schemas_path = REPO_ROOT / "shared" / "handoff_schemas.md"
    if not schemas_path.exists():
        print(f"ERROR: Cannot find {schemas_path}", file=sys.stderr)
        return 1

    # 1. Parse schema definitions
    schemas = parse_schemas(schemas_path)
    if not schemas:
        print("ERROR: No schemas found in handoff_schemas.md", file=sys.stderr)
        return 1

    # 2. Scan agent and SKILL files
    agent_refs = scan_agent_files(REPO_ROOT)
    skill_refs = scan_skill_files(REPO_ROOT)

    # 3. Run validation checks
    results: list[CheckResult] = [
        check_orphaned_schemas(schemas, agent_refs, skill_refs),
        check_undefined_references(schemas, agent_refs, skill_refs),
        check_producer_consumer_mismatch(schemas, agent_refs),
        check_skill_crossref(schemas, skill_refs),
        check_required_field_coverage(schemas, agent_refs),
    ]

    # 4. Print report
    print_report(schemas, agent_refs, skill_refs, results, verbose=verbose)

    # 5. Exit code
    has_fail = any(r.status == "FAIL" for r in results)
    return 1 if has_fail else 0


if __name__ == "__main__":
    sys.exit(main())
