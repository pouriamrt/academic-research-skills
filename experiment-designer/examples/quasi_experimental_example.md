# Example: Quasi-Experimental Design — Comparing Teaching Methods Across Existing Class Sections

## User Request
```
Compare two teaching methods across existing class sections — I can't randomize students because they're already enrolled in their sections. I want to know if problem-based learning (PBL) improves critical thinking compared to traditional lectures.
```

## Phase 0: INTAKE

### intake_agent Output

**Mode**: `full` (user has clear RQ, specified design constraints, and a clear design need)

**Source**: User-supplied

**Design Brief**:
- Research Question: Does problem-based learning improve critical thinking compared to traditional lectures in undergraduate students?
- Design type: Quasi-experimental (user explicitly stated they cannot randomize)
- Methodology type: Quantitative
- Population: Undergraduate students in existing class sections
- Constraint: Cannot randomize — intact groups (pre-formed class sections)
- Timeline: One semester

**Key constraint detected**: "I can't randomize students because they're already enrolled in their sections." This rules out RCT. The design_architect_agent will select the strongest quasi-experimental alternative.

---

## Phase 1: DESIGN ARCHITECTURE

### design_architect_agent Output

**Experimental Design Blueprint**

**Selected Design**: Nonequivalent Control Group Pretest-Posttest Design
**Justification**: The user cannot randomize students to conditions because sections are pre-formed. This is the most common scenario in educational research. The nonequivalent control group design with pretest allows us to:
1. Assess baseline equivalence (are groups comparable?)
2. Control for pre-existing differences statistically (ANCOVA)
3. Estimate treatment effects with reasonable confidence (difference-in-differences)

The key threat — selection bias — is addressed through multiple strategies (see below).

**Reporting Standard**: TREND (Transparent Reporting of Evaluations with Nonrandomized Designs)

**Design Diagram**:
```
Existing class sections (NOT randomly assigned):
     |
Section A (Treatment):  O1  X_PBL  O2   (PBL instruction, n~30)
Section B (Treatment):  O1  X_PBL  O2   (PBL instruction, n~30)
Section C (Control):    O1  X_TL   O2   (Traditional lecture, n~30)
Section D (Control):    O1  X_TL   O2   (Traditional lecture, n~30)

O1 = Pretest (critical thinking + demographics)
X_PBL = Problem-based learning intervention (16 weeks)
X_TL = Traditional lecture (16 weeks, business as usual)
O2 = Posttest (critical thinking + satisfaction)

Total N ~ 120 (4 sections x ~30 students)
```

**Why 4 sections (not 2)**: Using 2 treatment and 2 control sections provides replication across sections, reducing the chance that results are due to section-specific factors (e.g., time of day, room assignment).

**Variables**:

| Role | Variable | Type | Operationalization |
|------|----------|------|--------------------|
| IV | Teaching method | Categorical (2 levels) | PBL vs Traditional lecture |
| DV (primary) | Critical thinking | Continuous | Watson-Glaser Critical Thinking Appraisal (WGCTA-III), 0-40 |
| DV (secondary) | Course satisfaction | Continuous | Course satisfaction survey, 7-point Likert, 8 items |
| Covariate | Baseline critical thinking | Continuous | WGCTA-III pretest score |
| Covariate | Prior GPA | Continuous | Cumulative GPA |
| Covariate | Year of study | Ordinal | Freshman/Sophomore/Junior/Senior |
| Control | Course content | Constant | Same syllabus, same textbook, same exams |
| Control | Instructor | **Critical issue** — see discussion below |

**Instructor Assignment Issue**:
The ideal scenario is one instructor teaching all 4 sections (eliminating instructor confound). If that is not possible, two instructors each teach one treatment and one control section (crossed design), which allows testing for instructor effects. Avoid the worst case: one instructor for all PBL sections and a different instructor for all traditional sections (perfect confound with instructor).

**Recommended instructor arrangement**:
```
              Instructor 1       Instructor 2
PBL           Section A          Section B
Traditional   Section C          Section D
```

This crossed design allows separating treatment effects from instructor effects.

**Threats to Validity Assessment**:

