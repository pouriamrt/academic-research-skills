# Academic Research Skills

A suite of Claude Code skills for rigorous academic research, experimentation, statistical analysis, paper writing, peer review, and pipeline orchestration. 8 skills, 57+ agents, 20 handoff schemas.

## Skills Overview

| Skill | Purpose | Key Modes |
|-------|---------|-----------|
| `deep-research` v2.9.4 | Universal 14-agent research team (with concept lineage) | full, quick, socratic, review, lit-review, fact-check, systematic-review |
| `experiment-designer` v1.0.1 | Experiment protocol and power analysis | full, guided, quick, power-only, instrument |
| `data-analyst` v1.0.1 | Statistical analysis execution | full, guided, quick, assumption-check, exploratory, replication |
| `simulation-runner` v1.0.1 | Computational experiments | full, guided, quick, power-sim, sensitivity, bootstrap |
| `lab-notebook` v1.0.1 | Experiment research record | full, log-entry, deviation, snapshot, export, audit |
| `academic-paper` v3.2.0 | 11-agent academic paper writing (English-only) | full, plan, outline-only, revision, revision-coach, abstract-only, lit-review, format-convert, citation-check, disclosure |
| `academic-paper-reviewer` v1.9.1 | Multi-perspective paper review (5 reviewers + optional cross-model DA critique) | full, re-review, quick, methodology-focus, guided, calibration |
| `academic-pipeline` v3.17.0 | Full pipeline orchestrator (suite-version-pinned, auto-by-default) | (coordinates all above) |

## v3.17.0 Breaking changes (2026-05-15)

1. **Pipeline runs unattended by default.** Auto mode is the new default — no checkpoint pauses, no `continue?` prompts, no mode-recommendation dialogue, no beep. Set `ARS_INTERACTIVE=1` to restore v3.16.0 interactive UX.
2. **Bilingual support removed.** Multiple bilingual files were deleted (see `CHANGELOG.md` for the full list). `academic-paper` agent count drops 12 → 11; the English abstract + keywords are now emitted inline by `draft_writer_agent` during Phase 4. Stage 6 PROCESS SUMMARY is English-only.

### New env vars

| Var | Default | Effect |
|-----|---------|--------|
| `ARS_INTERACTIVE` | unset (= auto) | When `=1`: restore v3.16.0 checkpoint pauses, mode-recommendation prompts, language pickers. When unset: full auto. |
| `ARS_AUTO_MAX_RETRIES` | `3` | Cap on auto-retry rounds for Stage 2.5 integrity fix. Stage 4.5 retry cap is hard-pinned `1`. |
| `ARS_AUTO_FAIL_MODE` | `exit-nonzero` | When retry budget is exhausted on FAIL: `exit-nonzero` (default) writes verdict to passport and stops; `continue-with-warning` is advisory. |
| `ARS_AUTO_NO_REENTRY` | unset | When `=1`: skip experiment re-entry at Stage 1.5-R / 1.5-R2 in auto mode (revision items flagged `requires_new_experiment` become Acknowledged Limitations). |

## v3.16 Upstream Sync (Imbad0202 v3.3.2 → v3.7.3)

Merged on 2026-05-15 from upstream `origin/main`. Brings v3.4–v3.7.3 features on top of fork's v3.15 experiment pipeline. Schema collisions resolved by renumbering upstream Schema 12 (Compliance Report) → **Schema 19** and Schema 13/13.1 (Sprint Contract) → **Schema 20/20.1** to preserve fork's experiment Schemas 10–18.

### v3.7.3 — Claim faithfulness + contaminated-source advisory (in progress upstream)

