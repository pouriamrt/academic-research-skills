# Academic Research Skills

A suite of Claude Code skills for rigorous academic research, paper writing, peer review, and pipeline orchestration.

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

## Full Academic Pipeline

```
deep-research (socratic/full)
  → [EXPERIMENT — optional, when methodology is experimental/quasi-experimental/simulation]
    → experiment-designer (full/guided)
      → data-analyst (full) and/or simulation-runner (full)
        → lab-notebook (continuous, auto-logging)
  → academic-paper (plan/full)
    → academic-paper-reviewer (full/guided)
      → academic-paper (revision)
        → academic-paper-reviewer (re-review, max 2 loops)
          → academic-paper (format-convert → final output)
```

The experiment stages are auto-detected from the Methodology Blueprint produced by deep-research. If the methodology does not require experimentation (e.g., literature review, theoretical, policy analysis), these stages are skipped entirely.

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

## Version Info
- **Version**: 3.0
- **Last Updated**: 2026-03-16
- **Author**: Cheng-I Wu
- **License**: CC-BY-NC 4.0
