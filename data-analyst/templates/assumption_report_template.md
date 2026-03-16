# Assumption Report Template

## Purpose

Template for the standalone assumption check report produced by `assumption_checker_agent`. Used in all modes (as Phase 3 output) and as the sole output in `assumption-check` mode.

---

## Instructions

1. Complete one section per planned analysis (a single analysis may require multiple assumption tests)
2. Every assumption receives a formal statistical test AND a diagnostic plot
3. Verdicts are exactly one of: `met`, `violated`, `marginal`
4. Actions specify what was done (or recommended) in response to the verdict
5. The Overall Recommendation summarizes whether to proceed with parametric or switch to non-parametric

---

## Report Structure

```markdown
# Assumption Check Report

**Date**: [YYYY-MM-DD]
**Dataset**: [filename], N = [n]
**Planned Analyses**: [list of planned tests]

---

## Analysis 1: [Test Name] — [DV] by [IV]

### Assumptions Required

| # | Assumption | Required Because |
|---|------------|-----------------|
| 1 | [Normality] | [Test assumes normally distributed DV per group] |
| 2 | [Homogeneity of variance] | [Test assumes equal variances across groups] |
| 3 | [Independence] | [Observations must be independent] |

### Test Results

#### Assumption 1: Normality

**Test**: Shapiro-Wilk
**Applied to**: [DV] in each group separately

| Group | W | p | Verdict |
|-------|---|---|---------|
| [Group A] | [W value] | [p value] | [met/violated/marginal] |
| [Group B] | [W value] | [p value] | [met/violated/marginal] |
| [Group C] | [W value] | [p value] | [met/violated/marginal] |

**Diagnostic Plot**: Q-Q plots per group

![Q-Q Group A](experiment_outputs/figures/qq_[variable]_[groupA].png)

*Figure A1. Q-Q plot for [variable] in [Group A].*

![Q-Q Group B](experiment_outputs/figures/qq_[variable]_[groupB].png)

*Figure A2. Q-Q plot for [variable] in [Group B].*

**Interpretation**: [Describe what the Q-Q plots show — points close to reference line = normality supported; curvature = departure from normality]

**Verdict**: [met / violated / marginal]

**Action**: [Proceed with parametric test / Switch to non-parametric / Proceed with caution (CLT applies, N > 30 per group)]

---

#### Assumption 2: Homogeneity of Variance

**Test**: Levene's test (median-based, robust to non-normality)

| Statistic | Value |
|-----------|-------|
| F | [F value] |
| df1 | [df1] |
| df2 | [df2] |
| p | [p value] |

**Verdict**: [met / violated / marginal]

**Action**: [Proceed / Apply Welch's correction / Use non-parametric test]

**Note on robustness**: [If groups are approximately equal size, ANOVA is robust to moderate violations. If group sizes are very unequal, violation is more concerning.]

---

#### Assumption 3: Independence

**Test**: By design (not statistically tested)

**Assessment**: [Observations are/are not independent based on study design. E.g., students nested in classrooms -> consider multilevel modeling.]

**Verdict**: [met / violated / marginal]

**Action**: [Proceed / Consider HLM / Not a concern for this design]

---

### Assumption Summary for Analysis 1

| Assumption | Test | Statistic | p | Verdict | Action |
|------------|------|-----------|---|---------|--------|
| Normality (Group A) | Shapiro-Wilk | W = [value] | [p] | [verdict] | [action] |
| Normality (Group B) | Shapiro-Wilk | W = [value] | [p] | [verdict] | [action] |
| Normality (Group C) | Shapiro-Wilk | W = [value] | [p] | [verdict] | [action] |
| Homogeneity | Levene's | F = [value] | [p] | [verdict] | [action] |
| Independence | By design | — | — | [verdict] | [action] |

### Overall Recommendation for Analysis 1

**Recommendation**: [PROCEED with [parametric test] / SWITCH to [non-parametric alternative] / PROCEED with correction ([specify])]

**Justification**: [Why this recommendation — which assumptions were met/violated, robustness considerations, sample size context]

**Alternative if needed**: [Non-parametric alternative name and brief rationale]

---

## Analysis 2: [Test Name] — [DV] predicted by [Predictors]

[Same structure as Analysis 1, with assumptions specific to the planned test]

### Assumptions Required

| # | Assumption | Required Because |
|---|------------|-----------------|
| 1 | Linearity | Relationship between predictors and DV must be linear |
| 2 | Normality of residuals | Residuals must be normally distributed |
| 3 | Homoscedasticity | Residual variance must be constant across fitted values |
| 4 | No multicollinearity | Predictors must not be highly correlated |
| 5 | Independence of residuals | Residuals must be independent (no autocorrelation) |

[Test results for each assumption with the same format as Analysis 1]

---

## Overall Summary

### All Assumptions at a Glance

| Analysis | Assumption | Verdict | Action Taken |
|----------|-----------|---------|-------------|
| [Analysis 1] | Normality | [verdict] | [action] |
| [Analysis 1] | Homogeneity | [verdict] | [action] |
| [Analysis 2] | Linearity | [verdict] | [action] |
| [Analysis 2] | Normality (residuals) | [verdict] | [action] |
| [Analysis 2] | Homoscedasticity | [verdict] | [action] |
| [Analysis 2] | Multicollinearity | [verdict] | [action] |

### Diagnostic Plots Index

| Plot | File | Purpose |
|------|------|---------|
| Q-Q plot (Group A) | experiment_outputs/figures/qq_*.png | Normality assessment |
| Q-Q plot (Group B) | experiment_outputs/figures/qq_*.png | Normality assessment |
| Residuals vs Fitted | experiment_outputs/figures/residuals_vs_fitted.png | Linearity + homoscedasticity |
| Scale-Location | experiment_outputs/figures/scale_location.png | Homoscedasticity |

### Proceed / Switch Decisions

| Analysis | Original Plan | Decision | Final Test |
|----------|---------------|----------|-----------|
| [Analysis 1] | [One-way ANOVA] | [Proceed] | [One-way ANOVA] |
| [Analysis 2] | [Multiple regression] | [Switch: use robust SE] | [Regression with HC3 SE] |

---

## Notes on Large Samples

For samples with N > 200, note that formal assumption tests (Shapiro-Wilk, Levene's) become overly sensitive and may flag trivial departures as "significant." In such cases:

1. **Emphasize visual diagnostics** (Q-Q plots, residual plots) over formal tests
2. **Consider the magnitude of departure**, not just the p-value
3. **Invoke the Central Limit Theorem** for normality — with large N, sampling distributions of means are approximately normal regardless of population distribution
4. **Report both** the formal test result and the visual assessment, noting the discrepancy when relevant
```

---

## Verdict Definitions

| Verdict | Criteria | Implication |
|---------|----------|-------------|
| `met` | Formal test p > .05 AND diagnostic plot shows no concerning pattern | Proceed with planned parametric test |
| `marginal` | Formal test .01 < p < .05, OR plot shows minor departure, OR large sample with trivial violation | Proceed with caution; note in report; consider robustness check |
| `violated` | Formal test p < .01 AND diagnostic plot confirms substantial departure | Switch to non-parametric alternative or apply correction |
