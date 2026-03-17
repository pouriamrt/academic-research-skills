# Superpowers Integration Protocol for Experiment Skills

All code-writing experiment agents follow this protocol. It ensures complex code is brainstormed, planned, test-driven, and verified before being declared complete, while simple library calls execute directly.

**Prerequisite**: The superpowers plugin must be installed (`claude plugin install superpowers@claude-plugins-official`).

**Superpowers skills used**: `brainstorming`, `writing-plans`, `test-driven-development`, `systematic-debugging`, `verification-before-completion`

---

## 1. Complexity Classification

Before writing any code, classify the task as SIMPLE or COMPLEX using the table below. SIMPLE tasks execute directly. COMPLEX tasks trigger the adaptive superpowers workflow (Section 2).

### SIMPLE — Direct Execution

| Skill | Simple Tasks |
|-------|-------------|
| `experiment-designer` | Standard power analysis (t-test, ANOVA, correlation, chi-square, regression) using `statsmodels.stats.power` one-liners |
| `data-analyst` | Single standard test via pingouin/scipy: t-test, ANOVA, correlation, chi-square, Mann-Whitney, Wilcoxon, Kruskal-Wallis |
| `data-analyst` | Standard assumption checks: Shapiro-Wilk, Levene, Mauchly |
| `data-analyst` | Standard plots: bar chart, box plot, scatter plot, histogram using seaborn defaults |
| `data-analyst` | Single regression (linear or logistic) via statsmodels |
| `data-analyst` | Standard descriptive statistics |
| `simulation-runner` | Standard bootstrap CI (percentile or BCa) on a single statistic |

### COMPLEX — Triggers Superpowers Workflow

| Skill | Complex Tasks |
|-------|-------------|
| `experiment-designer` | Factorial ANOVA power via simulation, cluster-adjusted power with custom ICC models, sequential analysis power, multi-endpoint power |
| `data-analyst` | SEM/CFA path models (semopy), HLM/multilevel models (MixedLM), mediation with custom bootstrap, survival analysis (lifelines), Bayesian analysis |
| `data-analyst` | Multi-step analysis pipelines (>2 dependent analyses) |
| `data-analyst` | Custom data cleaning pipelines: complex recoding, multiple imputation, outlier handling with domain logic |
| `data-analyst` | Custom visualizations: multi-panel figures, interaction plots with custom annotations, forest plots |
| `simulation-runner` | Custom DGPs (any user-specified data-generating process) |
| `simulation-runner` | Monte Carlo with convergence monitoring, agent-based models, parameter sweeps, power simulations, sensitivity analyses, stochastic process models |
| `simulation-runner` | Any code requiring parallelization via joblib |

### User Overrides

- **Force COMPLEX**: User says "use superpowers for this" → triggers superpowers workflow regardless of classification
- **Force SIMPLE**: User says "just run it" or "keep it simple" → direct execution regardless of classification

---

## 2. Adaptive Workflow Rules

Three workflow paths, selected based on the situation. All run **fully autonomously** — no human checkpoints during the workflow.

### Path 1: New Complex Code

**Trigger**: Agent needs to write complex code that doesn't exist yet.

```
brainstorming (self-directed, autonomous — see Section 3)
  → writing-plans (break into testable steps)
    → test-driven-development (RED → GREEN → REFACTOR per step — see Section 4)
      → verification-before-completion (run all tests, confirm output)
```

### Path 2: Debugging Failed Code

**Trigger**: Code throws a runtime error, produces wrong results, convergence failure, or test failure.

```
systematic-debugging (4-phase root cause investigation)
  → test-driven-development (write regression test for the bug)
    → verification-before-completion (confirm fix, run full suite)
```

### Path 3: Iterating on Existing Code

**Trigger**: Agent needs to modify working code — change parameters, swap analysis method, extend model, user requested changes.

```
writing-plans (plan the changes)
  → test-driven-development (update tests first, then code)
    → verification-before-completion (confirm nothing broke)
```

### Path Selection Logic

The agent determines which path by asking:

1. Does code for this task already exist? → No → **Path 1**
2. Did the existing code fail (error, wrong results, convergence failure)? → Yes → **Path 2**
3. Does the existing code work but needs modification? → Yes → **Path 3**

---

## 3. Autonomous Brainstorming Protocol

When Path 1 triggers, the agent self-directs brainstorming using upstream research context. No human checkpoint.

### Structure

1. **State the goal**: What code needs to be written and why (derived from upstream context)
2. **Generate 2-3 approaches**: Different implementation strategies with trade-offs (e.g., simulation-based vs analytical power, bootstrap vs asymptotic CI, different DGP parameterizations)
3. **Select approach**: Choose based on these criteria, in priority order:
   - (a) Faithfulness to research design (does it match the Experiment Design / Methodology Blueprint?)
   - (b) Statistical rigor (does it follow best practices for this method?)
   - (c) Computational efficiency (will it run in reasonable time?)
   - (d) Testability (can we write meaningful tests for it?)
4. **Document rationale**: Brief log of what was considered and why this approach was chosen (saved to superpowers log — see Section 6)
5. **Proceed to planning**: No pause

