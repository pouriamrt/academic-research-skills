# Example: RCT Design — AI-Assisted Feedback on Physics Learning Outcomes

## User Request
```
Design an RCT testing whether AI-assisted feedback improves physics learning outcomes in undergraduate students
```

## Phase 0: INTAKE

### intake_agent Output

**Mode**: `full` (user has clear RQ and specified design type)

**Source**: User-supplied

**Design Brief**:
- Research Question: Does AI-assisted formative feedback improve physics learning outcomes compared to traditional instructor feedback?
- Design type: RCT (user specified)
- Methodology type: Quantitative (experimental)
- Population: Undergraduate physics students
- Feasible N range: 100-300 (typical university course enrollment)
- Timeline: One semester (16 weeks)
- Upstream materials: None (no prior deep-research output)

**Missing Information**:
- Specific physics course/level
- Specific AI tool to be used
- Primary outcome measure
- Control condition details

**Resolution**: Downstream agents will specify these based on the RQ.

---

## Phase 1: DESIGN ARCHITECTURE

### design_architect_agent Output

**Experimental Design Blueprint**

**Selected Design**: Parallel-group RCT (two-arm)
**Justification**: The RQ asks a causal question (does X improve Y?), random assignment is feasible (students can be assigned to sections), and a between-subjects design avoids contamination that would occur if students in the same section received different feedback types.

**Reporting Standard**: CONSORT 2010

**Design Diagram**:
```
Recruitment: Undergraduate General Physics I students (Fall 2026)
     |
Eligibility screening (enrolled, consenting, no prior course)
     |
Baseline measurement (O1): Prior physics knowledge test + demographics
     |
Randomization (stratified by prior GPA: high/low)
     |
     +-> Treatment (n=90): AI-assisted formative feedback via XLearn platform
     |   - Weekly problem sets with immediate AI-generated feedback
     |   - Personalized hints and worked examples
     |   - 16 weeks
     |
     +-> Control (n=90): Traditional instructor feedback
         - Weekly problem sets with instructor grading (48-72hr turnaround)
         - Standard written comments
         - 16 weeks
     |
Post-test measurement (O2): Conceptual understanding + procedural skills
     |
Follow-up (O3): Retention test at 4 weeks post-course (optional)
```

**Variables**:

| Role | Variable | Type | Operationalization |
|------|----------|------|--------------------|
| IV | Feedback type | Categorical (2 levels) | AI-assisted vs Traditional instructor |
| DV (primary) | Physics learning outcomes | Continuous | Force Concept Inventory (FCI) post-test score, 0-30 |
| DV (secondary) | Procedural physics skills | Continuous | Physics Problem-Solving Assessment (PPSA), 0-100 |
| DV (secondary) | Self-efficacy for physics | Continuous | Physics Self-Efficacy Scale (PSES), 5-point Likert, 12 items |
| Covariate | Prior physics knowledge | Continuous | FCI pre-test score |
| Covariate | Prior GPA | Continuous | Cumulative GPA at enrollment |
| Control | Instructor | Categorical | Same instructor teaches all sections |
| Control | Course content | Constant | Identical syllabus, textbook, and exams |
| Moderator | Prior GPA | Continuous | Does prior achievement moderate the treatment effect? |

**Threats to Validity Assessment**:

| Category | Threat | Likelihood | Mitigation | Residual Risk |
|----------|--------|-----------|------------|---------------|
| Internal | Selection bias | Low | Random assignment with stratification by GPA | Minimal; check baseline equivalence |
| Internal | Attrition | Medium | Retention incentives (course credit); ITT analysis | Differential dropout if AI feedback is frustrating |
| Internal | Contamination | Medium | Separate class sections; students instructed not to share | Students may discuss assignments informally |
| Internal | Testing effect | Low | Different items on pre-test and post-test (parallel forms) | Some practice effect possible |
| External | Population validity | Medium | Single university sample | Results may not generalize to other institutions |
| External | Ecological validity | Low | Real classroom setting (not lab) | Good ecological validity |
| Construct | Mono-operation | Medium | AI feedback is one specific platform (XLearn) | Results may not generalize to other AI tools |
| Construct | Experimenter expectancy | Low | Assessments are standardized (FCI); graded blindly | Minimal |
| Statistical | Low power | Low | A priori power analysis (see below) | If effect is smaller than d=0.42, underpowered |
| Statistical | Multiple comparisons | Medium | 3 DVs: apply Holm correction | Adjusted alpha reduces power for secondary outcomes |

