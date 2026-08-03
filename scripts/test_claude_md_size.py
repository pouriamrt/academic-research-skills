"""`.claude/CLAUDE.md` is always loaded when working in this repo. Release
history is derivable from CHANGELOG.md and git log, so it must not live here."""

import pathlib
import re

REPO = pathlib.Path(__file__).resolve().parents[1]
DOC = REPO / ".claude" / "CLAUDE.md"
MAX_CHARS = 16000


def test_file_is_within_budget() -> None:
    n = len(DOC.read_text(encoding="utf-8"))
    assert n <= MAX_CHARS, f".claude/CLAUDE.md is {n} chars (max {MAX_CHARS})"


def test_no_embedded_version_history() -> None:
    """Any heading that is a bare version-release header belongs in CHANGELOG.md.

    Exception: exactly ONE `## vX.Y[.Z] Key Additions` heading is REQUIRED by
    scripts/check_version_consistency.py invariant 11, which compares it against the
    suite version. It is a lint anchor, not changelog prose, so it is permitted here —
    but only one, and only in that exact form. The point of this test is to stop the
    ~19k chars of release narration that used to live in this file from creeping back.
    """
    text = DOC.read_text(encoding="utf-8")
    offenders = re.findall(r"^#{2,3} v\d+\.\d+.*$", text, re.M)
    key_additions = [h for h in offenders if re.match(r"^## v[\d.]+ Key Additions\s*$", h)]
    assert len(key_additions) <= 1, f"more than one Key Additions heading: {key_additions}"
    offenders = [h for h in offenders if h not in key_additions and h.strip() != "## Version Info"]
    assert not offenders, f"version-history headings still present: {offenders[:5]}"


def test_behavioural_sections_survive() -> None:
    text = DOC.read_text(encoding="utf-8")
    for required in (
        "## Routing Rules",
        "## Key Rules",
        "## Handoff Protocol",
        "## Full Academic Pipeline",
        "## Validation Tools",
        "## Optional MCP Capabilities",
        "## Skills Overview",
        "## Command model routing",
    ):
        assert required in text, f"deleted a behavioural section: {required}"


def test_changelog_pointer_present() -> None:
    assert "CHANGELOG.md" in DOC.read_text(encoding="utf-8")
