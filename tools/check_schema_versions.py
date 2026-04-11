#!/usr/bin/env python3
"""Validate schema versioning across the academic-research-skills repository.

Checks:
1. All 15 schemas are documented in shared/handoff_schemas.md
2. Agent files that produce schemas include schema_version guidance
3. shared/schema_migrations.md exists and contains the migration registry
4. Version compatibility matrix matches plugin version from plugin.json
5. All schemas have version documentation

Exit code 0 if all checks pass, 1 otherwise.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

REPO_ROOT = Path(__file__).resolve().parent.parent
HANDOFF_SCHEMAS_PATH = REPO_ROOT / "shared" / "handoff_schemas.md"
SCHEMA_MIGRATIONS_PATH = REPO_ROOT / "shared" / "schema_migrations.md"
PLUGIN_JSON_PATH = REPO_ROOT / ".claude-plugin" / "plugin.json"

EXPECTED_SCHEMA_COUNT = 18

SCHEMA_NAMES: dict[int, str] = {
    1: "RQ Brief",
    2: "Bibliography",
    3: "Synthesis Report",
    4: "Paper Draft",
    5: "Integrity Report",
    6: "Review Report",
    7: "Revision Roadmap",
    8: "Response to Reviewers",
    9: "Material Passport",
    10: "Experiment Design",
    11: "Experiment Results",
    12: "Lab Record",
    13: "Simulation Specification",
    14: "Methodology Blueprint",
    15: "INSIGHT Collection",
    16: "Concept Lineage Report",
    17: "Style Profile",
    18: "R&R Traceability Matrix",
}

# Agents known to produce schema artifacts (agent file path relative to repo root)
# Maps agent -> list of schema numbers it produces
PRODUCER_AGENTS: dict[str, list[int]] = {
    "deep-research/agents/research_question_agent.md": [1],
    "deep-research/agents/socratic_mentor_agent.md": [1, 15],
    "deep-research/agents/bibliography_agent.md": [2],
    "deep-research/agents/synthesis_agent.md": [3],
    "deep-research/agents/research_architect_agent.md": [14],
    "deep-research/agents/report_compiler_agent.md": [4],
    "academic-paper/agents/draft_writer_agent.md": [4, 8],
    "academic-pipeline/agents/integrity_verification_agent.md": [5],
    "academic-paper-reviewer/agents/editorial_synthesizer_agent.md": [6, 7, 18],
    "experiment-designer/agents/protocol_compiler_agent.md": [9, 10, 13],
    "data-analyst/agents/report_compiler_agent.md": [11],
    "simulation-runner/agents/report_compiler_agent.md": [11],
    "lab-notebook/agents/provenance_auditor_agent.md": [12],
    "deep-research/agents/concept_lineage_agent.md": [16],
    "academic-paper/agents/intake_agent.md": [17],
}


# ---------------------------------------------------------------------------
# Result tracking
# ---------------------------------------------------------------------------


class CheckResult:
    """Stores the outcome of a single check."""

    def __init__(self, name: str) -> None:
        self.name = name
        self.status: str = "PASS"  # PASS | WARN | FAIL
        self.messages: list[str] = []

    def warn(self, msg: str) -> None:
        if self.status == "PASS":
            self.status = "WARN"
        self.messages.append(f"  WARN: {msg}")

    def fail(self, msg: str) -> None:
        self.status = "FAIL"
        self.messages.append(f"  FAIL: {msg}")

    def info(self, msg: str) -> None:
        self.messages.append(f"  INFO: {msg}")

    def report(self) -> str:
        header = f"[{self.status}] {self.name}"
        if self.messages:
            return header + "\n" + "\n".join(self.messages)
        return header


# ---------------------------------------------------------------------------
# Check 1: All 18 schemas documented in handoff_schemas.md
# ---------------------------------------------------------------------------


def check_schemas_documented() -> CheckResult:
    result = CheckResult(f"Check 1: All {EXPECTED_SCHEMA_COUNT} schemas documented in handoff_schemas.md")

    if not HANDOFF_SCHEMAS_PATH.exists():
        result.fail(f"File not found: {HANDOFF_SCHEMAS_PATH}")
        return result

    content = HANDOFF_SCHEMAS_PATH.read_text(encoding="utf-8")

    # Find all "## Schema N:" headers
    schema_pattern = re.compile(r"^## Schema (\d+):", re.MULTILINE)
    found_schemas = {int(m.group(1)) for m in schema_pattern.finditer(content)}

    for num in range(1, EXPECTED_SCHEMA_COUNT + 1):
        if num in found_schemas:
            result.info(f"Schema {num} ({SCHEMA_NAMES.get(num, '?')}): documented")
        else:
            result.fail(f"Schema {num} ({SCHEMA_NAMES.get(num, '?')}): NOT documented")

    # Check for unexpected schemas beyond 15 (excluding the "Schema Versioning" section)
    unexpected = found_schemas - set(range(1, EXPECTED_SCHEMA_COUNT + 1))
    for num in sorted(unexpected):
        result.warn(f"Unexpected Schema {num} found in handoff_schemas.md")

    result.info(f"Found {len(found_schemas)}/{EXPECTED_SCHEMA_COUNT} schemas")
    return result


# ---------------------------------------------------------------------------
# Check 2: Agent files include schema_version guidance
# ---------------------------------------------------------------------------


def check_agent_schema_guidance() -> CheckResult:
    result = CheckResult("Check 2: Producer agents include schema_version guidance")

    schema_version_patterns = [
        re.compile(r"schema.?version", re.IGNORECASE),
        re.compile(r"Schema Version.*1\.0", re.IGNORECASE),
        re.compile(r"\bschema_version\b", re.IGNORECASE),
    ]

    schema_ref_pattern = re.compile(r"Schema \d+", re.IGNORECASE)

    for agent_rel, schema_nums in PRODUCER_AGENTS.items():
        agent_path = REPO_ROOT / agent_rel
        if not agent_path.exists():
            result.warn(f"Agent file not found: {agent_rel}")
            continue

        if not schema_nums:
            # Agent doesn't produce schemas directly; skip version check
            continue

        content = agent_path.read_text(encoding="utf-8")

        # Check if agent references schema production
        has_schema_ref = bool(schema_ref_pattern.search(content))
        has_version_guidance = any(p.search(content) for p in schema_version_patterns)

        schemas_str = ", ".join(f"Schema {n}" for n in schema_nums)

        if has_schema_ref and has_version_guidance:
            result.info(
                f"{agent_rel}: references schemas ({schemas_str}) "
                f"AND includes schema_version guidance"
            )
        elif has_schema_ref and not has_version_guidance:
            result.warn(
                f"{agent_rel}: references schemas ({schemas_str}) "
                f"but MISSING schema_version guidance"
            )
        elif not has_schema_ref:
            result.warn(
                f"{agent_rel}: expected to produce {schemas_str} "
                f"but no schema references found"
            )

    return result


# ---------------------------------------------------------------------------
# Check 3: schema_migrations.md exists and has migration registry
# ---------------------------------------------------------------------------


def check_migrations_file() -> CheckResult:
    result = CheckResult("Check 3: schema_migrations.md exists with migration registry")

    if not SCHEMA_MIGRATIONS_PATH.exists():
        result.fail(f"File not found: {SCHEMA_MIGRATIONS_PATH}")
        return result

    content = SCHEMA_MIGRATIONS_PATH.read_text(encoding="utf-8")

    # Check for required sections
    required_sections = [
        ("Schema Versioning Protocol", r"##.*Schema Versioning Protocol"),
        ("Version Compatibility Matrix", r"##.*Version Compatibility Matrix"),
        ("Migration Rules", r"##.*Migration Rules"),
        ("Migration Registry", r"##.*Migration Registry"),
        ("Adding Schema Version", r"##.*Adding Schema Version"),
        ("Staleness Detection Protocol", r"##.*Staleness Detection"),
    ]

    for section_name, pattern in required_sections:
        if re.search(pattern, content, re.IGNORECASE):
            result.info(f"Section found: {section_name}")
        else:
            result.fail(f"Section MISSING: {section_name}")

    # Check that all 15 schemas are listed in the current versions table
    for num in range(1, EXPECTED_SCHEMA_COUNT + 1):
        schema_name = SCHEMA_NAMES.get(num, "?")
        # Look for "Schema N" in the versions table
        if re.search(rf"Schema {num}\s*\|", content):
            result.info(f"Schema {num} ({schema_name}): listed in versions table")
        else:
            result.warn(f"Schema {num} ({schema_name}): NOT listed in versions table")

    return result


# ---------------------------------------------------------------------------
# Check 4: Version compatibility matrix matches plugin version
# ---------------------------------------------------------------------------


def check_version_compatibility() -> CheckResult:
    result = CheckResult("Check 4: Compatibility matrix matches plugin.json version")

    if not PLUGIN_JSON_PATH.exists():
        result.fail(f"File not found: {PLUGIN_JSON_PATH}")
        return result

    if not SCHEMA_MIGRATIONS_PATH.exists():
        result.fail(f"File not found: {SCHEMA_MIGRATIONS_PATH}")
        return result

    try:
        plugin_data = json.loads(PLUGIN_JSON_PATH.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as exc:
        result.fail(f"Cannot parse plugin.json: {exc}")
        return result

    plugin_version = plugin_data.get("version", "")
    if not plugin_version:
        result.fail("plugin.json missing 'version' field")
        return result

    result.info(f"Plugin version from plugin.json: {plugin_version}")

    migrations_content = SCHEMA_MIGRATIONS_PATH.read_text(encoding="utf-8")

    # Extract the major.minor prefix for matching (e.g., "3.7.1" -> "3.7")
    version_parts = plugin_version.split(".")
    if len(version_parts) >= 2:
        major_minor = f"{version_parts[0]}.{version_parts[1]}"
    else:
        major_minor = plugin_version

    # Check that the compatibility matrix mentions the current version or its range
    # Look for patterns like "v3.7.1" or "v3.7.1+"
    version_in_matrix = re.search(
        rf"v{re.escape(plugin_version)}", migrations_content
    ) or re.search(rf"v{re.escape(major_minor)}\.\d+\+", migrations_content)

    if version_in_matrix:
        result.info(f"Plugin version v{plugin_version} found in compatibility matrix")
    else:
        result.fail(
            f"Plugin version v{plugin_version} NOT found in compatibility matrix. "
            f"Update the Version Compatibility Matrix in schema_migrations.md."
        )

    return result


# ---------------------------------------------------------------------------
# Check 5: All schemas have version documentation
# ---------------------------------------------------------------------------


def check_schema_version_docs() -> CheckResult:
    result = CheckResult("Check 5: All schemas have version documentation")

    if not HANDOFF_SCHEMAS_PATH.exists():
        result.fail(f"File not found: {HANDOFF_SCHEMAS_PATH}")
        return result

    content = HANDOFF_SCHEMAS_PATH.read_text(encoding="utf-8")

    # Check that the Schema Versioning section exists
    if re.search(r"##.*Schema Versioning", content, re.IGNORECASE):
        result.info("Schema Versioning section found in handoff_schemas.md")
    else:
        result.fail(
            "Schema Versioning section MISSING in handoff_schemas.md. "
            "Add '## 16. Schema Versioning' section."
        )

    # Check for schema_version field documentation
    if re.search(r"schema_version", content, re.IGNORECASE):
        result.info("schema_version field documented in handoff_schemas.md")
    else:
        result.warn("schema_version field not mentioned in handoff_schemas.md")

    # Check cross-reference to schema_migrations.md
    if re.search(r"schema_migrations\.md", content):
        result.info("Cross-reference to schema_migrations.md found")
    else:
        result.warn("No cross-reference to schema_migrations.md in handoff_schemas.md")

    # Check that the migrations file documents all 15 schemas
    if SCHEMA_MIGRATIONS_PATH.exists():
        migrations_content = SCHEMA_MIGRATIONS_PATH.read_text(encoding="utf-8")
        documented_in_migrations = set()
        for num in range(1, EXPECTED_SCHEMA_COUNT + 1):
            if re.search(rf"Schema {num}\s*\|", migrations_content):
                documented_in_migrations.add(num)

        missing = set(range(1, EXPECTED_SCHEMA_COUNT + 1)) - documented_in_migrations
        if missing:
            for num in sorted(missing):
                result.fail(
                    f"Schema {num} ({SCHEMA_NAMES.get(num, '?')}): "
                    f"missing version documentation in schema_migrations.md"
                )
        else:
            result.info(
                f"All {EXPECTED_SCHEMA_COUNT} schemas have version documentation "
                f"in schema_migrations.md"
            )
    else:
        result.fail("schema_migrations.md not found for version documentation check")

    return result


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> int:
    print("=" * 70)
    print("Schema Version Validation Report")
    print(f"Repository: {REPO_ROOT}")
    print("=" * 70)
    print()

    checks = [
        check_schemas_documented,
        check_agent_schema_guidance,
        check_migrations_file,
        check_version_compatibility,
        check_schema_version_docs,
    ]

    results: list[CheckResult] = []
    for check_fn in checks:
        check_result = check_fn()
        results.append(check_result)
        print(check_result.report())
        print()

    # Summary
    print("=" * 70)
    print("Summary")
    print("=" * 70)

    pass_count = sum(1 for r in results if r.status == "PASS")
    warn_count = sum(1 for r in results if r.status == "WARN")
    fail_count = sum(1 for r in results if r.status == "FAIL")

    print(f"  PASS: {pass_count}")
    print(f"  WARN: {warn_count}")
    print(f"  FAIL: {fail_count}")
    print()

    if fail_count > 0:
        print("RESULT: FAIL — address the issues above before proceeding.")
        return 1

    if warn_count > 0:
        print("RESULT: PASS WITH WARNINGS — review warnings above.")
        return 0

    print("RESULT: ALL CHECKS PASSED")
    return 0


if __name__ == "__main__":
    sys.exit(main())
