# Example: Monte Carlo Power Simulation — 2x3 Mixed ANOVA

## User Request

```
Simulate the power of a 2x3 mixed ANOVA to detect the interaction effect
across sample sizes 30-300 per group, assuming f = 0.25 for the interaction
```

## Phase 1: INTAKE

### intake_agent Output

```markdown
## Simulation Brief

**Simulation ID**: SIM-20260316-001
**Experiment ID**: AD-HOC
**Mode**: power-sim
**Simulation Type**: power_sim

### Source
- Input type: Ad-hoc
- Schema version: N/A

### Model Summary
- Description: Simulate statistical power for a 2 (between: treatment vs control)
  x 3 (within: time points) mixed ANOVA, focusing on the interaction effect.
- DGP: Y_ijk = mu + alpha_i + beta_j + (alpha*beta)_ij + pi_k(i) + epsilon_ijk
  where alpha = between-subjects, beta = within-subjects, pi = subject random effect
- Key parameters: f_interaction = 0.25, sigma = 10, rho = 0.5
- Distributions: epsilon ~ N(0, sigma^2), pi ~ N(0, sigma_subject^2)

### Execution Plan
- Iterations: 10,000 per sample size
- Chains: 4
- Burn-in: 0
- Convergence criterion: MCSE < 0.005
- Parallelization: yes, all available cores
- Estimated runtime: ~15 minutes

### Performance Measures
- Power: proportion of p < .05 for interaction under H1
- Type I error: proportion of p < .05 for interaction under H0
- Effect size bias: mean(estimated f) - true f

### ADEMP Summary
- **Aims**: Estimate power to detect interaction in 2x3 mixed ANOVA across n = 30-300
- **DGP**: Mixed ANOVA with normal errors, compound symmetry covariance
- **Estimands**: Power (interaction), Type I error (interaction), effect size bias
- **Methods**: Mixed ANOVA via statsmodels (Type III SS)
- **Performance**: Power as proportion, MCSE for precision

### Environment
- Python: 3.12.3
- Key packages: numpy 1.26.4, scipy 1.13.0, statsmodels 0.14.1
- OS: Windows 11
- Venv path: experiment_env/
- Requirements: experiment_env/requirements.txt
```

## Phase 2: MODEL BUILDING

### model_builder_agent Output

#### DGP Function

```python
import numpy as np
from numpy.random import Generator
import pandas as pd

def dgp(rng: Generator, params: dict) -> dict:
    """
    Data-Generating Process for a 2x3 mixed ANOVA.

    Generates data with:
    - Between-subjects factor: 2 levels (treatment, control)
    - Within-subjects factor: 3 levels (time1, time2, time3)
    - Subject-level random intercept
    - Compound symmetry covariance structure

    Parameters
    ----------
    rng : Generator
        Random number generator.
    params : dict
        Required keys:
        - n_per_group: int, sample size per between-subjects group
        - mu: float, grand mean (default 50)
        - alpha: list[float], between-subjects effects [0, delta]
        - beta: list[float], within-subjects effects [0, b2, b3]
        - interaction: list[list[float]], 2x3 interaction effects
        - sigma: float, residual SD
        - rho: float, within-subject correlation (compound symmetry)

    Returns
    -------
    dict with keys:
        - 'data': pd.DataFrame with columns [subject, group, time, y]
        - 'truth': dict with true parameter values
    """
    n = params['n_per_group']
    mu = params.get('mu', 50)
    alpha = params['alpha']          # [0, delta_between]
    beta = params['beta']            # [0, delta_time2, delta_time3]
    interaction = params['interaction']  # 2x3 matrix
    sigma = params['sigma']
    rho = params['rho']

    # Derive within-subject and residual variance components
    # Compound symmetry: Var(Y) = sigma_subject^2 + sigma_residual^2
    # Cor(Y_j, Y_k) = rho = sigma_subject^2 / (sigma_subject^2 + sigma_residual^2)
    total_var = sigma ** 2
    sigma_subject = np.sqrt(rho * total_var)
    sigma_residual = np.sqrt((1 - rho) * total_var)

    records = []
    subject_id = 0

    for i in range(2):      # group
        for k in range(n):   # subject within group
            # Subject random intercept
            subject_effect = rng.normal(0, sigma_subject)

            for j in range(3):  # time
                y = (mu
                     + alpha[i]
                     + beta[j]
                     + interaction[i][j]
                     + subject_effect
                     + rng.normal(0, sigma_residual))

                records.append({
                    'subject': subject_id,
                    'group': i,
                    'time': j,
                    'y': y,
                })

            subject_id += 1

    data = pd.DataFrame(records)

    return {
        'data': data,
        'truth': {
            'mu': mu,
            'alpha': alpha,
            'beta': beta,
            'interaction': interaction,
            'sigma': sigma,
            'rho': rho,
        }
    }
```

#### Analysis Function

