# Simulation Report Template — ADEMP-Structured Full Report

## Purpose

A fill-in template for the complete simulation report. Follows the ADEMP framework (Aims, Data-Generating Process, Estimands, Methods, Performance) as recommended by Morris et al. (2019). Maps directly to Schema 11 (Experiment Results) for downstream consumption by `academic-paper` and `lab-notebook`.

---

## Instructions

1. Fill all sections marked `[Required]`; sections marked `[Conditional]` are required only for specific modes
2. Replace all `[placeholder]` text with actual values
3. Reference all diagnostic plots by their file paths in `experiment_outputs/plots/`
4. The APA Results Text section should be copy-paste ready for academic papers
5. Ensure the Seed Log section enables exact reproduction of results

---

## Header

```
Simulation Report
=================

Simulation ID: [SIM-YYYYMMDD-NNN]
Experiment ID: [Schema 10 ID or AD-HOC]
Date: [ISO 8601 timestamp]
Mode: [full / guided / quick / power-sim / sensitivity / bootstrap]
Simulation Type: [monte_carlo / bootstrap / power_sim / parameter_sweep / agent_based / resampling / stochastic_process / optimization]
Overall Status: [Converged / Marginal / Not Converged]
```

---

## 1. Aims [Required]

> What question does this simulation answer? Why simulation rather than analytical solution?

```
Research Context:
[Brief description of the research problem that motivates this simulation]

Simulation Objectives:
1. [Primary objective — what this simulation is designed to estimate or evaluate]
2. [Secondary objective, if any]
3. [Tertiary objective, if any]

Justification for Simulation:
[Why analytical or closed-form solutions are insufficient for this problem]

Pre-Specified Hypotheses (if applicable):
- H1: [hypothesis statement]
- H2: [hypothesis statement, if any]
```

---

## 2. Data-Generating Process (DGP) [Required]

> Complete specification of how simulated data are created.

### 2.1 Model Description

```
Conceptual Model:
[Plain-language description of the data-generating mechanism]

Formal Specification:
[Mathematical notation for the DGP]
Example: Y_ij = mu + alpha_i + beta_j + (alpha*beta)_ij + epsilon_ij

Error Distribution:
[Distribution of random components]
Example: epsilon ~ N(0, sigma^2)

Functional Form:
[Relationships between variables]
```

### 2.2 Parameter Table

| Parameter | Symbol | Type | Default Value | Range (if swept) | Source/Justification |
|-----------|--------|------|---------------|-------------------|---------------------|
| [name] | [symbol] | [fixed/swept/derived] | [value] | [min, max] or N/A | [literature ref or rationale] |
| [name] | [symbol] | [fixed/swept/derived] | [value] | [min, max] or N/A | [literature ref or rationale] |
| [name] | [symbol] | [fixed/swept/derived] | [value] | [min, max] or N/A | [literature ref or rationale] |

### 2.3 Distributions

| Component | Distribution | Parameters | Library Call |
|-----------|-------------|------------|-------------|
| [component] | [distribution name] | [param values] | `rng.normal(mu, sigma, size=n)` |
| [component] | [distribution name] | [param values] | `rng.choice(options, size=n)` |

### 2.4 Assumptions

1. [Assumption]: [justification and impact if violated]
2. [Assumption]: [justification and impact if violated]
3. [Assumption]: [justification and impact if violated]

### 2.5 Model Specification Reference

> See: `templates/model_specification_template.md` for the detailed specification.

Script: `experiment_outputs/scripts/dgp_functions.py`

---

## 3. Estimands [Required]

> What specific quantities are being estimated from the simulation?

| # | Estimand | Description | True Value (if known) | Unit |
|---|----------|-------------|----------------------|------|
| E1 | [name] | [what it measures] | [value or "unknown"] | [unit] |
| E2 | [name] | [what it measures] | [value or "unknown"] | [unit] |
| E3 | [name] | [what it measures] | [value or "unknown"] | [unit] |

---

## 4. Methods [Required]

> Statistical methods applied to each iteration of simulated data.

### 4.1 Analysis Methods

| Estimand | Statistical Method | Implementation | Library |
|----------|-------------------|----------------|---------|
| E1 | [method name] | [brief description] | [scipy/statsmodels/custom] |
| E2 | [method name] | [brief description] | [scipy/statsmodels/custom] |

### 4.2 Execution Parameters

```
Iterations: [n_iterations]
Chains: [n_chains]
Burn-in: [n_burn_in iterations removed]
Check Interval: [every N iterations]
Convergence Criterion: [MCSE < threshold / R-hat < 1.05 / custom]
Parallelization: [yes/no], [n_workers] workers
Early Stopping: [enabled/disabled]
```

### 4.3 Parameter Sweep Grid [Conditional: sensitivity/sweep modes]

| Parameter | Values | Total Cells |
|-----------|--------|-------------|
| [param 1] | [value list] | — |
| [param 2] | [value list] | — |
| **Total grid size** | — | [N cells] |

Iterations per cell: [n]

---

## 5. Performance Measures [Required]

> How the quality of estimands is assessed.

| Measure | Definition | Applied To |
|---------|-----------|------------|
| Bias | E[theta_hat] - theta | All estimands with known truth |
| MSE | E[(theta_hat - theta)^2] | All estimands with known truth |
| Coverage | Proportion of CIs containing true value | CI-based estimands |
| Power | Proportion of p < alpha under H1 | Hypothesis testing estimands |
| Type I Error | Proportion of p < alpha under H0 | Hypothesis testing estimands |
| MCSE | SD(theta_hat) / sqrt(n_iterations) | All estimands |
| [Custom] | [definition] | [which estimands] |

