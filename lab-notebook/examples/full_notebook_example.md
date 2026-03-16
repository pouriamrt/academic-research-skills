# Example: Full Notebook Lifecycle — AI-Assisted Formative Assessment Study

## Overview

This example demonstrates a complete lab notebook lifecycle for a quasi-experimental study examining AI-assisted formative assessment in undergraduate physics. It shows:
- Notebook creation from Schema 10 (Experiment Design)
- Design Record, Environment Record, and initial entries
- 3 data collection entries over 3 weeks
- 1 data preparation entry (from data-analyst)
- 1 analysis entry (from data-analyst Schema 11)
- 1 deviation entry (sample fell below target N)
- 2 decision entries
- File manifest with SHA-256 hashes
- Audit report with completeness score
- Final Schema 12 artifact

---

## Step 1: Notebook Creation (full mode)

**User command**: "Create a lab notebook for experiment EXP-20260316-001"

The notebook_manager_agent instantiates a notebook from the template, and the entry_writer_agent populates it.

---

# Lab Notebook — AI-Assisted Formative Assessment in Undergraduate Physics

## Header

| Field | Value |
|-------|-------|
| **Experiment ID** | EXP-20260316-001 |
| **Title** | Effect of AI-Assisted Formative Assessment on Undergraduate Physics Learning Outcomes |
| **Authors** | Dr. Wei-Lin Chen (PI), Yu-Ting Huang (RA), Mei-Ling Wu (RA) |
| **Created** | 2026-03-16 09:00 |
| **Last Modified** | 2026-05-02 16:30 |
| **Status** | active |
| **Timezone** | UTC+8 (Taipei) |
| **Protocol Reference** | experiment_outputs/protocols/protocol_EXP-20260316-001.md |
| **Design Type** | quasi_experimental |

**Notebook File**: experiment_outputs/logs/notebook_2026-03-16_ai-assessment.md

---

## Design Record

### Entry [NB-001] -- 2026-03-16 09:00

- **Type**: design
- **Author**: experiment-designer/protocol_compiler_agent
- **Related Entries**: None
- **Related Files**: experiment_outputs/protocols/protocol_EXP-20260316-001.md

**Design Type**: quasi_experimental

**Hypotheses**:
- H1 (primary, positive): Students receiving AI-assisted formative assessment will show significantly higher final exam scores than students receiving traditional assessment
- H2 (secondary, positive): Students in the AI-assisted group will report higher self-efficacy on the Physics Self-Efficacy Scale

**Variables**:
| Role | Name | Type | Operationalization | Levels |
|------|------|------|--------------------|--------|
| Independent | Assessment method | categorical | AI-assisted (XLearn platform) vs. traditional (paper-based) | 2 (treatment, control) |
| Dependent | Final exam score | continuous | Departmental final exam (0-100 points) | N/A |
| Dependent | Self-efficacy | continuous | Physics Self-Efficacy Scale (Likert composite, 1-5) | N/A |
| Control | Prior GPA | continuous | Cumulative GPA from university records | N/A |
| Control | Gender | binary | Self-reported | 2 (male, female) |
| Control | Year of study | ordinal | Self-reported | 4 (1st-4th year) |

**Sample Plan**:
- Target N: 195 (accounting for 15% attrition buffer)
- Effective N needed: 166 (83 per group)
- Power: 0.80
- Alpha: 0.05
- Effect size: Cohen's d = 0.50 (medium, based on Wang & Chen, 2023)
- Attrition buffer: 15%
- Sampling: Intact class sections (2 treatment, 2 control)

**Analysis Plan**:
- Primary: Independent samples t-test for H1 (assessment method -> final exam score)
- Primary robustness: ANCOVA controlling for prior GPA (assessment method -> final exam score | GPA)
- Secondary: Independent samples t-test for H2 (assessment method -> self-efficacy)
- Exploratory: Moderation analysis (prior GPA x assessment method on final exam score)

