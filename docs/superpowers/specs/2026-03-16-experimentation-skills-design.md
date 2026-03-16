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

#### 1.5 Agent Naming Convention

Agent names are scoped to their skill directory. Multiple skills may have agents with the same name (e.g., `intake_agent`). When referencing agents cross-skill, always use the fully-qualified path: `skill-name/agent_name` (e.g., `data-analyst/intake_agent` vs `simulation-runner/intake_agent`). This matches the convention used in `shared/handoff_schemas.md` producer/consumer fields.

#### 1.6 Auto-Logging Protocol

When experiment skills (`experiment-designer`, `data-analyst`, `simulation-runner`) execute within the pipeline, they check for an existing notebook at `./experiment_outputs/logs/notebook_*.md` at the start of execution. If a notebook exists:

1. The pipeline orchestrator passes `notebook_path` as a parameter to each experiment skill
2. At the end of each agent phase, the skill appends a structured entry to the notebook file using the entry format defined in Section 5.5
3. Entries are appended directly (file append) -- lab-notebook agents are NOT invoked mid-execution to avoid circular dependencies
4. The `lab-notebook` skill's `provenance_auditor_agent` validates all auto-logged entries during `audit` or `export` mode

If no notebook exists and the pipeline is active, the pipeline orchestrator creates one via `lab-notebook` (full mode) at the start of Stage 1.5 before dispatching other experiment skills.

When experiment skills run standalone (outside the pipeline), auto-logging is disabled. Users can manually invoke `lab-notebook` (log-entry mode) to record results after the fact.

#### 1.7 Failure Paths

Common failure scenarios across all experiment skills. Each skill's SKILL.md will reference this shared section and add skill-specific failures.

| Failure | Trigger | Recovery |
|---------|---------|----------|
| `VENV_CREATE_FAILED` | Cannot create virtual environment (permissions, disk space) | Report error, suggest manual venv creation, provide requirements.txt |
| `PACKAGE_INSTALL_FAILED` | pip install fails (network, version conflict) | Report specific package, suggest alternatives, continue with available packages if possible |
| `DATA_FILE_NOT_FOUND` | User-specified data file does not exist | Prompt user for correct path, list files in current directory |
| `DATA_FORMAT_UNREADABLE` | File format not recognized or corrupted | Report detected format, suggest conversion, list supported formats |
| `EXECUTION_TIMEOUT` | Python script exceeds reasonable execution time (>10 min) | Kill process, report last output, suggest reducing iterations/sample size |
| `CONVERGENCE_FAILURE` | Simulation or optimization does not converge | Report diagnostics, suggest parameter adjustment, offer manual override |
| `ALL_ASSUMPTIONS_VIOLATED` | Every statistical assumption fails for chosen test | Recommend non-parametric alternative, present options to user, do not proceed without user confirmation |
| `POWER_TOO_LOW` | Computed power < 0.80 for feasible sample size | Report power table, suggest effect size or design changes, warn but do not block |
| `NOTEBOOK_CORRUPTED` | Lab notebook file is malformed or unreadable | Create backup, start fresh notebook, attempt to salvage entries |
| `HANDOFF_INCOMPLETE` | Required schema fields missing in upstream handoff | Report missing fields, request re-generation from upstream skill |
| `SCHEMA_VALIDATION_FAILED` | Handoff artifact does not conform to schema | Report specific violations, request correction |

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

### 2.2b Trigger Conditions

**English**: design experiment, experimental design, power analysis, sample size calculation, randomization, create survey, build instrument, write protocol, plan experiment, RCT design, factorial design, quasi-experimental design, crossover design

**Traditional Chinese**: 實驗設計, 樣本數計算, 檢定力分析, 隨機分派, 設計問卷, 建立量表, 撰寫計畫書, 規劃實驗

**Guided mode triggers**: "help me design an experiment", "I'm not sure what design to use", "what sample size do I need", "guide my experiment design"

**Does NOT trigger**:

| Scenario | Use Instead |
|----------|-------------|
| Have data, want to run analysis | `data-analyst` |
| Need to run a simulation | `simulation-runner` |
| Need to write up results as a paper | `academic-paper` |
| Need research/literature review | `deep-research` |

### 2.3 Agent Team (6 agents)

