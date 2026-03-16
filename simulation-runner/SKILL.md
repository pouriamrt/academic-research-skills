---
name: simulation-runner
description: "Computational simulation agent team. 5-agent pipeline for designing and executing Monte Carlo simulations, bootstrap resampling, power simulations, parameter sweeps, agent-based models, and stochastic process simulations. 6 modes: full simulation pipeline, guided simulation design, quick single-run, power simulation, sensitivity analysis, and bootstrap resampling. Covers simulation design (ADEMP framework), model building, parallel execution with convergence monitoring, diagnostic assessment, and APA-formatted reporting with Schema 11 output. Triggers on: Monte Carlo, simulation, bootstrap, parameter sweep, sensitivity analysis, agent-based model, power simulation, simulate, computational experiment, stochastic, resampling, permutation test, 蒙地卡羅, 模擬, 拔靴法, 參數掃描, 敏感度分析, 代理人模型, 檢定力模擬, 計算實驗, 隨機過程, 重抽樣."
metadata:
  version: "1.0"
  last_updated: "2026-03-16"
---

# Simulation Runner — Computational Experiment Agent Team

Computational simulation tool — a domain-agnostic 5-agent team for designing and executing rigorous computational experiments. v1.0 supports Monte Carlo, bootstrap, power simulation, parameter sweeps, agent-based models, resampling methods, stochastic processes, and optimization-based simulations.

## Quick Start

**Minimal command:**
```
Simulate the power of a 2x3 mixed ANOVA across sample sizes 30-300
```

**Bootstrap mode:**
```
Bootstrap 95% BCa confidence intervals for the median difference between groups A and B
```

**Guided mode:**
```
Help me design a Monte Carlo simulation for my regression model
Guide my simulation design for testing robustness of my estimator
```

**Execution:**
1. Intake — Parse request, determine simulation type, validate inputs
2. Model Building — Translate conceptual model to executable Python code
3. Execution — Run simulation with convergence monitoring and parallel processing
4. Diagnostics — Assess quality via MCSE, R-hat, ESS, diagnostic plots
5. Reporting — Compile APA-formatted results with Schema 11 artifact

---

## Trigger Conditions

### Trigger Keywords

**English**: Monte Carlo, simulation, bootstrap, parameter sweep, sensitivity analysis, agent-based model, power simulation, simulate, computational experiment, stochastic, resampling, permutation test

**繁體中文**: 蒙地卡羅, 模擬, 拔靴法, 參數掃描, 敏感度分析, 代理人模型, 檢定力模擬, 計算實驗, 隨機過程, 重抽樣

### Guided Mode Activation

Activate `guided` mode when the user's **intent** matches any of the following patterns, **regardless of language**. Detect meaning, not exact keywords.

**Intent signals** (any one is sufficient):
1. User wants help designing a simulation but does not have a concrete model yet
2. User asks to be "guided" or "helped through" simulation setup
3. User expresses uncertainty about which simulation type to use
4. User describes a research question without specifying a simulation approach
5. User has a statistical question that could be answered by simulation but has not framed it that way

**Default rule**: When intent is ambiguous between `guided` and `full`, **prefer `guided`** — it is safer to help the user think through their simulation design than to produce an unwanted result.

### Does NOT Trigger

| Scenario | Use Instead |
|----------|-------------|
| Analyzing existing data (no simulation) | `data-analyst` |
| Designing an experiment protocol (not a simulation) | `experiment-designer` |
| Writing a paper about simulation results | `academic-paper` |
| Full research-to-paper pipeline | `academic-pipeline` |

### Quick Mode Selection Guide

| Your Situation 你的狀況 | Recommended Mode |
|----------------|-----------------|
| Have a complete simulation spec, need full pipeline / 有完整模擬規格 | `full` |
| Vague idea, need help designing the simulation / 需要引導設計模擬 | `guided` |
| Quick single-run, no convergence diagnostics / 快速單次執行 | `quick` |
| Need statistical power for a planned study / 需要檢定力分析 | `power-sim` |
| Need parameter sensitivity analysis / 需要敏感度分析 | `sensitivity` |
| Need bootstrap CIs or resampling inference / 需要拔靴法推論 | `bootstrap` |

Not sure? Start with `guided` — it will help you figure out what you need.
不確定？先用 `guided` 模式——它會幫你釐清你需要什麼。

---