**Validity Threats**:
| Threat | Type | Likelihood | Mitigation | Residual Risk |
|--------|------|-----------|------------|---------------|
| Selection bias | internal | medium | Compare baseline GPA between groups; ANCOVA controls for prior GPA | Groups may differ on unmeasured variables |
| Testing effect | internal | low | Both groups receive same number of assessments; only format differs | Novelty effect of AI platform |
| Maturation | internal | low | Same semester, same duration for both groups | None expected |
| Diffusion of treatment | internal | medium | Sections meet at different times; no shared online platform access | Informal student communication |
| Hawthorne effect | external | medium | Routine classroom integration; no special attention to treatment group | Students aware of study participation |

**Timeline**:
| Milestone | Planned Date |
|-----------|-------------|
| Data collection start (Week 1 surveys + platform setup) | 2026-03-25 |
| Mid-semester check | 2026-04-15 |
| Data collection end (Week 16 final exam + post-survey) | 2026-07-10 |
| Analysis start | 2026-07-15 |
| Report deadline | 2026-08-15 |

**Pre-registration**: Yes — OSF Registries — Status: completed (osf.io/xxxxx)

---

## Environment Record

### Entry [NB-002] -- 2026-03-16 09:15

- **Type**: note
- **Author**: Yu-Ting Huang
- **Related Entries**: NB-001
- **Related Files**: experiment_env/requirements.txt

**Computational Environment**:
- Python: 3.12.3
- OS: Ubuntu 22.04 LTS (analysis server)
- Key packages:
  - pandas 2.2.1
  - scipy 1.13.0
  - statsmodels 0.14.1
  - pingouin 0.5.4
  - matplotlib 3.9.0
  - seaborn 0.13.2

**Random Seeds**: Primary seed: 42 (set in all scripts)

**Data Collection Platform**: XLearn v3.2 (AI-assisted formative assessment platform, hosted on university servers)

**Survey Platform**: Qualtrics (university license)

---

## Data Collection Log

### Entry [NB-003] -- 2026-03-27 16:30

- **Type**: collection
- **Author**: Mei-Ling Wu
- **Related Entries**: NB-001 (design)
- **Related Files**: experiment_outputs/data/raw/survey_week1_section_a.csv, experiment_outputs/data/raw/survey_week1_section_b.csv

**Instrument**: Physics Self-Efficacy Scale (pre-test) + demographic survey
**Participants**: Sections A and B (treatment group)
**Count**: N=96 surveys distributed, valid=93, response_rate=96.9%
**Conditions**: Administered during first 15 minutes of class. Room temperature normal. No disruptions.
**Duration**: 2026-03-27 14:00 to 2026-03-27 16:30 (two back-to-back sections)
**Data Storage**: Qualtrics export -> CSV in experiment_outputs/data/raw/
**Notes**: Three students arrived late and completed the survey after class. One student declined to participate (Section B). Two incomplete responses excluded (< 50% completion).

### Entry [NB-004] -- 2026-04-03 15:45

- **Type**: collection
- **Author**: Yu-Ting Huang
- **Related Entries**: NB-001 (design)
- **Related Files**: experiment_outputs/data/raw/survey_week1_section_c.csv, experiment_outputs/data/raw/survey_week1_section_d.csv

**Instrument**: Physics Self-Efficacy Scale (pre-test) + demographic survey
**Participants**: Sections C and D (control group)
**Count**: N=99 surveys distributed, valid=95, response_rate=96.0%
**Conditions**: Administered during first 15 minutes of class. Room change for Section D (moved to Room 302 due to scheduling conflict; same building, similar environment).
**Duration**: 2026-04-03 10:00 to 2026-04-03 15:45 (morning and afternoon sections)
**Data Storage**: Qualtrics export -> CSV in experiment_outputs/data/raw/
**Notes**: Four incomplete responses excluded. Section D had a fire drill at 15:20 but all participants had completed the survey by then. Minor setting deviation logged separately (see NB-005).

### Entry [NB-005] -- 2026-04-03 16:00

- **Type**: note
- **Author**: Yu-Ting Huang
- **Related Entries**: NB-004 (collection)
- **Related Files**: None

