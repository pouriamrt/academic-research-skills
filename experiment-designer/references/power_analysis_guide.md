# Power Analysis Guide — Core Concepts, Python Code, and Common Pitfalls

## Purpose

A comprehensive reference for statistical power analysis. Covers the theoretical foundations, effect size conventions, Python code examples using statsmodels and scipy, power curve generation, and common pitfalls. Used by the power_analyst_agent.

---

## Core Concepts

### The Four Parameters

Every power analysis involves four interdependent parameters. Given any three, you can solve for the fourth.

```
                     +-- alpha (Type I error rate)
                     |
Statistical Power <--+-- power (1 - Type II error rate)
                     |
                     +-- effect size (magnitude of the true effect)
                     |
                     +-- N (sample size)
```

| Parameter | Symbol | Definition | Typical Values |
|-----------|--------|-----------|---------------|
| Alpha | alpha | Probability of rejecting H0 when H0 is true (false positive) | 0.05 (standard), 0.01 (conservative), 0.005 (stringent) |
| Power | 1 - beta | Probability of rejecting H0 when H1 is true (correctly detecting a real effect) | 0.80 (standard), 0.90 (clinical), 0.95 (confirmatory) |
| Effect size | d, f, r, etc. | Standardized magnitude of the difference or relationship | Depends on metric and context |
| Sample size | N | Number of observations (total or per group) | Solved from the other three |

### The Relationship

```
Power INCREASES when:
  - Effect size increases (larger effects are easier to detect)
  - N increases (more data = more precision)
  - Alpha increases (accepting more false positives makes it easier to detect true positives)

Power DECREASES when:
  - Effect size decreases
  - N decreases
  - Alpha decreases (more stringent threshold)
  - Variance increases (noisier data)
```

### Type I vs Type II Error Trade-off

```
                    Reality
                    H0 True         H1 True
Decision:
  Reject H0       Type I Error     Correct (Power)
                   (alpha)         (1 - beta)

  Fail to         Correct          Type II Error
  Reject H0       (1 - alpha)      (beta)
```

---

## Effect Size Conventions

### Cohen's (1988) Benchmarks

| Metric | Small | Medium | Large | Typical Use |
|--------|-------|--------|-------|-------------|
| d | 0.20 | 0.50 | 0.80 | Two-group mean comparisons |
| f | 0.10 | 0.25 | 0.40 | ANOVA (omnibus F-test) |
| r | 0.10 | 0.30 | 0.50 | Correlations |
| f-squared | 0.02 | 0.15 | 0.35 | Regression (R-squared change) |
| w | 0.10 | 0.30 | 0.50 | Chi-square tests |
| eta-squared | 0.01 | 0.06 | 0.14 | ANOVA effect sizes |
| partial eta-sq | 0.01 | 0.06 | 0.14 | Factorial ANOVA |

### Important Caveats

1. **Conventions are benchmarks, not justifications**: "I used d = 0.5 because it is a medium effect" is NOT adequate justification for a power analysis. Use:
   - **Prior meta-analysis**: Best source. Report k (number of studies) and total N
   - **Prior empirical study**: Report N, design, and whether the study was well-powered
   - **Pilot data**: Small N, wide confidence interval — treat as rough estimate
   - **SESOI (Smallest Effect Size of Interest)**: What is the minimum effect that would be practically meaningful? This is often the best approach for applied research

