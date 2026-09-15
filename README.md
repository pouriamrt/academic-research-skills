# Academic Research Skills for Claude Code

[![Version](https://img.shields.io/badge/version-v3.22.0-blue)](https://github.com/pouriamrt/academic-research-skills)
[![License: CC BY-NC 4.0](https://img.shields.io/badge/license-CC%20BY--NC%204.0-lightgrey)](https://creativecommons.org/licenses/by-nc/4.0/)

A Claude Code plugin covering the full academic research lifecycle — from literature review through experimentation, statistical analysis, paper writing, peer review, and publication. **8 skills, 58+ agents, 20 handoff schemas + 6 claim-audit schemas**, full pipeline orchestration with PRISMA-trAIce + RAISE compliance gates, reviewer + writer/evaluator sprint contracts, opt-in L3 claim ↔ reference faithfulness audit gate (v3.18.0 #103), passport reset boundary for long-running sessions, three-layer citation locator, temporal verification (v3.18.0 #135), Phase Boundary protocol (v3.18.0 #133), cross-index triangulation (v3.18.0 #102), and collaboration depth observer. **v3.17.0 runs the pipeline unattended by default — set `ARS_INTERACTIVE=1` to restore prompts.** English-only output. New `/ars-mark-read`, `/ars-unmark-read`, `/ars-reviewer` plugin commands. Experiment skills integrate with the [superpowers](https://github.com/obra/superpowers) plugin for disciplined, test-driven code development.

## Skills

**Install in 30 seconds** (Claude Code CLI / VS Code / JetBrains, v3.17.0+; plugin packaging from upstream v3.7.0):

```text
/plugin marketplace add Imbad0202/academic-research-skills
/plugin install academic-research-skills
```

Then try `/ars-plan` to walk through your paper structure via Socratic dialogue, or jump to [Quick install](#quick-install) for prerequisites and the traditional symlink flow.

> **AI is your copilot, not the pilot.** This tool won't write your paper for you. It handles the grunt work — hunting down references, formatting citations, verifying data, checking logical consistency — so you can focus on the parts that actually require your brain: defining the question, choosing the method, interpreting what the data means, and writing the sentence after "I argue that."
>
> Style Calibration learns your voice from past work. Writing Quality Check catches the patterns that make prose feel machine-generated, and `scripts/check_prose_tells.py` scans for the mechanically detectable ones with `file:line` evidence. The goal is prose you would have written yourself.

### Why human-in-the-loop, not full automation?

Lu et al. (2026, *Nature* 651:914-919) built **The AI Scientist** — the first fully autonomous AI research system to publish a paper through blind peer review at a top-tier ML venue (ICLR 2025 workshop, score 6.33/10 vs workshop average 4.87). Their Limitations section enumerates the failure modes that any fully-autonomous AI research pipeline inherits: implementation bugs, hallucinated results, shortcut reliance, bug-as-insight reframing, methodology fabrication, frame-lock, citation hallucinations.

ARS is built on the premise that **a human researcher augmented by AI avoids these failure modes better than either alone**. Stage 2.5 and Stage 4.5 integrity gates run a 7-mode blocking checklist (see [`academic-pipeline/references/ai_research_failure_modes.md`](academic-pipeline/references/ai_research_failure_modes.md)); the reviewer offers an opt-in calibration mode that measures its own FNR/FPR against a user-supplied gold set.

[**Zhao et al.**](https://arxiv.org/abs/2605.07723) (2026-05) audited 111M references across 2.5M papers on arXiv, bioRxiv, SSRN, and PMC. Their conservative estimate is 146,932 hallucinated citations for 2025 alone, with an observed mid-2024 inflection; for the bioRxiv-to-PMC pairing they report 85.3% preprint-to-published persistence. The paper describes "real citations deployed to support claims the cited references do not actually make" as an open challenge. ARS v3.7.1 added trust-chain frontmatter for source provenance; v3.7.3 added locator infrastructure (three-layer citation anchors) for future claim-level audits and surfaces advisory risk signals at cite time (ARS labels the claim-faithfulness gap internally as "L3"; this is ARS terminology, not the paper's). v3.7.x is motivated by Zhao et al.'s corpus-scale findings; corpus-scale evaluation of ARS itself remains future work.

v3.8 closes the second half of the L3 gap. v3.7.3 made every citation carry a locator anchor; v3.8 adds an opt-in audit pass (`ARS_CLAIM_AUDIT=1`) that fetches the cited source against each anchor and judges whether the claim is actually supported. Five new HIGH-WARN classes (claim-not-supported, negative-constraint-violation, fabricated-reference, anchorless, constraint-violation-uncited) gate-refuse output through the formatter terminal hard gate. Calibration is shipped as a 20-tuple gold set with FNR<0.15 + FPR<0.10 acceptance thresholds; ramp-on plan is deferred to post-calibration evidence per v3.8 spec §5.

[**Ren et al.**](https://arxiv.org/abs/2607.13104) (2026, *Self-Improvements in Modern Agentic Systems: A Survey*) supplies a third, survey-level anchor. Its scientific-discovery synthesis (§7.4) concludes that discovery agents cannot easily verify novelty, correctness, or reproducibility on their own and may exploit weak proxies instead, must manage evidence across heterogeneous tools and literature, and raise governance issues — "scientific writing can also amplify misinformation when the evidence is weak." Its generation-loop chapters (§5.1–§5.2) list human auditing and retained human anchors among the practical safeguards for self-generated evaluation loops, and its historical chapter (§2.2) records the oldest form of the same lesson: the practical success of Lenat's EURISKO depended heavily on the user serving as the external evaluation signal, pruning unproductive heuristic drift — a limitation the survey notes persists in modern agentic systems. ARS cites the survey as design rationale for its human-in-the-loop stance, not as empirical proof that human-in-the-loop pipelines outperform autonomous ones; the survey's actionable deltas for ARS are tracked in #539–#541 and #547–#550.

[**Gartenberg et al.**](https://doi.org/10.1287/orsc.2026.ed.v37.n3) (2026, *Organization Science* 37(3):795-812, "More versus better") supplies a fourth anchor, and the first from the journal side. The *Organization Science* AI Task Force scored every first submission (6,957) and every text-format review (10,389) the journal received between January 2021 and February 2026 with a commercial AI-writing classifier and standard readability indices. Manuscripts scored as heavily AI-written read worse on those indices and were desk-rejected more often; reviews scored as more AI-written leaned toward theory and away from data; and the editors conclude that current AI tools, amplified by publish-or-perish incentives, "appear to be pushing the system toward an equilibrium of more rather than better research." Their §5 contrasts "cognitive surrender" (Shaw & Nave, 2026, as cited there) with human-first use and asks authors to disclose how a manuscript was produced. The evidence is observational, aggregate, and from one journal, and the classifier is a proprietary instrument. ARS cites the editorial as design rationale for recording volume as a non-goal (see `POSITIONING.md`) and for the Collaboration Depth Observer and the claim-strength ladder, not as evidence about ARS output; the actionable deltas are tracked in #829–#833.

[**Wang, Li et al.**](https://arxiv.org/abs/2609.07713) (2026-09, *The Emerging AI Paper-Review Arms Race: Adversarial Co-Evolution in Scholarly Publishing*, a survey of 230 sources) supplies a fifth anchor, and the first that treats research production and peer review as one coupled system. Its evaluative-authority ladder (§4.1) runs from author-facing feedback through reviewer assistance and official AI reviews to scoring and decision support, with the survey's point that capability at one rung does not justify use at the next; ARS's simulated panel sits on the lowest rung by design (see `POSITIONING.md`). Two of its findings shape the reviewer roadmap. First, as the survey summarizes Dycke & Gurevych (2026, §4.5), 391 edits that break a paper's scientific support relations produced no statistically significant difference in the tested automated reviewers' aspects, sentiment, or scores compared with 540 soundness-neutral controls, while presentation-only rewrites with the science held fixed moved AI-review scores (§5.2); the survey's §9.2 conclusion is that a static evaluation can overstate an AI reviewer's reliability once authors can observe and adapt to it. ARS tracks the corresponding Round-1 paired controls in #871 and the author-identity-cue controls (§7.2) in #872; both are measurements, not new mechanisms. Second, its §9.1 cites Brodeur et al. (2026, *PNAS* 123(22):e2524747123), a randomized study in which 288 researchers in 103 teams reproduced published quantitative social-science results under three conditions: human-only, AI-assisted (ChatGPT as a collaborative tool), and AI-led (ChatGPT with minimal human oversight). Human-only and AI-assisted teams reproduced 94% and 91%, AI-led teams 37%, and the AI-assisted teams detected fewer major coding errors than the human-only teams. In that study, then, AI assistance did not verify better than humans alone and AI-led verification did much worse; ARS reads this as a reason to keep verification human-led at every checkpoint, not as evidence that its own checkpoints or integrity gates are effective. The survey is a synthesis rather than an experiment, its structured search stops at 2026-07-01 and the later targeted update did not rerun every query (§10), its deployment evidence is concentrated in a small number of AI/CS conferences, OpenReview-based settings, and selected journals, and its "arms race" framing is a lens, not a finding; ARS cites it as design rationale, not as evidence about ARS output.

v3.3 was inspired by [**PaperOrchestra**](https://arxiv.org/abs/2604.05018) (Song, Song, Pfister & Yoon, 2026, Google): Semantic Scholar API verification, anti-leakage protocol, VLM figure verification, and revision-trajectory tracking. ARS now implements that last idea through categorical, evidence-anchored criterion trajectories rather than score deltas.

---

| Skill | Agents | What it does | Key Modes |
|-------|--------|-------------|-----------|
| **deep-research** v2.9.4 | 14 | Research team with concept lineage, systematic review, PRISMA, meta-analysis, Semantic Scholar API verification | full, quick, socratic*, review, lit-review, fact-check, systematic-review |
| **experiment-designer** v1.0.1 | 6 | Experiment protocol, power analysis, instruments, randomization | full, guided*, quick, power-only, instrument |
| **data-analyst** v1.0.1 | 7 | Statistical analysis execution with APA-formatted results | full, guided*, quick, assumption-check, exploratory, replication |
| **simulation-runner** v1.0.1 | 5 | Monte Carlo, bootstrap, agent-based models, parameter sweeps | full, guided*, quick, power-sim, sensitivity, bootstrap |
| **lab-notebook** v1.0.1 | 4 | Experiment research record with provenance tracking | full, log-entry, deviation, snapshot, export, audit |
| **academic-paper** v3.2.0 | 11 | English-only paper writing with experiment integration, LaTeX output, anti-leakage protocol, VLM figure verification, disclosure mode | full, plan*, outline-only, revision, revision-coach, abstract-only, lit-review, format-convert, citation-check, disclosure |
| **academic-paper-reviewer** v1.9.1 | 7 | Multi-perspective peer review (EIC + 3 reviewers + Devil's Advocate + optional cross-model DA critique) with calibration + sprint-contract gates; auto-routes from machine-readable verdict | full, re-review, quick, methodology-focus, guided*, calibration |
| **academic-pipeline** v3.17.0 | 4 in-skill + 1 shared (`compliance_agent`) | Auto-by-default pipeline orchestrator with AI Research Failure Mode Checklist (Lu 2026), score trajectory tracking, early-stopping, PRISMA-trAIce + RAISE compliance (Schema 19), sprint-contract gates (Schema 20 / 20.1), passport reset boundary, collaboration depth observer | auto-detected stages |

`*` = mode only fires when `ARS_INTERACTIVE=1` is set. In auto mode (default) the orchestrator forces `mode=full` on every dispatched sub-skill.

See the [Quick Reference Card](docs/QUICK_REFERENCE.md) for a full "I want to X → use skill Y in mode Z" lookup table, [MODE_REGISTRY.md](MODE_REGISTRY.md) for the single source of truth on all 24+ modes (with spectrum / output / oversight / triggers), and [POSITIONING.md](POSITIONING.md) for the design philosophy and allowed/discouraged uses.

## Architecture & pipeline

**👉 [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)** — the full pipeline view: flow diagram, stage-by-stage matrix, data-access flow, skill dependency graph, quality gates, and mode list. (Fork extends with experiment Stage 1.5.)

## Quick install

**Prerequisites**

- [Claude Code](https://docs.claude.com/en/docs/claude-code/setup) (latest; plugin packaging requires recent versions)
- `ANTHROPIC_API_KEY` exported, or set on first `claude` run
- *Optional:* Pandoc for DOCX (via Pandoc when available); Markdown + instructions otherwise. Tectonic + Source Han Serif TC for APA 7.0 PDF. Markdown output works without either.
- *Optional (real Python):* needed only for the write-scope guard and a few opt-in commands; the core skills are prompt-driven. Details, including the Windows notes on Git Bash and the Microsoft Store Python stub, are in [docs/SETUP.md § Python (optional)](docs/SETUP.md#python-optional).

> **Which controls are active in *your* install channel?** Availability varies by install channel. See the per-channel map: [docs/CONTROL_AVAILABILITY.md](docs/CONTROL_AVAILABILITY.md).

**Plugin install (v3.17.0+, recommended):**

```text
/plugin marketplace add pouriamrt/academic-research-skills
/plugin install academic-research-skills
```

(Upstream channel: `Imbad0202/academic-research-skills` — fork omits the experiment pipeline.)

**Verify it works:** run `/ars-plan` and describe a paper you're working on — ARS will start a Socratic dialogue to map out chapter structure. For a single-shot test instead, try `/ars-lit-review "your topic"`.

**👉 [docs/SETUP.md](docs/SETUP.md)** — full guide: install Claude Code, set up API keys, optional Pandoc/tectonic for DOCX/PDF, cross-model verification (`ARS_CROSS_MODEL`), and six installation methods (Plugin, project skills, global skills, claude.ai Project, repo-cloned, Claude Science import).

**👉 [docs/DATA_FLOWS.md](docs/DATA_FLOWS.md)** — what leaves your machine (bibliographic resolvers, optional consent-gated cross-model calls, the plugin update check), what is cached locally, for how long, and how to turn each path off.

**👉 [docs/RISK_REGISTER.md](docs/RISK_REGISTER.md)** — the standing risks the suite knows about, which existing controls address each one, the evidence status behind those controls, and what remains open.

**Using Claude Science?** The eight skills import directly: **Skills → Import from GitHub**, paste `https://github.com/pouriamrt/academic-research-skills`, **Preview**, then **Import 8 skills** (requires v3.20.0+ of this fork — the importer reads the explicit skill paths in the marketplace manifest). Imports are point-in-time snapshots: re-import after ARS updates. Imported skills carry the ARS methodology (research / writing / review protocols); Claude Code-specific machinery — slash commands, hooks, subagent orchestration — does not transfer. See [docs/SETUP.md](docs/SETUP.md) Method 5 for details.

**Using Codex CLI?** Upstream maintains a sibling distribution at [`Imbad0202/academic-research-skills-codex`](https://github.com/Imbad0202/academic-research-skills-codex) — same workflow content, Codex-native packaging. Fork has not yet been ported to Codex.

**Third-party platforms and integrations** that wrap or host ARS are listed in [THIRD_PARTY.md](THIRD_PARTY.md) — community-submitted and not reviewed or endorsed by the maintainer.

**Governance:** who decides, what cross-model review does and does not provide, and the project's end-of-life posture are stated in [GOVERNANCE.md](GOVERNANCE.md); security reporting and triage in [SECURITY.md](SECURITY.md).

## Performance & cost

**👉 [docs/PERFORMANCE.md](docs/PERFORMANCE.md)** — per-mode token budgets, full-pipeline estimate (~$4–6 for a 15k-word paper), and recommended Claude Code settings (Auto mode; Agent Team optional).

## Guides & articles

- [Academic Writing Shouldn't Be a Solo Act](https://open.substack.com/pub/edwardwu223235/p/academic-writing-shouldnt-be-a-solo?r=4dczl&utm_medium=ios) — upstream's full pipeline walkthrough

## Pipeline

<p align="center">
  <img src="assets/pipeline.png" alt="Academic Research Pipeline" width="700"/>
</p>

The experiment stages (1.5) are auto-detected from the methodology blueprint produced by deep-research. Literature reviews, theoretical papers, and policy analyses skip straight to writing.

- **Deep Research** — 14-agent research team with concept lineage, Socratic guided mode + systematic review / PRISMA + SCR Loop + **intent detection** + **dialogue health monitoring** + **optional cross-model DA** + **argumentation & reasoning cognitive framework** + **Semantic Scholar API verification** (v3.3 PaperOrchestra)
- **Experiment Designer / Data Analyst / Simulation Runner / Lab Notebook** — 4 experiment skills (22 agents) with auto-detected pipeline integration, power analysis, APA-formatted statistics, Monte Carlo / bootstrap / SEM / HLM, full provenance tracking, and superpowers integration for disciplined code development
- **Academic Paper** — 11-agent English-only paper writing with experiment results integration (Schema 11/12), Style Calibration, Writing Quality Check, LaTeX output hardening, visualization, revision coaching, citation conversion, **writing judgment framework**, **anti-leakage protocol**, **VLM figure verification**, **disclosure mode** (venue-specific AI usage statements), and **v3.6.6/v3.6.8 generator-evaluator sprint contract** for paper drafting (Schema 20.1, renumbered from upstream 13.1)
- **Academic Paper Reviewer** — Multi-perspective peer review with criterion-bound, evidence-anchored narrative judgements (Journal-Fit Reviewer + 3 dynamic reviewers + Devil's Advocate) with **concession threshold protocol** + **attack intensity preservation** + **optional cross-model review**) + **R&R traceability matrix** + **read-only constraint** + **review quality thinking framework** + **calibration mode** (FNR/FPR measurement against gold-standard sets) + **v3.6.2 sprint-contract hard gate** for reviewers (Schema 20, renumbered from upstream 13). Current live reviews remain `NOT_CALIBRATED`; full calibration produces a bounded candidate profile, while live-profile application is not yet wired.
- **Academic Pipeline** — Full pipeline orchestrator (10 stages + experiment re-entry) with adaptive checkpoints, audible alerts, claim verification, Material Passport, **optional cross-model integrity verification**, **mid-conversation reinforcement**, **self-check questions**, narrative criterion-by-criterion regression checks (the typed trajectory carrier is deferred), **early-stopping criterion**, **AI Research Failure Mode Checklist** (Lu 2026 — 7-mode taxonomy, mandatory blocking at Stage 2.5/4.5), **PRISMA-trAIce + RAISE compliance** (Schema 19, v3.4.0+), and **passport reset boundary** for long-running sessions (v3.6.3+)

## Upstream features adopted in v3.16

- **Data Access Level Metadata** (v3.3.2+) — every skill declares `data_access_level` (`raw` / `redacted` / `verified_only`); enforced by `scripts/check_data_access_level.py`. Pattern adapted from Anthropic's automated-w2s-researcher (2026). See [`shared/ground_truth_isolation_pattern.md`](shared/ground_truth_isolation_pattern.md).
- **Task Type Annotation** (v3.3.2+) — every skill declares `task_type` (`open-ended` or `outcome-gradable`).
- **Benchmark Report Schema** (v3.3.5+) — JSON Schema + lint for honest benchmark comparisons.
- **Artifact Reproducibility Lockfile** (v3.3.5+) — optional `repro_lock` sub-block on Material Passport. **Configuration documentation, not replay guarantee.**
- **Literature corpus adapter contract** (v3.6.4+) + **consumer integration** (v3.6.5+) — bring-your-own bibliography via Zotero / Obsidian / folder scan adapters.
- **Trust-chain frontmatter** (v3.7.1+) + **claim faithfulness locator** (v3.7.3+) — three-layer citation anchors with NO-LOCATOR hard gate.
- **Model Tiering** (#517, v3.16+) — optional `ARS_MODEL_TIERING` switch with two directions: `economy` (execution-type agents dispatch one tier below the session model, floor Opus-class) and `quality-boost` (judgment-type agents at integrity gates and final review step up to the frontier tier). Default unset = byte-equivalent to pre-#517 behavior. See [`shared/model_tiering.md`](shared/model_tiering.md).
- **Canonical Cross-Model Handoff Envelope** (#527, v3.17+) — the owner→dispatcher→owner blind-checkpoint transport path (#523) now has a machine-stable `[CROSS-MODEL-HANDOFF v1]` envelope with a normative Python grammar (`scripts/cross_model_handoff.py`) instead of prose-only enforcement, pinning agreement/divergence/malformed-result routing across all three checkpoint owners. See [`shared/cross_model_verification.md`](shared/cross_model_verification.md) §"Cross-model handoff envelope".
- **Experiment Provenance Intake** (#260) — optional `experiment_provenance[]` on the Material Passport records experiments run **outside the ARS experiment skills** (the fork's experiment-designer / data-analyst / simulation-runner produce Schema 11/12 records natively; `experiment_provenance[]` covers externally run experiments), and manuscript claims join to them via `claim_intent_manifest.planned_experiment_ids[]`. The integrity gate (Stage 2.5/4.5) audits each experiment-backed claim against declared provenance — `ALIGNED` / `OVERSTATED` / `NOT_SUPPORTED_BY_PROVENANCE` / `PROVENANCE_INSUFFICIENT` — **without judging whether the experiment itself was correct**. A fail-closed `experiment_intake_declaration` makes "did you run experiments?" an explicit Stage 1 decision (even literature-only runs declare `no_experiments_declared`). See [`shared/handoff_schemas.md`](shared/handoff_schemas.md) §"Experiment Provenance Intake (#260)".

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

**Integrity and verification boundary:** ARS checks the manuscript and the reported process—including citation existence, claim–source alignment, reported methodology, declared experiment–result alignment, figure/table fidelity, and reporting/process/package conformance. Some checks are sampled or LLM-mediated. ARS does **not** establish that procedures were actually performed, raw data are authentic, or results reproduce; a consistently reported fabrication can pass these checks. See [POSITIONING.md § Integrity checks and the empirical-work boundary](POSITIONING.md#integrity-checks-and-the-empirical-work-boundary).

---

## Showcase: real pipeline output

See the complete artifacts from a real 10-stage pipeline run — peer review reports, integrity verification reports, and the final paper:

**[Browse all pipeline artifacts →](examples/showcase/)**

| Artifact | Description |
|---|---|
| [Final Paper](examples/showcase/full_paper_apa7.pdf) | APA 7.0 formatted, LaTeX-compiled |
| [Integrity Report — Pre-Review](examples/showcase/integrity_report_stage2.5.pdf) | Stage 2.5: caught 15 fabricated refs + 3 statistical errors |
| [Integrity Report — Final](examples/showcase/integrity_report_stage4.5.pdf) | Stage 4.5: zero regressions confirmed |
| [Peer Review Round 1](examples/showcase/stage3_review_report.pdf) | Journal-Fit Reviewer + 3 Reviewers + Devil's Advocate |
| [Re-Review](examples/showcase/stage3prime_rereview_report.pdf) | Verification after revisions |
| [Peer Review Round 2](examples/showcase/stage3_review_report_r2.pdf) | Follow-up review |
| [Response to Reviewers](examples/showcase/response_to_reviewers_r2.pdf) | Point-by-point author response |
| [Post-Publication Audit Report](examples/showcase/post_publication_audit_2026-03-09.pdf) | Independent full-reference audit: found 21/68 issues missed by 3 rounds of integrity checks |

---

## Built-in Experiment Pipeline

This fork ships with **4 experiment skills** (22 agents) that auto-detect from the methodology blueprint and run inline within the pipeline. No external companion repo required. (Upstream Imbad0202 maintains the [Experiment Agent](https://github.com/Imbad0202/experiment-agent) as a separate skill — fork has it built in.)

```
Stage 1 RESEARCH  →  RQ Brief + Methodology Blueprint
        ↓
Stage 1.5 EXPERIMENT (auto-detected)
  ├─ experiment-designer → protocol, power analysis, instruments
  ├─ data-analyst        → real-data statistics with APA reporting
  ├─ simulation-runner   → Monte Carlo / bootstrap / SEM / HLM / ABM
  └─ lab-notebook        → provenance tracking + deviation log
        ↓
Stage 2 WRITE  →  paper with verified experiment results integrated
```

**Schema flow**: experiment-designer (Schema 10/13) → data-analyst / simulation-runner (Schema 11) → lab-notebook (Schema 12) → academic-paper (integrated into Methods + Results sections).

**Reviewer-driven re-entry**: if reviewers request new experimental data, the editorial synthesizer flags items with `requires_new_experiment = true` and the pipeline re-enters Stage 1.5-R / 1.5-R2 before text revision. Users can opt out and convert items to Acknowledged Limitations.

**Code discipline**: complex experiment code (custom DGPs, SEM, agent-based models, multi-step analysis pipelines) auto-invokes the [superpowers](https://github.com/obra/superpowers) plugin's TDD workflow with scientific test patterns (known-answer tests, synthetic data validation, reproducibility checks).

> **Upstream alternative**: the upstream suite (Imbad0202) splits experiment work into a separate [experiment-agent](https://github.com/Imbad0202/experiment-agent) companion repo. This fork takes the opposite design: experiments are built in. If you prefer the lean writer-focused upstream + standalone experiment-agent, use the upstream repo instead.

**Stage 1 intake declaration (#260)**: at Stage 1, ARS detects whether the run will carry experiment-backed claims and sets a fail-closed `experiment_intake_declaration` on the Material Passport. If you ran experiments externally, the scholar enters one `experiment_provenance[]` entry per experiment (`experiment_id`, nested `repro_lock`, `planned_vs_executed[]`, `negative_results[]`, `known_limitations[]`) and the declaration is set to `experiments_declared`; if not, it is set to `no_experiments_declared`. The declaration is **required on every post-#260 passport** — a run that touches no experiments still declares `no_experiments_declared`, so the integrity gate can never be silently bypassed by a forgotten provenance block. The `experiment_id`s are frozen at this intake point; the writers later reference them via `planned_experiment_ids[]`.

**Teaching-side companion**: [Teaching Skills](https://github.com/YujxZJCN/teaching-skills) applies the ARS architecture (skill ensembles, shared contracts, staged gates, a Course Passport) to the teaching side of academic life — course design → lessons → assessment → delivery → reflection; its `sotl` mode hands classroom-inquiry projects off to ARS deep-research / academic-paper for the publication phase.

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
| **self_test.py** | Structural integrity check (196+ checks across 7 categories) | `python tools/self_test.py` |
| **validate_schemas.py** | Handoff schema cross-reference validation | `python tools/validate_schemas.py` |
| **check_schema_versions.py** | Schema versioning and migration registry check | `python tools/check_schema_versions.py` |
| **generate_dependency_graph.py** | Auto-generate Mermaid agent dependency graph | `python tools/generate_dependency_graph.py --output file` |
| **generate_dashboard.py** | Pipeline progress dashboard (HTML) from state JSON | `python tools/generate_dashboard.py --init` |
| **replay_experiments.py** | Re-execute reproducibility scripts and compare outputs | `python tools/replay_experiments.py --dry-run` |

Run `python tools/self_test.py` after making changes to catch regressions. CI workflows under `.github/workflows/` (added by upstream v3.6.x): `pytest.yml`, `spec-consistency.yml`, `freshness-check.yml`.

## Mode reference (per skill)

#### Deep Research (8 modes)

```
"Research the impact of AI on higher education"       → full mode
"Give me a quick brief on X"                          → quick mode
"Do a systematic review on X with PRISMA"             → systematic-review mode
"Guide my research on X"                              → socratic mode (guided)
"Fact-check these claims"                             → fact-check mode
"Do a literature review on X"                         → lit-review mode
"Compare these papers in WHY/HOW/WHAT format"         → three-way-scan mode
"Review this paper's research quality"                → review mode
```

#### Academic Paper (11 modes)

```
"Write a paper on X"                                  → full mode
"Guide me through writing a paper"                    → plan mode (guided)
"Build a paper outline"                               → outline-only mode
"I have a draft, here are reviewer comments"          → revision mode
"Parse these reviewer comments into a roadmap"        → revision-coach mode
"Write an abstract for this paper"                    → abstract-only mode
"Turn this into a literature review paper"            → lit-review mode
"Convert to LaTeX" / "Convert citations to IEEE"      → format-convert mode
"Check citations"                                     → citation-check mode
"Generate an AI disclosure statement for NeurIPS"     → disclosure mode
"Audit my rebuttal draft against the reviews"         → rebuttal-audit mode
```

#### Academic Paper Reviewer (6 modes)

```
"Review this paper"                                   → full mode (Journal-Fit Reviewer + R1/R2/R3 + Devil's Advocate)
"Quick assessment of this paper"                      → quick mode
"Guide me to improve this paper"                      → guided mode
"Check the methodology"                               → methodology-focus mode
"Verify the revisions"                                → re-review mode
"Calibrate this reviewer against my gold set"         → calibration mode
```

#### Academic Pipeline (Orchestrator)

```
"I want to write a complete research paper"           → full pipeline from Stage 1
"I already have a paper, review it"                   → mid-entry at Stage 2.5 (integrity first)
"I received reviewer comments"                        → mid-entry at Stage 4
```

> Pipeline ends with **Stage 6: Process Summary** — auto-generates a paper creation process record with 6-dimension Collaboration Quality Evaluation (1–100 scoring).

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

> A condensed cross-skill matrix (per-agent responsibilities, per-stage artifacts) lives in [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md). The detailed agent rosters below are the fork's authoritative reference.

### Deep Research (v2.9.4)

14-agent pipeline for rigorous academic research:

| Agent | Role |
|-------|------|
| Research Question Agent | FINER-scored RQ formulation |
| Research Architect | Methodology design + Methodology Blueprint (Schema 14) |
| Bibliography Agent | Systematic literature search (Semantic Scholar + OpenAlex + WebSearch) with **Tier 0 S2 API verification** |
| Source Verification Agent | Evidence grading, predatory journal detection, **DOI mismatch detection** |
| Synthesis Agent | Cross-source integration + methodology distribution analysis |
| Concept Lineage Agent | Intellectual genealogy tracing via citation graph APIs |
| Report Compiler | APA 7.0 report drafting + optional Style Profile + Writing Quality Check |
| Editor-in-Chief | Q1 journal editorial review |
| Devil's Advocate | Assumption challenging (3 checkpoints) + literature assumption audit + **concession threshold protocol (1-5 scale, no concession below 4)** |
| Ethics Review Agent | AI disclosure, attribution integrity |
| Socratic Mentor | Guided research dialogue with convergence criteria + SCR reflection (togglable) + **intent detection** |
| Risk of Bias Agent | RoB 2 + ROBINS-I assessment, traffic-light output |
| Meta-Analysis Agent | Effect sizes, heterogeneity, forest plot data, GRADE |
| Monitoring Agent | Post-pipeline literature monitoring alerts |

**Modes:** full, quick, review, lit-review, fact-check, socratic, **systematic-review**

### Experiment Designer / Data Analyst / Simulation Runner / Lab Notebook (v1.0 each)

Four experiment skills (22 agents total) auto-detected from the methodology blueprint:

| Skill | Agents | Purpose |
|-------|--------|---------|
| **experiment-designer** | 6 | Protocol design, power analysis, instruments, randomization, EQUATOR/CONSORT compliance, simulation specification (Schema 13) |
| **data-analyst** | 7 | Real-data statistical analysis, assumption testing, APA-formatted reporting, effect size interpretation, visualization |
| **simulation-runner** | 5 | Monte Carlo, bootstrap, agent-based models, parameter sweeps, convergence diagnostics, parallel execution |
| **lab-notebook** | 4 | Experiment record with provenance tracking, deviation logging, file manifest, reproducibility audit |

**Schema flow:** experiment-designer (Schema 10/13) → data-analyst / simulation-runner (Schema 11) → lab-notebook (Schema 12) → academic-paper

**Superpowers integration:** complex code (custom DGPs, SEM, ABM, multi-step pipelines) auto-invokes superpowers TDD workflow with scientific test patterns (known-answer, synthetic data, reproducibility).

### Academic Paper (v3.2.0)

| Agent | Role |
|-------|------|
| Intake Agent | Configuration interview + handoff detection + Style Calibration (optional) |
| Literature Strategist | Search strategy + annotated bibliography (with corpus-first integration, v3.6.5+) |
| Structure Architect | Paper outline + word allocation |
| Argument Builder | Thesis + claim-evidence chains |
| Draft Writer | Section-by-section writing + English abstract + 5-7 keywords inline + Writing Quality Check sweep + Style Profile application + **Anti-Leakage Protocol** (knowledge isolation) + **v3.6.6 writer sprint contract** (Phase 4a/4b) + **v3.7.3 three-layer citation emission** |
| Citation Compliance | Multi-format citation audit + APA↔Chicago↔MLA↔IEEE↔Vancouver conversion |
| Peer Reviewer | 5-dimension review (max 2 rounds) + **v3.6.6 evaluator sprint contract** (Phase 6a/6b) |
| Formatter | LaTeX/DOCX/PDF output — mandatory `apa7` class, `ragged2e` justification fix, tectonic compilation + **v3.7.3 NO-LOCATOR hard-gate refusal** |
| Socratic Mentor | Chapter-by-chapter guided planning with convergence criteria + SCR reflection (togglable) |
| Visualization Agent | 9 chart types, matplotlib/ggplot2, APA 7.0 standards + **VLM Figure Verification** (optional closed-loop visual quality check) |
| Revision Coach Agent | Parses unstructured reviewer comments → Revision Roadmap |

**Modes:** full, plan, outline-only, revision, revision-coach, abstract-only, lit-review, format-convert, citation-check, **disclosure** (venue-specific AI usage statement)

### Academic Paper Reviewer (v1.9.1)

7-agent multi-perspective review with **criterion-bound narrative judgements** and the **v3.6.2 sprint contract hard gate**. No numerical total is mapped to Accept, Minor Revision, Major Revision, or Reject; live reviews remain `NOT_CALIBRATED`. First-round review panel vs. contract-governed re-review dispatch boundary: see ARCHITECTURE.md §3 Stage 3 / Stage 3'.

| Agent | Role |
|-------|------|
| Field Analyst | Identifies domain, configures reviewer personas |
| Editor-in-Chief | Journal fit, novelty, significance + sprint contract Phase 1/2 |
| Methodology Reviewer | Research design, statistics, reproducibility + sprint contract Phase 1/2 |
| Domain Reviewer | Literature coverage, theoretical framework + sprint contract Phase 1/2 |
| Perspective Reviewer | Cross-disciplinary, practical impact + sprint contract Phase 1/2 |
| Devil's Advocate Reviewer | Core thesis challenge, logical fallacy detection, strongest counter-argument + **concession threshold protocol** + **attack intensity preservation** |
| Editorial Synthesizer | Consensus analysis, revision roadmap with `requires_new_experiment` flags, **criterion-bound judgements** + **R&R traceability matrix (Schema 18)** + **three-step mechanical synthesis protocol (v3.6.2)** |

**Modes:** full, re-review (verification), quick, methodology-focus, guided, **calibration** (FNR/FPR/balanced accuracy measurement against gold-standard sets)


**Optional cross-model verification:** set `ARS_CROSS_MODEL` to use GPT-5.4 Pro or Gemini 3.1 Pro as an independent second reviewer.

### Academic Pipeline (v3.22.0; suite-version-pinned, auto-by-default)

Pipeline orchestrator with integrity verification, compliance, sprint-contract gates, two-stage review, experiment re-entry, Socratic coaching, passport reset boundary, and collaboration evaluation:

| Stage | Skill | Purpose |
|-------|-------|---------|
| 1. RESEARCH | deep-research | Clarify RQ, find literature (with corpus-first integration v3.6.5+), produce Methodology Blueprint |
| **1.5. EXPERIMENT** *(auto-detected)* | experiment-designer → data-analyst / simulation-runner → lab-notebook | Run experiments if methodology requires them |
| 2. WRITE | academic-paper | Draft the paper (with Anti-Leakage Protocol + v3.6.6 writer sprint contract + v3.7.3 three-layer citations) |
| **2.5. INTEGRITY** | **integrity_verification_agent** + **compliance_agent (v3.4+)** | **100% reference & data verification + 7-mode AI Research Failure Mode Checklist + PRISMA-trAIce + RAISE compliance (Schema 19)** |
| 3. REVIEW | academic-paper-reviewer | 5-person review with **v3.6.2 sprint contract gate (Schema 20)** for each reviewer + **v3.6.6 evaluator gate (Schema 20.1)** for in-pair |
| → | *Socratic Revision Coaching* | *Guide user through review feedback* |
| **1.5-R. EXPERIMENT RE-ENTRY** *(if `requires_new_experiment`)* | experiment-designer / data-analyst / simulation-runner | Run new experiments requested by reviewers |
| 4. REVISE | academic-paper | Address review comments (with **Score Trajectory tracking**) |
| 3'. RE-REVIEW | academic-paper-reviewer | Verification review of revisions |
| → | *Socratic Residual Coaching* | *Guide user through remaining issues (if Major)* |
| **1.5-R2. EXPERIMENT RE-ENTRY 2** *(final opportunity)* | experiment-designer / data-analyst / simulation-runner | Last chance for new experimental data |
| 4'. RE-REVISE | academic-paper | Final revision (if needed) |
| **4.5. FINAL INTEGRITY** | **integrity_verification_agent** + **compliance_agent** | **100% final verification + 7-mode failure checklist + final compliance check (independent re-run, zero issues required)** |
| 5. FINALIZE | academic-paper | Ask format style → MD + DOCX + LaTeX → tectonic → PDF |
| **6. PROCESS SUMMARY** | **pipeline + collaboration_depth_agent (v3.5+)** | **Paper creation process record + AI Self-Reflection Report + Collaboration Quality Evaluation (1–100) + Collaboration Depth Observer (4-dimension score)** |

**Pipeline guarantees:**
- Every stage requires user confirmation checkpoint (FULL / SLIM / MANDATORY)
- Integrity + compliance verification (Stage 2.5 + 4.5) cannot be skipped
- 7-mode AI Research Failure Mode Checklist is mandatory and blocking; no `--no-block` escape hatch
- Experiment stages auto-detected and conditional on methodology blueprint
- Reviewer requests for new data trigger experiment re-entry (user can opt out → Acknowledged Limitation)
- Reproducible — standardized process with full audit trail
- Post-pipeline collaboration evaluation with honest, evidence-based scoring
- Score trajectory tracking detects revision regressions across 7 quality dimensions
- Early-stopping criterion + budget transparency at pipeline start
- **v3.6.3 passport reset boundary** — opt-in `ARS_PASSPORT_RESET=1` for cross-session resume from Material Passport ledger ([`academic-pipeline/references/passport_as_reset_boundary.md`](academic-pipeline/references/passport_as_reset_boundary.md))
- **v3.6.7 downstream-agent pattern protection** — hardens 13/18 documented hallucination/drift patterns in synthesis/research-architect/report-compiler agents
- **v3.7.1+ trust-chain frontmatter** + **v3.7.3 three-layer citation locator** — NO-LOCATOR hard-gate refusal at finalizer

---

## Key Features

### Pipeline orchestration
1. Adaptive checkpoints (FULL / SLIM / MANDATORY) after every stage
2. Auto-detected experiment stages (1.5) — pipeline runs experiments only when the methodology requires them
3. Experiment re-entry stages (1.5-R, 1.5-R2) — reviewer requests for new data trigger conditional re-execution
4. Material passport for mid-entry provenance tracking
5. Cross-skill mode advisor (14 scenarios + user archetypes)
6. Audible checkpoint alerts — ascending tones for FULL/MANDATORY checkpoints (cross-platform)

### Integrity & failure-mode prevention
7. Pre-review integrity verification — 100% reference, data, and claim validation (Phase A-E)
8. **7-mode AI Research Failure Mode Checklist** (Lu 2026) — mandatory blocking at Stage 2.5/4.5; covers implementation bugs, hallucinated results, shortcut reliance, bug-as-insight, methodology fabrication, frame-lock, and citation hallucinations
9. **Semantic Scholar API verification** (Tier 0) — programmatic reference existence check with Levenshtein title matching and DOI mismatch detection
10. **Anti-leakage protocol** — Knowledge Isolation Directive prioritizes session materials over LLM parametric memory; flags `[MATERIAL GAP]` for missing content
11. Final integrity verification before publication (independent re-run, not just delta check)

### Review & revision
12. Two-stage review with Devil's Advocate + 0-100 quality rubrics + **concession threshold protocol** (1-5 scale, no concession below 4)
13. **Reviewer calibration mode** — opt-in FNR/FPR/balanced-accuracy measurement against user-supplied gold-standard sets
14. **Score trajectory tracking** — per-dimension rubric score delta tracking across revision rounds with regression detection
15. Socratic revision coaching with SCR Loop (State-Challenge-Reflect, user-togglable) between review and revision stages
16. **Cross-model verification** (optional) — set `ARS_CROSS_MODEL` to use GPT-5.4 Pro or Gemini 3.1 Pro as an independent second reviewer
17. **R&R traceability matrix** (Schema 18) — every reviewer concern tracked with explicit status

### Writing quality & disclosure
18. Output: MD + DOCX + LaTeX (APA 7.0 `apa7` class / IEEE / Chicago) → PDF via tectonic
19. **Disclosure mode** — venue-specific AI usage statement generator (v1 covers ICLR, NeurIPS, Nature, Science, ACL, EMNLP)
20. **Style Calibration** — learn the author's writing voice from past papers (optional, intake Step 10)
21. **Writing Quality Check** — writing quality checklist catching overused AI-typical patterns
22. **VLM figure verification** (optional) — closed-loop visual quality check using a vision-capable LLM with 10-point checklist

### Research depth
23. **Concept lineage** — trace intellectual genealogy via Semantic Scholar + OpenAlex APIs
24. **Argumentation reasoning framework** (Toulmin, Bradford Hill, IBE) for research design
25. **Review quality thinking framework** (three lenses, reviewer traps, calibration questions)
26. **Writing judgment framework** (clarity test, reader's journey, voice, revision matrix)
27. **Fidelity-Originality mode spectrum** — classifies all 24+ modes for predictability vs exploration trade-offs

### Process & meta
28. Post-pipeline process summary with 6-dimension collaboration quality scoring (1–100)
29. **AI Self-Reflection Report** (Stage 6) — concession rate, health alerts, sycophancy risk rating
30. Early-stopping criterion + budget transparency estimate at pipeline start
31. Mid-conversation reinforcement protocol with stage-specific IRON RULE + Anti-Pattern reminders

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
Based on Academic Research Skills (full-pipeline fork) by Pouria Mortezaagha
https://github.com/pouriamrt/academic-research-skills
Built on the upstream skills suite by Cheng-I Wu
https://github.com/Imbad0202/academic-research-skills
```

---

## Authors & Contributors

### Fork maintainer

**Pouria Mortezaagha** ([pouriamrt](https://github.com/pouriamrt)) — Maintains the full-lifecycle fork. Designed and built the experiment pipeline (4 skills: `experiment-designer`, `data-analyst`, `simulation-runner`, `lab-notebook`), the visualization pipeline (Phase 4.5), the concept lineage agent + Semantic Scholar/OpenAlex protocol, the validation tooling (`tools/self_test.py`, `tools/validate_schemas.py`, `tools/check_schema_versions.py`, `tools/replay_experiments.py`, `tools/generate_dependency_graph.py`, `tools/generate_dashboard.py`, `tools/beep.sh`), the experiment-aware handoff schemas (10-18), the experiment re-entry stages, audible checkpoint alerts, and superpowers integration for code-heavy experiment skills. Continuously merges improvements from the upstream suite while preserving the full-pipeline scope.

### Upstream author

**Cheng-I Wu** ([Imbad0202](https://github.com/Imbad0202)) — Original author of the [upstream skills suite](https://github.com/Imbad0202/academic-research-skills). Built the core writing-and-review skills (`deep-research`, `academic-paper`, `academic-paper-reviewer`, `academic-pipeline`) and contributes ongoing improvements that this fork integrates: anti-sycophancy protocols (v3.0), anti-context-rot refactoring + cognitive frameworks (v3.1), Lu 2026 failure-mode integration (v3.2 — 7-mode checklist, calibration mode, disclosure mode, mode spectrum), and PaperOrchestra integration (v3.3 — Semantic Scholar API, anti-leakage protocol, VLM figure verification, score trajectory).

### External contributors (via upstream)

**[mchesbro1](https://github.com/mchesbro1)** — Originally proposed and drafted the IS Basket of 8 journals for `academic-paper-reviewer/references/top_journals_by_field.md` ([Issue #5](https://github.com/Imbad0202/academic-research-skills/issues/5)).

**[cloudenochcsis](https://github.com/cloudenochcsis)** — Extended the IS section from the *Basket of 8* to the full *Senior Scholars' Basket of 11* — adding *Decision Support Systems*, *Information & Management*, and *Information and Organization* ([Issue #7](https://github.com/Imbad0202/academic-research-skills/issues/7), [PR #8](https://github.com/Imbad0202/academic-research-skills/pull/8)). Sourced from the [AIS Senior Scholars' List of Premier Journals](https://aisnet.org/page/SeniorScholarListofPremierJournals).

**[devCharlotte](https://github.com/devCharlotte)** — Contributor. Translated the upstream Korean README (`README.ko-KR.md`, upstream-only — this fork is English-only) ([PR #469](https://github.com/Imbad0202/academic-research-skills/pull/469)).

**[Yaobin29](https://github.com/Yaobin29)** — Contributor. Proposed reviewer-response tooling in [PR #433](https://github.com/Imbad0202/academic-research-skills/pull/433); the `deep-research three-way-scan` mode and the `academic-paper rebuttal-audit` mode (rescued from the PR's `audit` concept) were integrated from that contribution in v3.12.1.

**[ktao732084-arch](https://github.com/ktao732084-arch)** — Contributor. Expanded the `academic-paper` disclosure system with nine medical-publishing policy targets, target-specific required-fact intake, and fail-closed standalone rendering ([Issue #596](https://github.com/Imbad0202/academic-research-skills/issues/596), [PR #599](https://github.com/Imbad0202/academic-research-skills/pull/599)); expanded the EQUATOR clinical-reporting reference with condensed CARE, STARD and TRIPOD+AI guidance plus a fail-closed study-design routing sequence ([Issue #594](https://github.com/Imbad0202/academic-research-skills/issues/594), [PR #601](https://github.com/Imbad0202/academic-research-skills/pull/601)); and designed and contributed the standalone Chinese-literature resolver, API protocol, and synthetic transport-fixture suite ([Issue #595](https://github.com/Imbad0202/academic-research-skills/issues/595), [PR #600](https://github.com/Imbad0202/academic-research-skills/pull/600)).

**[didacrios](https://github.com/didacrios)** — Contributor. Translated the Spanish README upstream; this English-only fork does not ship it.

---

## Changelog



Only the three most recent releases are summarized here. The full release history is in [CHANGELOG.md](CHANGELOG.md).

### v3.22.0 (2026-08-03) — Deterministic prose-tells scanner
- **`scripts/check_prose_tells.py`**: stdlib scanner for the four mechanically detectable AI copy tells (`copy-em-dash`, `copy-antithesis`, `hype-copy`, `copy-servile`) with `file:line` evidence. Flags: `--json`, `--strict`, `--exclude-quotes`, stdin via `-`. Skips fenced code blocks; `copy-ignore` exempts a line
- **Wired as the deterministic pass** opening `academic-paper/references/writing_quality_check.md`. Sections A–E keep the judgment calls regex cannot make. The scanner count is now reported; judgment findings stay internal
- **Anti-humanizer positioning retired**: the anti-detection-evasion framing is removed from README, POSITIONING, both design-boundary blockquotes, and two SKILL.md clauses. CONTRIBUTING's decision principle governing it is deleted (4 principles → 3). The non-removable `disclosure_addendum` mechanism is unchanged — the compliance ladder enforces it in code, so it never rested on the policy
- MIT port from jcarterjohnson/vibecoded-design-tells via humanizer-stack; attribution in `THIRD_PARTY.md`. The CC BY-SA-derived `humanizer/SKILL.md` was deliberately not vendored (license incompatible with this repo's NC terms)

### v3.21.0 (2026-08-03) — Upstream sync: v3.17.0 → v3.19.0+ (re-review three-gate contract, role-scoped reviewer scoring, risk-stratified claim gate)

Merges 51 upstream commits (Imbad0202 `039d94f` → `49e79a7`, spanning upstream v3.18.0 and v3.19.0) onto the fork's v3.20.1 baseline via a true git merge — 364 files, 46 conflicts resolved by hand. **Adopted:** the #576 three-gate re-review contract (criteria committed before the revision is seen, evidence verdicts before the author's persuasion), #574 role-scoped reviewer scoring with typed evidence anchors and abstention, #549 risk-stratified Stage 2.5 claim verification (100% of HIGH-IMPACT claims + a 10% random sentinel, replacing the flat 30% sample), #547 scope-conformance and #548 search-bounded novelty advisories, #569/#570 revision-round claim-drift guards, #512 PDF read-integrity preflight, #513 `read_scope` attestation on `/ars-mark-read`, #541 verification-cache staleness advisory, #540/#539 cross-model reviewer and judge-independence tracks, #544 SessionStart update reminder, #595 Chinese-literature resolver client, and bare `/ars-*` command aliases (#633). **Fork-side:** English-only surfaces stay deleted, fork schema numbering (18 / 20 / 20.1) and the experiment pipeline (Stage 1.5a/b/c re-entry, Phase F) survive inside upstream's rewritten files, and every file arriving from upstream was brought up to the fork's ruff gate.

### v3.20.0 (2026-07-16) — Upstream sync: v3.13.0 → v3.17.0 (boundary semantics, cross-model envelope, model tiering, panel checker)

Merges 54 upstream commits (Imbad0202 v3.13.0 → v3.17.0) onto the fork's v3.19.0 baseline via a true git merge. Bilingual additions (zh-CN/ja-JP/ko-KR READMEs, Korean trigger keywords + routing fixtures) NOT merged — fork stays English-only. Highlights: Stage 5/6 boundary semantics with terminal acknowledgement (#528/#529, AUTO-mode adapted) + whole-file content locks; canonical `[CROSS-MODEL-HANDOFF v1]` envelope + dispatcher contract (#527/#523); opt-in model tiering (#517) with the classification fork-extended 39 → 61 agents (the 4 experiment skills + `concept_lineage`); cross-model gate hardening + blind disagreement checkpoints (#518); executable sprint-contract panel checker + majority-formula fix (#510); machine-readable degradation registry (#511); tools allowlist + defrift lock (#514/#524); CARS intro-rhetoric + title-crafting reference (#500); WP advisory generalization (#501/#505); OpenAlex auth + backoff (#495); Claude Science importability with all 8 fork skills declared (#480); vendored release-discipline toolkit. Full detail in `CHANGELOG.md` [3.20.0].
