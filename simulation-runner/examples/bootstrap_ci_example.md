# Example: Bootstrap Confidence Intervals — BCa CIs for Median Difference

## User Request

```
Bootstrap 95% BCa confidence intervals for the median difference between
Group A and Group B. The data is in experiment_outputs/data/group_comparison.csv
and I suspect the distributions are skewed.
```

## Phase 1: INTAKE

### intake_agent Output

```markdown
## Simulation Brief

**Simulation ID**: SIM-20260316-002
**Experiment ID**: AD-HOC
**Mode**: bootstrap
**Simulation Type**: bootstrap

### Source
- Input type: Data file
- Schema version: N/A

### Model Summary
- Description: Bias-corrected and accelerated (BCa) bootstrap confidence intervals
  for the difference in medians between two independent groups.
- DGP: Nonparametric resampling with replacement from observed data.
- Key parameters: n_bootstrap = 10,000, confidence_level = 0.95, method = BCa
- Distributions: Empirical (resampling from observed data)

### Data File
- Path: experiment_outputs/data/group_comparison.csv
- Rows: 87 total (Group A: 42, Group B: 45)
- Columns used: group (A/B), score
- Validation: passed
  - n >= 20 per group: Yes
  - No missing values in target columns
  - Score column is numeric

### Execution Plan
- Bootstrap resamples: 10,000
- Chains: N/A (bootstrap is i.i.d.)
- Burn-in: N/A
- Convergence criterion: MCSE of CI bounds < 1% of CI width
- Parallelization: yes, all available cores
- Estimated runtime: ~30 seconds

### Performance Measures
- Median difference: median(A) - median(B)
- BCa 95% CI: bias-corrected and accelerated percentile interval
- Percentile 95% CI: for comparison
- Bootstrap SE: standard deviation of bootstrap distribution

### ADEMP Summary
- **Aims**: Estimate the median difference between Group A and Group B with
  BCa confidence interval, accounting for potential skewness.
- **DGP**: Nonparametric resampling from observed data (87 observations).
- **Estimands**: Median difference, BCa 95% CI bounds.
- **Methods**: BCa bootstrap (Efron, 1987).
- **Performance**: MCSE of CI bounds, comparison of BCa vs percentile intervals.

### Environment
- Python: 3.12.3
- Key packages: numpy 1.26.4, scipy 1.13.0
- Venv path: experiment_env/
```

## Phase 2: MODEL BUILDING

### model_builder_agent Output

#### Data Loading and Inspection

```python
import numpy as np
import pandas as pd

# Load data
data = pd.read_csv('experiment_outputs/data/group_comparison.csv')
group_a = data[data['group'] == 'A']['score'].values
group_b = data[data['group'] == 'B']['score'].values

# Descriptive statistics
print(f"Group A: n={len(group_a)}, median={np.median(group_a):.2f}, "
      f"mean={np.mean(group_a):.2f}, skewness={scipy.stats.skew(group_a):.2f}")
print(f"Group B: n={len(group_b)}, median={np.median(group_b):.2f}, "
      f"mean={np.mean(group_b):.2f}, skewness={scipy.stats.skew(group_b):.2f}")

# Output (example):
# Group A: n=42, median=23.50, mean=26.31, skewness=1.24
# Group B: n=45, median=20.08, mean=21.73, skewness=0.87
# Observed median difference: 3.42
```

The right-skewness of both groups (skewness > 0.5) confirms that the median is a more appropriate measure of central tendency than the mean, and that BCa bootstrap is preferable over percentile bootstrap for interval estimation.

#### Bootstrap Resampling Function

```python
from numpy.random import Generator

def bootstrap_median_diff(group_a: np.ndarray, group_b: np.ndarray,
                          rng: Generator) -> float:
    """
    Compute the median difference on one bootstrap resample.

    Resamples each group independently with replacement,
    then computes median(A*) - median(B*).

    Parameters
    ----------
    group_a : np.ndarray
        Original Group A data.
    group_b : np.ndarray
        Original Group B data.
    rng : Generator
        Random number generator.

    Returns
    -------
    float : bootstrap median difference
    """
    n_a = len(group_a)
    n_b = len(group_b)

    # Resample each group independently
    resample_a = group_a[rng.choice(n_a, size=n_a, replace=True)]
    resample_b = group_b[rng.choice(n_b, size=n_b, replace=True)]

    return np.median(resample_a) - np.median(resample_b)
```