- **L3-1 Three-Layer Citation Emission**: `synthesis_agent`, `draft_writer_agent`, `report_compiler_agent` gain `<!--anchor:<kind>:<value>-->` after `<!--ref:slug-->`, where `<kind>` ∈ `{quote, page, section, paragraph, none}`. Quote anchors capped at 25 words. `pipeline_orchestrator_agent` finalizer becomes 5-cell with precedence-zero NO-LOCATOR check; `formatter_agent` gains hard-gate refusal for `[UNVERIFIED CITATION — NO QUOTE OR PAGE LOCATOR]`.
- **L3-2 Contaminated-source advisory signals**: optional `contamination_signals: { preprint_post_llm_inflection, semantic_scholar_unmatched }` in `literature_corpus_entry`. Advisory only — does NOT change gate decision.
- **Motivation**: Zhao et al. arXiv:2605.07723 documents 146,932 hallucinated citations across arXiv/bioRxiv/SSRN/PMC in 2025, with 85.3% surviving into the published record.

### v3.7.2 — Trust-provenance hardening

- 12-round 0-P1-sustained convergence on `trust_provenance` + drift transparency framework.

### v3.7.1 — Two-Layer Citation Emission

- Cite-time provenance finalizer; agent two-layer citation emission; D2 audit Scope Report block + lint enforcement; SHA byte-equivalence gate + D1 trust-chain frontmatter schema.

### v3.7.0 — Claude Code plugin packaging

- ARS installs in one line via `/plugin marketplace add` + `/plugin install`. Adds `.claude-plugin/`, `commands/`, `agents/`, `hooks/`, `skills/` symlink dir. **10 slash commands** under `commands/ars-*.md` with model routing (opus for `full`/`revision-coach`, sonnet for the other 8, no Haiku). **3 plugin-shipped agents** under `agents/` as relative symlinks to v3.6.7-hardened downstream agents. **SessionStart announce hook** lists commands + agents + token budget.

### v3.6.8 — Generator-Evaluator Contract (Schema 20.1)

- Schema 20.1 (renumbered from upstream 13.1) adds `writer_full` + `evaluator_full` modes to sprint contracts, with `pre_commitment_artifacts` (writer-only) + `disagreement_handling` (evaluator-only). 12 `allOf` branches enforce mode-conditional gates. Two-phase orchestration inside `academic-paper full`: Phase 4a paper-blind pre-commitment + Phase 4b paper-visible drafting + self-scoring; Phase 6a/6b for evaluator. New templates: `shared/contracts/writer/full.json`, `shared/contracts/evaluator/full.json`.

### v3.6.7 — Downstream-agent pattern protection

- `synthesis_agent`, `research_architect_agent` (survey-designer mode), `report_compiler_agent` (abstract-only mode) carry `PATTERN PROTECTION (v3.6.7)` blocks hardening 13/18 documented hallucination/drift patterns (A1–A5 narrative, B1–B5 instrument, C1–C3 publication). Four reference glossaries in `shared/references/`. Cross-model audit prompt template at `shared/templates/codex_audit_multifile_template.md`. Ship-quality target: "end-to-end deliverable set passes independent xhigh cross-model audit at 0 P1+P2 finding within three rounds."

### v3.6.5 — Literature corpus consumer integration

- Material Passport `literature_corpus[]` consumer integration in Phase 1 of `bibliography_agent` + `literature_strategist_agent`. **Corpus-first, search-fills-gap** five-step flow + four Iron Rules. PRE-SCREENED reproducibility block in Search Strategy reports. Protocol ref: `academic-pipeline/references/literature_corpus_consumers.md`.

### v3.6.4 — Literature corpus adapter contract

- Material Passport `literature_corpus[]` input port via `shared/contracts/passport/literature_corpus_entry.schema.json`. Adapter contract `academic-pipeline/references/adapters/overview.md`. Three reference adapters: `scripts/adapters/{folder_scan,zotero,obsidian}.py`. Rejection log contract `shared/contracts/passport/rejection_log.schema.json`.

### v3.6.3 — Passport reset boundary

- Opt-in `ARS_PASSPORT_RESET=1` flag promotes every FULL checkpoint to a context-reset boundary. New `resume_from_passport=<hash>` mode in `academic-pipeline`. Schema 9 `reset_boundary[]` append-only ledger with `kind: boundary` + `kind: resume` entries. Protocol doc: `academic-pipeline/references/passport_as_reset_boundary.md`.

