# Academic Research Skills for Claude Code

[![Version](https://img.shields.io/badge/version-v3.15.0-blue)](https://github.com/pouriamrt/academic-research-skills)
[![License: CC BY-NC 4.0](https://img.shields.io/badge/license-CC%20BY--NC%204.0-lightgrey)](https://creativecommons.org/licenses/by-nc/4.0/)

A Claude Code plugin covering the full academic research lifecycle — from literature review through experimentation, statistical analysis, paper writing, peer review, and publication. 8 skills, 58 agents, 18 handoff schemas, and full pipeline orchestration. Experiment skills integrate with the [superpowers](https://github.com/obra/superpowers) plugin for disciplined, test-driven code development.

## Skills

> **AI is your copilot, not the pilot.** This tool won't write your paper for you. It handles the grunt work — hunting down references, formatting citations, verifying data, checking logical consistency — so you can focus on the parts that actually require your brain: defining the question, choosing the method, interpreting what the data means, and writing the sentence after "I argue that."
>
> Unlike a humanizer, this tool doesn't help you hide the fact that you used AI. It helps you write better. Style Calibration learns your voice from past work. Writing Quality Check catches the patterns that make prose feel machine-generated. The goal is quality, not cheating.

### Why human-in-the-loop, not full automation?

Lu et al. (2026, *Nature* 651:914-919) built **The AI Scientist** — the first fully autonomous AI research system to publish a paper through blind peer review at a top-tier ML venue (ICLR 2025 workshop, score 6.33/10 vs workshop average 4.87). It is the strongest published benchmark of what end-to-end autonomous AI research can do as of 2026.

Their own Limitations section enumerates the failure modes that any fully-autonomous AI research pipeline inherits:
- Implementation bugs that pass AI self-review but poison the results
- Hallucinated experimental results that look plausible
- Shortcut reliance (models exploiting spurious features and writing papers about "solving" the task)
- Implementation bugs reframed as novel insights
- Methodology fabrication (Methods section drifting from what was actually run)
- Frame-lock at early stages (wrong hyperparameter direction the pipeline cannot back out of)
- Citation hallucinations

ARS is built on the premise that **a human researcher augmented by AI avoids these failure modes better than either alone**. v3.2 directly operationalizes the Lu 2026 failure-mode taxonomy: the pipeline's Stage 2.5 and Stage 4.5 integrity gates now run a 7-mode blocking checklist (see `academic-pipeline/references/ai_research_failure_modes.md`), and the reviewer offers an opt-in calibration mode that measures its own FNR/FPR against a user-supplied gold set (see `academic-paper-reviewer/references/calibration_mode_protocol.md`).

The AI Scientist shows that autonomous AI research is now possible. ARS is designed to give you the leverage of that capability without inheriting its failure modes.

v3.3 was inspired by [**PaperOrchestra**](https://arxiv.org/abs/2604.05018) (Song, Song, Pfister & Yoon, 2026, Google), a multi-agent framework that autonomously authors LaTeX manuscripts from raw research materials. We integrated several of their techniques: **Semantic Scholar API verification** for programmatic citation checking, an **anti-leakage protocol** that prevents the LLM from silently filling gaps with parametric memory, **VLM figure verification** for closed-loop visual quality checks, and **score trajectory tracking** that detects when revisions inadvertently degrade specific quality dimensions.

---

| Skill | Agents | What it does | Key Modes |
|-------|--------|-------------|-----------|
| **deep-research** v2.9 | 14 | Research team with concept lineage, systematic review, PRISMA, meta-analysis, Semantic Scholar API verification | full, quick, socratic, review, lit-review, fact-check, systematic-review |
| **experiment-designer** v1.0 | 6 | Experiment protocol, power analysis, instruments, randomization | full, guided, quick, power-only, instrument |
| **data-analyst** v1.0 | 7 | Statistical analysis execution with APA-formatted results | full, guided, quick, assumption-check, exploratory, replication |
| **simulation-runner** v1.0 | 5 | Monte Carlo, bootstrap, agent-based models, parameter sweeps | full, guided, quick, power-sim, sensitivity, bootstrap |
| **lab-notebook** v1.0 | 4 | Experiment research record with provenance tracking | full, log-entry, deviation, snapshot, export, audit |
| **academic-paper** v3.0 | 12 | Paper writing with experiment integration, LaTeX output, anti-leakage protocol, VLM figure verification, disclosure mode | full, plan, outline-only, revision, revision-coach, abstract-only, lit-review, format-convert, citation-check, disclosure |
| **academic-paper-reviewer** v1.8 | 7 | Multi-perspective peer review (EIC + 3 reviewers + Devil's Advocate + optional cross-model) with calibration mode | full, re-review, quick, methodology-focus, guided, calibration |
| **academic-pipeline** v3.3 | 3 | Full pipeline orchestrator with AI Research Failure Mode Checklist (Lu 2026), score trajectory tracking, early-stopping | auto-detected stages |

See the [Quick Reference Card](docs/QUICK_REFERENCE.md) for a full "I want to X → use skill Y in mode Z" lookup table.

## Pipeline

<p align="center">
  <img src="assets/pipeline.png" alt="Academic Research Pipeline" width="700"/>
</p>

The experiment stages (1.5) are auto-detected from the methodology blueprint produced by deep-research. Literature reviews, theoretical papers, and policy analyses skip straight to writing.

- **Deep Research** — 14-agent research team with concept lineage, Socratic guided mode + systematic review / PRISMA + SCR Loop + **intent detection** + **dialogue health monitoring** + **optional cross-model DA** + **argumentation & reasoning cognitive framework** + **Semantic Scholar API verification** (v3.3 PaperOrchestra)
- **Experiment Designer / Data Analyst / Simulation Runner / Lab Notebook** — 4 experiment skills (22 agents) with auto-detected pipeline integration, power analysis, APA-formatted statistics, Monte Carlo / bootstrap / SEM / HLM, full provenance tracking, and superpowers integration for disciplined code development
- **Academic Paper** — 12-agent paper writing with experiment results integration (Schema 11/12), Style Calibration, Writing Quality Check, LaTeX output hardening, visualization, revision coaching, citation conversion, **writing judgment framework**, **anti-leakage protocol**, **VLM figure verification**, and **disclosure mode** (venue-specific AI usage statements)
- **Academic Paper Reviewer** — Multi-perspective peer review with 0-100 quality rubrics (EIC + 3 dynamic reviewers + Devil's Advocate with **concession threshold protocol** + **attack intensity preservation** + **optional cross-model review**) + **R&R traceability matrix** + **read-only constraint** + **review quality thinking framework** + **calibration mode** (FNR/FPR measurement against gold-standard sets)
- **Academic Pipeline** — Full pipeline orchestrator (10 stages + experiment re-entry) with adaptive checkpoints, audible alerts, claim verification, material passport, **optional cross-model integrity verification**, **mid-conversation reinforcement**, **self-check questions**, **score trajectory tracking**, **early-stopping criterion**, and **AI Research Failure Mode Checklist** (Lu 2026 — 7-mode taxonomy, mandatory blocking at Stage 2.5/4.5)

## Superpowers Integration

Experiment skills (`experiment-designer`, `data-analyst`, `simulation-runner`) integrate with the [superpowers](https://github.com/obra/superpowers) plugin for disciplined code development. When agents write complex code — custom simulations, SEM models, multi-step analysis pipelines — they autonomously invoke superpowers skills via the `Skill` tool:

<p align="center">
  <img src="assets/superpowers-workflow.png" alt="Superpowers Adaptive Workflow" width="700"/>
</p>

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

## Companion: Experiment Agent

If your research involves running experiments (code or human studies) before writing, the [Experiment Agent](https://github.com/Imbad0202/experiment-agent) skill fills the gap between ARS Stage 1 (RESEARCH) and Stage 2 (WRITE).

```
ARS Stage 1 RESEARCH  →  RQ Brief + Methodology Blueprint
        ↓
  experiment-agent     →  run/manage experiments → validate results
        ↓
ARS Stage 2 WRITE     →  write paper with verified experiment results
```

**What it does**: executes code experiments (Python, R, etc.) with real-time monitoring, manages human study protocols with IRB ethics checklist, interprets statistics with 11-type fallacy detection, and verifies reproducibility.

**How to use together**: pause the ARS pipeline after Stage 1, run experiments in a separate experiment-agent session, then bring the results (with Material Passport) back to ARS Stage 2. ARS requires zero modification. See the [experiment-agent README](https://github.com/Imbad0202/experiment-agent) for setup instructions.

---

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

## Validation Tools

The `tools/` directory contains automated validation scripts (Python stdlib only, no external dependencies):

| Tool | Purpose | Command |
|------|---------|---------|
| **self_test.py** | Structural integrity check (195 checks across 7 categories) | `python tools/self_test.py` |
| **validate_schemas.py** | Handoff schema cross-reference validation | `python tools/validate_schemas.py` |
| **check_schema_versions.py** | Schema versioning and migration registry check | `python tools/check_schema_versions.py` |
| **generate_dependency_graph.py** | Auto-generate Mermaid agent dependency graph | `python tools/generate_dependency_graph.py --output file` |
| **generate_dashboard.py** | Pipeline progress dashboard (HTML) from state JSON | `python tools/generate_dashboard.py --init` |
| **replay_experiments.py** | Re-execute reproducibility scripts and compare outputs | `python tools/replay_experiments.py --dry-run` |

Run `python tools/self_test.py` after making changes to catch regressions.

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
**Statistics:** t-tests, ANOVA, regression, chi-square, SEM, HLM, survival analysis, Bayesian, mediation, MANOVA, and more
**Visualization:** matplotlib/seaborn statistical plots (300 DPI, APA-formatted, colorblind-safe) + Mermaid MCP structural diagrams (CONSORT flow, analysis workflow, DGP architecture, convergence status) + PaperBanana MCP methodology diagrams (optional)

## Optional MCP Integrations

| MCP Server | Purpose | Requires | Used By |
|------------|---------|----------|---------|
| **Mermaid** | Structural diagrams (CONSORT, DGP, decision trees) | MCP connected | experiment-designer, data-analyst, simulation-runner |
| **PaperBanana** | Publication-quality methodology diagrams | `GOOGLE_API_KEY` env var | academic-paper (Methods section) |
| **Google Colab** | GPU-accelerated computation for heavy workloads | Human auth + GPU runtime | simulation-runner, data-analyst |

All MCP integrations are **optional** — the pipeline works without them and degrades gracefully. PaperBanana falls back to Mermaid; Colab falls back to local execution with reduced iterations.

**Google Colab note:** When a workload requires GPU, agents play an audible beep and pause for you to authenticate in Colab and switch the runtime to GPU before proceeding.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on adding agents, modes, schemas, and skills.

## Skill Details

### Deep Research (v2.5)

14-agent pipeline for rigorous academic research:

| Agent | Role |
|-------|------|
| Research Question Agent | FINER-scored RQ formulation |
| Research Architect | Methodology design |
| Bibliography Agent | Systematic literature search (Semantic Scholar + OpenAlex + WebSearch) |
| Source Verification Agent | Evidence grading, predatory journal detection |
| Synthesis Agent | Cross-source integration + methodology distribution analysis |
| Concept Lineage Agent | Intellectual genealogy tracing via citation graph APIs |
| Report Compiler | APA 7.0 report drafting + optional Style Profile + Writing Quality Check |
| Editor-in-Chief | Q1 journal editorial review |
| Devil's Advocate | Assumption challenging (3 checkpoints) + literature assumption audit |
| Ethics Review Agent | AI disclosure, attribution integrity |
| Socratic Mentor | Guided research dialogue with convergence criteria + SCR reflection (togglable) |
| Risk of Bias Agent | RoB 2 + ROBINS-I assessment, traffic-light output |
| Meta-Analysis Agent | Effect sizes, heterogeneity, forest plot data, GRADE |
| Monitoring Agent | Post-pipeline literature monitoring alerts |

**Modes:** full, quick, paper-review, lit-review, fact-check, socratic, **systematic-review**

### Academic Paper (v2.5)

12-agent pipeline for academic paper writing:

| Agent | Role |
|-------|------|
| Intake Agent | Configuration interview + handoff detection + Style Calibration (optional) |
| Literature Strategist | Search strategy + annotated bibliography |
| Structure Architect | Paper outline + word allocation |
| Argument Builder | Thesis + claim-evidence chains |
| Draft Writer | Section-by-section writing + Writing Quality Check sweep + Style Profile application |
| Citation Compliance | Multi-format citation audit + APA↔Chicago↔MLA↔IEEE↔Vancouver conversion |
| Abstract Bilingual | EN + Chinese abstracts |
| Peer Reviewer | 5-dimension review (max 2 rounds) |
| Formatter | LaTeX/DOCX/PDF output — mandatory `apa7` class, XeCJK bilingual, `ragged2e` justification fix, tectonic compilation |
| Socratic Mentor | Chapter-by-chapter guided planning with convergence criteria + SCR reflection (togglable) |
| Visualization Agent | 9 chart types, matplotlib/ggplot2, APA 7.0 standards |
| Revision Coach Agent | Parses unstructured reviewer comments → Revision Roadmap |

**Modes:** full, plan, revision, citation-check, format-convert, bilingual-abstract, writing-polish, full-auto, **revision-coach**

### Academic Paper Reviewer (v1.4)

7-agent multi-perspective review with **0-100 quality rubrics**:

| Agent | Role |
|-------|------|
| Field Analyst | Identifies domain, configures reviewer personas |
| Editor-in-Chief | Journal fit, novelty, significance |
| Methodology Reviewer | Research design, statistics, reproducibility |
| Domain Reviewer | Literature coverage, theoretical framework |
| Perspective Reviewer | Cross-disciplinary, practical impact |
| Devil's Advocate Reviewer | Core thesis challenge, logical fallacy detection, strongest counter-argument |
| Editorial Synthesizer | Consensus analysis, revision roadmap, **rubric-based scoring** |

**Modes:** full, re-review (verification), quick, methodology-focus, guided

**Decision mapping:** ≥80 Accept, 65-79 Minor Revision, 50-64 Major Revision, <50 Reject

### Academic Pipeline (v2.7)

10-stage orchestrator with integrity verification, two-stage review, Socratic coaching, and collaboration evaluation:

| Stage | Skill | Purpose |
|-------|-------|---------|
| 1. RESEARCH | deep-research | Clarify RQ, find literature |
| 2. WRITE | academic-paper | Draft the paper |
| **2.5. INTEGRITY** | **integrity_verification_agent** | **100% reference & data verification (v2.0: anti-hallucination mandate)** |
| 3. REVIEW | academic-paper-reviewer | 5-person review (EIC + R1/R2/R3 + Devil's Advocate) |
| → | *Socratic Revision Coaching* | *Guide user through review feedback* |
| 4. REVISE | academic-paper | Address review comments |
| 3'. RE-REVIEW | academic-paper-reviewer | Verification review of revisions |
| → | *Socratic Residual Coaching* | *Guide user through remaining issues (if Major)* |
| 4'. RE-REVISE | academic-paper | Final revision (if needed) |
| **4.5. FINAL INTEGRITY** | **integrity_verification_agent** | **100% final verification (zero issues required)** |
| 5. FINALIZE | academic-paper | Ask format style → MD + DOCX + LaTeX → tectonic → PDF |
| **6. PROCESS SUMMARY** | **pipeline** | **Paper creation process record + Collaboration Quality Evaluation (1–100)** |

**Pipeline guarantees:**
- Every stage requires user confirmation checkpoint
- Integrity verification (Stage 2.5 + 4.5) cannot be skipped
- Reproducible — standardized process with full audit trail
- Post-pipeline collaboration evaluation with honest, evidence-based scoring

---

## Key Features

1. Adaptive checkpoints (FULL / SLIM / MANDATORY) after every stage
2. Pre-review integrity verification — 100% reference, data, and claim validation (Phase A-E)
3. Two-stage review with Devil's Advocate + 0-100 quality rubrics
4. Socratic revision coaching with SCR Loop (State-Challenge-Reflect, user-togglable) between review and revision stages
5. Final integrity verification before publication
6. Output: MD + DOCX + LaTeX (APA 7.0 `apa7` class / IEEE / Chicago) → PDF via tectonic
7. Post-pipeline process summary with 6-dimension collaboration quality scoring (1–100)
8. Material passport for mid-entry provenance tracking
9. Cross-skill mode advisor (14 scenarios + user archetypes)
10. Style Calibration — learn the author's writing voice from past papers (optional, intake Step 10)
11. Writing Quality Check — writing quality checklist catching overused AI-typical patterns
12. Concept Lineage — trace intellectual genealogy via Semantic Scholar + OpenAlex APIs
13. Audible checkpoint alerts — ascending tones for FULL/MANDATORY checkpoints (cross-platform)

---

## License

This work is licensed under [CC-BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/).

**You are free to:**
- Share — copy and redistribute the material
- Adapt — remix, transform, and build upon the material

**Under the following terms:**
- **Attribution** — You must give appropriate credit
- **NonCommercial** — You may not use the material for commercial purposes

**Attribution format:**
```
Based on Academic Research Skills by Cheng-I Wu
https://github.com/Imbad0202/academic-research-skills
```

---

## Author

**Cheng-I Wu** (吳政宜)

**[mchesbro1](https://github.com/mchesbro1)** — Contributor. Originally proposed and drafted the IS Basket of 8 journals for `academic-paper-reviewer/references/top_journals_by_field.md` ([Issue #5](https://github.com/Imbad0202/academic-research-skills/issues/5)).

**[cloudenochcsis](https://github.com/cloudenochcsis)** — Contributor. Extended the IS section from the *Basket of 8* to the full *Senior Scholars' Basket of 11* — adding *Decision Support Systems*, *Information & Management*, and *Information and Organization* ([Issue #7](https://github.com/Imbad0202/academic-research-skills/issues/7), [PR #8](https://github.com/Imbad0202/academic-research-skills/pull/8)). Sourced from the [AIS Senior Scholars' List of Premier Journals](https://aisnet.org/page/SeniorScholarListofPremierJournals).

---

## Changelog

### v3.15.0 (2026-04-11) — Upstream Merge: PaperOrchestra + Lu 2026 Integration

Merged upstream (Imbad0202) commits through v3.3 while preserving the fork's full experiment pipeline.

**v3.3 — PaperOrchestra-inspired enhancements** (Song, Song, Pfister & Yoon, 2026, [arXiv:2604.05018](https://arxiv.org/abs/2604.05018)):
- **Semantic Scholar API Verification** — Tier 0 programmatic reference existence check via S2 API. Levenshtein >= 0.70 title matching, DOI mismatch detection, bibliography deduplication via S2 IDs. Graceful degradation if API unavailable.
- **Anti-Leakage Protocol** — Knowledge Isolation Directive prioritizes session materials over LLM parametric memory. Flags `[MATERIAL GAP]` for missing content instead of filling from memory.
- **VLM Figure Verification** (optional) — Closed-loop verification of rendered figures using vision-capable LLM. 10-point checklist, max 2 refinement iterations.
- **Score Trajectory Protocol** — Per-dimension rubric score delta tracking across revision rounds (7 dimensions). Detects regressions and triggers mandatory checkpoint.
- **Stage 2 Parallelization** — Visualization and argument building can run in parallel after outline completion.

**v3.2 — Lu 2026 Nature integration** (Lu et al., 2026, *Nature* 651:914-919):
- **7-mode AI Research Failure Mode Checklist** — blocks pipeline at Stage 2.5/4.5 on suspected implementation bugs, hallucinated results, shortcut reliance, bug-as-insight, methodology fabrication, frame-lock. Extends existing 5-type citation hallucination taxonomy.
- **Reviewer Calibration Mode** — opt-in FNR/FPR/balanced-accuracy measurement against user-supplied gold set. 5× ensembling, cross-model default-on.
- **Disclosure Mode** — venue-specific AI-usage statement generator (v1 covers ICLR, NeurIPS, Nature, Science, ACL, EMNLP).
- **Early-Stopping Criterion** — convergence check + budget transparency at pipeline start.
- **Fidelity-Originality Mode Spectrum** — classifies all modes per Lu 2026 Fig 1c.

**v3.1.1 — IS Senior Scholars' Basket of 11**: external contributions from [@mchesbro1](https://github.com/mchesbro1) and [@cloudenochcsis](https://github.com/cloudenochcsis). Added *Decision Support Systems*, *Information & Management*, and *Information and Organization* to the IS journals reference.

**Integration decisions**: Kept all 4 fork-only experiment skills (origin split these into a separate `experiment-agent` repo); kept all 18 handoff schemas (origin trimmed to 10); kept validation tooling (`tools/self_test.py`, `tools/validate_schemas.py`, etc.); kept `concept_lineage_agent` and `citation_graph_apis.md`; kept `.claude-plugin/plugin.json`. Restored upstream's `CHANGELOG.md`, `README.zh-TW.md`, `POSITIONING.md`, `MODE_REGISTRY.md`. Bumped versions: deep-research v2.9, academic-paper v3.0, academic-paper-reviewer v1.8, academic-pipeline v3.3.

### v3.14.0 (2026-04-07) — Upstream Merge: Anti-Sycophancy + Cognitive Frameworks
- Merged 8 upstream commits (origin v3.0-v3.1): devil's advocate concession threshold protocol, intent detection, cross-model verification, AI Self-Reflection Report, anti-context-rot anchors, cognitive frameworks (argumentation, review quality, writing judgment).

### v3.9.1 (2026-03-28) — Audible Checkpoint Alerts + Schema Fix
- **Audible checkpoint alerts**: FULL and MANDATORY pipeline checkpoints now play ascending tones (`tools/beep.sh`) so users know the pipeline has paused. Cross-platform (Windows/macOS/Linux). SLIM checkpoints remain silent and auto-continue.
- **Schema 10 collision fix**: Style Profile moved from Schema 10 → Schema 17 (Schema 10 was already Experiment Design)

### v3.9.0 (2026-03-28) — Citation Graph APIs & Concept Lineage Agent
- **Concept Lineage Agent** (deep-research, 14th agent): Traces intellectual genealogy of central concepts via Semantic Scholar + OpenAlex APIs. Citation chain tracing (origin → challenges → refinements → consensus), API-first with graceful degradation
- **Enhanced synthesis_agent**: Methodology distribution analysis + enriched gap analysis
- **Enhanced devils_advocate_agent**: Literature assumption audit at Checkpoint 2
- **Enhanced bibliography_agent**: Three-tier search (Semantic Scholar + OpenAlex + WebSearch)
- New handoff Schema 16: Concept Lineage Report
- Versions: deep-research v2.5

### v3.8.0 (2026-03-22) — Validation Tooling & Schema Formalization
- `tools/self_test.py`: 195 structural integrity checks
- Schema 14 (Methodology Blueprint) + Schema 15 (INSIGHT Collection) formalized
- FINER scale alignment (1-10), reviewer count propagation (5 reviewers), agent hardening

### v3.5.1 (2026-03-18) — Experiment Handoff Documentation
- Schema 11/12 integration documented in 3 academic-paper agents (draft_writer, abstract_bilingual, argument_builder)

### v2.9 (2026-03-27) — Style Calibration + Writing Quality Check
- **Style Calibration** (academic-paper intake Step 10, optional): Provide 3+ past papers and the pipeline learns your writing voice — sentence rhythm, vocabulary preferences, citation integration style. Applied as a soft guide during drafting; discipline conventions always take priority. Priority system: discipline norms (hard) > journal conventions (strong) > personal style (soft). See `shared/style_calibration_protocol.md`
- **Writing Quality Check** (`academic-paper/references/writing_quality_check.md`): Writing quality checklist applied during draft self-review. 5 categories: AI high-frequency term warnings (25 terms), punctuation pattern control (em dash ≤3), throat-clearing opener detection, structural pattern warnings (Rule of Three, uniform paragraphs, synonym cycling), and burstiness checks (sentence length variation). These are good writing rules — not detection evasion
- **Style Profile** carried through academic-pipeline Material Passport (Schema 17 in `shared/handoff_schemas.md`)
- **deep-research** report compiler also consumes both features optionally
- Versions: academic-paper v2.5, deep-research v2.4, academic-pipeline v2.7

### v2.8 (2026-03-22) — SCR Loop Phase 1: State-Challenge-Reflect
- **Socratic Mentor Agent** (deep-research + academic-paper): SCR (State-Challenge-Reflect) protocol integration
  - **Commitment Gates**: Collect user predictions before presenting evidence at each layer/chapter transition
  - **Certainty-Triggered Contradiction**: Detect high-confidence language ("obviously", "clearly") and introduce counterpoints
  - **Adaptive Intensity**: Track commitment accuracy, dynamically adjust challenge frequency
  - **Self-Calibration Signal (S5)**: New convergence signal tracking user's self-calibration growth across dialogue
  - **SCR Switch**: Users can say "skip the predictions" to disable or "turn predictions back on" to re-enable mid-dialogue; Socratic questioning continues normally
- `deep-research/references/socratic_questioning_framework.md`: SCR Overlay Protocol mapping SCR phases to Socratic functions
- Added `CHANGELOG.md`

### v2.7 (2026-03-09) — Integrity Verification v2.0: Anti-Hallucination Overhaul
- **integrity_verification_agent v2.0**: Anti-Hallucination Mandate (no AI memory verification), eliminated gray-zone classifications (VERIFIED/NOT_FOUND/MISMATCH only), mandatory WebSearch audit trail for every reference, Stage 4.5 fresh independent verification, Gray-Zone Prevention Rule
- **Known Hallucination Patterns**: 5-type taxonomy (TF/PAC/IH/PH/SH) from GPTZero × NeurIPS 2025 study, 5 compound deception patterns, real-world case study, literature statistics
- **Post-publication audit**: Full WebSearch verification of all 68 references found 21 issues (31% error rate) that passed 3 rounds of integrity checks — proving the necessity of external verification
- **Paper corrections**: Removed 4 fabricated references, fixed 6 author errors, corrected 7 metadata errors, fixed 2 format issues

### v2.6.2 (2026-03-09) — Intent-Based Mode Activation
- **deep-research**: Socratic mode now uses **intent-based activation** instead of keyword matching. Works in any language — detects meaning (e.g., "user wants guided thinking") rather than matching specific strings.
- **academic-paper**: Plan mode now uses **intent-based activation**. Detects intent signals like "user is uncertain how to start" or "user wants step-by-step guidance" in any language.
- Both modes now have a **default rule**: when intent is ambiguous, prefer `socratic`/`plan` over `full` — safer to guide first.
- Two-layer architecture: Layer 1 (skill activation) uses bilingual keywords for matching confidence; Layer 2 (mode routing) uses language-agnostic intent signals.

### v2.6.1 (2026-03-09) — Bilingual Trigger Keywords
- **deep-research**: Added Traditional Chinese trigger keywords for general activation and Socratic mode.
- **academic-paper**: Added Traditional Chinese trigger keywords and Plan Mode trigger section.
- Both mode selection guides now include bilingual examples and Chinese-specific misselection scenarios.

### v2.6 / v2.4 / v1.4 (2026-03-08) — 15+ Improvements
- **deep-research v2.3**: New systematic-review / PRISMA mode (7th); 3 new agents (risk_of_bias, meta_analysis, monitoring); PRISMA protocol/report templates; Socratic convergence criteria (4 signals + auto-end); Quick Mode Selection Guide
- **academic-paper v2.4**: 2 new agents (visualization, revision_coach); revision tracking template with 4 status types; citation format conversion (APA↔Chicago↔MLA↔IEEE↔Vancouver); statistical visualization standards; Socratic convergence criteria; revision recovery example; **LaTeX output hardening** — mandatory `apa7` document class, text justification fix (`ragged2e` + `etoolbox`), table column width formula, bilingual abstract centering, standardized font stack (Times New Roman + Source Han Serif TC VF + Courier New), PDF via tectonic only
- **academic-paper-reviewer v1.4**: Quality rubrics with 0-100 scoring and behavioral indicators; decision mapping (≥80 Accept, 65-79 Minor, 50-64 Major, <50 Reject); Quick Mode Selection Guide
- **academic-pipeline v2.6**: Adaptive checkpoint system (FULL/SLIM/MANDATORY); Phase E Claim Verification in integrity checks; Material Passport for mid-entry provenance; cross-skill mode advisor (14 scenarios); team collaboration protocol; enhanced handoff schemas (9 schemas); integrity failure recovery example

### v2.4 / v1.3 (2026-03-08)
- **academic-pipeline v2.4**: New Stage 6 PROCESS SUMMARY — auto-generates structured paper creation process record (MD → LaTeX → PDF, bilingual); mandatory final chapter: **Collaboration Quality Evaluation** with 6 dimensions scored 1–100 (Direction Setting, Intellectual Contribution, Quality Gatekeeping, Iteration Discipline, Delegation Efficiency, Meta-Learning), honest feedback, and improvement recommendations; pipeline expanded from 9 to 10 stages

### v2.3 / v1.3 (2026-03-08)
- **academic-pipeline v2.3**: Stage 5 FINALIZE now prompts for formatting style (APA 7.0 / Chicago / IEEE); PDF must compile from LaTeX via `tectonic` (no HTML-to-PDF); APA 7.0 uses `apa7` document class (`man` mode) with XeCJK for bilingual CJK support; font stack: Times New Roman + Source Han Serif TC VF + Courier New

### v2.2 / v1.3 (2025-03-05)
- **Cross-Agent Quality Alignment**: unified definitions (peer-reviewed, currency rule, CRITICAL severity, source tier) across all agents
- **deep-research v2.2**: synthesis anti-patterns, Socratic auto-end conditions, DOI+WebSearch verification, enhanced ethics integrity check, mode transition matrix
- **academic-paper v2.2**: 4-level argument scoring, plagiarism screening, 2 new failure paths (F11 Desk-Reject Recovery, F12 Conference-to-Journal), Plan→Full mode conversion
- **academic-paper-reviewer v1.3**: DA vs R3 role boundaries, CRITICAL finding criteria, consensus classification (4/3/SPLIT/DA-CRITICAL), confidence score weighting, Asian & Regional Journals reference
- **academic-pipeline v2.2**: checkpoint confirmation semantics, mode switching matrix, failure fallback matrix, state ownership protocol, material version control

### v2.0.1 (2026-03)
- **Simplify 4 SKILL.md** (-371 lines, -16.5%): remove cross-skill duplication, inline templates → file references, redundant routing tables, duplicate mode selection sections
- Fix revision loop cap contradiction between academic-paper and academic-pipeline

### v2.0 (2026-02)
- **academic-pipeline v2.0**: 5→9 stages, mandatory integrity verification, two-stage review, Socratic revision coaching, reproducibility guarantees
- **academic-paper-reviewer v1.1**: +Devil's Advocate Reviewer (7th agent), +re-review mode (verification), +post-review Socratic coaching
- New agent: `integrity_verification_agent` — 100% reference/data verification with audit trail
- New agent: `devils_advocate_reviewer_agent` — 8-dimension thesis challenger
- Output order: MD + DOCX → ask LaTeX → confirm → PDF

### v1.0 (2026-02)
- Initial release
- deep-research v2.0 (10 agents, 6 modes including socratic)
- academic-paper v2.0 (10 agents, 8 modes including plan)
- academic-paper-reviewer v1.0 (6 agents, 4 modes including guided)
- academic-pipeline v1.0 (orchestrator)