| Category | Threat | Likelihood | Mitigation | Residual Risk |
|----------|--------|-----------|------------|---------------|
| Internal | **Selection bias** | **HIGH** | ANCOVA with pretest + propensity score analysis; check baseline equivalence on multiple variables | Groups may differ on unmeasured variables |
| Internal | Selection-maturation | Medium | Include year of study as covariate; short study duration (1 semester) | Groups may mature at different rates |
| Internal | History | Medium | Multiple treatment/control sections reduce section-specific history effects | Campus-wide events affect all equally |
| Internal | Testing | Low | WGCTA-III has parallel forms A and B for pre/post | Minimal practice effect with different forms |
| Internal | Attrition | Medium | Track dropout by condition; compare completers vs dropouts; ITT analysis | If PBL is harder, more may drop from treatment |
| Internal | Instructor confound | Medium-High | Crossed instructor design (see above) | Cannot fully separate instructor personality from method |
| External | Population validity | Medium | Single institution, single discipline | May not generalize to other settings |
| External | Treatment variation | Medium | PBL facilitation guide and fidelity checklist | PBL quality may vary across sections |
| Construct | Hawthorne effect | Medium | Active control (traditional lecture is also instruction, not "no treatment") | PBL sections may feel "special" |
| Statistical | Low power | Medium | 4 sections x 30 students; pretest covariate boosts power | Clustering within sections reduces effective N |

**Addressing Selection Bias — The Primary Threat**

Since selection bias is the main concern in this design, multiple strategies are employed:

1. **Baseline equivalence check**: Compare treatment and control groups on all measured covariates (GPA, year, pretest score, demographics). Report results in a table.

2. **ANCOVA with pretest**: Statistically control for baseline critical thinking. This removes pre-existing differences on the primary outcome.

3. **Propensity score analysis**: Estimate the propensity of being in the treatment group based on observed covariates. Use propensity scores as a covariate or for matching/weighting.

4. **Difference-in-differences**: Compare the CHANGE in scores (posttest - pretest) between groups, not raw posttest scores. This accounts for baseline differences.

5. **Sensitivity analysis**: Conduct a sensitivity analysis for unmeasured confounders (e.g., Rosenbaum bounds) to assess how strong an unmeasured confounder would need to be to explain away the results.

```
Analysis hierarchy:
1. Naive comparison (t-test on posttest) — biased baseline
2. ANCOVA (posttest ~ group + pretest) — adjusts for baseline
3. Difference-in-differences — compares change scores
4. Propensity score weighted ANCOVA — adjusts for multiple covariates
5. Sensitivity analysis — what unmeasured confounder would nullify results?

If results are consistent across all 5 approaches, confidence increases.
```

---

## Phase 2: QUANTIFICATION & INSTRUMENTATION (Parallel)

### power_analyst_agent Output

**Power Analysis Report**

**Test Parameters**:
- Statistical test: ANCOVA (treatment group predicting posttest, controlling for pretest)
- Effect size: d = 0.50 (medium) — Source: Strobel & van Barneveld (2009) meta-analysis of PBL effects on critical thinking reported d = 0.33-0.80; we use d = 0.50 as the midpoint
- Alpha: 0.05 (two-tailed)
- Power: 0.80
- Pretest-posttest correlation: r = 0.60 (expected; WGCTA-III test-retest)

**Sample Size Calculation**:

```python
from statsmodels.stats.power import TTestIndPower
import numpy as np

# Conservative: independent t-test
analysis = TTestIndPower()
n_ttest = analysis.solve_power(effect_size=0.50, alpha=0.05, power=0.80,
                                ratio=1.0, alternative='two-sided')
# n_ttest = 64 per group

# ANCOVA adjustment: N_ancova = N_ttest * (1 - r^2)
r_prepost = 0.60
n_ancova = 64 * (1 - r_prepost**2)
# n_ancova = 64 * 0.64 = 41 per group

# Cluster adjustment (students nested in sections)
# ICC for classrooms typically 0.05-0.15; use 0.10
icc = 0.10
cluster_size = 30  # students per section
design_effect = 1 + (cluster_size - 1) * icc
# design_effect = 1 + 29 * 0.10 = 3.90

n_cluster_adjusted = int(np.ceil(41 * design_effect))
# n_cluster_adjusted = 160 (total)
# Per group: 80
# Sections needed per group: ceil(80/30) = 3

# With 2 sections per group (available):
n_per_group = 2 * 30  # = 60
# This is below 80 — the study is slightly underpowered for the cluster design

# With 15% attrition buffer:
n_target_per_group = int(np.ceil(60 / 0.85))  # = 71
```

**Result**:
- Required N per group (ANCOVA, no clustering): 41
- Required N per group (with ICC=0.10 adjustment): 80
- Available N per group (2 sections x 30): 60
- **Gap**: With 4 sections total (2 per condition), the study achieves approximately 0.68 power for d = 0.50 after clustering adjustment

**Recommendation**: The study is somewhat underpowered. Options to address:
1. **Add more sections** (3 per condition = 90 per group, power ~ 0.82) — preferred
2. **Accept lower power** (0.68) and report as limitation
3. **Seek larger sections** (40+ students per section)
4. **Use ANCOVA** (the pretest covariate substantially reduces error variance, partially offsetting the clustering penalty)

**For this example, we proceed with 4 sections (n ~ 120 total) and acknowledge the power limitation.**