**Note on Section D setting**: Section D was administered in Room 302 instead of the planned Room 205. Room 302 is a comparable lecture hall in the same building (similar seating capacity, lighting, and noise level). The room change was due to a scheduling conflict identified the morning of collection. This is a minor deviation — no impact on survey administration procedures. The fire drill occurred after all surveys were collected.

### Entry [NB-006] -- 2026-06-28 17:00

- **Type**: collection
- **Author**: Mei-Ling Wu
- **Related Entries**: NB-001 (design), NB-003, NB-004
- **Related Files**: experiment_outputs/data/raw/exam_scores_all_sections.csv, experiment_outputs/data/raw/survey_post_all_sections.csv

**Instrument**: Departmental final exam (0-100) + Physics Self-Efficacy Scale (post-test)
**Participants**: All four sections (A, B, C, D)
**Count**: N=180 exam scores collected (treatment: 88, control: 92), post-survey N=175, response_rate=97.2%
**Conditions**: Final exam administered under standard exam conditions (proctored, 2-hour time limit). Post-survey administered online via Qualtrics within 48 hours after exam.
**Duration**: 2026-06-26 (exam) to 2026-06-28 (post-survey deadline)
**Data Storage**: Exam scores from department -> CSV; Post-survey from Qualtrics -> CSV
**Notes**: 15 students who were enrolled at Week 1 did not take the final exam (8 treatment, 7 control). This represents a 7.7% overall attrition rate, within the 15% buffer. See deviation entry NB-008 for sample size analysis.

---

## Data Preparation Log

### Entry [NB-007] -- 2026-07-02 14:00

- **Type**: preparation
- **Author**: data-analyst/cleaning_agent
- **Related Entries**: NB-003, NB-004, NB-006 (collection entries)
- **Related Files**: experiment_outputs/data/raw/survey_week1_section_a.csv, experiment_outputs/data/raw/survey_week1_section_b.csv, experiment_outputs/data/raw/survey_week1_section_c.csv, experiment_outputs/data/raw/survey_week1_section_d.csv, experiment_outputs/data/raw/exam_scores_all_sections.csv, experiment_outputs/data/raw/survey_post_all_sections.csv, experiment_outputs/data/processed/combined_clean.csv, experiment_outputs/scripts/01_clean_data.py

**Input**: 6 raw data files (pre-survey sections A-D, exam scores, post-survey). Total participants: N=195

**Transformations**:
1. Merged 4 pre-survey files by participant ID -> combined pre-survey dataset
2. Joined pre-survey with exam scores and post-survey on participant ID
3. Reverse-scored Self-Efficacy items Q3, Q7, Q11 (per scale manual)
4. Computed Self-Efficacy composite: mean of all 15 items (pre and post separately)
5. Recoded gender (1=male, 2=female) to factor variable
6. Verified prior GPA from university records (merged by student ID)

**Exclusions**:
- 8 participants excluded: enrolled but did not take the final exam (treatment group)
- 7 participants excluded: enrolled but did not take the final exam (control group)
- Total excluded: 15 (attrition)

**Missing Data Strategy**: Listwise deletion for primary analyses. Missing rate: 2.8% on post-survey (5 participants completed exam but not post-survey). Little's MCAR test: chi-squared(12) = 14.3, p = .283 — missing data consistent with MCAR.

**Output**: experiment_outputs/data/processed/combined_clean.csv (N=180: treatment=88, control=92)

**Validation Checks**:
- [x] No duplicate IDs in output
- [x] All exam scores in range 0-100
- [x] All Self-Efficacy composites in range 1.0-5.0
- [x] Prior GPA in range 0.0-4.3
- [x] Composite scores spot-checked against manual calculation (5 random cases)

---

## Analysis Log

### Entry [NB-010] -- 2026-07-15 11:30

- **Type**: analysis
- **Author**: data-analyst/report_compiler_agent
- **Related Entries**: NB-007 (preparation), NB-001 (design)
- **Related Files**: experiment_outputs/scripts/02_primary_analysis.py, experiment_outputs/results/tables/table_1_descriptive_stats.csv, experiment_outputs/results/tables/table_2_primary_results.csv, experiment_outputs/results/figures/figure_1_boxplot_exam.png, experiment_outputs/results/figures/figure_2_qq_plots.png

