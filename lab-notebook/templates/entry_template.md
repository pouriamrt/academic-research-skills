# Entry Templates — Per-Type Entry Templates for All 8 Entry Types

## Purpose

This file provides the canonical entry template for each of the 8 entry types used in the lab notebook. The entry_writer_agent uses these templates when composing new entries. Every entry must include the standard header (Entry ID, timestamp, Type, Author, Related Entries, Related Files) plus the type-specific required fields documented below.

---

## Standard Entry Header

Every entry, regardless of type, begins with this header:

```markdown
### Entry [NB-XXX] -- YYYY-MM-DD HH:MM

- **Type**: [design | collection | preparation | analysis | simulation | deviation | decision | note]
- **Author**: [person or agent that produced this entry]
- **Related Entries**: [NB-YYY, NB-ZZZ] or "None"
- **Related Files**: [file paths] or "None"
```

**Rules**:
- `[NB-XXX]`: Sequential ID assigned by notebook_manager_agent (e.g., NB-001, NB-042)
- `YYYY-MM-DD HH:MM`: ISO 8601 timestamp of entry creation, in the notebook's declared timezone
- All four metadata fields are required; use "None" rather than omitting a field

---

## Type 1: `design`

**Target Section**: Design Record
**Source**: Schema 10 (Experiment Design), protocol document, or user specification

```markdown
### Entry [NB-XXX] -- YYYY-MM-DD HH:MM

- **Type**: design
- **Author**: [researcher name or experiment-designer skill]
- **Related Entries**: None
- **Related Files**: [path to protocol document or Schema 10 file]

**Design Type**: [RCT / quasi_experimental / factorial / crossover / single_subject / correlational / simulation / mixed]

**Hypotheses**:
- H1 (primary, [positive/negative/non-directional]): [hypothesis statement]
- H2 (secondary, [direction]): [hypothesis statement]
- H3 ([primary/secondary], [direction]): [hypothesis statement]

**Variables**:
| Role | Name | Type | Operationalization | Levels (if categorical) |
|------|------|------|--------------------|------------------------|
| Independent | [name] | [continuous/categorical/ordinal/binary] | [how measured/manipulated] | [levels or N/A] |
| Dependent | [name] | [type] | [how measured] | [levels or N/A] |
| Control | [name] | [type] | [how measured] | [levels or N/A] |
| Moderator | [name] | [type] | [how measured] | [levels or N/A] |
| Mediator | [name] | [type] | [how measured] | [levels or N/A] |

**Sample Plan**:
- Target N: [number]
- Power: [0.XX]
- Alpha: [0.XX]
- Effect size: [measure = value]
- Attrition buffer: [percentage]
- Sampling strategy: [random / convenience / stratified / cluster]

**Analysis Plan**:
- Primary: [statistical test] for [hypothesis ID] — [IV] -> [DV]
- Secondary: [statistical test] for [hypothesis ID]
- Exploratory: [planned exploratory analyses]

**Validity Threats**:
| Threat | Type | Likelihood | Mitigation | Residual Risk |
|--------|------|-----------|------------|---------------|
| [threat name] | [internal/external/construct/statistical] | [high/medium/low] | [strategy] | [remaining risk] |

**Timeline**:
| Milestone | Planned Date |
|-----------|-------------|
| Data collection start | [date] |
| Data collection end | [date] |
| Analysis start | [date] |
| Report deadline | [date] |

**Pre-registration**: [Yes/No] — [Platform: OSF / PROSPERO / AsPredicted / N/A] — [Status: planned/completed/N/A]
```

---

## Type 2: `collection`

**Target Section**: Data Collection Log
**Source**: Researcher report or data collection system log

```markdown
### Entry [NB-XXX] -- YYYY-MM-DD HH:MM

- **Type**: collection
- **Author**: [researcher name]
- **Related Entries**: [NB-001 (design)]
- **Related Files**: [path to raw data file]

**Instrument**: [survey name / interview protocol / observation rubric / sensor system]
**Participants**: [description: group, section, site, demographic summary]
**Count**: N=[total collected], valid=[usable responses], response_rate=[percentage]
**Conditions**: [environmental or procedural factors of note]
**Duration**: [start time] to [end time]
**Data Storage**: [where raw data is stored, format]
**Notes**: [observations, incidents, or anomalies during collection]
```

---

## Type 3: `preparation`

