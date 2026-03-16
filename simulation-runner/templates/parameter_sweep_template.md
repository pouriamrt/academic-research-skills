# Parameter Sweep Report Template — Sensitivity Analysis Documentation

## Purpose

A fill-in template for documenting parameter sweep and sensitivity analysis results. Covers the parameter grid, results matrix, visualization references (tornado, spider, heatmap), main effects, interactions, and robust region identification.

---

## Instructions

1. Complete all sections marked `[Required]`
2. Reference all plots by file path in `experiment_outputs/plots/`
3. The robust region section is critical for practical recommendations
4. For sweeps with > 2 dimensions, use the main effects table rather than full heatmaps
5. Interaction effects are required when sweeping 2+ parameters simultaneously

---

## Header

```
Parameter Sweep Report
======================

Simulation ID: [SIM-YYYYMMDD-NNN]
Date: [ISO 8601 timestamp]
Sweep Type: [one-at-a-time / full factorial / Latin hypercube / custom]
Total Grid Cells: [N]
Iterations per Cell: [n]
Overall Status: [Complete / Partial (N of M cells converged)]
```

---

## 1. Parameter Grid [Required]

### 1.1 Swept Parameters

| # | Parameter | Symbol | Baseline | Sweep Values | Scale | Justification |
|---|-----------|--------|----------|-------------|-------|---------------|
| P1 | [name] | [symbol] | [baseline value] | [value list or range] | [linear / log / custom] | [why these values] |
| P2 | [name] | [symbol] | [baseline value] | [value list or range] | [linear / log / custom] | [why these values] |
| P3 | [name] | [symbol] | [baseline value] | [value list or range] | [linear / log / custom] | [why these values] |

### 1.2 Fixed Parameters

| Parameter | Value | Justification |
|-----------|-------|---------------|
| [name] | [value] | [why fixed at this value] |
| [name] | [value] | [why fixed at this value] |

### 1.3 Grid Structure

```
Sweep Type: [one-at-a-time / full factorial / Latin hypercube]

For full factorial:
  Total cells = [product of all sweep value counts]
  Example: 5 x 4 x 3 = 60 cells

For one-at-a-time:
  Total cells = [sum of (sweep values - 1) for each parameter] + 1 (baseline)
  Example: (5-1) + (4-1) + (3-1) + 1 = 11 cells

For Latin hypercube:
  Total cells = [n_samples]
  Dimensions = [n_parameters]
```

---

## 2. Results Matrix [Required]

### 2.1 One-at-a-Time Results

For each parameter varied individually (others at baseline):

#### Parameter P1: [Name]

| P1 Value | Estimand E1 | MCSE | 95% Sim CI | Estimand E2 | MCSE | 95% Sim CI |
|----------|-------------|------|------------|-------------|------|------------|
| [value] | [result] | [mcse] | [lo, hi] | [result] | [mcse] | [lo, hi] |
| **[baseline]** | **[result]** | **[mcse]** | **[lo, hi]** | **[result]** | **[mcse]** | **[lo, hi]** |
| [value] | [result] | [mcse] | [lo, hi] | [result] | [mcse] | [lo, hi] |

[Repeat table for each swept parameter]

### 2.2 Full Factorial Results (if applicable)

For 2D sweeps, present as a matrix:

**Estimand E1: [Name]**

| | P2 = [v1] | P2 = [v2] | P2 = [v3] | P2 = [v4] |
|---|-----------|-----------|-----------|-----------|
| P1 = [v1] | [result] | [result] | [result] | [result] |
| P1 = [v2] | [result] | [result] | [result] | [result] |
| P1 = [v3] | [result] | [result] | [result] | [result] |

For higher dimensions, report marginal effects (averaged over other parameters).

### 2.3 Summary Statistics Across Sweep

| Estimand | Baseline | Min | Max | Range | Most Sensitive To |
|----------|----------|-----|-----|-------|------------------|
| E1 | [value] | [value] | [value] | [value] | [parameter name] |
| E2 | [value] | [value] | [value] | [value] | [parameter name] |

---

## 3. Visualizations [Required]

### 3.1 Tornado Plot

Shows the impact of each parameter on the estimand when varied from low to high, with all other parameters at baseline. Parameters are sorted by total impact (largest at top).

```
File: experiment_outputs/plots/tornado_[estimand_name].png

Interpretation:
[1-2 sentence description of what the tornado plot reveals]

Ranking (most to least influential):
1. [Parameter name]: range = [low_result] to [high_result] (total range: [value])
2. [Parameter name]: range = [low_result] to [high_result] (total range: [value])
3. [Parameter name]: range = [low_result] to [high_result] (total range: [value])
```

### 3.2 Spider Plot

Shows how the estimand changes as each parameter is varied from -50% to +50% of baseline, with all other parameters at baseline. Each parameter is a separate line.

```
File: experiment_outputs/plots/spider_[estimand_name].png

Interpretation:
[1-2 sentence description of linearity/nonlinearity observations]

Key observations:
- [Parameter A] shows [linear / nonlinear / threshold] relationship
- [Parameter B] has a steeper slope on the [positive/negative] side
- [Parameters C, D] have minimal influence
```

### 3.3 Heatmap [Conditional: 2D sweeps]

Shows the estimand value across a 2D parameter grid as a color map.

```
File: experiment_outputs/plots/heatmap_[estimand_name]_[param1]_[param2].png

Interpretation:
[1-2 sentence description of the landscape]

Key features:
- [Gradient direction and steepness]
- [Any ridges, valleys, or plateaus]
- [Interaction visible as non-parallel contours]
```

