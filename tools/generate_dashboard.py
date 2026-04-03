"""Generate a populated pipeline dashboard HTML from a JSON state file.

Usage:
    # Generate a blank state JSON template:
    uv run tools/generate_dashboard.py --init

    # Generate dashboard from an existing state file:
    uv run tools/generate_dashboard.py state.json

    # Specify a custom output path:
    uv run tools/generate_dashboard.py state.json -o custom_output.html

The HTML template is read from tools/templates/pipeline_dashboard.html and
the PIPELINE_STATE JSON block is replaced with the provided state data.
Output defaults to experiment_outputs/reports/pipeline_dashboard.html.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

# Resolve paths relative to this script's location (tools/ directory).
TOOLS_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = TOOLS_DIR.parent
TEMPLATE_PATH = TOOLS_DIR / "templates" / "pipeline_dashboard.html"
DEFAULT_OUTPUT_DIR = PROJECT_ROOT / "experiment_outputs" / "reports"
DEFAULT_OUTPUT_PATH = DEFAULT_OUTPUT_DIR / "pipeline_dashboard.html"
DEFAULT_STATE_PATH = PROJECT_ROOT / "experiment_outputs" / "pipeline_state.json"


def blank_state() -> dict:
    """Return a blank pipeline state with all stages pending."""
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    return {
        "meta": {
            "topic": "",
            "pipeline_version": "2.7",
            "last_updated": now,
            "session_id": "",
        },
        "stages": [
            {
                "id": "1",
                "label": "Research",
                "skill": "deep-research",
                "status": "pending",
                "mode": "",
                "completed_at": "",
            },
            {
                "id": "1.5",
                "label": "Experiment",
                "skill": "experiment-designer / data-analyst / simulation-runner / lab-notebook",
                "status": "pending",
                "mode": "",
                "completed_at": "",
                "optional": True,
                "sub_stages": [
                    {
                        "id": "1.5a",
                        "label": "Design",
                        "skill": "experiment-designer",
                        "status": "pending",
                        "completed_at": "",
                    },
                    {
                        "id": "1.5b",
                        "label": "Execute",
                        "skill": "data-analyst / simulation-runner",
                        "status": "pending",
                        "completed_at": "",
                    },
                    {
                        "id": "1.5c",
                        "label": "Log",
                        "skill": "lab-notebook",
                        "status": "pending",
                        "completed_at": "",
                    },
                ],
            },
            {
                "id": "2",
                "label": "Write",
                "skill": "academic-paper",
                "status": "pending",
                "mode": "",
                "completed_at": "",
            },
            {
                "id": "2.5",
                "label": "Integrity (Pre-Review)",
                "skill": "integrity-verification",
                "status": "pending",
                "mode": "pre-review",
                "completed_at": "",
            },
            {
                "id": "3",
                "label": "Peer Review",
                "skill": "academic-paper-reviewer",
                "status": "pending",
                "mode": "",
                "completed_at": "",
            },
            {
                "id": "4",
                "label": "Revision",
                "skill": "academic-paper (revision)",
                "status": "pending",
                "mode": "revision",
                "completed_at": "",
            },
            {
                "id": "3p",
                "label": "Re-Review",
                "skill": "academic-paper-reviewer (re-review)",
                "status": "pending",
                "mode": "re-review",
                "completed_at": "",
            },
            {
                "id": "4p",
                "label": "Re-Revision",
                "skill": "academic-paper (re-revision)",
                "status": "pending",
                "mode": "re-revision",
                "completed_at": "",
            },
            {
                "id": "4.5",
                "label": "Integrity (Final)",
                "skill": "integrity-verification",
                "status": "pending",
                "mode": "final-check",
                "completed_at": "",
            },
            {
                "id": "5",
                "label": "Format & Finalize",
                "skill": "academic-paper (format-convert)",
                "status": "pending",
                "mode": "",
                "completed_at": "",
            },
        ],
        "schemas": [
            {
                "id": 1,
                "name": "RQ Brief",
                "producer": "deep-research",
                "consumer": "academic-paper",
                "status": "not_produced",
            },
            {
                "id": 2,
                "name": "Bibliography",
                "producer": "deep-research",
                "consumer": "academic-paper",
                "status": "not_produced",
            },
            {
                "id": 3,
                "name": "Synthesis Report",
                "producer": "deep-research",
                "consumer": "academic-paper",
                "status": "not_produced",
            },
            {
                "id": 4,
                "name": "Paper Draft",
                "producer": "academic-paper",
                "consumer": "integrity / reviewer",
                "status": "not_produced",
            },
            {
                "id": 5,
                "name": "Integrity Report",
                "producer": "integrity-verification",
                "consumer": "pipeline / academic-paper",
                "status": "not_produced",
            },
            {
                "id": 6,
                "name": "Review Report",
                "producer": "academic-paper-reviewer",
                "consumer": "pipeline / academic-paper",
                "status": "not_produced",
            },
            {
                "id": 7,
                "name": "Revision Roadmap",
                "producer": "academic-paper-reviewer",
                "consumer": "academic-paper (revision)",
                "status": "not_produced",
            },
            {
                "id": 8,
                "name": "Response to Reviewers",
                "producer": "academic-paper (revision)",
                "consumer": "academic-paper-reviewer (re-review)",
                "status": "not_produced",
            },
            {
                "id": 9,
                "name": "Material Passport",
                "producer": "(cross-stage)",
                "consumer": "(cross-stage)",
                "status": "not_produced",
            },
            {
                "id": 10,
                "name": "Experiment Design",
                "producer": "experiment-designer",
                "consumer": "data-analyst / simulation-runner",
                "status": "not_produced",
            },
            {
                "id": 11,
                "name": "Experiment Results",
                "producer": "data-analyst / sim-runner",
                "consumer": "academic-paper / lab-notebook",
                "status": "not_produced",
            },
            {
                "id": 12,
                "name": "Lab Record",
                "producer": "lab-notebook",
                "consumer": "academic-paper / pipeline",
                "status": "not_produced",
            },
            {
                "id": 13,
                "name": "Simulation Specification",
                "producer": "experiment-designer",
                "consumer": "simulation-runner",
                "status": "not_produced",
            },
            {
                "id": 14,
                "name": "Methodology Blueprint",
                "producer": "deep-research",
                "consumer": "pipeline / experiment-designer",
                "status": "not_produced",
            },
            {
                "id": 15,
                "name": "INSIGHT Collection",
                "producer": "deep-research (socratic)",
                "consumer": "deep-research / academic-paper",
                "status": "not_produced",
            },
            {
                "id": 16,
                "name": "Concept Lineage Report",
                "producer": "deep-research",
                "consumer": "academic-paper",
                "status": "not_produced",
            },
            {
                "id": 17,
                "name": "Style Profile",
                "producer": "academic-paper (intake)",
                "consumer": "academic-paper (draft_writer / report_compiler)",
                "status": "not_produced",
            },
        ],
        "passports": [
            {
                "schema_id": 1,
                "name": "RQ Brief",
                "version": "",
                "verification_status": "",
                "upstream": [],
            },
            {
                "schema_id": 2,
                "name": "Bibliography",
                "version": "",
                "verification_status": "",
                "upstream": [1],
            },
            {
                "schema_id": 3,
                "name": "Synthesis Report",
                "version": "",
                "verification_status": "",
                "upstream": [1, 2],
            },
            {
                "schema_id": 14,
                "name": "Methodology Blueprint",
                "version": "",
                "verification_status": "",
                "upstream": [1],
            },
            {
                "schema_id": 15,
                "name": "INSIGHT Collection",
                "version": "",
                "verification_status": "",
                "upstream": [],
            },
            {
                "schema_id": 10,
                "name": "Experiment Design",
                "version": "",
                "verification_status": "",
                "upstream": [14],
            },
            {
                "schema_id": 13,
                "name": "Simulation Spec",
                "version": "",
                "verification_status": "",
                "upstream": [10],
            },
            {
                "schema_id": 11,
                "name": "Experiment Results",
                "version": "",
                "verification_status": "",
                "upstream": [10],
            },
            {
                "schema_id": 12,
                "name": "Lab Record",
                "version": "",
                "verification_status": "",
                "upstream": [10, 11],
            },
            {
                "schema_id": 4,
                "name": "Paper Draft",
                "version": "",
                "verification_status": "",
                "upstream": [1, 2, 3, 14],
            },
            {
                "schema_id": 5,
                "name": "Integrity Report",
                "version": "",
                "verification_status": "",
                "upstream": [4],
            },
            {
                "schema_id": 6,
                "name": "Review Report",
                "version": "",
                "verification_status": "",
                "upstream": [4],
            },
            {
                "schema_id": 7,
                "name": "Revision Roadmap",
                "version": "",
                "verification_status": "",
                "upstream": [6],
            },
            {
                "schema_id": 8,
                "name": "Response to Reviewers",
                "version": "",
                "verification_status": "",
                "upstream": [4, 7],
            },
            {
                "schema_id": 9,
                "name": "Material Passport",
                "version": "",
                "verification_status": "",
                "upstream": [],
            },
        ],
        "integrity": {
            "pre_review": {
                "verdict": "pending",
                "issues": {"serious": 0, "medium": 0, "minor": 0},
                "citation_integrity_score": None,
                "fabrication_risk_score": None,
                "timestamp": "",
            },
            "final_check": {
                "verdict": "pending",
                "issues": {"serious": 0, "medium": 0, "minor": 0},
                "citation_integrity_score": None,
                "fabrication_risk_score": None,
                "timestamp": "",
            },
        },
    }


def inject_state(template_html: str, state: dict) -> str:
    """Replace the PIPELINE_STATE JSON block in the template with new data.

    The template contains a `var PIPELINE_STATE = { ... };` block. This
    function locates it via regex and replaces the JSON object with the
    serialized state, preserving the surrounding JavaScript syntax.
    """
    state_json = json.dumps(state, indent=2, ensure_ascii=False)

    # Match the var PIPELINE_STATE = { ... }; block.
    # The pattern captures everything between `var PIPELINE_STATE = ` and the
    # closing `};` that sits on its own line (allowing for nested braces).
    pattern = r"(var PIPELINE_STATE\s*=\s*)(\{[\s\S]*?\});"

    match = re.search(pattern, template_html)
    if match is None:
        msg = (
            "Could not find 'var PIPELINE_STATE = {...};' block in the HTML template. "
            "Ensure the template at %s contains this marker."
        )
        raise ValueError(msg % TEMPLATE_PATH)

    replaced = (
        template_html[: match.start()]
        + match.group(1)
        + state_json
        + ";"
        + template_html[match.end() :]
    )
    return replaced


def load_state(state_path: Path) -> dict:
    """Load and validate a pipeline state JSON file."""
    if not state_path.exists():
        print(f"Error: state file not found: {state_path}", file=sys.stderr)
        sys.exit(1)

    with state_path.open("r", encoding="utf-8") as f:
        try:
            state = json.load(f)
        except json.JSONDecodeError as e:
            print(f"Error: invalid JSON in {state_path}: {e}", file=sys.stderr)
            sys.exit(1)

    # Basic structural validation
    required_keys = {"meta", "stages", "schemas", "passports", "integrity"}
    missing = required_keys - set(state.keys())
    if missing:
        print(
            f"Warning: state file is missing top-level keys: {', '.join(sorted(missing))}. "
            "Dashboard may render with defaults.",
            file=sys.stderr,
        )

    return state


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate an interactive pipeline dashboard HTML from a JSON state file.",
        epilog="Use --init to create a blank pipeline_state.json template.",
    )
    parser.add_argument(
        "state_file",
        nargs="?",
        type=Path,
        help="Path to the pipeline state JSON file. Omit when using --init.",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT_PATH,
        help=f"Output HTML path (default: {DEFAULT_OUTPUT_PATH.relative_to(PROJECT_ROOT)})",
    )
    parser.add_argument(
        "--init",
        action="store_true",
        help="Generate a blank pipeline_state.json template and exit.",
    )
    parser.add_argument(
        "--init-path",
        type=Path,
        default=DEFAULT_STATE_PATH,
        help=f"Path for the blank state file (default: {DEFAULT_STATE_PATH.relative_to(PROJECT_ROOT)})",
    )
    parser.add_argument(
        "-t",
        "--template",
        type=Path,
        default=TEMPLATE_PATH,
        help=f"Path to the HTML template (default: {TEMPLATE_PATH.relative_to(PROJECT_ROOT)})",
    )

    args = parser.parse_args()

    # --init: generate blank state JSON
    if args.init:
        init_path: Path = args.init_path
        init_path.parent.mkdir(parents=True, exist_ok=True)
        state = blank_state()
        with init_path.open("w", encoding="utf-8") as f:
            json.dump(state, f, indent=2, ensure_ascii=False)
        print(f"Blank pipeline state written to: {init_path}")

        # Also generate the dashboard HTML with the blank state
        template_path: Path = args.template
        if not template_path.exists():
            print(
                f"Warning: template not found at {template_path}, skipping HTML generation.",
                file=sys.stderr,
            )
            return

        template_html = template_path.read_text(encoding="utf-8")
        populated_html = inject_state(template_html, state)

        output_path: Path = args.output
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(populated_html, encoding="utf-8")
        print(f"Blank dashboard written to: {output_path}")
        return

    # Normal mode: require a state file
    if args.state_file is None:
        parser.error(
            "A state_file is required (or use --init to generate a blank template)."
        )

    state = load_state(args.state_file)

    # Update last_updated timestamp
    if "meta" not in state:
        state["meta"] = {}
    state["meta"]["last_updated"] = datetime.now(timezone.utc).isoformat(
        timespec="seconds"
    )

    # Read the template
    template_path = args.template
    if not template_path.exists():
        print(f"Error: HTML template not found at {template_path}", file=sys.stderr)
        sys.exit(1)

    template_html = template_path.read_text(encoding="utf-8")

    # Inject state and write output
    populated_html = inject_state(template_html, state)

    output_path: Path = args.output
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(populated_html, encoding="utf-8")
    print(f"Dashboard generated: {output_path}")


if __name__ == "__main__":
    main()
