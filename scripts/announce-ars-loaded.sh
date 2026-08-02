#!/usr/bin/env bash
# version: 1.1.0
#
# SessionStart hook script for the ARS Claude Code plugin (v3.7.0+).
#
# Reads the SessionStart event JSON on stdin and emits a hookSpecificOutput
# JSON with `additionalContext` describing what ARS provides in this session.
# The plugin loader injects that context into the LLM's first turn so the
# user (and Claude) can see, on session start, that ARS is loaded and which
# slash commands and plugin agents are available.
#
# Allowed invokers: Claude Code's plugin loader (SessionStart event).
# This script is safe to run from any context; it does not invoke codex,
# does not write outside its own stdout, and produces no side effects on
# the working tree.
#
# Exit codes:
#   0    Always — even on parse failure, fall back to the long-form announce.
#   2    Reserved (not used; SessionStart cannot block).

set -euo pipefail

# ---------------------------------------------------------------------------
# This script intentionally avoids Bash 4+ features (no associative arrays,
# no indirect expansion via `${!var}`, no `<<<` here-strings on the hot
# path). It runs cleanly on macOS stock /bin/bash 3.2 so plugin users
# don't have to `brew install bash` just to see the SessionStart announce.
# `run_codex_audit.sh` does need Bash 4+ — that wrapper guards itself.
# ---------------------------------------------------------------------------
# Read SessionStart event JSON from stdin and pull `source` (one of
# startup / resume / clear / compact) without taking a hard dependency on
# jq — many ARS users won't have it installed and we want this hook to
# work out of the box.
# ---------------------------------------------------------------------------
INPUT=""
if [[ ! -t 0 ]]; then
  INPUT=$(cat)
fi

SOURCE="startup"
if [[ -n "${INPUT}" ]]; then
  # Match `"source": "<value>"` with optional whitespace; tolerate single-line
  # or multi-line JSON. Falls through to default `startup` on any parse miss.
  if [[ "${INPUT}" =~ \"source\"[[:space:]]*:[[:space:]]*\"([a-z]+)\" ]]; then
    SOURCE="${BASH_REMATCH[1]}"
  fi
fi

# ---------------------------------------------------------------------------
# For `compact` and `resume` we keep the announce minimal: the LLM already
# has prior ARS context from the resumed transcript or carried-over summary,
# and re-injecting the full slash-command list every resume burns context.
# `startup` and `clear` get the full version.
# ---------------------------------------------------------------------------
case "${SOURCE}" in
  compact|resume)
    ANNOUNCE="ARS plugin still loaded after ${SOURCE}. Slash commands: /ars-full /ars-plan /ars-outline /ars-revision /ars-revision-coach /ars-rebuttal-audit /ars-abstract /ars-lit-review /ars-3w /ars-reviewer /ars-format-convert /ars-citation-check /ars-disclosure /ars-mark-read /ars-unmark-read /ars-cache-invalidate. Plugin agents: synthesis_agent, research_architect_agent, report_compiler_agent."
    ;;
  startup|clear|*)
    ANNOUNCE="ARS (academic-research-skills) v3.20.0 loaded.
Slash commands (16): /ars-full /ars-plan /ars-outline /ars-revision /ars-revision-coach /ars-rebuttal-audit /ars-abstract /ars-lit-review /ars-3w /ars-reviewer /ars-format-convert /ars-citation-check /ars-disclosure /ars-mark-read /ars-unmark-read /ars-cache-invalidate
Plugin agents: synthesis_agent, research_architect_agent, report_compiler_agent.
Per-command descriptions live in commands/*.md; cost reference in docs/PERFORMANCE.md (full run ~\$4-6)."
    ;;
esac

# ---------------------------------------------------------------------------
# Emit the JSON. We assemble it with a here-doc and a sentinel substitution
# rather than printf/jq to keep the output stable across Bash patch versions.
# additionalContext must be a JSON string — escape backslashes, double quotes,
# newlines.
# ---------------------------------------------------------------------------
escape_json() {
  local raw="$1"
  raw="${raw//\\/\\\\}"
  raw="${raw//\"/\\\"}"
  raw="${raw//$'\n'/\\n}"
  printf '%s' "${raw}"
}

ESCAPED=$(escape_json "${ANNOUNCE}")

cat <<JSON
{"hookSpecificOutput":{"hookEventName":"SessionStart","additionalContext":"${ESCAPED}"}}
JSON

exit 0
