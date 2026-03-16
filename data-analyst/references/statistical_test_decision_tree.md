# Statistical Test Decision Tree — Master Reference

## Purpose

Master decision tree for selecting the appropriate statistical test based on research question type, data type, number of groups, and study design. Used primarily by `intake_agent` (guided mode) and `analysis_executor_agent` to determine which test to run.

---

## Decision Tree

```
What is your research question?
    |
    +-- COMPARING groups on a continuous outcome?
    |   |
    |   +-- How many groups?
    |   |   |
    |   |   +-- 2 groups
    |   |   |   |
    |   |   |   +-- Independent (between-subjects)?
    |   |   |   |   +-- Assumptions met? --> Independent t-test
    |   |   |   |   +-- Assumptions violated? --> Mann-Whitney U
    |   |   |   |   +-- Unequal variances only? --> Welch's t-test
    |   |   |   |
    |   |   |   +-- Dependent (within-subjects / paired)?
    |   |   |       +-- Assumptions met? --> Paired t-test
    |   |   |       +-- Assumptions violated? --> Wilcoxon signed-rank
    |   |   |
    |   |   +-- 3+ groups
    |   |       |
    |   |       +-- Independent (between-subjects)?
    |   |       |   |
    |   |       |   +-- 1 factor?
    |   |       |   |   +-- Assumptions met? --> One-way ANOVA
    |   |       |   |   +-- Assumptions violated? --> Kruskal-Wallis
    |   |       |   |   +-- Unequal variances only? --> Welch's ANOVA
    |   |       |   |
    |   |       |   +-- 2+ factors?
    |   |       |       +-- Assumptions met? --> Factorial ANOVA
    |   |       |       +-- Need covariates? --> ANCOVA
    |   |       |
    |   |       +-- Dependent (within-subjects / repeated)?
    |   |       |   +-- Assumptions met? --> Repeated-measures ANOVA
    |   |       |   +-- Sphericity violated? --> RM ANOVA + Greenhouse-Geisser
    |   |       |   +-- Assumptions violated? --> Friedman test
    |   |       |
    |   |       +-- Mixed (between + within)?
    |   |           +-- Mixed ANOVA
    |   |           +-- Need covariates? --> Mixed ANCOVA
    |   |
    |   +-- Need to control for covariates?
    |       +-- ANCOVA (continuous covariates)
    |       +-- Stratified analysis (categorical covariates)
    |
    +-- EXAMINING a relationship between variables?
    |   |
    |   +-- Both continuous?
    |   |   +-- Linear relationship?
    |   |   |   +-- Assumptions met? --> Pearson r
    |   |   |   +-- Assumptions violated? --> Spearman rho
    |   |   +-- Non-linear? --> Spearman rho or polynomial regression
    |   |
    |   +-- One continuous, one ordinal?
    |   |   +-- Spearman rho
    |   |
    |   +-- One continuous, one binary?
    |   |   +-- Point-biserial correlation
    |   |
    |   +-- Both ordinal?
    |   |   +-- Kendall's tau
    |   |
    |   +-- Partial relationship (controlling for third variable)?
    |       +-- Partial correlation
    |
    +-- PREDICTING an outcome from predictors?
    |   |
    |   +-- Continuous outcome?
    |   |   |
    |   |   +-- 1 predictor? --> Simple linear regression
    |   |   +-- 2+ predictors? --> Multiple linear regression
    |   |   +-- Hierarchical entry? --> Hierarchical regression
    |   |   +-- Nested data (students in classes)? --> HLM / Mixed-effects model
    |   |   +-- Complex paths / latent variables? --> SEM (semopy)
    |   |
    |   +-- Binary outcome (yes/no)?
    |   |   +-- Binary logistic regression
    |   |   +-- Nested data? --> Multilevel logistic regression
    |   |
    |   +-- Ordinal outcome (ordered categories)?
    |   |   +-- Ordinal logistic regression
    |   |
    |   +-- Count outcome (0, 1, 2, ...)?
    |   |   +-- Poisson regression
    |   |   +-- Overdispersed? --> Negative binomial regression
    |   |
    |   +-- Time-to-event outcome?
    |       +-- Kaplan-Meier + log-rank (group comparison)
    |       +-- Cox proportional hazards (with predictors)
    |
    +-- TESTING association between categorical variables?
    |   |
    |   +-- 2x2 table?
    |   |   +-- Expected frequencies >= 5? --> Chi-square
    |   |   +-- Expected frequencies < 5? --> Fisher's exact test
    |   |
    |   +-- Larger table (r x c)?
    |   |   +-- Expected frequencies adequate? --> Chi-square
    |   |   +-- Many low expected? --> Collapse categories or exact test
    |   |
    |   +-- Paired/matched data?
    |       +-- McNemar's test
    |
    +-- TESTING mediation or moderation?
    |   |
    |   +-- Mediation (X -> M -> Y)?
    |   |   +-- Bootstrap mediation analysis (5000 resamples)
    |   |   +-- Complex model? --> SEM with indirect effects
    |   |
    |   +-- Moderation (X * Z -> Y)?
    |       +-- Include interaction term in regression
    |       +-- Probe significant interactions with simple slopes
    |
    +-- EXPLORING data structure?
    |   |
    |   +-- Reduce variables to factors?
    |   |   +-- Exploratory? --> EFA (principal axis factoring)
    |   |   +-- Confirmatory? --> CFA (semopy)
    |   |
    |   +-- Cluster observations?
    |       +-- K-means / hierarchical clustering
    |
    +-- TESTING scale reliability?
        +-- Internal consistency? --> Cronbach's alpha, McDonald's omega
        +-- Test-retest? --> ICC or Pearson r
```

