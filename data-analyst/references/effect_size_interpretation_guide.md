# Effect Size Interpretation Guide — Benchmarks, CIs, and Practical Significance

## Purpose

Reference guide for interpreting effect sizes in context. Covers Cohen's conventions, domain-specific benchmarks, confidence interval computation, and practical significance assessment. Used primarily by `effect_size_agent` and `report_compiler_agent`.

---

## 1. Cohen's Conventions (General Benchmarks)

Jacob Cohen (1988) provided benchmarks for interpreting effect sizes when no domain-specific norms are available. These are defaults, not absolutes.

### Standardized Mean Differences

| Measure | Small | Medium | Large |
|---------|-------|--------|-------|
| Cohen's *d* | 0.20 | 0.50 | 0.80 |
| Hedges' *g* | 0.20 | 0.50 | 0.80 |
| Glass's delta | 0.20 | 0.50 | 0.80 |

**Common Language Effect Size (CLES)**: The probability that a randomly selected person from one group scores higher than a randomly selected person from the other group.

| *d* | CLES |
|-----|------|
| 0.00 | 50% |
| 0.20 | 56% |
| 0.50 | 64% |
| 0.80 | 71% |
| 1.00 | 76% |
| 1.50 | 86% |
| 2.00 | 92% |

### Variance-Explained Measures

| Measure | Small | Medium | Large |
|---------|-------|--------|-------|
| eta-squared (eta-sq) | .01 | .06 | .14 |
| Partial eta-squared | .01 | .06 | .14 |
| Omega-squared (omega-sq) | .01 | .06 | .14 |
| *R*-squared | .02 | .13 | .26 |
| Cohen's *f*-squared | .02 | .15 | .35 |

### Correlation-Based Measures

| Measure | Small | Medium | Large |
|---------|-------|--------|-------|
| Pearson *r* | .10 | .30 | .50 |
| Spearman rho | .10 | .30 | .50 |
| Point-biserial *r* | .10 | .30 | .50 |

### Categorical Measures

| Measure | Small | Medium | Large |
|---------|-------|--------|-------|
| Cramer's *V* (df* = 1) | .10 | .30 | .50 |
| Cramer's *V* (df* = 2) | .07 | .21 | .35 |
| Cramer's *V* (df* = 3) | .06 | .17 | .29 |
| Phi | .10 | .30 | .50 |
| Odds Ratio | 1.5 | 2.5 | 4.0 |

*df* = min(rows - 1, cols - 1) for the contingency table

### Risk-Based Measures

| Measure | Small | Medium | Large |
|---------|-------|--------|-------|
| Relative Risk (RR) | 1.2-1.5 | 1.5-3.0 | > 3.0 |
| Hazard Ratio (HR) | 1.2-1.5 | 1.5-3.0 | > 3.0 |
| Number Needed to Treat (NNT) | > 10 | 4-10 | < 4 |

---

## 2. Domain-Specific Benchmarks

Cohen's conventions are starting points. In many fields, domain-specific norms provide better context.

### Education

| Source | Benchmark | Notes |
|--------|-----------|-------|
| Hattie (2009) | *d* > 0.40 = "zone of desired effects" | Based on 800+ meta-analyses |
| Hattie (2009) | *d* = 0.20 = "average teacher effect" | Baseline for what typical teaching produces |
| Hattie (2009) | *d* > 0.60 = "excellent effect" | Top-tier interventions |
| Kraft (2020) | *d* < 0.05 = negligible in RCTs | Specific to education RCTs |
| Kraft (2020) | *d* = 0.05-0.20 = typical education intervention | Most education RCTs fall here |
| Lipsey et al. (2012) | *d* = 0.20-0.30 = typical for educational programs | More realistic than Cohen's "small" |

### Clinical Psychology / Mental Health

| Source | Benchmark | Notes |
|--------|-----------|-------|
| Kazdin (1999) | *d* > 0.50 = clinically meaningful | Minimum for practical importance |
| Jacobson & Truax (1991) | Reliable Change Index > 1.96 | Clinical significance criterion |
| NICE guidelines | *d* = 0.50 = threshold for clinical recommendation | UK treatment guidelines |

### Medicine / Public Health

| Source | Benchmark | Notes |
|--------|-----------|-------|
| OR < 1.5 | Weak association | Potential confounding |
| OR = 1.5-3.0 | Moderate association | Worth investigating |
| OR > 3.0 | Strong association | Likely real effect |
| RR > 2.0 | Clinically significant | Standard epidemiological threshold |
| NNT < 10 | Practically useful treatment | Lower is better |

### Organizational / Industrial Psychology

| Source | Benchmark | Notes |
|--------|-----------|-------|
| Bosco et al. (2015) | *r* = .09 = 25th percentile | Based on 250,000+ correlations |
| Bosco et al. (2015) | *r* = .16 = 50th percentile (median) | |
| Bosco et al. (2015) | *r* = .27 = 75th percentile | |
| Meyer et al. (2001) | *r* > .20 = practically meaningful | Operational validity |

### Social Psychology

| Source | Benchmark | Notes |
|--------|-----------|-------|
| Richard et al. (2003) | *r* = .21 = typical effect | Mean of 474 meta-analyses |
| Funder & Ozer (2019) | *r* = .05 = very small | |
| Funder & Ozer (2019) | *r* = .10 = small | |
| Funder & Ozer (2019) | *r* = .20 = medium | |
| Funder & Ozer (2019) | *r* = .30 = large | |
| Funder & Ozer (2019) | *r* > .40 = very large | Rare in social psychology |

---

## 3. Confidence Interval Computation

### Why CIs Matter More Than Point Estimates

