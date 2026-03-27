# Academic Research Skills

A suite of Claude Code skills for rigorous academic research, experimentation, statistical analysis, paper writing, peer review, and pipeline orchestration. 8 skills, 57 agents, 15 handoff schemas.

## Skills Overview

| Skill | Purpose | Key Modes |
|-------|---------|-----------|
| `deep-research` v2.4 | Universal 13-agent research team | full, quick, socratic, review, lit-review, fact-check, systematic-review |
| `experiment-designer` v1.0 | Experiment protocol and power analysis | full, guided, quick, power-only, instrument |
| `data-analyst` v1.0 | Statistical analysis execution | full, guided, quick, assumption-check, exploratory, replication |
| `simulation-runner` v1.0 | Computational experiments | full, guided, quick, power-sim, sensitivity, bootstrap |
| `lab-notebook` v1.0 | Experiment research record | full, log-entry, deviation, snapshot, export, audit |
| `academic-paper` v2.5 | 12-agent academic paper writing | full, plan, outline-only, revision, abstract-only, lit-review, format-convert, citation-check |
| `academic-paper-reviewer` v1.4 | Multi-perspective paper review (5 reviewers) | full, re-review, quick, methodology-focus, guided |
| `academic-pipeline` v2.7 | Full pipeline orchestrator | (coordinates all above) |

## Routing Rules

1. **academic-pipeline vs individual skills**: academic-pipeline = full pipeline orchestrator (research → write → review → revise → finalize). If the user only needs a single function (just research, just write, just review), trigger the corresponding skill directly without the pipeline.

2. **deep-research vs academic-paper**: Complementary. deep-research = upstream research engine (investigation + fact-checking), academic-paper = downstream publication engine (paper writing + bilingual abstracts). Recommended flow: deep-research → academic-paper.

3. **deep-research socratic vs full**: socratic = guided Socratic dialogue to help users clarify their research question. full = direct production of research report. When the user's research question is unclear, suggest socratic mode.

4. **academic-paper plan vs full**: plan = chapter-by-chapter guided planning via Socratic dialogue. full = direct paper production. When the user wants to think through their paper structure, suggest plan mode.

5. **academic-paper-reviewer guided vs full**: guided = Socratic review that engages the author in dialogue about issues. full = standard multi-perspective review report. When the user wants to learn from the review, suggest guided mode.

6. **experiment-designer vs data-analyst**: experiment-designer = upstream design (protocol, power, instruments), data-analyst = downstream execution (run the actual stats). If user has data and wants analysis, go straight to data-analyst. If user needs to plan an experiment first, start with experiment-designer.

7. **data-analyst vs simulation-runner**: data-analyst = real data, simulation-runner = generated/synthetic data. If user says "bootstrap" or "Monte Carlo" with existing data, that's simulation-runner. If user says "run a regression on my data", that's data-analyst.

8. **lab-notebook**: Never the entry point to the experiment pipeline. Always accompanies other experiment skills. Automatically invoked by pipeline when experiment stages are active. Can be invoked standalone for log-entry, deviation, snapshot, export, or audit modes on an existing notebook.

## Key Rules

- All claims must have citations
- Evidence hierarchy respected (meta-analyses > RCTs > cohort > case reports > expert opinion)
- Contradictions disclosed with evidence quality comparison
- AI disclosure in all reports
- Default output language matches user input (Traditional Chinese or English)

## Optional MCP Capabilities

The following MCP servers enhance the pipeline when available. Both are **optional** — the pipeline degrades gracefully without them.

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
- **Requires**: Human-in-the-loop authentication (beep alert + pause for user to auth and switch runtime to GPU)
- **Used by**: `execution_engine_agent` (simulation-runner), `analysis_executor_agent` (data-analyst)
- **Fallback**: Local execution with reduced iterations if needed
- **Reference**: `shared/experiment_infrastructure.md` Section 11

## Full Academic Pipeline

```
Stage 1:   deep-research (socratic/full)
Stage 1.5: [EXPERIMENT — optional, auto-detected from Methodology Blueprint]
             → experiment-designer (Schema 10)
               → data-analyst / simulation-runner (Schema 11)
                 → lab-notebook (Schema 12, continuous)
Stage 2:   academic-paper (plan/full) ← integrates Schema 11/12 into Results & Methods
Stage 2.5: integrity verification (mandatory gate — references, claims, originality)
Stage 3:   academic-paper-reviewer (full/guided)
Stage 4:   academic-paper (revision) + Response to Reviewers
Stage 3':  academic-paper-reviewer (re-review)
Stage 4':  academic-paper (re-revision, max 1 round)
Stage 4.5: final integrity verification (mandatory, zero-tolerance)
Stage 5:   academic-paper (format-convert → LaTeX/DOCX/PDF)
Stage 6:   PROCESS SUMMARY (auto — bilingual paper creation record → PDF)
```

The experiment stages (1.5) are auto-detected from the Methodology Blueprint produced by deep-research. If the methodology does not require experimentation (e.g., literature review, theoretical, policy analysis), these stages are skipped entirely.

## Handoff Protocol

### deep-research → academic-paper
Materials: RQ Brief, Methodology Blueprint, Annotated Bibliography, Synthesis Report, INSIGHT Collection

### academic-paper → academic-paper-reviewer
Materials: Complete paper text. field_analyst_agent auto-detects domain and configures reviewers.

### academic-paper-reviewer → academic-paper (revision)
Materials: Editorial Decision Letter, Revision Roadmap, Per-reviewer detailed comments

### experiment-designer → data-analyst / simulation-runner
Materials: Experiment Design (Schema 10), Simulation Specification (Schema 13, if simulation design)

### data-analyst / simulation-runner → academic-paper
Materials: Experiment Results (Schema 11) — APA-formatted statistics, tables, figures, reproducibility script

### lab-notebook → academic-paper
Materials: Lab Record (Schema 12) — methods summary, file manifest, deviation log, completeness score

### academic-paper → integrity verification (Stage 2.5 & 4.5)
Materials: Complete paper draft (Schema 4). Integrity agent checks references, citation context, data, originality, claims. Produces Integrity Report (Schema 5) with PASS/PASS_WITH_CONDITIONS/FAIL verdict.

## Validation Tools

Run `python tools/self_test.py` to validate plugin structural integrity (192 checks). See `tools/` for schema validation, dependency graph generation, pipeline dashboard, and reproducibility replay.

## Version Info
- **Version**: 3.8.0
- **Last Updated**: 2026-03-26
- **Author**: Pouria Mortezaagha
- **License**: CC-BY-NC 4.0