### v3.6.2 — Sprint Contract hard gate (Schema 20)

- Schema 20 (renumbered from upstream 13) + validator + two reviewer templates (`reviewer/full.json` panel 5, `reviewer/methodology_focus.json` panel 2). Reviewer Phase 1 paper-content-blind + Phase 2 paper-visible via `<phase1_output>` data delimiter. Synthesizer three-step mechanical protocol (build matrix → evaluate with panel-relative quantifier → resolve precedence). Forbidden-ops list in `academic-paper-reviewer/agents/editorial_synthesizer_agent.md`.

### v3.5.1 — Socratic reading-check probe

- Opt-in `ARS_SOCRATIC_READING_PROBE=1`. Fires at most once per goal-oriented Socratic session when user cites a specific paper. Decline logged without penalty. Outcome carried into Stage 6 AI Self-Reflection Report.

### v3.5.0 — Collaboration Depth Observer

- New `collaboration_depth_agent` in `academic-pipeline` (Agent Team grows 3 → 4). Invoked at FULL/SLIM checkpoints + pipeline completion. Scores user-AI collaboration on 4 dimensions per `shared/collaboration_depth_rubric.md`. **Advisory only — never blocks.** Based on Wang & Zhang (2026) IJETHE 23:11.

### v3.4.0 — Compliance Agent (Schema 19)

- Single mode-aware `compliance_agent` running PRISMA-trAIce 17 items + RAISE 4 principles + 8-role matrix. Hooks Stage 2.5 / 4.5 Integrity Gates with tier-based block. Non-SR entries run principles-only warn-only. Schema 19 (renumbered from upstream Schema 12) `compliance_report` — append-only audit trail in Material Passport via `compliance_history[]`. 3-round override ladder with auto-injected `disclosure_addendum`.

### v3.3.5 — Human-baseline + artifact reproducibility

- `benchmark_report.schema.json` for ARS benchmark comparisons (required human baseline + independence fields). `repro_lock` sub-block on Material Passport — configuration lockfile, NOT replay guarantee. Pattern docs: `shared/benchmark_report_pattern.md`, `shared/artifact_reproducibility_pattern.md`.

### v3.3.2 — Skill metadata: data_access_level + task_type

- Every top-level `SKILL.md` declares `metadata.data_access_level` ∈ `{raw, redacted, verified_only}` and `metadata.task_type` ∈ `{outcome-gradable, open-ended}`. Enforced by `scripts/check_data_access_level.py` + `scripts/check_task_type.py` in CI.

## v3.15 Upstream Integration (PaperOrchestra + Lu 2026)

Merged from upstream (Imbad0202) v2.9-v3.3 while preserving the fork's full experiment pipeline (4 experiment skills, schemas 10-18, validation tooling).

### v3.3 — PaperOrchestra-inspired enhancements

- **Semantic Scholar API Verification**: Tier 0 programmatic reference verification. See `deep-research/references/semantic_scholar_api_protocol.md`.
- **Anti-Leakage Protocol**: Knowledge isolation prioritizing session materials over LLM memory. See `academic-paper/references/anti_leakage_protocol.md`.
- **VLM Figure Verification**: Optional closed-loop figure verification via vision LLM. See `academic-paper/references/vlm_figure_verification.md`.
- **Score Trajectory Protocol**: Per-dimension rubric score delta tracking across revision rounds. See `academic-pipeline/references/score_trajectory_protocol.md`.
- **Stage 2 Parallelization**: Visualization and argument building can run in parallel after outline.

### v3.2 — Lu 2026 integration

- **7-mode AI Research Failure Mode Checklist**: blocks pipeline at Stage 2.5/4.5 on suspected failures (Lu 2026). See `academic-pipeline/references/ai_research_failure_modes.md`.
- **Reviewer Calibration Mode**: opt-in FNR/FPR/balanced-accuracy measurement. See `academic-paper-reviewer/references/calibration_mode_protocol.md`.
- **Disclosure Mode**: venue-specific AI-usage statement (ICLR/NeurIPS/Nature/Science/ACL/EMNLP). See `academic-paper/references/disclosure_mode_protocol.md`.
- **Early-Stopping + Budget Transparency**: convergence check + token cost estimate at pipeline start.
- **Fidelity-Originality Mode Spectrum**: classifies all modes. See `shared/mode_spectrum.md`.

