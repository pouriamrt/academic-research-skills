#!/usr/bin/env python3
"""Deterministic scan for mechanically detectable AI copy tells in prose.

Ported from `devibe_scan.py` in jcarterjohnson/vibecoded-design-tells (MIT),
via jensheitmann/humanizer-stack (MIT). Copyright notice retained per license;
see THIRD_PARTY.md "Upstream & related projects".

WHY THIS EXISTS: `academic-paper/references/writing_quality_check.md` already
carries the judgment rules (vocabulary precision, burstiness, paragraph rhythm),
but it ends with "Do NOT report scores to the user. Just fix the issues silently"
— an unverifiable self-report in a repo where every other invariant has a
runnable checker. This script covers the regex-addressable slice so the
checklist gains a receipt:

  copy-em-dash      em dash between words in visible copy
  copy-antithesis   "not just X, it's Y" / "not only X but Y"
  hype-copy         marketing-cliche vocabulary
  copy-servile      sycophantic openers and signposted wrap-ups

Cadence tells (uniform sentence rhythm, formulaic shape, polished-but-empty)
are NOT catchable here. Sections A-E of writing_quality_check.md own those, and
they still need a reader. Scanner output is evidence; the rest is judgment.

Pure stdlib; deterministic; read-only. Run from repo root:
    python3 scripts/check_prose_tells.py draft.md
    python3 scripts/check_prose_tells.py --json draft.md      # machine-readable
    python3 scripts/check_prose_tells.py --strict draft.md    # exit 1 on any hit
    python3 scripts/check_prose_tells.py --exclude-quotes draft.md
    cat draft.md | python3 scripts/check_prose_tells.py -

Mark a line with `copy-ignore` to suppress it (intentional usage).
"""

from __future__ import annotations

import argparse
import html as html_mod
import json
import re
import sys
from typing import Any

# The four rules are the license-relevant substance of the upstream port and are
# kept verbatim. Changing a pattern here changes what ARS claims to detect —
# update scripts/test_check_prose_tells.py in the same commit.
RULES: list[dict[str, Any]] = [
    {
        "id": "copy-em-dash",
        "label": "Em dash in copy (the #1 'AI wrote this' writing tell)",
        "fix": "Use a comma, a period, or parentheses. Not a colon; that gets flagged too.",
        "pats": [r"\w\s*—\s*\w", r"\w\s*&mdash;\s*\w"],
        # Skip code, code comments, and fenced blocks: not user-facing copy.
        # Also skip "**Term** — description" definition bullets: typographic
        # convention, not flowing copy. Flowing prose in bullets still flags.
        # ARS reference docs are dense with both, so dropping this suppression
        # buries real hits under table and bullet noise.
        "suppress": (
            r"^\s*(\*|//|/\*|<!--|#|>|\||```)"
            r"|`[^`]*—[^`]*`"
            r"|^\s*([-*+]\s+)?\*\*[^*]+\*\*\s*(—|&mdash;)"
        ),
    },
    {
        "id": "copy-antithesis",
        "label": "The \"it's not just X, it's Y\" sentence (the AI accent)",
        "fix": "State the thing plainly. Lead with the real claim and drop the negation.",
        "pats": [
            r"(it'?s |it |that'?s )?\bnot just\b[^.,;!?]{1,40},?\s*(it'?s|but)\b",
            r"\bnot only\b[^.,;!?]{1,40},?\s*but\b",
        ],
    },
    {
        "id": "hype-copy",
        "label": "AI marketing-copy cliche",
        "fix": "Write what the thing literally does, in plain words, with a checkable claim.",
        "pats": [
            r"\bTransform your\b",
            r"\bSupercharge\b",
            r"\bUnleash\b",
            r"\bEffortlessly\b",
            r"\breimagined\b",
            r"take (your |it |things )?[^.]{0,30}to the next level",
            r"\bGame-?changer\b",
            r"\bunlock (your |the )?(full )?potential\b",
            r"\b(deep[- ]dive|dive in|let'?s dive)\b",
            r"\bdelve\b",
            r"\belevate your\b",
            r"\bin today'?s (fast-paced|digital) world\b",
            r"\bworld-class\b",
            r"\bcutting-edge\b",
            r"\brevolutionary\b",
            r"\bbest-in-class\b",
        ],
    },
    {
        "id": "copy-servile",
        "label": "Sycophantic opener / signposted wrap-up",
        "fix": "Start on the real point and end on the real point. Cut the framing.",
        "pats": [
            r"\bGreat question\b",
            r"\bI hope this helps\b",
            r"\bIn conclusion\b",
            r"\bIn summary\b",
        ],
    },
]

TAG_RE = re.compile(r"<[^>]+>")

# A Markdown blockquote line. writing_quality_check.md section B already exempts
# quoted source material ("Direct quotes from sources retain their original
# punctuation"), so --exclude-quotes lets the scanner honour a rule the
# checklist states but upstream's line-oriented scan cannot see.
QUOTE_RE = re.compile(r"^\s*>")

# A fenced-code delimiter (``` or ~~~, optionally indented, optional info string).
# Upstream's suppression is line-oriented: it skips the delimiter line and any
# line that *starts* with a comment/heading marker, but not the code between the
# fences. ARS reference docs carry long fenced examples containing em dashes and
# prose fragments, and flagging those is how a linter earns being ignored — so
# this port tracks fence state and skips the block body for every rule.
FENCE_RE = re.compile(r"^\s*(```|~~~)")

JUDGMENT_REF = "academic-paper/references/writing_quality_check.md"

# Every report ends on the same caveat: a clean scan is not a good draft. One
# constant so the two exit paths cannot drift into saying different things.
CADENCE_NOTE = f"Cadence tells are not scannable by regex. See {JUDGMENT_REF} sections A-E."


