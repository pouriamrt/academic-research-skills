# Simulation Design Patterns — Type Selection Decision Tree & Reference

## Purpose

A comprehensive reference for selecting the appropriate simulation type and designing its structure. Covers all 8 simulation types supported by `simulation-runner`, with decision criteria, model structures, key parameters, convergence criteria, and recommended Python libraries.

---

## Decision Tree: Which Simulation Type?

```
What is your research question?
    |
    +-- "What is the statistical power of my planned analysis?"
    |   --> POWER SIMULATION (Section 3)
    |
    +-- "How precise is my estimate? What's the CI?"
    |   +-- Do you have observed data?
    |   |   +-- Yes --> BOOTSTRAP (Section 2)
    |   |   +-- No --> MONTE CARLO (Section 1)
    |   |
    +-- "How sensitive are my results to model assumptions?"
    |   --> PARAMETER SWEEP (Section 4)
    |
    +-- "How do individual agents/units interact to produce macro behavior?"
    |   --> AGENT-BASED MODEL (Section 5)
    |
    +-- "Is there a significant difference/effect (nonparametric test)?"
    |   --> RESAMPLING / PERMUTATION (Section 6)
    |
    +-- "How does a system evolve over time with randomness?"
    |   --> STOCHASTIC PROCESS (Section 7)
    |
    +-- "What parameter values optimize an objective function?"
    |   --> OPTIMIZATION (Section 8)
    |
    +-- "I want to estimate a distributional property by repeated sampling"
    |   --> MONTE CARLO (Section 1)
```

### Secondary Decision Criteria

| Factor | Favors | Over |
|--------|--------|------|
| Have observed data | Bootstrap, Resampling | Monte Carlo, Power sim |
| Need power estimate | Power simulation | Monte Carlo |
| Need to vary assumptions | Parameter sweep | Single Monte Carlo |
| Model agent interactions | Agent-based | Monte Carlo |
| Need exact p-value without distributional assumptions | Permutation test | Parametric Monte Carlo |
| Time-varying system | Stochastic process | Static Monte Carlo |
| Search for optimal solution | Optimization | Exhaustive sweep |

---

## Section 1: Monte Carlo Simulation

### When to Use

- Estimating distributional properties (means, variances, quantiles) of a statistic
- Evaluating estimator properties (bias, MSE, coverage) under known conditions
- Approximating integrals or expectations that lack closed-form solutions
- Validating analytical results with numerical evidence

### Model Structure

```
For each iteration i = 1, ..., N:
    1. Generate data from DGP: X_i ~ F(theta)
    2. Compute statistic: T_i = g(X_i)
    3. Store T_i

After all iterations:
    Estimate = mean(T_1, ..., T_N)
    SE = sd(T_1, ..., T_N)
    MCSE = SE / sqrt(N)
```

### Key Parameters

| Parameter | Typical Range | Guidance |
|-----------|---------------|----------|
| n_iterations | 1,000 - 1,000,000 | More = more precise; 10,000 is a solid default |
| sample_size | Depends on context | Match planned study design |
| distribution_params | Problem-specific | Calibrate from pilot data or literature |
| seed | Any integer | Record for reproducibility |

### Convergence Criterion

- Primary: MCSE < desired precision (e.g., < 0.01 for proportions, < 0.1 for continuous)
- Secondary: Running mean stabilizes (visual check via trace plot)
- Rule of thumb: For estimating a proportion p, need N > 100 / (p * (1-p)) for MCSE < 0.01

### Python Libraries

- `numpy` (core): `rng.normal()`, `rng.uniform()`, `rng.choice()`, all `Generator` methods
- `scipy.stats`: Named distributions, PDF/CDF/PPF, statistical tests
- `statsmodels`: Regression, GLM, time series models

### Common Pitfalls

1. Using `np.random.seed()` instead of `Generator` — breaks parallel reproducibility
2. Insufficient iterations for rare events (p < 0.01 needs N > 10,000)
3. Not checking convergence — reporting unstable estimates as final
4. Confusing SE of the statistic with MCSE of the simulation

---

## Section 2: Bootstrap

### When to Use

- Constructing confidence intervals without distributional assumptions
- Estimating standard errors for complex statistics (medians, ratios, correlations)
- Bias correction for point estimates
- Inference when analytical formulas are unavailable or unreliable

### Model Structure