**Hypothesis Tested**: H1 (primary)

**Statistical Test**: Independent samples t-test (exam scores by assessment method)

**Assumption Checks**:
| Assumption | Test Used | Statistic | p-value | Verdict | Action Taken |
|------------|----------|-----------|---------|---------|-------------|
| Normality (treatment) | Shapiro-Wilk | W = 0.982 | .142 | met | Proceed with parametric test |
| Normality (control) | Shapiro-Wilk | W = 0.976 | .089 | met | Proceed with parametric test |
| Homogeneity of variance | Levene's | F = 1.23 | .269 | met | Proceed with pooled variance |

**Result**:
- Test statistic: t(178) = 3.42
- p-value: p < .001
- Significant: yes (at alpha = 0.05)

**Effect Size**:
- Measure: Cohen's d
- Value: 0.51
- 95% CI: [0.21, 0.81]
- Magnitude: medium

**APA Result String**: "An independent samples t-test revealed that students receiving AI-assisted formative assessment scored significantly higher on the final exam (M = 78.3, SD = 12.1) than students receiving traditional assessment (M = 72.1, SD = 12.8), t(178) = 3.42, p < .001, d = 0.51, 95% CI [0.21, 0.81]."

**ANCOVA Robustness Check** (controlling for prior GPA):
- F(1, 177) = 10.87, p = .001, partial eta-squared = .058
- Prior GPA was a significant covariate: F(1, 177) = 45.23, p < .001
- Adjusted means: treatment = 77.9, control = 72.5
- Conclusion: Result is robust to controlling for prior GPA

**Interpretation**: H1 is supported. Students receiving AI-assisted formative assessment scored significantly higher on the final exam, with a medium effect size. The effect persists after controlling for prior GPA, reducing the concern about selection bias between intact class sections.

**Diagnostic Plots**: experiment_outputs/results/figures/figure_2_qq_plots.png (Q-Q plots show approximate normality for both groups)

---

## Simulation Log

_No simulations were planned for this experiment. This section remains empty. Simulation Log weight (10%) is redistributed to Design Record (+5%) and Analysis Log (+5%) during auditing._

---

## Deviation Log

### Entry [NB-008] -- 2026-06-28 18:00

- **Type**: deviation
- **Author**: Dr. Wei-Lin Chen
- **Related Entries**: NB-001 (design), NB-006 (final collection)
- **Related Files**: experiment_outputs/protocols/protocol_EXP-20260316-001.md

**Deviation ID**: DEV-001
**Severity**: major
**Discovery Date**: 2026-06-28
**Discovery Context**: Discovered when compiling final exam participation records after the exam administration.

**What Changed**: Final sample size (N=180) fell below the pre-registered target (N=195). The effective sample per group is treatment=88, control=92, compared to the planned ~97 per group.

**Original Plan** (from protocol):
> Target N=195 (accounting for 15% attrition buffer). Effective N needed: 166 (83 per group) for power=0.80 to detect d=0.50 at alpha=0.05.

**Actual**: N=180 (treatment=88, control=92). Attrition=15 students (7.7%), which is within the 15% buffer. Effective N per group exceeds the minimum of 83.

**Reason**: 15 students withdrew during the semester citing schedule conflicts (n=9), medical leave (n=3), and course withdrawal (n=3). Attrition was roughly balanced between groups (8 treatment, 7 control).

**Impact Assessment**:
| Validity Type | Impact | Explanation |
|---------------|--------|-------------|
| Internal validity | minor | Attrition was balanced between groups (8 vs 7); no differential attrition pattern detected. Comparison of baseline characteristics (GPA, pre-test self-efficacy) between completers and non-completers showed no significant differences. |
| External validity | minor | Slightly smaller sample, but demographic composition of remaining sample closely matches the full enrolled cohort. |
| Statistical validity | minor | Post-hoc power analysis with N=180 and observed d=0.51: power = 0.82, still above the 0.80 threshold. Minimal impact on statistical conclusions. |