---

## Quick Reference Table

| Research Question | DV Type | IV Type | Groups | Design | Test | Non-Parametric Alt |
|-------------------|---------|---------|--------|--------|------|-------------------|
| Group difference | Continuous | Categorical | 2 | Between | Independent t-test | Mann-Whitney U |
| Group difference | Continuous | Categorical | 2 | Within | Paired t-test | Wilcoxon |
| Group difference | Continuous | Categorical | 3+ | Between | One-way ANOVA | Kruskal-Wallis |
| Group difference | Continuous | Categorical | 3+ | Within | RM ANOVA | Friedman |
| Group difference | Continuous | 2+ Categorical | — | Between | Factorial ANOVA | — |
| Group diff + covariate | Continuous | Categorical | 2+ | Between | ANCOVA | Quade's test |
| Relationship | Continuous | Continuous | — | — | Pearson r | Spearman rho |
| Prediction | Continuous | Mixed | — | — | Multiple regression | — |
| Prediction | Binary | Mixed | — | — | Logistic regression | — |
| Association | Categorical | Categorical | — | — | Chi-square | Fisher's exact |
| Mediation | Continuous | Continuous | — | — | Bootstrap mediation | — |
| Factor structure | Continuous | — | — | — | EFA / CFA | — |
| Nested data | Continuous | Mixed | — | Hierarchical | HLM (MixedLM) | — |
| Time-to-event | Duration | Mixed | — | — | Cox PH / KM | — |

---

## Per-Test Reference Cards

### Independent t-Test

| Property | Detail |
|----------|--------|
| **When** | Compare means of 2 independent groups |
| **Assumptions** | Normality per group, homogeneity of variance, independence |
| **Python** | `pingouin.ttest(x, y, paired=False)` |
| **Effect size** | Cohen's d (Hedges' g if N < 20) |
| **Non-parametric alt** | Mann-Whitney U |
| **APA format** | *t*(df) = X.XX, *p* = .XXX, *d* = X.XX |
| **Post-hoc** | N/A (only 2 groups) |

### One-Way ANOVA

| Property | Detail |
|----------|--------|
| **When** | Compare means of 3+ independent groups |
| **Assumptions** | Normality per group, homogeneity of variance, independence |
| **Python** | `pingouin.anova(data, dv, between)` |
| **Effect size** | Eta-squared, omega-squared |
| **Non-parametric alt** | Kruskal-Wallis |
| **APA format** | *F*(df1, df2) = X.XX, *p* = .XXX, eta-sq = .XX |
| **Post-hoc** | Tukey HSD, Bonferroni, Games-Howell |

### Multiple Linear Regression

