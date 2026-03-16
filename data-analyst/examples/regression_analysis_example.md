# Example: Multiple Regression — Predicting GPA from Study Habits

## Scenario

A researcher wants to predict undergraduate GPA from three predictors: weekly study hours, class attendance rate (%), and prior achievement (high school GPA). The dataset contains N = 200 students.

**Research Question**: How well do study hours, attendance, and prior achievement predict undergraduate GPA?

**Hypotheses**:
- H1: The overall model significantly predicts GPA
- H2: Each predictor makes a unique significant contribution
- H3: Prior achievement is the strongest predictor

---

## Phase 1: Intake

### Mode Detection

User command: "Run a multiple regression predicting GPA from study hours, attendance, and prior GPA"

**Mode**: `full`

### Data Loading

```python
import pandas as pd
import numpy as np

df = pd.read_csv("student_gpa.csv")
print(f"Shape: {df.shape}")
print(df.head())
```

**Output**:
```
Shape: (200, 5)

   student_id  study_hours  attendance  prior_gpa    gpa
0           1         12.5       85.0       3.21   3.15
1           2          8.0       72.0       2.85   2.67
2           3         15.0       92.0       3.55   3.42
3           4          6.0       65.0       2.40   2.31
4           5         20.0       95.0       3.78   3.71
```

### Dataset Profile

| Variable | Type | Missing | Missing % | Mean | SD | Min | Max | Skew |
|----------|------|---------|-----------|------|------|-----|-----|------|
| student_id | int | 0 | 0% | — | — | 1 | 200 | — |
| study_hours | float | 5 | 2.5% | 12.4 | 5.2 | 1.0 | 30.0 | 0.45 |
| attendance | float | 8 | 4.0% | 79.3 | 14.7 | 30.0 | 100.0 | -0.62 |
| prior_gpa | float | 3 | 1.5% | 3.02 | 0.52 | 1.50 | 4.00 | -0.28 |
| gpa | float | 0 | 0% | 2.94 | 0.58 | 1.20 | 4.00 | -0.33 |

### Analysis Plan

- **Primary**: Multiple linear regression — DV: gpa, Predictors: study_hours, attendance, prior_gpa
- **Alpha**: .05

---

## Phase 2: Data Preparation

### Missing Data Assessment

```python
from scipy import stats

# Missing data summary
missing = df.isnull().sum()
print(missing[missing > 0])
# study_hours    5 (2.5%)
# attendance     8 (4.0%)
# prior_gpa      3 (1.5%)
# Total: 16 missing values across 3 variables
```

### Little's MCAR Test

```python
# Using the custom implementation from data_preparation_agent
result = littles_mcar_test(df[['study_hours', 'attendance', 'prior_gpa', 'gpa']])
print(f"Little's MCAR test: chi-sq({result['df']}) = {result['chi_sq']}, p = {result['p']}")
```

**Result**: chi-sq(8) = 6.42, *p* = .600 -> MCAR supported

### Missing Data Strategy

Given MCAR and < 5% missingness, listwise deletion is appropriate.

```python
df_clean = df.dropna(subset=['study_hours', 'attendance', 'prior_gpa', 'gpa'])
print(f"Original N: {len(df)}, After listwise deletion: {len(df_clean)}, Dropped: {len(df) - len(df_clean)}")
# Original N: 200, After listwise deletion: 186, Dropped: 14
```

### Outlier Detection

```python
# Mahalanobis distance for multivariate outliers
from scipy.stats import chi2

predictors = ['study_hours', 'attendance', 'prior_gpa']
X = df_clean[predictors].values
mean = np.mean(X, axis=0)
cov = np.cov(X.T)
inv_cov = np.linalg.pinv(cov)

mahal = np.array([np.sqrt((x - mean) @ inv_cov @ (x - mean)) for x in X])
p_values = 1 - chi2.cdf(mahal**2, df=len(predictors))
outliers = (p_values < 0.001).sum()
print(f"Multivariate outliers (Mahalanobis, p < .001): {outliers}")
```

