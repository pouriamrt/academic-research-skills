# Hot-path and quality hardening — design

**Date:** 2026-08-02
**Status:** proposed
**Scope:** `hooks/run_guard.sh`, `scripts/announce-ars-loaded.sh`, `hooks/hooks.json`,
`.claude/CLAUDE.md`, `.github/workflows/pytest.yml`, `pyproject.toml`, `.claude-plugin/plugin.json`

## Problem

A harness audit over 50 session transcripts (2026-07-24 → 2026-08-02, 9 days, 52,098 lines)
measured ARS as the dominant per-call latency source in the host Claude Code install, and the
repo as a large fixed context cost in every session — including sessions doing no academic work
at all.

| Symptom | Measurement |
|---|---|
| `run_guard.sh` PreToolUse | 4,890 runs · median **1,392 ms** · max 26,285 ms · **9,527 s total** |
| `announce-ars-loaded.sh` SessionStart | 59 runs · median 1,123 ms · **2,363 chars injected per session** |
| `.claude/CLAUDE.md` | 32,327 chars always loaded in-repo, **61 % of it release history** |
| `hooks/**` in CI | **not a `pytest` trigger path** — the guard's own tests never gate its changes |
| Lint / type checking | **absent** — no ruff, mypy, or equivalent in `pyproject.toml` or 14 CI workflows |

The two hook costs are unconditional: they are paid by every user of the plugin on every tool
call and every session start, whether or not the paper pipeline is ever invoked.

## Non-goals

- Removing or weakening the write-scope guard. The Bucket A fence is load-bearing and the
  operator confirmed the paper pipeline runs regularly.
- Dropping `Bash` from the PreToolUse matcher. That would silently retire the Bucket A Bash
  deny, which spec §3.2/§3.3/§7 identifies as the only policy that cannot fail open.
- Adding type annotations across the codebase. mypy adoption is scoped to the hook path only;
  broad typing is a separate project.

---

## S1 — `run_guard.sh`: four Python spawns per call → zero (Bash) or three (writes)

### Current cost structure

Each invocation cold-starts Python **four** times, measured with a counting shim on `PATH`
(2026-08-02) — not three as first assumed, because `find_real_python()` probes `py -3` first,
that probe fails on this machine, and it then probes `python3`:

| Spawn | Function | Purpose |
|---|---|---|
| 1 | `find_real_python()` | probes `py -3` — fails here |
| 2 | `find_real_python()` | probes `python3` — succeeds |
| 3 | the guard | The actual decision |
| 4 | `is_valid_hook_json()` | Spawns Python to JSON-parse the guard's own output |

On Windows (Git Bash) that is ~1.4 s of interpreter startup per tool call.

### Change 1 — shell fast path

Inserted immediately after `PAYLOAD=$(cat)`:

```sh
# Fast path: skip Python when no deny is reachable. The guard inspects only
# INSPECTED_TOOLS = STRUCTURED_WRITE_TOOLS | {"Bash"}; everything else is
# allowed by its first branch. For Bash the sole deny needs Bucket A gating,
# which needs `agent_type`. So: not a structured write tool AND no agent_type
# => `allow` is the only reachable outcome.
case $PAYLOAD in
    *'"agent_type"'* ) ;;                              # Bucket A possible -> real guard
    *'"Write"'* | *'"Edit"'* | *'"MultiEdit"'* ) ;;    # structured write -> real guard
    * ) emit_passthrough_and_exit ;;
esac
```

**Correctness.** Enumerating every path in `evaluate_decision()` that can return `deny`:

| Deny path | Requires | Excluded by |
|---|---|---|
| Bash + Bucket A | `agent_type` in manifest | `"agent_type"` arm |
| Structured + no `file_path` (schema drift) | `tool_name` ∈ STRUCTURED_WRITE_TOOLS | tool-name arm |
| Structured + infra-protected target | same | tool-name arm |
| Structured + escape + Bucket A | same | tool-name arm |
| Structured + Bucket A glob miss | same | tool-name arm |

Every other tool hits `if tool_name not in INSPECTED_TOOLS: return allow`. So the fast path
fires only where `allow` is the guard's sole reachable outcome.

- *False match* (a Bash command string containing `"Write"`, say) falls through to the real
  guard. Slower, still correct — the safe direction.
- *False skip* is impossible: both arms key on JSON that Claude Code must emit for the guard
  itself to reach the corresponding branch. If the guard can see it, the substring is there.
