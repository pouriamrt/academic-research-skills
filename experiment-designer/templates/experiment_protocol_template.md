# Experiment Protocol Template — SPIRIT-Aligned Full Protocol

## Purpose

A comprehensive fill-in protocol template aligned with SPIRIT 2013 (Standard Protocol Items: Recommendations for Interventional Trials). This template maps directly to Schema 10 (Experiment Design) from `shared/handoff_schemas.md`. Applicable to RCTs, factorial, crossover, quasi-experimental, and single-subject designs with minor adaptations.

## Instructions

1. Complete all sections marked `[Required]`. Sections marked `[If applicable]` should be completed when relevant to your design.
2. Items in `[brackets]` are placeholders — replace with your specific content.
3. After completion, the protocol_compiler_agent will cross-validate all sections for internal consistency.
4. For quasi-experimental designs, skip randomization sections and document the rationale.
5. For single-subject designs, adapt the sample section to describe the individual participant(s).

---

## 1. Administrative Information [Required]

### 1.1 Study Title
```
[Descriptive title including design type, population, intervention, and primary outcome]
```

### 1.2 Protocol Version and Date
```
Version: [1.0]
Date: [YYYY-MM-DD]
Protocol ID: [EXP-YYYYMMDD-NNN]
```

### 1.3 Investigators
| Name | Institution | Role | Email | ORCID |
|------|-------------|------|-------|-------|
| [Name] | [Institution] | [PI / Co-PI / Statistician / RA] | [Email] | [ORCID] |
| [Name] | [Institution] | [Role] | [Email] | [ORCID] |

### 1.4 Funding
```
Funding source: [Agency / Grant number / Self-funded / None]
Role of funder: [No role in design / Provided input on design / Unfunded]
Conflicts of interest: [None / Describe]
```

---

## 2. Introduction [Required]

### 2.1 Background and Rationale
```
[2-3 paragraphs summarizing:
- The problem or gap in knowledge
- What previous research has shown (cite key studies)
- Why this experiment is needed
- What this study will add to existing knowledge]
```

### 2.2 Research Question(s)
```
Primary RQ: [State the primary research question in interrogative form]
Secondary RQ: [If applicable]
```

### 2.3 Hypotheses
```
H1 (primary, [positive/negative/non-directional]):
[State the hypothesis in declarative form with expected direction]

H2 (secondary, [direction]):
[State hypothesis if applicable]

H3 (exploratory):
[State exploratory hypothesis if applicable]
```

---

## 3. Study Design [Required]

### 3.1 Design Type
```
Design: [RCT / 2x2 factorial / crossover / nonequivalent control group / ITS / ABAB / correlational / etc.]
Classification: [Between-subjects / Within-subjects / Mixed]
```

### 3.2 Design Diagram
```
[Draw the design structure using R, O, X notation or appropriate diagram]

Example (RCT):
R  O1  X   O2  (Treatment)
R  O1      O2  (Control)

Example (2x2 factorial):
         Factor B: Low    Factor B: High
Factor A: Low    Cell 1         Cell 2
Factor A: High   Cell 3         Cell 4
```

### 3.3 Design Justification
```
[Explain why this design was chosen over alternatives. Address:
- Why this design best answers the RQ
- What designs were considered and rejected, with reasons
- Key trade-offs (internal vs external validity)]
```

### 3.4 Reporting Standard
```
Applicable guideline: [SPIRIT 2013 / CONSORT 2010 / TREND / STROBE / SCRIBE / Other]
Checklist status: [Completed / In progress]
```

---

## 4. Participants [Required]

### 4.1 Eligibility Criteria
```
Inclusion criteria:
1. [Criterion 1]
2. [Criterion 2]
3. [Criterion 3]

Exclusion criteria:
1. [Criterion 1]
2. [Criterion 2]
```

### 4.2 Recruitment
```
Setting: [University / Clinic / Online / Community / etc.]
Recruitment method: [Flyers / Email / Course credit / Snowball / etc.]
Recruitment period: [Start date] to [End date]
Incentives: [Payment / Course credit / None / Describe]
```