---

## 6. Results [Required]

### 6.1 Summary Table

| Estimand | Estimate | SE | MCSE | 95% Sim CI | Bias | MSE | Convergence |
|----------|----------|-----|------|------------|------|-----|-------------|
| E1 | [value] | [value] | [value] | [lo, hi] | [value] | [value] | [status] |
| E2 | [value] | [value] | [value] | [lo, hi] | [value] | [value] | [status] |

### 6.2 Power Curve [Conditional: power-sim mode]

| Sample Size (per group) | Power | MCSE | 95% Sim CI | Type I Error |
|------------------------|-------|------|------------|-------------|
| [n] | [value] | [value] | [lo, hi] | [value] |
| [n] | [value] | [value] | [lo, hi] | [value] |

**Recommended sample size**: To achieve power >= .80 at alpha = .05: **n >= [X] per group**

Power curve plot: `experiment_outputs/plots/power_curve.png`

### 6.3 Sensitivity Results [Conditional: sensitivity mode]

See `templates/parameter_sweep_template.md` for the detailed sweep report.

Tornado plot: `experiment_outputs/plots/tornado_[estimand].png`
Spider plot: `experiment_outputs/plots/spider_[estimand].png`

### 6.4 Bootstrap Results [Conditional: bootstrap mode]

| Statistic | Observed | Bootstrap Mean | Bias | BCa 95% CI | Percentile 95% CI |
|-----------|----------|---------------|------|-----------|-------------------|
| [name] | [value] | [value] | [value] | [lo, hi] | [lo, hi] |

BCa correction constants: z0 = [value], a = [value]
Bootstrap distribution plot: `experiment_outputs/plots/bootstrap_dist_[statistic].png`

---

## 7. Convergence Diagnostics [Required for full/power-sim/sensitivity/bootstrap modes]

> See: Convergence Report from `diagnostics_agent`

### 7.1 Summary

| Estimand | MCSE | R-hat | ESS | Overall Verdict |
|----------|------|-------|-----|----------------|
| E1 | [value] | [value] | [value] | [Converged/Marginal/Not Converged] |
| E2 | [value] | [value] | [value] | [Converged/Marginal/Not Converged] |

### 7.2 Diagnostic Plots

| Estimand | Trace | ACF | Distribution | Running MCSE |
|----------|-------|-----|-------------|-------------|
| E1 | [path] | [path] | [path] | [path] |
| E2 | [path] | [path] | [path] | [path] |

### 7.3 Issues and Recommendations

```
[List any convergence issues and specific recommendations, or "No issues detected."]
```

---

## 8. Seed Log [Required]

```
Master Seed: [seed]
SeedSequence Entropy: [entropy]
Child Seeds: [n] streams spawned
Method: SeedSequence.spawn

Reproduction Command:
  from numpy.random import SeedSequence, default_rng
  ss = SeedSequence([master_seed])
  rngs = [default_rng(s) for s in ss.spawn([n_streams])]
```

---

## 9. Script Reference [Required]

```
Main simulation script: experiment_outputs/scripts/simulation_SIM-YYYYMMDD-NNN.py
DGP functions: experiment_outputs/scripts/dgp_functions.py
Results data: experiment_outputs/results/summary_statistics.csv
Raw results: experiment_outputs/results/raw_results.npz
Environment: experiment_env/requirements.txt
```

**To reproduce**: Run the main simulation script in the recorded environment with the recorded master seed.

---

## 10. APA Results Text [Required]

> Copy-paste ready text for the Methods and Results sections of an academic paper.

### Methods Section Insert

```
[APA-formatted description of the simulation design, following ADEMP structure.
Include: simulation type, DGP specification, number of iterations, convergence
criteria, software environment.]
```

### Results Section Insert

```
[APA-formatted results with italicized statistics, MCSE for every estimate,
simulation CIs, convergence confirmation.]
```

---

## 11. Limitations [Required]

1. [Limitation]: [impact on interpretation]
2. [Limitation]: [impact on interpretation]
3. [Limitation]: [impact on interpretation]

---

## 12. AI Disclosure [Required]

```
This simulation was designed and executed with the assistance of AI-powered
simulation tools (simulation-runner skill, v1.0). The data-generating process,
execution parameters, and convergence diagnostics were reviewed by the researcher.
All code is available at the referenced script paths for independent verification.
```

---

## 13. Model Provenance [Conditional: when Schema 13 is the source]

```
Source: Schema 13 Simulation Specification
Experiment ID: [from Schema 13]
ADEMP Pre-Specified: [yes/no]
Deviations from Specification: [list or "None"]
```

---

## Pre-Submission Checklist

- [ ] All [Required] sections completed
- [ ] All estimates accompanied by MCSE and simulation CI
- [ ] Convergence diagnostics report attached (full/power-sim/sensitivity/bootstrap modes)
- [ ] Seed log enables exact reproduction
- [ ] Script runs independently in the recorded environment
- [ ] All referenced plot files exist
- [ ] APA results text is correctly formatted
- [ ] AI disclosure included
- [ ] Limitations section addresses key assumptions
- [ ] Schema 11 artifact generated (if downstream pipeline)
- [ ] Material Passport generated (if downstream pipeline)
