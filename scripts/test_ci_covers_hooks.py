"""CI must run pytest when hooks/ changes — scripts/test_run_guard_launcher.py
tests hooks/run_guard.sh, so an uncovered hooks/ path means the guard's own
tests never gate its changes."""

import pathlib
import re

WORKFLOW = pathlib.Path(__file__).resolve().parents[1] / ".github" / "workflows" / "pytest.yml"


def _path_blocks(text: str) -> list[list[str]]:
    """Return each `paths:` list in the workflow as a list of glob strings."""
    blocks, current = [], None
    for line in text.splitlines():
        if re.match(r"^\s*paths:\s*$", line):
            current = []
            blocks.append(current)
            continue
        m = re.match(r"^\s*-\s*'([^']+)'\s*$", line)
        if m and current is not None:
            current.append(m.group(1))
        elif current is not None and line.strip() and not line.strip().startswith("-"):
            current = None
    return blocks


def test_every_paths_block_covers_hooks() -> None:
    blocks = _path_blocks(WORKFLOW.read_text(encoding="utf-8"))
    assert blocks, "no paths: blocks found — workflow shape changed"
    missing = [i for i, b in enumerate(blocks) if not any(g.startswith("hooks/") for g in b)]
    assert not missing, (
        f"paths block(s) {missing} do not trigger on hooks/**; "
        f"editing hooks/run_guard.sh would run no tests in CI"
    )