**Analysis Plan Update Required**: no
**Corrective Action Taken**: Post-hoc power analysis conducted to confirm adequate power. Baseline comparison of completers vs. non-completers performed to verify no differential attrition.
**Residual Risk**: Minimal. Power remains adequate and attrition appears random.

---

## Decision Log

### Entry [NB-009] -- 2026-07-01 10:00

- **Type**: decision
- **Author**: Dr. Wei-Lin Chen
- **Related Entries**: NB-008 (deviation)
- **Related Files**: None

**Decision**: Proceed with the original analysis plan without modification despite the sample size deviation.

**Context**: After discovering that N=180 (below target N=195), the team needed to decide whether to modify the analysis approach.

**Alternatives Considered**:
1. **Recruit additional participants**: Rejected because the semester is over; recruiting from a different semester would introduce temporal confounds.
2. **Switch to non-parametric tests**: Rejected because parametric assumptions are met and power remains adequate. Non-parametric tests would reduce power further.
3. **Use bootstrapping for all inferences**: Rejected because standard parametric tests are appropriate given the sample characteristics. Bootstrapping could be used as a supplementary robustness check.

**Rationale**: Post-hoc power analysis confirms power = 0.82 for the observed effect size (d=0.51), which exceeds the 0.80 threshold. Attrition is balanced and appears random. The original analysis plan is appropriate.

**Impact**:
- Affects: None — original analysis plan remains unchanged
- Requires: Document the deviation and power analysis in the Methods section
- Pre-registration update needed: no (N=180 > minimum effective N=166)

### Entry [NB-011] -- 2026-07-16 09:00

- **Type**: decision
- **Author**: Dr. Wei-Lin Chen, Yu-Ting Huang
- **Related Entries**: NB-010 (analysis), NB-001 (design)
- **Related Files**: None

**Decision**: Add a sensitivity analysis using Welch's t-test alongside the pooled-variance t-test for H1, even though Levene's test indicated equal variances.

**Context**: During the primary analysis, the research team discussed whether to add robustness checks beyond ANCOVA.

**Alternatives Considered**:
1. **Only report pooled t-test**: Rejected because a reviewer might question the equal-variance assumption despite Levene's test passing.
2. **Replace pooled t-test with Welch's**: Rejected because the pre-registered analysis specifies the pooled t-test; changing it would be a deviation.
3. **Report both as sensitivity analysis**: Chosen — transparent, addresses potential reviewer concern, and does not deviate from the pre-registered primary analysis.

**Rationale**: Reporting Welch's t-test alongside the pre-registered pooled t-test provides evidence of robustness without changing the primary analysis. If both tests reach the same conclusion (which they did: Welch's t(175.8) = 3.41, p < .001), this strengthens confidence in the finding.

**Impact**:
- Affects: Results reporting (add one additional line to Results section)
- Requires: Run Welch's t-test and document results (completed: see supplementary analysis in NB-010 Related Files)
- Pre-registration update needed: no (this is an additional sensitivity analysis, not a change to the primary analysis)

---

## File Manifest