| # | Agent | Role | Phase |
|---|-------|------|-------|
| 1 | `intake_agent` | Parses user request, determines mode, validates that RQ/methodology blueprint exists (from `deep-research` or user-supplied) | Phase 0 |
| 2 | `design_architect_agent` | Core designer -- selects experimental design (RCT, quasi-experimental, factorial, crossover, etc.), defines IV/DV/controls, identifies threats to validity | Phase 1 |
| 3 | `power_analyst_agent` | Executes power analysis via Python (statsmodels, scipy) -- computes required sample size, detects minimum effect size, generates power curves | Phase 1 |
| 4 | `instrument_builder_agent` | Builds measurement instruments -- survey items, rubrics, coding schemes, observation protocols. Assesses content validity, suggests pilot testing | Phase 2 |
| 5 | `randomization_agent` | Designs allocation scheme -- simple random, stratified, block, cluster. Generates actual randomization sequences via Python (numpy) | Phase 2 |
| 6 | `protocol_compiler_agent` | Assembles the complete experiment protocol document, cross-validates all components for coherence, produces the Experiment Design handoff artifact (Schema 10) and, when design_type is `simulation`, also produces the Simulation Specification (Schema 13) | Phase 3 |

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
- **Downstream**: Produces Experiment Design (Schema 10) consumed by `data-analyst`, `simulation-runner`, `lab-notebook`. When `design_type` is `simulation`, also produces Simulation Specification (Schema 13) consumed by `simulation-runner`
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

### 3.2b Trigger Conditions

**English**: analyze data, run statistics, statistical analysis, t-test, ANOVA, regression, correlation, chi-square, descriptive statistics, check assumptions, explore data, EDA, replicate analysis, analyze my data, run the analysis, effect size, missing data

**Traditional Chinese**: 分析資料, 統計分析, 跑統計, 描述統計, 檢驗假設, 探索資料, 複製分析, 效果量, 缺失值處理

**Guided mode triggers**: "I have data but don't know what test to run", "help me choose the right analysis", "what statistics should I use"

**Does NOT trigger**:

| Scenario | Use Instead |
|----------|-------------|
| Need to design an experiment (no data yet) | `experiment-designer` |
| Need Monte Carlo, bootstrap, simulation | `simulation-runner` |
| Need to write up results as a paper | `academic-paper` |
| Need literature/research review | `deep-research` |

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

### 4.2b Trigger Conditions

**English**: Monte Carlo, simulation, bootstrap, parameter sweep, sensitivity analysis, agent-based model, power simulation, simulate, computational experiment, stochastic, resampling, permutation test

**Traditional Chinese**: 蒙地卡羅, 模擬, 拔靴法, 參數掃描, 敏感度分析, 代理人模型, 檢定力模擬, 計算實驗, 隨機過程, 重抽樣

**Guided mode triggers**: "I want to simulate but don't know how to set up the model", "help me design a Monte Carlo study"

**Does NOT trigger**:

| Scenario | Use Instead |
|----------|-------------|
| Have real data to analyze | `data-analyst` |
| Need to design an experiment (protocol, instruments) | `experiment-designer` |
| Need literature/research review | `deep-research` |

**Ad-hoc request minimum fields** (when no Schema 10/13 available):
- Simulation type (Monte Carlo, bootstrap, etc.)
- Model description or data file (for bootstrap)
- Number of iterations (or accept default: 10,000)
- What to measure / report

### 4.3 Agent Team (5 agents)

| # | Agent | Role | Phase |
|---|-------|------|-------|
| 1 | `intake_agent` | Parses request, determines simulation type, validates inputs (existing data for bootstrap, model spec for Monte Carlo, or Experiment Design Schema 10/13 for pre-planned simulations) | Phase 0 |
| 2 | `model_builder_agent` | Translates the conceptual model into executable Python code -- defines data-generating process (DGP), parameters, distributions, stopping rules. For agent-based models: defines agents, rules, environment, interaction topology | Phase 1 |
| 3 | `execution_engine_agent` | Runs the simulation -- manages iterations, seeds for reproducibility, parallel execution where possible. Monitors convergence (Monte Carlo error, Gelman-Rubin R-hat). Implements early stopping if convergence criteria met | Phase 2 |
| 4 | `diagnostics_agent` | Assesses simulation quality -- convergence diagnostics, trace plots, autocorrelation, effective sample size. For parameter sweeps: generates heatmaps, tornado plots, spider plots. Flags non-convergence or instability | Phase 3 |
| 5 | `report_compiler_agent` | Assembles simulation report -- model specification, parameter tables, results summary, diagnostic plots, reproducibility seed log. Produces Schema 11 handoff artifact (consumes Schema 13 from experiment-designer for model provenance) | Phase 4 |

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