- *Field renamed upstream by Claude Code* → the fast path allows, and so does the Python guard,
  which derives `is_bucket_a` from the same field. The fast path inherits the guard's existing
  dependency rather than introducing a new one.

> **Design note — a rejected earlier version.** The first draft keyed on the absence of
> `"agent_type"` **and** `"file_path"`, reasoning that structured denies are all downstream of
> `_extract_structured_target()`, which requires `file_path`. Empirical validation against the
> real launcher (2026-08-02) falsified this: the schema-drift deny fires precisely when
> `file_path` is **absent**, so a `Write` payload lacking it carries neither substring, and the
> v1 fast path would have skipped a real `deny`. A genuine fail-open. Keying on the tool name
> instead of `file_path` closes it and needs no reasoning about which paths are infra-protected
> — the property holds structurally.

### Change 2 — REJECTED: do not delete `find_real_python()`

The first draft folded the probe into the guard run, on the reasoning that running the guard
proves a candidate is real Python just as the marker probe did. Empirical testing on
2026-08-02 falsified this twice over:

1. **It breaks the test doubles' contract.** `_fake_real_python()` builds fakes that satisfy the
   marker-probe contract (`-c <script>`). `LauncherHangingCandidateTest.test_hanging_py_then_real_python3`
   provisions only a hanging `py` and a real `python3` — no `python` at all. Running the guard as
   the probe changes which candidate wins and how failures cascade; the test hung to its 45 s
   timeout.
2. **It made writes SLOWER.** `py -3` is roughly 2× the startup cost of `python3` here (the
   launcher shim resolves a version and re-dispatches). The existing probe is cheap enough that
   `py -3` failing costs little; running the *guard* under `py -3` costs a full guard execution.
   Reordering candidates to put `python3` first fixed the speed but broke the hanging-candidate
   test, whose whole premise is `py`-first ordering.

The probe stays. It is doing real work for ~1 cheap spawn, and the fast path already eliminates
the interpreter entirely for the majority of calls, which is where the win actually lives.

### Change 3 — delete `is_valid_hook_json()` (this one is safe)

Its role is absorbed by the `case` prefix match in the loop above. The original comment rejects
*substring* grep as false-accepting `not json "hookSpecificOutput"`; an anchored prefix glob is
not subject to that, and the guard's output is always `json.dumps()` output from
`render_hook_output()`.

Residual risk: a malformed payload that begins with the prefix would be forwarded to Claude
Code and fail its parse. That degrades to a non-blocking hook error, not to a missed deny.

### Preserved unchanged

`run_bounded()`, the `setsid`/watchdog fallback, the done-file handshake, `ARS_PROBE_BOUND`,
the `mktemp` discipline, stderr advisory relay on the success path, and the
pass-through-on-anything-weird posture.

### Measured result

Wall-clock on this machine is too noisy to quote (the same case measured 970–3,618 ms across
runs under varying load). The load-independent metric is **interpreter spawns per call**,
counted with a logging shim on `PATH`:

| Case | before | after | decision |
|---|---|---|---|
| main-session Bash (~65% of matched calls) | 4 | **0** | identical |
| main-session Write | 4 | 3 | identical |
| schema-drift Write (deny) | 4 | 3 | identical |
| Bucket A Bash (deny) | 4 | 3 | identical |

Bash — the dominant case at 6,393 of 9,773 matched calls in the audit window — stops touching
Python at all. Structured writes drop one spawn of four. All decisions verified byte-identical
across both launchers.

Secondary benefit: `scripts/test_run_guard_launcher.py` runs 21/21 green against the modified
launcher, and its wall clock fell from 39.8 s to roughly 26–45 s depending on load.

---

## S2 — `announce-ars-loaded.sh`: stop injecting a listing the harness already provides

The SessionStart hook returns 2,363 characters of `additionalContext` (~590 tokens) enumerating
16 slash commands and 3 plugin agents. This is loaded into **every session in every project**,
academic or not, and costs 1,123 ms median at startup.

The content is fully derivable by the host: slash commands already appear in the command
listing, and plugin agents already appear in the agent-type listing. The banner is a third copy.

**Change:** reduce `additionalContext` to a single orienting line:

```
ARS v3.20.0 loaded — /ars-full runs the pipeline; see docs/PERFORMANCE.md for cost.
```

