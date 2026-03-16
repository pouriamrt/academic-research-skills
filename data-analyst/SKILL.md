---
name: data-analyst
description: "Statistical analysis execution engine. 7-agent pipeline for rigorous data analysis, assumption testing, and publication-ready results. 6 modes: full analysis, guided interactive, quick summary, assumption-check, exploratory EDA, and replication. Covers data profiling, cleaning, missing data handling, assumption testing, parametric and non-parametric tests, regression, ANOVA, SEM, HLM, mediation, survival analysis, Bayesian methods, effect size computation, publication-quality visualization, and APA 7 report compilation. Triggers on: analyze data, run statistics, statistical analysis, t-test, ANOVA, regression, correlation, chi-square, descriptive statistics, check assumptions, explore data, EDA, replicate analysis, analyze my data, run the analysis, effect size, missing data, 分析資料, 統計分析, 跑統計, 描述統計, 檢驗假設, 探索資料, 複製分析, 效果量, 缺失值處理."
metadata:
  version: "1.0"
  last_updated: "2026-03-16"
---

# Data Analyst — Statistical Analysis Execution Engine

Execution engine for statistical analysis — a domain-agnostic 7-agent team that takes data, runs rigorous analyses in Python, and produces publication-ready results with APA-formatted text, tables, and figures. v1.0 covers the full spectrum from descriptive statistics through advanced methods (SEM, HLM, survival, Bayesian).

## Quick Start

**Minimal command:**
```
Analyze the data in survey_results.csv — compare group scores using ANOVA
```

**Guided mode:**
```
Help me analyze my data — I have exam scores across three teaching methods
幫我分析資料，我有三種教學法的考試成績
```

**Execution:**
1. Intake — Parse request, locate data, profile dataset
2. Preparation — Clean data, handle missing values, transform variables
3. Assumptions — Test all relevant statistical assumptions
4. Analysis — Execute primary and secondary analyses
5. Effect Sizes — Compute and interpret effect sizes with CIs
6. Visualization — Generate publication-quality figures
7. Reporting — Compile APA results text, tables, figures, Schema 11

---

## Trigger Conditions

### Trigger Keywords

**English**: analyze data, run statistics, statistical analysis, t-test, ANOVA, regression, correlation, chi-square, descriptive statistics, check assumptions, explore data, EDA, replicate analysis, analyze my data, run the analysis, effect size, missing data, run ANCOVA, factor analysis, SEM, HLM, mediation analysis, survival analysis, Bayesian analysis

**Traditional Chinese**: 分析資料, 統計分析, 跑統計, 描述統計, 檢驗假設, 探索資料, 複製分析, 效果量, 缺失值處理

### Guided Mode Activation

Activate `guided` mode when the user's **intent** matches any of the following patterns, **regardless of language**:

**Intent signals** (any one is sufficient):
1. User has data but is unsure which analysis to run
2. User asks for help choosing a statistical test
3. User expresses uncertainty about how to handle their data
4. User wants step-by-step guidance through the analysis process
5. User describes a research question without specifying a test

**Default rule**: When intent is ambiguous between `guided` and `full`, **prefer `guided`** — it is safer to help the user choose the right analysis than to run the wrong one.

### Does NOT Trigger

| Scenario | Use Instead |
|----------|-------------|
| Designing an experiment (not analyzing data) | `experiment-designer` |
| Writing a paper (not running statistics) | `academic-paper` |
| Running a simulation (not analyzing real data) | `simulation-runner` |
| Full pipeline (research to paper) | `academic-pipeline` |

### Quick Mode Selection Guide

| Your Situation | Recommended Mode |
|----------------|-----------------|
| Have data + clear analysis plan / 有資料和明確分析計畫 | `full` |
| Have data, unsure which test / 有資料但不確定要用什麼統計 | `guided` |
| Need quick descriptive summary / 快速描述統計摘要 | `quick` |
| Only need assumption checks / 只需要檢驗假設 | `assumption-check` |
| Want to explore data first / 想先探索資料 | `exploratory` |
| Replicating a published analysis / 複製已發表的分析 | `replication` |

