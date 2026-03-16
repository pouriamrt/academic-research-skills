# Reporting Simulation Studies — ADEMP Framework & Best Practices

## Purpose

A comprehensive reference for reporting computational simulation studies in academic publications. Based on the ADEMP framework (Aims, Data-Generating Process, Estimands, Methods, Performance) as recommended by Morris et al. (2019). Includes a full checklist, reporting table format, and guidance for translating simulation results into publishable text.

---

## The ADEMP Framework

Morris et al. (2019) propose a structured framework for planning and reporting simulation studies. Every simulation study should address five components:

### A — Aims

**What question does this simulation answer?**

The aims section must clearly state:
1. The specific research question the simulation addresses
2. Why simulation is necessary (i.e., why analytical solutions are insufficient)
3. What the simulation is expected to demonstrate or evaluate

**Reporting checklist for Aims:**
- [ ] Research question is stated precisely
- [ ] Justification for simulation (vs. analytical solution) is provided
- [ ] Specific hypotheses or expectations are pre-stated (if applicable)
- [ ] Scope of the simulation is defined (what it does and does not address)

**Example:**
> "This simulation study aims to evaluate the statistical power of the planned 2 x 3 mixed ANOVA to detect the hypothesized interaction effect across a range of sample sizes (N = 30 to 300 per group). Analytical power calculations for mixed designs with non-spherical covariance structures are not available in closed form, necessitating a simulation approach."

### D — Data-Generating Process (DGP)

**How are simulated data created?**

The DGP section must fully specify the mechanism by which data are generated. Another researcher should be able to re-implement the DGP from this description alone.

**Reporting checklist for DGP:**
- [ ] Mathematical model is specified (equations, functional form)
- [ ] All parameters are listed with values and justifications
- [ ] All distributions are named with their parameters
- [ ] Assumptions are explicitly stated
- [ ] Any data transformations or processing are described
- [ ] For multiple DGP scenarios, each scenario is described
- [ ] Code is available (or DGP is simple enough to re-implement from text)

**Required parameter table format:**

| Parameter | Symbol | Value(s) | Justification |
|-----------|--------|----------|---------------|
| Sample size | *n* | 30, 60, 90, 120, 180, 240, 300 | Range around expected required *n* |
| Effect size (interaction) | *f* | 0, 0.10, 0.15, 0.20, 0.25, 0.30, 0.40 | Cohen's conventions + SESOI |
| Error variance | sigma^2 | 100 | Based on pilot study |
| Correlation (within-subject) | rho | 0.5 | Moderate correlation per literature |

### E — Estimands

**What quantities are being estimated?**

The estimands section must precisely define what is being measured from each simulation iteration.

**Reporting checklist for Estimands:**
- [ ] Each estimand is named and defined
- [ ] True values are stated (if known from the DGP)
- [ ] Units are specified
- [ ] The relationship between estimands and the research question is clear

**Common estimands in simulation studies:**

| Estimand | Definition | When to Use |
|----------|-----------|-------------|
| Power | P(reject H0 \| H1 true) | Power analysis |
| Type I error | P(reject H0 \| H0 true) | Calibration check |
| Bias | E[theta_hat] - theta | Estimator evaluation |
| MSE | E[(theta_hat - theta)^2] | Estimator evaluation |
| Coverage | P(CI contains theta) | CI evaluation |
| CI width | Mean width of CIs | CI evaluation |
| Rejection rate | Proportion of p < alpha | Any hypothesis test |
| Effect size estimate | Mean of estimated effect sizes | Effect size accuracy |

### M — Methods

**What statistical methods are applied to each simulated dataset?**

The methods section describes the analysis applied to each iteration of simulated data.

**Reporting checklist for Methods:**
- [ ] Statistical test(s) or model(s) are named precisely
- [ ] Software implementation is cited (package name, version)
- [ ] Any method-specific settings (e.g., optimizer, convergence criteria for the statistical model) are reported
- [ ] Multiple methods compared are described with equal detail
- [ ] The number of iterations is stated with justification
- [ ] Convergence criteria for the simulation itself are stated
- [ ] Seed management strategy is described
- [ ] Parallelization details are provided (if applicable)

### P — Performance Measures

**How is the quality of estimands assessed?**

The performance section defines how the simulation output is evaluated.

**Reporting checklist for Performance:**
- [ ] Each performance measure is defined mathematically
- [ ] Performance measures are appropriate for the estimands
- [ ] MCSE is reported for every performance measure
- [ ] Target thresholds are stated (e.g., power >= 0.80, coverage >= 0.90)
- [ ] Convergence status of the simulation is reported

**Standard performance measures:**

