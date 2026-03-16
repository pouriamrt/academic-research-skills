# Experimentation Skills Design Spec

**Date**: 2026-03-16
**Status**: Approved
**Author**: Pouria (design) + Claude (spec)
**Version**: 1.0

---

## Summary

Add 4 new skills to the academic-research-skills suite that bridge the gap between research design (`deep-research`) and paper writing (`academic-paper`): **experiment-designer**, **data-analyst**, **simulation-runner**, and **lab-notebook**. These skills handle the "doing" phase of research — designing experiments, executing statistical analyses, running computational simulations, and maintaining the research record.

## Key Design Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Execution scope | Full execution (generate + run Python) | Skills generate AND execute code, returning actual results |
| Pipeline integration | Flexible standalone + optional pipeline | Many projects don't need experiments; pipeline detects when needed |
| Domain scope | Broad quantitative sciences | Social + natural + computational sciences; no wet-lab |
| Environment management | Virtual environment per project | Isolated, reproducible, clean user environment |
| Output format | Markdown tables + APA stats + static plots (PNG/PDF) | Publication-ready results for the paper writing stage |
| Modes | Skill-specific (tailored per skill) | Each skill gets modes that make sense for its workflow |
| Architecture | Shared infrastructure + independent skills | Matches existing suite pattern; avoids duplication without over-coupling |

---

## 1. Shared Experiment Infrastructure

### `shared/experiment_infrastructure.md`

Provides instructions referenced by all 4 experiment skills.

#### 1.1 Venv Management Protocol

- Create venv at `./experiment_env/` on first use
- Core packages: `numpy`, `scipy`, `pandas`, `statsmodels`, `matplotlib`, `seaborn`, `pingouin`, `scikit-learn`
- `requirements.txt` generated and tracked
- Activation/deactivation handled automatically by each skill's execution agents
- If venv already exists, reuse it; only install missing packages

#### 1.2 APA Statistical Formatting Rules

