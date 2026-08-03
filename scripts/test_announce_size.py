"""The SessionStart announce is injected into EVERY session's context, in every
project. Its per-command description table duplicates the harness's own command
listing, so it is pure resident-context cost. Cap it."""
import pathlib
import re
import subprocess

REPO = pathlib.Path(__file__).resolve().parents[1]
SCRIPT = REPO / "scripts" / "announce-ars-loaded.sh"
MAX_CHARS = 700  # startup branch budget; compact/resume branch is 387

COMMANDS = sorted(p.stem for p in (REPO / "commands").glob("*.md"))


def _regions() -> list[str]:
    text = SCRIPT.read_text(encoding="utf-8")
    return re.findall(r'ANNOUNCE="([^"]*)"', text, re.S)


def test_every_announce_region_is_small() -> None:
    for i, region in enumerate(_regions()):
        assert len(region) <= MAX_CHARS, (
            f"ANNOUNCE region {i} is {len(region)} chars (max {MAX_CHARS}). "
            "It is injected into every session's context."
        )


def test_every_region_still_lists_every_command() -> None:
    """Mirrors the CI command-invariants rule so a size trim can't silently
    break the release-discipline lint."""
    for i, region in enumerate(_regions()):
        for name in COMMANDS:
            assert f"/{name}" in region, f"region {i} lost /{name}"


def test_count_literal_present_and_accurate() -> None:
    counts = re.findall(r"Slash commands \((\d+)\)", SCRIPT.read_text(encoding="utf-8"))
    assert counts, "count_pattern literal 'Slash commands (N)' vanished — CI lint fails"
    assert all(int(c) == len(COMMANDS) for c in counts), f"{counts} != {len(COMMANDS)}"


def test_still_emits_valid_hook_json() -> None:
    p = subprocess.run(["bash", "scripts/announce-ars-loaded.sh"], input="{}",
                       capture_output=True, text=True, cwd=REPO, timeout=60)
    assert p.returncode == 0, p.stderr
    import json
    d = json.loads(p.stdout)
    assert d["hookSpecificOutput"]["hookEventName"] == "SessionStart"
    assert d["hookSpecificOutput"]["additionalContext"]