| # | File Path | Purpose | SHA-256 Hash | Created | Producer | Dependencies |
|---|-----------|---------|-------------|---------|----------|-------------|
| 1 | experiment_outputs/protocols/protocol_EXP-20260316-001.md | Full experiment protocol (Schema 10) | 7a3f2b9c1d8e4f... | 2026-03-16 08:30 | experiment-designer | None |
| 2 | experiment_outputs/data/raw/survey_week1_section_a.csv | Pre-test survey, Section A (N=48) | 2b4c6d8e0f1a3b... | 2026-03-27 16:45 | Qualtrics export | None |
| 3 | experiment_outputs/data/raw/survey_week1_section_b.csv | Pre-test survey, Section B (N=45) | 3c5d7e9f1a2b4c... | 2026-03-27 16:50 | Qualtrics export | None |
| 4 | experiment_outputs/data/raw/survey_week1_section_c.csv | Pre-test survey, Section C (N=50) | 4d6e8f0a2b3c5d... | 2026-04-03 16:00 | Qualtrics export | None |
| 5 | experiment_outputs/data/raw/survey_week1_section_d.csv | Pre-test survey, Section D (N=45) | 5e7f9a1b3c4d6e... | 2026-04-03 16:05 | Qualtrics export | None |
| 6 | experiment_outputs/data/raw/exam_scores_all_sections.csv | Final exam scores (N=180) | 6f8a0b2c4d5e7f... | 2026-06-28 16:00 | Department records | None |
| 7 | experiment_outputs/data/raw/survey_post_all_sections.csv | Post-test survey (N=175) | 7a9b1c3d5e6f8a... | 2026-06-28 17:00 | Qualtrics export | None |
| 8 | experiment_outputs/scripts/01_clean_data.py | Data cleaning and merging script | 8b0c2d4e6f7a9b... | 2026-07-01 10:00 | Yu-Ting Huang | None |
| 9 | experiment_outputs/data/processed/combined_clean.csv | Cleaned, merged dataset (N=180) | 9c1d3e5f7a8b0c... | 2026-07-02 14:00 | data-analyst | #2, #3, #4, #5, #6, #7, #8 |
| 10 | experiment_outputs/scripts/02_primary_analysis.py | Primary analysis script (t-test, ANCOVA) | 0d2e4f6a8b9c1d... | 2026-07-14 09:00 | Yu-Ting Huang | None |
| 11 | experiment_outputs/results/tables/table_1_descriptive_stats.csv | Descriptive statistics by group | 1e3f5a7b9c0d2e... | 2026-07-15 11:00 | data-analyst | #9, #10 |
| 12 | experiment_outputs/results/tables/table_2_primary_results.csv | Primary analysis results | 2f4a6b8c0d1e3f... | 2026-07-15 11:15 | data-analyst | #9, #10 |
| 13 | experiment_outputs/results/figures/figure_1_boxplot_exam.png | Box plot of exam scores by group | 3a5b7c9d1e2f4a... | 2026-07-15 11:20 | data-analyst | #9, #10 |
| 14 | experiment_outputs/results/figures/figure_2_qq_plots.png | Q-Q plots for normality check | 4b6c8d0e2f3a5b... | 2026-07-15 11:25 | data-analyst | #9, #10 |
| 15 | experiment_env/requirements.txt | Python environment specification | 5c7d9e1f3a4b6c... | 2026-03-16 09:00 | Yu-Ting Huang | None |

---

## Step 2: Audit (audit mode)

**User command**: "Audit notebook experiment_outputs/logs/notebook_2026-03-16_ai-assessment.md"

The provenance_auditor_agent performs a full completeness audit.

---

## Audit Trail

### Audit 2026-07-20 10:00

- **Completeness Score**: 0.90
- **Interpretation**: Excellent
- **Files Verified**: 15 / 15
- **Hash Mismatches**: 0
- **Broken References**: 0
- **Recommendations**: 3 (HIGH: 1, MEDIUM: 1, LOW: 1)
- **Previous Score**: First audit
- **Score Change**: N/A

**Section Scores**:
| Section | Weight | Score | Status |
|---------|--------|-------|--------|
| Design Record | 25% | 1.00 | complete |
| Environment Record | 5% | 1.00 | complete |
| Data Collection Log | 15% | 1.00 | complete |
| Data Preparation Log | 10% | 1.00 | complete |
| Analysis Log | 25% | 0.50 | partial (H1 analyzed, H2 not yet) |
| Simulation Log | 0% | N/A | not planned |
| Deviation Log | 10% | 1.00 | complete |
| Decision Log | 5% | 1.00 | complete |
| File Manifest | 15% | 1.00 | complete |

**Weighted Score**: (0.25 * 1.0) + (0.05 * 1.0) + (0.15 * 1.0) + (0.10 * 1.0) + (0.25 * 0.5) + (0.10 * 1.0) + (0.05 * 1.0) + (0.15 * 1.0) = 0.25 + 0.05 + 0.15 + 0.10 + 0.125 + 0.10 + 0.05 + 0.15 = **0.90** (rounding: weights verified to sum to 1.00 with simulation redistribution)