**Result**: 2 multivariate outliers detected. Analysis run with and without them; results are consistent. Outliers retained.

### Data Saved

- Cleaned data: `experiment_outputs/tables/cleaned_data.csv`
- Cleaning log: `experiment_outputs/logs/data_cleaning_log.md`

---

## Phase 3: Assumption Checking

### Assumption 1: Linearity

```python
import statsmodels.api as sm

X = sm.add_constant(df_clean[predictors])
y = df_clean['gpa']
model = sm.OLS(y, X).fit()

# Residuals vs Fitted plot
from statsmodels.nonparametric.smoothers_lowess import lowess

fig, ax = plt.subplots(figsize=(8, 6))
ax.scatter(model.fittedvalues, model.resid, alpha=0.5, s=20, color='steelblue')
ax.axhline(0, color='red', linestyle='--')
smooth = lowess(model.resid, model.fittedvalues, frac=0.3)
ax.plot(smooth[:, 0], smooth[:, 1], color='orange', linewidth=2, label='LOWESS')
ax.set_xlabel("Fitted Values")
ax.set_ylabel("Residuals")
ax.legend()
plt.savefig("experiment_outputs/figures/figure_01_residuals_vs_fitted.png", dpi=300, bbox_inches='tight')
plt.close()
```

**Verdict**: Met — LOWESS line stays close to zero; no curvature detected.

### Assumption 2: Normality of Residuals

```python
W, p = stats.shapiro(model.resid)
print(f"Shapiro-Wilk (residuals): W = {W:.4f}, p = {p:.4f}")
```

**Result**: W = 0.9891, *p* = .143 -> Met

Q-Q plot saved to `experiment_outputs/figures/figure_02_qq_residuals.png`. Points follow the reference line closely.

### Assumption 3: Homoscedasticity

```python
from statsmodels.stats.diagnostic import het_breuschpagan

bp_stat, bp_p, f_stat, f_p = het_breuschpagan(model.resid, model.model.exog)
print(f"Breusch-Pagan: LM = {bp_stat:.4f}, p = {bp_p:.4f}")
```

**Result**: LM = 3.21, *p* = .360 -> Met

### Assumption 4: No Multicollinearity

```python
from statsmodels.stats.outliers_influence import variance_inflation_factor

vif_data = pd.DataFrame({
    'Variable': predictors,
    'VIF': [variance_inflation_factor(X.values, i+1) for i in range(len(predictors))]
})
print(vif_data)
```

| Variable | VIF | Verdict |
|----------|-----|---------|
| study_hours | 1.34 | OK |
| attendance | 1.28 | OK |
| prior_gpa | 1.41 | OK |

All VIF < 5 -> No multicollinearity.

### Assumption 5: Independence of Residuals

```python
from statsmodels.stats.stattools import durbin_watson

dw = durbin_watson(model.resid)
print(f"Durbin-Watson: {dw:.4f}")
```

**Result**: DW = 2.08 -> Met (acceptable range: 1.5-2.5)

### Assumption Summary

| Assumption | Test | Statistic | p | Verdict | Action |
|------------|------|-----------|---|---------|--------|
| Linearity | Residual plot + LOWESS | — | — | Met | Proceed |
| Normality (residuals) | Shapiro-Wilk | W = 0.99 | .143 | Met | Proceed |
| Homoscedasticity | Breusch-Pagan | LM = 3.21 | .360 | Met | Proceed |
| No multicollinearity | VIF | max = 1.41 | — | Met | Proceed |
| Independence | Durbin-Watson | DW = 2.08 | — | Met | Proceed |

**Overall**: All assumptions met. Proceed with standard OLS regression.

---

## Phase 4: Analysis Execution

### Multiple Regression

