# Deviation Handling Guide — Types, Documentation, Impact Assessment, and Corrective Actions

## Purpose

Comprehensive reference for handling protocol deviations in research. Covers deviation types (minor, major, critical), documentation requirements, the impact assessment framework for internal, external, and statistical validity, determination of when deviations invalidate results, corrective actions, and Methods section reporting. Used primarily by the deviation_tracker_agent.

---

## Deviation Types

### Overview

A protocol deviation is any departure from the IRB-approved protocol, the pre-registered analysis plan, or the documented experiment design (Schema 10). Deviations range from trivial administrative variations to fundamental design failures.

```
                         Severity Spectrum

  Minor                      Major                      Critical
  |--------------------------|--------------------------|
  Timing shifts              Sample size shortfall      Treatment contamination
  Wording adjustments        Instrument changes         Data loss
  Setting variations         Non-random attrition       IRB violations
  Administrative errors      Method changes             Design invalidation
```

### Minor Deviations — Detailed Classification

Minor deviations are departures that do not substantively affect the study's validity or conclusions. They are documented for completeness but do not require analysis plan changes.

| Sub-Type | Examples | Documentation Required |
|----------|---------|----------------------|
| **Timing deviations** | Data collection session started 30 minutes late; survey window extended by 1 day; follow-up conducted 2 days after the planned date | What changed, original schedule, actual schedule, reason |
| **Wording deviations** | Slight rewording of verbal instructions; clarification question asked by participant addressed informally; typo in instrument discovered and noted | Original wording, actual wording, when discovered |
| **Setting deviations** | Room changed from planned location; online participant used a mobile device instead of desktop; ambient noise level higher than usual | Planned setting, actual setting, potential impact |
| **Administrative deviations** | Consent form version 1.1 used instead of 1.2 (no content change); wrong date written on a paper form; participant ID assigned out of sequence | What happened, correction applied |
| **Format deviations** | Data saved in XLSX instead of planned CSV; figure generated as JPG instead of PNG; file naming convention not followed for one file | Planned format, actual format, whether converted |

**Key characteristic**: If you need to ask "does this really matter?", it is probably minor. Document it anyway.

### Major Deviations — Detailed Classification

Major deviations are substantive departures that could affect the study's validity and require careful consideration, potential analysis plan changes, and explicit Methods section reporting.

| Sub-Type | Examples | Impact Area | Documentation Required |
|----------|---------|-------------|----------------------|
| **Sample size deviations** | Actual N fell below target (e.g., N=180 vs planned N=195); one site recruited significantly more than another; attrition exceeded the buffer | Statistical validity | Original target, actual N, reason for shortfall, post-hoc power calculation |
| **Measurement deviations** | Instrument changed mid-study (e.g., survey platform migrated); scale reliability lower than expected; measurement procedure modified | Construct validity | Original instrument, new instrument, when changed, psychometric comparison |
| **Randomization deviations** | Randomization compromised for a subset (e.g., participants self-selected into groups); block sizes unbalanced; stratification variable miscoded | Internal validity | Original randomization plan, what went wrong, affected participants |
| **Environmental deviations** | Significant external event during data collection (e.g., pandemic, policy change); data collection method changed (in-person to online) | External validity | What changed, when, affected participants/sessions, potential confound |
| **Attrition deviations** | Differential attrition between groups (attrition rate significantly different); attrition pattern non-random (correlated with outcome) | Internal + statistical validity | Attrition rates per group, pattern analysis, comparison of completers vs. non-completers |
| **Timeline deviations** | Data collection period extended significantly (e.g., 8 weeks became 16 weeks); analysis delayed so long that interim results may have influenced later collection | Internal validity | Original timeline, actual timeline, reason, potential for temporal confounds |

**Key characteristic**: These require the researcher to decide whether the deviation undermines the study and what mitigating actions to take.

### Critical Deviations — Detailed Classification

Critical deviations are fundamental departures that may invalidate the study's core conclusions. They require immediate action, potentially including halting the study.

