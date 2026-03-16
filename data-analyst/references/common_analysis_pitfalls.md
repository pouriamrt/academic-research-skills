# Common Analysis Pitfalls — Detection, Prevention, and Reporting

## Purpose

Reference guide for recognizing and avoiding common statistical analysis errors. Each pitfall includes a description, how to detect it, how to prevent it, and how to report transparently when it arises. Used by all agents as a quality safeguard.

---

## 1. Multiple Comparisons Problem

### Description

When performing multiple statistical tests, the probability of finding at least one significant result by chance increases. With 20 tests at alpha = .05, you expect 1 false positive even when no true effects exist.

**Family-wise error rate**: P(at least one Type I error) = 1 - (1 - alpha)^k

| Tests (k) | FWER (uncorrected) |
|-----------|-------------------|
| 1 | .050 |
| 5 | .226 |
| 10 | .401 |
| 20 | .642 |
| 50 | .923 |

### Detection

- Counting the number of hypothesis tests performed (including all t-tests, ANOVAs, correlations)
- Noticing selective reporting of only significant results from many tests

### Prevention

#### Correction Methods

| Method | When to Use | Python | Conservatism |
|--------|-------------|--------|-------------|
| **Bonferroni** | Small number of planned comparisons | alpha_adj = 0.05 / k | Very conservative |
| **Holm-Bonferroni** | Step-down alternative to Bonferroni | `pingouin.multicomp(p_values, method='holm')` | Less conservative |
| **Benjamini-Hochberg (FDR)** | Large number of tests, discovery-oriented | `pingouin.multicomp(p_values, method='fdr_bh')` | Controls false discovery rate |
| **Tukey HSD** | All pairwise comparisons after ANOVA | `pingouin.pairwise_tukey()` | Designed for this purpose |
| **Sidak** | Independent tests | alpha_adj = 1 - (1 - 0.05)^(1/k) | Slightly less conservative than Bonferroni |

```python
import pingouin as pg
import numpy as np

# Example: correcting multiple p-values
p_values = [0.002, 0.013, 0.029, 0.041, 0.078, 0.123]

# Bonferroni
reject_bonf, p_bonf = pg.multicomp(p_values, method='bonf')

# Holm
reject_holm, p_holm = pg.multicomp(p_values, method='holm')

# FDR (Benjamini-Hochberg)
reject_fdr, p_fdr = pg.multicomp(p_values, method='fdr_bh')

print("Original p-values:", p_values)
print("Bonferroni adjusted:", [round(p, 4) for p in p_bonf])
print("Holm adjusted:", [round(p, 4) for p in p_holm])
print("FDR adjusted:", [round(p, 4) for p in p_fdr])
```

### Reporting

Always state: (1) how many tests were performed, (2) which correction method was used, (3) both corrected and uncorrected p-values.

---

## 2. p-Hacking (Selective Analysis)

### Description

Manipulating data or analyses until a significant p-value appears. Includes:
- Running many tests and reporting only significant ones
- Adding or removing covariates until p < .05
- Collecting data until p < .05 (optional stopping)
- Transforming variables until significance emerges
- Excluding outliers selectively (only when it helps significance)
- Trying different dependent variable definitions

### Detection

- Results cluster just below p = .05 (p-values of .03, .04, .048)
- Many analyses described but only significant ones highlighted
- Post-hoc rationale for analytical decisions ("we controlled for X because...")
- No preregistration

### Prevention

1. **Preregister** the analysis plan before examining data
2. **Distinguish** confirmatory from exploratory analyses in the report
3. **Report all analyses** — including non-significant ones
4. **Fix the analysis plan** before seeing results
5. **Use multiverse analysis** to show results across all reasonable analytical choices

### Reporting

```
The following analyses were pre-specified [or: were exploratory]. All planned
analyses are reported below, including non-significant results. [If exploratory:]
These analyses should be interpreted as hypothesis-generating and will require
replication.
```

---

## 3. HARKing (Hypothesizing After Results are Known)

### Description

Presenting post-hoc hypotheses as if they were predicted a priori. This converts exploratory findings into false "confirmations," inflating apparent replication success.

### Detection

- Hypotheses perfectly match results (suspiciously precise predictions)
- No preregistration
- Introduction section seems tailored to justify specific findings

### Prevention