#### BCa Interval Computation

```python
from scipy.stats import norm

def compute_bca_ci(boot_distribution: np.ndarray, observed_stat: float,
                   jackknife_stats: np.ndarray, confidence_level: float = 0.95) -> dict:
    """
    Compute BCa (bias-corrected and accelerated) confidence interval.

    Parameters
    ----------
    boot_distribution : np.ndarray
        Array of bootstrap statistics (length B).
    observed_stat : float
        The statistic computed on the original data.
    jackknife_stats : np.ndarray
        Leave-one-out jackknife statistics (length n) for acceleration.
    confidence_level : float
        Confidence level (default 0.95).

    Returns
    -------
    dict with keys:
        - 'ci_lower': float, lower bound
        - 'ci_upper': float, upper bound
        - 'z0': float, bias correction constant
        - 'a': float, acceleration constant
        - 'percentile_ci': tuple, standard percentile CI for comparison
    """
    B = len(boot_distribution)
    alpha = 1 - confidence_level

    # Bias correction constant (z0)
    # Proportion of bootstrap values below the observed statistic
    prop_below = np.mean(boot_distribution < observed_stat)
    z0 = norm.ppf(prop_below)

    # Acceleration constant (a)
    # From jackknife influence values
    jack_mean = np.mean(jackknife_stats)
    jack_diff = jack_mean - jackknife_stats
    a = np.sum(jack_diff ** 3) / (6 * (np.sum(jack_diff ** 2)) ** 1.5)

    # Adjusted percentiles
    z_alpha_lower = norm.ppf(alpha / 2)
    z_alpha_upper = norm.ppf(1 - alpha / 2)

    # BCa adjusted quantiles
    adj_lower = norm.cdf(z0 + (z0 + z_alpha_lower) / (1 - a * (z0 + z_alpha_lower)))
    adj_upper = norm.cdf(z0 + (z0 + z_alpha_upper) / (1 - a * (z0 + z_alpha_upper)))

    # Ensure quantiles are within [0, 1]
    adj_lower = np.clip(adj_lower, 1 / (B + 1), B / (B + 1))
    adj_upper = np.clip(adj_upper, 1 / (B + 1), B / (B + 1))

    sorted_boot = np.sort(boot_distribution)
    ci_lower = np.percentile(boot_distribution, adj_lower * 100)
    ci_upper = np.percentile(boot_distribution, adj_upper * 100)

    # Standard percentile CI for comparison
    pct_lower = np.percentile(boot_distribution, (alpha / 2) * 100)
    pct_upper = np.percentile(boot_distribution, (1 - alpha / 2) * 100)

    return {
        'ci_lower': ci_lower,
        'ci_upper': ci_upper,
        'z0': z0,
        'a': a,
        'percentile_ci': (pct_lower, pct_upper),
    }


def compute_jackknife_median_diff(group_a: np.ndarray, group_b: np.ndarray) -> np.ndarray:
    """
    Compute leave-one-out jackknife statistics for the median difference.

    Removes one observation at a time from the combined dataset,
    recalculates the median difference.
    """
    n_a = len(group_a)
    n_b = len(group_b)
    n_total = n_a + n_b
    combined = np.concatenate([group_a, group_b])
    group_labels = np.array(['A'] * n_a + ['B'] * n_b)

    jack_stats = np.zeros(n_total)
    for i in range(n_total):
        mask = np.ones(n_total, dtype=bool)
        mask[i] = False
        remaining = combined[mask]
        remaining_labels = group_labels[mask]
        jack_a = remaining[remaining_labels == 'A']
        jack_b = remaining[remaining_labels == 'B']
        jack_stats[i] = np.median(jack_a) - np.median(jack_b)

    return jack_stats
```

## Phase 3: EXECUTION

