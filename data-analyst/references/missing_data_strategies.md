# Missing Data Strategies — Diagnosis, Treatment, and Reporting

## Purpose

Comprehensive reference for handling missing data in statistical analyses. Covers mechanism diagnosis, treatment strategies, implementation code, and reporting requirements. Used primarily by `data_preparation_agent`.

---

## 1. Missing Data Mechanisms

Understanding the mechanism is essential for choosing the right strategy. Using the wrong strategy can introduce bias.

### MCAR — Missing Completely At Random

**Definition**: The probability of missingness is unrelated to any observed or unobserved variable. Missingness is essentially random.

**Example**: A respondent accidentally skips a question because they turned two pages at once.

**Consequence**: No bias from any deletion method, but reduced power.

**Diagnosis**: Little's MCAR test (see Section 2).

### MAR — Missing At Random

**Definition**: The probability of missingness is related to observed variables but NOT to the missing value itself, conditional on observed data.

**Example**: Male participants are less likely to report their weight, but conditional on gender, the missingness is random (not related to actual weight).

**Consequence**: Listwise deletion produces biased estimates. Multiple imputation or FIML is required.

**Diagnosis**: Cannot be definitively tested, but logistic regression predicting missingness from observed variables provides evidence.

### MNAR — Missing Not At Random

**Definition**: The probability of missingness is related to the missing value itself, even after conditioning on observed data.

**Example**: Participants with very low test scores are more likely to drop out of the study (and their scores are the missing values).

**Consequence**: All standard methods (deletion, MI) may be biased. Sensitivity analysis is required.

**Diagnosis**: Cannot be statistically tested. Must rely on domain knowledge and theoretical reasoning.

---

## 2. Diagnosing the Mechanism

### Little's MCAR Test

H0: Data is MCAR. If p > .05, MCAR is supported.

```python
import numpy as np
from scipy import stats
import pandas as pd

def littles_mcar_test(df):
    """
    Simplified Little's MCAR test.
    Tests whether the pattern of missing data is consistent with MCAR.
    """
    numeric_df = df.select_dtypes(include='number')
    n, p_vars = numeric_df.shape

    # Only proceed if there is missing data
    if not numeric_df.isnull().any().any():
        return {'result': 'No missing data', 'verdict': 'N/A'}

    # Get unique missing data patterns
    patterns = numeric_df.isnull()
    unique_patterns = patterns.drop_duplicates()

    grand_mean = numeric_df.mean()
    grand_cov = numeric_df.cov()

    chi_sq_total = 0
    df_total = 0

    for _, pattern in unique_patterns.iterrows():
        # Get rows matching this pattern
        mask = (patterns == pattern).all(axis=1)
        subset = numeric_df[mask]
        n_pattern = len(subset)

        if n_pattern < 2:
            continue

        # Get observed variables for this pattern
        obs_vars = pattern[~pattern].index.tolist()
        if len(obs_vars) == 0 or len(obs_vars) == p_vars:
            continue

        # Compute chi-square contribution
        pattern_mean = subset[obs_vars].mean()
        mean_diff = pattern_mean - grand_mean[obs_vars]

        try:
            cov_sub = grand_cov.loc[obs_vars, obs_vars]
            inv_cov = np.linalg.pinv(cov_sub.values)
            chi_sq_contribution = n_pattern * float(
                mean_diff.values @ inv_cov @ mean_diff.values
            )
            chi_sq_total += chi_sq_contribution
            df_total += len(obs_vars)
        except np.linalg.LinAlgError:
            continue

    df_total -= p_vars

    if df_total <= 0:
        return {'chi_sq': np.nan, 'df': 0, 'p': np.nan,
                'verdict': 'Cannot compute (insufficient patterns)'}

    p_value = 1 - stats.chi2.cdf(chi_sq_total, df_total)

    return {
        'chi_sq': round(chi_sq_total, 4),
        'df': df_total,
        'p': round(p_value, 4),
        'verdict': 'MCAR' if p_value > 0.05 else 'Not MCAR (likely MAR or MNAR)'
    }
```

### Logistic Regression Approach (MAR Evidence)

Predict missingness from observed variables. If observed variables predict missingness, data is at least MAR.

