# Convergence Report Template — Per-Estimand Diagnostic Assessment

## Purpose

A fill-in template for documenting the convergence assessment of a simulation. Each estimand receives its own assessment with numerical metrics and plot references. The overall verdict is the most conservative (worst-case) across all estimands.

---

## Instructions

1. Complete one assessment block per estimand
2. All four metrics (MCSE, R-hat, ESS, ACF) must be computed for each estimand
3. R-hat is marked N/A for single-chain simulations or i.i.d. methods (bootstrap, pure Monte Carlo)
4. All diagnostic plots must be generated and paths recorded
5. The overall verdict must match the most conservative per-estimand verdict
6. If any estimand is "Not Converged", recommendations are mandatory

---

## Header

```
Convergence Report
==================

Simulation ID: [SIM-YYYYMMDD-NNN]
Date: [ISO 8601 timestamp]
Iterations Completed: [n] / [n_requested]
Chains: [n_chains]
Early Stopped: [Yes, at iteration N / No]
Overall Verdict: [CONVERGED / MARGINAL / NOT CONVERGED]
```

---

## Summary Table

| # | Estimand | MCSE | MCSE Verdict | R-hat | R-hat Verdict | ESS | ESS Verdict | Overall |
|---|----------|------|-------------|-------|-------------|-----|------------|---------|
| E1 | [name] | [value] | [Pass/Marginal/Fail] | [value or N/A] | [Pass/Marginal/Fail/N/A] | [value] | [Pass/Marginal/Fail] | [Converged/Marginal/Not Converged] |
| E2 | [name] | [value] | [Pass/Marginal/Fail] | [value or N/A] | [Pass/Marginal/Fail/N/A] | [value] | [Pass/Marginal/Fail] | [Converged/Marginal/Not Converged] |
| E3 | [name] | [value] | [Pass/Marginal/Fail] | [value or N/A] | [Pass/Marginal/Fail/N/A] | [value] | [Pass/Marginal/Fail] | [Converged/Marginal/Not Converged] |

### Verdict Thresholds Applied

| Metric | Pass | Marginal | Fail |
|--------|------|----------|------|
| MCSE | < [threshold] | < [2x threshold] | >= [2x threshold] |
| R-hat | < 1.05 | 1.05 - 1.10 | > 1.10 |
| ESS | > 400 | 200 - 400 | < 200 |

MCSE threshold: [value, context-dependent — see diagnostics_agent.md for thresholds by simulation type]

---

## Per-Estimand Detailed Assessment

### Estimand E1: [Name]

#### Description
```
[What this estimand measures, e.g., "Statistical power to detect interaction effect at alpha = .05"]
```

#### Metrics

| Metric | Value | Threshold | Verdict | Notes |
|--------|-------|-----------|---------|-------|
| MCSE | [value to 4 decimal places] | [threshold] | [Pass / Marginal / Fail] | [e.g., "Well below threshold"] |
| R-hat | [value to 3 decimal places] | < 1.05 | [Pass / Marginal / Fail / N/A] | [e.g., "4 chains, split-R-hat"] |
| ESS | [value to nearest integer] | > 400 | [Pass / Marginal / Fail] | [e.g., "ESS ratio = 0.85"] |
| ACF at lag 1 | [value] | — | [Info only] | |
| ACF at lag 5 | [value] | — | [Info only] | |
| ACF at lag 10 | [value] | < 0.1 (ideal) | [Info only] | |
| ACF drops below 0.05 at lag | [value] | — | [Info only] | |

#### Simulation Estimate

```
Point Estimate: [value]
Standard Error: [value]
MCSE: [value]
95% Simulation CI: [lower, upper]  (estimate +/- 1.96 * MCSE)
Bias (if truth known): [value]
```

#### Convergence History

```
Running MCSE at key checkpoints:
  Iteration 500:   MCSE = [value]
  Iteration 1000:  MCSE = [value]
  Iteration 2000:  MCSE = [value]
  Iteration 5000:  MCSE = [value]
  Iteration 10000: MCSE = [value]

Trend: [Monotonically decreasing (good) / Plateaued (adequate) / Fluctuating (concerning)]
```