## Agent Team (5 Agents)

| # | Agent | Role | Phase |
|---|-------|------|-------|
| 1 | `intake_agent` | Parses request, determines simulation type, validates inputs, sets up venv, detects mode | Phase 1 |
| 2 | `model_builder_agent` | Translates conceptual model to Python functions (DGP, resampling, agent rules, parameter grids) | Phase 2 |
| 3 | `execution_engine_agent` | Runs simulation with seed management, parallelization, convergence monitoring, early stopping | Phase 3 |
| 4 | `diagnostics_agent` | Computes MCSE, R-hat, ESS; generates trace/autocorrelation/distribution plots; flags non-convergence | Phase 4 |
| 5 | `report_compiler_agent` | Assembles ADEMP-structured report, APA-formatted results, Schema 11 artifact, Material Passport | Phase 5 |

---

## Simulation Types Coverage

| Type | Description | Key Parameters | Convergence Criterion | Libraries |
|------|-------------|----------------|----------------------|-----------|
| Monte Carlo | Repeated random sampling to estimate distributional properties | n_iterations, DGP, estimands | MCSE < threshold | numpy, scipy |
| Bootstrap | Resampling with replacement for inference (percentile, BCa, studentized) | n_bootstrap, data, statistic | MCSE of CI bounds | numpy, scipy |
| Power simulation | Estimate statistical power by simulating data under H1 and running tests | n_sim, effect_size, sample_sizes, alpha | MCSE of power < 0.01 | numpy, scipy, statsmodels |
| Parameter sweep | Systematic variation of model parameters to map output landscape | param_grid, n_per_cell | Per-cell MCSE | numpy, scipy, joblib |
| Agent-based | Emergent behavior from agent interactions on a network/grid | n_agents, rules, topology, n_steps | Steady-state detection | numpy, networkx |
| Resampling/CV | Permutation tests, cross-validation, jackknife | n_permutations, folds | Stable p-value | numpy, scipy, scikit-learn |
| Stochastic processes | Markov chains, random walks, queuing models, diffusion | transition_matrix, n_steps | Stationarity / mixing time | numpy, scipy |
| Optimization | Stochastic optimization, simulated annealing, genetic algorithms | objective, bounds, n_restarts | Convergence of objective | numpy, scipy.optimize |

---

## Mode Selection Guide

```
User Input
    |
    +-- Has Schema 10/13 from experiment-designer?
    |   +-- Yes --> full mode (pre-planned simulation)
    |   +-- No --> Has clear simulation spec?
    |              +-- Yes --> What type?
    |              |          +-- Power analysis --> power-sim mode
    |              |          +-- Sensitivity/sweep --> sensitivity mode
    |              |          +-- Bootstrap/resampling --> bootstrap mode
    |              |          +-- Other (complete spec) --> full mode
    |              +-- No --> Want guidance designing simulation?
    |                         +-- Yes --> guided mode
    |                         +-- No --> quick mode (single run, minimal diagnostics)
```

---

## Orchestration Workflow (5 Phases)