### 5.2b Trigger Conditions

**English**: lab notebook, log experiment, record deviation, experiment log, track experiment, research record, audit notebook, export notebook, experiment snapshot

**Traditional Chinese**: 實驗紀錄, 記錄偏差, 實驗日誌, 追蹤實驗, 研究紀錄, 審計紀錄, 匯出紀錄

**Does NOT trigger as entry point**: `lab-notebook` is never the *entry point* to the experiment pipeline (i.e., don't start with lab-notebook when no experiment context exists). However, it can be invoked standalone for `log-entry`, `deviation`, `snapshot`, `export`, or `audit` modes on an existing notebook.

| Scenario | Use Instead |
|----------|-------------|
| Need to design an experiment | `experiment-designer` |
| Need to run statistical analysis | `data-analyst` |
| Need to run simulations | `simulation-runner` |

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
- `entry_template.md` -- Per-type entry templates (collection, deviation, decision, etc.)
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
Stage 2.5: INTEGRITY (existing, extended)
  -> New Phase F: Experiment Reproducibility Verification
     1. Locate reproducibility script from Schema 11 `reproducibility.script_path`
     2. Re-execute the script in the experiment venv
     3. Diff output tables/stats against reported Schema 11 results
     4. Verify figure file hashes match (regenerated vs reported)
     5. If any mismatch: SERIOUS issue, blocks pipeline
Stage 3-9: (existing stages unchanged)
```

### 6.2 Schema 1 Extension: Methodology Type

The existing Schema 1 (RQ Brief) has a `methodology_type` field with enum values `"qualitative"` / `"quantitative"` / `"mixed"`. This is too coarse for the detection logic. **Required change to Schema 1**: add a new field `methodology_subtype` to carry the specific design:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `methodology_subtype` | enum | No (new) | `"experimental"` / `"quasi_experimental"` / `"correlational"` / `"simulation"` / `"secondary_data_analysis"` / `"survey"` / `"case_study"` / `"content_analysis"` / `"literature_review"` / `"theoretical"` / `"mixed_methods"` |

This field is populated by `deep-research/research_architect_agent` when it produces the Methodology Blueprint. The existing `methodology_type` field (`qualitative`/`quantitative`/`mixed`) remains unchanged for backward compatibility.

### 6.3 Methodology Blueprint Formalization

The Methodology Blueprint is an informal artifact produced by `deep-research/research_architect_agent`. For the pipeline detection logic to work reliably, the following fields MUST be present in any Methodology Blueprint:

| Field | Type | Description |
|-------|------|-------------|
| `research_paradigm` | string | Positivist / Interpretivist / Pragmatist / Critical |
| `method_type` | string | qualitative / quantitative / mixed |
| `specific_method` | string | E.g., "quasi-experimental", "comparative case study" |
| `data_type` | string | primary / secondary / both |
| `requires_experiment_design` | boolean | Whether an experiment protocol is needed |
| `requires_data_collection` | boolean | Whether primary data collection is needed |
| `requires_simulation` | boolean | Whether computational simulation is needed |

These fields enable the pipeline orchestrator to make routing decisions without parsing free text.

### 6.4 Detection Logic

```
Trigger experimentation stages based on Methodology Blueprint fields:
- requires_experiment_design = true  -> experiment-designer (full) + data-analyst
- requires_simulation = true         -> experiment-designer (guided) + simulation-runner
- methodology_subtype = "correlational" AND requires_data_collection = true
                                     -> data-analyst only (no design needed)
- methodology_subtype = "secondary_data_analysis"
                                     -> data-analyst only
- method_type = "mixed" AND requires_data_collection = true
                                     -> experiment-designer + data-analyst
- All others                         -> skip experimentation
```

### 6.5 Updated CLAUDE.md Routing Rules

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

8. lab-notebook: Never the *entry point* to the experiment pipeline. Always
   accompanies other experiment skills. Automatically invoked by pipeline when
   experiment stages are active. Can be invoked standalone for log-entry,
   deviation, snapshot, export, or audit modes on an existing notebook.
```

---

## 7. New Handoff Schemas

### Schema 10: Experiment Design

**Producer**: `experiment-designer/protocol_compiler_agent`
**Consumer**: `data-analyst/intake_agent` | `simulation-runner/intake_agent` | `lab-notebook/entry_writer_agent`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `experiment_id` | string | Yes | Unique experiment identifier |
| `design_type` | enum | Yes | `RCT` / `quasi_experimental` / `factorial` / `crossover` / `single_subject` / `correlational` / `simulation` / `mixed` |
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
| `deep-research` | v2.3 -> v2.4 | Universal research team (+ methodology_subtype in RQ Brief) | full, quick, socratic, review, lit-review, fact-check, systematic-review |
| `experiment-designer` | v1.0 (NEW) | Experiment protocol and power analysis | full, guided, quick, power-only, instrument |
| `data-analyst` | v1.0 (NEW) | Statistical analysis execution | full, guided, quick, assumption-check, exploratory, replication |
| `simulation-runner` | v1.0 (NEW) | Computational experiments | full, guided, quick, power-sim, sensitivity, bootstrap |
| `lab-notebook` | v1.0 (NEW) | Experiment research record | full, log-entry, deviation, snapshot, export, audit |
| `academic-paper` | v2.4 -> v2.5 | Academic paper writing (+ Schema 11/12 consumption) | full, plan, outline-only, revision, abstract-only, lit-review, format-convert, citation-check |
| `academic-paper-reviewer` | v1.4 (unchanged) | Multi-perspective paper review | full, re-review, quick, methodology-focus, guided |
| `academic-pipeline` | v2.6 -> v2.7 | Full pipeline orchestrator (+ experiment stages) | (coordinates all above) |

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
  examples/
    rct_design_example.md
    quasi_experimental_example.md

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
  examples/
    anova_analysis_example.md
    regression_analysis_example.md

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
  examples/
    monte_carlo_power_example.md
    bootstrap_ci_example.md

lab-notebook/
  SKILL.md
  agents/
    notebook_manager_agent.md
    entry_writer_agent.md
    deviation_tracker_agent.md
    provenance_auditor_agent.md
  templates/
    notebook_template.md
    entry_template.md
    audit_checklist_template.md
    file_manifest_template.md
  references/
    lab_notebook_best_practices.md
    reproducibility_standards.md
    deviation_handling_guide.md
    provenance_tracking_guide.md
  examples/
    full_notebook_example.md

shared/
  experiment_infrastructure.md  (NEW)
  handoff_schemas.md            (UPDATED -- add schemas 10-13)
```

**Total new files: 71**
- experiment-designer: 1 SKILL + 6 agents + 4 templates + 5 references + 2 examples = 18
- data-analyst: 1 SKILL + 7 agents + 4 templates + 6 references + 2 examples = 20
- simulation-runner: 1 SKILL + 5 agents + 4 templates + 5 references + 2 examples = 17
- lab-notebook: 1 SKILL + 4 agents + 4 templates + 4 references + 1 example = 14
- shared: 1 new file (experiment_infrastructure.md) + 1 updated file (handoff_schemas.md) = 1 new + 1 updated

**Modified files: 7**
- `shared/handoff_schemas.md` -- Add schemas 10-13
- `.claude/CLAUDE.md` -- Add routing rules 6-8, update skills overview table
- `academic-pipeline/SKILL.md` -- Add Stage 1.5 (EXPERIMENT), bump to v2.7
- `academic-pipeline/agents/pipeline_orchestrator_agent.md` -- Add experiment stage detection logic
- `academic-pipeline/agents/integrity_verification_agent.md` -- Add Phase F: Experiment Reproducibility Verification
- `academic-paper/SKILL.md` -- Document Schema 11/12 consumption, bump to v2.5
- `deep-research/SKILL.md` -- Add `methodology_subtype` field to RQ Brief output, bump to v2.4