### Context Sources Per Agent

| Agent | Upstream Context for Brainstorming |
|-------|-----------------------------------|
| `power_analyst_agent` | Experiment Design (Schema 10): design type, IV/DV, effect size source, alpha, power target |
| `analysis_executor_agent` | Cleaned dataset profile, assumption check results, analysis plan from intake |
| `data_preparation_agent` | Raw dataset profile, missing data patterns, variable types, research requirements |
| `visualization_agent` | Analysis results, publication target requirements, APA format constraints |
| `model_builder_agent` | Simulation Specification (Schema 13): simulation type, DGP description, parameters, convergence criteria |
| `execution_engine_agent` | Executable model from model_builder, parameter grid, convergence thresholds |

---

## 4. TDD Adaptation for Scientific Code

Standard TDD says "write a failing test first." For scientific code, "test" translates to statistical property checks, known-answer validations, and structural assertions.

### Test Strategy Per Agent

| Agent | Test Types |
|-------|-----------|
| `power_analyst_agent` | **Known-answer test**: Run power analysis with published parameters, compare to published N (tolerance ±2). **Boundary test**: Power = 0 when effect = 0; power → 1 when N → ∞. **Monotonicity test**: Power increases with N, effect size, and alpha. |
| `analysis_executor_agent` | **Synthetic data test**: Generate data with known parameters (e.g., two groups with known d = 0.8), run analysis, verify test detects the effect (p < .05). **Null test**: Generate data under H0, verify p > alpha in most runs. **Output structure test**: Result dict contains all required keys for APA formatting. |
| `data_preparation_agent` | **Missing count test**: Missing count decreases (or stays same) after cleaning. **No-new-NaN test**: No unexpected NaN introduced. **Type test**: Column types match expected types after transformation. **Row count test**: Row count within expected range (no accidental drops). |
| `visualization_agent` | **File existence test**: Plot file created at expected path. **Smoke test**: Plot function runs without error on sample data. **Dimensions test**: Figure size matches APA spec (width, DPI). |
| `model_builder_agent` | **Purity test**: Same seed → identical output (call twice, assert equal). **Structure test**: Output dict has required keys (`data`, `truth`). **Edge case test**: Degenerate parameters (n=1, sigma=0) don't crash. **Distribution test**: Generated data has expected distributional properties (mean within 3 SE of target). |
| `execution_engine_agent` | **Reproducibility test**: Same master seed → identical results. **Convergence test**: Known-convergent model converges within iteration limit. **Parallel equivalence test**: Sequential vs parallel produce identical results (same seeds). |

### Test Infrastructure

- **Test location**: `experiment_outputs/tests/`
- **Test naming**: `test_<agent_short_name>_<task_description>.py` (e.g., `test_dgp_two_group_normal.py`)
- **Runner**: `pytest` executed within `experiment_env`
- **Execution command**:
  - Unix: `source experiment_env/bin/activate && pytest experiment_outputs/tests/ -v`
  - Windows: `experiment_env\Scripts\activate && pytest experiment_outputs\tests\ -v`

---

## 5. Escape Hatch Protocol

If any superpowers step fails **twice** on the same problem:

1. **Collect diagnostics**:
   - Error messages and stack traces
   - Test output (which tests pass, which fail)
   - What approaches were tried and why they failed
   - Current state of the code

2. **Surface to user**:

```
⚠ Superpowers Escape Hatch Triggered

Task: [description of what the agent was trying to do]
Workflow: [Path 1/2/3] at step [brainstorming/planning/TDD/verification]
Attempts: 2

What I tried:
1. [First approach and why it failed]
2. [Second approach and why it failed]

Diagnostics:
[Error output / test failures / convergence status]

Options:
A. I try a different approach: [brief description of alternative]
B. You provide guidance on how to proceed
C. Skip superpowers and execute directly (bypass discipline)
```

3. **Wait for user input** before continuing

---

## 6. Logging Protocol

All superpowers workflow decisions and outcomes are logged for traceability.

### Log File

`experiment_outputs/logs/superpowers_log.md`

### Log Entry Format

```markdown
### [YYYY-MM-DD HH:MM] — [Agent Name]

**Task**: [Description of the code task]
**Classification**: SIMPLE | COMPLEX (reason: [matching category])
**Workflow**: Path [1/2/3] | Direct execution
**Steps completed**: [brainstorming ✓ | planning ✓ | TDD ✓ | verification ✓]
**Outcome**: SUCCESS | ESCAPE_HATCH | USER_OVERRIDE
**Tests**: [N] passed, [N] failed — `experiment_outputs/tests/[test_file]`
**Brainstorm rationale** (if Path 1): [1-2 sentence summary of approach selection]
**Duration**: [estimated token/time cost]
```

### Lab Notebook Integration

When a lab notebook is active (`notebook_path` parameter provided), append a summary of each superpowers workflow run to the notebook's **Analysis Log** or **Simulation Log** section:

```markdown
**[NB-XXX] Superpowers Workflow Record**
- Agent: [agent name]
- Task: [description]
- Workflow: Path [1/2/3]
- Approach selected: [brief description]
- Tests: [summary]
- Code files: [paths]
```