```
User: "Simulate [specification]"
     |
=== Phase 1: INTAKE (intake_agent) ===
     |
     +-> [intake_agent] -> Simulation Brief
         - Determine simulation type (Monte Carlo / Bootstrap / Power / Sweep / ABM / etc.)
         - Parse and validate inputs:
           * Schema 10/13 present? -> extract model_definition, execution_plan
           * Ad-hoc request? -> enforce minimum fields (see Ad-Hoc Requirements below)
         - Detect mode from user intent
         - Set up virtual environment:
           * Core: numpy, scipy, matplotlib, pandas, statsmodels
           * Extras: joblib, networkx, tqdm
         - Output: Simulation Brief (type, parameters, data refs, mode, venv status)
     |
=== Phase 2: MODEL BUILDING (model_builder_agent) ===
     |
     +-> [model_builder_agent] -> Executable Model
         - Translate conceptual model to Python:
           * Monte Carlo: DGP function (distributions, transformations, noise)
           * Bootstrap: resampling function (numpy Generator.choice)
           * Agent-based: agent class + rules + environment + topology (networkx)
           * Power sim: wrap statistical test in DGP loop
           * Parameter sweep: parameterize DGP, define grid
         - Output: Python functions + parameter dict
         - Quality check: function is pure, deterministic given seed, returns structured output
     |
=== Phase 3: EXECUTION (execution_engine_agent) ===
     |
     +-> [execution_engine_agent] -> Raw Results
         - Seed management via numpy.random.SeedSequence
         - Parallelize independent iterations with joblib.Parallel + delayed
         - Monitor convergence:
           * Running MCSE every N iterations
           * R-hat for multiple chains (if applicable)
         - Early stopping when convergence criteria met
         - Progress tracking via tqdm
         - Save results to experiment_outputs/
         - Output: raw result arrays, seed log, execution metadata
     |
=== Phase 4: DIAGNOSTICS (diagnostics_agent) ===
     |
     +-> [diagnostics_agent] -> Convergence Report
         - Compute per-estimand:
           * Monte Carlo Standard Error (MCSE)
           * R-hat (potential scale reduction factor)
           * Effective Sample Size (ESS)
           * Autocorrelation function
         - Generate diagnostic plots:
           * Trace plots (per chain/estimand)
           * Autocorrelation plots
           * Distribution/histogram plots
           * Running mean/MCSE plots
         - For sweeps: heatmaps, tornado plots, spider plots
         - Flag non-convergence with specific recommendations
         - Output: convergence_report per convergence_report_template.md
     |
=== Phase 5: REPORTING (report_compiler_agent) ===
     |
     +-> [report_compiler_agent] -> Final Report + Schema 11
         - Assemble report per simulation_report_template.md:
           * ADEMP summary
           * Model specification reference
           * Execution parameters (iterations, seeds, parallelization)
           * Results (estimates, CIs, convergence status)
           * Diagnostic plots
           * Seed log
           * Script reference
         - Generate Schema 11 artifact (Experiment Results)
         - Generate Material Passport (Schema 9)
         - APA-formatted results text ready for paper insertion
         - If notebook_path provided: auto-log to lab notebook
```

---

## Ad-Hoc Request Requirements

When no Schema 10/13 is provided (user makes a direct request), the `intake_agent` enforces the following minimum fields. If any are missing, the agent asks the user before proceeding.

| Field | Required | Default | Description |
|-------|----------|---------|-------------|
| `simulation_type` | Yes | — | Which type of simulation (Monte Carlo, bootstrap, power, sweep, ABM, etc.) |
| `model_description` or `data_file` | Yes | — | Conceptual model description (for generative sims) or path to data file (for bootstrap/resampling) |
| `iterations` | No | 10,000 | Number of simulation iterations |
| `what_to_measure` | Yes | — | What quantities to estimate (power, bias, coverage, CI width, etc.) |

### Optional Ad-Hoc Fields

| Field | Default | Description |
|-------|---------|-------------|
| `alpha` | 0.05 | Significance level |
| `sample_sizes` | — | Range of sample sizes for power curves |
| `effect_size` | — | Expected or hypothesized effect size |
| `confidence_level` | 0.95 | For bootstrap CIs |
| `parameter_grid` | — | For parameter sweeps |
| `n_chains` | 4 | Number of independent chains for convergence |
| `convergence_threshold` | MCSE < 0.01 | When to stop |

---

## Guided Mode: SIMULATION DESIGN DIALOGUE

Core principle: Help users design rigorous simulations through Socratic questioning about their research goals, model assumptions, and performance measures. Guide them to articulate the ADEMP framework before any code is written.

```
User: "Help me design a simulation for [topic]"
     |
=== Round 1: AIMS ===
     |
     +-> [intake_agent] -> Clarify research question and simulation goals
         - "What question are you trying to answer with this simulation?"
         - "What would a successful simulation tell you?"
         - "Is this for power analysis, robustness check, method comparison, or exploration?"
     |
=== Round 2: DATA-GENERATING PROCESS ===
     |
     +-> [model_builder_agent] -> Define the model
         - "What does your data look like? What distributions are involved?"
         - "What are the key parameters? Which are fixed vs. varied?"
         - "What assumptions does your model make? Are they realistic?"
     |
=== Round 3: ESTIMANDS & METHODS ===
     |
     +-> [intake_agent] + [model_builder_agent] -> Define measures and methods
         - "What specific quantities do you want to estimate?"
         - "What statistical methods will you apply to the simulated data?"
         - "How will you measure performance (bias, MSE, coverage, power)?"
     |
=== Round 4: PERFORMANCE & EXECUTION ===
     |
     +-> [execution_engine_agent] -> Plan execution
         - "How many iterations do you need for stable estimates?"
         - "Do you need parameter sweeps across multiple conditions?"
         - "What convergence criteria should we use?"
     |
     +-> Compile into Simulation Brief -> proceed to full pipeline
```

