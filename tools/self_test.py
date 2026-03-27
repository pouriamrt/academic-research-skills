#!/usr/bin/env python3
"""Structural integrity validator for the academic-research-skills plugin.

Validates plugin structure, agent completeness, shared infrastructure,
cross-reference integrity, template/reference/example coverage, version
consistency, and documentation health.  This is NOT an end-to-end pipeline
execution — it catches regressions after updates by verifying that all
declared components exist and are properly wired together.

Usage:
    python tools/self_test.py            # standard report
    python tools/self_test.py --verbose  # detailed per-check output
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Literal

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

EXPECTED_SKILLS = [
    "deep-research",
    "experiment-designer",
    "data-analyst",
    "simulation-runner",
    "lab-notebook",
    "academic-paper",
    "academic-paper-reviewer",
    "academic-pipeline",
]

SHARED_FILES = [
    "shared/handoff_schemas.md",
    "shared/experiment_infrastructure.md",
    "shared/superpowers_integration.md",
]

EXPECTED_SCHEMAS = list(range(1, 16))  # Schema 1-15

DOC_FILES = [
    "README.md",
    "CONTRIBUTING.md",
    ".claude/CLAUDE.md",
    ".claude/CHANGELOG.md",
]

# ---------------------------------------------------------------------------
# Result tracking
# ---------------------------------------------------------------------------

Status = Literal["PASS", "WARN", "FAIL"]


@dataclass
class CheckResult:
    """A single validation check result."""

    name: str
    status: Status
    message: str


@dataclass
class CategoryResult:
    """Results for a whole validation category."""

    name: str
    checks: list[CheckResult] = field(default_factory=list)

    def add(self, name: str, status: Status, message: str) -> None:
        self.checks.append(CheckResult(name=name, status=status, message=message))

    @property
    def status(self) -> Status:
        statuses = {c.status for c in self.checks}
        if "FAIL" in statuses:
            return "FAIL"
        if "WARN" in statuses:
            return "WARN"
        return "PASS"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _read_text(path: Path) -> str:
    """Read file as UTF-8 text, returning empty string on failure."""
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return ""


def _extract_agent_names_from_skill_md(text: str) -> set[str]:
    """Extract agent names referenced in a SKILL.md file.

    Matches patterns like:
      - `agent_name` in table rows (backtick-wrapped names ending with _agent)
      - [agent_name] in pipeline diagrams (bracket-wrapped)
      - agents/agent_name.md in file path references

    Excludes agents attributed to other skills, e.g.
    ``academic-paper``'s ``intake_agent`` is NOT counted as a local agent.
    """
    names: set[str] = set()

    # Collect cross-skill agent names so we can exclude them.
    # Pattern: `other-skill`'s `agent_name` or other-skill/agent_name
    cross_skill_agents: set[str] = set()
    for m in re.finditer(
        r"`[a-z][a-z0-9-]+`(?:'s|'s)\s+`([a-z][a-z0-9_]*_agent)`", text
    ):
        cross_skill_agents.add(m.group(1))
    for m in re.finditer(r"[a-z][a-z0-9-]+/([a-z][a-z0-9_]*_agent)", text):
        cross_skill_agents.add(m.group(1))

    # Backtick-wrapped agent names: `some_agent`
    for m in re.finditer(r"`([a-z][a-z0-9_]*_agent)`", text):
        name = m.group(1)
        if name not in cross_skill_agents:
            names.add(name)

    # Bracket-wrapped agent names in pipeline diagrams: [some_agent]
    for m in re.finditer(r"\[([a-z][a-z0-9_]*_agent)\]", text):
        names.add(m.group(1))

    # File path references: agents/some_agent.md
    for m in re.finditer(r"agents/([a-z][a-z0-9_]*_agent)\.md", text):
        names.add(m.group(1))

    return names


def _extract_schema_refs(text: str) -> set[int]:
    """Extract Schema N references from text."""
    return {int(m.group(1)) for m in re.finditer(r"Schema\s+(\d+)", text)}


def _extract_cross_agent_refs(text: str) -> set[tuple[str, str]]:
    """Extract cross-skill agent references like `skill-name/agent_name`.

    Returns set of (skill_name, agent_name) tuples.  Matches patterns such as:
      - `academic-paper/draft_writer_agent`
      - academic-paper/draft_writer_agent  (unquoted)
    """
    refs: set[tuple[str, str]] = set()
    for m in re.finditer(
        r"(?:`)?([a-z][a-z0-9-]*)/([a-z][a-z0-9_]*_agent)(?:`)?", text
    ):
        refs.add((m.group(1), m.group(2)))
    return refs


# ---------------------------------------------------------------------------
# Validation categories
# ---------------------------------------------------------------------------


def check_plugin_structure(root: Path, verbose: bool) -> CategoryResult:
    """1. Plugin Structure — plugin.json, skill dirs, SKILL.md, agents/."""
    cat = CategoryResult(name="Plugin Structure")

    # plugin.json exists and is valid JSON
    plugin_json_path = root / ".claude-plugin" / "plugin.json"
    if not plugin_json_path.is_file():
        cat.add("plugin.json exists", "FAIL", f"Missing: {plugin_json_path}")
        return cat

    try:
        plugin_data = json.loads(_read_text(plugin_json_path))
        cat.add("plugin.json valid JSON", "PASS", "Parsed successfully")
    except json.JSONDecodeError as exc:
        cat.add("plugin.json valid JSON", "FAIL", f"JSON parse error: {exc}")
        return cat

    # Skill paths resolve
    declared_skills = plugin_data.get("skills", [])
    for skill_path in declared_skills:
        # Paths in plugin.json are like "./deep-research"
        resolved = (root / skill_path).resolve()
        skill_name = Path(skill_path).name
        if resolved.is_dir():
            cat.add(f"skill dir: {skill_name}", "PASS", str(resolved))
        else:
            cat.add(f"skill dir: {skill_name}", "FAIL", f"Missing: {resolved}")

    # All 8 expected skills present
    declared_names = {Path(s).name for s in declared_skills}
    for expected in EXPECTED_SKILLS:
        if expected not in declared_names:
            cat.add(
                f"expected skill: {expected}", "FAIL", "Not declared in plugin.json"
            )

    # Each skill has SKILL.md and agents/
    for skill_name in EXPECTED_SKILLS:
        skill_dir = root / skill_name
        if not skill_dir.is_dir():
            continue  # already reported above

        skill_md = skill_dir / "SKILL.md"
        if skill_md.is_file():
            cat.add(f"{skill_name}/SKILL.md", "PASS", "Present")
        else:
            cat.add(f"{skill_name}/SKILL.md", "FAIL", "Missing")

        agents_dir = skill_dir / "agents"
        if agents_dir.is_dir():
            cat.add(f"{skill_name}/agents/", "PASS", "Present")
        else:
            cat.add(f"{skill_name}/agents/", "FAIL", "Missing")

    return cat


def check_agent_completeness(root: Path, verbose: bool) -> CategoryResult:
    """2. Agent Completeness — referenced vs actual agent files."""
    cat = CategoryResult(name="Agent Completeness")

    for skill_name in EXPECTED_SKILLS:
        skill_dir = root / skill_name
        agents_dir = skill_dir / "agents"
        skill_md_path = skill_dir / "SKILL.md"

        if not skill_md_path.is_file() or not agents_dir.is_dir():
            cat.add(
                f"{skill_name}: prerequisites",
                "FAIL",
                "SKILL.md or agents/ missing — skipping agent checks",
            )
            continue

        skill_text = _read_text(skill_md_path)
        referenced = _extract_agent_names_from_skill_md(skill_text)
        actual_files = {
            p.stem for p in agents_dir.iterdir() if p.suffix == ".md" and p.is_file()
        }

        # Every referenced agent must exist as a file
        missing = referenced - actual_files
        for agent in sorted(missing):
            cat.add(
                f"{skill_name}: {agent}",
                "FAIL",
                "Referenced in SKILL.md but no .md file in agents/",
            )

        # Orphaned agent files (exist but not referenced)
        orphaned = actual_files - referenced
        for agent in sorted(orphaned):
            cat.add(
                f"{skill_name}: {agent}",
                "WARN",
                "File exists in agents/ but not referenced in SKILL.md",
            )

        # Matched agents present
        matched = referenced & actual_files
        for agent in sorted(matched):
            cat.add(f"{skill_name}: {agent}", "PASS", "Referenced and present")

        # Agent files have at least one ## heading
        for agent_file in sorted(agents_dir.iterdir()):
            if agent_file.suffix != ".md" or not agent_file.is_file():
                continue
            text = _read_text(agent_file)
            headings = re.findall(r"^##\s+.+", text, re.MULTILINE)
            if len(headings) >= 1:
                cat.add(
                    f"{skill_name}/{agent_file.name} sections",
                    "PASS",
                    f"{len(headings)} ## headings found",
                )
            else:
                cat.add(
                    f"{skill_name}/{agent_file.name} sections",
                    "WARN",
                    "No ## headings found — agent may lack required sections",
                )

    return cat


def check_shared_infrastructure(root: Path, verbose: bool) -> CategoryResult:
    """3. Shared Infrastructure — handoff_schemas, experiment_infrastructure, superpowers."""
    cat = CategoryResult(name="Shared Infrastructure")

    for rel_path in SHARED_FILES:
        full_path = root / rel_path
        if full_path.is_file():
            cat.add(rel_path, "PASS", "Present")
        else:
            cat.add(rel_path, "FAIL", f"Missing: {full_path}")

    # handoff_schemas.md contains Schema 1-15
    schemas_path = root / "shared" / "handoff_schemas.md"
    if schemas_path.is_file():
        text = _read_text(schemas_path)
        defined_schemas = set()
        for m in re.finditer(r"^## Schema (\d+)", text, re.MULTILINE):
            defined_schemas.add(int(m.group(1)))

        for n in EXPECTED_SCHEMAS:
            if n in defined_schemas:
                cat.add(f"Schema {n} defined", "PASS", "Present in handoff_schemas.md")
            else:
                cat.add(
                    f"Schema {n} defined", "FAIL", "Missing from handoff_schemas.md"
                )

    return cat


def check_cross_reference_integrity(root: Path, verbose: bool) -> CategoryResult:
    """4. Cross-Reference Integrity — schema refs, cross-skill agent refs, shared doc paths."""
    cat = CategoryResult(name="Cross-Reference Integrity")

    # Build set of defined schema numbers
    schemas_path = root / "shared" / "handoff_schemas.md"
    defined_schemas: set[int] = set()
    if schemas_path.is_file():
        text = _read_text(schemas_path)
        for m in re.finditer(r"^## Schema (\d+)", text, re.MULTILINE):
            defined_schemas.add(int(m.group(1)))

    # Scan all agent files for Schema N references
    schema_issues = 0
    for skill_name in EXPECTED_SKILLS:
        agents_dir = root / skill_name / "agents"
        if not agents_dir.is_dir():
            continue
        for agent_file in sorted(agents_dir.iterdir()):
            if agent_file.suffix != ".md" or not agent_file.is_file():
                continue
            text = _read_text(agent_file)
            refs = _extract_schema_refs(text)
            for n in sorted(refs):
                if n not in defined_schemas:
                    cat.add(
                        f"{skill_name}/{agent_file.name}: Schema {n}",
                        "FAIL",
                        "References undefined schema",
                    )
                    schema_issues += 1
    if schema_issues == 0:
        cat.add("schema references", "PASS", "All schema refs match defined schemas")

    # Cross-skill agent references (e.g., academic-paper/draft_writer_agent)
    xref_issues = 0
    for skill_name in EXPECTED_SKILLS:
        agents_dir = root / skill_name / "agents"
        if not agents_dir.is_dir():
            continue
        for agent_file in sorted(agents_dir.iterdir()):
            if agent_file.suffix != ".md" or not agent_file.is_file():
                continue
            text = _read_text(agent_file)
            xrefs = _extract_cross_agent_refs(text)
            for target_skill, target_agent in sorted(xrefs):
                # Skip self-references
                if target_skill == skill_name:
                    target_path = agents_dir / f"{target_agent}.md"
                else:
                    target_path = root / target_skill / "agents" / f"{target_agent}.md"
                if not target_path.is_file():
                    cat.add(
                        f"{skill_name}/{agent_file.name}: {target_skill}/{target_agent}",
                        "FAIL",
                        f"Cross-reference target not found: {target_path}",
                    )
                    xref_issues += 1
    if xref_issues == 0:
        cat.add(
            "cross-skill agent refs",
            "PASS",
            "All cross-skill agent references resolve",
        )

    # File path references in shared/ docs
    shared_dir = root / "shared"
    path_issues = 0
    if shared_dir.is_dir():
        for shared_file in sorted(shared_dir.iterdir()):
            if shared_file.suffix != ".md" or not shared_file.is_file():
                continue
            text = _read_text(shared_file)
            # Match relative paths like ../skill/file.md or shared/file.md
            for m in re.finditer(
                r"(?:\.\.?/)?(?:[a-z][a-z0-9_-]*/)+[a-z][a-z0-9_-]*\.\w+", text
            ):
                ref_path = m.group(0)
                # Resolve relative to shared/ or root
                candidate1 = (shared_dir / ref_path).resolve()
                candidate2 = (root / ref_path).resolve()
                if not (candidate1.is_file() or candidate2.is_file()):
                    # Only flag .md file references — skip things like APA7.0
                    if ref_path.endswith(".md"):
                        cat.add(
                            f"shared/{shared_file.name}: {ref_path}",
                            "WARN",
                            "File path reference may not resolve",
                        )
                        path_issues += 1
    if path_issues == 0:
        cat.add(
            "shared doc file refs",
            "PASS",
            "All file path references in shared/ resolve (or no .md refs found)",
        )

    return cat


def check_template_reference_coverage(root: Path, verbose: bool) -> CategoryResult:
    """5. Template & Reference Coverage — each subdir has at least 1 file."""
    cat = CategoryResult(name="Template & Reference Coverage")

    for skill_name in EXPECTED_SKILLS:
        skill_dir = root / skill_name
        if not skill_dir.is_dir():
            continue

        for subdir_name in ("templates", "references", "examples"):
            subdir = skill_dir / subdir_name
            if not subdir.is_dir():
                # Not all skills are required to have all subdirs;
                # only check if the dir exists
                continue

            files = [
                f
                for f in subdir.iterdir()
                if f.is_file() and not f.name.startswith(".")
            ]
            if files:
                cat.add(
                    f"{skill_name}/{subdir_name}",
                    "PASS",
                    f"{len(files)} file(s)",
                )
            else:
                cat.add(
                    f"{skill_name}/{subdir_name}",
                    "FAIL",
                    "Directory exists but contains no files",
                )

    return cat


def check_version_consistency(root: Path, verbose: bool) -> CategoryResult:
    """6. Version Consistency — plugin.json vs .claude/CLAUDE.md."""
    cat = CategoryResult(name="Version Consistency")

    plugin_json_path = root / ".claude-plugin" / "plugin.json"
    claude_md_path = root / ".claude" / "CLAUDE.md"

    plugin_version: str | None = None
    claude_md_version: str | None = None

    if plugin_json_path.is_file():
        try:
            data = json.loads(_read_text(plugin_json_path))
            plugin_version = data.get("version")
        except json.JSONDecodeError:
            pass

    if claude_md_path.is_file():
        text = _read_text(claude_md_path)
        m = re.search(r"\*\*Version\*\*:\s*(\S+)", text)
        if m:
            claude_md_version = m.group(1)

    if plugin_version is None:
        cat.add(
            "plugin.json version", "FAIL", "Could not read version from plugin.json"
        )
    else:
        cat.add("plugin.json version", "PASS", f"v{plugin_version}")

    if claude_md_version is None:
        cat.add(
            "CLAUDE.md version", "FAIL", "Could not read version from .claude/CLAUDE.md"
        )
    else:
        cat.add("CLAUDE.md version", "PASS", f"v{claude_md_version}")

    if plugin_version and claude_md_version:
        if plugin_version == claude_md_version:
            cat.add(
                "version match",
                "PASS",
                f"Both report v{plugin_version}",
            )
        else:
            cat.add(
                "version match",
                "FAIL",
                f"plugin.json={plugin_version} vs CLAUDE.md={claude_md_version}",
            )

    return cat


def check_documentation_health(root: Path, verbose: bool) -> CategoryResult:
    """7. Documentation Health — README, CONTRIBUTING, CLAUDE.md, CHANGELOG."""
    cat = CategoryResult(name="Documentation Health")

    for rel_path in DOC_FILES:
        full_path = root / rel_path
        if full_path.is_file():
            size = full_path.stat().st_size
            if size > 0:
                cat.add(rel_path, "PASS", f"Present ({size:,} bytes)")
            else:
                cat.add(rel_path, "WARN", "File exists but is empty")
        else:
            cat.add(rel_path, "FAIL", f"Missing: {full_path}")

    return cat


# ---------------------------------------------------------------------------
# Report
# ---------------------------------------------------------------------------

# ANSI color codes (gracefully degrade on terminals that don't support them)
_COLOR_RESET = "\033[0m"
_COLOR_GREEN = "\033[32m"
_COLOR_YELLOW = "\033[33m"
_COLOR_RED = "\033[31m"
_COLOR_BOLD = "\033[1m"
_COLOR_DIM = "\033[2m"

_STATUS_COLORS: dict[Status, str] = {
    "PASS": _COLOR_GREEN,
    "WARN": _COLOR_YELLOW,
    "FAIL": _COLOR_RED,
}


def _supports_color() -> bool:
    """Heuristic: does the terminal likely support ANSI colors?"""
    if os.environ.get("NO_COLOR"):
        return False
    if os.environ.get("FORCE_COLOR"):
        return True
    return hasattr(sys.stdout, "isatty") and sys.stdout.isatty()


def _colorize(text: str, color: str, use_color: bool) -> str:
    if use_color:
        return f"{color}{text}{_COLOR_RESET}"
    return text


def _status_badge(status: Status, use_color: bool) -> str:
    color = _STATUS_COLORS.get(status, "")
    return _colorize(f"[{status}]", color, use_color)


def print_report(categories: list[CategoryResult], verbose: bool) -> None:
    """Print the full validation report."""
    use_color = _supports_color()

    print()
    print(_colorize("=" * 70, _COLOR_BOLD, use_color))
    print(
        _colorize(
            "  Academic Research Skills — Plugin Self-Test Report",
            _COLOR_BOLD,
            use_color,
        )
    )
    print(_colorize("=" * 70, _COLOR_BOLD, use_color))
    print()

    total_pass = 0
    total_warn = 0
    total_fail = 0

    for cat in categories:
        pass_count = sum(1 for c in cat.checks if c.status == "PASS")
        warn_count = sum(1 for c in cat.checks if c.status == "WARN")
        fail_count = sum(1 for c in cat.checks if c.status == "FAIL")

        total_pass += pass_count
        total_warn += warn_count
        total_fail += fail_count

        badge = _status_badge(cat.status, use_color)
        header = f"{badge} {cat.name}"
        summary = f"  ({pass_count} pass, {warn_count} warn, {fail_count} fail)"
        print(f"{header}{_colorize(summary, _COLOR_DIM, use_color)}")

        if verbose:
            for check in cat.checks:
                cbadge = _status_badge(check.status, use_color)
                print(f"    {cbadge} {check.name}")
                if check.message:
                    print(f"         {_colorize(check.message, _COLOR_DIM, use_color)}")
            print()

    # Summary
    print()
    print(_colorize("-" * 70, _COLOR_BOLD, use_color))
    total = total_pass + total_warn + total_fail
    print(f"  Total checks: {total}")
    print(f"    {_colorize(f'PASS: {total_pass}', _COLOR_GREEN, use_color)}")
    print(f"    {_colorize(f'WARN: {total_warn}', _COLOR_YELLOW, use_color)}")
    print(f"    {_colorize(f'FAIL: {total_fail}', _COLOR_RED, use_color)}")
    print(_colorize("-" * 70, _COLOR_BOLD, use_color))

    if total_fail > 0:
        print(
            _colorize(
                "\n  RESULT: FAIL — structural issues detected\n",
                _COLOR_RED,
                use_color,
            )
        )
    elif total_warn > 0:
        print(
            _colorize(
                "\n  RESULT: PASS (with warnings)\n",
                _COLOR_YELLOW,
                use_color,
            )
        )
    else:
        print(
            _colorize(
                "\n  RESULT: ALL PASS\n",
                _COLOR_GREEN,
                use_color,
            )
        )


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def find_repo_root() -> Path:
    """Locate the repository root by walking up from this script's location.

    Looks for the .claude-plugin/plugin.json marker file.
    """
    candidate = Path(__file__).resolve().parent.parent
    if (candidate / ".claude-plugin" / "plugin.json").is_file():
        return candidate

    # Fallback: walk up from cwd
    candidate = Path.cwd()
    for _ in range(10):
        if (candidate / ".claude-plugin" / "plugin.json").is_file():
            return candidate
        parent = candidate.parent
        if parent == candidate:
            break
        candidate = parent

    # Last resort: assume parent of tools/
    return Path(__file__).resolve().parent.parent


def main() -> int:
    """Run all validation checks and print the report.

    Returns:
        0 if all checks pass (warnings allowed), 1 if any check fails.
    """
    parser = argparse.ArgumentParser(
        description="Validate structural integrity of the academic-research-skills plugin.",
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Show detailed per-check output",
    )
    args = parser.parse_args()

    root = find_repo_root()

    categories = [
        check_plugin_structure(root, args.verbose),
        check_agent_completeness(root, args.verbose),
        check_shared_infrastructure(root, args.verbose),
        check_cross_reference_integrity(root, args.verbose),
        check_template_reference_coverage(root, args.verbose),
        check_version_consistency(root, args.verbose),
        check_documentation_health(root, args.verbose),
    ]

    print_report(categories, args.verbose)

    has_failures = any(c.status == "FAIL" for c in categories)
    return 1 if has_failures else 0


if __name__ == "__main__":
    sys.exit(main())