**Design Trade-offs**:
- Prioritized internal validity (controlled comparison, random assignment)
- Sacrificed some external validity (single institution, single AI platform)
- Used active control (traditional feedback, not no feedback) to isolate the AI component

**Preliminary Analysis Plan**:
- Primary: ANCOVA — FCI post-test ~ Feedback type + FCI pre-test
- Secondary: ANCOVA — PPSA ~ Feedback type + FCI pre-test; t-test on PSES
- Exploratory: Moderation — FCI post-test ~ Feedback type * Prior GPA + FCI pre-test

**Parameters for Power Analysis**:
- Target effect size: d = 0.50 (based on meta-analysis of formative feedback, Hattie & Timperley, 2007: d = 0.73; conservative estimate accounting for AI-specific context)
- Alpha: 0.05 (two-tailed)
- Power: 0.80
- Test: ANCOVA (independent t-test as conservative estimate)

---

## Phase 2: QUANTIFICATION & INSTRUMENTATION (Parallel)

### power_analyst_agent Output

**Power Analysis Report**

**Test Parameters**:
- Statistical test: Independent samples t-test (conservative; ANCOVA will be more powerful)
- Effect size: d = 0.50 (medium) — Source: Hattie & Timperley (2007) meta-analysis reported d = 0.73 for formative feedback; we use d = 0.50 as conservative estimate for AI-specific context
- Alpha: 0.05 (two-tailed)
- Power: 0.80

**Sample Size Result**:
```python
from statsmodels.stats.power import TTestIndPower
import numpy as np

analysis = TTestIndPower()
n = analysis.solve_power(effect_size=0.50, alpha=0.05, power=0.80,
                          ratio=1.0, alternative='two-sided')
n_per_group = int(np.ceil(n))  # 64

# With 15% attrition buffer
n_adjusted = int(np.ceil(64 / 0.85))  # 76

# ANCOVA adjustment: pretest-posttest r ~ 0.60 expected
# ANCOVA effective N = N * (1 - r^2) = 64 * 0.64 = 41
# So with ANCOVA, we need fewer; but we power conservatively with t-test
```

- Required N per group: 64
- Attrition buffer: 15%
- Adjusted N per group: 76
- **Recommendation: Recruit 90 per group (180 total)** for additional safety margin

**Power Curve**: [Figure showing power curves for d = 0.3, 0.5, 0.8 across N = 10-150]

**Sensitivity Analysis**:

| N per group | Min detectable d | Magnitude |
|-------------|-----------------|-----------|
| 50 | 0.57 | Medium-Large |
| 64 | 0.50 | Medium |
| 75 | 0.46 | Medium |
| 90 | 0.42 | Small-Medium |
| 100 | 0.40 | Small-Medium |

**Interpretation**: With 90 per group, the study can detect effects as small as d = 0.42. If the true effect is d = 0.50, power is 0.87 (exceeding the 0.80 target).

---

### instrument_builder_agent Output

**Instrument 1: Force Concept Inventory (FCI)** — Existing validated instrument

- Construct: Conceptual understanding of Newtonian mechanics
- Type: 30-item multiple choice
- Validation: Extensively validated (Hestenes et al., 1992; Hake, 1998)
- Reliability: alpha = 0.89 (Hestenes et al., 1992)
- Decision: **Use as-is** (no modification needed)

**Instrument 2: Physics Problem-Solving Assessment (PPSA)** — Researcher-developed