**Sensitivity Analysis**:

| Total N (4 sections) | Min detectable d (with clustering) | Power for d=0.50 |
|----------------------|-----------------------------------|-------------------|
| 80 (20/section) | 0.72 | 0.52 |
| 100 (25/section) | 0.63 | 0.60 |
| 120 (30/section) | 0.58 | 0.68 |
| 160 (40/section) | 0.49 | 0.81 |
| 180 (3 sections/group x 30) | 0.46 | 0.85 |

---

### instrument_builder_agent Output

**Instrument 1: Watson-Glaser Critical Thinking Appraisal (WGCTA-III)** — Existing validated instrument

- Construct: Critical thinking (inference, recognition of assumptions, deduction, interpretation, evaluation of arguments)
- Type: 40-item multiple choice, timed (30 minutes)
- Forms: Form A (pretest), Form B (posttest) — parallel forms to reduce testing effect
- Validation: Extensively validated (Watson & Glaser, 2008; Pearson)
- Reliability: alpha = 0.81 (Watson & Glaser, 2008)
- Decision: **Use as-is** (licensed instrument, no modification permitted)

**Instrument 2: Course Satisfaction Survey** — Researcher-developed (8 items)

- Construct: Student satisfaction with teaching method (2 dimensions: learning experience, instructor support)
- Scale: 7-point Likert (1=Strongly Disagree to 7=Strongly Agree)

**Items**:

| # | Item | Dimension | Reverse |
|---|------|-----------|---------|
| 1 | The teaching approach in this course helped me learn effectively | Learning | No |
| 2 | I found the class activities engaging and relevant | Learning | No |
| 3 | I had difficulty understanding the material due to how it was taught | Learning | Yes |
| 4 | The course improved my ability to think critically about problems | Learning | No |
| 5 | The instructor provided adequate support for my learning | Support | No |
| 6 | I felt comfortable asking questions in this class | Support | No |
| 7 | I did not receive enough feedback on my work | Support | Yes |
| 8 | Overall, I am satisfied with this course | Overall | No |

- Reliability target: alpha >= 0.80
- Content validity: Expert review by 3 education researchers
- Pilot: Cognitive pretest with 6 students from non-participating sections

**Instrument 3: PBL Fidelity Checklist** — Observation instrument

- Purpose: Verify that PBL is implemented as intended
- Observer: Trained research assistant observes 20% of PBL sessions (random selection)
- Items: 10-item checklist (e.g., "Students work in small groups", "Problem is presented before content instruction", "Instructor serves as facilitator, not lecturer")
- Scoring: Percentage of items observed (target >= 80% fidelity)
- Inter-rater reliability: Two observers for 10% of observations; target kappa >= 0.70

---

### randomization_agent Output

**Status**: SKIPPED

**Reason**: This is a quasi-experimental design with intact class sections. Students are pre-enrolled and cannot be randomly assigned to conditions.

**Alternative bias-reduction strategy**: Propensity score analysis using observed covariates (pretest score, GPA, year, demographics) to adjust for selection bias. Baseline equivalence table will be reported. Sensitivity analysis for unmeasured confounders will be conducted.

**Section assignment** (non-random): Sections were assigned to conditions based on schedule availability and instructor willingness, NOT based on student characteristics. This is documented but does not constitute randomization.

```
Section A (MWF 9:00am): PBL — Instructor 1
Section B (TR 10:30am): PBL — Instructor 2
Section C (MWF 11:00am): Traditional — Instructor 2
Section D (TR 1:00pm): Traditional — Instructor 1
```

Note: The crossed instructor design (each instructor teaches one PBL and one traditional section) addresses instructor confounding.

---

## Phase 3: PROTOCOL COMPILATION

### protocol_compiler_agent Output

**Cross-Validation Report**:

| Check | Status | Details |
|-------|--------|---------|
| Design-Power alignment | WARNING | Study achieves ~0.68 power for d=0.50 with clustering; slightly below 0.80 target. Acknowledged as limitation. ANCOVA partially compensates. |
| Design-Instrument alignment | PASS | WGCTA-III measures primary DV (critical thinking); course satisfaction survey measures secondary DV. PBL fidelity checklist monitors treatment integrity. |
| Design-Randomization alignment | PASS (SKIPPED) | Randomization correctly skipped for quasi-experimental design. Alternative bias-reduction strategies documented. |
| Design-Analysis alignment | PASS | ANCOVA tests H1; propensity score sensitivity analysis provides robustness check. Instructor crossed design allows testing instructor effects. |
| Timeline feasibility | PASS | 16-week semester fits data collection timeline. IRB needed for human subjects. Pilot time for satisfaction survey included. |

**Overall Status**: READY (with power limitation acknowledged)

