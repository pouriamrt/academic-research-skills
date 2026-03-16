# Assumption Testing Guide — Per-Assumption Reference with Python Code

## Purpose

Comprehensive reference for testing every statistical assumption encountered in common analyses. Each assumption includes: what it is, why it matters, how to test it (formal test + visual diagnostic), Python code, interpretation guidelines, and what to do when it is violated.

---

## 1. Normality

### What It Is

The data (or residuals, depending on the test) follow a normal (Gaussian) distribution. Most parametric tests assume normality of the dependent variable within each group, or normality of the residuals in regression.

### Why It Matters

- Parametric tests derive their p-values from the normal distribution
- Violations lead to inaccurate p-values (usually conservative for large N, liberal for small N)
- The Central Limit Theorem provides robustness for large samples (N > 30 per group)

### How to Test

#### Shapiro-Wilk Test (Formal)

Best for N < 5000. H0: data is normally distributed.

```python
from scipy import stats

data = df['score'].dropna()
W, p = stats.shapiro(data)
print(f"Shapiro-Wilk: W = {W:.4f}, p = {p:.4f}")

if p > 0.05:
    print("Verdict: MET — normality assumption supported")
elif p > 0.01:
    print("Verdict: MARGINAL — borderline violation")
else:
    print("Verdict: VIOLATED — significant departure from normality")
```

#### D'Agostino-Pearson Test (Alternative for Larger Samples)

```python
stat, p = stats.normaltest(data)
print(f"D'Agostino-Pearson: K2 = {stat:.4f}, p = {p:.4f}")
```

#### Q-Q Plot (Visual)

```python
import matplotlib.pyplot as plt
from scipy import stats as scipy_stats

fig, ax = plt.subplots(figsize=(6, 6))
scipy_stats.probplot(data, dist="norm", plot=ax)
ax.set_title("Q-Q Plot")
ax.get_lines()[0].set_markerfacecolor('steelblue')
ax.get_lines()[0].set_markersize(4)
plt.savefig("experiment_outputs/figures/qq_plot.png", dpi=300, bbox_inches='tight')
plt.close()
```

#### Skewness and Kurtosis

```python
skew = data.skew()
kurt = data.kurtosis()
print(f"Skewness: {skew:.3f} (acceptable: |skew| < 2)")
print(f"Kurtosis: {kurt:.3f} (acceptable: |kurt| < 7)")
```

### Interpretation Guide

| Indicator | Normal | Marginal | Non-Normal |
|-----------|--------|----------|------------|
| Shapiro-Wilk p | > .05 | .01-.05 | < .01 |
| Q-Q plot | Points on line | Minor deviation at tails | Clear curvature or S-shape |
| Skewness | |skew| < 0.5 | 0.5-2.0 | > 2.0 |
| Kurtosis | |kurt| < 1 | 1-7 | > 7 |

### When Violated

1. **N > 30 per group**: Invoke CLT — parametric tests are robust; note in report
2. **N < 30 and mild violation**: Consider transformation (log, sqrt)
3. **Severe violation**: Switch to non-parametric alternative
4. **Always report**: Both the test result and your decision

---

## 2. Homogeneity of Variance (Homoscedasticity for Groups)

### What It Is

The variance of the dependent variable is approximately equal across all groups being compared.

### Why It Matters

- ANOVA and t-tests assume equal variances
- Violations inflate Type I error when group sizes are unequal
- More robust when group sizes are approximately equal

### How to Test

#### Levene's Test (Robust)

H0: variances are equal. Levene's test using medians is robust to non-normality.

```python
from scipy import stats

groups = [df[df['group'] == g]['score'].dropna() for g in df['group'].unique()]
F, p = stats.levene(*groups, center='median')
print(f"Levene's test: F = {F:.4f}, p = {p:.4f}")
```

#### Bartlett's Test (Sensitive, Assumes Normality)

```python
stat, p = stats.bartlett(*groups)
print(f"Bartlett's test: T = {stat:.4f}, p = {p:.4f}")
```

#### Variance Ratio (Quick Check)

```python
variances = [g.var() for g in groups]
ratio = max(variances) / min(variances)
print(f"Variance ratio: {ratio:.2f} (acceptable: < 3.0)")
```

### When Violated

| Scenario | Solution |
|----------|----------|
| t-test, unequal variances | Use Welch's t-test (does not assume equal variance) |
| ANOVA, unequal variances | Use Welch's ANOVA or Games-Howell post-hoc |
| Regression | Use heteroscedasticity-consistent standard errors (HC3) |
| Severe + unequal N | Non-parametric alternative strongly recommended |

---

## 3. Sphericity (Repeated Measures)

### What It Is

The variances of the differences between all pairs of within-subject conditions are equal. Required for repeated-measures ANOVA with 3+ levels.

### Why It Matters

- Violation inflates Type I error in RM ANOVA
- Not applicable when there are only 2 within-subject levels

### How to Test

#### Mauchly's Test

H0: sphericity is met.

