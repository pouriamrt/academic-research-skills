# Mode Registry

Single source of truth for all modes across the ARS suite. **50 modes** across 8 skills.

When adding or modifying modes, update this file first — SKILL.md files and CLAUDE.md should reference this registry.

Last updated: v3.21.0 (2026-08-03)

---

## deep-research (8 modes)

| Mode | Spectrum | Output | Oversight | Triggers |
|------|----------|--------|-----------|----------|
| `full` | Balanced | APA 7.0 report, 3,000-8,000 words | High | "research [topic]", "deep research", "academic analysis" |
| `quick` | Fidelity | Research brief, 500-1,500 words | Medium | "quick brief", "30 minute summary", "quick research" |
| `review` | Balanced | Reviewer report on provided text | High | "review this paper", "evaluate this paper", "assess this source" |
| `lit-review` | Fidelity | Annotated bibliography + synthesis | Medium | "literature review", "annotated bibliography" |
| `three-way-scan` | Fidelity | WHY/HOW/WHAT paper shortlist + cross-paper synthesis | Low | "WHY HOW WHAT papers", "3W literature scan", "compare these papers" |
| `fact-check` | Fidelity | Claim-by-claim verification report | Medium | "verify claims", "fact-check", "evidence verification" |
| `socratic` | Originality | Research Plan Summary + INSIGHT collection | Very High | "guide my research", "help me think through", "I'm not sure what to research" |
| `systematic-review` | Fidelity | PRISMA 2020 report, 5,000-15,000 words | Medium | "systematic review", "meta-analysis", "PRISMA" |

## academic-paper (11 modes)

| Mode | Spectrum | Output | Oversight | Triggers |
|------|----------|--------|-----------|----------|
| `full` | Balanced | Complete paper draft (IMRaD or domain-appropriate) | High | "write a paper", "academic paper", "research paper" |
| `plan` | Originality | Chapter Plan + INSIGHT collection (Socratic) | Very High | "guide my paper", "help me plan", "step by step paper" |
| `outline-only` | Balanced | Detailed outline + evidence map | High | "paper outline", "just need an outline" |
| `revision` | Fidelity | Revised draft + point-by-point R&R responses | High | "revise paper", "incorporate reviewer feedback" |
| `revision-coach` | Balanced | Reviewer path: Revision Roadmap + Response Letter Skeleton. Explicit real-committee variant: source-accounted concern tracker + placeholder response skeleton | Medium | "parse reviews", "I got reviewer comments", "track these committee comments" |
| `abstract-only` | Fidelity | English abstract (150-300 words, structured) + 5-7 keywords | Medium | "write abstract" |
| `lit-review` | Fidelity | Annotated bibliography in paper format | Medium | "literature review paper", "write a lit review" |
| `format-convert` | Fidelity | Formatted document (LaTeX/DOCX-via-Pandoc/PDF/MD) | Low | "convert to LaTeX", "convert citations to [format]" |
| `citation-check` | Fidelity | Citation error report | Low | "check citations", "verify references" |
| `disclosure` | Fidelity | Default venue path: applicability/status bundle; policy-anchor path: anchor-specific render | Low | "AI disclosure for [venue]", "generate AI usage statement" |
| `rebuttal-audit` | Fidelity | Advisory QA of an existing rebuttal draft (per-comment coverage + gaps + risk flags); no generation; no Schema 11 emission | Low | "audit my response", "check my rebuttal", "did I miss any reviewer comment" |

## academic-paper-reviewer (6 modes)

| Mode | Spectrum | Output | Oversight | Triggers |
|------|----------|--------|-----------|----------|
| `full` | Balanced | 5 review reports + Editorial Decision + Revision Roadmap | High | "review paper", "peer review", "manuscript review" |
| `re-review` | Fidelity | Revision verification checklist + residual issues | Medium | "check revisions", "verification review" |
| `quick` | Fidelity | Journal-Fit Reviewer quick assessment + key issues list | Low | "quick review", "quick look" |
| `methodology-focus` | Fidelity | In-depth methodology review | Medium | "check methodology", "focus on methods" |
| `guided` | Originality | Socratic issue-by-issue dialogue | Very High | "guide me to improve", "walk me through issues" |
| `calibration` | Fidelity | Explicit 3-paper directional readout or default full Calibration Report + tier-scoped disclosure | Medium | "calibrate reviewer", "measure reviewer accuracy" |

## experiment-designer (5 modes)

