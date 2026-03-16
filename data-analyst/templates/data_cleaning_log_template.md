# Data Cleaning Log Template

## Purpose

Template for documenting every data cleaning decision made by `data_preparation_agent`. This log provides full provenance from original dataset to analysis-ready dataset. Every exclusion, imputation, and transformation is recorded with justification.

---

## Instructions

1. Complete every section — if a step was not needed, write "Not applicable" with brief justification
2. The original dataset must never be modified; all cleaning operates on a copy
3. Each cleaning step includes: what was done, why, how many cases affected, and the code used
4. The exclusion flowchart at the end summarizes the complete data flow from original N to final N
5. Save this log to `experiment_outputs/logs/data_cleaning_log.md`

---

## Log Structure

```markdown
# Data Cleaning Log

**Date**: [YYYY-MM-DD HH:MM]
**Original File**: [filename and path]
**Cleaned File**: experiment_outputs/tables/cleaned_data.csv
**Analyst**: data-analyst v1.0

---

## 1. Original Dataset Summary

| Property | Value |
|----------|-------|
| File name | [filename] |
| File format | [CSV / Excel / SPSS / Stata] |
| Rows (observations) | [N] |
| Columns (variables) | [K] |
| File size | [MB] |
| Date loaded | [YYYY-MM-DD HH:MM] |

### Variable List

| # | Variable | Type | Description | Missing N | Missing % |
|---|----------|------|-------------|-----------|-----------|
| 1 | [name] | [numeric/categorical/ordinal] | [description or SPSS/Stata label] | [n] | [pct]% |
| 2 | [name] | [type] | [description] | [n] | [pct]% |

### Initial Data Quality Flags

- [ ] Duplicate rows detected: [N duplicates]
- [ ] Constant columns: [list]
- [ ] Highly skewed variables (|skew| > 2): [list]
- [ ] Possible ID columns (all unique values): [list]
- [ ] Unexpected data types: [list, e.g., numeric column stored as string]

---

## 2. Missing Data Assessment

### 2.1 Missing Data Pattern

| Variable | Missing N | Missing % | Pattern |
|----------|-----------|-----------|---------|
| [name] | [n] | [pct]% | [scattered / block / monotone] |

**Total cells missing**: [n] / [total cells] = [pct]%

### 2.2 Mechanism Diagnosis

**Test**: Little's MCAR test
**Result**: chi-sq([df]) = [X.XX], p = [.XXX]
**Conclusion**: [MCAR / Not MCAR (likely MAR or MNAR)]

**Additional diagnostics**:
- [Logistic regression predicting missingness from observed variables: results]
- [Visual inspection of missing data pattern: observations]
- [Domain knowledge considerations for MNAR assessment]

### 2.3 Missing Data Strategy

**Strategy chosen**: [Listwise deletion / Multiple imputation / FIML / Other]
**Justification**: [Why this strategy was chosen given the mechanism and missing percentage]

**Details**:
- [If listwise: N excluded, % of data lost]
- [If MI: number of imputations (m), imputation model details, convergence status]
- [If FIML: built into downstream SEM model]

**Code used**:
```python
# [Actual Python code executed for missing data handling]
```

**Cases affected**: [N cases imputed or excluded]

---

## 3. Outlier Assessment

### 3.1 Detection Method

**Method**: [IQR / Z-score / Mahalanobis distance]
**Threshold**: [1.5 * IQR / |z| > 3.0 / Mahalanobis p < .001]

### 3.2 Outliers Detected

| Variable | N Outliers | % | Direction | Values |
|----------|-----------|---|-----------|--------|
| [name] | [n] | [pct]% | [high/low/both] | [list of extreme values] |

**Multivariate outliers** (if Mahalanobis used): [N cases with p < .001]

### 3.3 Outlier Handling

**Action**: [Flagged only / Removed / Winsorized / Kept with note]
**Justification**: [Why this action — domain knowledge, impact on results]

**Sensitivity check**: [Were analyses run with and without outliers? Results comparison]

**Code used**:
```python
# [Actual Python code for outlier detection and handling]
```

**Cases affected**: [N cases]

---

## 4. Variable Recoding

### 4.1 Recoding Operations

| Variable | Operation | Details | Justification |
|----------|-----------|---------|---------------|
| [name] | Reverse score | Items [list], max = [value] | [Standard for this scale] |
| [name] | Dummy coding | Reference = [level], created [k-1] dummies | [Required for regression] |
| [name] | Composite score | Mean of items [list] | [Scale composite per instrument manual] |
| [name] | Binning | Cut points: [list], labels: [list] | [Clinical thresholds / research design] |

### 4.2 Code Used

```python
# [Actual Python code for all recoding operations]
```

---

## 5. Transformations

### 5.1 Transformation Decisions

| Variable | Original Skew | Transformation | Post-Transform Skew | Shapiro-Wilk Pre | Shapiro-Wilk Post |
|----------|---------------|----------------|---------------------|------------------|-------------------|
| [name] | [value] | [log / sqrt / none] | [value] | W = [v], p = [p] | W = [v], p = [p] |

### 5.2 Transformation Justification

For each transformed variable:
- **Why**: [Skewness > 2, normality assumption required for planned test]
- **Which transformation**: [Log transformation chosen because positive skew, no zero values]
- **Did it help**: [Yes — skewness reduced from X.XX to X.XX, Shapiro-Wilk p improved from .XXX to .XXX]

### 5.3 Code Used

```python
# [Actual Python code for transformations]
```

---

## 6. Additional Cleaning Steps

### 6.1 Duplicate Removal

- **Duplicates found**: [N]
- **Action**: [Removed / Kept (first occurrence) / Not applicable]
- **Criteria**: [Exact match on all columns / Match on key columns only]

### 6.2 Data Type Corrections

| Variable | Original Type | Corrected Type | Reason |
|----------|---------------|----------------|--------|
| [name] | [string] | [numeric] | [Values are numbers stored as text] |
| [name] | [float] | [categorical] | [Group codes 1/2/3, not continuous] |

### 6.3 Value Corrections

| Variable | Original Value | Corrected Value | N Cases | Reason |
|----------|----------------|-----------------|---------|--------|
| [name] | [impossible value, e.g., age = -5] | [NaN] | [n] | [Data entry error] |

---

## 7. Final Dataset Summary

| Property | Original | Final | Change |
|----------|----------|-------|--------|
| Rows | [N_orig] | [N_final] | -[N_excluded] ([pct]%) |
| Columns | [K_orig] | [K_final] | [+/- N_cols] |
| Missing cells | [N_miss_orig] | [N_miss_final] | -[N_resolved] |
| Missing % | [pct_orig]% | [pct_final]% | -[diff]% |

### Final Variable Summary

| Variable | Type | N Valid | Mean/Mode | SD/Freq |
|----------|------|---------|-----------|---------|
| [name] | [type] | [n] | [value] | [value] |

---

## 8. Exclusion Flowchart

```
Original dataset: N = [N_original]
    |
    +-- Duplicate removal: -[n] cases
    |   Remaining: N = [N1]
    |
    +-- Missing data (listwise/exclusion): -[n] cases
    |   Remaining: N = [N2]
    |
    +-- Outlier removal: -[n] cases
    |   Remaining: N = [N3]
    |
    +-- Data entry error exclusion: -[n] cases
    |   Remaining: N = [N4]
    |
    +-- [Other exclusion criteria]: -[n] cases
    |   Remaining: N = [N5]
    |
    Final analysis sample: N = [N_final]