```
Given observed data X = (x_1, ..., x_n):

For each bootstrap replicate b = 1, ..., B:
    1. Draw bootstrap sample: X*_b = sample_with_replacement(X, size=n)
    2. Compute statistic: T*_b = g(X*_b)
    3. Store T*_b

Confidence Intervals:
    Percentile: [T*_(alpha/2), T*_(1-alpha/2)]
    BCa: bias and acceleration corrected percentiles
    Studentized: (T - T*) / SE* quantiles
```

### Bootstrap Variants

| Variant | When to Use | Accuracy | Complexity |
|---------|-------------|----------|------------|
| Percentile | Simple, symmetric distributions | First-order | Low |
| BCa (bias-corrected and accelerated) | Skewed distributions, general use | Second-order | Medium |
| Studentized (bootstrap-t) | When SE can be computed per resample | Second-order | High |
| Parametric bootstrap | When distribution family is known | Depends on model | Medium |
| Stratified bootstrap | Grouped data, rare outcomes | Improves on unstratified | Medium |
| Block bootstrap | Time series, spatial data | Preserves dependence | Medium |

### Key Parameters

| Parameter | Typical Range | Guidance |
|-----------|---------------|----------|
| n_bootstrap | 1,000 - 50,000 | 10,000 for CIs; 1,000 may suffice for SEs |
| confidence_level | 0.90, 0.95, 0.99 | 0.95 is standard |
| method | percentile, bca, studentized | BCa recommended as default |
| data_size | n >= 20 | Warn if n < 50; bootstrap is unreliable for very small n |

### Convergence Criterion

- MCSE of CI bounds < 0.5% of CI width
- Bootstrap distribution shape stabilizes (check at 1,000, 5,000, 10,000)
- For BCa: acceleration constant stabilizes

### Python Libraries

- `numpy`: `rng.choice(n, size=n, replace=True)` for resampling
- `scipy.stats`: For parametric bootstrap distributions
- `scipy.stats.bootstrap` (scipy >= 1.7): Built-in BCa bootstrap

### Common Pitfalls

1. Bootstrapping with n < 15 — results are unstable and misleading
2. Using percentile intervals when data are skewed — use BCa instead
3. Not accounting for clustering — use block or cluster bootstrap
4. Interpreting bootstrap distribution as posterior distribution — they are different

---

## Section 3: Power Simulation

### When to Use

- Estimating statistical power for a planned study
- Determining required sample size to achieve target power
- Evaluating power under realistic (non-ideal) conditions
- Comparing power across alternative analysis strategies

### Model Structure

```
For each sample size n in sample_sizes:
    For each iteration i = 1, ..., N:
        1. Generate data under H1: X_i ~ DGP(effect_size, n)
        2. Run planned statistical test: p_i = test(X_i)
        3. Record: significant_i = (p_i < alpha)

    Power(n) = mean(significant_1, ..., significant_N)
    MCSE(Power) = sqrt(Power * (1-Power) / N)

Also run under H0 (effect_size = 0) to verify Type I error rate.
```

### Key Parameters

| Parameter | Typical Range | Guidance |
|-----------|---------------|----------|
| n_sim | 5,000 - 50,000 | 10,000 recommended; MCSE < 0.005 for power |
| sample_sizes | 20 - 500 | Range around expected required n |
| effect_size | Problem-specific | Use pilot data, meta-analysis, or SESOI |
| alpha | 0.05, 0.01, 0.005 | Match planned analysis |
| test | t-test, ANOVA, regression, etc. | Match planned analysis exactly |

### Convergence Criterion

- MCSE of power < 0.005 (so power of 0.80 is reported as 0.800 +/- 0.005)
- Type I error rate within simulation CI of nominal alpha
- Power monotonically increases with sample size (sanity check)

### Python Libraries

- `numpy`, `scipy.stats`: DGP and standard tests
- `statsmodels`: ANOVA, regression, mixed models
- `pingouin`: ANOVA with effect sizes, repeated measures

### Common Pitfalls

1. Simulating under H0 conditions when H1 is intended (effect_size = 0 accidentally)
2. Not verifying Type I error rate (power is meaningless if test is miscalibrated)
3. Using effect sizes from significant-only studies (inflated by publication bias)
4. Not accounting for multiple comparisons, dropout, or clustering in the DGP

---

## Section 4: Parameter Sweep

### When to Use

- Sensitivity analysis: how sensitive are results to model assumptions?
- Identifying which parameters most influence the outcome
- Finding the "robust region" where results meet a criterion
- Mapping the response surface across multiple conditions

### Model Structure

