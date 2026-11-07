---
disable-model-invocation: true
name: ars-abstract
description: ARS academic-paper `abstract-only` mode — English abstract + keywords
model: sonnet
---

First invoke the Skill tool with `skill: "academic-research-skills:academic-paper"`. Pass the mode and the user's request described below as its arguments. Use the loaded skill and its supporting files before producing the result.

Trigger the `academic-paper` skill in `abstract-only` mode. Produces an English abstract (150-300 words, structured) plus 5-7 keywords. Fidelity spectrum, medium oversight. Carries the v3.6.7 `report_compiler_agent` PATTERN PROTECTION layer when invoked through the pipeline.

Mode reference: `${CLAUDE_PLUGIN_ROOT}/MODE_REGISTRY.md` § academic-paper.
Skill entry: `${CLAUDE_PLUGIN_ROOT}/academic-paper/SKILL.md`.

Resolve plugin resources from `${CLAUDE_PLUGIN_ROOT}`, not from the paper project's working directory. If the skill or a required file cannot be loaded, report the loading failure and stop; do not substitute this command summary for the mode instructions.