### Guided Mode Dialogue Rules

- At least 1 round of dialogue per ADEMP component before proceeding
- Users can skip to execution at any time by saying "run it" or "let's go"
- Agent responses limited to 200-400 words per round
- If dialogue exceeds 8 rounds without convergence -> compile current understanding and proceed
- Output: complete Simulation Brief that feeds into Phase 2

---

## Operational Modes

| Mode | Agents Active | Output | Typical Iterations |
|------|---------------|--------|--------------------|
| `full` (default) | All 5 | Full ADEMP report + Schema 11 + convergence diagnostics | 10,000+ |
| `guided` | intake + model_builder (interactive), then all 5 | Simulation Brief -> full pipeline | Varies |
| `quick` | intake + model_builder + execution + report (minimal diagnostics) | Summary results, no convergence analysis | 1,000-5,000 |
| `power-sim` | All 5 (power-focused) | Power curve + sample size recommendation | 10,000 per cell |
| `sensitivity` | All 5 (sweep-focused) | Tornado/spider plots + robust region map | 1,000-5,000 per cell |
| `bootstrap` | All 5 (resampling-focused) | Bootstrap distribution + CIs (percentile, BCa) | 10,000+ |

---

## Virtual Environment Setup

All simulations run inside a managed Python virtual environment. The `intake_agent` sets up the venv at the start of each pipeline run.

### Core Packages (always installed)
- numpy
- scipy
- matplotlib
- pandas
- statsmodels

### Extra Packages (installed for simulation-runner)
- joblib (parallel execution)
- networkx (agent-based model topologies)
- tqdm (progress monitoring)

### Venv Protocol

1. Create or reuse venv at `experiment_env/`
2. Install core + extras via `pip install`
3. Freeze environment: `pip freeze > experiment_env/requirements.txt`
4. Record in Material Passport: Python version, package versions, OS

---

## Failure Paths

| Failure Scenario | Trigger Condition | Recovery Strategy |
|---------|---------|---------|
| Non-convergence | MCSE remains above threshold after max iterations | Double iterations, increase chains, check DGP for pathology |
| Execution timeout | Single iteration exceeds 60s | Profile code, reduce model complexity, check for infinite loops |
| Memory exhaustion | Results array exceeds available memory | Switch to streaming/chunked storage, reduce stored outputs |
| Degenerate DGP | All iterations produce identical results | Verify random seed propagation, check DGP for determinism |
| Bootstrap on tiny data | n < 20 for bootstrap | Warn about instability, suggest exact methods or larger sample |
| Parameter sweep explosion | Grid has > 10,000 cells | Suggest Latin hypercube or adaptive sampling instead of full grid |
| ABM non-stationarity | Agent-based model never reaches steady state | Increase run length, check for absorbing states, reduce step size |
| Missing data file | Bootstrap/resampling requested but data_file not found | Ask user for correct path, offer to generate synthetic data |

---

## Integration with Other Skills

### Upstream: Schema 10/13 from experiment-designer

When `experiment-designer` produces a Schema 10 with `design_type: "simulation"` and an accompanying Schema 13 (Simulation Specification), those artifacts feed directly into `intake_agent`, bypassing ad-hoc field collection.

**Consumed fields from Schema 13:**
- `simulation_type` -> determines pipeline configuration
- `model_definition` -> feeds `model_builder_agent`
- `execution_plan` -> configures `execution_engine_agent`
- `performance_measures` -> guides `diagnostics_agent`
- `ademp_checklist` -> structures `report_compiler_agent` output

### Downstream: Schema 11 to academic-paper / lab-notebook

The `report_compiler_agent` produces a Schema 11 (Experiment Results) artifact that can be consumed by:
- `academic-paper/draft_writer_agent` — inserts simulation results into paper
- `lab-notebook/entry_writer_agent` — logs simulation as experiment entry

```
experiment-designer (Schema 10/13)
    -> simulation-runner (this skill)
        -> academic-paper (Schema 11)
        -> lab-notebook (Schema 11)
```

### Sibling: data-analyst