Everything the banner uniquely carried that is *not* derivable — the model-tiering note, the
"other ARS agents are in-skill prompt templates" clarification, the `$4–6` cost figure — belongs
in `.claude/CLAUDE.md` (loaded only in-repo, where it is actionable) rather than in every
session everywhere.

Saves ~590 tokens per session and ~1.1 s per session start.

---

## Q1 — `.claude/CLAUDE.md`: delete the embedded changelog

32,327 chars, always loaded when working in this repo. Lines 18–186 — **19,733 chars, 61 % of
the file** — are release notes for v2.9 through v3.20.0, duplicating `CHANGELOG.md` (352 KB, in
the same repo, spot-checked: `v3.6.7` appears 30×, `v3.4.0` 3×, `v2.9` 6×).

Per the derivability test, release history is reconstructible from `CHANGELOG.md` and `git log`
and does not steer in-session behavior.

**Change:** delete lines 18–186, replacing them with a one-line pointer:

```markdown
## Version history

See `CHANGELOG.md`. Current: v3.20.0.
```

**Retained** (the 12,594 chars that do steer behavior): Skills Overview, Routing Rules, Key
Rules, Optional MCP Capabilities, Full Academic Pipeline, Handoff Protocol, Validation Tools,
Version Info.

Saves ~4.9k tokens per in-repo session. The file drops from 32.3k to ~12.9k chars, well clear of
the ~40,000-char large-memory-file warning threshold it was approaching.

---

## Q3 — CI must cover `hooks/**` (land first)

`.github/workflows/pytest.yml` triggers on `scripts/**`, `tests/**`, `shared/contracts/**`,
`conftest.py`, `pyproject.toml`, `requirements-dev.txt`, `.github/workflows/pytest.yml`, and
three named paths. **`hooks/**` is absent.**

A PR touching only `hooks/run_guard.sh` therefore runs no tests, despite
`scripts/test_run_guard_launcher.py` existing specifically to test it. S1 edits exactly that
file, so this gap must close first or S1 ships CI-untested.

**Change:** add `- 'hooks/**'` to both the `pull_request` and `push` `paths` lists.

---

## Q2 — adopt ruff (staged), and mypy on the hook path only

No linter or type checker is configured anywhere. 40 `# noqa` comments exist in the codebase and
38 of them are flagged `RUF100 unused-noqa`, indicating a linter was run once historically and
then abandoned.

Measured surface (`uvx ruff check`, ruff via `uvx`, no config present):

| Selection | Findings | Auto-fixable |
|---|---|---|
| Default rules (`E4,E7,E9,F`) | **86** | 49 |
| Wide opt-in ruleset | 533 | 312 |

Staged so each phase is independently reviewable:

**Phase 1 — default rules as the CI gate.** Add `[tool.ruff]` to `pyproject.toml` pinning
`target-version` and `select = ["E4", "E7", "E9", "F"]`. Run `ruff check --fix` (49 auto), hand-
fix the remaining ~37 (`E702` ×10, `E401` ×8, `E402` ×6, `F841` ×5, `E731` ×4, `F811` ×1). Add a
`ruff check` step to the pytest workflow. Small enough to land in one PR.

**Phase 2 — `ruff format`.** Separate commit, so the formatting diff never mixes with logic
changes and stays reviewable.

**Phase 3 — incremental opt-in, one family per PR.** `I001` (115, all auto-fixable in a single
pass), `RUF100` (38 stale noqa — deletions), `UP035`/`UP045` (66, mechanical), `F401` (27).

**Deferred to triage, not bulk-fixed:** `PLW1510` subprocess-run-without-check (60) and
`BLE001` blind-except (24). Each encodes a real decision about failure handling in a repo whose
whole guard design is about failing in a chosen direction; mechanical fixes here could change
degradation behavior. These get read individually.

**Noted, not treated as defects:** `PLE2515` invalid-character-zero-width-space (7) are
*deliberate* U+200B test fixtures in `scripts/test_check_tools_allowlist.py`, verifying the
tools-allowlist checker handles format characters. Escaping them to a Unicode escape sequence is still worth
doing — invisible characters in source are hostile to review — but they are not bugs.
`B023` function-uses-loop-variable (12) are concentrated in
`scripts/migrate_literature_corpus_to_v3_9_0.py`, a one-off migration script; real pattern, low
blast radius.

**mypy:** scope to `scripts/ars_write_scope_guard.py` and the hook path only. Typing 251 files
is a separate project and is explicitly out of scope here.