### v2.9 — Style & IS Senior Scholars' Basket

- **Information Systems — Senior Scholars' Basket of 11**: complete AIS official premier journal list (added *Decision Support Systems*, *Information & Management*, *Information and Organization*).
- **Style Calibration**: optional intake step to learn the author's writing voice from past papers. See `shared/style_calibration_protocol.md`.
- **Anti-sycophancy protocols**: DA agents score rebuttals 1-5 before conceding. No concession below 4/5. Frame-lock detection.
- **Intent detection**: Socratic Mentor classifies user intent as exploratory vs. goal-oriented. Exploratory mode disables auto-convergence.
- **Cross-model verification** (optional): Set `ARS_CROSS_MODEL` env var to enable GPT-5.4 Pro or Gemini 3.1 Pro for integrity sample checks and independent Devil's Advocate critique. Peer-review sixth-reviewer support remains planned. See `shared/cross_model_verification.md`.
- **AI Self-Reflection Report**: Pipeline Stage 6 now includes AI behavioral self-assessment (concession rate, health alerts, sycophancy risk rating).

## Routing Rules

1. **academic-pipeline vs individual skills**: academic-pipeline = full pipeline orchestrator (research → write → integrity → review → revise → final integrity → finalize). If the user only needs a single function (just research, just write, just review), trigger the corresponding skill directly without the pipeline.

2. **deep-research vs academic-paper**: Complementary. deep-research = upstream research engine (investigation + fact-checking), academic-paper = downstream publication engine (paper writing). Recommended flow: deep-research → academic-paper.

3. **Auto vs interactive**: auto is the default. The orchestrator forces `mode=full` on every dispatched sub-skill and writes checkpoint deliverables to the passport ledger without prompting. Per-skill `socratic` / `plan` / `guided` modes only fire when `ARS_INTERACTIVE=1` is set.

4. **deep-research socratic (interactive only)**: When `ARS_INTERACTIVE=1` and the research question is unclear, suggest socratic mode for Socratic dialogue. Otherwise `full` runs.

5. **academic-paper plan (interactive only)**: When `ARS_INTERACTIVE=1` and the user wants chapter-by-chapter Socratic guidance, suggest plan mode. Otherwise `full` runs.

6. **academic-paper-reviewer guided (interactive only)**: When `ARS_INTERACTIVE=1` and the user wants a learning-focused Socratic review, suggest guided mode. Otherwise `full` runs.

7. **experiment-designer vs data-analyst**: experiment-designer = upstream design (protocol, power, instruments), data-analyst = downstream execution (run the actual stats). If user has data and wants analysis, go straight to data-analyst. If user needs to plan an experiment first, start with experiment-designer.

8. **data-analyst vs simulation-runner**: data-analyst = real data, simulation-runner = generated/synthetic data. If user says "bootstrap" or "Monte Carlo" with existing data, that's simulation-runner. If user says "run a regression on my data", that's data-analyst.

9. **lab-notebook**: Never the entry point to the experiment pipeline. Always accompanies other experiment skills. Automatically invoked by pipeline when experiment stages are active. Can be invoked standalone for log-entry, deviation, snapshot, export, or audit modes on an existing notebook.

## Key Rules

- All claims must have citations
- Evidence hierarchy respected (meta-analyses > RCTs > cohort > case reports > expert opinion)
- Contradictions disclosed with evidence quality comparison
- AI disclosure in all reports
- Output language: English only

## Optional MCP Capabilities

The following MCP servers enhance the pipeline when available. Both are **optional** — the pipeline degrades gracefully without them.