### execution_engine_agent Output

```markdown
## Execution Results

**Simulation ID**: SIM-20260316-002
**Status**: Converged

### Execution Summary
- Bootstrap resamples completed: 10,000
- Jackknife leave-one-out: 87 iterations (for acceleration constant)
- Early stopped: No (all 10,000 completed)
- Wall time: 24 seconds
- Peak memory: 180 MB
- Workers used: 8

### Bootstrap Distribution Summary
- Observed median difference: 3.42
- Bootstrap mean of median difference: 3.38
- Bootstrap SE: 1.76
- Bootstrap distribution skewness: 0.34
- Bootstrap distribution kurtosis: 3.12

### BCa Constants
- Bias correction (z0): 0.021
- Acceleration (a): 0.015

### Confidence Intervals
| Method | 95% CI Lower | 95% CI Upper | Width |
|--------|-------------|-------------|-------|
| BCa | 1.87 | 5.23 | 3.36 |
| Percentile | 1.62 | 5.01 | 3.39 |
| Normal approx | -0.03 | 6.87 | 6.90 |

### Convergence
| Metric | Value | Threshold | Verdict |
|--------|-------|-----------|---------|
| MCSE (median diff) | 0.018 | < 0.05 | Pass |
| MCSE (CI lower) | 0.031 | < 0.034 (1% of CI width) | Pass |
| MCSE (CI upper) | 0.028 | < 0.034 (1% of CI width) | Pass |
| R-hat | N/A | N/A | N/A (i.i.d. bootstrap) |
| ESS | 10,000 | > 400 | Pass |

### Seed Log
Master Seed: 42
Method: SeedSequence.spawn(10,000) — one RNG per bootstrap resample
```

## Phase 4: DIAGNOSTICS

### diagnostics_agent Output

```markdown
## Convergence Report

**Simulation ID**: SIM-20260316-002
**Overall Verdict**: CONVERGED

### Bootstrap Distribution Assessment
The bootstrap distribution of the median difference is unimodal and moderately
right-skewed (skewness = 0.34). This skewness confirms the appropriateness of
the BCa correction over the standard percentile method.

### CI Method Comparison
| Method | 95% CI | Width | Notes |
|--------|--------|-------|-------|
| BCa | [1.87, 5.23] | 3.36 | Recommended: adjusts for bias and skewness |
| Percentile | [1.62, 5.01] | 3.39 | Wider on left; does not correct for skewness |
| Normal approx | [-0.03, 6.87] | 6.90 | Much wider; assumes normality (inappropriate here) |

The BCa interval is shifted rightward relative to the percentile interval,
reflecting the positive bias correction (z0 = 0.021). The acceleration
constant (a = 0.015) is small, indicating modest skewness in the influence
function. The normal approximation interval is substantially wider and
includes zero, illustrating why distribution-free methods are preferred
for skewed data.

### Diagnostic Plots
| Plot | Path | Observation |
|------|------|-------------|
| Bootstrap distribution | experiment_outputs/plots/bootstrap_dist_median_diff.png | Right-skewed, unimodal; observed statistic (3.42) near center |
| Running mean | experiment_outputs/plots/convergence_boot_mean.png | Stabilized by 2,000 resamples |
| Running MCSE | experiment_outputs/plots/convergence_boot_mcse.png | Below threshold by 3,000 resamples |
| QQ plot vs normal | experiment_outputs/plots/qq_bootstrap.png | Departure from normality in upper tail |

### Recommendations
No issues detected. BCa interval is well-estimated with MCSE < 1% of CI width.
```

## Phase 5: REPORTING

### report_compiler_agent Output — Schema 11