1. **Preregister hypotheses** before data collection
2. **Separate confirmatory and exploratory sections** in the paper
3. **Label exploratory findings explicitly**: "An exploratory analysis revealed..."
4. **Document the timeline**: When were hypotheses formulated? When was data collected?

### Reporting

Always include an explicit section distinguishing pre-specified hypotheses from exploratory findings discovered during analysis.

---

## 4. Inappropriate Outlier Handling

### Description

Removing outliers without justification, or selectively removing outliers that make results significant (a form of p-hacking).

### Detection

- Outliers removed only when they change significance
- No documented criteria for outlier detection
- Different criteria applied to different variables or groups
- Large number of exclusions without justification

### Prevention

1. **Pre-specify** outlier detection criteria (method and threshold) before analysis
2. **Apply criteria consistently** across all variables and groups
3. **Run analyses with and without outliers** — report both
4. **Investigate outliers** — are they data entry errors or genuine extreme values?
5. **Consider robust methods** (trimmed means, robust regression) rather than deletion

### Reporting

```
Outliers were defined as observations exceeding 3 standard deviations from the
group mean [or: 1.5 * IQR below Q1 or above Q3]. [N] outliers were identified
across [k] variables. Results are reported both with and without outliers.
The pattern of significance [did/did not] change when outliers were excluded.
```

---

## 5. Confusing Correlation with Causation

### Description

Interpreting a correlational finding as evidence of a causal relationship. Correlation only establishes association; causation requires experimental manipulation or strong quasi-experimental design.

### Detection

- Causal language ("X causes Y", "X leads to Y") in observational studies
- No discussion of confounding variables or alternative explanations
- Ignoring directionality (does X cause Y, or Y cause X, or Z cause both?)

### Prevention

1. **Use correlational language**: "X is associated with Y", "X predicts Y"
2. **Discuss confounds explicitly**: What third variables could explain the relationship?
3. **Consider directionality**: Cross-lagged designs, mediation, or experiments
4. **Note limitations**: "This cross-sectional design cannot establish causality"

### Reporting

```
[Variable X] was significantly correlated with [Variable Y] (r = .45, p < .001).
However, given the cross-sectional design, causal inferences cannot be drawn.
[Potential confound Z] was not measured and may partially account for this
association.
```

---

## 6. Ignoring Effect Sizes

### Description

Reporting only p-values without effect sizes. A statistically significant result with a tiny effect size may be practically meaningless. Conversely, a non-significant result may reflect an important effect in an underpowered study.

### Detection

- Results reported as "significant" or "not significant" without magnitudes
- No effect sizes or confidence intervals
- No discussion of practical importance

### Prevention

1. **Report effect sizes for every test** (APA requires this)
2. **Include confidence intervals**
3. **Interpret practical significance** — is the effect large enough to matter?
4. **Discuss statistical vs practical significance** when they diverge

### Reporting

Always include: test statistic, df, exact p-value, effect size, and CI. Then interpret the effect's practical meaning.

---

## 7. Overfitting

### Description

A model fits the sample data very well but fails to generalize to new data. Occurs when the model captures noise rather than signal, often due to too many predictors relative to sample size.

### Detection

- Very high R-squared but poor out-of-sample prediction
- Large gap between R-squared and adjusted R-squared
- Predictors that are theoretically implausible but statistically significant
- N:predictor ratio < 10:1

### Prevention

1. **Follow sample size guidelines**: N >= 50 + 8k for regression (Green, 1991)
2. **Use adjusted R-squared** or AIC/BIC for model selection
3. **Cross-validate**: k-fold CV to estimate out-of-sample performance
4. **Use regularization**: Ridge or LASSO regression when many predictors
5. **Prefer parsimonious models**: Simpler models often generalize better

```python
from sklearn.model_selection import cross_val_score
from sklearn.linear_model import LinearRegression

model = LinearRegression()
cv_scores = cross_val_score(model, X, y, cv=5, scoring='r2')
print(f"Cross-validated R-sq: {cv_scores.mean():.3f} (+/- {cv_scores.std():.3f})")
```

### Reporting

```
The model explained [R-sq]% of variance in the training data (adjusted R-sq = [value]).
Five-fold cross-validation yielded an average R-sq of [value] (SD = [value]),
suggesting [good/moderate/poor] generalization.
```

---

## 8. Ecological Fallacy

### Description