```python
import statsmodels.api as sm

X = sm.add_constant(df_clean[['study_hours', 'attendance', 'prior_gpa']])
y = df_clean['gpa']
model = sm.OLS(y, X).fit()
print(model.summary())
```

### Results

**Overall Model**: *F*(3, 182) = 27.14, *p* < .001, *R*-sq = .309, Adjusted *R*-sq = .298

**Coefficients**:

| Predictor | *b* | *SE* | *t* | *p* | 95% CI | beta |
|-----------|------|------|------|------|--------|------|
| Intercept | 0.42 | 0.28 | 1.50 | .135 | [-0.13, 0.97] | — |
| study_hours | 0.02 | 0.01 | 2.67 | .008 | [0.01, 0.04] | .19 |
| attendance | 0.01 | 0.003 | 2.34 | .020 | [0.001, 0.014] | .17 |
| prior_gpa | 0.53 | 0.08 | 6.63 | < .001 | [0.37, 0.69] | .47 |

### Reproducibility Script

Saved to `experiment_outputs/scripts/analysis.py` with seed = 42.

---

## Phase 5: Effect Sizes

### Overall Model

```python
r_sq = model.rsquared
adj_r_sq = model.rsquared_adj
f_sq = r_sq / (1 - r_sq)
print(f"R-squared: {r_sq:.4f}")
print(f"Adjusted R-squared: {adj_r_sq:.4f}")
print(f"Cohen's f-squared: {f_sq:.4f}")
```

| Measure | Value | 95% CI | Magnitude |
|---------|-------|--------|-----------|
| *R*-sq | .309 | [.20, .42] | Large |
| Adjusted *R*-sq | .298 | — | Large |
| Cohen's *f*-sq | .447 | — | Large |

### Per-Predictor Contribution

Unique variance explained (sr-squared, squared semi-partial correlation):

| Predictor | sr-sq | Unique % | Magnitude |
|-----------|-------|----------|-----------|
| prior_gpa | .171 | 17.1% | Large |
| study_hours | .028 | 2.8% | Small |
| attendance | .021 | 2.1% | Small |

### Interpretation

The full model explains 30.9% of the variance in GPA — a large effect (*R*-sq = .309). Prior achievement is the strongest unique predictor (beta = .47), uniquely accounting for 17.1% of the variance. Study hours (beta = .19) and attendance (beta = .17) each make smaller but significant unique contributions (2.8% and 2.1%, respectively).

In practical terms: for each 1-hour increase in weekly study time, GPA increases by approximately 0.02 points, holding other predictors constant. For each 1-point increase in prior GPA, undergraduate GPA increases by approximately 0.53 points.

---

## Phase 6: Visualization

### Figure 1: Residual Diagnostic Plots (4-Panel)

```python
fig, axes = plt.subplots(2, 2, figsize=(12, 10))

# Panel 1: Residuals vs Fitted
axes[0, 0].scatter(model.fittedvalues, model.resid, alpha=0.5, s=20, color='steelblue')
axes[0, 0].axhline(0, color='red', linestyle='--')
axes[0, 0].set_xlabel("Fitted Values")
axes[0, 0].set_ylabel("Residuals")
axes[0, 0].set_title("Residuals vs Fitted")

# Panel 2: Q-Q Plot
from scipy import stats as scipy_stats
scipy_stats.probplot(model.resid, dist="norm", plot=axes[0, 1])
axes[0, 1].set_title("Normal Q-Q")

# Panel 3: Scale-Location
std_resid = (model.resid - model.resid.mean()) / model.resid.std()
axes[1, 0].scatter(model.fittedvalues, np.sqrt(np.abs(std_resid)), alpha=0.5, s=20)
axes[1, 0].set_xlabel("Fitted Values")
axes[1, 0].set_ylabel("sqrt(|Standardized Residuals|)")
axes[1, 0].set_title("Scale-Location")

# Panel 4: Residuals vs Leverage
from statsmodels.stats.outliers_influence import OLSInfluence
influence = OLSInfluence(model)
leverage = influence.hat_matrix_diag
axes[1, 1].scatter(leverage, std_resid, alpha=0.5, s=20)
axes[1, 1].axhline(0, color='red', linestyle='--')
axes[1, 1].set_xlabel("Leverage")
axes[1, 1].set_ylabel("Standardized Residuals")
axes[1, 1].set_title("Residuals vs Leverage")

plt.tight_layout()
plt.savefig("experiment_outputs/figures/figure_01_residual_diagnostics.png", dpi=300, bbox_inches='tight')
plt.savefig("experiment_outputs/figures/figure_01_residual_diagnostics.pdf", bbox_inches='tight')
plt.close()
```

