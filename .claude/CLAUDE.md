# Academic Research Skills

A suite of Claude Code skills for rigorous academic research, experimentation, statistical analysis, systematic-review screening, paper writing, peer review, and pipeline orchestration. 9 skills, 65 agents, 21 handoff schemas + passport schemas. Upstream is merged through v3.24.2 (`sr-screener`, run ledger, acronym check, panel reference and claim checks). Full history in `CHANGELOG.md`.

## Skills Overview

| Skill | Purpose | Key Modes |
|-------|---------|-----------|
| `deep-research` v2.9.4 | Universal 14-agent research team (with concept lineage) | full, quick, socratic, review, lit-review, three-way-scan, fact-check, systematic-review |
| `experiment-designer` v1.0.1 | Experiment protocol and power analysis | full, guided, quick, power-only, instrument |
| `data-analyst` v1.0.1 | Statistical analysis execution | full, guided, quick, assumption-check, exploratory, replication |
| `simulation-runner` v1.0.1 | Computational experiments | full, guided, quick, power-sim, sensitivity, bootstrap |
| `lab-notebook` v1.0.1 | Experiment research record | full, log-entry, deviation, snapshot, export, audit |
| `academic-paper` v3.2.0 | 11-agent academic paper writing (English-only) | full, plan, outline-only, revision, revision-coach, abstract-only, lit-review, format-convert, citation-check, disclosure, rebuttal-audit |
| `academic-paper-reviewer` v1.9.1 | Multi-perspective paper review (5 reviewers + optional cross-model DA critique) | full, re-review, quick, methodology-focus, guided, calibration |
| `sr-screener` v1.0.0 | Protocol-driven study screening (2 blinded AI reviewers + adjudicator) | protocol, quick, pilot, ta-screen, ft-screen, adjudicate, audit, report |
| `academic-pipeline` v3.23.0 | Full pipeline orchestrator (suite-version-pinned, auto-by-default) | (coordinates all above) |


## v3.23.0 Key Additions

- **Upstream sync v3.22.0 → v3.24.2** (`7e019f5..6d93886`): `sr-screener` is the ninth
  skill; skill paths are declared in `plugin.json`; the one-process guard launcher sits
  behind the fork's no-Python fast path; run ledger, acronym and panel claim checks.
- **Not merged (English-only):** `output_language_pair`, the locale track, translated
  READMEs.

## Cross-model reviewer track — standing invariants

Not release notes. These sentences are byte-witnesses pinned by
`scripts/check_calibration_tiers.py` (`CLAUDE_WITNESSES`), so they must stay in this file
verbatim. They previously lived inside a `## vX Key Additions` section and were lost when
that section was rotated out at release — keep them here, outside any release heading.

The ordinary reviewer path is `reviewer_full` only and consent-gated; Reviewer 2 runs on
the second model family as a substrate swap inside the fixed five-seat panel, never a 6th
reviewer. Do NOT re-wrap the next line — the witness is matched as an exact substring, so
a line break inside it fails the lint.

Calibration is the sole explicit exception and uses the canonical non-sprint single-call transport plus attempt-atomic fallback in `shared/cross_model_verification.md`; it never borrows the sprint payload or mixes substrates in one scored attempt.

Cross-model verification (`ARS_CROSS_MODEL`, optional) runs integrity sample checks, a blind and separately executed Devil's Advocate critique, and blind disagreement checkpoints at design freeze and final editorial decision (#518). The once-planned generic sixth reviewer is retired, not deferred. These execution facts are not a binary independence claim.

## Command model routing

Not derivable from Claude Code's command listing; only actionable in this repo:

- `/ars-full`, `/ars-revision-coach`, `/ars-reviewer`, `/ars-citation-check` inherit the
  session model (the v3.7.0 opus floor was retired in 2026-06; citation-check since #912).
- The other 12 `/ars-*` commands pin `model: sonnet` in their frontmatter.
- The 4 plugin agents (`synthesis-agent`, `research-architect-agent`, `report-compiler-agent`,
  `screening-reviewer-agent`) carry a tools allowlist (#514; the screening reviewer gets
  Read/Grep only). Every OTHER ARS agent is an in-skill prompt template loaded via
  SKILL.md, NOT a plugin agent.

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

10. **rebuttal-audit vs revision-coach**: route by input shape. `rebuttal-audit` only when the user supplies BOTH reviewer comments AND an existing response draft (advisory QA; generates nothing, never emits Schema 18). Comments alone → `revision-coach` (Response Letter Skeleton). Unclear → clarify.

11. **real-committee correspondence (#668)**: the `revision-coach` committee-correspondence variant only when the user explicitly names a real committee or institutional review office; formal tone does not establish authority. It loads `academic-paper/references/committee_correspondence_protocol.md` and never emits reviewer severity, Schema 18, a determination, or a resolution claim.

12. **sr-screener vs deep-research systematic-review**: `sr-screener` for eligibility decisions on records the user already has (exports, abstracts, full texts), or a screening protocol, pilot, conflict adjudication, exclusion audit, or selection report. A request for the review itself, or a bare "systematic review" / "PRISMA", stays with `deep-research` `systematic-review`. `sr-screener` owns screening decisions and starts only when asked; nothing hands over to it automatically.

## Key Rules

- All claims must have citations
- Evidence hierarchy respected (meta-analyses > RCTs > cohort > case reports > expert opinion)
- Contradictions disclosed with evidence quality comparison
- AI disclosure in all reports
- Output language: English only

## Optional MCP Capabilities

All **optional**; the pipeline degrades gracefully without them.

### Semantic Scholar + OpenAlex (Citation Graph APIs)
- **Tools**: `WebFetch` against REST APIs (not MCP servers)
- **Semantic Scholar** (`api.semanticscholar.org/graph/v1`): Citation chain tracing with intent/context data, influential citation filtering, SPECTER embeddings
- **OpenAlex** (`api.openalex.org`): Broad bibliometric data, topic hierarchy, institution/funder data, FWCI normalization
- **Scope**: Citation chain analysis (concept lineage), enhanced bibliography search, paper verification
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
- **Requires**: Human-in-the-loop auth (beep + pause to switch the runtime to GPU). With `ARS_INTERACTIVE` unset, the auto pipeline writes a `colab-auth-required` marker to the passport and exits non-zero.
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

### deep-research → sr-screener → academic-paper (systematic reviews)
In: screening protocol source (proposal, PROSPERO record, or `systematic-review` protocol), database exports (RIS, .nbib, Web of Science, CSV), full texts. Out: `*_literature_corpus.yaml` (`literature_corpus[]` for the Material Passport), PRISMA 2020 counts, methods draft, exclusion reasons, screening log.

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

`python tools/self_test.py` validates plugin structure (200+ checks); `tools/` also holds schema validation, dependency graph, dashboard, and replay. CI: `.github/workflows/` (`pytest.yml`, `spec-consistency.yml`, `freshness-check.yml`).

## Version Info
- **Version**: 3.23.0
- **Suite version**: 3.23.0
- **Last Updated**: 2026-11-07
- **Author**: Pouria Mortezaagha
- **Upstream**: Imbad0202 (merged through v3.24.2 / commit 6d93886)
- **License**: CC-BY-NC 4.0