```python
def diagnose_mar(df, target_var):
    """
    Use logistic regression to test whether missingness in target_var
    is predicted by other observed variables (evidence for MAR).
    """
    import statsmodels.api as sm

    # Create missingness indicator
    df_test = df.copy()
    df_test['_missing'] = df_test[target_var].isnull().astype(int)

    # Use other numeric variables as predictors
    predictors = [c for c in df.select_dtypes(include='number').columns
                  if c != target_var and df[c].isnull().sum() == 0]

    if len(predictors) == 0:
        return {'verdict': 'Cannot test (no complete predictors)', 'predictors': []}

    X = sm.add_constant(df_test[predictors].dropna())
    y = df_test.loc[X.index, '_missing']

    try:
        model = sm.Logit(y, X).fit(disp=0)
        sig_predictors = [p for p in predictors if model.pvalues[p] < 0.05]

        return {
            'verdict': 'MAR likely' if sig_predictors else 'No MAR evidence (could be MCAR or MNAR)',
            'predictors': sig_predictors,
            'model_p': round(model.llr_pvalue, 4),
            'details': {p: round(model.pvalues[p], 4) for p in predictors}
        }
    except Exception as e:
        return {'verdict': f'Test failed: {str(e)}', 'predictors': []}
```

### MNAR Assessment Checklist

Since MNAR cannot be statistically tested, use domain knowledge:

1. Is there a plausible reason why the value itself would predict its own missingness?
2. Would people with extreme values (very high or very low) be more likely to not respond?
3. Is attrition related to the outcome being measured?
4. Does the literature in this field report MNAR concerns?

If you suspect MNAR, conduct a sensitivity analysis comparing results under different assumptions.

---

## 3. Missing Data Strategies

### Strategy Decision Tree

```
Missing data detected
    |
    +-- Missing % < 5%?
    |   +-- Yes --> Little's MCAR test passed?
    |   |           +-- Yes --> Listwise deletion (simplest, unbiased)
    |   |           +-- No  --> Multiple imputation (to be safe)
    |   +-- No  --> Missing % < 20%?
    |               +-- Yes --> Multiple imputation (m = 5-20)
    |               +-- No  --> Missing % < 50%?
    |                           +-- Yes --> MI (m = 20+) + sensitivity analysis
    |                           +-- No  --> STOP — MISSING_DATA_EXTREME
    |                                       Consider dropping variable
```

### Listwise Deletion

**When**: MCAR confirmed, < 5% missing

```python
df_complete = df.dropna(subset=key_variables)
n_dropped = len(df) - len(df_complete)
print(f"Dropped {n_dropped} cases ({n_dropped/len(df)*100:.1f}%)")
```

**Advantages**: Simple, unbiased under MCAR, all standard analyses apply
**Disadvantages**: Loses data, reduces power, biased if not MCAR

### Pairwise Deletion

**When**: MCAR, correlation/covariance analyses where different analyses use different variable subsets

```python
# Default behavior in pandas correlations
corr_matrix = df[variables].corr()  # Uses pairwise complete observations
```

**Advantages**: Uses all available data for each pair
**Disadvantages**: Different N for each correlation, can produce non-positive-definite matrices

### Multiple Imputation (MI)

**When**: MAR mechanism, > 5% missing, parametric assumptions needed

```python
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer
import numpy as np

def multiple_imputation(df, n_imputations=5, random_state=42):
    """
    Perform multiple imputation using MICE (chained equations).
    Returns list of imputed datasets.
    """
    numeric_cols = df.select_dtypes(include='number').columns.tolist()

    imputed_datasets = []
    for i in range(n_imputations):
        imputer = IterativeImputer(
            max_iter=50,
            random_state=random_state + i,
            sample_posterior=True,  # Important for proper MI
            n_nearest_features=None
        )
        df_imputed = df.copy()
        df_imputed[numeric_cols] = imputer.fit_transform(df[numeric_cols])
        imputed_datasets.append(df_imputed)

    return imputed_datasets
```

#### Rubin's Rules for Pooling MI Results

After running the analysis on each imputed dataset, combine results using Rubin's rules:

```python
def pool_estimates(estimates, variances, m):
    """
    Pool parameter estimates from m imputed datasets using Rubin's rules.
    estimates: list of m point estimates
    variances: list of m variance estimates (SE^2)
    """
    estimates = np.array(estimates)
    variances = np.array(variances)

    # Pooled estimate: mean of estimates
    Q_bar = np.mean(estimates)

    # Within-imputation variance
    U_bar = np.mean(variances)

    # Between-imputation variance
    B = np.var(estimates, ddof=1)

    # Total variance
    T = U_bar + (1 + 1/m) * B

    # Pooled SE
    SE = np.sqrt(T)

    # Degrees of freedom (Barnard-Rubin adjustment)
    r = (1 + 1/m) * B / U_bar
    df_old = (m - 1) * (1 + 1/r)**2

    return {
        'estimate': round(Q_bar, 4),
        'se': round(SE, 4),
        'df': round(df_old, 2),
        't': round(Q_bar / SE, 4),
        'p': round(2 * (1 - stats.t.cdf(abs(Q_bar / SE), df_old)), 4)
    }
```

