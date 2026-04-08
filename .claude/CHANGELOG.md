# Academic Research Skills Changelog

Cross-skill fixes and update history.

---

## 2026-04-07

### v3.14.0 — Upstream Merge: Anti-Sycophancy, Cognitive Frameworks, Reference Extraction

**Merged 8 upstream commits (origin v3.0-v3.1) into fork (v3.13).**

**New content from upstream**:
- 20+ new reference files: protocols, cognitive frameworks, review guides, changelogs
- Devil's advocate agents with concession threshold protocol (1-5 scale, no concession below 4)
- Socratic mentor intent detection layer + dialogue health indicator
- Cross-model verification protocol (`shared/cross_model_verification.md`)
- Argumentation reasoning framework (Toulmin, Bradford Hill, IBE)
- QUICKSTART.md onboarding guide

**Integration fixes**:
- Renumbered R&R Traceability Matrix: Schema 11 -> Schema 18 (collision fix)
- Wired 22 new reference files into 4 SKILL.md reference tables
- Fixed cross-reference path format in devils_advocate_agent.md
- Removed dead README.zh-TW.md link from QUICKSTART.md
- Updated schema count 17 -> 18 across CLAUDE.md, README, CONTRIBUTING

**Conflict resolution**: Kept fork's SKILL.md, CLAUDE.md, README as authoritative. Accepted upstream's new files and agent enhancements.

---

## 2026-04-03

### v3.13.0 — 6-Agent Team Review: 24 Issues Fixed, Phase F Defined

**Files changed**: 10 files across 5 skills + shared + pipeline agents + plugin config

**High-priority fix**:
- **Schema compatibility matrix**: Added Schema 16-17 columns to `shared/schema_migrations.md` Version Compatibility Matrix (previously only covered Schemas 1-15). Added v3.9.0+ row for full version coverage.

**Medium-priority fixes**:
- **Phase F defined**: Added complete reproducibility script re-execution protocol (F1-F4) to `academic-pipeline/agents/integrity_verification_agent.md`. Previously referenced but never defined. Includes script discovery, execution, output comparison, and script-paper consistency check with sampling strategies for both Mode 1 and Mode 2.
- **Stage 4.5 fallback corrected**: Fixed `pipeline_orchestrator_agent.md` Skill Failure Fallback Matrix: Stage 4.5 FAIL was incorrectly routing to "Stage 5 (revision)" (Stage 5 is FINALIZE). Now correctly says "fix and re-verify within Stage 4.5 (max 3 rounds)".
- **State machine diagram**: Added Stage 6 (PROCESS SUMMARY) to ASCII state diagram in `pipeline_state_machine.md` (was shown in legal transitions table but missing from diagram).
- **Schema number annotations**: Added explicit Schema N references to `deep-research/SKILL.md` handoff protocol (Schemas 1-3, 14-16), `academic-paper/SKILL.md` handoff section (Schemas 1-3, 14-16), and `academic-paper-reviewer/SKILL.md` (Schemas 6-7 with cross-reference to `shared/handoff_schemas.md`).
- **Stale counts fixed**: `CONTRIBUTING.md` (16 -> 17 schemas, Schema 1-15 -> 1-17, added 2 missing shared/ files), `schema_migrations.md` prose (1-15 -> 1-17), `academic-pipeline/SKILL.md` (9 schemas -> 17, version table 2.7 -> 2.8).
- **Schema 17 version**: Fixed `schema_migrations.md` Schema 17 (Style Profile) established version from v2.9.0 to v3.9.0 (was pre-v3.x era typo).

**Low-priority fixes**:
- Added experiment re-entry material tracking (`experiment_results_revision`, `experiment_results_revision_2`) to `state_tracker_agent.md` materials registry and version control table
- Fixed `state_tracker_agent.md` example JSON `pipeline_version` from "2.7" to "2.8"
- Clarified `requires_data_collection` flag as informational (not a routing trigger) in orchestrator agent
- Added Concept Lineage Report + INSIGHT Collection + Methodology Blueprint to pipeline orchestrator handoff material transfer table
- Annotated all CLAUDE.md handoff protocol materials with Schema numbers
- Fixed self_test check count in CLAUDE.md (195 -> 196)