| Mode | Spectrum | Output | Oversight | Triggers |
|------|----------|--------|-----------|----------|
| `full` | Balanced | Complete protocol (Schema 10) + power analysis + instruments + randomization | High | "design experiment", "experimental design", "plan experiment", "write protocol" |
| `guided` | Originality | Design Blueprint + recommendations, can transition to `full` | Very High | "help me design", "walk me through the design" |
| `quick` | Fidelity | Design brief + sample size estimate | Medium | "quick design", "rough design brief" |
| `power-only` | Fidelity | Power analysis report with curves | Medium | "power analysis", "sample size calculation", "how many participants" |
| `instrument` | Balanced | Instrument package (survey / rubric / coding scheme) | High | "create survey", "build instrument", "design a rubric" |

## data-analyst (6 modes)

| Mode | Spectrum | Output | Oversight | Triggers |
|------|----------|--------|-----------|----------|
| `full` | Fidelity | Full analysis report + Schema 11 | High | "analyze data", "run statistics", "statistical analysis" |
| `guided` | Balanced | Interactive test selection, then the full pipeline | Very High | "help me choose a test", "walk me through the analysis" |
| `quick` | Fidelity | Descriptive stats + key results | Medium | "quick stats", "just the descriptives" |
| `assumption-check` | Fidelity | Assumption report + diagnostic plots | Medium | "check assumptions", "is my data normal" |
| `exploratory` | Balanced | EDA report with distributions and correlations | Medium | "explore data", "EDA", "what's in this dataset" |
| `replication` | Fidelity | Replication report with original-study comparison | High | "replicate analysis", "reproduce these results" |

## simulation-runner (6 modes)

| Mode | Spectrum | Output | Oversight | Triggers |
|------|----------|--------|-----------|----------|
| `full` | Fidelity | Full ADEMP report + Schema 11 + convergence diagnostics | High | "Monte Carlo", "simulation", "computational experiment" |
| `guided` | Balanced | Simulation Brief, then the full pipeline | Very High | "help me design a simulation" |
| `quick` | Fidelity | Summary results, no convergence analysis | Medium | "quick simulation", "rough estimate" |
| `power-sim` | Fidelity | Power curve + sample size recommendation | Medium | "power simulation", "simulate power" |
| `sensitivity` | Fidelity | Tornado / spider plots + robust region map | Medium | "sensitivity analysis", "parameter sweep" |
| `bootstrap` | Fidelity | Bootstrap distribution + CIs (percentile, BCa) | Medium | "bootstrap", "resampling", "permutation test" |

## lab-notebook (6 modes)

| Mode | Spectrum | Output | Oversight | Triggers |
|------|----------|--------|-----------|----------|
| `full` | Fidelity | New notebook file + initial entries + audit | High | "lab notebook", "start a research record" |
| `log-entry` | Fidelity | Appended entry in an existing notebook | Low | "log experiment", "record this step" |
| `deviation` | Fidelity | Deviation entry with impact assessment | Medium | "record deviation", "we changed the protocol" |
| `snapshot` | Fidelity | Status summary (displayed, not written) | Low | "experiment snapshot", "where are we" |
| `export` | Fidelity | Schema 12 Lab Record artifact | Medium | "export notebook", "hand off the lab record" |
| `audit` | Fidelity | Audit report + completeness score | Medium | "audit notebook", "is the record complete" |

## academic-pipeline (1 orchestrator + 1 resume mode)

| Mode | Spectrum | Output | Oversight | Triggers |
|------|----------|--------|-----------|----------|
| (pipeline) | Balanced | 10-stage orchestrated workflow | Very High | "academic pipeline", "research to paper", "full paper workflow" |
| `resume_from_passport=<hash>` | Fidelity | Resume a prior pipeline run from a Material Passport reset boundary. Opt-in (`ARS_PASSPORT_RESET=1`). See `academic-pipeline/references/passport_as_reset_boundary.md`. | High | "resume from passport", "continue pipeline from reset boundary" |

---

## Summary

| Metric | Count |
|--------|-------|
| Total modes | 50 |
| Fidelity | 33 (66%) |
| Balanced | 12 (24%) |
| Originality | 5 (10%) |

### Oversight levels

| Level | Meaning |
|-------|---------|
| Very High | User-led dialogue or mandatory checkpoints at every stage |
| High | User confirms key decisions (RQ, outline, configuration) |
| Medium | Structured format with limited decision points |
| Low | Mechanical/template-driven, minimal human input |
