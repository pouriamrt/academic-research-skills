# Convergence Criteria Guide — When to Stop a Simulation

## Purpose

A comprehensive reference for determining when a simulation has run long enough to produce reliable results. Covers numerical criteria (MCSE, R-hat, ESS), visual diagnostics, early stopping rules, and remediation strategies when convergence fails.

---

## The Three Pillars of Convergence

A simulation is declared **converged** when ALL three criteria are simultaneously met:

| Pillar | Metric | Threshold | What It Means |
|--------|--------|-----------|---------------|
| Precision | MCSE | < context-specific threshold | Simulation estimate is precise enough for the research question |
| Mixing | R-hat | < 1.05 | Multiple independent chains agree (exploring the same distribution) |
| Independence | ESS | > 400 | Enough effectively independent samples for reliable inference |

If any one pillar fails, the simulation is **not converged**, and results should not be reported as final.

---

## Pillar 1: Monte Carlo Standard Error (MCSE)

### Definition

MCSE quantifies the simulation-induced uncertainty in an estimate. It answers: "If I ran this simulation again with different seeds, how much would the result change?"

```
MCSE = SD(estimand_values) / sqrt(n_effective)
```

For i.i.d. iterations: `n_effective = n_iterations`
For autocorrelated chains: `n_effective = ESS`

### Context-Specific Thresholds

The acceptable MCSE depends on the precision needed for the research question.

| Simulation Context | Target MCSE | Rationale | Iterations Needed (approx.) |
|-------------------|-------------|-----------|----------------------------|
| Power estimation | < 0.005 | Power of 0.80 vs 0.81 matters for sample size planning | ~10,000 for power near 0.50; fewer for extreme power |
| Type I error verification | < 0.002 | Must verify alpha = 0.05 precisely | ~25,000 |
| Bootstrap CI bounds | < 1% of CI width | CI precision must be much finer than CI width | ~10,000 |
| Monte Carlo mean estimate | < 1% of SD | Estimate precise relative to variability | ~10,000 |
| Parameter sweep (per cell) | < 5% of range across cells | Cells must be distinguishable | ~1,000-5,000 |
| ABM steady-state | < 5% of steady-state SD | Long-run behavior stable | ~500 runs |

### Computing Iterations Needed

Given a target MCSE and the variability of the estimand:

```
n_needed = (SD / target_MCSE)^2
```

For proportions (power, coverage):
```
n_needed = p * (1 - p) / target_MCSE^2

Example: For power = 0.80, target MCSE = 0.005:
n_needed = 0.80 * 0.20 / 0.005^2 = 6,400 iterations
```

### MCSE for Functions of Simulation Output

For estimates that are functions of the raw simulation output (e.g., CI width, quantiles), use the delta method:

```
MCSE(f(theta_hat)) ≈ |f'(theta_hat)| * MCSE(theta_hat)
```

Or, for complex functions, compute MCSE via batch means:
1. Divide N iterations into k batches of size m = N/k
2. Compute the estimate within each batch
3. MCSE = SD(batch_estimates) / sqrt(k)

---

## Pillar 2: R-hat (Potential Scale Reduction Factor)

### Definition

R-hat compares the variance within independent chains to the variance between chains. If chains are exploring different regions of the parameter space, between-chain variance will be large relative to within-chain variance, yielding R-hat >> 1.

### Split-R-hat (Recommended)

Split each chain in half before computing R-hat. This catches within-chain non-stationarity (e.g., a chain that drifts over time).

```
m_split = 2 * m_chains (each chain split in half)
n = length of each half-chain

B = n * Var(chain_half_means)     [between-chain variance]
W = Mean(Var(each_chain_half))    [within-chain variance]

var_hat = ((n-1)/n) * W + (1/n) * B
R-hat = sqrt(var_hat / W)
```

### Thresholds

| R-hat | Verdict | Action |
|-------|---------|--------|
| < 1.01 | Excellent | Proceed with confidence |
| < 1.05 | Adequate | Standard threshold; proceed |
| 1.05 - 1.10 | Marginal | Run longer; report with caveat |
| > 1.10 | Not converged | Do NOT report; diagnose and fix |
| > 2.0 | Severely non-converged | Chains exploring completely different regions; model issue |

### When R-hat is Not Applicable

