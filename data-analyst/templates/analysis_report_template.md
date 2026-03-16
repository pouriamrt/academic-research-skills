# Analysis Report Template

## Purpose

Standard template for the full analysis report produced by `report_compiler_agent`. All sections map directly to Schema 11 fields. This template is used in `full`, `guided`, and `replication` modes.

---

## Instructions

1. Complete every section; mark sections not applicable as "N/A — [reason]"
2. All statistical results use APA 7 formatting (see `shared/experiment_infrastructure.md` Section 2)
3. Tables and figures are numbered sequentially (Table 1, 2, ...; Figure 1, 2, ...)
4. File paths are relative to the project root
5. The Schema 11 Handoff section at the end is the machine-readable artifact for downstream skills

---

## Report Structure

```markdown
# Statistical Analysis Report

**Experiment ID**: [EXP-YYYYMMDD-NNN or session ID]
**Date**: [YYYY-MM-DD]
**Analyst**: data-analyst v1.0 (Claude Code skill)
**Data Source**: [file path]

---

## 1. Dataset Summary

**File**: [filename]
**Original N**: [rows]
**Variables**: [count]
**Format**: [CSV / Excel / SPSS / Stata]

### Variable Overview

| Variable | Type | Role | Missing | Missing % |
|----------|------|------|---------|-----------|
| [name] | [continuous/categorical/ordinal/binary] | [IV/DV/covariate/demographic] | [n] | [pct]% |

### Key Distributions

[Reference to distribution figures if generated in exploratory phase]

---

## 2. Data Preparation

**Cleaning Log**: `experiment_outputs/logs/data_cleaning_log.md`
**Cleaned Data**: `experiment_outputs/tables/cleaned_data.csv`

### Missing Data

| Variable | Missing N | Missing % | Mechanism | Strategy |
|----------|-----------|-----------|-----------|----------|
| [name] | [n] | [pct]% | [MCAR/MAR/MNAR] | [listwise/MI/FIML] |

**Little's MCAR Test**: chi-sq([df]) = [X.XX], p = [.XXX]
**Overall Strategy**: [describe]

### Outliers

**Detection Method**: [IQR / Z-score / Mahalanobis]
**Outliers Detected**: [n] across [k] variables
**Action**: [flagged / removed / winsorized]
**Impact**: [describe effect on N]

### Transformations

| Variable | Original Distribution | Transformation | Post-Transformation |
|----------|----------------------|----------------|---------------------|
| [name] | Skew = [X.XX] | [log / sqrt / none] | Skew = [X.XX] |

### Final Sample

**Analyzed N**: [n] ([n_excluded] excluded, [pct]%)
**Exclusion Reasons**: [list with counts]

---

## 3. Assumption Checks

**Full Assumption Report**: `experiment_outputs/reports/assumption_report.md`

### Summary

| Assumption | Test | Statistic | p | Diagnostic Plot | Verdict | Action |
|------------|------|-----------|---|----------------|---------|--------|
| [assumption] | [test] | [stat] | [p] | [figure ref] | [met/violated/marginal] | [action] |

### Overall Verdict

[Parametric / Non-parametric / Mixed — with justification]

---

## 4. Primary Results

### Analysis 1: [Hypothesis H1]

**Hypothesis**: [H1 statement]
**Test**: [test name]

[APA results text block — ready for manuscript insertion]

**Table [N]**: [descriptive statistics or results table]

[Inline APA table or reference to experiment_outputs/tables/]

**Figure [N]**: [figure reference]

![Figure N](experiment_outputs/figures/figure_NN_description.png)

*Figure N. [APA caption]*

### Analysis 2: [Hypothesis H2]

[Same format as Analysis 1]

---

## 5. Secondary Results

### Analysis [N]: [Description]

[APA results text block]

[Tables and figures as needed]

---

## 6. Exploratory Results

> **Note**: The following analyses were not pre-specified and should be interpreted as hypothesis-generating, not hypothesis-confirming.

### Exploratory Analysis 1: [Description]

[APA results text block]

---

## 7. Effect Size Summary

| Analysis | Hypothesis | Measure | Value | 95% CI | Magnitude | Interpretation |
|----------|-----------|---------|-------|--------|-----------|----------------|
| [test] | [H1] | [Cohen's d / eta-sq / etc.] | [X.XX] | [[X.XX, X.XX]] | [small/medium/large] | [plain language] |

### Practical Significance Notes

[Domain-specific interpretation]
[Statistical vs practical significance discrepancies]

---

## 8. Limitations

### Statistical Limitations

- [Assumption violations and their potential impact]
- [Missing data and chosen strategy limitations]
- [Sample size considerations]
- [Multiple comparison concerns]

### Methodological Limitations

- [Design limitations relevant to interpreting results]
- [Generalizability constraints]

---

## 9. Reproducibility

**Script**: `experiment_outputs/scripts/analysis.py`
**Random Seed**: [value]
**Python Environment**: `experiment_env/requirements.txt`

To reproduce these results:
1. Activate the virtual environment: `source experiment_env/bin/activate`
2. Run the script: `python experiment_outputs/scripts/analysis.py`
3. All output files will be regenerated in `experiment_outputs/`

---

## 10. Material Passport

| Item | Value |
|------|-------|
| **Experiment ID** | [ID] |
| **Data Source** | [path] |
| **Cleaned Data** | experiment_outputs/tables/cleaned_data.csv |
| **Cleaning Log** | experiment_outputs/logs/data_cleaning_log.md |
| **Analysis Script** | experiment_outputs/scripts/analysis.py |
| **Random Seed** | [seed] |
| **Python Environment** | experiment_env/requirements.txt |
| **Analysis Date** | [YYYY-MM-DD HH:MM] |
| **Analyst Tool** | data-analyst v1.0 |
| **Upstream Schema** | [Schema 10 ID or "User-provided"] |

---

## AI Disclosure

This analysis was conducted with the assistance of data-analyst v1.0, a Claude Code skill for statistical analysis. All statistical tests were executed in Python within a controlled virtual environment. Results were reviewed for accuracy and APA compliance. The reproducibility script allows independent verification of all reported results.

---

## Schema 11 Handoff Artifact

[Structured Schema 11 output per shared/handoff_schemas.md]
```

---

## Section Mapping to Schema 11

| Report Section | Schema 11 Field |
|---------------|-----------------|
| 1. Dataset Summary | `dataset_info` |
| 3. Assumption Checks | `assumption_checks` |
| 4. Primary Results | `primary_results` + `apa_results_text.primary` |
| 5. Secondary Results | `secondary_results` + `apa_results_text.secondary` |
| 6. Exploratory Results | `apa_results_text.exploratory` |
| 7. Effect Size Summary | `effect_sizes` |
| Tables (all sections) | `tables` |
| Figures (all sections) | `figures` |
| 9. Reproducibility | `reproducibility` |

---

## Mode Variants

| Mode | Sections Included |
|------|------------------|
| `full` | All sections (1-10) |
| `guided` | All sections (1-10), with test selection rationale in Section 4 |
| `quick` | Sections 1, 2 (abbreviated), 4 (primary only), 7, 9 |
| `assumption-check` | Sections 1, 2, 3 only |
| `exploratory` | Sections 1, 2, 6, 7 (no primary/secondary distinction) |
| `replication` | All sections (1-10), plus Section 4 includes comparison to original results |