| Sub-Type | Examples | Consequence | Required Action |
|----------|---------|-------------|----------------|
| **Treatment contamination** | Control group exposed to the intervention; treatment group did not receive the full intervention; cross-over occurred without design accommodating it | Causal inference destroyed | STOP. Assess extent. May need to restart or redesign |
| **Data loss** | Primary DV cannot be measured (server crash, instrument failure); substantial data corruption; key variable not recorded | Hypothesis untestable | STOP. Assess recoverability. May need new data collection |
| **Ethical violations** | IRB protocol violated (e.g., consent not obtained, vulnerable population not protected); participant harm occurred; data privacy breach | Ethical and legal liability | STOP immediately. Report to IRB. May need to discard data |
| **Design invalidation** | Fundamental assumption violated (e.g., independence assumption when clustering exists); confound discovered that cannot be controlled; manipulation check shows treatment did not work | Results uninterpretable | STOP. Assess whether redesign can salvage the study |
| **Data integrity** | Evidence of data fabrication or falsification; systematic measurement error discovered; coding error that corrupted all processed data | Results fraudulent or unreliable | STOP. Investigate. May need to retract or discard |

**Key characteristic**: The study cannot continue as planned. A fundamental rethinking is needed.

---

## Documentation Requirements

### Minimum Documentation by Severity

| Field | Minor | Major | Critical |
|-------|-------|-------|----------|
| What changed | Required | Required | Required |
| When discovered | Required | Required | Required |
| Original plan (quote) | Recommended | Required | Required |
| Actual (what happened) | Required | Required | Required |
| Reason | Required | Required | Required |
| Impact assessment (3 validity types) | Brief | Detailed | Detailed |
| Analysis plan update | Not needed | If applicable | Required |
| Corrective action | Not needed | Required | Required |
| Residual risk | Not needed | Required | Required |
| Compound assessment | Not needed | If 2+ deviations | Required |
| PI notification | Not needed | Recommended | Required |
| IRB notification | Not needed | If ethics-related | Required |
| Study halt consideration | Not needed | Not needed | Required |

### Documentation Timing

| Severity | Maximum Acceptable Delay |
|----------|------------------------|
| Minor | End of the workday |
| Major | Within 4 hours of discovery |
| Critical | Immediately (before any further data collection or analysis) |

---

## Impact Assessment Framework

### Internal Validity Assessment

Internal validity is the degree to which the study design allows causal inference (the treatment caused the observed effect, not some confounding factor).

**Assessment questions**:

1. **Confounding**: Does the deviation introduce a variable that co-varies with the IV and could explain the DV?
   - If yes -> at least `moderate` impact
   - If the confound cannot be statistically controlled -> `severe` impact

2. **Selection bias**: Does the deviation differentially affect who is in each group?
   - If groups are no longer comparable at baseline -> `moderate` to `severe`
   - If baseline equivalence can be demonstrated post-hoc -> `minor`

3. **Temporal ordering**: Does the deviation disrupt the IV -> DV causal sequence?
   - If the DV was measured before the IV fully occurred -> `severe`

4. **History / maturation**: Does the deviation introduce time-varying confounds?
   - Extended data collection period with external events -> `moderate`
   - Brief, controlled delay -> `minor` or `none`

### External Validity Assessment

External validity is the degree to which findings generalize beyond the specific study context.

**Assessment questions**:

1. **Population representativeness**: Does the deviation change who is in the sample?
   - Higher attrition in one demographic -> `moderate`
   - Sample now unrepresentative of target population -> `severe`

2. **Setting representativeness**: Does the deviation change the study context?
   - Minor venue change -> `none` or `minor`
   - Switching from in-person to online -> `moderate`

3. **Treatment representativeness**: Does the deviation change what the treatment looks like?
   - Dosage or duration changed -> `moderate`
   - Treatment fundamentally altered -> `severe`

4. **Outcome representativeness**: Does the deviation change what is measured?
   - Measurement timing shifted -> `minor`
   - Entirely different outcome measure -> `severe`

### Statistical Validity Assessment

Statistical validity is the degree to which statistical conclusions are warranted.

**Assessment questions**:

1. **Power**: Does the deviation reduce the effective sample size?
   - Calculate post-hoc power: if power dropped from target (e.g., 0.80) to below 0.70 -> `moderate`
   - If power dropped below 0.50 -> `severe`
   - Formula: use the original effect size with the actual N

2. **Assumption violations**: Does the deviation cause statistical assumptions to be violated?
   - Non-random attrition may violate MCAR assumption -> `moderate`
   - Clustering introduced without multilevel modeling -> `severe`

3. **Type I error inflation**: Does the deviation increase the risk of false positives?
   - Additional unplanned comparisons -> `minor` to `moderate`
   - Outcome switching (testing DV2 because DV1 was non-significant) -> `severe`

4. **Effect size bias**: Does the deviation systematically bias the estimated effect?
   - Differential attrition favoring the treatment group -> `moderate`
   - Regression to the mean not accounted for -> `moderate`

