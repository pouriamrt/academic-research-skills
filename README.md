# Academic Research Skills for Claude Code

[![License: CC BY-NC 4.0](https://img.shields.io/badge/license-CC%20BY--NC%204.0-lightgrey)](https://creativecommons.org/licenses/by-nc/4.0/)

A Claude Code plugin covering the full academic research lifecycle — from literature review through experimentation, statistical analysis, paper writing, peer review, and publication. Experiment skills integrate with the [superpowers](https://github.com/obra/superpowers) plugin for disciplined, test-driven code development.

## Skills

| Skill | What it does | Key Modes |
|-------|-------------|-----------|
| **deep-research** | 13-agent research team with systematic review + PRISMA | full, quick, socratic, lit-review, fact-check, systematic-review |
| **experiment-designer** | Experiment protocol, power analysis, instruments, randomization | full, guided, quick, power-only, instrument |
| **data-analyst** | Statistical analysis execution with APA-formatted results | full, guided, quick, assumption-check, exploratory, replication |
| **simulation-runner** | Monte Carlo, bootstrap, agent-based models, parameter sweeps | full, guided, quick, power-sim, sensitivity, bootstrap |
| **lab-notebook** | Experiment research record with provenance tracking | full, log-entry, deviation, snapshot, export, audit |
| **academic-paper** | 12-agent paper writing with LaTeX output | full, plan, revision, format-convert, citation-check |
| **academic-paper-reviewer** | Multi-perspective peer review (EIC + 3 reviewers + Devil's Advocate) | full, re-review, quick, methodology-focus, guided |
| **academic-pipeline** | Full pipeline orchestrator coordinating all skills above | auto-detected stages |

## Pipeline

<p align="center">
  <img src="assets/pipeline.png" alt="Academic Research Pipeline" width="500"/>
</p>

The experiment stages are auto-detected from the methodology blueprint. Literature reviews, theoretical papers, and policy analyses skip straight to writing.

## Superpowers Integration

Experiment skills (`experiment-designer`, `data-analyst`, `simulation-runner`) integrate with the **superpowers** plugin for disciplined code development. When agents need to write complex code — custom simulations, SEM models, multi-step analysis pipelines — they autonomously run through the superpowers workflow:

<p align="center">
  <img src="assets/superpowers-workflow.png" alt="Superpowers Adaptive Workflow" width="700"/>
</p>

**How it works:**

- **Category-based trigger** — a lookup table classifies each code task as SIMPLE or COMPLEX
- **SIMPLE** tasks (standard t-test, basic power analysis) execute directly — no overhead
- **COMPLEX** tasks (custom DGPs, SEM, agent-based models, multi-step pipelines) trigger one of 3 adaptive paths:
  - **New code** — brainstorm approach, plan steps, TDD with scientific tests, verify
  - **Bug/failure** — systematic debugging, regression test, verify
  - **Iteration** — plan changes, update tests, verify
- **Fully autonomous** — no human checkpoints during the workflow; escape hatch surfaces to user after 2 failed attempts
- **TDD adapted for scientific code** — known-answer tests, synthetic data validation, reproducibility checks, distributional property assertions

**Prerequisite:** Install the superpowers plugin: `claude plugin install superpowers@claude-plugins-official`

## Installation

### As a Claude Code Plugin (Recommended)

```bash
# Register as a local marketplace
claude plugin marketplace add /path/to/academic-research-skills

# Install the plugin
claude plugin install academic-research-skills
```

After installation, all 8 skills auto-trigger in every project based on your request.

### As a Standalone Project

```bash
git clone https://github.com/pouriamrt/academic-research-skills.git
cd academic-research-skills
claude
```

### As Project Skills

```bash
cd /path/to/your/project
mkdir -p .claude/skills
git clone https://github.com/pouriamrt/academic-research-skills.git .claude/skills/academic-research-skills
```

## Usage

```bash
# Full pipeline (research -> experiment -> write -> review -> publish)
"I want to write a research paper on the effect of gamification on student engagement"

# Just research
"Research the impact of AI on healthcare outcomes"

# Design an experiment
"Design an experiment testing whether AI tutoring improves calculus scores"

# Analyze data
"Analyze my data: ./experiment_data.csv"

# Run a simulation
"Run a Monte Carlo power simulation for a 2x3 mixed ANOVA"

# Write a paper (with guided planning)
"Guide me through writing a paper on demographic decline in higher education"

# Review a paper
"Review this paper" (then provide the paper)
```

## Recommended Settings

| Setting | Purpose |
|---------|---------|
| **Claude Opus 4.6 + Max plan** | Full pipeline can exceed 200K+ tokens |
| **`--dangerously-skip-permissions`** | Uninterrupted autonomous execution for long pipelines |
| **superpowers plugin** | Enables disciplined TDD workflow for complex experiment code |

## Supported Formats

**Citation:** APA 7.0 (default), Chicago, MLA, IEEE, Vancouver
**Paper structures:** IMRaD, Literature Review, Theoretical, Case Study, Policy Brief, Conference Paper
**Output:** Markdown, LaTeX, DOCX, PDF (via tectonic)
**Statistics:** t-tests, ANOVA, regression, chi-square, SEM, HLM, survival analysis, Bayesian, and more

## License

[CC-BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/) — Free to share and adapt with attribution for non-commercial use.