---

### v3.12.0 — Deep Plugin Audit: 16 Issues Fixed Across All Skills

**Files changed**: 14 files across 7 skills + shared + tools + plugin config

**Critical fixes**:
- **Schema count alignment**: Updated `tools/self_test.py`, `tools/check_schema_versions.py`, and `tools/generate_dashboard.py` to recognize all 17 schemas (previously expected 15-16, missing Schema 16 Concept Lineage Report and Schema 17 Style Profile)
- **Schema migrations**: Added Schema 16-17 to `shared/schema_migrations.md` Current Versions table
- **Version synchronization**: Updated `README.md` badge (v3.9.1 -> v3.12.0), `marketplace.json` (v3.8.0 -> v3.12.0), added missing CHANGELOG entries for v3.9.1, v3.10.0, v3.11.0
- **Systematic-review spec gap**: Added `concept_lineage_agent` to `deep-research/SKILL.md` systematic-review mode Phase 3 (was listed in mode table but missing from workflow diagram)

**High-priority fixes**:
- **Mode routing**: Added `revision-coach` mode to `academic-paper/agents/intake_agent.md` Mode Detection and Paper Configuration Record (was defined in SKILL.md but missing from intake routing)
- **Visualization agent**: Added Mermaid MCP and PaperBanana MCP documentation to `academic-paper/agents/visualization_agent.md` with clear responsibility boundaries vs `draft_writer_agent`

**Medium-priority fixes**:
- Added Stage 6 (Process Summary) to `academic-pipeline/examples/full_pipeline_example.md`
- Added Experiment Re-Entry Detection section to `academic-pipeline/agents/pipeline_orchestrator_agent.md`
- Added `requires_new_experiment` flag example to `academic-paper-reviewer/agents/editorial_synthesizer_agent.md` Revision Roadmap template
- Documented figure regeneration protocol in revision mode (`academic-paper/agents/draft_writer_agent.md`)
- Documented user opt-out prompting for Stage 3' -> 1.5-R2 in orchestrator agent

**Low-priority fixes**:
- Added auto-logging protocol note to `lab-notebook/SKILL.md` Integration section
- Added `revision_recovery_example.md` to `academic-paper/SKILL.md` examples table
- Clarified LaTeX template vs formatter agent relationship
- Documented dynamic template selection in academic-paper SKILL.md
- Clarified auto-logging phase numbering in `shared/experiment_infrastructure.md`

---

### v3.11.0 (2026-04-03) — Visualization Pipeline & Superpowers Gates

- Wired visualization pipeline for publication-ready papers with figures
- Injected superpowers classification gates into experiment agent workflows

### v3.10.0 (2026-03-28) — Experiment Pipeline Fix

- Fixed experiment pipeline: auto-detection, full-mode enforcement, revision re-entry

### v3.9.1 (2026-03-28) — Version Bump

- Bumped version to 3.9.1 in plugin.json and CLAUDE.md

---

## 2026-03-28

### v3.9.0 — Citation Graph APIs, Concept Lineage Agent & Literature Analysis Enhancements

**Files changed**: 9 files across deep-research + shared + plugin config

**New agent** (`deep-research/agents/concept_lineage_agent.md`):
- 14th agent in deep-research pipeline — traces intellectual genealogy of 3-5 central concepts
- Uses Semantic Scholar API (citation context, intents, influential citations) and OpenAlex API (bibliometrics, topic hierarchy, FWCI) via WebFetch
- Produces concept lineage trees: origin → challenges → refinements → current consensus
- API-first with 3-tier graceful degradation (both APIs → one API → WebSearch inference)
- Rate-limited: ≤100 API calls per run, exponential backoff on 429
- Runs in Phase 3 parallel with synthesis_agent

**New reference** (`deep-research/references/citation_graph_apis.md`):
- Comprehensive API reference for Semantic Scholar Academic Graph API and OpenAlex API
- Endpoint documentation, field specifications, rate limits, error handling
- Combined workflow patterns for concept lineage tracing and enhanced bibliography search
- Filter semantics guide (OpenAlex `cites:` vs `cited_by:` — counterintuitive naming documented)