### 4.3 Informed Consent
```
Consent process: [Written / Verbal / Online / Waived (with justification)]
Key disclosures: [Risks, benefits, voluntary participation, right to withdraw]
Special populations: [Minors / Vulnerable groups / None]
```

---

## 5. Variables [Required]

### 5.1 Independent Variable(s)
```
IV1: [Name]
- Type: [Categorical / Continuous / Ordinal / Binary]
- Levels: [Level 1 / Level 2 / Level 3]
- Operationalization: [How it is manipulated or defined]
- Manipulation check: [How you verify the manipulation worked]

IV2: [If applicable, same format]
```

### 5.2 Dependent Variable(s)
```
DV1 (primary): [Name]
- Type: [Continuous / Categorical / Ordinal / Binary]
- Measurement instrument: [Name of instrument]
- Operationalization: [How it is measured — specific scores, scales, units]
- Measurement timing: [Pre / Post / Multiple time points]

DV2 (secondary): [If applicable, same format]
```

### 5.3 Control Variables
```
Control 1: [Name] — Measured by: [method] — Rationale: [why it needs controlling]
Control 2: [Name] — Measured by: [method] — Rationale: [why]
```

### 5.4 Covariates
```
Covariate 1: [Name] — Type: [type] — Role: [statistical control / stratification variable]
Covariate 2: [If applicable]
```

### 5.5 Potential Moderators [If applicable]
```
Moderator: [Name] — Hypothesis: [How it might modify the treatment effect]
```

### 5.6 Potential Mediators [If applicable]
```
Mediator: [Name] — Hypothesis: [Proposed mechanism]
```

---

## 6. Sample Size and Power [Required]

### 6.1 Power Analysis Parameters
```
Statistical test: [e.g., independent t-test, two-way ANOVA]
Effect size: [value and metric] — Source: [prior study / meta-analysis / SESOI / pilot]
Alpha: [0.05]
Desired power: [0.80]
Tails: [Two-tailed / One-tailed with justification]
Additional parameters: [Number of groups, levels, ICC, correlation, etc.]
```

### 6.2 Sample Size Result
```
Required N per group: [value]
Total required N: [value]
Attrition buffer: [%]
Adjusted total N (recruitment target): [value]
Design effect: [if cluster design, value and ICC]
```

### 6.3 Sensitivity Analysis
```
| Available N per group | Minimum detectable effect size | Magnitude |
|-----------------------|-------------------------------|-----------|
| [N1] | [metric] = [value] | [small/medium/large] |
| [N2] | [metric] = [value] | [small/medium/large] |
| [N3] | [metric] = [value] | [small/medium/large] |
```

### 6.4 Stopping Rule
```
- [ ] Stop when target N is reached
- [ ] Stop at deadline: [date]
- [ ] Interim analysis at N = [value] (specify decision rules)
- [ ] Other: [describe]
```

---

## 7. Randomization [If applicable — skip for quasi-experimental/correlational]

### 7.1 Method
```
Randomization type: [Simple / Block / Stratified block / Cluster / Adaptive]
Allocation ratio: [1:1 / 2:1 / Other]
Block size: [Fixed: N / Varying: N1, N2, N3]
Stratification variables: [Variable 1 (levels), Variable 2 (levels)]
```

### 7.2 Sequence Generation
```
Method: numpy.random.Generator (PCG64)
Seed: [integer]
NumPy version: [version]
Date generated: [YYYY-MM-DD]
Code: [reference to appendix or inline]
```

### 7.3 Allocation Concealment
```
Method: [Central allocation / Sealed envelopes / Computer system / Other]
Details: [How concealment is maintained until enrollment]
```

### 7.4 Blinding [If applicable]
```
Blinding level: [No blinding / Single-blind / Double-blind / Triple-blind]
Who is blinded: [Participants / Investigators / Outcome assessors / Data analysts]
Blinding maintenance: [How blinding is preserved]
Unblinding criteria: [When/how blinding will be broken]
```

