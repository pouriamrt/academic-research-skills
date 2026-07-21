#!/usr/bin/env python3
"""SETUP cross-model example membership lint (#491 fold-in, fork EN-only).

The quick-setup bash block in docs/SETUP.md hardcodes verifier model IDs
(`ARS_CROSS_MODEL="..."`) because they are literal export strings a user
pastes — they cannot be made version-agnostic the way the canonical doc's
primary row was. That makes them a drift surface: the gpt-5.4→gpt-5.5 lineup
migration (2026-06-10, F-003) fixed the canonical doc but missed SETUP for
three weeks (B4-F02, audits/harness-retirement-2026-07-04.md).

Fork note: upstream's invariant 1 (en ↔ zh-TW parity) is retired — this fork
deleted docs/SETUP.zh-TW.md in v3.17.0 (English-only). The surviving
invariant:

1. **canonical membership** — every example value must appear in a model
   TABLE of shared/cross_model_verification.md (the column whose header
   contains "API ID": the first-party supported table + the compat-provider
   table). Backticked ids elsewhere in the doc deliberately do NOT count —
   the legacy-accepted note backticks `gpt-5.4`/`gpt-5.4-pro`, and "accepted
   for existing setups" is not "recommended in SETUP examples" (false-pass
   surface caught by codex review on PR #492).

Fail-closed twice: zero ARS_CROSS_MODEL examples in a SETUP file, or zero
ids extracted from the canonical tables, is an error (the extraction went
stale), never a silent pass.

Exit codes: 0 on pass, 1 on any failure.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

SETUP_EN = REPO_ROOT / "docs/SETUP.md"
CANONICAL = REPO_ROOT / "shared/cross_model_verification.md"

# Matches active and commented example lines alike:
#   export ARS_CROSS_MODEL="gpt-5.5"
#   # or: export ARS_CROSS_MODEL="gemini-3.1-pro-preview"
ASSIGNMENT_RE = re.compile(r'ARS_CROSS_MODEL="([^"]+)"')

def canonical_model_ids(canonical_text: str) -> set[str]:
    """Backticked ids from the "API ID" column of the canonical doc's model
    tables ONLY. A table starts at a header row containing "API ID" and ends
    at the first non-table line; ids backticked in surrounding prose (e.g.
    the legacy-accepted note) are deliberately excluded."""
    ids: set[str] = set()
    api_id_col: int | None = None
    for line in canonical_text.splitlines():
        stripped = line.strip()
        if not stripped.startswith("|"):
            api_id_col = None
            continue
        cells = [c.strip() for c in stripped.strip("|").split("|")]
        if api_id_col is None:
            if any("API ID" in c for c in cells):
                api_id_col = next(i for i, c in enumerate(cells) if "API ID" in c)
            continue
        if len(cells) > api_id_col:
            # Globs like `gpt-*` (from the compat table's "any non-`gpt-*`
            # id" prose) are prefix patterns, not model ids — exclude them.
            ids.update(
                tok
                for tok in re.findall(r"`([^`]+)`", cells[api_id_col])
                if "*" not in tok
            )
    return ids


def extract_ids(setup_text: str) -> list[str]:
    """All ARS_CROSS_MODEL example values in a SETUP file, in order."""
    return ASSIGNMENT_RE.findall(setup_text)


def check(en_text: str, canonical_text: str) -> list[str]:
    errors: list[str] = []
    en_ids = extract_ids(en_text)

    if not en_ids:
        errors.append(
            "docs/SETUP.md: no ARS_CROSS_MODEL example values found — either "
            "the quick-setup block was removed or the extraction regex went "
            "stale. Fail-closed per lint contract."
        )

    known = canonical_model_ids(canonical_text)
    if not known:
        errors.append(
            "shared/cross_model_verification.md: no ids extracted from any "
            "'API ID' table column — the table format changed and the parser "
            "went stale. Fail-closed per lint contract."
        )
        return errors
    for model_id in en_ids:
        if model_id not in known:
            errors.append(
                f"docs/SETUP.md: ARS_CROSS_MODEL example {model_id!r} is not in "
                f"the canonical model tables of "
                f"shared/cross_model_verification.md (B4-F02 drift class; "
                f"legacy ids in the accepted-note do not count as "
                f"recommended). Update the example or the canonical table, "
                f"in the same PR."
            )
    return errors


def main() -> int:
    errors = check(
        SETUP_EN.read_text(encoding="utf-8"),
        CANONICAL.read_text(encoding="utf-8"),
    )
    if errors:
        print("SETUP cross-model parity lint FAILED:", file=sys.stderr)
        for err in errors:
            print(f"  - {err}", file=sys.stderr)
        return 1
    print("SETUP cross-model parity lint PASSED: all example values are in "
          "the canonical lineup.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
