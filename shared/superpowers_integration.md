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

**CRITICAL — How to invoke superpowers skills**: Each step in the workflow below requires invoking the actual superpowers skill via the `Skill` tool. This loads the full skill content (instructions, checklists, process flows) which the agent then follows. Do NOT just follow the protocol descriptions in this file — invoke the real skills.

### Path 1: New Complex Code

**Trigger**: Agent needs to write complex code that doesn't exist yet.

```
Step 1: Invoke Skill("superpowers:brainstorming")
        → Follow the loaded skill, but in autonomous mode (see Section 3)
        → Output: design approach documented in superpowers log

Step 2: Invoke Skill("superpowers:writing-plans")
        → Follow the loaded skill to break the design into testable steps
        → Output: implementation plan with test-first steps

Step 3: Invoke Skill("superpowers:test-driven-development")
        → Follow the loaded skill's RED → GREEN → REFACTOR cycle
        → Use the scientific test adaptations from Section 4
        → Output: tested, working code

Step 4: Invoke Skill("superpowers:verification-before-completion")
        → Follow the loaded skill to run all tests and confirm output
        → Output: verified results
```

### Path 2: Debugging Failed Code

**Trigger**: Code throws a runtime error, produces wrong results, convergence failure, or test failure.

```
Step 1: Invoke Skill("superpowers:systematic-debugging")
        → Follow the loaded skill's 4-phase root cause investigation
        → Output: identified root cause

Step 2: Invoke Skill("superpowers:test-driven-development")
        → Write a regression test for the bug, then fix
        → Output: bug fixed with regression test

Step 3: Invoke Skill("superpowers:verification-before-completion")
        → Run full test suite, confirm fix doesn't break anything
        → Output: verified fix
```

### Path 3: Iterating on Existing Code

**Trigger**: Agent needs to modify working code — change parameters, swap analysis method, extend model, user requested changes.

```
Step 1: Invoke Skill("superpowers:writing-plans")
        → Plan the changes as testable steps
        → Output: modification plan

Step 2: Invoke Skill("superpowers:test-driven-development")
        → Update tests first, then modify code
        → Output: updated code with passing tests

Step 3: Invoke Skill("superpowers:verification-before-completion")
        → Confirm nothing broke
        → Output: verified changes
```

### Path Selection Logic

The agent determines which path by asking:

1. Does code for this task already exist? → No → **Path 1**
2. Did the existing code fail (error, wrong results, convergence failure)? → Yes → **Path 2**
3. Does the existing code work but needs modification? → Yes → **Path 3**

---

## 3. Autonomous Brainstorming Protocol

When Path 1 triggers, the agent invokes `Skill("superpowers:brainstorming")` which loads the full brainstorming skill. However, the brainstorming skill is designed for human-in-the-loop dialogue (ask questions, propose approaches, get approval). In autonomous mode, the agent adapts the skill as follows:

### Adaptation for Autonomous Execution

The brainstorming skill's normal process is: explore context → ask clarifying questions → propose 2-3 approaches → present design → get user approval → write spec. In autonomous mode, the agent replaces human interaction with research context:

1. **Skip clarifying questions**: The agent already has upstream context (see table below). Use it instead of asking the user.
2. **Generate 2-3 approaches**: Follow the brainstorming skill's instruction to propose approaches with trade-offs — but evaluate them yourself.
3. **Select approach**: Choose based on these criteria, in priority order:
   - (a) Faithfulness to research design (does it match the Experiment Design / Methodology Blueprint?)
   - (b) Statistical rigor (does it follow best practices for this method?)
   - (c) Computational efficiency (will it run in reasonable time?)
   - (d) Testability (can we write meaningful tests for it?)
4. **Skip spec writing and review**: The brainstorming skill normally writes a spec doc and dispatches a reviewer. In autonomous mode, skip this — document the rationale in the superpowers log (Section 6) and proceed directly to the next skill invocation.
5. **Proceed to `Skill("superpowers:writing-plans")`**: Do not wait for user approval. The selected approach becomes the input for the planning skill.

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

When the workflow reaches the TDD step, the agent invokes `Skill("superpowers:test-driven-development")` which loads the full TDD skill. The TDD skill enforces RED → GREEN → REFACTOR discipline. Follow it exactly, but use the scientific test patterns below instead of standard unit tests.

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

---

## 7. Runtime Execution Checklist

This is the exact sequence an agent follows when it encounters a code task. Follow these steps mechanically.

### Before Writing Any Code

1. **Identify the code task**: What code needs to be written/modified/debugged?
2. **Classify**: Check the complexity table in Section 1. Is it SIMPLE or COMPLEX?
3. **If SIMPLE**: Write the code directly. Skip the rest of this checklist. Log the classification (Section 6).
4. **If COMPLEX**: Continue to step 5.
5. **Select path**: Use the path selection logic in Section 2 to determine Path 1, 2, or 3.

### Path 1 Execution (New Complex Code)

```
1. Log: "Starting superpowers Path 1 for [task description]"
2. Invoke: Skill("superpowers:brainstorming")
   - When the skill loads, follow it but adapt per Section 3:
     - Use upstream research context instead of asking the user
     - Generate 2-3 approaches, select the best, document rationale
     - Skip spec writing/review — go straight to planning
3. Invoke: Skill("superpowers:writing-plans")
   - When the skill loads, follow it to create a step-by-step plan
   - Each step should be a testable unit of work
   - The plan does NOT need to be saved to docs/superpowers/plans/
     (save to experiment_outputs/logs/ instead)
4. Invoke: Skill("superpowers:test-driven-development")
   - When the skill loads, follow its RED → GREEN → REFACTOR cycle
   - Use the scientific test patterns from Section 4 for this agent
   - Write tests to experiment_outputs/tests/
   - Run tests in experiment_env via pytest
5. Invoke: Skill("superpowers:verification-before-completion")
   - When the skill loads, follow it to verify all tests pass
   - Confirm output files exist and are correct
6. Log the outcome (Section 6)
```

### Path 2 Execution (Debugging Failed Code)

```
1. Log: "Starting superpowers Path 2 for [failure description]"
2. Invoke: Skill("superpowers:systematic-debugging")
   - Follow the skill's 4-phase investigation
   - Do NOT skip to guessing — follow the phases
3. Invoke: Skill("superpowers:test-driven-development")
   - Write a regression test that reproduces the bug
   - Fix the code until the test passes
4. Invoke: Skill("superpowers:verification-before-completion")
   - Run full test suite to confirm fix doesn't break anything
5. Log the outcome (Section 6)
```

### Path 3 Execution (Iterating on Existing Code)

```
1. Log: "Starting superpowers Path 3 for [modification description]"
2. Invoke: Skill("superpowers:writing-plans")
   - Plan the changes as testable steps
3. Invoke: Skill("superpowers:test-driven-development")
   - Update tests first to reflect new expected behavior
   - Then modify the code until tests pass
4. Invoke: Skill("superpowers:verification-before-completion")
   - Confirm all tests pass (old and new)
5. Log the outcome (Section 6)
```

### Escape Hatch

At ANY point during steps 2-5 above, if a step fails twice on the same problem, trigger the escape hatch (Section 5). Do not continue the workflow — surface to the user.