---

## 8. Measurement Instruments [Required]

### 8.1 Instrument 1: [Name]
```
Construct measured: [construct name]
DV mapped to: [DV1 / DV2]
Type: [Likert survey / Semantic differential / Rubric / Coding scheme / Behavioral measure / Physiological measure]
Number of items: [N]
Scale: [e.g., 5-point Likert: 1=Strongly Disagree to 5=Strongly Agree]
Scoring: [Sum / Mean / Factor score]
Reverse-coded items: [item numbers]
Administration time: [minutes]
Existing validation: [cite validation studies]
Reliability evidence: [Cronbach's alpha = X from Study Y]
Pilot plan: [Phase 1: cognitive pretest N=5-10 / Phase 2: pilot N=30-50]
Full instrument: [See Appendix A]
```

### 8.2 Instrument 2: [Name]
```
[Same format as 8.1]
```

---

## 9. Procedures [Required]

### 9.1 Step-by-Step Protocol
```
Step 1: [Recruitment and screening — description, duration]
Step 2: [Informed consent — description, duration]
Step 3: [Baseline measurement (pretest) — instruments, duration]
Step 4: [Randomization (if applicable) — method, timing]
Step 5: [Intervention delivery — description, duration, frequency]
Step 6: [Post-test measurement — instruments, duration, timing]
Step 7: [Follow-up (if applicable) — timing, instruments]
Step 8: [Debriefing — description]
```

### 9.2 Intervention Description (Treatment Group)
```
Content: [What the intervention involves]
Dose: [Frequency, duration, intensity]
Delivery: [Who delivers, training required]
Materials: [Required materials, software, equipment]
Fidelity monitoring: [How adherence to protocol is ensured]
```

### 9.3 Control Condition
```
Type: [No treatment / Treatment as usual / Active control / Waitlist / Placebo]
Description: [What control participants experience]
Justification: [Why this control was chosen]
```

### 9.4 Fidelity Monitoring
```
Method: [Observation checklist / Audio recording / Self-report / None]
Frequency: [Every session / Random 20% of sessions / etc.]
Threshold: [Minimum fidelity percentage to retain data, e.g., 80%]
```

---

## 10. Analysis Plan [Required]

### 10.1 Primary Analysis
```
Hypothesis tested: [H1]
Statistical test: [e.g., independent samples t-test]
IV: [variable name]
DV: [variable name]
Covariates: [if any]
Software: [R / Python / SPSS / Stata]
Model specification: [e.g., DV ~ IV + covariate1 + covariate2]
```

### 10.2 Secondary Analysis
```
Hypothesis tested: [H2]
[Same format as primary]
```

### 10.3 Exploratory Analysis
```
[Description of planned exploratory analyses — clearly labeled as exploratory]
```

### 10.4 Assumption Checking
```
| Assumption | Test | Action if Violated |
|------------|------|--------------------|
| Normality | Shapiro-Wilk + Q-Q plot | Use non-parametric alternative or bootstrap |
| Homogeneity of variance | Levene's test | Use Welch's correction |
| Independence | Design-based | [N/A for between-subjects / Address for repeated measures] |
| Sphericity (if RM) | Mauchly's test | Greenhouse-Geisser correction |
```

### 10.5 Missing Data Strategy
```
Prevention: [How missing data is minimized]
Assessment: [How missingness pattern is evaluated — MCAR/MAR/MNAR]
Handling: [Listwise deletion / Multiple imputation / Full information ML / Other]
Sensitivity analysis: [Compare results across missing data methods]
```

### 10.6 Multiple Comparison Correction
```
Number of primary tests: [N]
Correction method: [Bonferroni / Holm / Benjamini-Hochberg FDR / None — justify]
Adjusted alpha: [value]
```

### 10.7 Effect Size Reporting
```
Primary effect size: [Cohen's d / eta-squared / R-squared / Other]
Confidence intervals: [95% CI for all effect sizes]
Interpretation benchmark: [Cohen's conventions / field-specific norms]
```

