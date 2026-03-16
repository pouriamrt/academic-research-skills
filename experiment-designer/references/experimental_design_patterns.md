# Experimental Design Patterns — Comprehensive Design Decision Tree

## Purpose

Ready-to-use design templates and decision trees for selecting the optimal experimental design. Used by the design_architect_agent. Each design includes when to use, design template, threats to validity, and the appropriate reporting standard.

---

## Master Design Selection Flowchart

```
START: What is the primary research goal?
|
+-- Establish causation (does X cause Y?)
|   |
|   +-- Can you randomly assign participants to conditions?
|   |   |
|   |   +-- YES: How many independent variables?
|   |   |   |
|   |   |   +-- 1 IV
|   |   |   |   +-- Between-subjects? --> Pattern 1: RCT (Parallel Group)
|   |   |   |   +-- Within-subjects (reversible, washout OK)? --> Pattern 3: Crossover
|   |   |   |
|   |   |   +-- 2+ IVs
|   |   |       +-- All between-subjects? --> Pattern 2: Factorial (Between)
|   |   |       +-- Mix of between and within? --> Pattern 2b: Factorial (Mixed)
|   |   |       +-- All within-subjects? --> Pattern 2c: Factorial (Within/RM)
|   |   |
|   |   +-- NO: Why not?
|   |       |
|   |       +-- Ethical/practical barriers, intact groups available
|   |       |   +-- Pretest available? --> Pattern 4a: Nonequivalent Control Group
|   |       |   +-- Multiple time points before/after? --> Pattern 4b: Interrupted Time Series
|   |       |   +-- Natural cutoff/threshold? --> Pattern 4c: Regression Discontinuity
|   |       |
|   |       +-- Very small sample (N = 1-5)
|   |           +-- Effect reversible? --> Pattern 5a: ABAB Withdrawal
|   |           +-- Effect irreversible / multiple behaviors? --> Pattern 5b: Multiple Baseline
|   |
|   +-- Need to generalize to real-world practice?
|       +-- YES: Consider pragmatic trial variant of any above design
|
+-- Establish association (is X related to Y?)
|   +-- One time point? --> Pattern 6a: Cross-Sectional Correlational
|   +-- Multiple time points? --> Pattern 6b: Longitudinal Panel
|   +-- Many predictors, complex model? --> Pattern 6c: SEM/Path Analysis Design
|
+-- Establish effectiveness in practice?
    +-- Pattern 7: Pragmatic / Hybrid Effectiveness-Implementation
```

---

## Pattern 1: Randomized Controlled Trial (RCT, Parallel Group)

### When to Use
- Testing a single causal hypothesis (does intervention X improve outcome Y?)
- Random assignment is feasible and ethical
- Between-subjects comparison is appropriate (no carryover concern)
- Considered the gold standard for causal inference

### Design Template
```
Recruitment -> Eligibility Screening -> Baseline (O1) -> Randomization
   |
   +-> Treatment Group:  O1  X  O2  [O3 follow-up]
   +-> Control Group:    O1     O2  [O3 follow-up]

R = Randomization
O = Observation/measurement
X = Intervention
```

### Variants
- **Waitlist control**: Control receives treatment after study period. Ethical when withholding treatment is problematic
- **Active control**: Control receives alternative treatment. Controls for attention/placebo effects
- **Three-arm**: Treatment A vs Treatment B vs Control. Tests comparative effectiveness
- **Solomon four-group**: Adds two groups without pretest to assess testing effects
  ```
  R  O1  X  O2  (Treatment + pretest)
  R  O1     O2  (Control + pretest)
  R      X  O2  (Treatment, no pretest)
  R         O2  (Control, no pretest)
  ```

### Key Threats
| Threat | Likelihood | Notes |
|--------|-----------|-------|
| Selection bias | LOW (randomization addresses this) | Check baseline equivalence |
| Attrition | MEDIUM-HIGH (especially long studies) | Use ITT analysis |
| Contamination | MEDIUM (same setting) | Separate groups physically |
| Hawthorne effect | MEDIUM | Use active control |
| Experimenter expectancy | MEDIUM | Double-blind if possible |

### Reporting Standard
**CONSORT 2010** — 25-item checklist. Key items: randomization method, allocation concealment, blinding, ITT analysis, flow diagram.

---

## Pattern 2: Factorial Design

### When to Use
- Testing 2+ independent variables simultaneously
- Interested in interaction effects (does the effect of A depend on B?)
- More efficient than running separate experiments for each factor
- When factors are theoretically expected to interact