```

---

## 9. Reproducibility

All cleaning steps can be reproduced by running the cleaning code in sequence within the `experiment_env` virtual environment.

**Cleaned dataset saved to**: `experiment_outputs/tables/cleaned_data.csv`
**This log saved to**: `experiment_outputs/logs/data_cleaning_log.md`
**Associated analysis script**: `experiment_outputs/scripts/analysis.py`

---

## 10. Audit Trail

| Step | Timestamp | Action | Cases Before | Cases After | Cases Affected |
|------|-----------|--------|-------------|------------|----------------|
| 1 | [HH:MM] | Load data | — | [N] | — |
| 2 | [HH:MM] | Remove duplicates | [N] | [N1] | [n] |
| 3 | [HH:MM] | Handle missing (listwise) | [N1] | [N2] | [n] |
| 4 | [HH:MM] | Flag outliers | [N2] | [N2] | [n flagged] |
| 5 | [HH:MM] | Apply transformations | [N2] | [N2] | [n vars] |
| 6 | [HH:MM] | Save cleaned data | [N2] | [N2] | — |
```

---

## Checklist

Before marking data preparation as complete:

- [ ] Original dataset file is unchanged
- [ ] Every exclusion has a documented justification
- [ ] Missing data mechanism was diagnosed (not assumed)
- [ ] Outlier detection method matches data distribution
- [ ] All transformations were validated for improvement
- [ ] Cleaned dataset saved to `experiment_outputs/tables/cleaned_data.csv`
- [ ] This log is complete with no blank sections
- [ ] Exclusion flowchart accounts for total difference between original and final N
- [ ] Audit trail timestamps are present