Not sure? Start with `guided` — it will help you figure out which analysis you need.
不確定？先用 `guided` 模式——它會幫你選擇合適的統計分析。

---

## Agent Team (7 Agents)

| # | Agent | Role | Phase |
|---|-------|------|-------|
| 1 | `intake_agent` | Parse request, locate data files, detect format, load and profile dataset, detect mode | Phase 1 |
| 2 | `data_preparation_agent` | Clean data — missing values, outliers, recoding, transformations; save cleaned dataset | Phase 2 |
| 3 | `assumption_checker_agent` | Test statistical assumptions — normality, homogeneity, sphericity, linearity, VIF, homoscedasticity | Phase 3 |
| 4 | `analysis_executor_agent` | Execute primary analyses — t-tests, ANOVA, regression, SEM, HLM, chi-square, survival, Bayesian | Phase 4 |
| 5 | `effect_size_agent` | Compute effect sizes with 95% CIs, classify magnitude, interpret practical significance | Phase 5 |
| 6 | `visualization_agent` | Generate publication-quality figures following shared infrastructure standards | Phase 6 |
| 7 | `report_compiler_agent` | Assemble analysis report, generate APA text blocks, produce Schema 11 handoff artifact | Phase 7 |

---

## Statistical Methods Coverage

| Category | Methods | Python Source |
|----------|---------|--------------|
| Descriptive | Mean, SD, median, IQR, skewness, kurtosis, frequency tables | `pandas`, `scipy.stats` |
| Comparison (2-group) | Independent t-test, paired t-test, Mann-Whitney U, Wilcoxon signed-rank | `scipy.stats`, `pingouin` |
| Comparison (3+ groups) | One-way ANOVA, factorial ANOVA, repeated-measures ANOVA, ANCOVA, Kruskal-Wallis, Friedman | `statsmodels`, `pingouin` |
| Post-hoc | Tukey HSD, Bonferroni, Games-Howell, Dunn's test | `statsmodels`, `pingouin`, `scikit-posthocs` |
| Correlation | Pearson r, Spearman rho, Kendall tau, partial correlation, point-biserial | `scipy.stats`, `pingouin` |
| Regression | Simple linear, multiple linear, logistic, ordinal, hierarchical | `statsmodels`, `scikit-learn` |
| Factor analysis | EFA (principal axis, ML), CFA, reliability (Cronbach's alpha, McDonald's omega) | `factor_analyzer`, `semopy`, `pingouin` |
| Non-parametric | Mann-Whitney, Wilcoxon, Kruskal-Wallis, Friedman, chi-square, Fisher's exact | `scipy.stats`, `pingouin` |
| Advanced | HLM/multilevel (MixedLM), SEM/path analysis (semopy), mediation (bootstrap), moderation | `statsmodels`, `semopy` |
| Survival | Kaplan-Meier, Cox proportional hazards, log-rank test | `lifelines` |
| Bayesian | Bayesian t-test, Bayesian correlation, Bayes factor | `pingouin` |

---

## Venv Setup

Follows `shared/experiment_infrastructure.md` Section 1. On first run:

1. Create or reuse `./experiment_env/`
2. Install core packages (numpy, scipy, pandas, statsmodels, matplotlib, seaborn, pingouin, scikit-learn)
3. Install skill-specific extras: `semopy`, `lifelines`, `openpyxl`, `pyreadstat`

---

## Mode Selection Guide

```
User Input
    |
    +-- Have data file + clear analysis plan?
    |   +-- Yes --> Need full analysis report?
    |   |           +-- Yes --> full mode
    |   |           +-- No --> Only need assumptions?
    |   |                      +-- Yes --> assumption-check mode
    |   |                      +-- No --> quick mode
    |   +-- No --> Have data but unsure what test?
    |              +-- Yes --> guided mode
    |              +-- No --> Want to explore data first?
    |                         +-- Yes --> exploratory mode
    |                         +-- No --> Replicating published analysis?
    |                                    +-- Yes --> replication mode
    |                                    +-- No --> guided mode
```