| Measure | Formula | Interpretation |
|---------|---------|---------------|
| Bias | (1/N) * sum(theta_hat_i - theta) | Mean deviation from truth; 0 = unbiased |
| Empirical SE | SD(theta_hat_1, ..., theta_hat_N) | Variability of the estimator |
| MSE | (1/N) * sum((theta_hat_i - theta)^2) | Bias^2 + Variance |
| Relative bias | Bias / theta * 100% | Bias as percentage of truth |
| Coverage | (1/N) * sum(I(CI_i contains theta)) | Proportion of CIs capturing truth |
| Mean CI width | (1/N) * sum(CI_upper_i - CI_lower_i) | Average interval width |
| Power | (1/N) * sum(I(p_i < alpha)) under H1 | Detection probability |
| Type I error | (1/N) * sum(I(p_i < alpha)) under H0 | False positive rate |
| MCSE | SE(performance_measure) / sqrt(N) | Simulation precision |

---

## Reporting Table Format

The core results of a simulation study should be presented in a structured table. Morris et al. (2019) recommend the following format.

### Single-Scenario Table

| Estimand | True Value | Estimate | Bias | Empirical SE | MSE | Coverage | Mean CI Width | MCSE |
|----------|-----------|----------|------|-------------|-----|----------|--------------|------|
| theta_1 | [value] | [value] | [value] | [value] | [value] | [value] | [value] | [value] |
| theta_2 | [value] | [value] | [value] | [value] | [value] | [value] | [value] | [value] |

### Multi-Scenario Table (Power Study)

| *n* | *f* | Power | MCSE | Type I Error | MCSE | Coverage | MCSE |
|-----|-----|-------|------|-------------|------|----------|------|
| 30 | 0.20 | .312 | .005 | .048 | .002 | .942 | .002 |
| 60 | 0.20 | .571 | .005 | .051 | .002 | .948 | .002 |
| 90 | 0.20 | .742 | .004 | .049 | .002 | .950 | .002 |
| 120 | 0.20 | .856 | .004 | .050 | .002 | .951 | .002 |

**Key rule**: Every performance measure MUST be accompanied by its MCSE. A power estimate without MCSE is like a mean without a standard error — it conceals the precision of the estimate.

---

## Full Reporting Checklist

Based on Morris et al. (2019), adapted for the simulation-runner context.

### Section 1: Introduction / Background
- [ ] Research question clearly stated
- [ ] Motivation for simulation approach explained
- [ ] Prior simulation studies on the same topic cited (if any)

### Section 2: Simulation Design (ADEMP)

#### Aims
- [ ] Primary aim stated
- [ ] Secondary aims stated (if any)
- [ ] Why simulation (not analytical) is needed

#### Data-Generating Process
- [ ] Mathematical specification of the DGP
- [ ] All parameters listed with values and justifications
- [ ] All distributions named and parameterized
- [ ] All assumptions explicitly stated
- [ ] Multiple DGP scenarios described (if applicable)
- [ ] DGP code available (as supplementary material or in-text)

#### Estimands
- [ ] Each estimand defined precisely
- [ ] True values stated
- [ ] Relationship to research question clear

#### Methods
- [ ] Statistical method(s) named and cited
- [ ] Software packages and versions reported
- [ ] Number of simulation iterations stated and justified
- [ ] Number of chains (if applicable) stated
- [ ] Convergence criteria stated
- [ ] Seed management strategy described
- [ ] Computational resources described (CPU, parallelization)

#### Performance
- [ ] Each performance measure defined
- [ ] MCSE reported for every performance measure
- [ ] Target thresholds stated
- [ ] Convergence of the simulation itself confirmed

### Section 3: Results
- [ ] Results presented in structured tables (see format above)
- [ ] MCSE accompanies every estimate
- [ ] Figures used for complex patterns (power curves, heatmaps)
- [ ] Key findings highlighted in text
- [ ] Convergence diagnostics summarized

### Section 4: Discussion
- [ ] Findings interpreted in context of research question
- [ ] Comparison to analytical results (if available)
- [ ] Limitations of the simulation design acknowledged
- [ ] Sensitivity of results to DGP assumptions discussed
- [ ] Practical recommendations stated (e.g., sample size recommendation)

### Section 5: Reproducibility
- [ ] Master seed reported
- [ ] Complete code available (supplementary material, repository, or appendix)
- [ ] Environment specifications provided (Python version, packages)
- [ ] Instructions for reproducing results

---

## Writing Simulation Results in APA Style

### Methods Section Template