---

## Q4 — `plugin.json` description

The `description` field is ~1,200 characters. It opens correctly ("Suite of Claude Code skills
for rigorous academic research…") then spends four sentences narrating the v3.20 → v3.19 →
v3.17 → v3.16 merge history. This string is what a prospective user reads in a plugin listing.

**Change:** keep the first sentence and the 8-skill summary; move version narration to
`CHANGELOG.md`, where the same content already lives. Retain the "Optional integrations" clause
— that is capability information, not history.

---

## Q5 — install payload (noted, likely won't-fix)

The cache install is 29 MB and carries 129 test files, 3.6 MB of `docs/` (design specs and HTML
snapshots), and 18 PDFs/PNGs. Worth one check of whether the directory-marketplace loader honors
an ignore file. If it does not, record the finding and move on — it is install size only, with
no runtime cost.

---

## Testing

**S1** — `python -m pytest scripts/test_run_guard_launcher.py -q` is the gate. The existing
21-test suite already covers no-Python passthrough, 0-byte stub skip ordering, `py -3` argument
splitting, guard-broke degradation, hanging candidates, watchdog robustness, and infra
protection. `LauncherStubSkipOrderingTest` may need its assertions reframed, since
`find_real_python()` no longer exists — the *behavior* it verifies (stub skipped in favour of a
real interpreter) must still hold.

Four cases to add:

1. Main-session Bash payload → pass-through **and zero Python invocations**, asserted with a
   counting stub on `PATH`. This proves the fast path fired, rather than merely that the right
   answer came back.
2. Bucket A Bash payload (`agent_type` present, in manifest) → still `deny`. The regression that
   matters most.
3. **Schema drift: `Write` / `Edit` / `MultiEdit` with no top-level `file_path` → still `deny`.**
   This is the case that killed the v1 predicate; it must be a permanent regression test.
4. Main-session Write targeting an ARS infra file (`hooks/*.sh`) → still `deny`.

A validation harness exercising all of these against the *unmodified* launcher was run on
2026-08-02 — 12 payloads, 5 of them real `deny` outcomes — and confirmed the v2 predicate never
fast-paths a non-pass-through. Port it into the test file rather than leaving it ad hoc.

### Pre-existing baseline: the suite is NOT green

Measured at HEAD (`7d54ac1`) with no changes applied. The count depends on the environment:
**without** `PYTHONUTF8=1`, 22 failures; **with** it — as this plan mandates everywhere —
**11 failed, 3355 passed, 7 skipped, 1 xfailed in 932 s**. Both clusters are environmental,
not regressions:

| Cluster | Count | Cause | Mitigation |
|---|---|---|---|
| Unicode / `charmap` | 11 | Windows console cp1252 cannot encode ` `, `—` | run with `PYTHONUTF8=1` — recovers all 11 |
| `check_v3_6_8_pattern_protection` | 11 | anti-self-baseline git-history guard; needs a PR-shaped base ref, and the fork's merge-sync history trips its `merge-base..HEAD` path scan | CI-only; not reproducible on a local checkout sitting on `main` |

**Consequence for every task in this plan:** the gate is *"no NEW failures against this recorded
baseline"*, never *"the suite is green"*. Because `PYTHONUTF8=1` is mandatory, the recorded baseline
is the **11** pattern-protection failures; diff against those. A run reporting 22 is a run that
forgot the variable, not a regression.

The launcher suite that actually gates S1 — `scripts/test_run_guard_launcher.py` — **is** fully
green (21/21, 39.8 s), so S1 has a trustworthy gate regardless.

**S2 / Q1 / Q4** — content edits, verified by re-measuring emitted bytes and file size.
**Q3** — verified by a PR touching only `hooks/` and observing pytest run.
**Q2** — `uvx ruff check .` exits 0 at the pinned selection; full suite stays green.

## Rollout

All edits land in the source repo (`~/Python/AI/AI_scientist/academic-research-skills`, git
`main`), **never** in the version-pinned cache at
`~/.claude/plugins/cache/academic-research-skills/academic-research-skills/3.20.0/` — a cache
edit is discarded at the next version bump.

Order: **Q3 → S2 → Q1 → S1 → Q2 (phased) → Q4**. Q3 first so S1 is CI-covered when it lands.
Version bump and `CHANGELOG.md` entry per existing release discipline; `tag-version-match` and
`changelog-covers-merges` workflows enforce this already.