```python
import pingouin as pg

spher, W, chi2, dof, p = pg.sphericity(
    data=df, dv='score', within='time', subject='participant'
)
print(f"Mauchly's test: W = {W:.4f}, chi-sq({dof}) = {chi2:.4f}, p = {p:.4f}")
```

### When Violated

1. **Greenhouse-Geisser correction**: Conservative; use when epsilon < .75
2. **Huynh-Feldt correction**: Less conservative; use when epsilon >= .75
3. **Multivariate approach (MANOVA)**: Does not require sphericity

```python
# pingouin automatically applies corrections:
aov = pg.rm_anova(data=df, dv='score', within='time', subject='participant', correction=True)
# Check epsilon value to determine which correction is appropriate
epsilon = aov['eps'].values[0]
print(f"Epsilon: {epsilon:.3f}")
if epsilon < 0.75:
    print("Use Greenhouse-Geisser correction")
else:
    print("Use Huynh-Feldt correction")
```

---

## 4. Linearity

### What It Is

The relationship between the independent and dependent variables is linear (for regression, correlation, and ANCOVA).

### Why It Test

A non-linear relationship with a linear model produces biased estimates and misleading results.

### How to Test

#### Residual vs Fitted Plot (Visual)

```python
import statsmodels.api as sm
from statsmodels.nonparametric.smoothers_lowess import lowess

# Fit model first
X = sm.add_constant(df[predictors])
model = sm.OLS(df[dv], X).fit()

fig, ax = plt.subplots(figsize=(8, 6))
ax.scatter(model.fittedvalues, model.resid, alpha=0.5, s=20, color='steelblue')
ax.axhline(0, color='red', linestyle='--')

# LOWESS smoother to detect curvature
smooth = lowess(model.resid, model.fittedvalues, frac=0.3)
ax.plot(smooth[:, 0], smooth[:, 1], color='orange', linewidth=2, label='LOWESS')
ax.set_xlabel("Fitted Values")
ax.set_ylabel("Residuals")
ax.legend()
plt.savefig("experiment_outputs/figures/linearity_check.png", dpi=300, bbox_inches='tight')
plt.close()
```

#### Component-Plus-Residual (Partial Regression) Plots

```python
from statsmodels.graphics.regressionplots import plot_partregress_grid

fig = plot_partregress_grid(model)
plt.savefig("experiment_outputs/figures/partial_regression.png", dpi=300, bbox_inches='tight')
plt.close()
```

#### Rainbow Test (Formal)

```python
from statsmodels.stats.diagnostic import linear_rainbow

stat, p = linear_rainbow(model)
print(f"Rainbow test: F = {stat:.4f}, p = {p:.4f}")
```

### When Violated

1. Add polynomial terms (quadratic, cubic)
2. Apply transformation to predictor or outcome
3. Use generalized additive models (GAM)
4. Consider non-linear regression

---

## 5. Multicollinearity

### What It Is

Two or more predictor variables in a regression model are highly correlated, making individual coefficient estimates unstable.

### Why It Matters

- Inflated standard errors -> imprecise coefficient estimates
- Individual predictors may appear non-significant even when the model is significant
- Does NOT affect overall model fit (R-squared), only individual coefficients

### How to Test

#### Variance Inflation Factor (VIF)

```python
from statsmodels.stats.outliers_influence import variance_inflation_factor
import pandas as pd

X = df[predictors].dropna()
vif = pd.DataFrame({
    'Variable': predictors,
    'VIF': [variance_inflation_factor(X.values, i) for i in range(len(predictors))]
})
print(vif)
```

#### Correlation Matrix

```python
corr = df[predictors].corr()
print("High correlations (|r| > 0.80):")
for i in range(len(predictors)):
    for j in range(i+1, len(predictors)):
        if abs(corr.iloc[i, j]) > 0.80:
            print(f"  {predictors[i]} <-> {predictors[j]}: r = {corr.iloc[i, j]:.3f}")
```

#### Condition Number

```python
X = sm.add_constant(df[predictors].dropna())
cond = np.linalg.cond(X.values)
print(f"Condition number: {cond:.1f} (> 30 = concern)")
```

### Interpretation

| VIF | Interpretation |
|-----|---------------|
| 1.0 | No multicollinearity |
| 1-5 | Low to moderate; acceptable |
| 5-10 | Moderate to high; investigate |
| > 10 | Severe; action required |

### When Violated

1. Remove one of the correlated predictors (choose based on theory)
2. Combine correlated predictors into a composite score
3. Use principal components regression
4. Use ridge regression (penalized)
5. Center interaction terms to reduce VIF in moderation models

---

## 6. Homoscedasticity (Residuals)

### What It Is

The variance of residuals is constant across all levels of the fitted values (for regression models). Different from homogeneity of variance across groups.

### Why It Matters

- Violation makes standard errors biased (usually underestimated)
- Hypothesis tests and confidence intervals become unreliable

### How to Test

#### Breusch-Pagan Test (Formal)

H0: homoscedasticity (constant variance).