- Construct: Procedural physics problem-solving skills
- Type: 10 open-ended physics problems, scored with analytic rubric (0-10 per problem)
- Development: Based on course learning objectives
- Pilot plan: Phase 1 cognitive pretest (N=8), Phase 2 pilot (N=40)
- Reliability target: Inter-rater ICC >= 0.80

**PPSA Rubric** (per problem):

| Score | Descriptor |
|-------|-----------|
| 10 | Correct solution with clear reasoning, appropriate physics principles identified and applied, correct units |
| 8 | Correct final answer with minor reasoning gaps OR incorrect answer with sound methodology |
| 6 | Appropriate approach chosen but significant errors in execution |
| 4 | Partial understanding shown; major conceptual or procedural errors |
| 2 | Minimal relevant physics content; largely incorrect approach |
| 0 | No attempt or completely irrelevant response |

**Instrument 3: Physics Self-Efficacy Scale (PSES)** — New instrument (12 items)

- Construct: Self-efficacy for learning physics (3 dimensions: conceptual understanding, problem-solving, lab skills)
- Scale: 5-point Likert (1=Strongly Disagree to 5=Strongly Agree)
- Sample items:
  - "I am confident I can understand the physics concepts covered in this course" (Conceptual, forward)
  - "I struggle to solve physics problems on my own" (Problem-solving, reverse)
  - "I can successfully conduct physics laboratory experiments" (Lab skills, forward)
- Reliability target: alpha >= 0.80 per dimension
- Content validity: Expert panel of 4 physics education researchers (I-CVI >= 0.78)
- Pilot plan: Cognitive pretest (N=8), small pilot (N=40), CFA on full sample

---

### randomization_agent Output

**Randomization Schedule**

**Method**: Stratified block randomization
- Stratification variable: Prior GPA (High >= 3.0 vs Low < 3.0)
- Block size: Varying (4, 6, 8) to prevent prediction
- Allocation ratio: 1:1

**Seed Record**:
- Master seed: 20260316
- Algorithm: PCG64 via numpy.random.default_rng
- NumPy version: 1.26.4
- Date: 2026-03-16

**Code**:
```python
import numpy as np
import pandas as pd

rng = np.random.default_rng(seed=20260316)

# Stratified block randomization
def assign(participants_df, seed=20260316):
    df = participants_df.copy()
    df['group'] = ''
    strata = df.groupby('gpa_stratum')

    stratum_seed = seed
    for name, stratum_df in strata:
        stratum_seed += 1
        stratum_rng = np.random.default_rng(stratum_seed)
        n = len(stratum_df)
        assignments = []
        block_sizes = [4, 6, 8]
        while len(assignments) < n:
            bs = stratum_rng.choice(block_sizes)
            block = ['Treatment'] * (bs // 2) + ['Control'] * (bs // 2)
            stratum_rng.shuffle(block)
            assignments.extend(block)
        df.loc[stratum_df.index, 'group'] = assignments[:n]
    return df
```

**Allocation Table (first 10)**:

| ID | GPA Stratum | Group |
|----|------------|-------|
| P001 | High | Treatment |
| P002 | High | Control |
| P003 | Low | Treatment |
| P004 | High | Control |
| P005 | Low | Control |
| P006 | High | Treatment |
| P007 | Low | Treatment |
| P008 | Low | Control |
| P009 | High | Treatment |
| P010 | High | Control |

**Balance Summary**:

| Group | N | High GPA | Low GPA |
|-------|---|----------|---------|
| Treatment | 90 | 48 | 42 |
| Control | 90 | 47 | 43 |

**Concealment Plan**: Central allocation via sealed sequentially numbered envelopes prepared by an independent research assistant. Envelopes opened only after participant completes baseline measurement and confirms enrollment.

---

## Phase 3: PROTOCOL COMPILATION

### protocol_compiler_agent Output

**Cross-Validation Report**:

| Check | Status | Details |
|-------|--------|---------|
| Design-Power alignment | PASS | RCT (2-group) matches independent t-test power analysis; ANCOVA will be more powerful |
| Design-Instrument alignment | PASS | FCI measures primary DV; PPSA measures secondary DV; PSES measures tertiary DV |
| Design-Randomization alignment | PASS | 2-group design matches 1:1 allocation; stratified by GPA as specified |
| Design-Analysis alignment | PASS | ANCOVA for H1 (FCI ~ Group + pretest); t-test for H2 (PSES); moderation for exploratory |
| Timeline feasibility | PASS | 16-week semester + 4-week follow-up; IRB submission 8 weeks prior |

**Overall Status**: READY

---

### Schema 10: Experiment Design

**Experiment ID**: EXP-20260316-001

**Design Type**: RCT

**Hypotheses**:
- H1 (primary, positive): Students receiving AI-assisted formative feedback will score significantly higher on the FCI post-test than students receiving traditional instructor feedback, controlling for pre-test scores
- H2 (secondary, positive): Students in the AI feedback group will report higher physics self-efficacy
- H3 (exploratory, non-directional): Prior GPA moderates the effect of feedback type on FCI scores

**Variables**:
- Independent: Feedback type — categorical — Levels: [AI-assisted, Traditional] — Operationalization: AI-assisted = XLearn platform with immediate personalized feedback; Traditional = instructor grading with 48-72hr turnaround
- Dependent (primary): FCI post-test score — continuous — Measurement: Force Concept Inventory, 30 items, 0-30
- Dependent (secondary): PPSA score — continuous — Measurement: 10 open-ended problems, rubric-scored 0-100
- Dependent (secondary): PSES score — continuous — Measurement: 12-item Likert scale, 12-60
- Control: Prior knowledge (FCI pre-test), Prior GPA, Instructor (constant), Course content (constant)
- Moderator: Prior GPA — continuous

**Sample**: target_n=180, power=0.80, alpha=0.05, effect_size="d=0.50", attrition_buffer=0.15

**Analysis Plan**:
- Primary: ANCOVA | IV: Feedback type | DV: FCI post-test | Covariates: FCI pre-test | Hypothesis: H1
- Secondary: Independent t-test | IV: Feedback type | DV: PSES total | Hypothesis: H2
- Secondary: ANCOVA | IV: Feedback type | DV: PPSA | Covariates: FCI pre-test | Hypothesis: H1b
- Exploratory: Moderated regression | IV: Feedback type * Prior GPA | DV: FCI post-test | Hypothesis: H3

**Validity Threats**: [10 threats assessed, as detailed above]

**Randomization**: method="stratified_block", seed=20260316, allocation_ratio="1:1"

**Instruments**: FCI (validated), PPSA (researcher-developed, rubric), PSES (new, 12-item Likert)

**Timeline**:

| Milestone | Week | Duration |
|-----------|------|----------|
| IRB submission | -8 | 6 weeks for approval |
| Instrument pilot (PPSA, PSES) | -4 | 3 weeks |
| Recruitment and baseline (O1) | 1 | 1 week |
| Randomization | 1 | Same day as baseline |
| Intervention period | 2-16 | 15 weeks |
| Post-test (O2) | 17 | 1 week |
| Follow-up (O3) | 21 | 1 week |
| Data analysis | 22-26 | 5 weeks |

---

### Material Passport (Schema 9)

- Origin Skill: experiment-designer
- Origin Mode: full
- Origin Date: 2026-03-16T10:00:00Z
- Verification Status: UNVERIFIED
- Version Label: experiment_design_v1
- Upstream Dependencies: [none — user-supplied input]

---

## Final Output Summary

- Complete SPIRIT-aligned protocol document
- Schema 10 artifact with all required fields
- Power analysis: N=90 per group (180 total), power=0.87 for d=0.50
- 3 instruments: FCI (validated), PPSA (researcher-developed rubric), PSES (new 12-item scale)
- Stratified block randomization with recorded seed
- 10 validity threats assessed with mitigations
- CONSORT 2010 reporting standard identified
- Timeline: 26 weeks from IRB submission to analysis completion