R-hat requires multiple independent chains. It is **not applicable** for:
- Single-chain simulations (use MCSE + ESS only)
- Bootstrap (resamples are i.i.d. by construction; R-hat is always near 1.0)
- Pure Monte Carlo with i.i.d. iterations (no chain structure)
- Permutation tests (permutations are exchangeable)

In these cases, mark R-hat as "N/A" and rely on MCSE and ESS.

### Minimum Chains for Reliable R-hat

- 2 chains: Minimum; can detect gross non-convergence
- 4 chains: Recommended; standard in Bayesian computation (Stan default)
- 8+ chains: For publication-quality convergence assessment

---

## Pillar 3: Effective Sample Size (ESS)

### Definition

ESS estimates the number of i.i.d. samples that would provide the same precision as the actual (potentially autocorrelated) samples.

```
ESS = n / (1 + 2 * sum(positive_autocorrelations))
```

### Thresholds

| ESS | Verdict | What It Means |
|-----|---------|---------------|
| > 1,000 | Excellent | Highly reliable estimates |
| > 400 | Adequate | Standard minimum for publication |
| 200 - 400 | Marginal | Estimates imprecise; consider more iterations |
| 100 - 200 | Poor | Substantial imprecision; not recommended |
| < 100 | Insufficient | Do NOT report; chain is severely autocorrelated |

### ESS Ratio

```
ESS_ratio = ESS / n_iterations
```

| ESS Ratio | Interpretation |
|-----------|---------------|
| > 0.80 | Near-i.i.d. behavior; excellent |
| 0.50 - 0.80 | Low autocorrelation; good |
| 0.10 - 0.50 | Moderate autocorrelation; acceptable but could improve |
| < 0.10 | High autocorrelation; problematic |
| < 0.01 | Severe autocorrelation; reparameterize or thin aggressively |

### Improving ESS

1. **Run longer**: ESS increases linearly with n_iterations (if chain is stationary)
2. **Thin the chain**: Keep every k-th sample; reduces autocorrelation but wastes computation
3. **Reparameterize**: Transform parameters to reduce correlation (e.g., centering, scaling)
4. **Improve mixing**: Modify the DGP or MCMC algorithm for better exploration

---

## Visual Diagnostics

### Trace Plot Assessment

| Pattern | Verdict | Action |
|---------|---------|--------|
| "Hairy caterpillar" — random fluctuations around stable mean | Good mixing | Proceed |
| Upward/downward trend | Non-stationarity | Increase burn-in or check for time-varying parameters |
| Periodic oscillations | Autocorrelation | Thin or reparameterize |
| Long flat sections ("sticky") | Poor mixing | Check for multimodality or strong correlations |
| Sudden jumps between levels | Multimodality | Run more chains; report multiple modes |
| Diverging chains (moving apart) | Non-convergence | Model misspecification; review DGP |

### Autocorrelation Plot Assessment

| Pattern | Verdict | Action |
|---------|---------|--------|
| Drops to zero within 5 lags | Excellent mixing | ESS near n_iterations |
| Drops to zero within 20 lags | Acceptable | ESS adequate |
| Slow decay (geometric) | Moderate autocorrelation | Run longer; ESS may be < 50% of n |
| Does not decay (flat near 1.0) | Severe autocorrelation | Reparameterize; model may be poorly specified |
| Negative autocorrelation (alternating) | Anti-persistent | Usually harmless; ESS may exceed n |

### Distribution Plot Assessment

| Pattern | Verdict | Action |
|---------|---------|--------|
| Unimodal, approximately symmetric | Expected for most estimands | Proceed |
| Unimodal, skewed | Check if expected given DGP | Report median and quantile-based CI |
| Bimodal or multimodal | Multiple modes in DGP | Investigate; may need mode-specific analysis |
| Heavy tails | High variance of estimand | Increase iterations; consider robust estimators |
| Spike at boundary | Truncation or floor/ceiling effect | Check DGP for constraints |

---

## Early Stopping Rules

### When to Stop Early (Converged)

Check every `check_interval` iterations (default: 500). Stop if ALL of the following are true for ALL estimands:

1. MCSE < target threshold
2. R-hat < 1.05 (if multiple chains)
3. ESS > 400
4. Running mean has been stable for > 2 * check_interval iterations

### When to Stop Early (Divergence)

Stop immediately and flag as pathological if:

1. MCSE is increasing over the last 3 check intervals (divergence)
2. R-hat > 5.0 (chains in completely different regions)
3. Any numerical overflow or NaN detected in results
4. Single iteration runtime exceeds 60 seconds (likely infinite loop or explosion)