---

## Orchestration Workflow (7 Phases)

```
User: "Analyze [data] with [method]"
     |
=== Phase 1: INTAKE ===
     |
     |-> [intake_agent] -> Dataset Profile + Analysis Plan
     |   - Locate and load data file (CSV, Excel, SPSS, Stata)
     |   - Profile: shape, dtypes, missingness, distributions
     |   - If Schema 10 available: extract analysis plan
     |   - If no plan: determine tests from user request
     |   - Detect mode (full/guided/quick/assumption-check/exploratory/replication)
     |
     ** In guided mode: interactive dialogue to determine analyses **
     |
=== Phase 2: DATA PREPARATION ===
     |
     |-> [data_preparation_agent] -> Cleaned Dataset + Cleaning Log
     |   - Diagnose missing data mechanism (MCAR/MAR/MNAR)
     |   - Apply appropriate strategy (listwise/MI/FIML)
     |   - Detect and handle outliers (IQR/Z-score/Mahalanobis)
     |   - Recode variables, apply transformations
     |   - Save cleaned data to experiment_outputs/tables/
     |   - Save cleaning log to experiment_outputs/logs/
     |
=== Phase 3: ASSUMPTION CHECKING ===
     |
     |-> [assumption_checker_agent] -> Assumption Report + Diagnostic Plots
     |   - Test all assumptions relevant to planned analyses
     |   - Normality: Shapiro-Wilk, Q-Q plots
     |   - Homogeneity: Levene's test
     |   - Sphericity: Mauchly's test (repeated measures)
     |   - Linearity: residual plots
     |   - Multicollinearity: VIF
     |   - Homoscedasticity: Breusch-Pagan
     |   - Generate diagnostic plots
     |   - Recommend parametric vs non-parametric
     |
     ** If ALL assumptions violated -> CHECKPOINT: present alternatives **
     |
=== Phase 4: ANALYSIS EXECUTION ===
     |
     |-> [analysis_executor_agent] -> Raw Results + Reproducibility Script
     |   - Execute all planned analyses (primary, secondary, exploratory)
     |   - Generate reproducibility script at experiment_outputs/scripts/analysis.py
     |   - Store raw results for downstream agents
     |
=== Phase 5: EFFECT SIZE COMPUTATION ===
     |
     |-> [effect_size_agent] -> Effect Sizes + Interpretation
     |   - Compute appropriate effect size for each analysis
     |   - 95% confidence intervals (analytical or bootstrap)
     |   - Classify magnitude per Cohen's conventions
     |   - Practical significance interpretation
     |
=== Phase 6: VISUALIZATION ===
     |
     |-> [visualization_agent] -> Publication-Quality Figures
     |   - Generate figures following shared/experiment_infrastructure.md standards
     |   - 300 DPI, colorblind-safe palette, Times New Roman
     |   - Save as PNG + PDF to experiment_outputs/figures/
     |   - Number figures sequentially
     |
=== Phase 7: REPORT COMPILATION ===
     |
     |-> [report_compiler_agent] -> Analysis Report + Schema 11
         - Assemble full analysis report
         - Generate APA results text blocks (ready for paper insertion)
         - Number tables and figures
         - Produce Schema 11 handoff artifact
         - If notebook_path provided: append auto-logging entry
```

### Checkpoint Rules

1. **Assumption violations**: If all assumptions fail for the chosen test, present non-parametric alternatives and require user confirmation before proceeding
2. **Missing data**: If missingness > 20%, warn user and present options (MI recommended)
3. **Convergence**: If SEM/HLM fails to converge, report diagnostics and suggest model simplification
4. Revision loops for guided mode capped at **3 interactions** per decision point

---

