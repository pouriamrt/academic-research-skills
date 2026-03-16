# Power Analysis Report Template

## Purpose

A fill-in template for documenting power analysis results. Produced by the power_analyst_agent. Captures all parameters, results, power curves, and sensitivity analysis in a standardized format for inclusion in the experiment protocol.

## Instructions

1. Complete all sections marked `[Required]`
2. Include the power curve figure (saved as PNG at 300 DPI)
3. Provide the complete Python code for reproducibility
4. If multiple primary analyses exist, produce a separate power analysis section for each

---

## A. Analysis Identification [Required]

### Study Information
```
Study title: [Enter study title]
Protocol ID: [EXP-YYYYMMDD-NNN]
Hypothesis tested: [H1 / H2 / etc.]
Date computed: [YYYY-MM-DD]
Analyst: [Name or "experiment-designer/power_analyst_agent"]
```

---

## B. Test Specification [Required]

### Statistical Test
```
Test family: [t-test / ANOVA / chi-square / regression / mixed model / etc.]
Specific test: [Independent samples t-test / One-way ANOVA / 2x2 factorial ANOVA / etc.]
Number of groups: [integer]
Number of levels per factor: [e.g., Factor A: 2, Factor B: 3]
Between/within: [Between-subjects / Within-subjects / Mixed]
Tails: [Two-tailed / One-tailed — if one-tailed, provide justification]
```

---

## C. Parameters [Required]

### Effect Size
```
Metric: [Cohen's d / Cohen's f / eta-squared / partial eta-squared / r / f-squared / w / odds ratio]
Value: [numeric value]
Magnitude: [Negligible / Small / Medium / Large per conventions]

Source of effect size estimate:
- [ ] Prior meta-analysis: [citation, k studies, N total]
- [ ] Prior empirical study: [citation, N, design]
- [ ] Pilot study: [N, brief description]
- [ ] Smallest effect size of interest (SESOI): [justification for why this is the minimum meaningful effect]
- [ ] Expert judgment: [justification — note: weakest source]

If multiple sources are available, report all and justify the selected value:
| Source | Effect Size | N | Notes |
|--------|------------|---|-------|
| [Study 1] | d = [value] | [N] | [context] |
| [Study 2] | d = [value] | [N] | [context] |
| [Meta-analysis] | d = [value] | k = [studies] | [context] |
| Selected | d = [value] | — | [justification for selection] |
```

### Alpha Level
```
Alpha (Type I error rate): [0.05 / 0.01 / 0.005 / other]
Justification for non-standard alpha: [if not 0.05, explain why]
```

### Desired Power
```
Power (1 - beta): [0.80 / 0.90 / 0.95]
Justification:
- [ ] Standard (0.80) — typical for social/behavioral research
- [ ] Elevated (0.90) — clinical trial or high-stakes decision
- [ ] High (0.95) — confirmatory replication or regulatory requirement
```

### Additional Parameters
```
Allocation ratio: [1:1 / 2:1 / Other — justify unequal allocation]
Correlation between repeated measures: [r = value, if within-subjects]
Number of predictors (regression): [integer]
ICC (cluster designs): [value, source]
Cluster size (cluster designs): [average N per cluster]
Number of covariates: [integer, expected R-squared with DV]
```

---

## D. Sample Size Result [Required]

### Primary Calculation
```
Required N per group: [integer — always round UP]
Number of groups: [integer]
Total required N: [integer]
```

### Attrition Adjustment
```
Expected attrition rate: [%] — Source: [prior study / institutional data / estimate]
Adjusted N per group: ceil(N_required / (1 - attrition_rate)) = [integer]
Total recruitment target: [integer]
```

### Design Effect Adjustment [If applicable — cluster designs only]
```
ICC: [value]
Average cluster size: [integer]
Design effect: 1 + (cluster_size - 1) * ICC = [value]
Adjusted N: N_required * design_effect = [integer]
Clusters per group: ceil(N_adjusted / cluster_size) = [integer]
Total clusters needed: [integer]
```

### Final Recommendation
```
RECRUIT: [Total N] participants
Per group: [N per group]
[If cluster: [N clusters] clusters with ~[size] participants each]
```

---

## E. Power Curve [Required]

### Figure
```
[Insert power curve figure or reference path]
Path: experiment_outputs/figures/power_curve_[protocol_id].png
```

### Curve Parameters
```
X-axis: Sample size per group, range [min] to [max]
Y-axis: Statistical power (0 to 1)
Effect sizes plotted: [d = 0.2, d = 0.5, d = 0.8] (or appropriate values)
Target power line: [0.80] (dashed red line)
Selected N marked: [vertical line at chosen N]
```

### Interpretation
```
[2-3 sentences interpreting the power curve. Example:
"With N=64 per group, the study achieves 0.80 power to detect a medium effect
(d=0.50) but only 0.30 power to detect a small effect (d=0.20). If the true
effect is large (d=0.80), the study is well-powered at 0.99."]
```

---

## F. Sensitivity Analysis [Required]

### What Can We Detect?

Given various feasible sample sizes, what is the minimum detectable effect size at the target power level?

