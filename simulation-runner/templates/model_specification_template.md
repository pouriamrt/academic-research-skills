# Model Specification Template — Data-Generating Process Documentation

## Purpose

A fill-in template for documenting the complete data-generating process (DGP) of a simulation. This template ensures that every aspect of the model is explicitly stated: distributions, parameters, functional form, assumptions, and limitations. The completed specification serves as the authoritative reference for what the simulation code implements.

---

## Instructions

1. Complete all sections marked `[Required]`
2. The specification must be detailed enough for an independent researcher to re-implement the DGP from scratch
3. Every parameter must have a default value, a type, and a justification
4. All assumptions must be explicitly stated with their potential impact
5. This document is the "contract" between the conceptual model and the code

---

## 1. Model Overview [Required]

### 1.1 Model Name

```
[Descriptive name for the DGP, e.g., "Two-Group Normal DGP for Power Analysis"]
```

### 1.2 Purpose

```
[What this DGP is designed to simulate and why]
```

### 1.3 Simulation Type

```
Type: [monte_carlo / bootstrap / power_sim / parameter_sweep / agent_based / resampling / stochastic_process / optimization]
```

### 1.4 Conceptual Description

```
[Plain-language description of the data-generating mechanism, accessible to a domain
expert who may not be a programmer. Describe what happens in one realization of the
simulation: what data are generated, how variables are related, what randomness is
involved.]
```

---

## 2. Formal Specification [Required]

### 2.1 Mathematical Model

```
[Formal mathematical notation for the DGP]

Example for a two-group comparison:
  Y_ij = mu + alpha_i + epsilon_ij
  where:
    i = 1, 2 (group index)
    j = 1, ..., n_i (observation index within group)
    mu = grand mean
    alpha_1 = 0 (reference group)
    alpha_2 = delta (treatment effect)
    epsilon_ij ~ N(0, sigma^2)
```

### 2.2 Structural Equations (if multiple stages)

```
[For multi-stage DGPs, list each stage]

Stage 1: Generate covariates
  X ~ [distribution]

Stage 2: Generate treatment assignment
  T | X ~ [mechanism]

Stage 3: Generate outcome
  Y | X, T ~ [model]
```

### 2.3 Functional Form

```
[Explicit functional relationship between variables]

Example:
  Linear: Y = beta_0 + beta_1 * X + epsilon
  Logistic: logit(P(Y=1)) = beta_0 + beta_1 * X
  Interaction: Y = beta_0 + beta_1 * A + beta_2 * B + beta_3 * A * B + epsilon
```

---

## 3. Parameter Table [Required]

| # | Parameter | Symbol | Type | Default | Range | Unit | Source/Justification |
|---|-----------|--------|------|---------|-------|------|---------------------|
| P1 | [name] | [symbol] | [fixed / swept / derived] | [value] | [min, max] or N/A | [unit] | [citation or rationale] |
| P2 | [name] | [symbol] | [fixed / swept / derived] | [value] | [min, max] or N/A | [unit] | [citation or rationale] |
| P3 | [name] | [symbol] | [fixed / swept / derived] | [value] | [min, max] or N/A | [unit] | [citation or rationale] |
| P4 | [name] | [symbol] | [fixed / swept / derived] | [value] | [min, max] or N/A | [unit] | [citation or rationale] |
| P5 | [name] | [symbol] | [fixed / swept / derived] | [value] | [min, max] or N/A | [unit] | [citation or rationale] |

### Parameter Types

- **Fixed**: Constant across all iterations and conditions
- **Swept**: Varied systematically across conditions (parameter sweep)
- **Derived**: Computed from other parameters (document the derivation formula)

### Parameter Constraints

```
[List any constraints on parameter values]

Example:
- sigma > 0 (variance must be positive)
- 0 <= p <= 1 (probability bounded)
- n must be a positive integer
- effect_size >= 0 (for power simulations)
```

---

## 4. Distributions [Required]

| Component | Distribution | Parameters | Notation | numpy Call |
|-----------|-------------|------------|----------|-----------|
| [component name] | [distribution name] | [param = value, ...] | [mathematical notation] | `rng.distribution(params, size=n)` |
| [component name] | [distribution name] | [param = value, ...] | [mathematical notation] | `rng.distribution(params, size=n)` |

### Distribution Justification

For each distribution choice, document:

```
[Component]: [Distribution]
Justification: [Why this distribution was chosen]
Sensitivity: [How sensitive are results to this distributional choice?]
Alternative: [What other distributions were considered?]
```

---

## 5. Assumptions [Required]

List every assumption the model makes, with explicit discussion of impact.

### 5.1 Distributional Assumptions