## Operational Modes

| Mode | Agents Active | Output | Description |
|------|---------------|--------|-------------|
| `full` (default) | All 7 | Full analysis report + Schema 11 | Complete analysis pipeline |
| `guided` | Intake (interactive) + all 7 | Full analysis report + Schema 11 | Interactive test selection then full pipeline |
| `quick` | Intake + Preparation + Analysis + Report | Descriptive stats + key results | Fast summary without full assumption/effect size detail |
| `assumption-check` | Intake + Preparation + Assumption Checker | Assumption report + diagnostic plots | Assumption testing only |
| `exploratory` | Intake + Preparation + Visualization + partial Analysis | EDA report with distributions and correlations | Data exploration, no confirmatory tests |
| `replication` | All 7 (strict protocol) | Replication report with original comparison | Reproduce published analysis, compare results |

---

## Failure Paths

Inherits shared failure paths from `shared/experiment_infrastructure.md` Section 7. Skill-specific additions:

| Failure Code | Trigger | Severity | Recovery |
|-------------|---------|----------|----------|
| `ALL_ASSUMPTIONS_VIOLATED` | Every assumption fails for chosen test | MAJOR | Report violations. Recommend non-parametric alternative. Present options. Do NOT proceed with parametric test without user confirmation. |
| `CONVERGENCE_FAILURE` | SEM/HLM model fails to converge | MAJOR | Report fit indices and convergence diagnostics. Suggest: simplify model, check starting values, increase iterations. |
| `MULTICOLLINEARITY_SEVERE` | VIF > 10 for one or more predictors | MAJOR | Report VIF table. Suggest: remove predictor, combine variables, use PCA/ridge regression. Require user decision. |
| `INSUFFICIENT_SAMPLE` | N < minimum for planned analysis (e.g., SEM requires N > 200) | MAJOR | Report minimum sample requirements. Suggest: simpler analysis, combine groups, bootstrapping. |
| `MISSING_DATA_EXTREME` | Missingness > 50% on key variables | BLOCKING | Report missingness pattern. Recommend against imputation at this level. Suggest collecting more data or dropping variable. |
| `REPLICATION_DIVERGENCE` | Replication results significantly differ from original | WARNING | Report comparison table. Discuss possible explanations (different software, rounding, data cleaning). |
| `NO_ANALYSIS_PLAN` | No Schema 10 and user provides no clear analysis request | BLOCKING | Switch to guided mode. Walk user through test selection using decision tree. |

---

## Integration

### Upstream: Schema 10 (experiment-designer -> data-analyst)

When a Schema 10 artifact is available from `experiment-designer`, the `intake_agent` extracts:
- `analysis_plan.primary` / `secondary` / `exploratory` -> planned analyses
- `variables` -> variable definitions and types
- `hypotheses` -> directional hypotheses for testing
- `sample.alpha` -> significance threshold

### Downstream: Schema 11 (data-analyst -> academic-paper / lab-notebook)

The `report_compiler_agent` produces a Schema 11 artifact containing:
- `assumption_checks` -> per-assumption test results
- `primary_results` / `secondary_results` -> all analysis results with APA strings
- `effect_sizes` -> all effect sizes with CIs
- `tables` / `figures` -> file paths to all generated artifacts
- `apa_results_text` -> ready-to-insert APA text blocks
- `reproducibility` -> script path, seed, environment info

### User Data (no upstream schema)

When users provide data directly (no Schema 10), the `intake_agent`:
1. Locates the data file from user's description
2. Profiles the dataset
3. Determines appropriate analyses from user's request or via guided dialogue
4. Constructs an internal analysis plan equivalent to Schema 10's `analysis_plan`

---

## Agent File References

| Agent | Definition File |
|-------|----------------|
| intake_agent | `agents/intake_agent.md` |
| data_preparation_agent | `agents/data_preparation_agent.md` |
| assumption_checker_agent | `agents/assumption_checker_agent.md` |
| analysis_executor_agent | `agents/analysis_executor_agent.md` |
| effect_size_agent | `agents/effect_size_agent.md` |
| visualization_agent | `agents/visualization_agent.md` |
| report_compiler_agent | `agents/report_compiler_agent.md` |