### Design Template (2x2 Between-Subjects)
```
              Factor B
              B1 (Low)    B2 (High)
Factor A1     Cell 1       Cell 2        n per cell
(Control)     (A1B1)       (A1B2)

Factor A2     Cell 3       Cell 4        n per cell
(Treatment)   (A2B1)       (A2B2)

Total N = 4 * n_per_cell
```

### Design Template (2x3 Mixed)
```
              Time (Within-subjects)
              T1 (Pre)    T2 (Post)   T3 (Follow-up)
Treatment     O1          O2          O3            n
Control       O1          O2          O3            n

Between factor: Group (Treatment vs Control)
Within factor: Time (Pre, Post, Follow-up)
```

### Common Configurations

| Configuration | Cells | Primary Use | N Consideration |
|---------------|-------|-------------|-----------------|
| 2x2 | 4 | Two binary factors | Most efficient factorial |
| 2x3 | 6 | One binary factor + one 3-level factor | Moderate N |
| 3x3 | 9 | Two 3-level factors | Large N required |
| 2x2x2 | 8 | Three binary factors | Three-way interaction is hard to interpret |
| 2x2 mixed | 4 (2 between) | One between, one within factor | Within-subjects reduces N |

### Key Rule: Power for Interactions
The interaction effect typically requires **4x the sample size** of main effects to achieve the same power. If the interaction is the primary hypothesis, power the study for the interaction, not the main effects.

### Key Threats
| Threat | Likelihood | Notes |
|--------|-----------|-------|
| Underpowered interaction | HIGH | Most common problem with factorial designs |
| Complexity of interpretation | MEDIUM | Higher-order interactions (3-way+) are difficult to interpret |
| Cell size imbalance | MEDIUM | Unequal cell sizes complicate ANOVA |
| Multiple comparisons | MEDIUM | Multiple main effects + interaction = multiple tests |

### Reporting Standard
**CONSORT 2010** (extension for factorial trials) — report all main effects and interactions, even non-significant ones.

---

## Pattern 3: Crossover Design

### When to Use
- Each participant can receive multiple treatments (treatment effects are temporary)
- Adequate washout period exists between treatments
- Want to reduce between-subject variability (each person is their own control)
- Fewer participants needed than parallel design

### Design Template (AB/BA)
```
Period 1        Washout        Period 2
Group 1:  A    [washout]       B
Group 2:  B    [washout]       A

Measurements at end of each period.
```

### Design Template (Latin Square, 3 treatments)
```
         Period 1    Period 2    Period 3
Group 1:    A           B           C
Group 2:    B           C           A
Group 3:    C           A           B
```

### Critical Requirements
1. **Washout period**: Must be long enough for treatment effect to fully dissipate. Use pharmacokinetic half-life (drugs) or theoretical recovery time (behavioral interventions)
2. **Stable condition**: The underlying condition should not change over the study period (no progressive disease)
3. **No carryover**: Treatment in period 1 must not permanently change the participant

### Key Threats
| Threat | Likelihood | Notes |
|--------|-----------|-------|
| Carryover effect | HIGH | Primary risk; washout must be adequate |
| Period effect | MEDIUM | Participants change from period 1 to 2 regardless of treatment |
| Dropout between periods | MEDIUM | Longer study = more attrition |
| Unequal sequences | LOW (if properly randomized) | Randomize sequence assignment |

### Analysis Note
Use mixed models or repeated-measures ANOVA with sequence, period, and treatment as factors. Test for carryover (sequence x treatment interaction) before interpreting treatment effect.

### Reporting Standard
**CONSORT extension for crossover trials** — report both periods, washout duration, carryover test results.

---

## Pattern 4: Quasi-Experimental Designs

### Pattern 4a: Nonequivalent Control Group Design

#### When to Use
- Intact groups (classrooms, clinics, departments) cannot be randomized
- Pretest is available to assess baseline equivalence
- Most common quasi-experimental design in education and social science

#### Design Template
```
(No R)  O1  X  O2  (Treatment group — intact group)
(No R)  O1     O2  (Control group — comparison intact group)

No R = Not randomly assigned
O1 = Pretest (same measure as O2)
X = Intervention
O2 = Posttest
```

#### Strengthening Strategies
- **Propensity score matching**: Match treatment and control participants on observed covariates
- **ANCOVA with pretest**: Statistically control for baseline differences
- **Difference-in-differences**: Compare the change (O2-O1) between groups, not raw O2 scores
- **Multiple pretests**: O1a, O1b, O1c to establish baseline trajectory