```
Define parameter grid: G = P1_values x P2_values x ... x Pk_values

For each cell c in G:
    For each iteration i = 1, ..., N:
        1. Generate data: X_i ~ DGP(params_c)
        2. Analyze: R_i = analyze(X_i)

    Estimand(c) = aggregate(R_1, ..., R_N)
    MCSE(c) = compute_mcse(R_1, ..., R_N)
```

### Key Parameters

| Parameter | Typical Range | Guidance |
|-----------|---------------|----------|
| n_parameters | 2 - 10 | Curse of dimensionality above 5; use Latin hypercube |
| values_per_param | 3 - 20 | 5-7 per parameter is typical for one-at-a-time |
| n_per_cell | 500 - 5,000 | Lower than full Monte Carlo; precision per cell is less critical |
| sweep_type | OAT, factorial, LHS | OAT for initial exploration; factorial for interactions |

### Convergence Criterion

- Per-cell MCSE < 0.05 (looser than full Monte Carlo, since many cells)
- Total runtime < budget (grid explosion is the main risk)
- Robust region boundaries stable to +/- 1 grid step

### Python Libraries

- `itertools.product`: Full factorial grid
- `scipy.stats.qmc.LatinHypercube`: Latin hypercube sampling
- `joblib`: Parallel execution across cells
- `matplotlib`: Heatmaps, tornado plots, spider plots

### Common Pitfalls

1. Full factorial with > 5 parameters (grid explosion: 5^5 = 3,125 cells at 5 values each)
2. Not exploring interactions (one-at-a-time misses synergistic/antagonistic effects)
3. Reporting sensitivity without a robust region definition
4. Confusing parameter sensitivity with parameter uncertainty

---

## Section 5: Agent-Based Model

### When to Use

- Studying emergent behavior from individual-level rules
- Modeling systems with heterogeneous agents on networks
- Investigating tipping points, phase transitions, cascading effects
- When macro-level behavior cannot be derived analytically from micro-level rules

### Model Structure

```
Initialize:
    1. Create N agents with initial states
    2. Build interaction topology (network)

For each time step t = 1, ..., T:
    For each agent a (in randomized order):
        1. Observe neighbor states
        2. Apply decision rules
        3. Update state

    Record macro-level summary statistics at step t

Steady-state analysis:
    Detect when summary statistics stabilize
    Report steady-state values and transition dynamics
```

### Key Parameters

| Parameter | Typical Range | Guidance |
|-----------|---------------|----------|
| n_agents | 50 - 10,000 | Depends on phenomenon; finite-size effects below 100 |
| topology | complete, grid, small_world, scale_free | Match real network structure |
| n_steps | 100 - 10,000 | Until steady state is reached |
| n_runs | 50 - 500 | Multiple runs for stochastic variability |
| update_order | random, synchronous, sequential | Random is most common |

### Convergence Criterion

- Steady-state detection: summary statistics stable for > 100 steps
- Cross-run variance: MCSE across runs < threshold
- Sensitivity to n_agents: results stable across 2x and 0.5x agent counts

### Python Libraries

- `networkx`: Graph creation, analysis, visualization
- `numpy`: Agent state arrays, random updates
- `mesa` (optional): Full ABM framework
- `matplotlib`: Network visualization, time series

### Common Pitfalls

1. Too few agents for the phenomenon being studied (finite-size effects)
2. Not testing sensitivity to network topology
3. Order effects: synchronous vs. asynchronous update can change outcomes
4. Not running enough replications (ABMs have high stochastic variance)

---

## Section 6: Resampling & Cross-Validation

### When to Use

- Permutation tests: exact p-values without distributional assumptions
- Cross-validation: estimate out-of-sample prediction error
- Jackknife: bias estimation and variance computation
- Any inference where exchangeability holds but distribution is unknown

### Model Structure (Permutation Test)

```
Observed test statistic: T_obs = test(data)

For each permutation p = 1, ..., N_perm:
    1. Randomly permute group labels
    2. Compute test statistic: T*_p = test(permuted_data)

p-value = (count(T*_p >= T_obs) + 1) / (N_perm + 1)
```

### Key Parameters

| Parameter | Typical Range | Guidance |
|-----------|---------------|----------|
| n_permutations | 1,000 - 100,000 | 10,000 for reliable p-values; exact for small n |
| folds (CV) | 5, 10, LOOCV | 10-fold is standard; LOOCV for small n |
| statistic | mean_diff, t_stat, correlation | Match research question |

### Convergence Criterion

- p-value MCSE < 0.001 (N_perm > 10,000 for p near 0.05)
- For CV: stable mean error across repeated CV runs

### Python Libraries