---

## 11. Threats to Validity [Required]

```
[Use the threats_to_validity_template.md for the complete matrix]

| Category | Threat | Likelihood | Mitigation | Residual Risk |
|----------|--------|-----------|------------|---------------|
| Internal | [threat] | [H/M/L] | [strategy] | [remaining risk] |
| Internal | [threat] | [H/M/L] | [strategy] | [remaining risk] |
| External | [threat] | [H/M/L] | [strategy] | [remaining risk] |
| Construct | [threat] | [H/M/L] | [strategy] | [remaining risk] |
| Statistical | [threat] | [H/M/L] | [strategy] | [remaining risk] |
```

---

## 12. Ethical Considerations [Required]

### 12.1 IRB Review
```
Review level: [Exempt / Expedited / Full Board]
IRB institution: [name]
Application status: [Not yet submitted / Under review / Approved]
Approval number: [if approved]
```

### 12.2 Risk-Benefit Assessment
```
Risks to participants: [Describe potential risks — physical, psychological, social, economic]
Risk level: [Minimal / Greater than minimal]
Benefits: [Direct benefits to participants / Indirect benefits to society]
Risk minimization: [How risks are reduced]
```

### 12.3 Data Management
```
Data storage: [Encrypted drive / Institutional server / Cloud with encryption]
Access control: [Who can access data, how access is restricted]
De-identification: [Method of de-identifying data]
Retention period: [How long data will be stored]
Destruction plan: [How data will be destroyed after retention period]
```

### 12.4 AI Disclosure
```
AI tools used in design: [experiment-designer skill / Other]
AI role: [Study design assistance, power analysis computation, instrument review]
Human oversight: [All AI outputs were reviewed and validated by the research team]
```

---

## 13. Timeline [Required]

```
| Phase | Activity | Start | End | Duration | Responsible |
|-------|----------|-------|-----|----------|-------------|
| 0 | IRB submission and approval | [date] | [date] | [weeks] | [PI] |
| 1 | Instrument pilot testing | [date] | [date] | [weeks] | [RA] |
| 2 | Recruitment | [date] | [date] | [weeks] | [RA] |
| 3 | Baseline measurement | [date] | [date] | [weeks] | [RA] |
| 4 | Intervention delivery | [date] | [date] | [weeks] | [PI/RA] |
| 5 | Post-test measurement | [date] | [date] | [weeks] | [RA] |
| 6 | Data analysis | [date] | [date] | [weeks] | [Statistician] |
| 7 | Report writing | [date] | [date] | [weeks] | [PI] |
```

---

## 14. References

```
[APA 7.0 formatted reference list — include references cited in Background, instrument validation studies, and methodological references]
```

---

## 15. Appendices

### Appendix A: Full Instrument Text
```
[Complete instrument(s) as developed by instrument_builder_agent]
```

### Appendix B: Randomization Code
```python
[Complete reproducible randomization code with seed]
```

### Appendix C: Power Analysis Code and Figures
```python
[Complete power analysis code with output]
```

### Appendix D: Consent Form Template
```
[Institutional consent form adapted for this study]
```

---

## Pre-Submission Checklist

- [ ] All [Required] sections are complete
- [ ] Design type matches the research question
- [ ] Hypotheses are stated with direction
- [ ] Power analysis justifies the sample size
- [ ] Effect size source is documented (not just "convention")
- [ ] All DVs have corresponding measurement instruments
- [ ] Randomization method and seed are documented (if applicable)
- [ ] Analysis plan matches design and hypotheses
- [ ] Threats to validity are assessed with mitigations
- [ ] IRB review level is determined
- [ ] Timeline is realistic with all phases included
- [ ] AI disclosure is included
- [ ] Reporting guideline (SPIRIT/CONSORT/TREND/STROBE) is referenced
- [ ] Schema 10 artifact is complete and internally consistent
- [ ] Material Passport (Schema 9) is attached