#### Key Threats
| Threat | Likelihood | Notes |
|--------|-----------|-------|
| Selection bias | HIGH | The primary threat; groups may differ systematically |
| Selection-maturation interaction | MEDIUM | Groups may mature at different rates |
| Regression to the mean | MEDIUM | If groups selected for extreme scores |
| Local history | MEDIUM | Group-specific events may co-occur with treatment |

### Pattern 4b: Interrupted Time Series (ITS)

#### When to Use
- A policy, program, or event occurs at a specific time point
- Multiple observations exist before and after the event
- No control group is available (single-group ITS) or a comparison series exists (controlled ITS)

#### Design Template
```
Single-group ITS:
O1  O2  O3  O4  O5  |X|  O6  O7  O8  O9  O10

Controlled ITS:
Treatment:  O1 O2 O3 O4 O5  |X|  O6 O7 O8 O9 O10
Comparison: O1 O2 O3 O4 O5       O6 O7 O8 O9 O10
```

#### Minimum Requirements
- At least 8 time points total (ideally 4+ before and 4+ after intervention)
- Equal spacing between time points
- Consistent measurement across all time points

#### Analysis
- Segmented regression: test for change in level and slope at the intervention point
- ARIMA models for autocorrelated time series data

#### Key Threats
| Threat | Likelihood | Notes |
|--------|-----------|-------|
| History (co-occurring events) | HIGH (single-group) / MEDIUM (controlled) | The primary threat |
| Instrumentation change | MEDIUM | Ensure same measurement across all points |
| Seasonality | MEDIUM | Model seasonal patterns in the pre-intervention series |
| Autocorrelation | HIGH | Statistical issue — use ARIMA or Newey-West SEs |

### Pattern 4c: Regression Discontinuity Design (RDD)

#### When to Use
- Treatment is assigned based on a continuous assignment variable with a cutoff (e.g., GPA > 3.0 gets scholarship, test score > 70 passes)
- The assignment rule is strictly followed (no manipulation near cutoff)
- Provides strong causal inference at the cutoff point

#### Design Template
```
Score:     |--------|--------|--------|
           20       50   [cutoff=60]   100

Below cutoff: Control (no treatment)
Above cutoff: Treatment

Causal estimate: Compare outcomes just above vs just below the cutoff
```

#### Analysis
- Local linear regression with bandwidth selection
- Test for manipulation (McCrary density test) at the cutoff
- Sensitivity analysis across different bandwidths

#### Key Threats
| Threat | Likelihood | Notes |
|--------|-----------|-------|
| Manipulation of assignment variable | MEDIUM | Participants gaming the cutoff |
| Functional form misspecification | MEDIUM | Wrong model for the running variable |
| Limited generalizability | HIGH | Causal estimate only valid at the cutoff |
| Bandwidth sensitivity | MEDIUM | Results may change with different bandwidth choices |

### Reporting Standard for All Quasi-Experimental
**TREND Statement** — Transparent Reporting of Evaluations with Nonrandomized Designs. 22-item checklist.

---

## Pattern 5: Single-Subject Designs

### Pattern 5a: ABAB Withdrawal Design

#### When to Use
- Very small N (1-5 participants)
- Treatment effect is expected to be reversible
- Ethical to withdraw treatment temporarily
- Common in clinical psychology, special education, behavior analysis

#### Design Template
```
Phase A1 (Baseline):     Measure behavior without treatment (5+ data points)
Phase B1 (Treatment):    Introduce treatment, continue measurement
Phase A2 (Withdrawal):   Remove treatment, continue measurement
Phase B2 (Re-introduction): Re-introduce treatment, continue measurement

A1 -------- B1 -------- A2 -------- B2 --------
[baseline]  [treatment]  [withdrawal] [treatment]
```

#### Logic of Inference
If behavior improves during B phases and deteriorates during A phases, the treatment is likely responsible. Three demonstrations of effect (B1 vs A1, A2 vs B1, B2 vs A2) strengthen causal inference.

### Pattern 5b: Multiple Baseline Design

#### When to Use
- Treatment effect is irreversible (cannot withdraw)
- Multiple participants, behaviors, or settings available
- Stagger treatment introduction across baselines

#### Design Template
```
Participant 1: A A A | B B B B B B B B
Participant 2: A A A A A | B B B B B B
Participant 3: A A A A A A A | B B B B

| = Treatment introduction (staggered)
```