### Semantic Scholar + OpenAlex (Citation Graph APIs)
- **Tools**: `WebFetch` to call REST APIs — not MCP servers, but direct HTTP endpoints
- **Semantic Scholar** (`api.semanticscholar.org/graph/v1`): Citation chain tracing with intent/context data, influential citation filtering, SPECTER embeddings
- **OpenAlex** (`api.openalex.org`): Broad bibliometric data, topic hierarchy, institution/funder data, FWCI normalization
- **Scope**: Citation chain analysis (concept lineage), enhanced bibliography search, paper verification
- **Requires**: No API key required for basic use; optional keys increase rate limits
- **Used by**: `concept_lineage_agent` (primary), `bibliography_agent` (enhanced search)
- **Fallback**: WebSearch-only mode with bibliography-based inference if APIs are unavailable
- **Reference**: `deep-research/references/citation_graph_apis.md`

### PaperBanana MCP (Methodology Diagrams)
- **Tool**: `mcp__paperbanana__generate_diagram` — generates publication-quality methodology diagrams from text
- **Scope**: Methodology/research design diagrams ONLY (not statistical plots)
- **Requires**: `GOOGLE_API_KEY` environment variable
- **Used by**: `draft_writer_agent` (Methods section), `protocol_compiler_agent` (experiment protocol)
- **Fallback**: Mermaid MCP for structural flowcharts
- **Reference**: `shared/experiment_infrastructure.md` Section 10

### Google Colab MCP (GPU Computation)
- **Tool**: `mcp__colab-proxy-mcp__open_colab_browser_connection` — offloads heavy computation to Colab GPU
- **Scope**: Heavy simulations (>50K iterations), large SEM/HLM, massive bootstrap
- **Requires**: Human-in-the-loop authentication (beep alert + pause for user to auth and switch runtime to GPU). Note: when `ARS_INTERACTIVE` is unset, the auto pipeline writes a `colab-auth-required` marker to the passport and exits non-zero — unattended Colab auth cannot happen.
- **Used by**: `execution_engine_agent` (simulation-runner), `analysis_executor_agent` (data-analyst)
- **Fallback**: Local execution with reduced iterations if needed
- **Reference**: `shared/experiment_infrastructure.md` Section 11

## Full Academic Pipeline

```
Stage 1:   deep-research (full; socratic only when ARS_INTERACTIVE=1)
Stage 1.5: [EXPERIMENT — optional, auto-detected from Methodology Blueprint]
             → experiment-designer (Schema 10)
               → data-analyst / simulation-runner (Schema 11)
                 → lab-notebook (Schema 12, continuous)
Stage 2:   academic-paper (full; plan only when ARS_INTERACTIVE=1) ← integrates Schema 11/12 into Results & Methods
Stage 2.5: integrity check (Stage 2.5) (mandatory gate — references, claims, originality; integrity verification + PRISMA-trAIce + RAISE compliance check Schema 19, v3.4.0+). Auto-retry on FAIL up to ARS_AUTO_MAX_RETRIES (default 3); exit non-zero on exhaustion per ARS_AUTO_FAIL_MODE.
Stage 3:   academic-paper-reviewer (full; guided only when ARS_INTERACTIVE=1)
           ← sprint contract gate (Schema 20, v3.6.2+) for each reviewer call. Auto-routes from editorial_synthesizer_agent verdict (accept | minor | major | reject).
  → Experiment Re-Entry Check: scan Revision Roadmap for requires_new_experiment items (skip when ARS_AUTO_NO_REENTRY=1)
Stage 1.5-R: [EXPERIMENT RE-ENTRY — conditional, triggered by reviewer requests for new data]
             → experiment-designer / data-analyst / simulation-runner (based on experiment_type)
Stage 4:   academic-paper (revision) + Response to Reviewers (integrates new Schema 11-R if available)
           ← writer/evaluator sprint contract (Schema 20.1, v3.6.6/v3.6.8+) for generator-evaluator pair
Stage 3':  academic-paper-reviewer (re-review)
  → Experiment Re-Entry Check (last opportunity for experiments)
Stage 1.5-R2: [EXPERIMENT RE-ENTRY 2 — conditional, final experiment opportunity]
Stage 4':  academic-paper (re-revision, max 1 round)
Stage 4.5: final integrity check (Stage 4.5) (mandatory, zero-tolerance integrity verification + final compliance check). Auto-retry on FAIL — hard cap 1; exit non-zero on second FAIL.
Stage 5:   academic-paper (format-convert → LaTeX/DOCX-via-Pandoc/PDF output)
Stage 6:   PROCESS SUMMARY (auto — English paper creation record → PDF)
           + AI Self-Reflection Report (concession rate, health alerts, sycophancy risk)
```