> A Monte Carlo simulation study was conducted to [aims]. The data-generating process specified [brief DGP description]. [List key parameters with values]. Data were generated under [N scenarios/conditions], with [M] iterations per scenario. Convergence was assessed via Monte Carlo standard error (MCSE < [threshold]), split-R-hat (< 1.05), and effective sample size (ESS > 400). The simulation was implemented in Python [version] using numpy [version], scipy [version], and statsmodels [version]. Seeds were managed via `numpy.random.SeedSequence` (master seed = [value]) for parallel reproducibility across [K] workers. Complete simulation code is available at [reference].

### Results Section Template

> Table [N] presents the simulation results across [describe conditions]. Statistical power to detect the [effect name] exceeded .80 (*MCSE* = [value]) for sample sizes *n* >= [value] per group at alpha = .05 with an effect size of [description]. The Type I error rate was [value] (*MCSE* = [value]), consistent with the nominal .05 level. Convergence diagnostics confirmed adequate simulation precision for all estimands: MCSE < [value], R-hat < [value], ESS > [value].

> [For sensitivity analysis:] The tornado plot (Figure [N]) revealed that [estimand] was most sensitive to [parameter] (range: [low] to [high]) and least sensitive to [parameter] (range: [low] to [high]). The robust region, defined as [criterion], encompassed [description of parameter values].

### APA Formatting Rules

1. Italicize single-letter statistics: *N*, *n*, *M*, *SD*, *p*, *f*, *d*, *r*, *F*, *t*, *z*
2. Do not italicize Greek letters or multi-letter abbreviations: MCSE, ESS, ANOVA
3. Report proportions to 2-3 decimal places: power = .812, Type I error = .049
4. Report MCSE to one more decimal place than the estimate: power = .812 (*MCSE* = .0039)
5. Use simulation confidence intervals: .812, 95% simulation CI [.804, .820]
6. Always report the number of iterations: "Based on 10,000 simulation iterations..."
7. Cite the seed management approach for reproducibility

---

## Common Mistakes in Reporting Simulation Studies

| Mistake | Problem | Fix |
|---------|---------|-----|
| No MCSE reported | Reader cannot assess simulation precision | Report MCSE for every estimate |
| Insufficient iterations | MCSE too large for meaningful conclusions | Compute required N from target MCSE |
| DGP not fully specified | Cannot reproduce the simulation | Provide full mathematical specification + code |
| No convergence assessment | Results may be unreliable | Report MCSE, R-hat (if multi-chain), ESS |
| Single DGP scenario only | Results may not generalize | Run multiple scenarios with varied assumptions |
| No Type I error check | Test may be miscalibrated | Always run under H0 to verify alpha |
| Seed not reported | Cannot reproduce results | Always report master seed |
| Code not available | Cannot verify implementation | Provide code as supplementary material |
| Confusing SE with MCSE | SE = variability of estimator; MCSE = precision of simulation estimate | Report both, clearly labeled |
| Reporting more precision than MCSE supports | Reporting power = 0.8123456 when MCSE = 0.005 | Round to precision supported by MCSE |

---

## Simulation Study Workflow Summary

```
1. PLAN (before coding)
   - Define ADEMP components
   - Compute required iterations from target MCSE
   - Pre-register if feasible (OSF)

2. IMPLEMENT (model_builder_agent)
   - Code DGP as pure functions
   - Code analysis as pure functions
   - Validate with known analytical results

3. EXECUTE (execution_engine_agent)
   - Run with seed management (SeedSequence)
   - Monitor convergence in real time
   - Stop when converged or at maximum iterations

4. DIAGNOSE (diagnostics_agent)
   - Compute MCSE, R-hat, ESS per estimand
   - Generate diagnostic plots
   - Flag non-convergence

5. REPORT (report_compiler_agent)
   - Follow ADEMP structure
   - Include MCSE for every estimate
   - Provide code and seed for reproducibility
```

---

## References

- Morris, T. P., White, I. R., & Crowther, M. J. (2019). Using simulation studies to evaluate statistical methods. *Statistics in Medicine*, 38(11), 2074-2102. doi:10.1002/sim.8086
- Burton, A., Altman, D. G., Royston, P., & Holder, R. L. (2006). The design of simulation studies in medical statistics. *Statistics in Medicine*, 25(24), 4279-4292.
- Boulesteix, A. L., Groenwold, R. H., Abrahamowicz, M., et al. (2020). Introduction to statistical simulations in health research. *BMJ Open*, 10(12), e039921.
- Gasparini, A. (2018). rsimsum: Summarise results from Monte Carlo simulation studies. *Journal of Open Source Software*, 3(26), 739.
- White, I. R. (2010). simsum: Analyses of simulation studies including Monte Carlo error. *The Stata Journal*, 10(3), 369-385.