| Property | Detail |
|----------|--------|
| **When** | Predict continuous DV from 2+ predictors |
| **Assumptions** | Linearity, normality of residuals, homoscedasticity, no multicollinearity, independence |
| **Python** | `statsmodels.OLS(y, X).fit()` |
| **Effect size** | R-squared, adjusted R-squared, Cohen's f-squared (for change) |
| **APA format** | *F*(df1, df2) = X.XX, *p* = .XXX, *R*-sq = .XX |
| **Diagnostics** | VIF, residual plots, Cook's distance |

### Chi-Square Test

| Property | Detail |
|----------|--------|
| **When** | Test association between 2 categorical variables |
| **Assumptions** | Expected frequencies >= 5 in 80% of cells, independence |
| **Python** | `scipy.stats.chi2_contingency(table)` |
| **Effect size** | Cramer's V (general), Phi (2x2 only) |
| **Non-parametric alt** | Fisher's exact (small expected frequencies) |
| **APA format** | chi-sq(df) = X.XX, *p* = .XXX, Cramer's *V* = .XX |

### Pearson Correlation

| Property | Detail |
|----------|--------|
| **When** | Assess linear relationship between 2 continuous variables |
| **Assumptions** | Bivariate normality, linearity, homoscedasticity |
| **Python** | `pingouin.corr(x, y, method='pearson')` |
| **Effect size** | r is itself an effect size |
| **Non-parametric alt** | Spearman rho |
| **APA format** | *r*(df) = .XX, *p* = .XXX |

### HLM / Multilevel Model

| Property | Detail |
|----------|--------|
| **When** | Nested data (students in classrooms, patients in hospitals) |
| **Assumptions** | Normality of residuals at each level, linearity, homoscedasticity |
| **Python** | `statsmodels.MixedLM(formula, data, groups)` |
| **Effect size** | Pseudo R-squared (Nakagawa), ICC |
| **APA format** | Report fixed effects: *b* = X.XX, *SE* = X.XX, *t* = X.XX, *p* = .XXX |

### SEM / CFA

| Property | Detail |
|----------|--------|
| **When** | Test complex path models or confirm factor structure |
| **Assumptions** | Multivariate normality, adequate N (> 200), no multicollinearity |
| **Python** | `semopy.Model(spec).fit(data)` |
| **Effect size** | Standardized path coefficients |
| **Fit indices** | chi-sq, CFI, TLI, RMSEA, SRMR |
| **APA format** | chi-sq(df) = X.XX, *p* = .XXX, CFI = .XX, RMSEA = .XX |

### Survival Analysis

| Property | Detail |
|----------|--------|
| **When** | Analyze time-to-event data |
| **Assumptions** | Proportional hazards (Cox), non-informative censoring |
| **Python** | `lifelines.KaplanMeierFitter`, `lifelines.CoxPHFitter` |
| **Effect size** | Hazard ratio |
| **APA format** | HR = X.XX, 95% CI [X.XX, X.XX], *p* = .XXX |

---

## Post-Hoc Test Selection

| Situation | Recommended Post-Hoc | Python |
|-----------|---------------------|--------|
| Equal variances, balanced groups | Tukey HSD | `pingouin.pairwise_tukey()` |
| Equal variances, conservative | Bonferroni | `pingouin.pairwise_tests(padjust='bonf')` |
| Unequal variances | Games-Howell | `pingouin.pairwise_gameshowell()` |
| Non-parametric (after Kruskal-Wallis) | Dunn's test | `scikit_posthocs.posthoc_dunn()` |
| Repeated measures | Bonferroni-corrected paired tests | `pingouin.pairwise_tests(padjust='bonf')` |

---

## Sample Size Guidelines

| Test | Rule of Thumb | Formal Method |
|------|---------------|---------------|
| t-test | N >= 30 per group | G*Power: specify d, alpha, power |
| ANOVA | N >= 20 per group | G*Power: specify f, alpha, power, k groups |
| Correlation | N >= 50 | Fisher's z: specify r, alpha, power |
| Regression | N >= 50 + 8 * k predictors | Green (1991) |
| Chi-square | N >= 5 * cells | Expected frequency >= 5 |
| SEM / CFA | N >= 200 (minimum); 10-20 per parameter | Kline (2016) |
| HLM | 30+ clusters, 20+ per cluster | Optimal depends on ICC and model |
| Mediation | N >= 100 (Fritz & MacKinnon, 2007) | Monte Carlo power analysis |