| # | Assumption | Justification | Impact if Violated | Mitigation |
|---|-----------|---------------|-------------------|-----------|
| A1 | [e.g., Errors are normally distributed] | [e.g., CLT applies for n > 30] | [e.g., Power estimates may be biased for heavy-tailed data] | [e.g., Run sensitivity analysis with t-distribution errors] |
| A2 | [assumption] | [justification] | [impact] | [mitigation] |

### 5.2 Structural Assumptions

| # | Assumption | Justification | Impact if Violated | Mitigation |
|---|-----------|---------------|-------------------|-----------|
| A3 | [e.g., Linear relationship between X and Y] | [e.g., Consistent with prior literature] | [e.g., Nonlinear effects would reduce power] | [e.g., Add quadratic term in sensitivity analysis] |
| A4 | [assumption] | [justification] | [impact] | [mitigation] |

### 5.3 Independence Assumptions

| # | Assumption | Justification | Impact if Violated | Mitigation |
|---|-----------|---------------|-------------------|-----------|
| A5 | [e.g., Observations within groups are independent] | [e.g., No repeated measures] | [e.g., Inflated Type I error if correlated] | [e.g., Model correlation structure explicitly] |
| A6 | [assumption] | [justification] | [impact] | [mitigation] |

---

## 6. Output Specification [Required]

### 6.1 Per-Iteration Output

```
Each iteration of the DGP returns a dictionary with the following keys:

{
    'data': {
        [key]: [type, shape, description]
        [key]: [type, shape, description]
    },
    'truth': {
        [key]: [type, description — the true parameter values for this iteration]
        [key]: [type, description]
    }
}
```

### 6.2 Per-Iteration Analysis Output

```
The analysis function applied to each iteration's data returns:

{
    [key]: [type, description]
    [key]: [type, description]
}
```

### 6.3 Aggregated Output (across all iterations)

```
The final aggregated results contain:

{
    [estimand]: {
        'estimate': [mean across iterations],
        'se': [standard deviation across iterations],
        'mcse': [SE / sqrt(n_iterations)],
        'ci_lower': [2.5th percentile],
        'ci_upper': [97.5th percentile],
    }
}
```

---

## 7. Limitations [Required]

### 7.1 Known Limitations

| # | Limitation | Impact on Results | Severity |
|---|-----------|-------------------|----------|
| L1 | [limitation description] | [how it affects interpretation] | [Low/Medium/High] |
| L2 | [limitation description] | [how it affects interpretation] | [Low/Medium/High] |
| L3 | [limitation description] | [how it affects interpretation] | [Low/Medium/High] |

### 7.2 Simplifications

```
[List any simplifications made relative to the real-world phenomenon being modeled]

Example:
- Real data may have missing values; this DGP generates complete data
- Real effect sizes may vary across participants; this DGP uses fixed effects
- Real errors may be heteroscedastic; this DGP assumes constant variance
```

### 7.3 Generalizability Boundaries

```
[Define the conditions under which simulation results are expected to be valid]

Results are expected to generalize when:
- [condition 1]
- [condition 2]

Results may NOT generalize when:
- [condition 1]
- [condition 2]
```

---

## 8. Code Reference [Required]

```
Implementation file: experiment_outputs/scripts/dgp_functions.py
Main function: dgp(rng: Generator, params: dict) -> dict
Analysis function: analyze(data: dict, params: dict) -> dict
Performance function: measure_performance(results: list, truth: dict) -> dict

Test: Run with default parameters and seed=42 to verify output structure.
```

---

## 9. Validation [Required]

### 9.1 Sanity Checks

```
[List checks performed to validate that the DGP behaves as expected]

1. Under H0 (no effect): mean difference should be approximately 0
2. Under H1 (effect present): mean difference should be approximately delta
3. Sample variance should be approximately sigma^2
4. Group sizes should be approximately equal (if balanced design)
```

### 9.2 Known Analytical Results

```
[If analytical solutions exist for special cases, verify the simulation matches]

Example:
- For n=1000, delta=0.5, sigma=1, alpha=0.05:
  Analytical power (two-sample t-test) = 0.XXX
  Simulated power (10,000 iterations) = 0.XXX (MCSE = 0.00X)
  Agreement: [within MCSE / discrepancy noted]
```

---

## Pre-Completion Checklist

- [ ] All [Required] sections completed
- [ ] Mathematical model is unambiguous and complete
- [ ] Every parameter has a default value, type, and justification
- [ ] All distributions are specified with exact parameter values
- [ ] Assumptions are explicitly listed with impact analysis
- [ ] Output structure is documented for both per-iteration and aggregated results
- [ ] Code reference points to a working implementation
- [ ] Sanity checks have been performed and documented
- [ ] An independent researcher could re-implement the DGP from this document alone