Drawing conclusions about individuals based on group-level (aggregate) data. Patterns observed at the group level may not hold for individuals.

### Detection

- Analyzing country-level or school-level averages and drawing individual-level conclusions
- Using aggregated data (e.g., state-level income) to predict individual outcomes

### Prevention

1. **Use individual-level data** when the research question is about individuals
2. **Use multilevel modeling** when data has a hierarchical structure
3. **Clearly state** the level of analysis (individual, group, population)
4. **Avoid cross-level inferences** without multilevel modeling

### Reporting

```
Note: This analysis uses [school/state/country]-level data. Findings describe
patterns at the [aggregate level] and should not be interpreted as describing
individual-level relationships (ecological fallacy).
```

---

## 9. Simpson's Paradox

### Description

A trend that appears in several different groups of data disappears or reverses when these groups are combined. Often caused by a lurking confounding variable.

### Detection

- Results change direction when a third variable is controlled
- Subgroup analyses show different patterns than the overall analysis

### Prevention

1. **Always examine subgroups** when theoretically relevant
2. **Control for known confounds** in the analysis
3. **Use causal reasoning** (DAGs) to identify confounders
4. **Report both** overall and subgroup results

---

## 10. Violation of Independence

### Description

Analyzing clustered or nested data with methods that assume independence. Students in the same classroom are not independent; patients in the same hospital share contextual factors.

### Detection

- Data has a natural hierarchy (students in schools, patients in clinics)
- Repeated measures on the same subjects
- ICC > 0.05 suggests non-trivial clustering

### Prevention

1. **Check the ICC** (intraclass correlation coefficient) for clustered data
2. **Use multilevel modeling (HLM)** for nested data
3. **Use repeated-measures designs** for within-subject data
4. **Use cluster-robust standard errors** if full multilevel modeling is not feasible

```python
import pingouin as pg

icc = pg.intraclass_corr(data=df, targets='student', raters='classroom',
                          ratings='score', nan_policy='omit')
print(icc[['Type', 'ICC', 'CI95%']])
# If ICC1 > 0.05, clustering matters
```

---

## 11. Post-Hoc Power Analysis

### Description

Computing statistical power after the study is complete using the observed effect size. This is circular and uninformative — observed power is a direct function of the p-value and adds no new information.

### Detection

- Power analysis using the observed (sample) effect size
- Claiming "the study had 35% power" to explain a non-significant result

### Prevention

1. **Conduct power analysis a priori** (before data collection) using effect sizes from prior literature or minimal meaningful effects
2. **Do NOT compute post-hoc power** — it is mathematically redundant with the p-value
3. **Report confidence intervals** instead — they convey the same information more usefully
4. **If underpowered**, acknowledge the limitation and report the CI to show what effects remain plausible

### Reporting

Instead of post-hoc power:
```
The 95% confidence interval for Cohen's d ranged from -0.12 to 0.68, indicating
that effects ranging from negligible to medium remain consistent with the data.
Future research with larger samples would be needed to detect the smaller effects
within this range.
```

---

## 12. Dichotomizing Continuous Variables

### Description

Converting a continuous variable into categories (e.g., median split into "high" and "low" groups). This discards information and reduces statistical power.

### Detection

- Continuous predictor or moderator split into two groups at the median
- Significant results only after dichotomization

### Prevention

1. **Keep variables continuous** in regression and correlation analyses
2. **Use interaction terms** for moderation instead of subgroup analysis
3. If categorization is theoretically required, use established cutoffs (e.g., clinical thresholds), not median splits
4. **Report** the continuous analysis alongside any categorical version

---

## Pitfall Checklist

Before finalizing any analysis, verify:

- [ ] Multiple comparison correction applied (if > 1 test)
- [ ] Pre-specified vs exploratory analyses clearly distinguished
- [ ] Effect sizes reported for all primary results
- [ ] Outlier handling criteria were pre-specified and consistently applied
- [ ] Causal language used only for experimental designs
- [ ] Sample size adequate for the analysis (no overfitting)
- [ ] Independence assumption checked (no unmodeled clustering)
- [ ] Continuous variables not inappropriately dichotomized
- [ ] All planned analyses reported (not just significant ones)
- [ ] Confidence intervals provided for key estimates
- [ ] No post-hoc power analyses reported
- [ ] Simpson's paradox checked when relevant subgroups exist