**Figure 1.** *Regression diagnostic plots. Top left: residuals vs fitted values (linearity). Top right: Q-Q plot (normality of residuals). Bottom left: scale-location (homoscedasticity). Bottom right: residuals vs leverage (influential observations).*

### Figure 2: Scatter Plots (Each Predictor vs GPA)

```python
fig, axes = plt.subplots(1, 3, figsize=(18, 5))

for i, pred in enumerate(['study_hours', 'attendance', 'prior_gpa']):
    sns.regplot(data=df_clean, x=pred, y='gpa', ax=axes[i],
                scatter_kws={'alpha': 0.5, 's': 20}, ci=95)
    axes[i].set_xlabel(pred.replace('_', ' ').title())
    axes[i].set_ylabel("GPA")

plt.tight_layout()
plt.savefig("experiment_outputs/figures/figure_02_scatter_predictors.png", dpi=300, bbox_inches='tight')
plt.savefig("experiment_outputs/figures/figure_02_scatter_predictors.pdf", bbox_inches='tight')
plt.close()
```

**Figure 2.** *Scatter plots of GPA by each predictor with linear regression lines and 95% confidence bands. Left: study hours. Center: attendance. Right: prior GPA.*

### Figure 3: Correlation Heatmap

```python
corr = df_clean[['study_hours', 'attendance', 'prior_gpa', 'gpa']].corr()

fig, ax = plt.subplots(figsize=(8, 6))
mask = np.triu(np.ones_like(corr, dtype=bool), k=1)
sns.heatmap(corr, mask=mask, annot=True, fmt='.2f', cmap='RdBu_r',
            center=0, vmin=-1, vmax=1, square=True, ax=ax, linewidths=0.5)
plt.savefig("experiment_outputs/figures/figure_03_correlation_heatmap.png", dpi=300, bbox_inches='tight')
plt.savefig("experiment_outputs/figures/figure_03_correlation_heatmap.pdf", bbox_inches='tight')
plt.close()
```

**Figure 3.** *Correlation matrix heatmap for study hours, attendance, prior GPA, and GPA. Values represent Pearson correlation coefficients.*

---

## Phase 7: Report Compilation

### APA Results Text

