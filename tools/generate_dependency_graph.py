#!/usr/bin/env python3
"""Generate a Mermaid dependency graph for the academic-research-skills repository.

Parses SKILL.md files, agent definitions, and handoff_schemas.md to produce
a Mermaid flowchart showing agent-to-agent and schema-based data flow across
all eight skills.

Usage:
    python generate_dependency_graph.py                    # print Mermaid to stdout
    python generate_dependency_graph.py --output file      # write to docs/dependency_graph.mmd
    python generate_dependency_graph.py --output png       # write .mmd + note about mcp__mermaid
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

REPO_ROOT = Path(__file__).resolve().parent.parent

SKILL_DIRS = [
    "deep-research",
    "experiment-designer",
    "data-analyst",
    "simulation-runner",
    "lab-notebook",
    "academic-paper",
    "academic-paper-reviewer",
    "academic-pipeline",
]

SKILL_COLORS = {
    "deep-research": "#4A90D9",
    "experiment-designer": "#F5A623",
    "data-analyst": "#2ECC71",
    "simulation-runner": "#9B59B6",
    "lab-notebook": "#E67E22",
    "academic-paper": "#3498DB",
    "academic-paper-reviewer": "#E74C3C",
    "academic-pipeline": "#1ABC9C",
}

# Maps skill-dir name to a short prefix used for Mermaid node IDs.
SKILL_PREFIX = {
    "deep-research": "dr",
    "experiment-designer": "ed",
    "data-analyst": "da",
    "simulation-runner": "sr",
    "lab-notebook": "ln",
    "academic-paper": "ap",
    "academic-paper-reviewer": "apr",
    "academic-pipeline": "apl",
}

# Human-friendly labels for subgraphs.
SKILL_LABEL = {
    "deep-research": "Deep Research",
    "experiment-designer": "Experiment Designer",
    "data-analyst": "Data Analyst",
    "simulation-runner": "Simulation Runner",
    "lab-notebook": "Lab Notebook",
    "academic-paper": "Academic Paper",
    "academic-paper-reviewer": "Academic Paper Reviewer",
    "academic-pipeline": "Academic Pipeline",
}


# ---------------------------------------------------------------------------
# Parsing helpers
# ---------------------------------------------------------------------------


def _node_id(skill: str, agent: str) -> str:
    """Return a Mermaid-safe node ID for an agent."""
    prefix = SKILL_PREFIX[skill]
    # Strip _agent suffix to keep IDs shorter.
    short = agent.replace("_agent", "")
    return f"{prefix}_{short}"


def _human_label(agent: str) -> str:
    """Turn an agent filename stem into a readable label."""
    return agent.replace("_agent", "").replace("_", " ").title()


def parse_agents_from_skill_md(skill_dir: str) -> list[str]:
    """Extract agent names from the Agent Team table in SKILL.md.

    Looks for back-ticked agent names like `research_question_agent` in the
    markdown table rows under the '## Agent Team' heading.
    """
    skill_path = REPO_ROOT / skill_dir / "SKILL.md"
    if not skill_path.exists():
        return []

    text = skill_path.read_text(encoding="utf-8")
    agents: list[str] = []

    # Match back-ticked agent names inside table rows.
    # The SKILL.md tables have rows like:
    #   | 1 | `research_question_agent` | ... |
    for m in re.finditer(r"\|\s*`(\w+_agent)`\s*\|", text):
        agent_name = m.group(1)
        if agent_name not in agents:
            agents.append(agent_name)

    return agents


def discover_agent_files(skill_dir: str) -> list[Path]:
    """List all .md files under <skill_dir>/agents/."""
    agents_dir = REPO_ROOT / skill_dir / "agents"
    if not agents_dir.is_dir():
        return []
    return sorted(agents_dir.glob("*.md"))


def parse_schema_references(text: str) -> list[int]:
    """Find all 'Schema N' references in *text*."""
    return sorted(set(int(m.group(1)) for m in re.finditer(r"Schema\s+(\d+)", text)))


def parse_agent_cross_references(
    text: str, all_agents: set[str], own_skill: str
) -> list[tuple[str, str]]:
    """Find mentions of agents from *other* skills.

    Returns a list of (target_skill, target_agent) pairs.
    """
    refs: list[tuple[str, str]] = []
    # Match back-ticked or bare agent names like `draft_writer_agent` or
    # path-style references like academic-paper/draft_writer_agent.
    for m in re.finditer(r"(?:`?(\w[\w-]*)/)?\b(\w+_agent)\b`?", text):
        skill_hint = m.group(1)  # may be None
        agent_name = m.group(2)
        if agent_name not in all_agents:
            continue
        if skill_hint and skill_hint != own_skill:
            refs.append((skill_hint, agent_name))
    return refs


# ---------------------------------------------------------------------------
# Schema handoff parsing
# ---------------------------------------------------------------------------

_SCHEMA_HEADER_RE = re.compile(
    r"^##\s+Schema\s+(\d+):\s+(.+?)(?:\s+\(.*\))?\s*$", re.MULTILINE
)

_PRODUCER_RE = re.compile(r"\*\*Producer\*\*:\s*(.+)", re.MULTILINE)

_CONSUMER_RE = re.compile(r"\*\*Consumer\*\*:\s*(.+)", re.MULTILINE)


def _parse_agent_refs(line: str) -> list[tuple[str, str]]:
    """Parse 'skill/agent | skill/agent' references from a Producer/Consumer line.

    Examples:
        `deep-research/research_question_agent` | `deep-research/socratic_mentor_agent`
        `academic-paper/draft_writer_agent`
        `academic-paper-reviewer/*`
    """
    results: list[tuple[str, str]] = []
    # Match back-ticked path-style references.
    for m in re.finditer(r"`([\w-]+)/([\w*]+_?[\w*]*)`", line):
        skill = m.group(1)
        agent = m.group(2)
        if agent == "*":
            # Wildcard — represents all agents in that skill.  We record it
            # with a sentinel so the caller can expand later.
            results.append((skill, "*"))
        else:
            results.append((skill, agent))
    return results


def parse_handoff_schemas(
    schemas_path: Path,
) -> list[dict]:
    """Parse shared/handoff_schemas.md and return schema transfer records.

    Each record is:
        {
            "schema_id": int,
            "schema_name": str,
            "producers": [(skill, agent), ...],
            "consumers": [(skill, agent), ...],
        }
    """
    if not schemas_path.exists():
        return []

    text = schemas_path.read_text(encoding="utf-8")
    records: list[dict] = []

    # Split text into schema sections.
    headers = list(_SCHEMA_HEADER_RE.finditer(text))
    for i, hdr in enumerate(headers):
        start = hdr.end()
        end = headers[i + 1].start() if i + 1 < len(headers) else len(text)
        section = text[start:end]

        schema_id = int(hdr.group(1))
        schema_name = hdr.group(2).strip()

        producers: list[tuple[str, str]] = []
        consumers: list[tuple[str, str]] = []

        pm = _PRODUCER_RE.search(section)
        if pm:
            producers = _parse_agent_refs(pm.group(1))

        cm = _CONSUMER_RE.search(section)
        if cm:
            consumers = _parse_agent_refs(cm.group(1))

        records.append(
            {
                "schema_id": schema_id,
                "schema_name": schema_name,
                "producers": producers,
                "consumers": consumers,
            }
        )

    return records


# ---------------------------------------------------------------------------
# Graph assembly
# ---------------------------------------------------------------------------


def build_graph() -> str:
    """Build the complete Mermaid flowchart definition."""

    # 1. Discover all agents per skill.
    skill_agents: dict[str, list[str]] = {}
    all_agent_set: set[str] = set()
    agent_to_skill: dict[str, str] = {}

    for skill in SKILL_DIRS:
        agents_from_md = parse_agents_from_skill_md(skill)
        # Also discover agent files for any not listed in SKILL.md.
        agent_files = discover_agent_files(skill)
        file_agents = [p.stem for p in agent_files]

        # Merge: prefer the SKILL.md ordering, then add any file-only agents.
        combined: list[str] = list(agents_from_md)
        for fa in file_agents:
            if fa not in combined:
                combined.append(fa)

        skill_agents[skill] = combined
        for a in combined:
            all_agent_set.add(a)
            agent_to_skill[a] = skill

    # 2. Parse handoff schemas.
    schemas = parse_handoff_schemas(REPO_ROOT / "shared" / "handoff_schemas.md")

    # Expand wildcard consumers/producers.
    for rec in schemas:
        for role in ("producers", "consumers"):
            expanded: list[tuple[str, str]] = []
            for skill, agent in rec[role]:
                if agent == "*":
                    expanded.extend((skill, a) for a in skill_agents.get(skill, []))
                else:
                    expanded.append((skill, agent))
            rec[role] = expanded

    # 3. Parse cross-references from agent files.
    cross_refs: list[tuple[str, str, str, str]] = []
    for skill in SKILL_DIRS:
        for agent_path in discover_agent_files(skill):
            agent_name = agent_path.stem
            text = agent_path.read_text(encoding="utf-8")
            refs = parse_agent_cross_references(text, all_agent_set, skill)
            for target_skill, target_agent in refs:
                if target_skill in SKILL_PREFIX:
                    cross_refs.append((skill, agent_name, target_skill, target_agent))

    # 4. Build Mermaid output.
    lines: list[str] = []
    lines.append("flowchart TD")
    lines.append("")

    # -- Subgraphs with agents ---
    for skill in SKILL_DIRS:
        prefix = SKILL_PREFIX[skill]
        label = SKILL_LABEL[skill]
        lines.append(f'    subgraph {prefix}_sub["{label}"]')
        lines.append(
            f"        style {prefix}_sub fill:{SKILL_COLORS[skill]},fill-opacity:0.15,stroke:{SKILL_COLORS[skill]},stroke-width:2px"
        )
        for agent in skill_agents.get(skill, []):
            nid = _node_id(skill, agent)
            nlabel = _human_label(agent)
            lines.append(f'        {nid}["{nlabel}"]')
        lines.append("    end")
        lines.append("")

    # -- Schema-based edges ---
    lines.append("    %% Schema handoff edges")
    # To avoid duplicate edges, track emitted edges.
    emitted_edges: set[str] = set()

    for rec in schemas:
        schema_id = rec["schema_id"]

        for p_skill, p_agent in rec["producers"]:
            if p_skill not in SKILL_PREFIX:
                continue
            if p_agent not in skill_agents.get(p_skill, []):
                continue
            src = _node_id(p_skill, p_agent)

            for c_skill, c_agent in rec["consumers"]:
                if c_skill not in SKILL_PREFIX:
                    continue
                if c_agent not in skill_agents.get(c_skill, []):
                    continue
                dst = _node_id(c_skill, c_agent)
                if src == dst:
                    continue

                edge_key = f"{src}-->{dst}:{schema_id}"
                if edge_key in emitted_edges:
                    continue
                emitted_edges.add(edge_key)

                lines.append(f'    {src} -->|"S{schema_id}"| {dst}')

    lines.append("")

    # -- Cross-reference edges (agent mentions other agents) ---
    lines.append("    %% Cross-agent collaboration edges")
    for src_skill, src_agent, tgt_skill, tgt_agent in cross_refs:
        if src_skill not in SKILL_PREFIX or tgt_skill not in SKILL_PREFIX:
            continue
        if src_agent not in skill_agents.get(src_skill, []):
            continue
        if tgt_agent not in skill_agents.get(tgt_skill, []):
            continue
        src = _node_id(src_skill, src_agent)
        dst = _node_id(tgt_skill, tgt_agent)
        if src == dst:
            continue
        edge_key = f"{src}-..->{dst}"
        if edge_key in emitted_edges:
            continue
        emitted_edges.add(edge_key)
        lines.append(f"    {src} -.-> {dst}")

    lines.append("")

    # -- Node styling ---
    lines.append("    %% Node styles")
    for skill in SKILL_DIRS:
        color = SKILL_COLORS[skill]
        for agent in skill_agents.get(skill, []):
            nid = _node_id(skill, agent)
            lines.append(
                f"    style {nid} fill:{color},fill-opacity:0.3,stroke:{color},color:#000"
            )

    lines.append("")

    # -- Legend ---
    lines.append("    %% Legend")
    lines.append('    subgraph legend["Legend"]')
    lines.append("        direction LR")
    lines.append('        leg_schema["Solid arrow = Schema handoff"]')
    lines.append('        leg_collab["Dashed arrow = Agent collaboration"]')
    lines.append("        leg_schema ~~~ leg_collab")
    lines.append("    end")
    lines.append("    style legend fill:#f9f9f9,stroke:#ccc,stroke-width:1px")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Statistics summary
# ---------------------------------------------------------------------------


def print_summary() -> None:
    """Print a brief summary of what was parsed to stderr."""
    total_agents = 0
    for skill in SKILL_DIRS:
        agents = parse_agents_from_skill_md(skill)
        agent_files = discover_agent_files(skill)
        combined = set(agents) | {p.stem for p in agent_files}
        count = len(combined)
        total_agents += count
        print(f"  {skill}: {count} agents", file=sys.stderr)

    schemas = parse_handoff_schemas(REPO_ROOT / "shared" / "handoff_schemas.md")
    print(f"  Schemas parsed: {len(schemas)}", file=sys.stderr)
    print(f"  Total agents: {total_agents}", file=sys.stderr)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate a Mermaid dependency graph for academic-research-skills."
    )
    parser.add_argument(
        "--output",
        choices=["mermaid", "file", "png"],
        default="mermaid",
        help="Output mode: mermaid (stdout), file (docs/dependency_graph.mmd), png (file + note).",
    )
    args = parser.parse_args()

    print("Parsing repository...", file=sys.stderr)
    print_summary()

    mermaid_code = build_graph()

    if args.output == "mermaid":
        print(mermaid_code)

    elif args.output in ("file", "png"):
        out_dir = REPO_ROOT / "docs"
        out_dir.mkdir(exist_ok=True)
        out_path = out_dir / "dependency_graph.mmd"
        out_path.write_text(mermaid_code, encoding="utf-8")
        print(f"Written to {out_path}", file=sys.stderr)

        if args.output == "png":
            print(
                "NOTE: To render as PNG, use the Mermaid CLI (mmdc) or the "
                "mcp__mermaid__generate MCP tool with the .mmd file contents.",
                file=sys.stderr,
            )


if __name__ == "__main__":
    main()