**Target Section**: Data Preparation Log
**Source**: Analyst report or data-analyst skill output

```markdown
### Entry [NB-XXX] -- YYYY-MM-DD HH:MM

- **Type**: preparation
- **Author**: [analyst name or data-analyst skill]
- **Related Entries**: [NB-YYY (collection entry providing the input data)]
- **Related Files**: [input data file], [output data file], [cleaning script]

**Input**: [source file path] (N=[count before preparation])

**Transformations**:
1. [Step 1: e.g., "Removed 3 duplicate records based on participant ID"]
2. [Step 2: e.g., "Reverse-scored items Q5, Q12, Q18"]
3. [Step 3: e.g., "Computed composite score: mean of Q1-Q10"]
4. [Step N: ...]

**Exclusions**:
- [N] participants excluded for [reason 1]
- [N] participants excluded for [reason 2]
- Total excluded: [N]

**Missing Data Strategy**: [listwise deletion / pairwise deletion / multiple imputation / mean substitution / N/A]
- Missing data rate: [percentage]
- MCAR test: [result if performed]

**Output**: [output file path] (N=[count after preparation])

**Validation Checks**:
- [ ] No duplicate IDs in output
- [ ] All variables within expected ranges
- [ ] Composite scores computed correctly (spot-checked)
```

---

## Type 4: `analysis`

**Target Section**: Analysis Log
**Source**: Schema 11 (Experiment Results), analyst report, or data-analyst skill output

```markdown
### Entry [NB-XXX] -- YYYY-MM-DD HH:MM

- **Type**: analysis
- **Author**: [analyst name or data-analyst skill]
- **Related Entries**: [NB-YYY (preparation entry), NB-001 (design)]
- **Related Files**: [analysis script], [output tables], [output figures]

**Hypothesis Tested**: [H1 / H2 / exploratory]

**Statistical Test**: [test name, e.g., independent samples t-test, one-way ANOVA, linear regression]

**Assumption Checks**:
| Assumption | Test Used | Statistic | p-value | Verdict | Action Taken |
|------------|----------|-----------|---------|---------|-------------|
| Normality | Shapiro-Wilk | W = [value] | [p] | [met/violated/marginal] | [proceed/switch to non-parametric] |
| Homogeneity of variance | Levene's | F = [value] | [p] | [met/violated/marginal] | [proceed/use Welch's] |
| [other assumptions] | [test] | [stat] | [p] | [verdict] | [action] |

**Result**:
- Test statistic: [e.g., t(178) = 3.42]
- p-value: [e.g., p < .001]
- Significant: [yes/no] (at alpha = [alpha level])

**Effect Size**:
- Measure: [Cohen's d / eta-squared / R-squared / odds ratio]
- Value: [number]
- 95% CI: [[lower], [upper]]
- Magnitude: [negligible / small / medium / large]

**APA Result String**: [Full APA-formatted result, e.g., "t(178) = 3.42, p < .001, d = 0.51, 95% CI [0.21, 0.81]"]

**Interpretation**: [What this result means for the hypothesis. State whether the hypothesis is supported, partially supported, or not supported. Note any caveats.]

**Diagnostic Plots**: [paths to Q-Q plots, residual plots, etc., if generated]
```

---

## Type 5: `simulation`

**Target Section**: Simulation Log
**Source**: Schema 11 (if result_type = simulation), simulation-runner skill output, or manual run

```markdown
### Entry [NB-XXX] -- YYYY-MM-DD HH:MM

- **Type**: simulation
- **Author**: [analyst name or simulation-runner skill]
- **Related Entries**: [NB-001 (design)]
- **Related Files**: [simulation script], [results data file], [convergence plots]

**Simulation Type**: [monte_carlo / bootstrap / power_sim / agent_based / parameter_sweep / stochastic_process]
**Purpose**: [Brief description of what this simulation investigates]

**Model Definition**:
- Description: [what is being simulated]
- DGP: [data-generating process formula or description]
- Key parameters: [list with values]
- Distributions: [distributional assumptions]

**Execution Configuration**:
- Iterations: [N]
- Burn-in: [N or 0]
- Random seed(s): [seed values]
- Convergence criterion: [e.g., MCSE < 0.01]

**Convergence Status**: [converged / not converged / partial]
- MCSE: [value if applicable]
- Effective sample size: [if applicable]

**Results**:
| Measure | Estimate | SE/CI | Interpretation |
|---------|----------|-------|---------------|
| [e.g., Power] | [value] | [95% CI] | [interpretation] |
| [e.g., Type I error] | [value] | [95% CI] | [interpretation] |
| [e.g., Bias] | [value] | [SE] | [interpretation] |

**Runtime**: [wall clock time, e.g., "12 min 34 sec"]

**Interpretation**: [What the simulation results indicate. Implications for the experiment design or analysis plan.]
```