The experiment stages (1.5) are auto-detected from the Methodology Blueprint produced by deep-research. If the methodology does not require experimentation (e.g., literature review, theoretical, policy analysis), these stages are skipped entirely.

The experiment re-entry stages (1.5-R, 1.5-R2) are triggered when reviewers request new empirical evidence during revision. The editorial_synthesizer_agent flags revision items with `requires_new_experiment = true`, and the pipeline re-enters experiment stages before text revision. Set `ARS_AUTO_NO_REENTRY=1` to skip re-entry; affected items become Acknowledged Limitations.

## Handoff Protocol

### deep-research → academic-paper
Materials: RQ Brief (Schema 1), Methodology Blueprint (Schema 14), Annotated Bibliography (Schema 2), Synthesis Report (Schema 3), INSIGHT Collection (Schema 15), Concept Lineage Report (Schema 16)

### academic-paper → academic-paper-reviewer
Materials: Complete paper text (Schema 4). field_analyst_agent auto-detects domain and configures reviewers.

### academic-paper-reviewer → academic-paper (revision)
Materials: Editorial Decision Letter, Review Report (Schema 6), Revision Roadmap (Schema 7, with `requires_new_experiment` flags on applicable items), Per-reviewer detailed comments

### academic-paper-reviewer → pipeline orchestrator → experiment re-entry
When Revision Roadmap contains `requires_new_experiment = true` items: pipeline re-enters Stage 1.5-R before Stage 4. New Schema 11-R and Schema 12-R are produced and merged with existing experiment materials for integration into the revised paper.

### experiment-designer → data-analyst / simulation-runner
Materials: Experiment Design (Schema 10), Simulation Specification (Schema 13, if simulation design), Material Passport (Schema 9)

### data-analyst / simulation-runner → academic-paper
Materials: Experiment Results (Schema 11) — APA-formatted statistics, tables, figures, reproducibility script

### lab-notebook → academic-paper
Materials: Lab Record (Schema 12) — methods summary, file manifest, deviation log, completeness score

### academic-paper → integrity check (Stage 2.5) and final integrity check (Stage 4.5)
Materials: Complete paper draft (Schema 4). Integrity agent checks references, citation context, data, originality, claims. Produces Integrity Report (Schema 5) with PASS/PASS_WITH_CONDITIONS/FAIL verdict. compliance_agent (v3.4.0+) emits Schema 19 compliance_report appended to passport's `compliance_history[]`.

### orchestrator → reviewer / writer / evaluator
Materials: Sprint Contract (Schema 20, v3.6.2+ for reviewers; Schema 20.1, v3.6.6+ for writer/evaluator) — frozen pre-registered acceptance criteria. Phase 1 (paper-content-blind) commits scoring plan; Phase 2 (paper-visible) executes.

## Validation Tools

Run `python tools/self_test.py` to validate plugin structural integrity (200+ checks). See `tools/` for schema validation, dependency graph generation, pipeline dashboard, and reproducibility replay. CI workflows under `.github/workflows/`: `pytest.yml`, `spec-consistency.yml`, `freshness-check.yml`.

## Version Info
- **Version**: 3.17.0
- **Suite version**: 3.17.0
- **Last Updated**: 2026-05-15
- **Author**: Pouria Mortezaagha
- **Upstream**: Imbad0202 (merged through v3.7.3)
- **License**: CC-BY-NC 4.0