**New handoff schema** (`shared/handoff_schemas.md`):
- **Schema 16: Concept Lineage Report** — ConceptLineage, SourceRef, ChallengeEntry, RefinementEntry, ConsensusAssessment objects with full field specifications and example

**Enhanced agents**:
- `synthesis_agent`: Added Step 1.5 (Methodology Distribution Analysis — aggregates method types across corpus, identifies dominant/underrepresented/weakest methods). Enhanced Step 4 (Gap Analysis — now includes Closest Paper and Proposed Methodology per gap). Added Concept Lineage integration section
- `devils_advocate_agent`: Checkpoint 2 now includes Literature Assumption Audit sub-task — extracts shared untested assumptions across surveyed papers with reliance mapping and consequence analysis. New output section: "Shared Literature Assumptions" table
- `bibliography_agent`: Added WebFetch to Required Tools. Step 2 (Execute Search) now uses three-tier search: Tier 1 (Semantic Scholar + OpenAlex APIs), Tier 2 (WebSearch), Tier 3 (domain-specific databases)

**Plugin-level updates**:
- `.claude/CLAUDE.md`: Agent count 57→58, schema count 15→16, deep-research v2.4→v2.5, added Semantic Scholar + OpenAlex to Optional MCP Capabilities, updated handoff protocol, version 3.8.0→3.9.0
- `deep-research/SKILL.md`: Agent count 13→14, Phase 3 updated for parallel concept lineage, version 2.4→2.5, updated operational modes table, handoff protocol, agent references, reference files table

---

## 2026-03-27

### Style Calibration + Writing Quality Check (v2.9)

**Files changed**: 10 files across `academic-paper/`, `deep-research/`, `academic-pipeline/`, `shared/`, root

**New files**:
- `shared/style_calibration_protocol.md`: Full calibration flow (6 dimensions: sentence length, paragraph length, vocabulary preferences, citation integration, modifier style, register shifts). Priority system: discipline norms (hard) > journal conventions (strong) > personal style (soft). Conflict resolution with user notification.
- `academic-paper/references/writing_quality_check.md`: Writing quality checklist (5 categories: 25-term AI high-frequency word warnings, punctuation pattern control, throat-clearing detection, structural pattern warnings, burstiness checks). Not a humanizer — good writing rules applicable regardless of author.

**Modified agents**:
- `academic-paper/agents/intake_agent.md`: New Step 10 (Style Calibration, optional). Renumbered Funding Sources to Step 11. Added `style_profile` field to Paper Configuration Record.
- `academic-paper/agents/draft_writer_agent.md`: Step 1 pre-writing checklist gains Style Profile + Writing Quality Check items. Step 2 self-review gains Step 7 (style & lint check).
- `deep-research/agents/report_compiler_agent.md`: New sections for optional Style Calibration and Writing Quality Check before Writing Style Guidelines.
- `academic-pipeline/agents/pipeline_orchestrator_agent.md`: Style Profile carry-through in Material Passport.

**Schema update**:
- `shared/handoff_schemas.md`: Schema 17 (Style Profile) with 8 required fields, 3 optional fields, consumption priority system, and example.

**SKILL.md updates**:
- `academic-paper/SKILL.md`: v2.4 -> v2.5
- `deep-research/SKILL.md`: v2.3 -> v2.4
- `academic-pipeline/SKILL.md`: v2.6 -> v2.7

**README updates**: EN + zh-TW both updated with v2.9 badge, new features in Features list, and changelog entry.

**Design rationale**: The original proposal included 4 features (Argue-First Gate, Skeleton Drafting, Weighting, Style Calibration) under a "Jarvis Framework". Analysis showed Argue-First Gate, Skeleton Drafting, and Weighting overlapped 60-90% with existing Socratic convergence signals, Plan Mode Chapter Summary, and Integrity Verification respectively. Only Style Calibration was genuinely new. Writing Quality Check was adopted from Type A humanizer research (term/pattern replacement) as a writing quality improvement, explicitly not for AI detection evasion.

---

## 2026-03-22

### v3.7.0 — Cross-Skill Integrity Audit & Schema Formalization

**Files changed**: 16 files across 7 skills + shared + plugin config