### 3.4 Convergence Across Sweep Cells

```
File: experiment_outputs/plots/sweep_convergence_summary.png

Cells converged: [n] / [total]
Cells marginal: [n]
Cells not converged: [n]

Worst-converging cells: [list parameter combinations with poorest convergence]
```

---

## 4. Main Effects [Required]

The main effect of a parameter is the average change in the estimand when that parameter is varied, holding all others at baseline (one-at-a-time) or averaging over all other parameter combinations (factorial).

### 4.1 Main Effects Table

| Parameter | Direction | Magnitude | Significance | Description |
|-----------|-----------|-----------|-------------|-------------|
| P1: [name] | [Positive / Negative / Non-monotonic] | [change in estimand units] | [Large / Moderate / Small / Negligible] | [1-sentence description] |
| P2: [name] | [Positive / Negative / Non-monotonic] | [change in estimand units] | [Large / Moderate / Small / Negligible] | [1-sentence description] |
| P3: [name] | [Positive / Negative / Non-monotonic] | [change in estimand units] | [Large / Moderate / Small / Negligible] | [1-sentence description] |

### 4.2 Magnitude Classification

| Category | Criterion |
|----------|----------|
| Large | Changes estimand by > 20% of baseline |
| Moderate | Changes estimand by 5-20% of baseline |
| Small | Changes estimand by 1-5% of baseline |
| Negligible | Changes estimand by < 1% of baseline |

---

## 5. Interaction Effects [Conditional: when 2+ parameters swept simultaneously]

### 5.1 Two-Way Interactions

| Parameter Pair | Interaction Present? | Direction | Magnitude | Description |
|----------------|---------------------|-----------|-----------|-------------|
| P1 x P2 | [Yes / No] | [Synergistic / Antagonistic] | [value] | [description] |
| P1 x P3 | [Yes / No] | [Synergistic / Antagonistic] | [value] | [description] |
| P2 x P3 | [Yes / No] | [Synergistic / Antagonistic] | [value] | [description] |

### 5.2 Interaction Interpretation

```
[For each significant interaction, explain what it means practically]

Example:
The interaction between effect size and sample size is synergistic: the benefit
of increasing sample size is greater at larger effect sizes. Specifically, going
from n=30 to n=60 increases power by .15 when d=0.2, but by .35 when d=0.5.
This suggests that the marginal return on increasing sample size depends on the
expected effect size.
```

### 5.3 Interaction Plots

```
File: experiment_outputs/plots/interaction_[param1]_[param2]_[estimand].png

[Non-parallel lines indicate interaction; crossing lines indicate disordinal interaction]
```

---

## 6. Robust Region [Required]

The robust region is the set of parameter values for which the estimand meets a specified criterion (e.g., power >= .80, bias < 5%, coverage >= .90).

### 6.1 Criterion Definition

```
Criterion: [estimand name] [operator] [threshold]
Example: Power >= 0.80 at alpha = .05
Example: Coverage of 95% CI >= 0.90
Example: Absolute bias < 5% of true value
```

### 6.2 Robust Region Description

```
The [estimand] meets the criterion ([criterion]) under the following conditions:

- [Parameter 1]: [range or condition]
- [Parameter 2]: [range or condition]
- [Parameter 3]: [any value (insensitive)]

Boundary conditions (parameters at the edge of the robust region):
- [Parameter 1] = [value] (just meets criterion)
- [Parameter 2] = [value] (just meets criterion)
```

### 6.3 Robust Region Visualization

```
File: experiment_outputs/plots/robust_region_[estimand_name].png

[Shaded region on 2D parameter space showing where criterion is met]
```

### 6.4 Practical Recommendation

```
[Based on the robust region, what should the researcher do?]

Example:
To ensure statistical power >= .80 for the planned 2x3 mixed ANOVA:
- Use a minimum sample size of n >= 55 per group
- The design is robust to moderate deviations in the assumed correlation
  structure (rho from 0.3 to 0.7)
- Effect size is the dominant factor; if the true effect is smaller than
  f = 0.20, no feasible sample size achieves .80 power
```

---

## 7. Summary and Conclusions [Required]

### 7.1 Key Findings

```
1. [Most important finding from the sweep]
2. [Second most important finding]
3. [Third most important finding]
```

### 7.2 Parameter Ranking (by influence)

```
1. [Most influential parameter]: [brief description of impact]
2. [Second most influential]: [brief description]
3. [Least influential]: [brief description — can be fixed at any reasonable value]
```

### 7.3 Limitations of the Sweep

```
1. [Limitation, e.g., "Only one-at-a-time variation; higher-order interactions not explored"]
2. [Limitation, e.g., "Grid resolution may miss narrow regions of parameter space"]
3. [Limitation, e.g., "Results conditional on fixed parameters not swept"]
```

---

## Pre-Submission Checklist

- [ ] All swept parameters documented with baseline, values, and justification
- [ ] Fixed parameters documented with justification
- [ ] Results matrix complete for all grid cells
- [ ] Tornado plot generated and interpretation provided
- [ ] Spider plot generated and interpretation provided
- [ ] Heatmap generated for 2D sweeps
- [ ] Main effects table complete with magnitude classification
- [ ] Interaction effects assessed (if 2+ parameters)
- [ ] Robust region defined with practical recommendation
- [ ] Convergence assessed per cell (or summary)
- [ ] Summary ranks parameters by influence
- [ ] All plot files exist at referenced paths