- Standard formatting: `F(2, 87) = 4.32, p = .016, eta-sq = .09`
- Rounding rules: p-values to 3 decimals (except p < .001), test stats to 2 decimals, effect sizes to 2 decimals
- Effect size interpretation thresholds (small/medium/large per Cohen's conventions)
- Table formatting: APA 7 table style (no vertical lines, horizontal rules only at top, under header, bottom)

#### 1.3 Plot Generation Standards

- Default style: `seaborn-v0_8-whitegrid` with publication-quality DPI (300)
- Font: Times New Roman 12pt (matching LaTeX output)
- Color palette: colorblind-safe (`colorblind` from seaborn)
- Output: PNG (for preview) + PDF (for LaTeX inclusion)
- Saved to `./experiment_outputs/figures/`

#### 1.4 Output Directory Convention

```
./experiment_outputs/
  figures/          (plots: PNG + PDF)
  tables/           (CSV + formatted Markdown)
  scripts/          (generated .py files, reproducibility record)
  logs/             (lab notebook entries)
  reports/          (analysis reports, simulation reports)
```

---

## 2. Skill: `experiment-designer`

### 2.1 Overview

Designs experimental protocols — from power analysis to randomization schemes to instrument construction. The "architect" of the experiment phase.

### 2.2 Modes

| Mode | When to use | Output |
|------|------------|--------|
| `full` | Clear experiment goals, ready to design | Complete protocol + power analysis + instruments |
| `guided` | Unsure about design choices, want to explore trade-offs | Socratic dialogue -> protocol |
| `quick` | Need a rapid design sketch (e.g., for a grant proposal) | Simplified protocol, no instrument generation |
| `power-only` | Just need sample size / power calculation | Power analysis report only |
| `instrument` | Just need to build a survey/measure/rubric | Instrument + validity assessment only |

### 2.3 Agent Team (6 agents)

| # | Agent | Role | Phase |
|---|-------|------|-------|
| 1 | `intake_agent` | Parses user request, determines mode, validates that RQ/methodology blueprint exists (from `deep-research` or user-supplied) | Phase 0 |
| 2 | `design_architect_agent` | Core designer -- selects experimental design (RCT, quasi-experimental, factorial, crossover, etc.), defines IV/DV/controls, identifies threats to validity | Phase 1 |
| 3 | `power_analyst_agent` | Executes power analysis via Python (statsmodels, scipy) -- computes required sample size, detects minimum effect size, generates power curves | Phase 1 |
| 4 | `instrument_builder_agent` | Builds measurement instruments -- survey items, rubrics, coding schemes, observation protocols. Assesses content validity, suggests pilot testing | Phase 2 |
| 5 | `randomization_agent` | Designs allocation scheme -- simple random, stratified, block, cluster. Generates actual randomization sequences via Python (numpy) | Phase 2 |
| 6 | `protocol_compiler_agent` | Assembles the complete experiment protocol document, cross-validates all components for coherence, produces the Experiment Design handoff artifact (Schema 10) | Phase 3 |

### 2.4 Key Deliverables

1. **Experiment Protocol** -- Complete step-by-step protocol document
2. **Power Analysis Report** -- With power curves (plot), sample size tables, sensitivity analysis
3. **Instruments** -- Survey items, rubrics, coding schemes (if applicable)
4. **Randomization Schedule** -- Actual allocation sequences (if applicable)
5. **Threats-to-Validity Matrix** -- Identified threats + mitigation strategies
6. **Schema 10 Handoff Artifact** -- Structured data for downstream skills

### 2.5 Templates

- `experiment_protocol_template.md` -- Master protocol document
- `power_analysis_template.md` -- Power analysis report format
- `instrument_template.md` -- Survey/rubric/coding scheme format
- `threats_to_validity_template.md` -- Validity threat matrix

### 2.6 References

- `experimental_design_patterns.md` -- Design decision tree (RCT, factorial, crossover, quasi-experimental, single-subject, etc.)
- `power_analysis_guide.md` -- Effect size conventions, software usage, common pitfalls
- `instrument_development_guide.md` -- Item writing rules, validity/reliability types, pilot testing
- `randomization_methods.md` -- Allocation methods with code examples
- `equator_protocol_guidelines.md` -- SPIRIT (trials), STROBE (observational), CONSORT (reporting)

### 2.7 Integration Points

- **Upstream**: Consumes RQ Brief (Schema 1) + Methodology Blueprint from `deep-research`
- **Downstream**: Produces Experiment Design (Schema 10) consumed by `data-analyst`, `simulation-runner`, `lab-notebook`
- **Pipeline**: Inserted as optional stage between RESEARCH and WRITE when methodology is experimental/quasi-experimental

---

## 3. Skill: `data-analyst`

### 3.1 Overview

The execution engine for statistical analysis. Takes data and an analysis plan, runs the actual analyses in Python, and produces publication-ready results -- APA-formatted statistics, tables, and figures.

### 3.2 Modes

| Mode | When to use | Output |
|------|------------|--------|
| `full` | Have data + analysis plan, run everything | Complete analysis report + figures + tables |
| `guided` | Have data but unsure what analysis to run | Socratic dialogue about data -> analysis plan -> execution |
| `quick` | Need rapid descriptive stats + key test | Descriptive statistics + one primary analysis |
| `assumption-check` | Need to verify statistical assumptions before committing to a test | Normality, homogeneity, independence checks with recommendations |
| `exploratory` | No hypotheses, want to explore the dataset | EDA report -- distributions, correlations, outliers, missing data patterns |
| `replication` | Re-running someone else's analysis with their data | Execute a pre-specified analysis script, compare with reported results |

### 3.3 Agent Team (7 agents)

| # | Agent | Role | Phase |
|---|-------|------|-------|
| 1 | `intake_agent` | Parses user request, locates data files, detects file format (CSV/Excel/SPSS/Stata), loads and profiles the dataset (shape, types, missingness) | Phase 0 |
| 2 | `data_preparation_agent` | Cleans data -- handles missing values (listwise, pairwise, imputation), detects outliers (IQR, Z-score, Mahalanobis), recodes variables, creates computed variables. Executes Python, saves cleaned dataset | Phase 1 |
| 3 | `assumption_checker_agent` | Tests statistical assumptions -- normality (Shapiro-Wilk, Q-Q plots), homogeneity of variance (Levene's), sphericity (Mauchly's), linearity, multicollinearity (VIF). Produces assumption report with plots. Recommends parametric vs non-parametric | Phase 2 |
| 4 | `analysis_executor_agent` | Runs the primary analyses -- t-tests, ANOVA/ANCOVA, regression, chi-square, correlation, SEM, HLM, factor analysis, non-parametric alternatives. Uses scipy, statsmodels, pingouin, scikit-learn. Produces raw results | Phase 3 |
| 5 | `effect_size_agent` | Computes and interprets effect sizes -- Cohen's d, eta-sq, omega-sq, r-sq, odds ratios, Cramer's V. Computes confidence intervals. Classifies magnitude per Cohen's conventions and domain-specific benchmarks | Phase 3 |
| 6 | `visualization_agent` | Generates publication-quality figures -- bar charts, box plots, scatter plots, forest plots, interaction plots, residual plots, correlation heatmaps. Follows shared plot standards (300 DPI, colorblind-safe, PDF+PNG) | Phase 4 |
| 7 | `report_compiler_agent` | Assembles the complete analysis report -- APA-formatted results text, tables, figure captions, interpretation guide. Produces Schema 11 handoff artifact for `academic-paper` | Phase 5 |

### 3.4 Statistical Methods Coverage

| Category | Methods |
|----------|---------|
| **Descriptive** | Mean, SD, median, IQR, frequencies, crosstabs, skewness, kurtosis |
| **Comparison (2 groups)** | Independent t-test, paired t-test, Mann-Whitney U, Wilcoxon signed-rank |
| **Comparison (3+ groups)** | One-way ANOVA, repeated measures ANOVA, factorial ANOVA, ANCOVA, Kruskal-Wallis, Friedman |
| **Post-hoc** | Tukey HSD, Bonferroni, Games-Howell, Dunn's test |
| **Correlation** | Pearson, Spearman, Kendall, partial correlation, point-biserial |
| **Regression** | Simple/multiple linear, logistic (binary/multinomial/ordinal), hierarchical, stepwise |
| **Factor analysis** | EFA (principal axis, ML), CFA (via semopy), reliability (Cronbach's alpha, McDonald's omega) |
| **Non-parametric** | Chi-square (goodness of fit, independence), Fisher's exact, McNemar's |
| **Advanced** | Multilevel/HLM (via statsmodels MixedLM), mediation (Baron-Kenny + bootstrap), moderation, SEM (via semopy) |
| **Survival** | Kaplan-Meier, log-rank, Cox proportional hazards (via lifelines) |
| **Bayesian** | Bayesian t-test, Bayesian correlation (via pingouin) |

### 3.5 Key Deliverables

1. **Cleaned Dataset** -- Saved to `experiment_outputs/` with cleaning log
2. **Assumption Check Report** -- With diagnostic plots
3. **Analysis Results** -- APA-formatted text blocks ready for paper insertion
4. **Tables** -- APA 7 formatted (CSV + Markdown), numbered (Table 1, Table 2...)
5. **Figures** -- Publication-quality plots (PNG + PDF), numbered (Figure 1, Figure 2...)
6. **Reproducibility Script** -- Complete `.py` file that re-runs the entire analysis from raw data
7. **Schema 11 Handoff Artifact** -- Structured results for `academic-paper`

### 3.6 Templates

- `analysis_report_template.md` -- Full analysis report format
- `apa_results_template.md` -- APA results section text patterns (per test type)
- `assumption_report_template.md` -- Assumption check report format
- `data_cleaning_log_template.md` -- Data preparation documentation

### 3.7 References

- `statistical_test_decision_tree.md` -- Which test for which data/question combination
- `assumption_testing_guide.md` -- When and how to test each assumption
- `apa_stats_formatting_guide.md` -- APA 7 formatting rules for every statistical test
- `effect_size_interpretation_guide.md` -- Conventions, domain-specific benchmarks, CI computation
- `missing_data_strategies.md` -- Listwise, pairwise, MI, FIML -- when to use which
- `common_analysis_pitfalls.md` -- Multiple comparisons, p-hacking, HARKing, outlier handling mistakes

### 3.8 Additional Venv Packages

Beyond the shared core packages:
- `semopy` (SEM/CFA)
- `lifelines` (survival analysis)
- `openpyxl` (Excel reading)
- `pyreadstat` (SPSS/Stata file reading)

### 3.9 Integration Points

- **Upstream**: Consumes Experiment Design (Schema 10) from `experiment-designer` for pre-planned analysis, OR user-provided data + ad-hoc analysis request
- **Downstream**: Produces Experiment Results (Schema 11) consumed by `academic-paper/draft_writer_agent` for the Results section, and by `lab-notebook` for the research record
- **Pipeline**: Inserted as optional stage after EXPERIMENT-DESIGN, before WRITE

---

## 4. Skill: `simulation-runner`

### 4.1 Overview

Designs and executes computational experiments -- Monte Carlo simulations, agent-based models, parameter sweeps, bootstrap analyses, and sensitivity analyses. Generates data through computational models to answer "what if" questions, estimate distributions, or validate analytical results.

### 4.2 Modes

| Mode | When to use | Output |
|------|------------|--------|
| `full` | Have a model specification, run complete simulation study | Full simulation report + convergence diagnostics + figures |
| `guided` | Know what you want to simulate but unsure about model specification or parameters | Socratic dialogue -> model spec -> execution |
| `quick` | Need a fast simulation (e.g., single Monte Carlo with default iterations) | Streamlined report, reduced iterations |
| `power-sim` | Power analysis via simulation (when analytical power formulas don't exist) | Simulated power curves for complex designs |
| `sensitivity` | Systematically vary parameters to test robustness | Sensitivity analysis report with tornado/spider plots |
| `bootstrap` | Bootstrap resampling of existing data for CIs or hypothesis testing | Bootstrap distribution + CI report |

### 4.3 Agent Team (5 agents)

| # | Agent | Role | Phase |
|---|-------|------|-------|
| 1 | `intake_agent` | Parses request, determines simulation type, validates inputs (existing data for bootstrap, model spec for Monte Carlo, or Experiment Design Schema 10/13 for pre-planned simulations) | Phase 0 |
| 2 | `model_builder_agent` | Translates the conceptual model into executable Python code -- defines data-generating process (DGP), parameters, distributions, stopping rules. For agent-based models: defines agents, rules, environment, interaction topology | Phase 1 |
| 3 | `execution_engine_agent` | Runs the simulation -- manages iterations, seeds for reproducibility, parallel execution where possible. Monitors convergence (Monte Carlo error, Gelman-Rubin R-hat). Implements early stopping if convergence criteria met | Phase 2 |
| 4 | `diagnostics_agent` | Assesses simulation quality -- convergence diagnostics, trace plots, autocorrelation, effective sample size. For parameter sweeps: generates heatmaps, tornado plots, spider plots. Flags non-convergence or instability | Phase 3 |
| 5 | `report_compiler_agent` | Assembles simulation report -- model specification, parameter tables, results summary, diagnostic plots, reproducibility seed log. Produces Schema 11 handoff artifact and Schema 13 for the model spec | Phase 4 |

### 4.4 Simulation Types Coverage

| Category | Methods |
|----------|---------|
| **Monte Carlo** | Distribution estimation, integration, hypothesis testing simulation, Type I/II error rates |
| **Bootstrap** | Non-parametric bootstrap, parametric bootstrap, BCa confidence intervals, permutation tests |
| **Power simulation** | Simulated power for mixed designs, multilevel models, SEM, non-standard effect sizes |
| **Parameter sweep** | Grid search, Latin hypercube sampling, one-at-a-time (OAT) sensitivity |
| **Agent-based** | Simple agent-based models -- agents with rules, spatial/network topology, emergent behavior tracking |
| **Resampling** | Cross-validation (k-fold, LOOCV, stratified), jackknife |
| **Stochastic processes** | Random walks, Markov chains, queuing models, birth-death processes |
| **Optimization** | Simple optimization via scipy.optimize -- grid search, Nelder-Mead, differential evolution |

### 4.5 Key Deliverables

1. **Model Specification Document** -- Mathematical model, DGP, parameters, assumptions
2. **Simulation Code** -- Complete `.py` script with seed management for full reproducibility
3. **Results Summary** -- Point estimates, CIs, convergence status, iteration count
4. **Diagnostic Report** -- Convergence plots, trace plots, autocorrelation, effective sample size
5. **Figures** -- Distribution plots, power curves, heatmaps, tornado plots (PNG + PDF)
6. **Seed Log** -- All random seeds used, for exact replication
7. **Schema 11 Handoff Artifact** -- Structured results for `academic-paper`

### 4.6 Templates

- `simulation_report_template.md` -- Full simulation study report
- `model_specification_template.md` -- Mathematical model documentation
- `convergence_report_template.md` -- Convergence diagnostics format
- `parameter_sweep_template.md` -- Sensitivity analysis report format

### 4.7 References

- `simulation_design_patterns.md` -- Decision tree for choosing simulation type
- `convergence_criteria_guide.md` -- When to stop iterating, Monte Carlo standard error thresholds, R-hat interpretation
- `seed_management_guide.md` -- Reproducibility best practices, numpy Generator vs legacy RandomState
- `parallel_execution_guide.md` -- When and how to parallelize (multiprocessing, joblib)
- `reporting_simulation_studies.md` -- ADEMP framework for simulation study reporting

### 4.8 Additional Venv Packages

Beyond the shared core packages:
- `joblib` (parallel execution)
- `networkx` (agent-based model topologies)
- `tqdm` (progress bars for long simulations)

### 4.9 Integration Points

- **Upstream**: Consumes Experiment Design (Schema 10) or Simulation Specification (Schema 13) from `experiment-designer`, OR ad-hoc user request
- **Downstream**: Produces Experiment Results (Schema 11) consumed by `academic-paper` and `lab-notebook`
- **Cross-skill**: `data-analyst` can invoke `simulation-runner` for bootstrap CIs or power simulations; `experiment-designer/power_analyst_agent` can delegate complex power analyses to `simulation-runner` in `power-sim` mode
- **Pipeline**: Optional stage, invoked when methodology involves computational experiments

---

## 5. Skill: `lab-notebook`

### 5.1 Overview

The research record keeper. Tracks the entire experiment lifecycle -- from design decisions through data collection, analysis, and results. Creates a timestamped, append-only log that serves as the provenance chain, meeting reproducibility standards and providing raw material for the Methods section.

### 5.2 Modes

| Mode | When to use | Output |
|------|------------|--------|
| `full` | Track a complete experiment lifecycle from design to results | Complete lab notebook document |
| `log-entry` | Add a single entry to an existing notebook | Appended entry with timestamp |
| `deviation` | Record a protocol deviation | Deviation entry with justification + impact assessment |
| `snapshot` | Capture current experiment state | Status summary report |
| `export` | Export the notebook for paper writing or archival | Formatted export (Markdown / PDF) + Schema 12 handoff artifact |
| `audit` | Review notebook completeness | Audit report with gaps identified |

### 5.3 Agent Team (4 agents)

| # | Agent | Role | Phase |
|---|-------|------|-------|
| 1 | `notebook_manager_agent` | Creates and manages notebook files. Handles mode routing, validates that a notebook exists (or creates one), manages the append-only log structure. Assigns entry IDs and timestamps | Always |
| 2 | `entry_writer_agent` | Writes structured log entries -- parses inputs from other skills (Schema 10, 11) or user-provided free text, structures them into standardized entry format with required fields, links to related entries | Always |
| 3 | `deviation_tracker_agent` | Specialized handler for protocol deviations -- records what changed, why, impact assessment on internal/external validity, whether the analysis plan needs updating. Cross-references original protocol (Schema 10) | On deviation |
| 4 | `provenance_auditor_agent` | Reviews the notebook for completeness -- checks that all pipeline stages are documented, all data files have provenance, all deviations are recorded, all results link back to methods. Produces audit report | On audit/export |

### 5.4 Notebook Structure

Single Markdown file per experiment, append-only:

```
./experiment_outputs/logs/
  notebook_YYYY-MM-DD_<experiment-name>.md
```

**Notebook sections (auto-created, populated over time):**

| Section | Populated by | Content |
|---------|-------------|---------|
| **Header** | `notebook_manager_agent` | Title, PI, date created, experiment ID, status |
| **1. Design Record** | Auto from Schema 10 | Experiment protocol summary, hypotheses, variables, sample size rationale |
| **2. Environment Record** | Auto from venv setup | Python version, package versions, OS, hardware |
| **3. Data Collection Log** | User entries via `log-entry` mode | Timestamped entries: what data was collected, when, by whom, any notes |
| **4. Data Preparation Log** | Auto from `data-analyst` Phase 1 | Cleaning steps, transformations, exclusions with reasons |
| **5. Analysis Log** | Auto from `data-analyst` Schema 11 | Analyses run, results summary, script file references |
| **6. Simulation Log** | Auto from `simulation-runner` Schema 11 | Model specs, iteration counts, seeds, convergence status |
| **7. Deviation Log** | User entries via `deviation` mode | Protocol deviations with justification and impact |
| **8. Decision Log** | User entries via `log-entry` mode | Key decisions made during the experiment and rationale |
| **9. File Manifest** | `provenance_auditor_agent` | All files produced, their purpose, creation timestamp, hash |
| **10. Audit Trail** | `provenance_auditor_agent` | Completeness checks, Material Passport references |

### 5.5 Entry Format

Every entry follows a consistent structure:

```markdown
### Entry [NB-XXX] -- YYYY-MM-DD HH:MM
- **Type**: design | collection | preparation | analysis | simulation | deviation | decision | note
- **Author**: [human name or skill name]
- **Related entries**: [NB-XXX, NB-XXX]
- **Related files**: [file paths]

[Content]

---
```

### 5.6 Key Deliverables

1. **Lab Notebook File** -- Append-only Markdown document, the primary research record
2. **File Manifest** -- Complete inventory of all experiment artifacts with hashes
3. **Audit Report** -- Completeness assessment against protocol
4. **Schema 12 Handoff Artifact** -- Structured lab record for `academic-paper` (Methods section) and `academic-pipeline`
5. **Environment Snapshot** -- Frozen requirements, Python version, OS info

### 5.7 Templates

- `notebook_template.md` -- Master notebook structure with all 10 sections
- `entry_templates.md` -- Per-type entry templates (collection, deviation, decision, etc.)
- `audit_checklist_template.md` -- Completeness checklist
- `file_manifest_template.md` -- Artifact inventory format

### 5.8 References

- `lab_notebook_best_practices.md` -- What makes a good research record, legal/regulatory requirements
- `reproducibility_standards.md` -- FAIR principles, computational reproducibility checklist, TOP guidelines
- `deviation_handling_guide.md` -- How to document deviations, impact assessment framework, when a deviation invalidates results
- `provenance_tracking_guide.md` -- File hashing, version tracking, upstream dependency chains

### 5.9 No Additional Venv Packages

`lab-notebook` uses only `hashlib` (stdlib) for file hashing. No extra packages needed beyond the shared core.

### 5.10 Integration Points

- **Upstream**: Consumes Schema 10 (from `experiment-designer`), Schema 11 (from `data-analyst` and `simulation-runner`), and user free-text entries
- **Downstream**: Produces Schema 12 (Lab Record) consumed by `academic-paper/draft_writer_agent` for Methods section provenance, and by `academic-pipeline` for process documentation
- **Auto-logging**: When other experiment skills execute, they can push entries to the notebook automatically (if one exists for the current experiment)
- **Pipeline**: Optional stage, runs continuously alongside other experiment stages rather than as a discrete step

---

## 6. Pipeline Integration

### 6.1 Updated Pipeline Flow

```
Stage 1: RESEARCH (deep-research)
  -> Methodology Blueprint says experimental/quasi-experimental/simulation?
    |-- Yes -> Stage 1.5: EXPERIMENT (new, optional)
    |         |-- 1.5a: DESIGN (experiment-designer)
    |         |-- 1.5b: EXECUTE (data-analyst and/or simulation-runner)
    |         |-- 1.5c: LOG (lab-notebook, continuous)
    |         +-- User checkpoint
    +-- No -> Skip to Stage 2
Stage 2: WRITE (academic-paper)
  -> Now receives Schema 11 results + Schema 12 lab record in addition to existing schemas
Stage 2.5: INTEGRITY (existing)
  -> Extended to also verify experiment results match analysis scripts
Stage 3-9: (existing stages unchanged)
```

### 6.2 Detection Logic

```
Trigger experimentation stages when methodology_type in Methodology Blueprint matches:
- "experimental"           -> experiment-designer (full) + data-analyst
- "quasi-experimental"     -> experiment-designer (full) + data-analyst
- "simulation"             -> experiment-designer (guided) + simulation-runner
- "mixed" with quant strand -> experiment-designer + data-analyst
- "correlational" with primary data -> data-analyst only (no design needed)
- "secondary data analysis" -> data-analyst only
- All others               -> skip experimentation
```

### 6.3 Updated CLAUDE.md Routing Rules

New additions:

```
6. experiment-designer vs data-analyst: experiment-designer = upstream design
   (protocol, power, instruments), data-analyst = downstream execution (run the
   actual stats). If user has data and wants analysis, go straight to data-analyst.
   If user needs to plan an experiment first, start with experiment-designer.

7. data-analyst vs simulation-runner: data-analyst = real data,
   simulation-runner = generated/synthetic data. If user says "bootstrap" or
   "Monte Carlo" with existing data, that's simulation-runner. If user says
   "run a regression on my data", that's data-analyst.

8. lab-notebook: Never runs alone as a first step. Always accompanies other
   experiment skills. Automatically invoked by pipeline when experiment stages
   are active. Can be invoked standalone for log-entry or audit after the fact.
```

---

## 7. New Handoff Schemas

### Schema 10: Experiment Design

**Producer**: `experiment-designer/protocol_compiler_agent`
**Consumer**: `data-analyst/intake_agent` | `simulation-runner/intake_agent` | `lab-notebook/entry_writer_agent`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `experiment_id` | string | Yes | Unique experiment identifier |
| `design_type` | enum | Yes | `RCT` / `quasi_experimental` / `factorial` / `crossover` / `single_subject` / `correlational` / `simulation` |
| `hypotheses` | list[Hypothesis] | Yes | Pre-registered hypotheses with direction |
| `variables` | object | Yes | `{independent: list[Variable], dependent: list[Variable], control: list[Variable], moderator: list[Variable], mediator: list[Variable]}` |
| `sample` | object | Yes | `{target_n: int, power: float, alpha: float, effect_size: string, attrition_buffer: float}` |
| `randomization` | object | Conditional | `{method: string, seed: int, allocation_ratio: string, schedule: list}` (required if RCT/factorial) |
| `instruments` | list[Instrument] | Conditional | Measurement instruments (if primary data collection) |
| `analysis_plan` | object | Yes | `{primary: list[AnalysisSpec], secondary: list[AnalysisSpec], exploratory: list[AnalysisSpec]}` |
| `validity_threats` | list[Threat] | Yes | Identified threats with mitigation strategies |
| `protocol_document` | string | Yes | Path to full protocol file |
| `timeline` | list[Milestone] | Yes | Data collection and analysis milestones |

### Schema 11: Experiment Results

**Producer**: `data-analyst/report_compiler_agent` | `simulation-runner/report_compiler_agent`
**Consumer**: `academic-paper/draft_writer_agent` | `lab-notebook/entry_writer_agent`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `experiment_id` | string | Yes | Links to Schema 10 |
| `result_type` | enum | Yes | `statistical_analysis` / `simulation` / `bootstrap` / `exploratory` |
| `dataset_info` | object | Yes | `{n_original: int, n_analyzed: int, exclusions: list[string], missing_strategy: string}` |
| `assumption_checks` | list[AssumptionCheck] | Yes | Each assumption tested with result and decision |
| `primary_results` | list[AnalysisResult] | Yes | Primary analysis results |
| `secondary_results` | list[AnalysisResult] | No | Secondary analysis results |
| `effect_sizes` | list[EffectSize] | Yes | All effect sizes with CIs |
| `tables` | list[Table] | Yes | `{id: string, caption: string, file_path: string, apa_formatted: string}` |
| `figures` | list[Figure] | Yes | `{id: string, caption: string, png_path: string, pdf_path: string}` |
| `apa_results_text` | object | Yes | `{primary: string, secondary: string, exploratory: string}` -- ready-to-insert APA text |
| `reproducibility` | object | Yes | `{script_path: string, seed: int, environment: string, requirements_path: string}` |

### Schema 12: Lab Record

**Producer**: `lab-notebook/provenance_auditor_agent`
**Consumer**: `academic-paper/draft_writer_agent` | `academic-pipeline/pipeline_orchestrator_agent`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `experiment_id` | string | Yes | Links to Schema 10 |
| `notebook_path` | string | Yes | Path to the notebook file |
| `entry_count` | integer | Yes | Total entries |
| `deviation_count` | integer | Yes | Number of protocol deviations |
| `deviations_summary` | list[string] | Conditional | Summary of each deviation (if any) |
| `file_manifest` | list[FileRecord] | Yes | `{path: string, purpose: string, hash: string, created: string}` |
| `completeness_score` | float | Yes | 0.0-1.0 audit completeness |
| `completeness_gaps` | list[string] | No | Sections that are incomplete |
| `environment_snapshot` | object | Yes | `{python_version: string, packages: dict, os: string}` |
| `methods_summary` | string | Yes | Condensed narrative for paper Methods section |

### Schema 13: Simulation Specification

**Producer**: `experiment-designer/protocol_compiler_agent`
**Consumer**: `simulation-runner/model_builder_agent`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `experiment_id` | string | Yes | Links to Schema 10 |
| `simulation_type` | enum | Yes | `monte_carlo` / `bootstrap` / `power_sim` / `agent_based` / `parameter_sweep` / `stochastic_process` |
| `model_definition` | object | Yes | `{description: string, dgp: string, parameters: dict, distributions: dict}` |
| `execution_plan` | object | Yes | `{n_iterations: int, burn_in: int, convergence_criterion: string, seeds: list[int]}` |
| `performance_measures` | list[string] | Yes | What to measure (bias, MSE, coverage, power, etc.) |
| `parameter_grid` | object | No | For parameter sweeps: `{param_name: [values]}` |
| `ademp_checklist` | object | Yes | `{aims: string, dgp: string, estimands: list, methods: list, performance: list}` |

---

## 8. Updated Skills Overview

| Skill | Version | Purpose | Key Modes |
|-------|---------|---------|-----------|
| `deep-research` | v2.3 | Universal research team | full, quick, socratic, review, lit-review, fact-check, systematic-review |
| `experiment-designer` | v1.0 | Experiment protocol and power analysis | full, guided, quick, power-only, instrument |
| `data-analyst` | v1.0 | Statistical analysis execution | full, guided, quick, assumption-check, exploratory, replication |
| `simulation-runner` | v1.0 | Computational experiments | full, guided, quick, power-sim, sensitivity, bootstrap |
| `lab-notebook` | v1.0 | Experiment research record | full, log-entry, deviation, snapshot, export, audit |
| `academic-paper` | v2.4 | Academic paper writing | full, plan, outline-only, revision, abstract-only, lit-review, format-convert, citation-check |
| `academic-paper-reviewer` | v1.4 | Multi-perspective paper review | full, re-review, quick, methodology-focus, guided |
| `academic-pipeline` | v2.7 | Full pipeline orchestrator | (coordinates all above) |

---

## 9. File Inventory

### New Directories and Files

```
experiment-designer/
  SKILL.md
  agents/
    intake_agent.md
    design_architect_agent.md
    power_analyst_agent.md
    instrument_builder_agent.md
    randomization_agent.md
    protocol_compiler_agent.md
  templates/
    experiment_protocol_template.md
    power_analysis_template.md
    instrument_template.md
    threats_to_validity_template.md
  references/
    experimental_design_patterns.md
    power_analysis_guide.md
    instrument_development_guide.md
    randomization_methods.md
    equator_protocol_guidelines.md

data-analyst/
  SKILL.md
  agents/
    intake_agent.md
    data_preparation_agent.md
    assumption_checker_agent.md
    analysis_executor_agent.md
    effect_size_agent.md
    visualization_agent.md
    report_compiler_agent.md
  templates/
    analysis_report_template.md
    apa_results_template.md
    assumption_report_template.md
    data_cleaning_log_template.md
  references/
    statistical_test_decision_tree.md
    assumption_testing_guide.md
    apa_stats_formatting_guide.md
    effect_size_interpretation_guide.md
    missing_data_strategies.md
    common_analysis_pitfalls.md

simulation-runner/
  SKILL.md
  agents/
    intake_agent.md
    model_builder_agent.md
    execution_engine_agent.md
    diagnostics_agent.md
    report_compiler_agent.md
  templates/
    simulation_report_template.md
    model_specification_template.md
    convergence_report_template.md
    parameter_sweep_template.md
  references/
    simulation_design_patterns.md
    convergence_criteria_guide.md
    seed_management_guide.md
    parallel_execution_guide.md
    reporting_simulation_studies.md

lab-notebook/
  SKILL.md
  agents/
    notebook_manager_agent.md
    entry_writer_agent.md
    deviation_tracker_agent.md
    provenance_auditor_agent.md
  templates/
    notebook_template.md
    entry_templates.md
    audit_checklist_template.md
    file_manifest_template.md
  references/
    lab_notebook_best_practices.md
    reproducibility_standards.md
    deviation_handling_guide.md
    provenance_tracking_guide.md

shared/
  experiment_infrastructure.md  (NEW)
  handoff_schemas.md            (UPDATED -- add schemas 10-13)
```

**Total new files: 54**
**Modified files: 3** (shared/handoff_schemas.md, .claude/CLAUDE.md, academic-pipeline/SKILL.md)