**Critical fixes**:
- **FINER scale alignment** (`deep-research/agents/research_question_agent.md`): Changed FINER scoring from 1-5 to 1-10 scale to match Schema 1 data contract in `shared/handoff_schemas.md`. Updated score table anchors, output format, and minimum thresholds (avg >= 6.0, no criterion below 4)
- **Reviewer count propagation** (`academic-paper-reviewer/agents/field_analyst_agent.md`, `editorial_synthesizer_agent.md`): Updated from 4 to 5 reviewers (EIC + 3 Peer + Devil's Advocate) in configuration protocol, report inventory table, quality gates, decision letter template, and Part 3 summary. DA column added to synthesis table with CRITICAL findings tracking

**Schema additions** (`shared/handoff_schemas.md`):
- **Schema 14: Methodology Blueprint** — formalized the routing artifact produced by `research_architect_agent` and consumed by `pipeline_orchestrator_agent`. Includes routing flags (`requires_experiment_design`, `requires_simulation`), method/data/validity fields, and IRB/preregistration metadata
- **Schema 15: INSIGHT Collection** — formalized the Socratic dialogue output with typed insight objects (scope_decision, methodology_choice, theoretical_anchor, etc.) and FINER dimension mapping

**Agent hardening**:
- Added Required Tools sections (tool name, purpose, criticality, fallbacks) to 5 critical agents: `integrity_verification_agent`, `bibliography_agent`, `power_analyst_agent`, `analysis_executor_agent`, `draft_writer_agent`
- Added **Dual-Pass Self-Verification Protocol** to `integrity_verification_agent`: adversarial self-check on VERIFIED verdicts, citation context double-check, internal consistency audit. Mandatory for Mode 2 (Stage 4.5)

**Version/metadata fixes**:
- Fixed `2025-03-05` → `2026-03-05` date typos in 4 SKILL.md changelogs + CHANGELOG.md
- Fixed `academic-pipeline/SKILL.md` version info table (v2.6 → v2.7) and added v2.7 changelog entry
- Removed stale "(future skill)" label from `data-analyst` reference in `experiment-designer/SKILL.md`
- Added Stage 6 (PROCESS SUMMARY) to pipeline flow in `.claude/CLAUDE.md`

---

## 2026-03-18

### v3.5.1 — Experiment Handoff Documentation & Cross-Agent Wiring

**Files changed**: 5 files across `academic-paper/`, `shared/`, `README.md`, `.claude-plugin/`

**academic-paper v2.5** (3 agent files modified):
- `agents/draft_writer_agent.md`: Added Schema 11 (Experiment Results) and Schema 12 (Lab Record) as input sources in Collaboration Rules. Added detailed integration instructions: 6 steps for Schema 11 (apa_results_text insertion, tables/figures, assumption checks, effect sizes, reproducibility) and 4 steps for Schema 12 (methods_summary, deviations→limitations, completeness gaps with score thresholds)
- `agents/abstract_bilingual_agent.md`: Added missing Collaboration Rules section — input sources, Schema 11/12 integration for abstracts, output destinations, handoff format requirements
- `agents/argument_builder_agent.md`: Added missing Collaboration Rules section — input sources, Schema 11/12 integration for CER chains, output destinations, handoff format requirements
- `SKILL.md`: Updated frontmatter description and opening paragraph from v2.4 to v2.5 with experiment integration as headline change

**shared/handoff_schemas.md**:
- Standardized `version_label` format in Schema 9 (Material Passport) to `{origin_skill}_v{major}.{minor}[-{variant}]` with examples. Updated example to match

**README.md**:
- Updated skill table with version numbers, accurate mode lists, and agent counts
- Added "57 agents, 13 handoff schemas" to description

**Motivation**: Full audit revealed that while all 13 handoff schemas were fully defined and the pipeline state machine was correctly enforced, three write-phase agents in academic-paper lacked documentation for consuming experiment results (Schema 11/12). This created a documentation gap for experiment-inclusive paper workflows despite the pipeline orchestrator and SKILL.md correctly describing the integration.

---

## 2026-03-09

### Intent-Based Mode Activation (v2.6.2)

**Files changed**: 6 files across `deep-research/`, `academic-paper/`, root

**deep-research/SKILL.md**:
- `### Socratic Mode Trigger Keywords` → `### Socratic Mode Activation`
- Replaced keyword-matching logic with intent-based activation: 5 intent signals that work in any language
- Added default rule: ambiguous intent → prefer `socratic` over `full`
- Example triggers condensed to single line with "or equivalent in any language"

**academic-paper/SKILL.md**:
- `### Plan Mode Trigger Keywords` → `### Plan Mode Activation`
- Replaced keyword-matching logic with intent-based activation: 6 intent signals
- Added default rule: ambiguous intent → prefer `plan` over `full`
- Example triggers condensed to single line with "or equivalent in any language"

**README.md / README.zh-TW.md**:
- Updated Supported Languages section: mode activation is intent-based and language-agnostic; general Trigger Keywords (Layer 1) still benefit from bilingual entries for skill-level matching confidence
- Added v2.6.2 changelog entry

**Design rationale — two-layer trigger architecture**:
- Layer 1 (skill activation): YAML `description` keywords → framework-level string matching → bilingual keywords help matching confidence → **keep bilingual**
- Layer 2 (mode routing): intent signals in SKILL.md → Claude's semantic reasoning → language-agnostic → **no per-language keyword lists needed**

---

### Bilingual Trigger Keywords for Socratic & Plan Mode (v2.6.1)

**Files changed**: 4 files across `deep-research/`, `academic-paper/`

**deep-research** (2 files):
- `SKILL.md`: Added Traditional Chinese (繁體中文) trigger keywords to YAML description, general Trigger Keywords section, and Socratic Mode Trigger Keywords section (6 Chinese keyword groups with variants). Added Chinese Quick Start examples. Quick Mode Selection Guide now bilingual.
- `references/mode_selection_guide.md`: Added Chinese trigger examples for socratic mode (5 examples). Common misselection table now bilingual.

**academic-paper** (2 files):
- `SKILL.md`: Added Traditional Chinese trigger keywords to YAML description and general Trigger Keywords section. **New section: Plan Mode Trigger Keywords** — English (5) + Chinese (7 keyword groups with variants). Previously plan mode had no dedicated trigger keywords.
- `references/mode_selection_guide.md`: Common misselection table now bilingual. Added 2 Chinese-specific misselection scenarios (「帶我寫論文」→ plan mode, 「第一次寫論文」→ plan mode).

**Motivation**: Original skills were designed in Chinese, then translated to English. After translation, trigger keywords were English-only, causing Socratic/Plan mode to fail to activate when users prompted in Chinese (defaulting to `full` mode instead).

---

## 2026-03-08

### Academic Skills Suite v2.6 — 15 Improvements Across 4 Skills

**Files changed**: 30 files (17 new, 13 modified) across `deep-research/`, `academic-paper/`, `academic-paper-reviewer/`, `academic-pipeline/`, `shared/`

**deep-research v2.3** (+7 new files, 3 modified):
- New systematic-review / PRISMA mode (7th mode) with 3 new agents: `risk_of_bias_agent` (RoB 2 + ROBINS-I), `meta_analysis_agent` (effect sizes, heterogeneity, GRADE), `monitoring_agent` (post-pipeline literature alerts)
- New references: `systematic_review_toolkit.md`, `literature_monitoring_strategies.md`
- New templates: `prisma_protocol_template.md`, `prisma_report_template.md`
- Enhanced `socratic_mentor_agent`: 4 convergence signals, question taxonomy, auto-end triggers
- Quick Mode Selection Guide added to SKILL.md

**academic-paper v2.3** (+4 new files, 3 modified):
- New agents: `visualization_agent` (11th, 9 chart types, APA 7.0 standards), `revision_coach_agent` (12th, parses unstructured reviewer comments)
- New reference: `statistical_visualization_standards.md` (chart decision tree, accessible palettes)
- New template: `revision_tracking_template.md` (4 status types: RESOLVED, DELIBERATE_LIMITATION, UNRESOLVABLE, REVIEWER_DISAGREE)
- New example: `revision_recovery_example.md` (Major Revision → revision tracking → Accept)
- Enhanced `formatter_agent`: citation format conversion (APA↔Chicago↔MLA↔IEEE↔Vancouver)
- Enhanced `socratic_mentor_agent`: 4 convergence criteria, question taxonomy
- Quick Mode Selection Guide added to SKILL.md

**academic-paper-reviewer v1.4** (+1 new file, 2 modified):
- New reference: `quality_rubrics.md` (5 dimensions scored 0-100 with behavioral indicators)
- Decision mapping: ≥80 Accept, 65-79 Minor, 50-64 Major, <50 Reject
- Updated `peer_review_report_template.md` to use 0-100 scoring referencing rubrics
- Quick Mode Selection Guide added to SKILL.md

**academic-pipeline v2.6** (+3 new files, 4 modified):
- Adaptive checkpoint system: FULL (first use/critical), SLIM (returning user), MANDATORY (integrity gates)
- Phase E Claim Verification protocol in integrity checks (E1 claim extraction, E2 source cross-reference, E3 verdict)
- Material Passport for mid-entry provenance tracking (stage-skip eligibility, freshness rules)
- New references: `mode_advisor.md` (14 scenarios, user archetypes, anti-patterns), `team_collaboration_protocol.md` (5 roles, handoff procedures, conflict resolution), `claim_verification_protocol.md` (Phase E protocol with 5 verdict types)
- New example: `integrity_failure_recovery.md` (Stage 2.5 FAIL → corrections → PASS)
- Enhanced `shared/handoff_schemas.md`: 9 comprehensive schemas with validation rules
- Enhanced orchestrator and state tracker agents for schema validation and adaptive checkpoints

---

### Full English Translation — All Skills Translated to English

**Files changed**: All `.md` files across `academic-pipeline/`, `academic-paper/`, `academic-paper-reviewer/`, `deep-research/`

**Changes**:
- Translated all Chinese content to English across 68+ files (agents, references, templates, examples, SKILL.md)
- TSSCI journal names in `top_journals_by_field.md` retain official Chinese names as proper nouns (with English translations)
- Privacy scan: removed residual `HEEACT Luminai` reference from `deep-research/references/socratic_questioning_framework.md`
- `README.zh-TW.md` intentionally kept in Chinese as the bilingual README option

---

### academic-pipeline v2.5 — External Review Protocol

**Files changed**: `academic-pipeline/SKILL.md`

**Changes**:
- New External Review Protocol section: 4-step workflow for handling real journal reviewer feedback (intake → strategic coaching → revise + Response to Reviewers → completeness check)
- Difference table: internal simulated review vs. external real review
- Strategic Revision Coaching: 4 layers (understanding → judgment → strategy → risk assessment)
- Response to Reviewers auto-generated template
- Self-verification completeness check adjustments
- Capability boundaries: AI verification ≠ real reviewer satisfaction

---

### academic-pipeline v2.4 — Stage 6 Process Summary + Collaboration Quality Evaluation

**Files changed**: `academic-pipeline/SKILL.md`, `README.md`, `README.zh-TW.md`

**academic-pipeline v2.4**:
- New Stage 6 PROCESS SUMMARY: auto-generates structured paper creation process record after pipeline completion
- Asks user preferred language (zh/en/both), generates MD → LaTeX → PDF
- Mandatory final chapter: **Collaboration Quality Evaluation** — 6 dimensions scored 1–100:
  - Direction Setting, Intellectual Contribution, Quality Gatekeeping
  - Iteration Discipline, Delegation Efficiency, Meta-Learning
- Includes: What Worked Well, Missed Opportunities, Recommendations, Human vs AI Value-Add, Claude's Self-Reflection
- Pipeline expanded from 9 to 10 stages (state machine, dashboard, audit trail updated)
- Scoring rubric: 90-100 Exceptional / 75-89 Excellent / 60-74 Good / 40-59 Basic / 1-39 Needs Improvement

**Lesson**: pandoc's newer longtable output uses `\real{}` macro which requires `\usepackage{calc}` in the LaTeX wrapper

---

### academic-pipeline v2.3 — APA 7.0 Formatting & LaTeX-to-PDF

**Files changed**: `academic-pipeline/SKILL.md`, `README.md`, `README.zh-TW.md`

**academic-pipeline v2.3**:
- Stage 5 FINALIZE now prompts user for formatting style (APA 7.0 / Chicago / IEEE) before generating LaTeX
- PDF must compile from LaTeX via `tectonic` (no HTML-to-PDF conversion allowed)
- APA 7.0 uses `apa7` document class (`man` mode) with `natbib` option (no biber required)
- XeCJK for bilingual CJK support; font stack: Times New Roman + Source Han Serif TC VF + Courier New
- Known apa7 quirks documented: `noextraspace` removed in v2.15, pandoc `\LTcaptype{none}` needs `\newcounter{none}`, `\addORCIDlink` takes ID only (not full URL)

**README updates**:
- Added Performance Notes section: recommended model Claude Opus 4.6 with Max plan; large token consumption warning
- Updated pipeline stage 5 description in both EN and zh-TW READMEs

**Lesson**: Always ask the user which academic formatting style they want (APA 7.0, Chicago, IEEE, etc.) before generating the final PDF — formatting style is a separate concern from citation style

---

## 2026-03-05

### v2.2 / v1.3 Cross-Agent Quality Alignment Update (4 skills)

**Files changed**: 19 files across 4 skills (+550 lines)

**deep-research v2.2**:
- Added cross-agent quality alignment definitions (peer-reviewed, currency rule, CRITICAL severity, source tier, minimum source count, verification threshold)
- Synthesis anti-patterns, Socratic quantified thresholds & auto-end conditions
- Reference existence verification (DOI + WebSearch)
- Enhanced ethics reference integrity check (50% + Retraction Watch)
- Mode transition matrix

**academic-paper v2.2**:
- 4-level argument strength scoring with quantified thresholds
- Plagiarism & retraction screening protocol
- F11 Desk-Reject Recovery + F12 Conference-to-Journal Conversion failure paths
- Plan → Full mode conversion protocol

**academic-paper-reviewer v1.3**:
- DA vs R3 role boundaries with explicit responsibility tables
- CRITICAL finding criteria with concrete examples
- Consensus classification (CONSENSUS-4/3/SPLIT/DA-CRITICAL)
- Confidence Score weighting rules
- Asian & Regional Journals reference (TSSCI + Asia-Pacific + OA options)

**academic-pipeline v2.2**:
- Checkpoint confirmation semantics (6 user commands with precise actions)
- Mode switching rules (safe/dangerous/prohibited matrix)
- Skill failure fallback matrix (per-stage degradation strategies)
- State ownership protocol (single source of truth with write access control)
- Material version control (versioned artifacts with audit trail)

---

## 2026-03-01

### Simplify Academic Research Skills SKILL.md (4 files)

**Motivation**: 4 academic research skills totaled 2,254 lines with significant cross-skill duplication and redundant inline content already available as template files.

**Files changed**:
- `academic-paper-reviewer/SKILL.md` (570→470, -100 lines)
- `academic-pipeline/SKILL.md` (675→535, -140 lines)
- `deep-research/SKILL.md` (469→435, -34 lines)
- `academic-paper/SKILL.md` (540→443, -97 lines)

**Changes**:
- A: Reviewer — removed inline templates, replaced with `templates/` file references (kept Devil's Advocate special format notes)
- B: Pipeline — removed ASCII state machine, replaced with concise 9-stage list + reference
- C: Pipeline — simplified Two-Stage Review Protocol to inputs/outputs/branching only
- D: 3 skills — "Full Academic Pipeline" section replaced with one-line reference to `academic-pipeline/SKILL.md`
- E: 4 skills — trimmed routing tables, removed HEI routes already defined in root CLAUDE.md
- F+G: Removed duplicate Mode Selection sections from deep-research and academic-paper
- H: academic-paper Handoff Protocol simplified to overview + upstream reference
- I: academic-paper Phase 0 Config replaced with reference to `agents/intake_agent.md`
- J: 4 skills — Output Language sections reduced to 1 line each
- K: Fixed revision loop cap contradiction (pipeline overrides academic-paper's max 2 rule)

**Result**: 2,254→1,883 lines (-371 lines, -16.5%), all 371 quality tests passed

**Lesson**: Inlining full template content in SKILL.md is unnecessary redundancy — a one-line reference suffices when template files exist at the correct path
