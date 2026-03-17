# Academic Research Skills for Claude Code

[![License: CC BY-NC 4.0](https://img.shields.io/badge/license-CC%20BY--NC%204.0-lightgrey)](https://creativecommons.org/licenses/by-nc/4.0/)

A Claude Code plugin covering the full academic research lifecycle — from literature review through experimentation, statistical analysis, paper writing, peer review, and publication. Experiment skills integrate with the [superpowers](https://github.com/obra/superpowers) plugin for disciplined, test-driven code development.

## Skills

| Skill | Agents | What it does | Key Modes |
|-------|--------|-------------|-----------|
| **deep-research** | 13 | Research team with systematic review, PRISMA, meta-analysis | full, quick, socratic, lit-review, fact-check, systematic-review |
| **experiment-designer** | 6 | Experiment protocol, power analysis, instruments, randomization | full, guided, quick, power-only, instrument |
| **data-analyst** | 7 | Statistical analysis execution with APA-formatted results | full, guided, quick, assumption-check, exploratory, replication |
| **simulation-runner** | 5 | Monte Carlo, bootstrap, agent-based models, parameter sweeps | full, guided, quick, power-sim, sensitivity, bootstrap |
| **lab-notebook** | 4 | Experiment research record with provenance tracking | full, log-entry, deviation, snapshot, export, audit |
| **academic-paper** | 12 | Paper writing with bilingual abstracts and LaTeX output | full, plan, revision, format-convert, citation-check |
| **academic-paper-reviewer** | 7 | Multi-perspective peer review (EIC + 3 reviewers + Devil's Advocate) | full, re-review, quick, methodology-focus, guided |
| **academic-pipeline** | 3 | Full pipeline orchestrator coordinating all skills above | auto-detected stages |

## Pipeline

```mermaid
flowchart TB
    subgraph S1["Stage 1: RESEARCH"]
        DR["deep-research<br/>13 agents"]
    end

    subgraph S15["Stage 1.5: EXPERIMENT — auto-detected"]
        direction TB
        ED["experiment-designer<br/>6 agents"]
        DA["data-analyst<br/>7 agents"]
        SR["simulation-runner<br/>5 agents"]
        LN["lab-notebook<br/>4 agents"]
        ED --> DA & SR
        DA & SR -.-> LN
    end

    subgraph S2["Stage 2: WRITE"]
        AP["academic-paper<br/>12 agents"]
    end

    subgraph S25["Stage 2.5: INTEGRITY"]
        IV1["integrity verification<br/>100% reference + data check"]
    end

    subgraph S3["Stage 3: REVIEW"]
        APR["academic-paper-reviewer<br/>EIC + 3 Reviewers + Devil's Advocate"]
    end

    subgraph S4["Stage 4: REVISE"]
        APrev["academic-paper<br/>revision mode"]
    end

    subgraph S3p["Stage 3': RE-REVIEW"]
        APR2["academic-paper-reviewer<br/>re-review mode"]
    end

    subgraph S45["Stage 4.5: FINAL INTEGRITY"]
        IV2["integrity verification<br/>zero-tolerance check"]
    end

    subgraph S5["Stage 5: FINALIZE"]
        FIN["MD + DOCX + LaTeX + PDF"]
    end

    S1 -->|"methodology<br/>blueprint"| S15
    S1 -->|"no experiment<br/>needed"| S2
    S15 -->|"Schema 10-12<br/>results"| S2
    S2 --> S25
    S25 -->|PASS| S3
    S25 -->|FAIL| S25
    S3 -->|"Minor / Major"| S4
    S3 -->|Accept| S45
    S4 --> S3p
    S3p -->|Accept| S45
    S3p -->|Major| S4
    S45 -->|PASS| S5

    style S1 fill:#4A90D9,color:#fff
    style S15 fill:#F5A623,color:#fff
    style S2 fill:#7B68EE,color:#fff
    style S25 fill:#E74C3C,color:#fff
    style S3 fill:#2ECC71,color:#fff
    style S4 fill:#9B59B6,color:#fff
    style S3p fill:#2ECC71,color:#fff
    style S45 fill:#E74C3C,color:#fff
    style S5 fill:#1ABC9C,color:#fff
```

The experiment stages (1.5) are auto-detected from the methodology blueprint produced by deep-research. Literature reviews, theoretical papers, and policy analyses skip straight to writing.

## Superpowers Integration

Experiment skills (`experiment-designer`, `data-analyst`, `simulation-runner`) integrate with the [superpowers](https://github.com/obra/superpowers) plugin for disciplined code development. When agents write complex code — custom simulations, SEM models, multi-step analysis pipelines — they autonomously invoke superpowers skills via the `Skill` tool:

```mermaid
flowchart LR
    subgraph classify["1. Classify Task"]
        CL{"SIMPLE<br/>or<br/>COMPLEX?"}
    end

    subgraph simple["Direct Execution"]
        SE["Run code directly<br/>library one-liners"]
    end

    subgraph path1["Path 1: New Code"]
        B1["Skill: brainstorming<br/>autonomous"]
        P1["Skill: writing-plans"]
        T1["Skill: TDD<br/>scientific tests"]
        V1["Skill: verification"]
        B1 --> P1 --> T1 --> V1
    end

    subgraph path2["Path 2: Debug"]
        D2["Skill: systematic<br/>debugging"]
        T2["Skill: TDD<br/>regression test"]
        V2["Skill: verification"]
        D2 --> T2 --> V2
    end

    subgraph path3["Path 3: Iterate"]
        P3["Skill: writing-plans"]
        T3["Skill: TDD<br/>update tests"]
        V3["Skill: verification"]
        P3 --> T3 --> V3
    end

    CL -->|SIMPLE| SE
    CL -->|"COMPLEX<br/>new code"| B1
    CL -->|"COMPLEX<br/>bug/failure"| D2
    CL -->|"COMPLEX<br/>modify"| P3

    style classify fill:#34495E,color:#fff
    style simple fill:#27AE60,color:#fff
    style path1 fill:#2980B9,color:#fff
    style path2 fill:#E74C3C,color:#fff
    style path3 fill:#F39C12,color:#fff
```

**How it works:**

- A **category-based lookup table** classifies each code task as SIMPLE or COMPLEX
- **SIMPLE** tasks (standard t-test, basic power analysis, seaborn plots) execute directly — zero overhead
- **COMPLEX** tasks (custom DGPs, SEM, agent-based models, multi-step pipelines) trigger the superpowers workflow:
  - Each step invokes the real superpowers skill via `Skill("superpowers:...")`, loading the full skill content
  - Brainstorming runs autonomously — the agent uses upstream research context instead of asking the user
  - TDD is adapted for scientific code — known-answer tests, synthetic data validation, reproducibility checks
- **Fully autonomous** — no human checkpoints; escape hatch surfaces to user after 2 failed attempts
- **Always active** — works both standalone and within the pipeline

**Prerequisite:** `claude plugin install superpowers@claude-plugins-official`

### Complexity Classification

| Category | Examples |
|----------|----------|
| **SIMPLE** | t-test, ANOVA, correlation, chi-square, standard power analysis, seaborn plots, bootstrap CI |
| **COMPLEX** | Custom DGPs, Monte Carlo simulations, SEM/HLM, agent-based models, parameter sweeps, mediation bootstrap, multi-panel figures, survival analysis |

### Scientific TDD

| Agent | Test Approach |
|-------|--------------|
| power_analyst | Known-answer tests against published power tables, boundary tests, monotonicity checks |
| analysis_executor | Synthetic data with known parameters, null hypothesis tests, output structure validation |
| data_preparation | Missing count assertions, no-new-NaN checks, type validation, row count guards |
| visualization | File existence, smoke tests, APA dimension checks |
| model_builder | Purity tests (same seed = same output), structure tests, edge case tests, distribution tests |
| execution_engine | Reproducibility tests, convergence tests, parallel equivalence tests |

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