### Maximum Iterations

Even if not converged, stop at the configured maximum to prevent runaway computation. Report the current convergence status and recommend next steps.

| Mode | Default Maximum | Rationale |
|------|----------------|-----------|
| full | 100,000 | Generous ceiling for complex simulations |
| quick | 5,000 | Quick results, less precision |
| power-sim | 50,000 | Power estimates need high precision |
| sensitivity | 10,000 per cell | Many cells; per-cell precision can be lower |
| bootstrap | 50,000 | Bootstrap is fast; generous ceiling |

---

## What to Do When Convergence Fails

### Diagnosis Flowchart

```
Not converged
    |
    +-- Which metric(s) failed?
        |
        +-- MCSE too high, ESS adequate, R-hat OK
        |   --> Just need more iterations. Double n_iterations.
        |
        +-- R-hat too high
        |   +-- Trace plots show different levels across chains
        |   |   --> Multimodality in DGP. Investigate model specification.
        |   +-- Trace plots show slow drift
        |   |   --> Increase burn-in. Check for non-stationarity.
        |   +-- One chain stuck, others OK
        |       --> Bad initialization. Increase warm-up or diversify starting points.
        |
        +-- ESS too low
        |   +-- ACF decays slowly
        |   |   --> High autocorrelation. Thin or reparameterize.
        |   +-- ACF does not decay
        |   |   --> Model is poorly specified. Revisit DGP.
        |   +-- ESS << n_iterations despite i.i.d. design
        |       --> Bug in seed management. Verify Generator usage.
        |
        +-- All metrics marginal
            --> Run 2x more iterations. Usually resolves borderline cases.
```

### Remediation Priority

| Action | Effort | Typical Impact |
|--------|--------|---------------|
| Increase iterations 2x | Low | Reduces MCSE by sqrt(2) |
| Increase iterations 4x | Low | Reduces MCSE by 2x |
| Add more chains (4 -> 8) | Low | Better R-hat assessment |
| Increase burn-in | Low | Helps with drift/non-stationarity |
| Thin the chain | Low | Improves ESS ratio but wastes samples |
| Reparameterize DGP | Medium | Can dramatically improve ESS |
| Simplify model | Medium | Reduces per-iteration variance |
| Use different algorithm | High | May resolve fundamental mixing issues |
| Increase n_agents (ABM) | Medium | Reduces stochastic variance |

---

## Special Cases

### Bootstrap Convergence

Bootstrap resamples are i.i.d. by construction, so:
- R-hat is N/A
- ESS = n_bootstrap (always)
- Only MCSE matters
- Convergence is almost always achieved with 10,000 resamples

### Power Simulation Convergence

Power is a proportion, so:
- MCSE = sqrt(power * (1-power) / n_sim)
- MCSE is maximized at power = 0.50 (MCSE = 0.005 at n_sim = 10,000)
- Power near 0 or 1 converges faster (lower variance)
- Verify Type I error converges separately (should match nominal alpha)

### Parameter Sweep Convergence

Each cell converges independently:
- Per-cell MCSE should be reported
- Some cells may converge faster than others
- Worst-converging cells drive the overall verdict
- For large grids (> 100 cells), report the fraction of converged cells

### ABM Convergence

Agent-based models require two levels of convergence:
1. **Within-run**: steady state reached (summary statistics stable for > 100 steps)
2. **Across-run**: MCSE across independent runs is acceptable

Both levels must be assessed. High stochastic variance across runs is common and expected; adjust n_runs accordingly.

---

## References

- Vehtari, A., Gelman, A., Simpson, D., Carpenter, B., & Burkner, P. C. (2021). Rank-normalization, folding, and localization: An improved R-hat for assessing convergence of MCMC. *Bayesian Analysis*, 16(2), 667-718.
- Flegal, J. M., & Jones, G. L. (2010). Batch means and spectral variance estimators in Markov chain Monte Carlo. *Annals of Statistics*, 38(2), 1034-1070.
- Morris, T. P., White, I. R., & Crowther, M. J. (2019). Using simulation studies to evaluate statistical methods. *Statistics in Medicine*, 38(11), 2074-2102.
- Koehler, E., Brown, E., & Haneuse, S. J. (2009). On the assessment of Monte Carlo error in simulation-based statistical analyses. *The American Statistician*, 63(2), 155-162.