```
Target power: [0.80]
Alpha: [0.05]

| N per group | Total N | Min detectable effect size | Magnitude | Interpretation |
|-------------|---------|--------------------------|-----------|----------------|
| [N1] | [N1*k] | d = [value] | [Small/Med/Large] | [Feasible? Meaningful?] |
| [N2] | [N2*k] | d = [value] | [Small/Med/Large] | [Feasible? Meaningful?] |
| [N3] | [N3*k] | d = [value] | [Small/Med/Large] | [Feasible? Meaningful?] |
| [N4] | [N4*k] | d = [value] | [Small/Med/Large] | [Feasible? Meaningful?] |
| [N5] | [N5*k] | d = [value] | [Small/Med/Large] | [Feasible? Meaningful?] |
```

### Sensitivity Interpretation
```
[2-3 sentences interpreting the sensitivity analysis. Example:
"With a maximum feasible sample of N=50 per group, the study can only detect
effects of d >= 0.57, which is between medium and large. If the expected effect
is truly medium (d=0.50), the study would be underpowered at 0.70. Consider
increasing to N=64 per group for adequate power."]
```

---

## G. Assumptions and Limitations [Required]

### Statistical Assumptions
```
- [ ] Equal variances across groups (if applicable)
- [ ] Normal distribution of the DV (or large N for CLT)
- [ ] Independence of observations
- [ ] No significant covariates omitted
- [ ] Effect size estimate is accurate (based on [source])
- [ ] Attrition is random (MCAR)
```

### Limitations
```
1. [Limitation 1 — e.g., "Effect size based on a single prior study with small N"]
2. [Limitation 2 — e.g., "ICC estimated from different population; actual clustering may differ"]
3. [Limitation 3 — e.g., "Power for interaction effect is substantially lower than for main effects"]
```

### What This Analysis Does NOT Tell You
```
- Power analysis assumes the statistical model is correctly specified
- Sample size is sufficient for the primary analysis but may be insufficient for subgroup analyses
- Post-hoc power analysis (computing power from observed effect size) is not meaningful and should not be performed
```

---

## H. Reproducibility [Required]

### Complete Python Code
```python
# Power Analysis for [Study Title]
# Protocol ID: [EXP-YYYYMMDD-NNN]
# Date: [YYYY-MM-DD]
# Environment: Python [version], statsmodels [version], scipy [version]

import numpy as np
import matplotlib.pyplot as plt
from statsmodels.stats.power import [appropriate class]

# Parameters
effect_size = [value]  # [metric], source: [source]
alpha = [value]
power = [value]
[additional parameters]

# Sample size calculation
analysis = [PowerClass]()
n_per_group = analysis.solve_power(
    effect_size=effect_size,
    alpha=alpha,
    power=power,
    [additional parameters]
)
n_per_group = int(np.ceil(n_per_group))
print(f"Required N per group: {n_per_group}")

# Attrition adjustment
attrition_rate = [value]
n_adjusted = int(np.ceil(n_per_group / (1 - attrition_rate)))
print(f"Adjusted N per group (with {attrition_rate*100:.0f}% attrition buffer): {n_adjusted}")

# Power curve
effect_sizes = [list of values]
ns = np.arange([min], [max], [step])
fig, ax = plt.subplots(figsize=(10, 6))
for d in effect_sizes:
    powers = [analysis.solve_power(effect_size=d, nobs1=n, alpha=alpha, alternative='two-sided') for n in ns]
    ax.plot(ns, powers, label=f"d = {d}", linewidth=2)
ax.axhline(y=[power_target], color='red', linestyle='--', label=f'Target power = {[power_target]}')
ax.axvline(x=n_per_group, color='gray', linestyle=':', alpha=0.5, label=f'Selected N = {n_per_group}')
ax.set_xlabel('Sample Size per Group')
ax.set_ylabel('Statistical Power')
ax.set_title('Power Curve')
ax.legend()
ax.set_ylim(0, 1.05)
ax.grid(True, alpha=0.3)
plt.tight_layout()
fig.savefig('experiment_outputs/figures/power_curve_[protocol_id].png', dpi=300, bbox_inches='tight')

# Sensitivity analysis
for n in [list of Ns]:
    min_d = analysis.solve_power(effect_size=None, nobs1=n, alpha=alpha, power=[power_target], alternative='two-sided')
    print(f"N={n}: minimum detectable d = {min_d:.3f}")
```

### Environment
```
Python version: [e.g., 3.12.3]
statsmodels version: [e.g., 0.14.1]
scipy version: [e.g., 1.13.0]
numpy version: [e.g., 1.26.4]
matplotlib version: [e.g., 3.8.3]
```

---

## Pre-Submission Checklist

- [ ] Effect size source is explicitly documented (not just "convention")
- [ ] Alpha and power levels are stated and justified
- [ ] Sample size is an integer (rounded UP)
- [ ] Attrition buffer is applied
- [ ] Design effect is applied (if cluster design)
- [ ] Power curve is generated with at least 3 effect sizes
- [ ] Sensitivity analysis covers at least 3 feasible sample sizes
- [ ] All assumptions are listed
- [ ] Complete reproducible Python code is provided
- [ ] Environment versions are documented
- [ ] Post-hoc power analysis is NOT included (this is a prospective analysis only)