```python
import statsmodels.api as sm
from statsmodels.formula.api import ols
from statsmodels.stats.anova import AnovaRM

def analyze(data_dict: dict, params: dict) -> dict:
    """
    Run mixed ANOVA and extract interaction test results.

    Returns p-value, F-statistic, and partial eta-squared for the interaction.
    """
    data = data_dict['data']
    alpha_level = params.get('alpha_level', 0.05)

    try:
        # Repeated measures ANOVA via statsmodels
        aov = AnovaRM(
            data=data,
            depvar='y',
            subject='subject',
            within=['time'],
            between=['group'],
        )
        result = aov.fit()

        # Extract interaction row
        interaction_row = result.anova_table.loc['group:time']
        f_stat = interaction_row['F Value']
        p_value = interaction_row['Pr > F']
        # Compute partial eta-squared
        ss_interaction = interaction_row['Num DF'] * f_stat * interaction_row['Den DF']
        # Approximation: partial eta^2 = F * df_num / (F * df_num + df_den)
        df_num = interaction_row['Num DF']
        df_den = interaction_row['Den DF']
        partial_eta_sq = (f_stat * df_num) / (f_stat * df_num + df_den)

        return {
            'p_value': p_value,
            'f_statistic': f_stat,
            'significant': p_value < alpha_level,
            'partial_eta_squared': partial_eta_sq,
        }

    except Exception as e:
        # If model fails (e.g., singular matrix), return non-significant
        return {
            'p_value': 1.0,
            'f_statistic': 0.0,
            'significant': False,
            'partial_eta_squared': 0.0,
            'error': str(e),
        }
```

#### Parameter Dictionary

```python
# H1 parameters (effect present)
params_h1 = {
    'n_per_group': 60,           # Swept: [30, 45, 60, 90, 120, 180, 240, 300]
    'mu': 50,                     # Grand mean
    'alpha': [0, 5],              # Between-subjects effect (control, treatment)
    'beta': [0, 2, 4],           # Within-subjects time trend
    'interaction': [              # 2x3 interaction effects
        [0, 0, 0],               # Control: no interaction
        [0, 1, 3],               # Treatment: growing advantage over time
    ],
    'sigma': 10,                  # Residual SD
    'rho': 0.5,                   # Within-subject correlation
    'alpha_level': 0.05,          # Significance level
}

# H0 parameters (no interaction, for Type I error check)
params_h0 = {
    **params_h1,
    'interaction': [
        [0, 0, 0],
        [0, 0, 0],               # No interaction under H0
    ],
}

# Sample sizes to sweep
sample_sizes = [30, 45, 60, 90, 120, 180, 240, 300]
```

## Phase 3: EXECUTION

### execution_engine_agent Output

```markdown
## Execution Results

**Simulation ID**: SIM-20260316-001
**Status**: Converged (all sample sizes)

### Execution Summary
- Iterations per cell: 10,000
- Chains: 4 (2,500 iterations each)
- Sample size cells: 8 (n = 30 to 300)
- H0 iterations: 10,000 (for Type I error)
- Total iterations: 90,000 (8 H1 cells + 1 H0 cell)
- Early stopped: Yes, 6 of 8 H1 cells converged before 10,000
- Wall time: 847 seconds
- Peak memory: 1.2 GB
- Workers used: 8

### Convergence Status
| Sample Size | Power MCSE | R-hat | ESS | Verdict |
|-------------|-----------|-------|-----|---------|
| 30 | 0.0046 | 1.002 | 9,847 | Converged |
| 45 | 0.0049 | 1.001 | 9,912 | Converged |
| 60 | 0.0038 | 1.003 | 9,756 | Converged |
| 90 | 0.0031 | 1.001 | 9,889 | Converged |
| 120 | 0.0024 | 1.002 | 9,934 | Converged |
| 180 | 0.0015 | 1.001 | 9,967 | Converged |
| 240 | 0.0009 | 1.000 | 9,989 | Converged |
| 300 | 0.0005 | 1.000 | 9,997 | Converged |
| H0 (n=60) | 0.0022 | 1.001 | 9,945 | Converged |

### Seed Log
Master Seed: 42
Method: SeedSequence.spawn
Hierarchy: master -> 9 cells -> 4 chains per cell -> 2,500 iterations per chain
```

## Phase 4: DIAGNOSTICS

### diagnostics_agent Output