A multiple linear regression was conducted to predict undergraduate GPA from weekly study hours, class attendance rate, and prior achievement (high school GPA). The overall model was significant, *F*(3, 182) = 27.14, *p* < .001, *R*-sq = .309, adjusted *R*-sq = .298, indicating that the three predictors collectively explained 30.9% of the variance in GPA — a large effect (Cohen's *f*-sq = 0.45).

Prior GPA was the strongest predictor, *b* = 0.53, *SE* = 0.08, *t*(182) = 6.63, *p* < .001, 95% CI [0.37, 0.69], beta = .47. For each 1-point increase in high school GPA, undergraduate GPA increased by approximately 0.53 points, holding study hours and attendance constant.

Study hours was a significant predictor, *b* = 0.02, *SE* = 0.01, *t*(182) = 2.67, *p* = .008, 95% CI [0.01, 0.04], beta = .19. Attendance was also a significant predictor, *b* = 0.01, *SE* = 0.003, *t*(182) = 2.34, *p* = .020, 95% CI [0.001, 0.014], beta = .17.

All regression assumptions were met: residuals were normally distributed (Shapiro-Wilk *W* = 0.99, *p* = .143), variance was homogeneous (Breusch-Pagan LM = 3.21, *p* = .360), no multicollinearity was present (all VIF < 1.5), and residuals were independent (Durbin-Watson = 2.08).

### Table 1: Regression Results

**Table 1**

*Multiple Regression Results Predicting Undergraduate GPA*

| Predictor | *b* | *SE* | *t* | *p* | 95% CI | beta |
|-----------|------|------|------|------|--------|------|
| Intercept | 0.42 | 0.28 | 1.50 | .135 | [-0.13, 0.97] | — |
| Study hours | 0.02 | 0.01 | 2.67 | .008 | [0.01, 0.04] | .19 |
| Attendance | 0.01 | 0.003 | 2.34 | .020 | [0.001, 0.014] | .17 |
| Prior GPA | 0.53 | 0.08 | 6.63 | < .001 | [0.37, 0.69] | .47 |

*Note.* *R*-sq = .309, Adjusted *R*-sq = .298. *F*(3, 182) = 27.14, *p* < .001. *N* = 186.

---

## Schema 11 Handoff Artifact

```markdown
## Experiment Results

**Experiment ID**: EXP-20260316-REG-DEMO
**Result Type**: statistical_analysis

**Dataset Info**:
- Original N: 200
- Analyzed N: 186 (14 excluded: listwise deletion for missing data)
- Missing strategy: Listwise deletion (MCAR confirmed, < 5%)

**Assumption Checks**:
| Assumption | Test | Statistic | p | Verdict | Action |
|------------|------|-----------|---|---------|--------|
| Linearity | Residual plot | — | — | Met | Proceed |
| Normality (residuals) | Shapiro-Wilk | W = 0.99 | .143 | Met | Proceed |
| Homoscedasticity | Breusch-Pagan | LM = 3.21 | .360 | Met | Proceed |
| Multicollinearity | VIF | max = 1.41 | — | Met | Proceed |
| Independence | Durbin-Watson | DW = 2.08 | — | Met | Proceed |

**Primary Results**:
- H1 (overall model): F(3, 182) = 27.14, p < .001, R-sq = .309
- H2 (individual predictors): all three significant (p < .05)
- H3 (strongest predictor): prior_gpa (beta = .47)

**Effect Sizes**:
| Measure | Value | 95% CI | Magnitude |
|---------|-------|--------|-----------|
| R-sq | .309 | [.20, .42] | Large |
| f-sq | .447 | — | Large |
| sr-sq (prior_gpa) | .171 | — | Large |
| sr-sq (study_hours) | .028 | — | Small |
| sr-sq (attendance) | .021 | — | Small |

**Tables**: Table 1 at experiment_outputs/tables/table_01_regression.csv
**Figures**:
- Figure 1 at experiment_outputs/figures/figure_01_residual_diagnostics.png
- Figure 2 at experiment_outputs/figures/figure_02_scatter_predictors.png
- Figure 3 at experiment_outputs/figures/figure_03_correlation_heatmap.png

**Reproducibility**: script at experiment_outputs/scripts/analysis.py, seed=42
```

---

## Key Takeaways from This Example

1. **Missing data handled transparently** — Little's test run, MCAR confirmed, listwise deletion justified
2. **All five regression assumptions tested** with formal tests and visual diagnostics
3. **Both unstandardized (b) and standardized (beta) coefficients** reported
4. **Semi-partial correlations** (sr-sq) decompose unique variance per predictor
5. **Three types of visualization** — diagnostic plots, scatter plots, correlation heatmap
6. **Practical interpretation** — coefficients translated to concrete GPA-point changes
7. **Complete Schema 11** artifact with all required fields for academic-paper handoff