#### How Many Imputations?

| Missing % | Recommended m |
|-----------|---------------|
| < 10% | 5 |
| 10-30% | 10-20 |
| 30-50% | 20-40 |
| > 50% | Not recommended — consider dropping variable |

### Full Information Maximum Likelihood (FIML)

**When**: MAR mechanism, SEM/CFA models (semopy and lavaan support FIML natively)

```python
# FIML is built into semopy's Model.fit() method
from semopy import Model
model = Model(specification)
model.fit(df)  # Handles missing data via FIML automatically
```

**Advantages**: No separate imputation step, uses all available data, efficient for SEM
**Disadvantages**: Only works within likelihood-based frameworks (SEM, latent variable models)

### Mean/Median Imputation (NOT RECOMMENDED)

**When**: Almost never. Included for completeness and to document why NOT to use it.

**Problems**:
1. Reduces variance (all imputed values are identical)
2. Distorts correlations (attenuates relationships)
3. Underestimates standard errors
4. Biased unless data is MCAR with negligible missingness

If a client insists, document the bias caveat prominently in the report.

---

## 4. Sensitivity Analysis for MNAR

When MNAR is suspected, compare results across multiple assumptions:

```python
def sensitivity_analysis_mnar(df, target_var, analysis_fn, delta_values=[-1, -0.5, 0, 0.5, 1]):
    """
    Pattern-mixture sensitivity analysis.
    Impute missing values with different delta shifts to assess MNAR impact.
    delta_values: shifts to apply to imputed values (in SD units)
    """
    results = []
    sd = df[target_var].std()

    for delta in delta_values:
        df_shifted = df.copy()
        # Impute with MI, then shift imputed values
        imputer = IterativeImputer(random_state=42)
        numeric = df_shifted.select_dtypes(include='number')
        imputed = imputer.fit_transform(numeric)
        df_shifted[numeric.columns] = imputed

        # Apply delta shift only to originally missing values
        missing_mask = df[target_var].isnull()
        df_shifted.loc[missing_mask, target_var] += delta * sd

        # Run analysis
        result = analysis_fn(df_shifted)
        result['delta'] = delta
        results.append(result)

    return pd.DataFrame(results)
```

---

## 5. Reporting Requirements

### APA 7 Reporting Standards for Missing Data

Every analysis report MUST include:

1. **Amount of missing data**: Per variable and total
2. **Pattern**: Monotone, arbitrary, or specific patterns
3. **Mechanism assessment**: MCAR test results and reasoning
4. **Strategy used**: What was done and why
5. **Impact on sample size**: Original N vs analyzed N
6. **Sensitivity**: If MNAR suspected, results under alternative assumptions

### Example Reporting Paragraph

```
Of the 200 participants, 12 (6%) had incomplete data. Missing data
ranged from 0% to 8.5% per variable (highest: anxiety score). Little's
MCAR test was not significant, chi-sq(14) = 18.23, p = .198, supporting
the MCAR assumption. Given the low overall missingness (< 10%) and
MCAR support, listwise deletion was applied, yielding a final analysis
sample of N = 188.
```

### Example for MI Reporting

```
Missing data ranged from 3% to 18% across variables. Little's MCAR test
was significant, chi-sq(22) = 41.56, p = .007, suggesting the data were
not MCAR. Logistic regression analyses indicated that missingness on the
anxiety measure was predicted by age (OR = 1.04, p = .023), consistent
with a MAR mechanism. Multiple imputation was performed using chained
equations (m = 20 imputations, 50 iterations per imputation) with all
analysis variables included in the imputation model. Results were pooled
using Rubin's rules.
```

---

## 6. Common Pitfalls

| Pitfall | Problem | Solution |
|---------|---------|----------|
| Assuming MCAR without testing | Biased results if MAR/MNAR | Always run Little's test |
| Using mean imputation | Artificially reduces variance | Use MI or FIML |
| Ignoring missing data | Reduces power, may introduce bias | Document and handle explicitly |
| Imputing the outcome variable | Can bias effect estimates | Impute predictors; analyze outcome as-is |
| Too few imputations | Unstable pooled estimates | Use m >= percentage of missing data |
| Not including outcome in imputation model | Biases imputed values | Include all analysis variables in MI model |
| Dropping high-missingness variables without consideration | May lose important information | Assess whether variable is essential; consider auxiliary variables |