def compile_rules() -> list[dict[str, Any]]:
    """Pre-compile every rule's patterns and optional suppression regex."""
    out: list[dict[str, Any]] = []
    for rule in RULES:
        out.append(
            {
                **rule,
                "re": [re.compile(p, re.I) for p in rule["pats"]],
                "suppress_re": (
                    re.compile(rule["suppress"], re.I) if rule.get("suppress") else None
                ),
            }
        )
    return out


def strip_html(text: str) -> str:
    """Drop script/style bodies and tags, then unescape entities."""
    text = re.sub(r"(?is)<(script|style)\b.*?</\1>", " ", text)
    return html_mod.unescape(TAG_RE.sub(" ", text))


def scan(
    text: str,
    rules: list[dict[str, Any]],
    path: str,
    *,
    exclude_quotes: bool = False,
) -> list[dict[str, Any]]:
    """Return one hit per (line, rule) match. At most one hit per rule per line.

    Fenced code blocks are skipped wholesale. An unterminated fence therefore
    swallows the rest of the file — under-reporting beats crying wolf on code —
    but silently returning zero hits would read as "clean" and pass `--strict`
    green, so that case warns on stderr naming the opening line.
    """
    hits: list[dict[str, Any]] = []
    in_fence = False
    fence_opened_at = 0
    for lineno, line in enumerate(text.splitlines(), 1):
        if FENCE_RE.match(line):
            in_fence = not in_fence
            fence_opened_at = lineno if in_fence else 0
            continue
        if in_fence:
            continue
        if "copy-ignore" in line:
            continue
        if exclude_quotes and QUOTE_RE.match(line):
            continue
        for rule in rules:
            if rule["suppress_re"] and rule["suppress_re"].search(line):
                continue
            for pat in rule["re"]:
                match = pat.search(line)
                if match:
                    hits.append(
                        {
                            "file": path,
                            "line": lineno,
                            "id": rule["id"],
                            "label": rule["label"],
                            "fix": rule["fix"],
                            "match": match.group(0).strip()[:80],
                            "text": line.strip()[:120],
                        }
                    )
                    break
    if in_fence:
        print(
            f"warning: {path}: unterminated code fence opened at line "
            f"{fence_opened_at}; everything after it was skipped",
            file=sys.stderr,
        )
    return hits


def read_source(path: str) -> tuple[str, str] | None:
    """Read one input. Returns (text, display_label), or None if unreadable."""
    if path == "-":
        return sys.stdin.read(), "<stdin>"
    try:
        with open(path, encoding="utf-8") as handle:
            return handle.read(), path
    except OSError as exc:
        print(f"skip {path}: {exc}", file=sys.stderr)
        return None


def render_report(all_hits: list[dict[str, Any]]) -> None:
    """Print the human-readable grouped report."""
    if not all_hits:
        print("clean: no mechanical copy tells found.")
        print(CADENCE_NOTE)
        return

    by_rule: dict[str, list[dict[str, Any]]] = {}
    for hit in all_hits:
        by_rule.setdefault(hit["id"], []).append(hit)

    for rule_id, hits in sorted(by_rule.items(), key=lambda kv: -len(kv[1])):
        print(f"\n{rule_id}  ({len(hits)} hit{'s' if len(hits) != 1 else ''})")
        print(f"  {hits[0]['label']}")
        print(f"  fix: {hits[0]['fix']}")
        for hit in hits[:12]:
            print(f"    {hit['file']}:{hit['line']}  [{hit['match']}]  {hit['text']}")
        if len(hits) > 12:
            print(f"    ... and {len(hits) - 12} more")

    print(f"\ntotal: {len(all_hits)} hits across {len(by_rule)} categories")
    print(CADENCE_NOTE)


def _force_utf8_streams() -> None:
    """Make stdout/stderr survive the characters this scanner exists to find.

    On Windows, stdout defaults to cp1252. Every reported hit echoes the offending
    source line, and the flagship rule matches an em dash — so the human-readable
    report reliably died with `UnicodeEncodeError: 'charmap' codec can't encode`
    and exited 1 on a NON-strict run, turning "found some tells" into "the tool
    is broken". `--json` masked it (json.dumps defaults to ensure_ascii=True).
    errors="replace" rather than a hard failure: a mangled glyph in a report line
    still points the reader at the right file:line.
    """
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if reconfigure is not None:  # absent when stdout is swapped for a plain object
            reconfigure(encoding="utf-8", errors="replace")


def main() -> int:
    _force_utf8_streams()
    parser = argparse.ArgumentParser(
        description="Scan prose for mechanically detectable AI copy tells.",
    )
    parser.add_argument("files", nargs="+", help="files to scan, or - for stdin")
    parser.add_argument("--html", action="store_true", help="strip HTML tags before scanning")
    parser.add_argument("--json", action="store_true", help="machine-readable output")
    parser.add_argument("--strict", action="store_true", help="exit 1 if any tell is found")
    parser.add_argument(
        "--exclude-quotes",
        action="store_true",
        help="skip Markdown blockquote lines (quoted sources are not the author's prose)",
    )
    args = parser.parse_args()

    rules = compile_rules()
    all_hits: list[dict[str, Any]] = []

    for path in args.files:
        source = read_source(path)
        if source is None:
            continue
        text, label = source
        if args.html or path.endswith((".html", ".htm")):
            text = strip_html(text)
        all_hits.extend(scan(text, rules, label, exclude_quotes=args.exclude_quotes))

    if args.json:
        print(json.dumps({"hits": all_hits, "count": len(all_hits)}, indent=2))
    else:
        render_report(all_hits)

    return 1 if (args.strict and all_hits) else 0


if __name__ == "__main__":
    sys.exit(main())