**Recommendations**:
1. **[HIGH]** Complete analysis for H2 (self-efficacy). The secondary hypothesis has not been tested yet.
2. **[MEDIUM]** Add post-survey response rate analysis (5 participants completed exam but not post-survey).
3. **[LOW]** Consider adding an exploratory analysis entry for the moderation analysis mentioned in the analysis plan.

---

## Step 3: Export (export mode)

**User command**: "Export notebook for EXP-20260316-001 as Schema 12 handoff"

The provenance_auditor_agent produces the Schema 12 artifact.

---

## Schema 12: Lab Record

**Experiment ID**: EXP-20260316-001
**Notebook**: experiment_outputs/logs/notebook_2026-03-16_ai-assessment.md
**Entries**: 11
**Deviations**: 1 (DEV-001: sample fell below target N=195; actual N=180; severity: major; impact: minor across all validity types)
**Completeness**: 0.90 (gap: H2 secondary analysis not yet completed)

**Methods Summary**: A quasi-experimental study was conducted with 180 undergraduate physics students across 4 intact class sections at a Taiwanese university during Spring 2026. Two sections (n=88) received AI-assisted formative assessment via the XLearn platform; two sections (n=92) received traditional paper-based assessment. The Physics Self-Efficacy Scale was administered as pre- and post-test. The primary outcome was the departmental final exam score (0-100). One protocol deviation occurred: the final sample (N=180) fell below the pre-registered target (N=195) due to attrition (7.7%), but post-hoc power analysis confirmed adequate power (0.82) for the observed effect (d=0.51). Attrition was balanced between groups. Data were cleaned using listwise deletion (missing rate 2.8%, MCAR confirmed). Primary analysis used an independent samples t-test with ANCOVA robustness check controlling for prior GPA. All analyses were conducted using Python 3.12.3 (scipy 1.13.0, statsmodels 0.14.1, pingouin 0.5.4). The study was pre-registered on OSF Registries.

**Environment**: Python 3.12.3, pandas 2.2.1, scipy 1.13.0, statsmodels 0.14.1, pingouin 0.5.4, matplotlib 3.9.0, seaborn 0.13.2

**File Manifest**: 15 files (see notebook File Manifest section for full inventory with SHA-256 hashes)

**Completeness Gaps**:
- Analysis Log: H2 (self-efficacy) analysis not yet completed (secondary hypothesis)

**Deviations Summary**:
- DEV-001 (major): Final sample N=180 fell below target N=195. Attrition balanced. Post-hoc power adequate (0.82). No analysis plan changes required.

## Material Passport

- Origin Skill: lab-notebook
- Origin Mode: export
- Origin Date: 2026-07-20T10:30:00+08:00
- Verification Status: VERIFIED
- Version Label: lab_record_v1
- Content Hash: d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2c3d4
- Upstream Dependencies: [protocol_EXP-20260316-001_v1.0]

---

## What This Example Demonstrates

1. **Structured recording**: Every entry follows the canonical format with type, author, related entries, and related files
2. **Sequential IDs**: NB-001 through NB-011, no gaps (NB-005 is a note, NB-008 is a deviation, NB-009 and NB-011 are decisions)
3. **Cross-referencing**: Collection entries reference the design; preparation references collections; analysis references preparation and design; deviation references design and collection; decisions reference deviations and analyses
4. **Deviation handling**: DEV-001 follows the full template (what changed, original plan, actual, reason, impact assessment on all 3 validity types, corrective action)
5. **Decision documentation**: Both decisions document alternatives considered, rationale, and impact
6. **File manifest with provenance**: All 15 files tracked with SHA-256 hashes, creation dates, producers, and dependency chains
7. **Completeness scoring**: Weighted score of 0.90 with clear identification of the gap (H2 analysis pending)
8. **Schema 12 export**: Condensed methods summary suitable for paper writing, complete provenance record, and Material Passport for downstream handoff