---

## Reference Files

| Reference | Purpose | Used By |
|-----------|---------|---------|
| `references/statistical_test_decision_tree.md` | Master decision tree for test selection | intake_agent (guided mode), analysis_executor |
| `references/assumption_testing_guide.md` | Per-assumption testing with Python code | assumption_checker |
| `references/apa_stats_formatting_guide.md` | APA 7 formatting rules for every test type | report_compiler, analysis_executor |
| `references/effect_size_interpretation_guide.md` | Cohen's benchmarks, domain-specific norms, CI computation | effect_size |
| `references/missing_data_strategies.md` | MCAR/MAR/MNAR diagnosis, MI code, decision tree | data_preparation |
| `references/common_analysis_pitfalls.md` | Multiple comparisons, p-hacking, overfitting, and more | all agents |

---

## Templates

| Template | Purpose |
|----------|---------|
| `templates/analysis_report_template.md` | Full analysis report structure (maps to Schema 11) |
| `templates/apa_results_template.md` | Per-test APA text patterns with fill-in values |
| `templates/assumption_report_template.md` | Per-assumption report with verdicts and actions |
| `templates/data_cleaning_log_template.md` | Cleaning log with steps, justifications, exclusion flowchart |

---

## Examples

| Example | Demonstrates |
|---------|-------------|
| `examples/anova_analysis_example.md` | Complete one-way ANOVA walkthrough (3 groups, N=90) |
| `examples/regression_analysis_example.md` | Complete multiple regression walkthrough (3 predictors, N=200) |

---

## Output Language

Follows the user's language. Statistical notation and APA formatting remain in English regardless of language. Variable names preserved as-is from the dataset.

---

## Quality Standards

1. **Every result must include an effect size** — statistical significance alone is insufficient
2. **Assumptions tested before every parametric test** — no shortcuts
3. **Exact p-values reported** — never "p < .05" alone; report exact values (except p < .001)
4. **Reproducibility** — every analysis generates a self-contained Python script
5. **Missing data transparency** — mechanism diagnosed, strategy justified, exclusions documented
6. **Multiple comparison correction** — applied and documented when testing multiple hypotheses
7. **AI disclosure** — all reports include a statement that AI-assisted analysis tools were used

## Cross-Agent Quality Alignment

| Concept | Definition | Applies To |
|---------|-----------|------------|
| **Statistical significance** | p < alpha (default alpha = .05 unless Schema 10 specifies otherwise). Always report exact p-value. | analysis_executor, report_compiler |
| **Practical significance** | Effect size magnitude classified per Cohen's conventions, supplemented by domain-specific benchmarks when available | effect_size, report_compiler |
| **Assumption violation** | A statistical assumption test yields p < .05 (for tests where H0 = assumption met) or diagnostic plot shows clear pattern | assumption_checker |
| **Marginal violation** | .01 < p < .05 on assumption test, or borderline diagnostic plot. Report but may proceed with caution | assumption_checker |
| **Publication-quality figure** | 300 DPI, colorblind-safe palette, serif font, clear labels, no chartjunk, APA-formatted caption | visualization |
| **Reproducibility** | Complete Python script that, when executed in the same venv with the same data, produces identical results | analysis_executor, report_compiler |

> **Cross-Skill Reference**: See `shared/handoff_schemas.md` for Schema 10 (input) and Schema 11 (output) data contracts. See `shared/experiment_infrastructure.md` for venv, formatting, and output directory standards.

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-03-16 | Initial release: 7 agents, 6 modes, 7-phase pipeline. Covers descriptive through advanced methods (SEM, HLM, survival, Bayesian). Full APA 7 formatting. Schema 10 input / Schema 11 output integration. |