```markdown
## Convergence Report

**Simulation ID**: SIM-20260316-001
**Overall Verdict**: CONVERGED

### Summary Table
| Sample Size | Power | MCSE | R-hat | ESS | Verdict |
|-------------|-------|------|-------|-----|---------|
| 30 | .312 | .0046 | 1.002 | 9,847 | Converged |
| 45 | .523 | .0049 | 1.001 | 9,912 | Converged |
| 60 | .691 | .0038 | 1.003 | 9,756 | Converged |
| 90 | .855 | .0031 | 1.001 | 9,889 | Converged |
| 120 | .938 | .0024 | 1.002 | 9,934 | Converged |
| 180 | .987 | .0015 | 1.001 | 9,967 | Converged |
| 240 | .997 | .0009 | 1.000 | 9,989 | Converged |
| 300 | .999 | .0005 | 1.000 | 9,997 | Converged |

### Type I Error Verification
| Test | Type I Error | MCSE | 95% Sim CI | Verdict |
|------|-------------|------|------------|---------|
| Interaction (H0, n=60) | .051 | .0022 | [.047, .055] | Nominal alpha (.05) within CI |

### Diagnostic Plots Generated
- Power curve: experiment_outputs/plots/power_curve.png
- Trace plots (per sample size): experiment_outputs/plots/trace_power_n*.png
- Running MCSE: experiment_outputs/plots/convergence_power_n*.png
- Distribution: experiment_outputs/plots/dist_power_n60.png (representative)

### Recommendations
No issues detected. All estimands converged well below thresholds.
```

## Phase 5: REPORTING

### report_compiler_agent Output — Schema 11 (Excerpt)

```markdown
## Experiment Results

**Experiment ID**: AD-HOC-SIM-20260316-001
**Result Type**: simulation

**Primary Results**:
| Sample Size (n/group) | Power | MCSE | 95% Sim CI | Type I Error |
|----------------------|-------|------|------------|-------------|
| 30 | .312 | .005 | [.303, .321] | — |
| 45 | .523 | .005 | [.513, .533] | — |
| 60 | .691 | .004 | [.684, .698] | .051 |
| 90 | .855 | .003 | [.849, .861] | — |
| 120 | .938 | .002 | [.934, .943] | — |
| 180 | .987 | .002 | [.984, .990] | — |
| 240 | .997 | .001 | [.996, .999] | — |
| 300 | .999 | .001 | [.998, 1.00] | — |

**Sample Size Recommendation**:
To achieve power >= .80 at alpha = .05 for the interaction effect (f = 0.25):
**n >= 75 per group** (interpolated from power curve)

**Effect Size Diagnostics**:
| n/group | Mean Est. partial eta^2 | True partial eta^2 | Bias |
|---------|------------------------|--------------------|----|
| 60 | .062 | .059 | +.003 |
| 120 | .060 | .059 | +.001 |
| 300 | .059 | .059 | .000 |

Effect size estimates converge to truth as n increases, with negligible upward bias
in small samples (consistent with known partial eta-squared bias).
```

### APA Results Text

> A Monte Carlo power simulation (*N* = 10,000 iterations per condition, master seed = 42) was conducted to estimate the statistical power of a 2 (treatment condition: between-subjects) x 3 (time point: within-subjects) mixed ANOVA for detecting the interaction effect. The data-generating process specified normally distributed errors (*sigma* = 10), compound symmetry covariance (*rho* = .50), and interaction effects corresponding to Cohen's *f* = 0.25. Eight sample sizes were evaluated (*n* = 30, 45, 60, 90, 120, 180, 240, and 300 per group).
>
> Results indicated that power exceeded .80 for sample sizes *n* >= 75 per group (Table 1; Figure 1). At *n* = 60, power was .691 (*MCSE* = .004, 95% simulation CI [.684, .698]), while at *n* = 90, power reached .855 (*MCSE* = .003, 95% simulation CI [.849, .861]). The Type I error rate under the null hypothesis was .051 (*MCSE* = .002), consistent with the nominal .05 level (95% simulation CI [.047, .055]). Partial eta-squared estimates showed negligible upward bias in small samples (+.003 at *n* = 60), converging to the true value at *n* >= 120. Convergence diagnostics confirmed adequate simulation precision: *MCSE* < .005 for all power estimates, split-*R*-hat < 1.01 across 4 chains, *ESS* > 9,700 for all conditions.
>
> Based on these results, a minimum sample size of *n* = 75 per group (total *N* = 150) is recommended for the planned 2 x 3 mixed ANOVA with the hypothesized interaction effect size.

### Material Passport

```markdown
## Material Passport

- Origin Skill: simulation-runner
- Origin Mode: power-sim
- Origin Date: 2026-03-16T14:30:00Z
- Verification Status: UNVERIFIED
- Version Label: sim_results_v1
- Upstream Dependencies: []
```

### Seed Log

```markdown
Master Seed: 42
Method: numpy.random.SeedSequence
Hierarchy: master -> 9 cells -> 4 chains -> 2,500 iterations
Reproduction:
  from numpy.random import SeedSequence, default_rng
  master = SeedSequence(42)
  cell_seeds = master.spawn(9)  # 8 H1 + 1 H0
  for cell in cell_seeds:
      chain_seeds = cell.spawn(4)
      for chain in chain_seeds:
          iter_rngs = [default_rng(s) for s in chain.spawn(2500)]
```