- A point estimate (e.g., *d* = 0.50) is a single best guess
- The CI tells you the range of plausible values given the data
- A wide CI means low precision (small sample or high variability)
- If the CI includes zero, the effect is not statistically significant

### Analytical CIs

#### CI for Cohen's d

```python
import numpy as np
from scipy import stats

def ci_cohens_d(d, n1, n2, confidence=0.95):
    """Compute CI for Cohen's d using non-central t distribution."""
    se = np.sqrt(n1 + n2) / np.sqrt(n1 * n2) + d**2 / (2 * (n1 + n2))
    se = np.sqrt(se)
    z = stats.norm.ppf(1 - (1 - confidence) / 2)
    return (round(d - z * se, 4), round(d + z * se, 4))
```

#### CI for r (Fisher's z transformation)

```python
def ci_correlation(r, n, confidence=0.95):
    """Compute CI for Pearson r using Fisher's z."""
    z_r = np.arctanh(r)
    se_z = 1 / np.sqrt(n - 3)
    z_crit = stats.norm.ppf(1 - (1 - confidence) / 2)
    z_lower = z_r - z_crit * se_z
    z_upper = z_r + z_crit * se_z
    return (round(np.tanh(z_lower), 4), round(np.tanh(z_upper), 4))
```

#### CI for Odds Ratio

```python
def ci_odds_ratio(or_val, se_log_or, confidence=0.95):
    """Compute CI for odds ratio."""
    z = stats.norm.ppf(1 - (1 - confidence) / 2)
    log_or = np.log(or_val)
    return (round(np.exp(log_or - z * se_log_or), 4),
            round(np.exp(log_or + z * se_log_or), 4))
```

### Bootstrap CIs (When Analytical Formulas Unavailable)

Use bootstrap when analytical CIs are not available (e.g., eta-squared, Cramer's V, mediation indirect effects).

```python
def bootstrap_ci(data, statistic_fn, n_boot=2000, confidence=0.95, seed=42):
    """
    Compute bootstrap CI for any statistic.
    statistic_fn: function that takes a resampled dataset and returns a scalar
    """
    np.random.seed(seed)
    boot_stats = []
    for _ in range(n_boot):
        idx = np.random.choice(len(data), size=len(data), replace=True)
        boot_sample = data.iloc[idx] if hasattr(data, 'iloc') else data[idx]
        boot_stats.append(statistic_fn(boot_sample))

    alpha = 1 - confidence
    lower = np.percentile(boot_stats, 100 * alpha / 2)
    upper = np.percentile(boot_stats, 100 * (1 - alpha / 2))
    return (round(lower, 4), round(upper, 4))
```

---

## 4. When Benchmarks Mislead

### Problem 1: One-Size-Fits-All Thinking

Cohen himself warned: "The terms 'small', 'medium', and 'large' are relative... to each other and to the context" (Cohen, 1988, p. 25). A *d* = 0.20 may be:
- **Trivial** for an expensive educational intervention
- **Enormous** for a low-cost public health intervention affecting millions

### Problem 2: Confusing Statistical and Practical Significance

| Scenario | Statistical | Practical | Interpretation |
|----------|------------|-----------|----------------|
| Large N, tiny effect | p < .001, d = 0.05 | Negligible | Statistically significant but practically meaningless |
| Small N, large effect | p = .08, d = 0.75 | Substantial | Not significant but potentially important (underpowered) |
| Moderate N, moderate effect | p = .01, d = 0.50 | Moderate | Both statistically and practically meaningful |

### Problem 3: Eta-Squared Inflation

Eta-squared is positively biased (overestimates population effect). For small samples:
- Report omega-squared alongside eta-squared
- Note the bias in the report
- Omega-squared = (SS_between - df_between * MS_within) / (SS_total + MS_within)

### Problem 4: Context Dependency

Consider these questions:
1. **What is the cost of the intervention?** A small effect from a cheap intervention may be more valuable than a large effect from an expensive one
2. **What is the base rate?** A small effect on a common outcome affects many people
3. **What are the consequences?** A small effect on mortality matters more than a large effect on satisfaction
4. **Is the effect cumulative?** Small daily effects compound over time

---

## 5. Practical Significance Interpretation Framework

For each effect size, answer these questions:

### Step 1: Classify Magnitude

Use domain-specific benchmarks if available; Cohen's conventions as fallback.

### Step 2: Compute CLES (for d)

"The average person in group A scores higher than X% of people in group B."

### Step 3: Translate to Concrete Units

Convert the effect size to the original measurement scale when possible:
- *d* = 0.50 on a 100-point exam = approximately 5-point difference (if SD = 10)
- *r* = .30 with GPA (SD = 0.5) = roughly 0.15 GPA points per SD of predictor

### Step 4: Compare to Published Benchmarks

- What do similar studies in this field typically find?
- Is this effect larger or smaller than established interventions?

### Step 5: Assess Precision

- Is the CI narrow (precise estimate) or wide (imprecise)?
- Does the CI include zero? Trivially small values? Meaningfully large values?

### Step 6: Consider the Stakes

- Who is affected? How many people?
- What are the costs and benefits?
- Is the effect actionable?

---

## 6. Reporting Effect Sizes: Best Practices

1. **Always report effect sizes** — APA requires them for all primary results
2. **Always include CIs** — a point estimate alone is incomplete
3. **Use the most appropriate measure** — d for group comparisons, r or R-sq for relationships, OR for categorical
4. **Report multiple measures when informative** — e.g., both eta-squared and omega-squared
5. **Interpret in context** — use domain-specific benchmarks, not just Cohen's labels
6. **Address practical significance explicitly** — do not let readers conflate statistical significance with importance
7. **Report non-significant effect sizes** — small or zero effects are informative
8. **Use forest plots** — when reporting multiple effect sizes, a visual summary aids interpretation