---

## When Deviation Invalidates Results

A deviation **invalidates** the study's primary conclusions when:

1. **The causal claim is untenable**: A confound exists that plausibly explains the observed effect as well as or better than the IV (internal validity = severe)
2. **The hypothesis is untestable**: The primary DV cannot be measured or the primary analysis cannot be conducted (design invalidation)
3. **Statistical conclusions are unreliable**: Power is critically low AND the result is non-significant (underpowered null), or multiple testing was uncontrolled (inflated Type I error)
4. **Data integrity is compromised**: Evidence of fabrication, systematic error, or corruption that cannot be isolated and removed
5. **Ethical violations preclude use**: Data obtained without proper consent or in violation of IRB protocol

**When invalidation is determined**:
1. Document the invalidation finding as a critical deviation
2. Create a decision entry documenting the response (terminate, restart, or salvage)
3. If salvageable: redesign the analysis approach and document as a new decision entry
4. If not salvageable: document the termination, preserve all records, and archive the notebook

---

## Corrective Actions

### By Severity

| Severity | Corrective Action Options |
|----------|--------------------------|
| Minor | Document and continue. No corrective action needed. |
| Major | One or more of: (1) sensitivity analysis to assess impact, (2) statistical control (add covariate), (3) subgroup analysis excluding affected participants, (4) post-hoc power analysis with actual N, (5) robustness check with alternative methods |
| Critical | One or more of: (1) halt data collection, (2) notify PI and IRB, (3) redesign analysis, (4) restart with corrected protocol, (5) terminate study, (6) salvage with fundamentally revised research question |

### Sensitivity Analysis for Major Deviations

When a major deviation occurs, a sensitivity analysis demonstrates whether the deviation affects conclusions:

1. **With/without analysis**: Run the primary analysis with and without the affected data points. If conclusions are the same, the deviation's impact is limited.
2. **Worst-case analysis**: Assume the deviation had the maximum possible impact (e.g., all attrited participants would have had the opposite result). If conclusions still hold, findings are robust.
3. **Alternative method analysis**: Run the analysis using a method that does not rely on the violated assumption. If conclusions converge, the deviation's impact is limited.

Document sensitivity analysis results in an `analysis` entry referencing the `deviation` entry.

---

## Methods Section Reporting

### What to Report

| Severity | Methods Section | Limitations Section |
|----------|----------------|-------------------|
| Minor | Summarize collectively: "Minor scheduling variations occurred but did not affect protocol adherence" | Not required unless accumulated minor deviations are notable |
| Major | Report individually with: what deviated, the impact, and how it was addressed | Discuss as a specific limitation with assessment of how it may affect conclusions |
| Critical | Report prominently in Methods and Limitations; qualify all conclusions | Dedicate a paragraph to the deviation; readers must understand its implications |

### Reporting Template

For major deviations in the Methods section:

```
One protocol deviation occurred during the study. The target sample size was
N = 195 (based on a priori power analysis for d = 0.50, power = 0.80,
alpha = .05); however, actual enrollment was N = 180 due to higher-than-expected
attrition (15 participants withdrew citing schedule conflicts). Post-hoc power
analysis confirmed adequate power (0.82) for the observed effect size (d = 0.51).
A sensitivity analysis comparing results with and without imputation for missing
data yielded consistent conclusions (see Supplementary Materials).
```

For the Limitations section:

```
The study's sample size (N = 180) fell below the pre-registered target (N = 195),
though post-hoc power analysis confirmed adequate power for the observed effect.
Attrition was not entirely random — withdrawals were concentrated in the evening
section — which may limit generalizability to students with schedule constraints.
Sensitivity analyses (worst-case and multiple imputation) did not alter the
pattern of results, suggesting this deviation had minimal impact on conclusions.
```

---

## Compound Deviation Interactions

When multiple deviations co-occur, their combined impact may be greater than the sum of their individual impacts. Common interaction patterns:

| Deviation A | Deviation B | Interaction Effect |
|-------------|-------------|-------------------|
| Reduced sample size | Non-random attrition | Amplified bias: smaller sample + systematic loss = biased smaller sample |
| Instrument change | Environmental change | Confounded: cannot distinguish instrument effect from environment effect |
| Timeline extension | External event | Temporal confound: extended timeline increases exposure to external threats |
| Randomization failure | Differential attrition | Compounded selection bias: groups were unequal at baseline AND lost unequally |

When assessing compound deviations, always consider whether the interaction creates a new threat not captured by either deviation alone.