---

## Type 6: `deviation`

**Target Section**: Deviation Log
**Source**: Researcher report, data quality check, or process monitoring

> **Note**: Deviation entries are typically written by the `deviation_tracker_agent`, not the `entry_writer_agent`. This template is included for reference and completeness. If the entry_writer_agent detects deviation-like content, it should route to the deviation_tracker_agent.

```markdown
### Entry [NB-XXX] -- YYYY-MM-DD HH:MM

- **Type**: deviation
- **Author**: [person who discovered/reported the deviation]
- **Related Entries**: [NB-001 (design), other affected entries]
- **Related Files**: [protocol document, affected data files]

**Deviation ID**: DEV-NNN
**Severity**: [minor / major / critical]
**Discovery Date**: YYYY-MM-DD
**Discovery Context**: [how the deviation was discovered]

**What Changed**: [Clear, specific description of the deviation]

**Original Plan** (from protocol):
> [Quote or summarize the relevant section of the protocol / Schema 10]

**Actual**:
> [What actually happened]

**Reason**: [Why the deviation occurred]

**Impact Assessment**:
| Validity Type | Impact | Explanation |
|---------------|--------|-------------|
| Internal validity | [none / minor / moderate / severe] | [explanation] |
| External validity | [none / minor / moderate / severe] | [explanation] |
| Statistical validity | [none / minor / moderate / severe] | [explanation] |

**Analysis Plan Update Required**: [yes / no]
**If yes, proposed changes**: [specific changes needed]

**Corrective Action Taken**: [what was done]
**Residual Risk**: [what risk remains]
```

---

## Type 7: `decision`

**Target Section**: Decision Log
**Source**: Researcher deliberation, team meeting, or response to deviation

```markdown
### Entry [NB-XXX] -- YYYY-MM-DD HH:MM

- **Type**: decision
- **Author**: [researcher name or team]
- **Related Entries**: [entries that prompted this decision, e.g., NB-YYY (deviation)]
- **Related Files**: [supporting documents, references consulted]

**Decision**: [Clear, concise statement of what was decided]

**Context**: [What situation or problem prompted this decision]

**Alternatives Considered**:
1. **[Alternative A]**: [description] — Rejected because: [reason]
2. **[Alternative B]**: [description] — Rejected because: [reason]
3. **[Alternative C]**: [description] — Rejected because: [reason]

**Rationale**: [Detailed justification for the chosen option. Reference evidence, methodological principles, or practical constraints.]

**Impact**:
- Affects: [which downstream steps, analyses, or timeline items are affected]
- Requires: [any follow-up actions needed]
- Pre-registration update needed: [yes / no]
```

---

## Type 8: `note`

**Target Section**: Most relevant section based on content (see entry_writer_agent placement rules)
**Source**: Researcher observation, annotation, or free-form input

```markdown
### Entry [NB-XXX] -- YYYY-MM-DD HH:MM

- **Type**: note
- **Author**: [researcher name]
- **Related Entries**: [if any relevant entries exist]
- **Related Files**: [if any relevant files exist]

[Free-form content. Notes may include:
- Observations during data collection
- Ideas for future analysis
- Questions to discuss with the team
- References to external events that may affect the experiment
- Preliminary interpretations or hunches (clearly labeled as such)
- Administrative updates (e.g., IRB renewal, equipment maintenance)]
```

---

## Usage Notes

1. **Choosing the right type**: When in doubt, prefer a more specific type over `note`. A `note` should be used only when no other type fits.
2. **Multiple types in one event**: If a single event involves both data collection and a deviation, create two separate entries (one `collection`, one `deviation`) and cross-reference them.
3. **Schema 11 mapping**: When writing from Schema 11 input, always include the `experiment_id` link and reference the Schema 11 `result_type` to determine whether to create an `analysis` or `simulation` entry.
4. **Append-only**: Once written, entries are never modified. To correct an error in a previous entry, create a new `note` entry that references the original and states the correction.