- `numpy`: Permutation via `rng.permutation()`
- `scipy.stats.permutation_test` (scipy >= 1.8)
- `scikit-learn`: `cross_val_score`, `KFold`, `StratifiedKFold`

---

## Section 7: Stochastic Processes

### When to Use

- Modeling systems that evolve over time with randomness (Markov chains, queues, diffusion)
- Estimating long-run properties (stationary distribution, mean recurrence time)
- Financial modeling (geometric Brownian motion, jump diffusion)
- Population dynamics (birth-death processes, branching processes)

### Model Structure

```
Initialize: X_0 = initial_state

For each step t = 1, ..., T:
    X_t = transition(X_{t-1}, params, rng)

Analysis:
    Burn-in: discard first B steps
    Stationary distribution: histogram of X_{B+1}, ..., X_T
    Mixing time: autocorrelation analysis
```

### Key Parameters

| Parameter | Typical Range | Guidance |
|-----------|---------------|----------|
| n_steps | 1,000 - 1,000,000 | Depends on mixing time |
| burn_in | 10-50% of n_steps | Longer for slow-mixing chains |
| transition_matrix | Problem-specific | Must be stochastic (rows sum to 1) |
| step_size (diffusion) | Problem-specific | Euler-Maruyama stability |

### Convergence Criterion

- Stationarity: distribution of states stable across time windows
- Mixing time: autocorrelation drops below 0.05 within reasonable lag
- R-hat < 1.05 across multiple independent chains

### Python Libraries

- `numpy`: Transition matrices, random walks
- `scipy.linalg`: Eigenvalue decomposition for stationary distribution
- `scipy.integrate`: SDE solvers

---

## Section 8: Optimization

### When to Use

- Finding parameter values that minimize/maximize an objective function
- Stochastic optimization when the objective involves randomness
- Simulated annealing for combinatorial problems
- Genetic algorithms for multi-modal objective landscapes

### Model Structure

```
Define: objective_function(params) -> scalar
Define: bounds for each parameter
Define: n_restarts for multi-start optimization

For each restart r = 1, ..., n_restarts:
    1. Initialize from random starting point
    2. Run optimization algorithm
    3. Record best solution

Best overall = best across all restarts
```

### Key Parameters

| Parameter | Typical Range | Guidance |
|-----------|---------------|----------|
| n_restarts | 10 - 100 | More for multi-modal landscapes |
| tolerance | 1e-6 to 1e-3 | Tighter for precise optimization |
| max_iterations | 100 - 10,000 | Per restart |
| bounds | Problem-specific | Required for bounded optimization |

### Convergence Criterion

- Objective function value stable across restarts
- Multiple restarts find the same optimum (global vs. local)
- Gradient norm < tolerance

### Python Libraries

- `scipy.optimize`: `minimize`, `differential_evolution`, `dual_annealing`
- `numpy`: Objective function evaluation

---

## Cross-Type Comparison Matrix

| Feature | Monte Carlo | Bootstrap | Power Sim | Sweep | ABM | Resampling | Stochastic | Optimization |
|---------|------------|-----------|-----------|-------|-----|-----------|-----------|-------------|
| Requires observed data | No | Yes | No | No | No | Yes | No | No |
| Iterations | 10K+ | 10K+ | 10K+ | 1K/cell | 50-500 runs | 10K+ | 1M steps | 10-100 restarts |
| Parallelizable | Yes | Yes | Yes | Yes (cells) | Yes (runs) | Yes | Yes (chains) | Yes (restarts) |
| Key metric | MCSE | CI width | Power | Range | Steady state | p-value | Mixing time | Objective |
| Main output | Estimate + CI | CI | Power curve | Sensitivity map | Time series | p-value | Distribution | Optimum |
| Typical runtime | Minutes | Minutes | Minutes-hours | Minutes-hours | Minutes-hours | Seconds-minutes | Minutes | Seconds-minutes |

---

## References

- Morris, T. P., White, I. R., & Crowther, M. J. (2019). Using simulation studies to evaluate statistical methods. *Statistics in Medicine*, 38(11), 2074-2102. doi:10.1002/sim.8086
- Davison, A. C., & Hinkley, D. V. (1997). *Bootstrap methods and their application*. Cambridge University Press.
- Efron, B., & Tibshirani, R. (1993). *An introduction to the bootstrap*. Chapman & Hall.
- Gilbert, N. (2019). *Agent-based models* (2nd ed.). SAGE Publications.
- Robert, C. P., & Casella, G. (2004). *Monte Carlo statistical methods* (2nd ed.). Springer.