#### Logic of Inference
If behavior change occurs at each baseline only when treatment is introduced (not before), the treatment is likely responsible. The staggering controls for history and maturation.

### Analysis for Single-Subject Designs
- Visual analysis: level, trend, variability, immediacy of effect, overlap
- Effect size: Percentage of Non-Overlapping Data (PND), Tau-U, between-case standardized mean difference
- Statistical: Randomization tests (if randomized phase onset)

### Reporting Standard
**SCRIBE 2016** — Single-Case Reporting guideline In BEhavioural interventions.

---

## Pattern 6: Correlational Designs

### Pattern 6a: Cross-Sectional Correlational

#### When to Use
- Exploring relationships between variables without manipulation
- All variables measured at a single time point
- Generating hypotheses for future experimental research

#### Design Template
```
Sample (N) --> Measure X1, X2, X3, Y at one time point

Analysis: Pearson/Spearman correlations, multiple regression, SEM
```

### Pattern 6b: Longitudinal Panel Design

#### When to Use
- Temporal ordering of variables is important (does X at T1 predict Y at T2?)
- Ruling out reverse causation
- Studying change over time

#### Design Template
```
T1              T2              T3
Measure X, Y    Measure X, Y    Measure X, Y
N participants   Same N          Same N (with attrition)

Analysis: Cross-lagged panel model, growth curve model, latent difference score
```

### Pattern 6c: SEM / Path Analysis Design

#### When to Use
- Testing a theoretical model with multiple variables and pathways
- Mediation analysis (does X affect Y through M?)
- Confirmatory factor analysis is needed

#### Key Requirement
Large sample: minimum N = 200, or 10 cases per estimated parameter.

### Key Limitations (All Correlational)
| Limitation | Explanation |
|-----------|------------|
| No causal inference | Association does not prove causation |
| Third-variable problem | Unmeasured confounders may explain the relationship |
| Directionality problem | Cannot determine which variable causes which (cross-sectional) |
| Common method variance | Self-report for both X and Y inflates correlation |

### Reporting Standard
**STROBE** — Strengthening the Reporting of Observational Studies in Epidemiology. 22-item checklist.

---

## Pattern 7: Pragmatic / Hybrid Design

### When to Use
- Testing whether an intervention works in real-world practice (effectiveness, not efficacy)
- Combining effectiveness testing with implementation research
- Relaxed inclusion criteria, real-world settings, flexible delivery

### Key Differences from Explanatory Trials

| Dimension | Explanatory (Efficacy) | Pragmatic (Effectiveness) |
|-----------|----------------------|--------------------------|
| Setting | Controlled lab/clinic | Real-world practice |
| Participants | Homogeneous, strict criteria | Heterogeneous, broad criteria |
| Intervention | Standardized, manualized | Flexible, adapted to context |
| Comparator | Placebo or no treatment | Treatment as usual |
| Outcomes | Surrogate or lab measures | Patient-relevant outcomes |
| Analysis | Per-protocol | Intention-to-treat |
| Blinding | Double-blind | Often unblinded |

### PRECIS-2 Tool
Use the PRECIS-2 (Pragmatic Explanatory Continuum Indicator Summary) to score where your trial falls on 9 dimensions, from fully explanatory to fully pragmatic.

### Reporting Standard
**CONSORT extension for pragmatic trials** or **CONSORT-SPI** (for social and psychological interventions).

---

## Quick Reference: Design Selection Summary

| Design | Randomization | N Required | Causal Strength | Key Limitation |
|--------|--------------|-----------|-----------------|----------------|
| RCT (parallel) | Yes | Medium-Large | Strongest | May lack generalizability |
| Factorial | Yes | Large (4x for interaction) | Strong (multiple factors) | Complex interpretation |
| Crossover | Yes | Small-Medium | Strong (within-subject) | Carryover effects |
| Nonequivalent CG | No | Medium | Moderate | Selection bias |
| ITS | No | Many time points needed | Moderate-Strong | History threats |
| RDD | No (cutoff-based) | Large (near cutoff) | Strong (at cutoff) | Local estimate only |
| ABAB | Optional | Very small (1-5) | Moderate | Reversibility required |
| Multiple baseline | Optional | Very small (3+) | Moderate | Staggering required |
| Correlational | No | Medium-Large | Weak (no causation) | No causal claims |
| Pragmatic trial | Yes (often cluster) | Large | Moderate-Strong | Less controlled |