For simulations that require pre-processing of empirical data (e.g., fitting distributions for a DGP, or preparing data for bootstrap), `data-analyst` can be invoked upstream. The two skills are complementary: `data-analyst` handles real data, `simulation-runner` handles generated data.

---

## Agent File References

| Agent | Definition File |
|-------|----------------|
| intake_agent | `agents/intake_agent.md` |
| model_builder_agent | `agents/model_builder_agent.md` |
| execution_engine_agent | `agents/execution_engine_agent.md` |
| diagnostics_agent | `agents/diagnostics_agent.md` |
| report_compiler_agent | `agents/report_compiler_agent.md` |

---

## Reference Files

| Reference | Purpose | Used By |
|-----------|---------|---------|
| `references/simulation_design_patterns.md` | Decision tree for simulation type selection, 8 type patterns | intake_agent, model_builder_agent |
| `references/convergence_criteria_guide.md` | When to stop: MCSE, R-hat, ESS thresholds, early stopping | execution_engine_agent, diagnostics_agent |
| `references/seed_management_guide.md` | numpy Generator, SeedSequence, parallel streams, seed logging | execution_engine_agent, model_builder_agent |
| `references/parallel_execution_guide.md` | joblib patterns, multiprocessing, overhead estimation | execution_engine_agent |
| `references/reporting_simulation_studies.md` | ADEMP framework, Morris et al. (2019), reporting checklist | report_compiler_agent, diagnostics_agent |

---

## Templates

| Template | Purpose |
|----------|---------|
| `templates/simulation_report_template.md` | Full simulation report (ADEMP, results, diagnostics, seeds) |
| `templates/model_specification_template.md` | DGP description, parameters, assumptions, limitations |
| `templates/convergence_report_template.md` | Per-estimand convergence metrics and diagnostic plot refs |
| `templates/parameter_sweep_template.md` | Sweep grid, results matrix, tornado/spider plots, robust region |

---

## Examples

| Example | Demonstrates |
|---------|-------------|
| `examples/monte_carlo_power_example.md` | Power simulation for 2x3 mixed ANOVA with convergence diagnostics |
| `examples/bootstrap_ci_example.md` | BCa bootstrap CIs for median difference with non-normal data |

---

## Output Language

Follows the user's language. Code comments and variable names always in English. Technical terms (MCSE, R-hat, ESS, DGP, ADEMP) kept in English regardless of output language.

---

## Quality Standards

1. **Every simulation must have a seed log** — full reproducibility requires recorded seeds
2. **Convergence must be assessed** — no results reported without convergence diagnostics (except `quick` mode)
3. **ADEMP framework** — every full report follows Aims, DGP, Estimands, Methods, Performance structure
4. **Parallel reproducibility** — results must be identical regardless of number of parallel workers (via SeedSequence)
5. **AI disclosure** — all reports include a statement that AI-assisted simulation tools were used
6. **Code transparency** — all generated simulation code saved to `experiment_outputs/scripts/` and referenced in report
7. **Bootstrap integrity** — bootstrap methods must use numpy.random.Generator (not legacy RandomState), and report the specific bootstrap variant (percentile, BCa, studentized)

## Cross-Agent Quality Alignment

| Concept | Definition | Applies To |
|---------|-----------|------------|
| **Converged** | MCSE < threshold AND R-hat < 1.05 AND ESS > 400. All three conditions must be met | execution_engine_agent, diagnostics_agent |
| **Non-converged** | Any convergence criterion not met after maximum iterations | diagnostics_agent |
| **Marginal** | MCSE within 2x threshold OR R-hat between 1.05-1.10 OR ESS between 200-400 | diagnostics_agent |
| **DGP** | Data-Generating Process — the complete specification of how simulated data are created, including distributions, parameters, functional form, and noise | model_builder_agent, report_compiler_agent |
| **MCSE** | Monte Carlo Standard Error — standard deviation of the estimand across iterations divided by sqrt(n_iterations) | execution_engine_agent, diagnostics_agent |
| **Default iterations** | 10,000 for full/power-sim/bootstrap; 1,000-5,000 for quick/sensitivity per cell | intake_agent |

> **Cross-Skill Reference**: See `shared/handoff_schemas.md` for Schema 10, 11, and 13 data exchange formats.

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-03-16 | Initial release: 5 agents, 6 modes, 8 simulation types, ADEMP reporting, Schema 10/13 intake, Schema 11 output, joblib parallelization, convergence diagnostics |