---

### Schema 10: Experiment Design

**Experiment ID**: EXP-20260316-002

**Design Type**: quasi_experimental

**Hypotheses**:
- H1 (primary, positive): Students in PBL sections will show significantly greater improvement in critical thinking (WGCTA-III) from pretest to posttest compared to students in traditional lecture sections, controlling for baseline scores
- H2 (secondary, positive): Students in PBL sections will report higher course satisfaction
- H3 (exploratory, non-directional): The effect of teaching method on critical thinking is moderated by prior GPA

**Variables**:
- Independent: Teaching method — categorical — Levels: [PBL, Traditional lecture] — Operationalization: PBL = structured problem-based learning per facilitation guide; Traditional = standard lecture format
- Dependent (primary): Critical thinking — continuous — Measurement: WGCTA-III, 0-40
- Dependent (secondary): Course satisfaction — continuous — Measurement: 8-item 7-point Likert, 8-56
- Control: Course content (constant syllabus), Instructor (crossed design)
- Covariate: Baseline WGCTA-III pretest, Prior GPA, Year of study
- Moderator: Prior GPA

**Sample**: target_n=120 (4 sections x 30), power=0.68, alpha=0.05, effect_size="d=0.50", attrition_buffer=0.15

**Analysis Plan**:
- Primary: ANCOVA | IV: Teaching method | DV: WGCTA-III posttest | Covariates: WGCTA-III pretest, Prior GPA | Hypothesis: H1
- Primary (robustness): Propensity score weighted ANCOVA | Same specification + propensity weights | Hypothesis: H1
- Primary (robustness): Difference-in-differences | Change score ~ Teaching method | Hypothesis: H1
- Secondary: Independent t-test | IV: Teaching method | DV: Course satisfaction | Hypothesis: H2
- Exploratory: Moderated regression | IV: Teaching method * GPA | DV: WGCTA-III posttest | Hypothesis: H3
- Sensitivity: Rosenbaum bounds for unmeasured confounding

**Validity Threats**: [10 threats assessed; selection bias is HIGH with multiple mitigations]

**Randomization**: Not applicable (quasi-experimental design; see alternative bias-reduction strategies)

**Instruments**: WGCTA-III (validated, licensed), Course satisfaction survey (researcher-developed, 8 items), PBL fidelity checklist (10 items)

**Timeline**:

| Milestone | Week | Duration |
|-----------|------|----------|
| IRB submission | -8 | 6 weeks |
| Satisfaction survey pilot | -3 | 2 weeks |
| Fidelity observer training | -2 | 1 week |
| Pretest + demographics (O1) | 1 | 1 week |
| PBL/Traditional instruction | 2-16 | 15 weeks |
| Fidelity observations (20% of PBL sessions) | 2-16 | Ongoing |
| Posttest + satisfaction (O2) | 17 | 1 week |
| Data analysis | 18-22 | 5 weeks |

---

### Material Passport (Schema 9)

- Origin Skill: experiment-designer
- Origin Mode: full
- Origin Date: 2026-03-16T11:00:00Z
- Verification Status: UNVERIFIED
- Version Label: experiment_design_v1
- Upstream Dependencies: [none — user-supplied input]

---

## Key Differences from the RCT Example

| Dimension | RCT Example | Quasi-Experimental Example |
|-----------|-------------|---------------------------|
| Randomization | Stratified block randomization | None (intact groups) |
| randomization_agent | Active | **SKIPPED** |
| Primary internal validity threat | Attrition (medium) | **Selection bias (HIGH)** |
| Bias-reduction strategy | Random assignment | ANCOVA + propensity scores + DiD + sensitivity analysis |
| Power analysis | Standard (N=90 per group, power=0.87) | Cluster-adjusted (N=60 per group, power=0.68) |
| Reporting standard | CONSORT 2010 | TREND |
| Instructor confound | One instructor for all | Crossed design (each teaches one of each) |
| Number of analysis approaches | 1 primary | 3 primary + sensitivity (robustness check) |
| Confidence in causal inference | Strong | Moderate (strengthened by convergent evidence across methods) |

---

## Final Output Summary

- Complete TREND-aligned protocol document
- Schema 10 artifact with all required fields
- Quasi-experimental design: nonequivalent control group with pretest-posttest
- Power analysis: N=120, power=0.68 for d=0.50 (limitation acknowledged; ANCOVA partially compensates)
- 3 instruments: WGCTA-III (validated), Course satisfaction (8 items), PBL fidelity checklist (10 items)
- Randomization: SKIPPED — alternative bias-reduction strategies documented
- Selection bias addressed through 5 complementary analytical approaches
- Crossed instructor design reduces instructor confounding
- TREND reporting standard identified
- 10 validity threats assessed with mitigations