```python
from statsmodels.stats.diagnostic import het_breuschpagan

bp_stat, bp_p, f_stat, f_p = het_breuschpagan(model.resid, model.model.exog)
print(f"Breusch-Pagan: LM = {bp_stat:.4f}, p = {bp_p:.4f}")
print(f"              F  = {f_stat:.4f}, p = {f_p:.4f}")
```

#### White's Test (More General)

```python
from statsmodels.stats.diagnostic import het_white

white_stat, white_p, f_stat, f_p = het_white(model.resid, model.model.exog)
print(f"White's test: LM = {white_stat:.4f}, p = {white_p:.4f}")
```

#### Scale-Location Plot (Visual)

```python
fig, ax = plt.subplots(figsize=(8, 6))
std_resid = (model.resid - model.resid.mean()) / model.resid.std()
ax.scatter(model.fittedvalues, np.sqrt(np.abs(std_resid)), alpha=0.5, s=20)
ax.set_xlabel("Fitted Values")
ax.set_ylabel("sqrt(|Standardized Residuals|)")
plt.savefig("experiment_outputs/figures/scale_location.png", dpi=300, bbox_inches='tight')
plt.close()
```

### When Violated

1. Use heteroscedasticity-consistent (robust) standard errors:

```python
model_robust = sm.OLS(y, X).fit(cov_type='HC3')
```

2. Transform the dependent variable (log, sqrt)
3. Use weighted least squares (WLS) if the variance structure is known
4. Use generalized least squares (GLS)

---

## 7. Independence of Observations / Residuals

### What It Is

Each observation is independent of all others. In regression, the residuals should be independent (no autocorrelation).

### Why It Matters

- Clustered/correlated data violates independence -> underestimated standard errors -> inflated Type I error
- Common in repeated measures, longitudinal, and hierarchical designs

### How to Test

#### Durbin-Watson Test (Regression Residuals)

Tests for first-order autocorrelation. Value ranges from 0 to 4; 2 = no autocorrelation.

```python
from statsmodels.stats.stattools import durbin_watson

dw = durbin_watson(model.resid)
print(f"Durbin-Watson: {dw:.4f}")
print(f"  < 1.5 or > 2.5: possible autocorrelation")
print(f"  1.5-2.5: acceptable")
```

#### By Design Assessment

Independence is primarily a design issue, not a statistical one:

| Design Feature | Violation Risk | Solution |
|---------------|---------------|----------|
| Students in classrooms | High (nesting) | Use HLM / multilevel model |
| Repeated measures | High (within-subject correlation) | Use RM ANOVA or mixed model |
| Time series data | High (autocorrelation) | Use GLS or time series models |
| Random independent sample | Low | Standard tests appropriate |
| Matched pairs | Expected (pairing) | Use paired tests |

### When Violated

1. Use multilevel modeling (HLM) for nested data
2. Use generalized estimating equations (GEE) for clustered data
3. Use Newey-West standard errors for autocorrelated time series
4. Use paired/repeated measures tests when data is naturally paired

---

## 8. Absence of Influential Outliers

### What It Is

No single observation has undue influence on the regression coefficients or model fit.

### How to Test

#### Cook's Distance

```python
from statsmodels.stats.outliers_influence import OLSInfluence

influence = OLSInfluence(model)
cooks_d = influence.cooks_distance[0]
threshold = 4 / len(df)

print(f"Cook's distance threshold: {threshold:.4f}")
print(f"Cases exceeding threshold: {(cooks_d > threshold).sum()}")

# Identify influential cases
influential = df.index[cooks_d > threshold]
print(f"Influential case indices: {list(influential)}")
```

#### DFFITS

```python
dffits = influence.dffits[0]
dffits_threshold = 2 * np.sqrt((model.df_model + 1) / len(df))
print(f"DFFITS threshold: {dffits_threshold:.4f}")
print(f"Cases exceeding: {(np.abs(dffits) > dffits_threshold).sum()}")
```

### When Detected

1. Investigate the case: is it a data entry error, or a genuine extreme observation?
2. Run the analysis with and without influential cases
3. Report both sets of results if conclusions differ
4. Use robust regression if many influential points

---

## Assumption Checklist by Test

| Test | Norm | Homog | Spher | Linear | Indep | Multicol | Homosc | Outliers |
|------|------|-------|-------|--------|-------|----------|--------|----------|
| Independent t | Y | Y | — | — | Y | — | — | — |
| Paired t | Y* | — | — | — | Y | — | — | — |
| One-way ANOVA | Y | Y | — | — | Y | — | — | — |
| RM ANOVA | Y | — | Y | — | — | — | — | — |
| ANCOVA | Y | Y | — | Y | Y | — | — | — |
| Pearson r | Y | — | — | Y | Y | — | Y | — |
| Linear regression | Y** | — | — | Y | Y | Y | Y | Y |
| Logistic regression | — | — | — | Y*** | Y | Y | — | Y |
| Chi-square | — | — | — | — | Y | — | — | — |
| SEM / CFA | Y**** | — | — | — | Y | Y | — | — |

Y = Normality of DV per group
Y* = Normality of differences
Y** = Normality of residuals
Y*** = Linearity of logit
Y**** = Multivariate normality