#### Diagnostic Plots

| Plot | Path | Key Observation |
|------|------|----------------|
| Trace plot | `experiment_outputs/plots/trace_[estimand_name].png` | [e.g., "Stable around mean, good mixing"] |
| ACF plot | `experiment_outputs/plots/acf_[estimand_name].png` | [e.g., "Drops to noise by lag 3"] |
| Distribution plot | `experiment_outputs/plots/dist_[estimand_name].png` | [e.g., "Approximately normal, slight right skew"] |
| Running mean/MCSE | `experiment_outputs/plots/convergence_[estimand_name].png` | [e.g., "MCSE below threshold by iteration 3000"] |

#### Multi-Chain Overlay (if applicable)

| Plot | Path | Key Observation |
|------|------|----------------|
| Multi-chain trace | `experiment_outputs/plots/trace_multichain_[estimand_name].png` | [e.g., "All 4 chains overlap substantially"] |
| Chain means comparison | — | Chain 1: [mean], Chain 2: [mean], Chain 3: [mean], Chain 4: [mean] |

#### Verdict for E1

```
Verdict: [CONVERGED / MARGINAL / NOT CONVERGED]
Reasoning: [1-2 sentence explanation, e.g., "All three metrics pass thresholds. MCSE is well below
the power simulation threshold of 0.005. Trace plot shows excellent mixing across all 4 chains."]
```

---

### Estimand E2: [Name]

[Repeat the same structure as E1]

---

### Estimand E3: [Name]

[Repeat the same structure as E1]

---

## Recommendations [Required if any estimand is Marginal or Not Converged]

### For Marginal Estimands

```
Estimand: [name]
Current Status: Marginal ([which metric(s) are marginal])
Recommendation:
  1. [Specific action, e.g., "Increase iterations from 10,000 to 20,000"]
  2. [Specific action, e.g., "Add 2 more chains for better R-hat assessment"]
Expected Improvement: [What we expect to change]
Priority: [Should fix before reporting / Acceptable with caveats]
```

### For Not Converged Estimands

```
Estimand: [name]
Current Status: Not Converged ([which metric(s) failed])
Diagnosis: [Root cause analysis]
  - [Possible cause 1, e.g., "Multimodal posterior causing chain mixing problems"]
  - [Possible cause 2, e.g., "Heavy-tailed distribution inflating variance"]
Recommendation:
  1. [Specific action with priority]
  2. [Specific action with priority]
  3. [Specific action with priority]
Do NOT Report: Results for this estimand should not be reported until convergence is achieved.
```

### General Recommendations

```
[Any cross-estimand recommendations]

Example:
- All estimands would benefit from longer chains; current ESS ratios suggest
  moderate autocorrelation. Consider increasing iterations by 2x.
- The parameter sweep cells with the smallest sample sizes show the worst
  convergence; consider increasing per-cell iterations for those cells.
```

---

## Execution Environment Confirmation

```
The convergence assessment was performed using:
- MCSE: Standard formula (SD / sqrt(n)) for i.i.d.; batch means for autocorrelated chains
- R-hat: Split-R-hat per Vehtari et al. (2021)
- ESS: FFT-based autocorrelation method
- ACF: Normalized autocovariance via FFT

All computations used the results stored at:
  experiment_outputs/results/raw_results.npz
  experiment_outputs/results/convergence_history.csv
```

---

## Pre-Submission Checklist

- [ ] One assessment block completed per estimand
- [ ] All four metrics computed for each estimand (R-hat marked N/A if single chain / i.i.d.)
- [ ] All diagnostic plots generated and paths verified
- [ ] Overall verdict is the most conservative across estimands
- [ ] Recommendations provided for all Marginal and Not Converged estimands
- [ ] Convergence history shows MCSE trend
- [ ] Multi-chain overlay included (if multiple chains)
- [ ] Summary table at top matches detailed assessments below