2. **Publication bias inflates effect sizes**: Published studies have systematically larger effect sizes than the true population effect (winner's curse). Apply a shrinkage factor (e.g., reduce published d by 20-30%) when using published studies as the source.

3. **Effect sizes are domain-specific**: A "small" effect in clinical psychology (d = 0.2) may be very meaningful for a public health intervention applied to millions of people.

---

## Python Code Examples

### Setup

```python
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.stats.power import (
    TTestIndPower,
    TTestPower,
    FTestAnovaPower,
    FTestPower,
    GofChisquarePower,
    NormalIndPower
)
from scipy import stats
```

### 1. Independent Samples t-test

```python
# How many participants per group for a medium effect?
analysis = TTestIndPower()

# Solve for N
n = analysis.solve_power(
    effect_size=0.50,     # Cohen's d = 0.50 (medium)
    alpha=0.05,           # Two-tailed alpha
    power=0.80,           # 80% power
    ratio=1.0,            # Equal groups (n2/n1)
    alternative='two-sided'
)
print(f"Required N per group: {int(np.ceil(n))}")
# Output: Required N per group: 64

# Solve for power (given N)
power = analysis.solve_power(
    effect_size=0.50,
    nobs1=50,
    alpha=0.05,
    ratio=1.0,
    alternative='two-sided'
)
print(f"Power with N=50 per group: {power:.3f}")

# Solve for minimum detectable effect size (given N and power)
min_d = analysis.solve_power(
    effect_size=None,
    nobs1=50,
    alpha=0.05,
    power=0.80,
    ratio=1.0,
    alternative='two-sided'
)
print(f"Minimum detectable d with N=50: {min_d:.3f}")
```

### 2. Paired Samples t-test

```python
analysis = TTestPower()

n = analysis.solve_power(
    effect_size=0.50,
    alpha=0.05,
    power=0.80,
    alternative='two-sided'
)
print(f"Required N (pairs): {int(np.ceil(n))}")
# Output: Required N (pairs): 34
# Note: Paired designs need fewer participants than independent designs
```

### 3. One-Way ANOVA (3+ groups)

```python
analysis = FTestAnovaPower()

# Cohen's f = 0.25 (medium), 3 groups
n_per_group = analysis.solve_power(
    effect_size=0.25,
    alpha=0.05,
    power=0.80,
    k_groups=3
)
print(f"Required N per group: {int(np.ceil(n_per_group))}")
print(f"Total N: {int(np.ceil(n_per_group)) * 3}")
# Output: Required N per group: 53, Total N: 159

# For 4 groups
n_per_group_4 = analysis.solve_power(
    effect_size=0.25,
    alpha=0.05,
    power=0.80,
    k_groups=4
)
print(f"Required N per group (4 groups): {int(np.ceil(n_per_group_4))}")
print(f"Total N: {int(np.ceil(n_per_group_4)) * 4}")
```

### 4. Multiple Regression (F-test for R-squared change)

```python
analysis = FTestPower()

# Testing 3 predictors, f-squared = 0.15 (medium)
f_squared = 0.15
f = np.sqrt(f_squared)

# df_num = number of predictors being tested
# We solve for df_denom (= N - total_predictors - 1)
df_denom = analysis.solve_power(
    effect_size=f,
    df_num=3,         # Testing 3 predictors
    alpha=0.05,
    power=0.80
)
total_predictors = 5  # Total predictors in the model
total_n = int(np.ceil(df_denom)) + total_predictors + 1
print(f"Required total N: {total_n}")
```

### 5. Chi-Square Test (Goodness of Fit)

```python
analysis = GofChisquarePower()

n = analysis.solve_power(
    effect_size=0.30,    # Cohen's w = 0.30 (medium)
    alpha=0.05,
    power=0.80,
    n_bins=4             # Number of categories
)
print(f"Required total N: {int(np.ceil(n))}")
```

### 6. Chi-Square Test (Independence)

```python
# For a 2x3 contingency table, df = (2-1)(3-1) = 2
# n_bins for independence test = df + 1
analysis = GofChisquarePower()

n = analysis.solve_power(
    effect_size=0.30,
    alpha=0.05,
    power=0.80,
    n_bins=3             # df + 1 = 2 + 1 = 3
)
print(f"Required total N: {int(np.ceil(n))}")
```

### 7. Correlation (Pearson r)

```python
# Use Fisher's z transformation
analysis = NormalIndPower()

r = 0.30
z = np.arctanh(r)  # Fisher's z

n = analysis.solve_power(
    effect_size=z,
    alpha=0.05,
    power=0.80,
    alternative='two-sided'
)
n_corrected = int(np.ceil(n)) + 3  # +3 for Fisher z correction
print(f"Required N: {n_corrected}")
```

---

## Power Curve Generation

### Standard Power Curve

```python
def generate_power_curve(test_class, effect_sizes, n_range=(10, 200),
                         alpha=0.05, power_target=0.80, title="Power Curve",
                         save_path=None, **solve_kwargs):
    """
    Generate a publication-quality power curve.

    Parameters:
        test_class: statsmodels power class instance
        effect_sizes: list of effect sizes to plot
        n_range: (min, max) sample sizes
        alpha: significance level
        power_target: target power (horizontal line)
        title: figure title
        save_path: path to save figure (PNG, 300 DPI)
        **solve_kwargs: additional kwargs for solve_power
    """
    ns = np.arange(n_range[0], n_range[1] + 1, 2)

    fig, ax = plt.subplots(figsize=(10, 6))

    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']

    for i, d in enumerate(effect_sizes):
        powers = []
        for n in ns:
            try:
                p = test_class.solve_power(
                    effect_size=d, nobs1=n, alpha=alpha,
                    alternative='two-sided', **solve_kwargs
                )
                powers.append(min(p, 1.0))
            except Exception:
                powers.append(np.nan)

        ax.plot(ns, powers, label=f"d = {d:.2f}",
                linewidth=2.5, color=colors[i % len(colors)])

    ax.axhline(y=power_target, color='red', linestyle='--',
               linewidth=1.5, label=f'Target power = {power_target}', alpha=0.7)

    ax.set_xlabel('Sample Size per Group', fontsize=13)
    ax.set_ylabel('Statistical Power (1 - beta)', fontsize=13)
    ax.set_title(title, fontsize=15, fontweight='bold')
    ax.legend(fontsize=11, loc='lower right')
    ax.set_ylim(0, 1.05)
    ax.set_xlim(n_range[0], n_range[1])
    ax.grid(True, alpha=0.3)
    ax.tick_params(labelsize=11)

    plt.tight_layout()

    if save_path:
        fig.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Saved to: {save_path}")

    return fig

# Example usage
analysis = TTestIndPower()
fig = generate_power_curve(
    test_class=analysis,
    effect_sizes=[0.20, 0.35, 0.50, 0.65, 0.80],
    n_range=(10, 150),
    title="Power Curve: Independent Samples t-test",
    save_path="experiment_outputs/figures/power_curve.png"
)
```

### Sensitivity Curve (Effect Size as a Function of N)

```python
def generate_sensitivity_curve(test_class, n_range=(10, 200),
                                alpha=0.05, power_target=0.80,
                                title="Sensitivity Curve", save_path=None):
    """
    Plot minimum detectable effect size as a function of sample size.
    """
    ns = np.arange(n_range[0], n_range[1] + 1, 5)
    min_effects = []

    for n in ns:
        try:
            d = test_class.solve_power(
                effect_size=None, nobs1=n, alpha=alpha,
                power=power_target, alternative='two-sided'
            )
            min_effects.append(d)
        except Exception:
            min_effects.append(np.nan)

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(ns, min_effects, linewidth=2.5, color='#1f77b4')

    # Reference lines for Cohen's benchmarks
    ax.axhline(y=0.20, color='green', linestyle=':', alpha=0.5, label='Small (d=0.20)')
    ax.axhline(y=0.50, color='orange', linestyle=':', alpha=0.5, label='Medium (d=0.50)')
    ax.axhline(y=0.80, color='red', linestyle=':', alpha=0.5, label='Large (d=0.80)')

    ax.set_xlabel('Sample Size per Group', fontsize=13)
    ax.set_ylabel('Minimum Detectable Effect Size (d)', fontsize=13)
    ax.set_title(title, fontsize=15, fontweight='bold')
    ax.legend(fontsize=11)
    ax.grid(True, alpha=0.3)
    ax.tick_params(labelsize=11)

    plt.tight_layout()

    if save_path:
        fig.savefig(save_path, dpi=300, bbox_inches='tight')

    return fig
```

---

## Special Cases

### Cluster Randomized Designs

Standard power analysis assumes independent observations. In cluster designs (randomization at group level), observations within clusters are correlated. The design effect inflates the required N.

```python
def cluster_power_analysis(n_individual, icc, avg_cluster_size):
    """
    Adjust required sample size for clustering.

    Design effect = 1 + (m - 1) * ICC
    where m = average cluster size

    Parameters:
        n_individual: Required N from standard (non-clustered) power analysis
        icc: Intraclass correlation coefficient
        avg_cluster_size: Average number of individuals per cluster
    """
    design_effect = 1 + (avg_cluster_size - 1) * icc
    n_adjusted = int(np.ceil(n_individual * design_effect))
    n_clusters_total = int(np.ceil(n_adjusted / avg_cluster_size))

    print(f"ICC: {icc}")
    print(f"Average cluster size: {avg_cluster_size}")
    print(f"Design effect: {design_effect:.2f}")
    print(f"Standard N: {n_individual}")
    print(f"Adjusted N: {n_adjusted}")
    print(f"Total clusters needed: {n_clusters_total}")
    print(f"Clusters per arm (2 arms): {int(np.ceil(n_clusters_total / 2))}")

    return {
        'design_effect': design_effect,
        'n_adjusted': n_adjusted,
        'n_clusters_total': n_clusters_total,
        'n_clusters_per_arm': int(np.ceil(n_clusters_total / 2))
    }

# Typical ICCs by domain
# Education (students in classrooms): ICC = 0.05-0.20
# Health (patients in clinics): ICC = 0.01-0.05
# Psychology (participants in groups): ICC = 0.01-0.10
```

### Repeated Measures / Within-Subjects

Within-subjects designs are more powerful because they control for between-subject variability.

```python
def within_subjects_n(n_between, correlation_between_measures):
    """
    Convert between-subjects N to within-subjects N.

    The within-subjects N is approximately:
    N_within = N_between * (1 - r) / number_of_measurements

    where r is the correlation between repeated measures.
    """
    n_within = n_between * (1 - correlation_between_measures)
    return max(int(np.ceil(n_within)), 2)

# Example: between-subjects needs N=64 per group, r=0.5 between pre and post
n_within = within_subjects_n(64, 0.5)
print(f"Within-subjects N: {n_within}")
# Output: 32 (half as many needed)
```

### ANCOVA Power Boost

Including a covariate (e.g., pretest) that correlates with the DV reduces error variance and increases power.

```python
def ancova_adjusted_n(n_required, r_covariate_dv):
    """
    Adjust N for ANCOVA (covariate reduces error variance).

    Effective N = N_original * (1 - r^2)
    So N_needed = N_anova * (1 - r^2)
    """
    n_adjusted = n_required * (1 - r_covariate_dv**2)
    return max(int(np.ceil(n_adjusted)), 2)

# Example: ANOVA needs 64 per group, pretest-posttest r = 0.6
n_ancova = ancova_adjusted_n(64, 0.6)
print(f"ANCOVA N per group: {n_ancova}")
# Output: 41 (substantial reduction)
```

---

## Common Pitfalls

### 1. Post-Hoc Power Analysis

**Problem**: Computing power using the observed effect size after the study is complete.
**Why it is wrong**: Post-hoc power is a direct function of the p-value. If p < 0.05, post-hoc power is always > 0.50. It provides zero additional information.
**Correct approach**: Report the observed effect size with confidence interval. If non-significant, report the minimum detectable effect size at the achieved N.

### 2. Using "Convention" as Justification

**Problem**: "We used d = 0.5 because Cohen (1988) considers this a medium effect."
**Why it is problematic**: Effect sizes vary enormously across domains and outcomes. A "medium" effect for one context may be unrealistically large for another.
**Correct approach**: Base effect size on prior research (meta-analysis preferred), pilot data, or SESOI.

### 3. Ignoring Attrition

**Problem**: Recruiting exactly the number the power analysis recommends.
**Why it fails**: Dropout, missing data, and exclusions reduce the final analyzable N below the target.
**Correct approach**: Inflate N by an attrition buffer. Default 15-20%; use empirical rates from prior studies when available.

### 4. Forgetting Design Effects in Cluster Designs

**Problem**: Using standard power analysis for cluster-randomized designs.
**Why it fails**: Observations within clusters are correlated, reducing effective sample size. A study with 20 classrooms of 25 students each (N=500) may have the effective N of only 100-200 independent observations.
**Correct approach**: Apply design effect correction (see Special Cases above).

### 5. Powering for Main Effects in Factorial Designs

**Problem**: Computing power for main effects when the interaction is the primary hypothesis.
**Why it fails**: The interaction effect requires approximately 4x the sample size to achieve the same power as a main effect of the same magnitude.
**Correct approach**: If the interaction is the primary hypothesis, power for the interaction specifically.

### 6. One-Tailed Tests Without Strong Justification

**Problem**: Using one-tailed tests to achieve higher power (or lower N).
**Why it is problematic**: One-tailed tests assume you know the direction of the effect a priori. If the effect is in the opposite direction, you cannot detect it.
**Correct approach**: Default to two-tailed. One-tailed requires: (a) strong theoretical justification, (b) pre-registration, (c) commitment to not interpret an opposite-direction effect.

### 7. Ignoring Multiple Comparisons

**Problem**: Powering for each test individually without adjusting for multiplicity.
**Why it fails**: Testing 5 hypotheses at alpha = 0.05 gives a familywise error rate of 1 - (1-0.05)^5 = 0.226 (23% chance of at least one false positive).
**Correct approach**: Use adjusted alpha in the power analysis (e.g., alpha = 0.05/5 = 0.01 for Bonferroni with 5 tests).

### 8. Confusing Effect Size Metrics

**Problem**: Using Cohen's d when the power function expects Cohen's f, or vice versa.
**Why it fails**: d = 0.5 and f = 0.5 represent very different effect sizes. d = 0.5 is medium; f = 0.5 is between medium and large.
**Conversion**: For 2-group comparison, f = d/2. For eta-squared, f = sqrt(eta_sq / (1 - eta_sq)).

---

## Quick Reference Table: Required N per Group

All values assume two-tailed alpha = 0.05, power = 0.80, equal groups.

| Test | Small Effect | Medium Effect | Large Effect |
|------|-------------|---------------|-------------|
| Independent t-test | 393 (d=0.2) | 64 (d=0.5) | 26 (d=0.8) |
| Paired t-test | 199 (d=0.2) | 34 (d=0.5) | 15 (d=0.8) |
| One-way ANOVA (3 groups) | 322 (f=0.1) | 53 (f=0.25) | 22 (f=0.4) |
| One-way ANOVA (4 groups) | 274 (f=0.1) | 45 (f=0.25) | 18 (f=0.4) |
| Correlation | 783 (r=0.1) | 85 (r=0.3) | 28 (r=0.5) |
| Chi-square (2x2) | 785 (w=0.1) | 88 (w=0.3) | 26 (w=0.5) |
| Regression (3 predictors) | 547 (f2=0.02) | 77 (f2=0.15) | 36 (f2=0.35) |

**Note**: These are per-group values for t-tests and ANOVA, and total N for correlations, chi-square, and regression.