```markdown
## Experiment Results

**Experiment ID**: AD-HOC-SIM-20260316-002
**Result Type**: bootstrap

**Dataset Info**:
- Original N: 87 (Group A: 42, Group B: 45)
- Analyzed N: 87 (no exclusions)
- Missing strategy: No missing values

**Assumption Checks**:
| Assumption | Test | Statistic | p | Verdict | Action |
|------------|------|-----------|---|---------|--------|
| Convergence (MCSE) | Running MCSE | 0.018 | N/A | Met | Proceed |
| Normality (Group A) | Shapiro-Wilk | W = 0.91 | .003 | Violated | Use BCa (not normal CI) |
| Normality (Group B) | Shapiro-Wilk | W = 0.93 | .012 | Violated | Use BCa (not normal CI) |

**Primary Results**:
- Observed median difference (A - B): 3.42
- BCa bootstrap 95% CI: [1.87, 5.23]
- Bootstrap SE: 1.76
- MCSE: 0.018

**Effect Sizes**:
| Measure | Value | CI Lower | CI Upper | Magnitude |
|---------|-------|----------|----------|-----------|
| Median difference | 3.42 | 1.87 | 5.23 | — |
| Hodges-Lehmann estimator | 3.28 | 1.65 | 5.05 | — |

**Tables**:
| ID | Caption | CSV Path |
|----|---------|----------|
| Table 1 | Descriptive statistics by group | experiment_outputs/results/descriptives.csv |
| Table 2 | Bootstrap CI comparison (BCa, percentile, normal) | experiment_outputs/results/ci_comparison.csv |

**Figures**:
| ID | Caption | PNG Path |
|----|---------|----------|
| Figure 1 | Bootstrap distribution of median difference | experiment_outputs/plots/bootstrap_dist_median_diff.png |
| Figure 2 | Group score distributions (histograms with medians) | experiment_outputs/plots/group_distributions.png |

**APA Results Text**:
- Primary: see below

**Reproducibility**:
- Script: experiment_outputs/scripts/simulation_SIM-20260316-002.py
- Seed: 42
- Environment: experiment_env/requirements.txt
```

### APA Results Text

> Bias-corrected and accelerated (BCa) bootstrap confidence intervals were computed for the median difference between Group A and Group B using 10,000 bootstrap resamples (master seed = 42). Both groups exhibited significant positive skewness (Group A: skewness = 1.24, *W* = .91, *p* = .003; Group B: skewness = 0.87, *W* = .93, *p* = .012), supporting the use of the median rather than the mean as the primary measure of central tendency, and BCa bootstrap rather than parametric confidence intervals.
>
> The observed median score was 23.50 for Group A (*n* = 42) and 20.08 for Group B (*n* = 45), yielding a median difference of 3.42. The BCa 95% bootstrap confidence interval was [1.87, 5.23], indicating a statistically significant difference that excludes zero. The bootstrap distribution was moderately right-skewed (skewness = 0.34), and the BCa correction constants were small (bias correction *z*0 = 0.021, acceleration *a* = 0.015). For comparison, the standard percentile interval [1.62, 5.01] was similar but did not account for the distributional asymmetry, while the normal approximation interval [-0.03, 6.87] was substantially wider and inappropriately included zero.
>
> Convergence diagnostics confirmed adequate bootstrap precision: MCSE for the median difference was 0.018, and MCSE for both CI bounds was less than 1% of the CI width. The complete simulation code and data are available at the referenced script path for independent replication.

### Material Passport

```markdown
## Material Passport

- Origin Skill: simulation-runner
- Origin Mode: bootstrap
- Origin Date: 2026-03-16T15:00:00Z
- Verification Status: UNVERIFIED
- Version Label: sim_results_v1
- Upstream Dependencies: [group_comparison.csv]
```

### Key Takeaways from This Example

1. **BCa vs. Percentile**: The BCa interval accounts for bias and skewness in the bootstrap distribution. For skewed data, it provides more accurate coverage than the percentile method.
2. **Normal approximation failure**: The normal approximation CI is nearly twice as wide and includes zero, demonstrating why it is inappropriate for skewed data.
3. **Convergence for bootstrap**: Since bootstrap resamples are i.i.d., convergence is straightforward — MCSE decreases as 1/sqrt(B). R-hat is not applicable.
4. **Jackknife for acceleration**: The acceleration constant requires a separate jackknife computation (n leave-one-out iterations), which adds minimal computation for moderate n.
5. **Data validation**: The intake_agent verified the data file before proceeding, confirming sufficient sample size and no missing values.
