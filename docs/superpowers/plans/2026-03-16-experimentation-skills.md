# Experimentation Skills Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add 4 new skills (experiment-designer, data-analyst, simulation-runner, lab-notebook) plus shared infrastructure to the academic-research-skills suite, bridging the gap between research and paper writing.

**Architecture:** Each skill follows the existing convention: SKILL.md (frontmatter + comprehensive instructions), agents/*.md (role definitions), templates/*.md (output formats), references/*.md (domain knowledge), examples/*.md (demonstrations). Skills communicate via handoff schemas defined in shared/handoff_schemas.md. All 4 skills share experiment infrastructure (venv management, APA formatting, plot standards).

**Tech Stack:** Markdown skill files following existing conventions. No code to compile. Validation = structural consistency checks.

**Spec:** `docs/superpowers/specs/2026-03-16-experimentation-skills-design.md`

**Existing patterns to follow:**
- `deep-research/SKILL.md` — SKILL.md frontmatter and structure reference
- `deep-research/agents/research_architect_agent.md` — Agent file structure reference
- `shared/handoff_schemas.md` — Handoff schema format reference
- `academic-pipeline/SKILL.md` — Pipeline integration reference

**Important conventions (from codebase analysis):**
- SKILL.md frontmatter: `name`, `description` (trigger keywords embedded), `metadata.version`, `metadata.last_updated`
- Agent files: `## Role Definition`, `## Core Principles`, domain-specific sections, `## Output Format`, `## Quality Criteria`
- Templates: Markdown with placeholder fields in `[brackets]` or backtick code blocks
- References: Factual domain knowledge, decision trees, guidelines — no agent instructions
- All content in English (the existing skills use English internally, with zh-TW trigger keywords in SKILL.md only)
- Material Passport (Schema 9) accompanies every handoff artifact

---

## Chunk 1: Shared Infrastructure + Handoff Schemas

This chunk creates the foundation that all 4 skills depend on. Must be completed first.

### Task 1.1: Create shared/experiment_infrastructure.md

**Files:**
- Create: `shared/experiment_infrastructure.md`

- [ ] **Step 1: Read the existing shared/handoff_schemas.md for format conventions**

Read `shared/handoff_schemas.md` to match the documentation style (headers, tables, code blocks).

- [ ] **Step 2: Write experiment_infrastructure.md**

Create `shared/experiment_infrastructure.md` with all 7 sections from the spec:
1. Venv Management Protocol (create at `./experiment_env/`, core packages list, reuse logic)
2. APA Statistical Formatting Rules (rounding rules, effect size thresholds, table style)
3. Plot Generation Standards (seaborn style, 300 DPI, Times New Roman, colorblind-safe, PNG+PDF)
4. Output Directory Convention (the `./experiment_outputs/` tree)
5. Agent Naming Convention (fully-qualified cross-skill references)
6. Auto-Logging Protocol (notebook_path passing, phase-end appending, standalone behavior)
7. Failure Paths table (11 failure scenarios with triggers and recovery)

Reference spec sections 1.1 through 1.7 for exact content.

- [ ] **Step 3: Commit**

```bash
git add shared/experiment_infrastructure.md
git commit -m "feat: add shared experiment infrastructure (venv, APA, plots, logging, failures)"
```

### Task 1.2: Add Schemas 10-13 to shared/handoff_schemas.md

**Files:**
- Modify: `shared/handoff_schemas.md` (append after Schema 9)

- [ ] **Step 1: Read current handoff_schemas.md to understand the exact format**

Read `shared/handoff_schemas.md` in full — pay attention to table structure, field types, example blocks, and validation rules section.

- [ ] **Step 2: Append Schema 10 (Experiment Design)**

Add after the existing Schema 9 section. Follow the exact format: `## Schema 10: Experiment Design`, Producer/Consumer line, Required Fields table, conditional fields, Example block. Copy all fields from spec Section 7 Schema 10.

- [ ] **Step 3: Append Schema 11 (Experiment Results)**

Same format. All fields from spec Section 7 Schema 11. Note: this schema has two producers (`data-analyst/report_compiler_agent | simulation-runner/report_compiler_agent`).

- [ ] **Step 4: Append Schema 12 (Lab Record)**

Same format. All fields from spec Section 7 Schema 12.

- [ ] **Step 5: Append Schema 13 (Simulation Specification)**

Same format. All fields from spec Section 7 Schema 13. Producer is `experiment-designer/protocol_compiler_agent` only.

- [ ] **Step 6: Update Validation Rules section**

Add rules for the new schemas:
- Schema 10 `experiment_id` must be unique and referenced by Schemas 11, 12, 13
- Schema 11 `experiment_id` must match an existing Schema 10 artifact
- Schema 13 is conditional: only produced when Schema 10 `design_type` is `simulation`
- Cross-reference: figures/tables in Schema 11 must have corresponding files in `experiment_outputs/`

- [ ] **Step 7: Commit**

```bash
git add shared/handoff_schemas.md
git commit -m "feat: add handoff schemas 10-13 (experiment design, results, lab record, simulation spec)"
```

---

## Chunk 2: experiment-designer Skill

18 files total. Build in order: SKILL.md first (defines the skill), then references (domain knowledge agents need), then templates (output formats agents produce), then agents (the actual workers), then examples.

### Task 2.1: Create experiment-designer/SKILL.md

**Files:**
- Create: `experiment-designer/SKILL.md`

- [ ] **Step 1: Read deep-research/SKILL.md for the exact frontmatter and structure pattern**

Read `deep-research/SKILL.md` in full. Note: frontmatter format (`name`, `description` with embedded trigger keywords, `metadata.version`, `metadata.last_updated`), Quick Start section, Trigger Conditions section, Mode Selection Guide, Agent Team table, execution flow, distinction tables.

- [ ] **Step 2: Write experiment-designer/SKILL.md**

Follow the exact structure from deep-research/SKILL.md. Include:
- Frontmatter: name `experiment-designer`, description with ALL trigger keywords (English + zh-TW) from spec Section 2.2b, version `1.0`, last_updated `2026-03-16`
- Quick Start with minimal command examples
- Trigger Conditions: English keywords, zh-TW keywords, Guided mode activation (intent signals + default rule: prefer guided when ambiguous), Does NOT trigger table
- Mode Selection Guide table (5 modes from spec Section 2.2)
- Agent Team table (6 agents from spec Section 2.3)
- Execution flow (Phase 0 -> Phase 1 -> Phase 2 -> Phase 3)
- Distinction from `data-analyst` table (design vs execution)
- Key deliverables list
- Integration points (upstream: Schema 1 + Methodology Blueprint, downstream: Schema 10 + Schema 13)
- Checkpoint: user confirmation after protocol compilation

- [ ] **Step 3: Commit**

```bash
git add experiment-designer/SKILL.md
git commit -m "feat: add experiment-designer SKILL.md (5 modes, 6 agents)"
```

### Task 2.2: Create experiment-designer references (5 files)

**Files:**
- Create: `experiment-designer/references/experimental_design_patterns.md`
- Create: `experiment-designer/references/power_analysis_guide.md`
- Create: `experiment-designer/references/instrument_development_guide.md`
- Create: `experiment-designer/references/randomization_methods.md`
- Create: `experiment-designer/references/equator_protocol_guidelines.md`

- [ ] **Step 1: Read deep-research/references/methodology_patterns.md for reference file conventions**

Read `deep-research/references/methodology_patterns.md` to understand: `## Purpose` header, decision trees in code blocks, template sections, quality criteria.

- [ ] **Step 2: Write experimental_design_patterns.md**

Decision tree for selecting experimental design. Include:
- Purpose section
- Design decision tree (RCT, factorial 2x2/2x3/3x3, crossover, Solomon four-group, quasi-experimental with subtypes: nonequivalent control group / interrupted time series / regression discontinuity, single-subject: ABAB / multiple baseline, correlational, simulation)
- For each design: When to Use, Design Template (IV/DV/controls/randomization), Threats to Validity, Reporting Standard
- "Choosing the Right Design" summary flowchart

- [ ] **Step 3: Write power_analysis_guide.md**

Comprehensive power analysis reference. Include:
- Purpose section
- Core concepts: alpha, beta, power (1-beta), effect size, sample size relationship
- Effect size conventions table (Cohen's d: 0.2/0.5/0.8, eta-sq: 0.01/0.06/0.14, r: 0.1/0.3/0.5, OR: 1.5/2.5/4.0, etc.)
- Python code examples using statsmodels and scipy for: t-test power, ANOVA power, correlation power, chi-square power, regression power
- Power curve generation code (matplotlib)
- Common pitfalls: post-hoc power, ignoring attrition, using wrong effect size metric
- Sensitivity analysis: compute minimum detectable effect for given N
- Special cases: multilevel designs, repeated measures, cluster randomization (design effect)

- [ ] **Step 4: Write instrument_development_guide.md**

Measurement instrument development reference. Include:
- Purpose section
- Item writing rules (clear, single-barreled, avoid double negatives, balanced scales)
- Scale types: Likert (4/5/6/7-point), semantic differential, visual analog, forced choice
- Validity types: content (expert panel), construct (factor analysis), criterion (concurrent/predictive), face
- Reliability types: internal consistency (Cronbach's alpha > 0.7, McDonald's omega), test-retest (ICC), inter-rater (Cohen's kappa, Krippendorff's alpha)
- Pilot testing protocol (cognitive interviews, item analysis, reliability check)
- Rubric development: analytic vs holistic, criterion definition, anchor examples
- Coding scheme development: deductive vs inductive, codebook structure, inter-coder reliability protocol

- [ ] **Step 5: Write randomization_methods.md**

Randomization methods with Python code. Include:
- Purpose section
- Methods: simple random (numpy), stratified (block by covariates), block (permuted blocks), cluster (unit of randomization != unit of analysis), adaptive (minimization)
- Python code for each method using numpy.random.Generator (NOT legacy RandomState)
- Allocation ratio examples (1:1, 2:1, 1:1:1)
- Seed management: how to record and reproduce sequences
- When NOT to randomize: quasi-experimental designs, ethical constraints, feasibility issues

- [ ] **Step 6: Write equator_protocol_guidelines.md**

EQUATOR reporting guidelines specific to experimental protocols. Include:
- Purpose section
- SPIRIT 2013 checklist (for trial protocols): all 33 items with descriptions
- STROBE checklist (for observational studies): key items
- CONSORT 2010 checklist (for reporting trials): key items relevant to protocol design
- TREND statement (for non-randomized evaluations)
- Mapping: design type -> recommended reporting guideline

- [ ] **Step 7: Commit**

```bash
git add experiment-designer/references/
git commit -m "feat: add experiment-designer references (design patterns, power, instruments, randomization, EQUATOR)"
```

### Task 2.3: Create experiment-designer templates (4 files)

**Files:**
- Create: `experiment-designer/templates/experiment_protocol_template.md`
- Create: `experiment-designer/templates/power_analysis_template.md`
- Create: `experiment-designer/templates/instrument_template.md`
- Create: `experiment-designer/templates/threats_to_validity_template.md`

- [ ] **Step 1: Read deep-research/templates/preregistration_template.md for template conventions**

Read `deep-research/templates/preregistration_template.md` to understand: `## Purpose`, `## Instructions`, fill-in sections with `[brackets]`, Required/Optional markers.

- [ ] **Step 2: Write all 4 templates**

Follow the preregistration template style. Each template should have:
- `## Purpose` header explaining what the template produces
- `## Instructions` with numbered steps
- Fill-in sections with `[placeholder text]`
- Required vs Optional field markers
- Schema reference (which handoff schema this template feeds into)

**experiment_protocol_template.md**: Full experimental protocol covering study info, design, variables, sample, randomization, instruments, procedures, analysis plan, ethics, timeline. Maps to Schema 10.

**power_analysis_template.md**: Power analysis report format — test type, parameters (alpha, power, effect size), sample size result, power curve figure reference, sensitivity analysis table. Referenced by power_analyst_agent output.

**instrument_template.md**: Measurement instrument format — construct definition, item pool, scale format, scoring, validity assessment plan, pilot results. Referenced by instrument_builder_agent output.

**threats_to_validity_template.md**: Validity threats matrix — rows for each threat type (internal: history, maturation, testing, instrumentation, regression, selection, mortality, diffusion; external: population, ecological, temporal; construct: mono-operation, mono-method, hypothesis guessing, experimenter expectancy; statistical: low power, violated assumptions, fishing), columns for threat description, likelihood (high/medium/low), mitigation strategy, residual risk.

- [ ] **Step 3: Commit**

```bash
git add experiment-designer/templates/
git commit -m "feat: add experiment-designer templates (protocol, power, instrument, threats)"
```

### Task 2.4: Create experiment-designer agents (6 files)

**Files:**
- Create: `experiment-designer/agents/intake_agent.md`
- Create: `experiment-designer/agents/design_architect_agent.md`
- Create: `experiment-designer/agents/power_analyst_agent.md`
- Create: `experiment-designer/agents/instrument_builder_agent.md`
- Create: `experiment-designer/agents/randomization_agent.md`
- Create: `experiment-designer/agents/protocol_compiler_agent.md`

- [ ] **Step 1: Read deep-research/agents/research_architect_agent.md AND academic-paper/agents/intake_agent.md for agent file conventions**

Read both files. Note the structure: `## Role Definition` (identity + core function), `## Core Principles` (numbered list), domain-specific sections (decision trees, tables, procedures), `## Output Format` (markdown template), `## Quality Criteria` (bullet list).

- [ ] **Step 2: Write intake_agent.md**

Role: Parse user request, determine mode, validate upstream inputs.
- Mode detection logic (map user intent to 5 modes)
- Input validation: check for RQ Brief (Schema 1), Methodology Blueprint, or user-supplied experiment description
- If no upstream input: prompt user for minimum info (research question, methodology type, target population)
- Output: mode selection + validated input summary
- Guided mode activation: intent signal matching (same pattern as deep-research socratic mode)

- [ ] **Step 3: Write design_architect_agent.md**

Role: Core experimental design selection and specification.
- Design decision tree (from experimental_design_patterns.md reference)
- For selected design: define IV (levels, manipulation), DV (measurement, operationalization), control variables, confounds
- Threats to validity identification (Campbell & Stanley framework)
- Internal validity vs external validity trade-off analysis
- Output: Design specification section of protocol
- Must reference `references/experimental_design_patterns.md`

- [ ] **Step 4: Write power_analyst_agent.md**

Role: Execute power analysis via Python.
- Determine appropriate power analysis type based on design
- Generate Python code using statsmodels.stats.power (TTestPower, FTestAnovaPower, GofChisquarePower, NormalIndPower) and scipy.stats
- Execute the code via Bash tool in experiment_env venv
- Generate power curves (matplotlib) saved to experiment_outputs/figures/
- Sensitivity analysis: compute MDE for range of sample sizes
- Output format: power analysis report per power_analysis_template.md
- Must reference `references/power_analysis_guide.md`
- **Venv setup**: If `./experiment_env/` does not exist, create it and install packages per shared/experiment_infrastructure.md before executing any Python

- [ ] **Step 5: Write instrument_builder_agent.md**

Role: Build measurement instruments.
- Determine instrument type needed (survey, rubric, coding scheme, observation protocol)
- For surveys: generate items following item writing rules, specify scale type, define scoring
- For rubrics: define criteria, levels, descriptors, anchor examples
- For coding schemes: define categories, coding rules, examples, inter-coder protocol
- Content validity assessment: expert panel review simulation
- Pilot testing plan
- Output format: instrument per instrument_template.md
- Must reference `references/instrument_development_guide.md`

- [ ] **Step 6: Write randomization_agent.md**

Role: Design and generate allocation sequences.
- Select randomization method based on design (simple, stratified, block, cluster)
- Generate Python code using numpy.random.Generator
- Execute code to produce actual randomization schedule
- Record seeds for reproducibility
- Output: randomization schedule table + code + seed log
- Must reference `references/randomization_methods.md`
- Skip entirely for quasi-experimental and correlational designs

- [ ] **Step 7: Write protocol_compiler_agent.md**

Role: Assemble complete experiment protocol and produce Schema 10.
- Collect outputs from all Phase 1-2 agents
- Cross-validate: design matches power analysis (effect size/N alignment), instruments measure declared DVs, randomization matches design type
- Assemble into experiment_protocol_template.md format
- Produce Schema 10 handoff artifact with all required fields
- If design_type is `simulation`, ALSO produce Schema 13 handoff artifact
- Attach Material Passport (Schema 9)
- Quality gate: all cross-validation checks must pass before handoff

- [ ] **Step 8: Commit**

```bash
git add experiment-designer/agents/
git commit -m "feat: add experiment-designer agents (intake, design, power, instrument, randomization, compiler)"
```

### Task 2.5: Create experiment-designer examples (2 files)

**Files:**
- Create: `experiment-designer/examples/rct_design_example.md`
- Create: `experiment-designer/examples/quasi_experimental_example.md`

- [ ] **Step 1: Read deep-research/examples/exploratory_research.md for example file conventions**

Read to understand format: scenario description, user input, step-by-step agent outputs, final deliverable.

- [ ] **Step 2: Write rct_design_example.md**

Complete walkthrough of designing an RCT:
- Scenario: "Design an experiment testing the effect of AI-assisted feedback on student learning outcomes in a university physics course"
- Show each agent's output in sequence (intake -> design architect -> power analyst -> instrument builder -> randomization -> protocol compiler)
- Include actual power analysis output (pre-computed), randomization schedule snippet, instrument items
- Final Schema 10 artifact

- [ ] **Step 3: Write quasi_experimental_example.md**

Walkthrough of a quasi-experimental design:
- Scenario: "Design a study comparing two teaching methods across existing class sections (cannot randomize students)"
- Show nonequivalent control group design selection, propensity score matching discussion, threats to validity (selection bias)
- No randomization agent (skipped)
- Final Schema 10 artifact

- [ ] **Step 4: Commit**

```bash
git add experiment-designer/examples/
git commit -m "feat: add experiment-designer examples (RCT, quasi-experimental)"
```

---

## Chunk 3: data-analyst Skill

20 files total. Same build order: SKILL.md -> references -> templates -> agents -> examples.

### Task 3.1: Create data-analyst/SKILL.md

**Files:**
- Create: `data-analyst/SKILL.md`

- [ ] **Step 1: Write data-analyst/SKILL.md**

Same structure as experiment-designer/SKILL.md. Include:
- Frontmatter with ALL trigger keywords from spec Section 3.2b (English + zh-TW)
- Quick Start (minimal command: "Analyze my data: [path to CSV]")
- Trigger Conditions with guided mode activation
- Mode Selection Guide (6 modes)
- Agent Team table (7 agents)
- Execution flow (Phase 0 -> 1 -> 2 -> 3 -> 4 -> 5)
- Statistical Methods Coverage table (from spec Section 3.4)
- Distinction from `simulation-runner` table
- Key deliverables
- Integration points (upstream: Schema 10 or user data, downstream: Schema 11)
- Additional venv packages (semopy, lifelines, openpyxl, pyreadstat)

- [ ] **Step 2: Commit**

```bash
git add data-analyst/SKILL.md
git commit -m "feat: add data-analyst SKILL.md (6 modes, 7 agents)"
```

### Task 3.2: Create data-analyst references (6 files)

**Files:**
- Create: `data-analyst/references/statistical_test_decision_tree.md`
- Create: `data-analyst/references/assumption_testing_guide.md`
- Create: `data-analyst/references/apa_stats_formatting_guide.md`
- Create: `data-analyst/references/effect_size_interpretation_guide.md`
- Create: `data-analyst/references/missing_data_strategies.md`
- Create: `data-analyst/references/common_analysis_pitfalls.md`

- [ ] **Step 1: Write statistical_test_decision_tree.md**

Comprehensive decision tree: research question type -> data type -> number of groups -> test selection.
- Purpose section
- Master decision tree covering all tests in spec Section 3.4
- For each test: when to use, assumptions, Python function (scipy/statsmodels/pingouin), non-parametric alternative
- Quick reference table: scenario -> recommended test -> Python code

- [ ] **Step 2: Write assumption_testing_guide.md**

Per-assumption testing procedures with Python code.
- Normality: Shapiro-Wilk (scipy.stats.shapiro), Q-Q plot (scipy.stats.probplot + matplotlib), skewness/kurtosis thresholds
- Homogeneity of variance: Levene's test (scipy.stats.levene), Bartlett's (if normal)
- Sphericity: Mauchly's test (pingouin), Greenhouse-Geisser/Huynh-Feldt corrections
- Linearity: residual plots, RESET test
- Independence: Durbin-Watson (statsmodels)
- Multicollinearity: VIF (statsmodels), correlation matrix
- Homoscedasticity: Breusch-Pagan (statsmodels)
- For each: what to do when violated (transformation, non-parametric alternative, robust method)

- [ ] **Step 3: Write apa_stats_formatting_guide.md**

APA 7 formatting for every statistical test.
- Master formatting rules (italicize test statistics, no leading zero on p-values, exact p to 3 decimals except p < .001)
- Per-test format strings:
  - t-test: `t(df) = X.XX, p = .XXX, d = X.XX, 95% CI [X.XX, X.XX]`
  - ANOVA: `F(df1, df2) = X.XX, p = .XXX, eta-sq = .XX`
  - Chi-square: `chi-sq(df) = X.XX, p = .XXX, Cramer's V = .XX`
  - Correlation: `r(df) = .XX, p = .XXX`
  - Regression: `b = X.XX, SE = X.XX, t(df) = X.XX, p = .XXX, 95% CI [X.XX, X.XX]`
  - etc. for all tests in the coverage table
- Table formatting rules (APA 7 table style)
- Figure caption formatting

- [ ] **Step 4: Write effect_size_interpretation_guide.md**

Effect size conventions and interpretation.
- Cohen's benchmarks table (d, r, eta-sq, omega-sq, Cramer's V, odds ratio)
- Domain-specific benchmarks (education: Hattie's zone of desired effects d > 0.4; psychology; medicine: NNT)
- CI computation methods for each effect size
- When Cohen's benchmarks are misleading (field-specific norms matter more)
- Practical significance vs statistical significance

- [ ] **Step 5: Write missing_data_strategies.md**

Missing data handling decision tree.
- Missing data mechanisms: MCAR, MAR, MNAR — how to diagnose (Little's MCAR test)
- Strategies: listwise deletion, pairwise deletion, mean imputation (NOT recommended), multiple imputation (MI), FIML
- Decision tree: mechanism -> strategy
- Python code for MI (from sklearn or statsmodels)
- Reporting requirements: percentage missing, mechanism assessment, strategy used

- [ ] **Step 6: Write common_analysis_pitfalls.md**

Common mistakes and how to avoid them.
- Multiple comparisons problem (family-wise error rate, Bonferroni, Holm, FDR)
- p-hacking / garden of forking paths
- HARKing (Hypothesizing After Results are Known)
- Outlier handling: when to remove, when to keep, winsorization, robust methods
- Confusing correlation with causation
- Ignoring effect sizes (reporting only p-values)
- Overfitting (too many predictors for sample size)
- Ecological fallacy
- Each pitfall: description, how to detect, how to prevent, APA reporting requirement

- [ ] **Step 7: Commit**

```bash
git add data-analyst/references/
git commit -m "feat: add data-analyst references (decision tree, assumptions, APA, effect sizes, missing data, pitfalls)"
```

### Task 3.3: Create data-analyst templates (4 files)

**Files:**
- Create: `data-analyst/templates/analysis_report_template.md`
- Create: `data-analyst/templates/apa_results_template.md`
- Create: `data-analyst/templates/assumption_report_template.md`
- Create: `data-analyst/templates/data_cleaning_log_template.md`

- [ ] **Step 1: Write all 4 templates**

**analysis_report_template.md**: Full analysis report — dataset summary, cleaning log reference, assumption checks summary, primary results (APA text + tables + figures), secondary results, exploratory findings, limitations, reproducibility info (script path, environment). Maps to Schema 11.

**apa_results_template.md**: Per-test-type APA text blocks. Template patterns for reporting each statistical test with fill-in values. E.g., "A [test type] was conducted to examine [research question]. Results indicated [significant/non-significant] [test stat], [p-value], [effect size]. [Interpretation]."

**assumption_report_template.md**: Assumption check report — per-assumption: test used, result (statistic + p-value), diagnostic plot reference, decision (assumption met/violated), action taken.

**data_cleaning_log_template.md**: Cleaning log — original dataset summary (N, variables, types), steps taken (recoding, exclusions, transformations), each with justification, final dataset summary, exclusion flowchart.

- [ ] **Step 2: Commit**

```bash
git add data-analyst/templates/
git commit -m "feat: add data-analyst templates (report, APA results, assumptions, cleaning log)"
```

### Task 3.4: Create data-analyst agents (7 files)

**Files:**
- Create: `data-analyst/agents/intake_agent.md`
- Create: `data-analyst/agents/data_preparation_agent.md`
- Create: `data-analyst/agents/assumption_checker_agent.md`
- Create: `data-analyst/agents/analysis_executor_agent.md`
- Create: `data-analyst/agents/effect_size_agent.md`
- Create: `data-analyst/agents/visualization_agent.md`
- Create: `data-analyst/agents/report_compiler_agent.md`

- [ ] **Step 1: Write intake_agent.md**

Role: Parse request, locate data, profile dataset.
- Detect data file format (CSV, Excel, SPSS .sav, Stata .dta) by extension
- Venv setup: ensure experiment_env exists with all packages including extras (semopy, lifelines, openpyxl, pyreadstat)
- Load data via Python (pandas.read_csv / read_excel / pyreadstat.read_sav / pyreadstat.read_dta)
- Profile: shape, column types, missing values count per column, first 5 rows summary
- Mode detection logic
- If Schema 10 available: extract analysis_plan and use it; if not: determine from user request
- Output: dataset profile + mode + analysis plan (explicit or to be determined in guided mode)

- [ ] **Step 2: Write data_preparation_agent.md**

Role: Clean and prepare data.
- Missing values: diagnose mechanism (Little's MCAR test), apply strategy per missing_data_strategies.md
- Outliers: detect (IQR method for univariate, Mahalanobis for multivariate), present to user, apply agreed action
- Recoding: create dummy variables, reverse-code items, compute scale scores
- Transformations: log, sqrt, Box-Cox if needed for normality
- Save cleaned dataset to `experiment_outputs/tables/cleaned_data.csv`
- Save cleaning log per data_cleaning_log_template.md
- All operations via Python (pandas), executed in experiment_env
- Must reference `references/missing_data_strategies.md`

- [ ] **Step 3: Write assumption_checker_agent.md**

Role: Test statistical assumptions.
- Determine which assumptions to test based on planned analysis
- Execute tests via Python (scipy.stats, statsmodels, pingouin)
- Generate diagnostic plots (Q-Q, residual, homogeneity) saved to experiment_outputs/figures/
- For each assumption: report test statistic, p-value, visual diagnosis, decision
- If violated: recommend alternative (non-parametric, robust, transformation)
- Output: assumption report per assumption_report_template.md
- Must reference `references/assumption_testing_guide.md`

- [ ] **Step 4: Write analysis_executor_agent.md**

Role: Run the primary statistical analyses.
- Execute analyses based on analysis plan (from Schema 10 or guided mode decision)
- Generate Python code using: scipy.stats, statsmodels, pingouin, sklearn, semopy, lifelines
- Execute in experiment_env via Bash
- Capture all results: test statistics, p-values, degrees of freedom, confidence intervals
- For each analysis: raw output + formatted APA string
- Save analysis script to `experiment_outputs/scripts/analysis.py` (full reproducibility script)
- Must reference `references/statistical_test_decision_tree.md`

- [ ] **Step 5: Write effect_size_agent.md**

Role: Compute and interpret effect sizes.
- For each analysis result: compute appropriate effect size (Cohen's d, eta-sq, omega-sq, r-sq, OR, Cramer's V)
- Compute 95% CIs for all effect sizes (bootstrap when analytical formula unavailable)
- Classify magnitude per Cohen's conventions AND domain-specific benchmarks
- Practical significance interpretation
- Output: effect size table with CIs and interpretations
- Must reference `references/effect_size_interpretation_guide.md`

- [ ] **Step 6: Write visualization_agent.md**

Role: Generate publication-quality figures.
- Select appropriate plot type per analysis (bar charts for group comparisons, scatter for correlations, box plots for distributions, forest plots for effect sizes, interaction plots for factorial designs, residual plots for regression diagnostics, heatmaps for correlation matrices)
- Generate via matplotlib/seaborn following shared/experiment_infrastructure.md plot standards
- Save PNG (preview) + PDF (LaTeX) to experiment_outputs/figures/
- Number figures sequentially (Figure 1, Figure 2...)
- Generate APA-style figure captions
- Execute all plotting code in experiment_env

- [ ] **Step 7: Write report_compiler_agent.md**

Role: Assemble analysis report and produce Schema 11.
- Collect outputs from all preceding agents
- Assemble into analysis_report_template.md format
- Generate APA results text blocks per apa_results_template.md patterns
- Number and caption all tables and figures
- Produce Schema 11 handoff artifact with all required fields
- Attach Material Passport (Schema 9)
- If auto-logging active (notebook_path provided): append analysis log entry to notebook

- [ ] **Step 8: Commit**

```bash
git add data-analyst/agents/
git commit -m "feat: add data-analyst agents (intake, prep, assumptions, executor, effect size, viz, compiler)"
```

### Task 3.5: Create data-analyst examples (2 files)

**Files:**
- Create: `data-analyst/examples/anova_analysis_example.md`
- Create: `data-analyst/examples/regression_analysis_example.md`

- [ ] **Step 1: Write anova_analysis_example.md**

Complete walkthrough: one-way ANOVA with post-hoc tests.
- Scenario: comparing exam scores across 3 teaching methods (N=90, 30 per group)
- Show: data loading, cleaning, assumption checks (normality per group, Levene's), ANOVA execution, Tukey HSD post-hoc, effect size (eta-sq), box plot, APA results text, Schema 11 artifact

- [ ] **Step 2: Write regression_analysis_example.md**

Complete walkthrough: multiple regression.
- Scenario: predicting GPA from study hours, attendance, prior achievement (N=200)
- Show: data profiling, missing data handling, assumption checks (linearity, normality of residuals, multicollinearity VIF, homoscedasticity), regression execution, standardized betas, R-sq, scatter plots with regression line, residual plots, APA results text, Schema 11 artifact

- [ ] **Step 3: Commit**

```bash
git add data-analyst/examples/
git commit -m "feat: add data-analyst examples (ANOVA, regression)"
```

---

## Chunk 4: simulation-runner Skill

17 files total.

### Task 4.1: Create simulation-runner/SKILL.md

**Files:**
- Create: `simulation-runner/SKILL.md`

- [ ] **Step 1: Write simulation-runner/SKILL.md**

Same structure. Include:
- Frontmatter with trigger keywords from spec Section 4.2b
- Quick Start
- Trigger Conditions with guided mode activation
- Mode Selection Guide (6 modes)
- Agent Team table (5 agents)
- Execution flow
- Simulation Types Coverage table
- Distinction from `data-analyst` table
- Ad-hoc request minimum fields (from spec Section 4.2b)
- Additional venv packages (joblib, networkx, tqdm)
- Integration points

- [ ] **Step 2: Commit**

```bash
git add simulation-runner/SKILL.md
git commit -m "feat: add simulation-runner SKILL.md (6 modes, 5 agents)"
```

### Task 4.2: Create simulation-runner references (5 files)

**Files:**
- Create: `simulation-runner/references/simulation_design_patterns.md`
- Create: `simulation-runner/references/convergence_criteria_guide.md`
- Create: `simulation-runner/references/seed_management_guide.md`
- Create: `simulation-runner/references/parallel_execution_guide.md`
- Create: `simulation-runner/references/reporting_simulation_studies.md`

- [ ] **Step 1: Write simulation_design_patterns.md**

Decision tree for simulation type selection. Cover all 8 types from spec Section 4.4. For each: when to use, model structure, key parameters, convergence criterion, Python libraries.

- [ ] **Step 2: Write convergence_criteria_guide.md**

When to stop iterating. Include: Monte Carlo standard error (MCSE < threshold), Gelman-Rubin R-hat (< 1.05), effective sample size (ESS > 400), visual diagnostics (trace plots, autocorrelation plots). Early stopping rules. What to do when convergence fails.

- [ ] **Step 3: Write seed_management_guide.md**

Reproducibility via seed management. Include: numpy.random.Generator vs legacy RandomState (always use Generator), SeedSequence for parallel streams, recording seeds in output, seed log format. Python code examples.

- [ ] **Step 4: Write parallel_execution_guide.md**

When and how to parallelize. Include: joblib Parallel/delayed, multiprocessing.Pool, when parallelization helps (independent iterations), when it doesn't (sequential dependencies), overhead estimation. Code examples.

- [ ] **Step 5: Write reporting_simulation_studies.md**

ADEMP framework (Aims, Data-generating mechanisms, Estimands, Methods, Performance measures). Include: full ADEMP checklist with descriptions, reporting table format, Morris et al. (2019) recommendations. This framework is referenced by Schema 13's `ademp_checklist` field.

- [ ] **Step 6: Commit**

```bash
git add simulation-runner/references/
git commit -m "feat: add simulation-runner references (patterns, convergence, seeds, parallel, ADEMP)"
```

### Task 4.3: Create simulation-runner templates (4 files)

**Files:**
- Create: `simulation-runner/templates/simulation_report_template.md`
- Create: `simulation-runner/templates/model_specification_template.md`
- Create: `simulation-runner/templates/convergence_report_template.md`
- Create: `simulation-runner/templates/parameter_sweep_template.md`

- [ ] **Step 1: Write all 4 templates**

**simulation_report_template.md**: Full simulation study report — ADEMP summary, model specification reference, execution parameters, results (point estimates, CIs, convergence status), diagnostic plots, seed log, reproducibility script reference. Maps to Schema 11.

**model_specification_template.md**: Mathematical model documentation — DGP description (distributions, parameters, functional form), assumptions, parameter table (name, type, default, range), known limitations.

**convergence_report_template.md**: Convergence diagnostics — per-estimand: MCSE, R-hat, ESS, trace plot reference, autocorrelation plot reference, verdict (converged/not converged/marginal).

**parameter_sweep_template.md**: Sensitivity analysis report — parameter grid, results matrix, tornado/spider plot references, main effects, interaction effects, robust region identification.

- [ ] **Step 2: Commit**

```bash
git add simulation-runner/templates/
git commit -m "feat: add simulation-runner templates (report, model spec, convergence, parameter sweep)"
```

### Task 4.4: Create simulation-runner agents (5 files)

**Files:**
- Create: `simulation-runner/agents/intake_agent.md`
- Create: `simulation-runner/agents/model_builder_agent.md`
- Create: `simulation-runner/agents/execution_engine_agent.md`
- Create: `simulation-runner/agents/diagnostics_agent.md`
- Create: `simulation-runner/agents/report_compiler_agent.md`

- [ ] **Step 1: Write intake_agent.md**

Role: Parse request, determine simulation type, validate inputs.
- Detect simulation type from user request or Schema 10/13
- For bootstrap: validate data file exists and is loadable
- For Monte Carlo: validate model specification (DGP, parameters)
- Ad-hoc: enforce minimum fields (type, model/data, iterations, measures)
- Venv setup: ensure experiment_env with extras (joblib, networkx, tqdm)
- Mode detection

- [ ] **Step 2: Write model_builder_agent.md**

Role: Translate conceptual model to Python code.
- For Monte Carlo: generate DGP function (sample from distributions, apply transformations, add noise)
- For bootstrap: generate resampling function (numpy.random.Generator.choice with replacement)
- For agent-based: define agent class, rules, environment, interaction topology (networkx)
- For power simulation: wrap analysis function inside DGP loop
- For parameter sweep: parameterize DGP, define grid
- Output: Python function(s) + parameter dictionary
- Must reference `references/simulation_design_patterns.md`

- [ ] **Step 3: Write execution_engine_agent.md**

Role: Run the simulation.
- Execute iterations with seed management (SeedSequence for reproducibility)
- Parallelize when appropriate (joblib for independent iterations)
- Monitor convergence: compute running MCSE every N iterations, check R-hat for multiple chains
- Early stopping: if convergence criteria met before max iterations
- Progress tracking (tqdm)
- Save results to experiment_outputs/
- Must reference `references/convergence_criteria_guide.md` and `references/seed_management_guide.md`

- [ ] **Step 4: Write diagnostics_agent.md**

Role: Assess simulation quality.
- Compute: MCSE, R-hat, ESS, autocorrelation
- Generate diagnostic plots: trace plots, autocorrelation plots, distribution plots, running mean plots
- For parameter sweeps: heatmaps, tornado plots, spider/radar plots
- Flag non-convergence with specific recommendations
- Output: convergence report per convergence_report_template.md

- [ ] **Step 5: Write report_compiler_agent.md**

Role: Assemble simulation report and produce Schema 11.
- Collect all outputs
- Assemble per simulation_report_template.md
- Generate APA-formatted results text for simulation findings
- Produce Schema 11 handoff artifact (consumes Schema 13 for model provenance)
- Attach Material Passport
- Seed log: record all seeds used in reproducible format
- If auto-logging active: append simulation log entry to notebook

- [ ] **Step 6: Commit**

```bash
git add simulation-runner/agents/
git commit -m "feat: add simulation-runner agents (intake, model builder, engine, diagnostics, compiler)"
```

### Task 4.5: Create simulation-runner examples (2 files)

**Files:**
- Create: `simulation-runner/examples/monte_carlo_power_example.md`
- Create: `simulation-runner/examples/bootstrap_ci_example.md`

- [ ] **Step 1: Write monte_carlo_power_example.md**

Walkthrough: simulated power analysis for a 2x3 mixed ANOVA.
- Scenario: analytical power formulas don't exist for this complex design
- Show: DGP definition (normal distributions with specified means/SDs per cell), iteration loop, significance counting, power curve across sample sizes, convergence diagnostics

- [ ] **Step 2: Write bootstrap_ci_example.md**

Walkthrough: bootstrap confidence intervals for a median difference.
- Scenario: non-normal data, want CI for median difference between groups
- Show: data loading, BCa bootstrap implementation, distribution plot, CI report

- [ ] **Step 3: Commit**

```bash
git add simulation-runner/examples/
git commit -m "feat: add simulation-runner examples (Monte Carlo power, bootstrap CI)"
```

---

## Chunk 5: lab-notebook Skill

14 files total.

### Task 5.1: Create lab-notebook/SKILL.md

**Files:**
- Create: `lab-notebook/SKILL.md`

- [ ] **Step 1: Write lab-notebook/SKILL.md**

Same structure. Include:
- Frontmatter with trigger keywords from spec Section 5.2b
- Quick Start
- Trigger Conditions with "never the entry point" rule
- Mode Selection Guide (6 modes)
- Agent Team table (4 agents)
- Notebook Structure (10 sections table from spec Section 5.4)
- Entry Format (from spec Section 5.5)
- Key deliverables
- Integration points
- No additional venv packages (stdlib hashlib only)

- [ ] **Step 2: Commit**

```bash
git add lab-notebook/SKILL.md
git commit -m "feat: add lab-notebook SKILL.md (6 modes, 4 agents)"
```

### Task 5.2: Create lab-notebook references (4 files)

**Files:**
- Create: `lab-notebook/references/lab_notebook_best_practices.md`
- Create: `lab-notebook/references/reproducibility_standards.md`
- Create: `lab-notebook/references/deviation_handling_guide.md`
- Create: `lab-notebook/references/provenance_tracking_guide.md`

- [ ] **Step 1: Write lab_notebook_best_practices.md**

What makes a good research record. Include: legal requirements (IP protection, regulatory compliance), academic standards, what to record (date, methods, observations, deviations, decisions, interpretations), contemporaneous recording principle, permanence (append-only), witness/verification.

- [ ] **Step 2: Write reproducibility_standards.md**

FAIR principles (Findable, Accessible, Interoperable, Reusable), TOP guidelines, computational reproducibility checklist (code, data, environment, documentation), file naming conventions, version control for research artifacts.

- [ ] **Step 3: Write deviation_handling_guide.md**

Protocol deviation handling. Include: types (minor, major, critical), documentation requirements, impact assessment framework (effect on internal validity, external validity, statistical validity), when a deviation invalidates results, corrective actions, reporting in Methods section.

- [ ] **Step 4: Write provenance_tracking_guide.md**

File provenance tracking. Include: SHA-256 hashing (Python hashlib), version tracking (file naming + content hash), upstream dependency chains, Material Passport integration, staleness detection.

- [ ] **Step 5: Commit**

```bash
git add lab-notebook/references/
git commit -m "feat: add lab-notebook references (best practices, reproducibility, deviations, provenance)"
```

### Task 5.3: Create lab-notebook templates (4 files)

**Files:**
- Create: `lab-notebook/templates/notebook_template.md`
- Create: `lab-notebook/templates/entry_template.md`
- Create: `lab-notebook/templates/audit_checklist_template.md`
- Create: `lab-notebook/templates/file_manifest_template.md`

- [ ] **Step 1: Write all 4 templates**

**notebook_template.md**: Master notebook with all 10 sections as empty scaffolding (Header, Design Record, Environment Record, Data Collection Log, Data Preparation Log, Analysis Log, Simulation Log, Deviation Log, Decision Log, File Manifest, Audit Trail).

**entry_template.md**: Per-type entry templates for each of the 8 entry types (design, collection, preparation, analysis, simulation, deviation, decision, note). Each with the standard `### Entry [NB-XXX]` format and type-specific required fields.

**audit_checklist_template.md**: Completeness checklist — checkboxes for each notebook section, cross-referencing (all Schema 10 fields documented? all data files in manifest? all deviations recorded?), completeness score calculation.

**file_manifest_template.md**: Artifact inventory — table with columns: file path, purpose, SHA-256 hash, creation timestamp, producing agent/skill, upstream dependencies.

- [ ] **Step 2: Commit**

```bash
git add lab-notebook/templates/
git commit -m "feat: add lab-notebook templates (notebook, entry, audit, manifest)"
```

### Task 5.4: Create lab-notebook agents (4 files)

**Files:**
- Create: `lab-notebook/agents/notebook_manager_agent.md`
- Create: `lab-notebook/agents/entry_writer_agent.md`
- Create: `lab-notebook/agents/deviation_tracker_agent.md`
- Create: `lab-notebook/agents/provenance_auditor_agent.md`

- [ ] **Step 1: Write notebook_manager_agent.md**

Role: Create and manage notebook files.
- Create new notebook from notebook_template.md at `experiment_outputs/logs/notebook_YYYY-MM-DD_<name>.md`
- Mode routing logic
- Validate notebook exists (for log-entry, deviation, snapshot, export, audit modes)
- Assign entry IDs (NB-001, NB-002, ...) using sequential counter
- Timestamp management (ISO 8601)
- Notebook status tracking (active, completed, archived)

- [ ] **Step 2: Write entry_writer_agent.md**

Role: Write structured log entries.
- Parse input: Schema 10 (design record), Schema 11 (analysis/simulation results), or free text
- Structure into standard entry format (spec Section 5.5)
- Auto-detect entry type from input source
- Cross-reference related entries (e.g., analysis entry references design entry)
- Cross-reference files (link to scripts, data files, figures)
- Append to correct notebook section based on entry type

- [ ] **Step 3: Write deviation_tracker_agent.md**

Role: Record protocol deviations.
- Require: what changed, why, when discovered
- Cross-reference original protocol (Schema 10) — show what was planned vs what happened
- Impact assessment: effect on internal validity, external validity, statistical validity
- Severity classification (minor/major/critical)
- Determine if analysis plan needs updating
- Must reference `references/deviation_handling_guide.md`

- [ ] **Step 4: Write provenance_auditor_agent.md**

Role: Audit notebook completeness and produce Schema 12.
- Check all 10 notebook sections for content
- Verify all data files have provenance (hash, source, creation date)
- Verify all Schema 10 fields are documented in Design Record
- Verify all deviations are recorded (cross-reference protocol timeline)
- Compute completeness score (0.0-1.0: number of filled sections / total sections, weighted by importance)
- Generate file manifest (compute SHA-256 hashes for all files in experiment_outputs/)
- Produce Schema 12 handoff artifact
- Generate methods_summary field (condensed narrative for paper Methods section)
- Must reference `references/provenance_tracking_guide.md`

- [ ] **Step 5: Commit**

```bash
git add lab-notebook/agents/
git commit -m "feat: add lab-notebook agents (manager, entry writer, deviation tracker, auditor)"
```

### Task 5.5: Create lab-notebook examples (1 file)

**Files:**
- Create: `lab-notebook/examples/full_notebook_example.md`

- [ ] **Step 1: Write full_notebook_example.md**

Complete notebook walkthrough from design through analysis.
- Show a notebook populated across multiple sessions: design record (from Schema 10), environment record, 3 data collection entries, 1 cleaning entry (from data-analyst), 1 analysis entry (from data-analyst Schema 11), 1 deviation entry (sample fell below target N), 2 decision entries, file manifest, audit report with completeness score
- Final Schema 12 artifact

- [ ] **Step 2: Commit**

```bash
git add lab-notebook/examples/
git commit -m "feat: add lab-notebook example (full notebook lifecycle)"
```

---

## Chunk 6: Pipeline Integration + Existing File Updates

7 modified files. This chunk integrates the 4 new skills into the existing pipeline.

### Task 6.1: Update .claude/CLAUDE.md

**Files:**
- Modify: `.claude/CLAUDE.md`

- [ ] **Step 1: Read current .claude/CLAUDE.md**

Read in full to understand current structure.

- [ ] **Step 2: Update Skills Overview table**

Add the 4 new skills to the table. Update existing skill versions (deep-research v2.4, academic-paper v2.5, academic-pipeline v2.7).

- [ ] **Step 3: Add Routing Rules 6-8**

Add experiment-designer vs data-analyst, data-analyst vs simulation-runner, and lab-notebook rules from spec Section 6.5.

- [ ] **Step 4: Update Full Academic Pipeline diagram**

Insert the experiment stage between deep-research and academic-paper:
```
deep-research -> [experiment-designer -> data-analyst/simulation-runner -> lab-notebook] -> academic-paper -> ...
```

- [ ] **Step 5: Add Handoff Protocol section for experiment skills**

Document: experiment-designer -> data-analyst (Schema 10), data-analyst -> academic-paper (Schema 11), lab-notebook -> academic-paper (Schema 12), experiment-designer -> simulation-runner (Schema 13).

- [ ] **Step 6: Commit**

```bash
git add .claude/CLAUDE.md
git commit -m "docs: update CLAUDE.md with experiment skills routing, overview, pipeline"
```

### Task 6.2: Update academic-pipeline/SKILL.md

**Files:**
- Modify: `academic-pipeline/SKILL.md`

- [ ] **Step 1: Read current academic-pipeline/SKILL.md in full**

- [ ] **Step 2: Bump version to v2.7 in frontmatter**

- [ ] **Step 3: Add Stage 1.5 (EXPERIMENT) to Pipeline Stages table**

Insert between Stage 1 (RESEARCH) and Stage 2 (WRITE). Three sub-stages: 1.5a DESIGN, 1.5b EXECUTE, 1.5c LOG.

- [ ] **Step 4: Add detection logic**

Add the detection logic from spec Section 6.4 — based on Methodology Blueprint fields.

- [ ] **Step 5: Update Stage 2.5 (INTEGRITY) description**

Add Phase F: Experiment Reproducibility Verification with the 5 concrete steps from spec Section 6.1.

- [ ] **Step 6: Commit**

```bash
git add academic-pipeline/SKILL.md
git commit -m "feat: add experiment stages to academic-pipeline v2.7"
```

### Task 6.3: Update academic-pipeline agents

**Files:**
- Modify: `academic-pipeline/agents/pipeline_orchestrator_agent.md`
- Modify: `academic-pipeline/agents/integrity_verification_agent.md`

- [ ] **Step 1: Read both agent files**

- [ ] **Step 2: Update pipeline_orchestrator_agent.md**

Add: experiment stage detection logic (Methodology Blueprint fields -> skill routing), notebook_path management (create notebook at Stage 1.5 start, pass to all experiment skills), user checkpoint after Stage 1.5 completion.

- [ ] **Step 3: Update integrity_verification_agent.md**

Add Phase F: Experiment Reproducibility Verification — locate reproducibility script, re-execute in experiment_env, diff output against Schema 11 results, verify figure hashes, SERIOUS issue on mismatch.

- [ ] **Step 4: Commit**

```bash
git add academic-pipeline/agents/
git commit -m "feat: update pipeline orchestrator and integrity agents for experiment stages"
```

### Task 6.4: Update deep-research/SKILL.md

**Files:**
- Modify: `deep-research/SKILL.md`

- [ ] **Step 1: Read current deep-research/SKILL.md**

- [ ] **Step 2: Bump version to v2.4 in frontmatter**

- [ ] **Step 3: Add methodology_subtype to RQ Brief output documentation**

In the section where RQ Brief output format is described, add the new `methodology_subtype` field with its enum values. Also add the three boolean routing fields (`requires_experiment_design`, `requires_data_collection`, `requires_simulation`) to the Methodology Blueprint output format.

- [ ] **Step 4: Commit**

```bash
git add deep-research/SKILL.md
git commit -m "feat: add methodology_subtype and routing fields to deep-research v2.4"
```

### Task 6.5: Update academic-paper/SKILL.md

**Files:**
- Modify: `academic-paper/SKILL.md`

- [ ] **Step 1: Read current academic-paper/SKILL.md**

- [ ] **Step 2: Bump version to v2.5 in frontmatter**

- [ ] **Step 3: Document Schema 11/12 consumption**

Add to the intake/draft phases: when Schema 11 (Experiment Results) is available, the draft_writer_agent integrates APA results text, tables, and figure references into the Results section. When Schema 12 (Lab Record) is available, the methods_summary is used to enhance the Methods section with experiment provenance details.

- [ ] **Step 4: Add fallback behavior**

When Schema 11/12 are absent (non-experimental papers), behavior is unchanged from v2.4.

- [ ] **Step 5: Commit**

```bash
git add academic-paper/SKILL.md
git commit -m "feat: add Schema 11/12 consumption to academic-paper v2.5"
```

### Task 6.6: Final validation

- [ ] **Step 1: Verify all files exist**

Run: `find experiment-designer data-analyst simulation-runner lab-notebook -name "*.md" | wc -l`
Expected: 69 files (71 new minus 2 shared files which are already counted)

- [ ] **Step 2: Verify handoff schema cross-references**

Check that every Schema 10/11/12/13 producer mentioned in agent files matches the schema definition in shared/handoff_schemas.md.

- [ ] **Step 3: Verify no broken references**

Check that every `references/*.md` and `templates/*.md` file referenced in agent files actually exists.

- [ ] **Step 4: Final commit with version tag**

```bash
git add -A
git commit -m "feat: complete experimentation skills suite v1.0

Added 4 new skills: experiment-designer, data-analyst, simulation-runner, lab-notebook
Updated: deep-research v2.4, academic-paper v2.5, academic-pipeline v2.7
New handoff schemas: 10 (Experiment Design), 11 (Results), 12 (Lab Record), 13 (Simulation Spec)
Shared experiment infrastructure: venv, APA formatting, plot standards, auto-logging, failure paths"
```
