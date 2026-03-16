# Instrument Template — Measurement Instrument Format

## Purpose

A fill-in template for documenting measurement instruments (surveys, rubrics, coding schemes) developed by the instrument_builder_agent. Each instrument maps to one or more dependent variables in the experiment protocol. Includes construct definition, item pool, scoring instructions, validity plan, and pilot testing protocol.

## Instructions

1. Complete all sections marked `[Required]` for the instrument type you are building
2. For surveys: complete Sections A-G
3. For rubrics: complete Sections A, B (adapted), C, F, G
4. For coding schemes: complete Sections A, B (adapted), D, F, G
5. Items in `[brackets]` are placeholders — replace with your specific content
6. After completion, the instrument should be ready for expert review (content validity) and pilot testing

---

## A. Construct Definition [Required]

### Construct Information
```
Construct name: [e.g., Academic Self-Efficacy]
Theoretical basis: [Theory/model with citation, e.g., Bandura's Social Cognitive Theory (1997)]
Operational definition: [Precise definition of what this instrument measures]
```

### Dimensionality
```
Structure: [Unidimensional / Multidimensional]

Dimensions (if multidimensional):
1. [Dimension 1]: [Definition — what this sub-dimension captures]
   - Observable indicators: [list of behaviors/attitudes]
2. [Dimension 2]: [Definition]
   - Observable indicators: [list]
3. [Dimension 3]: [Definition]
   - Observable indicators: [list]
```

### Boundary Conditions
```
This construct IS: [What it includes]
This construct is NOT: [What it excludes — discriminant validity boundaries]
Related but distinct constructs: [List with brief explanation of the distinction]
```

### Existing Instruments Reviewed
```
| Instrument | Citation | Items | Alpha | Why Not Used As-Is |
|------------|----------|-------|-------|-------------------|
| [Name] | [Citation] | [N] | [alpha] | [Reason: wrong population / missing dimension / etc.] |
| [Name] | [Citation] | [N] | [alpha] | [Reason] |
```

---

## B. Instrument Specifications [Required]

### Overview
```
Instrument name: [Full name]
Abbreviation: [Short name]
Type: [Likert survey / Frequency survey / Semantic differential / Analytic rubric / Holistic rubric / Coding scheme]
Number of items: [Total] ([N per dimension])
Scale type: [e.g., 5-point Likert]
Scale anchors: [e.g., 1=Strongly Disagree, 2=Disagree, 3=Neutral, 4=Agree, 5=Strongly Agree]
Administration mode: [Paper / Online / Interview / Observation]
Administration time: [Estimated minutes]
Target population: [Description]
Reading level: [Grade level]
Language: [English / Bilingual English-Chinese / etc.]
```

---

## C. Item Pool — Survey/Questionnaire [Required for surveys]

### Instructions to Respondents
```
[Write the exact instructions respondents will see. Example:
"Please read each statement carefully and indicate the extent to which you agree
or disagree. There are no right or wrong answers. Please respond based on how
you actually feel, not how you think you should feel. Rate each item on the
following scale:
1 = Strongly Disagree
2 = Disagree
3 = Neutral
4 = Agree
5 = Strongly Agree"]
```

### Dimension 1: [Name]

| # | Item Text | Reverse | Source |
|---|-----------|---------|--------|
| 1 | [Item text — one idea, no double-barreled, appropriate reading level] | No | [Original / Adapted from Citation] |
| 2 | [Item text] | No | [Source] |
| 3 | [Item text] | Yes | [Source] |
| 4 | [Item text] | No | [Source] |
| 5 | [Item text] | No | [Source] |

### Dimension 2: [Name]

| # | Item Text | Reverse | Source |
|---|-----------|---------|--------|
| 6 | [Item text] | No | [Source] |
| 7 | [Item text] | No | [Source] |
| 8 | [Item text] | Yes | [Source] |
| 9 | [Item text] | No | [Source] |
| 10 | [Item text] | No | [Source] |

### Dimension 3: [Name]

| # | Item Text | Reverse | Source |
|---|-----------|---------|--------|
| 11 | [Item text] | No | [Source] |
| 12 | [Item text] | No | [Source] |
| 13 | [Item text] | Yes | [Source] |
| 14 | [Item text] | No | [Source] |
| 15 | [Item text] | No | [Source] |

### Item Quality Checklist Summary
```
Total items: [N]
Positively worded: [N] ([%])
Reverse-coded: [N] ([%]) — Target: 20-30%
Items per dimension: [list, e.g., Dim1: 5, Dim2: 5, Dim3: 5]
Reading level verified: [Yes / No — method used]
Double-barreled items: [0 — confirmed none]
```

---

## C-alt. Rubric Items [Required for rubrics]

### Analytic Rubric

```
Task being assessed: [Description of the performance task]
Number of dimensions: [N]
Rating scale: [Number of levels, e.g., 4-point: 1=Beginning to 4=Exemplary]
```

| Dimension | Weight | 4 (Exemplary) | 3 (Proficient) | 2 (Developing) | 1 (Beginning) |
|-----------|--------|---------------|-----------------|-----------------|----------------|
| [Dim 1] | [%] | [Observable behaviors/qualities at this level] | [Descriptors] | [Descriptors] | [Descriptors] |
| [Dim 2] | [%] | [Descriptors] | [Descriptors] | [Descriptors] | [Descriptors] |
| [Dim 3] | [%] | [Descriptors] | [Descriptors] | [Descriptors] | [Descriptors] |
| [Dim 4] | [%] | [Descriptors] | [Descriptors] | [Descriptors] | [Descriptors] |

### OR Holistic Rubric

| Score | Descriptor |
|-------|-----------|
| 5 | [Complete description of performance at this level using observable indicators] |
| 4 | [Description] |
| 3 | [Description] |
| 2 | [Description] |
| 1 | [Description] |

---

## D. Coding Scheme [Required for coding schemes]

### Codebook

```
Unit of analysis: [Sentence / Paragraph / Speaking turn / Episode / Document]
Coding approach: [Deductive (theory-driven) / Inductive (data-driven) / Hybrid]
Mutual exclusivity: [Codes are mutually exclusive / Codes can co-occur]
Exhaustiveness: [All units must be coded / "Other" category included]
```

| Code | Label | Definition | Inclusion Criteria | Exclusion Criteria | Example |
|------|-------|-----------|-------------------|-------------------|---------|
| C01 | [Label] | [Precise definition] | [What counts] | [What does NOT count] | [Verbatim example from pilot data] |
| C02 | [Label] | [Precise definition] | [What counts] | [What does NOT count] | [Example] |
| C03 | [Label] | [Precise definition] | [What counts] | [What does NOT count] | [Example] |
| C04 | [Label] | [Precise definition] | [What counts] | [What does NOT count] | [Example] |
| C99 | Other | Units that do not fit any other code | [Residual] | [N/A] | [Example] |

### Coding Decision Rules
```
1. When a unit could fit multiple codes: [Apply the most specific code / Apply all applicable codes / etc.]
2. When a unit is ambiguous: [Code as "Other" and flag for discussion / Apply the first matching code]
3. Minimum evidence threshold: [A code requires at least X indicators to be assigned]
```

### Coder Training Protocol
```
Phase 1: Introduction (2 hours)
- Review codebook definitions and examples
- Practice coding 3-5 units together with trainer

Phase 2: Independent Practice (2-4 hours)
- Code [N] units independently
- Compare with gold standard
- Discuss disagreements

Phase 3: Calibration (1-2 hours)
- Resolve systematic disagreements
- Revise codebook if needed
- Code additional [N] units

Phase 4: Reliability Assessment
- Code [20%] of total dataset independently (both coders)
- Calculate Cohen's kappa (target >= 0.60)
- If kappa < 0.60: return to Phase 2
```

---

## E. Scoring Instructions [Required]

### Reverse Scoring
```
Items requiring reverse scoring: [list item numbers]
Reverse scoring formula: [New score = (max + 1) - original score]
Example: For a 5-point scale, reverse score = 6 - original score
```

### Dimension Scores
```
Dimension 1 ([Name]): [Sum / Mean] of items [list item numbers]
  Range: [min] to [max]

Dimension 2 ([Name]): [Sum / Mean] of items [list item numbers]
  Range: [min] to [max]

Dimension 3 ([Name]): [Sum / Mean] of items [list item numbers]
  Range: [min] to [max]
```

### Total Score
```
Calculation: [Sum of dimension scores / Weighted sum / Mean of all items]
Formula: Total = [formula]
Range: [min] to [max]
```

### Score Interpretation
```
| Score Range | Interpretation |
|-------------|---------------|
| [range] | [High — description] |
| [range] | [Moderate — description] |
| [range] | [Low — description] |

Note: Cut-off scores should only be established after normative data is collected.
These ranges are preliminary interpretive guidelines.
```

### Missing Data Rules
```
Per-dimension: If > [X]% of items in a dimension are missing, do not compute dimension score
Overall: If > [X]% of total items are missing, exclude the case
Imputation: [None / Item-level mean imputation if < X% missing per dimension]
```

---

## F. Validity Plan [Required]

### Content Validity
```
Method: Expert panel review
Panel size: [3-5] subject matter experts
Expert qualifications: [Describe required expertise]
Review procedure:
1. Experts independently rate each item's relevance (1-4 scale)
2. Calculate Item-level CVI (I-CVI) — retain items with I-CVI >= 0.78
3. Calculate Scale-level CVI (S-CVI/Ave) — target >= 0.90
4. Experts review dimension assignments — confirm each item maps correctly
Timeline: [weeks]
```

### Construct Validity (planned for validation study)
```
Convergent validity:
- Correlate with: [Instrument name] (expected r >= 0.50)
- Rationale: [Why these constructs should be related]

Discriminant validity:
- Correlate with: [Instrument name] (expected r < 0.30)
- Rationale: [Why these constructs should NOT be related]

Factor analysis:
- Method: Confirmatory Factor Analysis (CFA)
- Expected model: [N-factor model]
- Fit criteria: CFI > 0.95, TLI > 0.95, RMSEA < 0.06, SRMR < 0.08
- Minimum N: [200 or 10 per item, whichever is larger]
```

### Criterion Validity (planned for validation study) [If applicable]
```
Concurrent validity:
- Gold standard measure: [Name]
- Expected correlation: [r >= value]

Predictive validity:
- Outcome: [Future outcome the construct should predict]
- Expected relationship: [Direction and approximate strength]
- Timeline: [How long between measurement and outcome]
```

---

## G. Pilot Testing Plan [Required]

### Phase 1: Cognitive Pretesting
```
N: [5-10] participants from target population
Method: Think-aloud protocol
Focus: Item comprehension, response process, time burden
Expected duration: [30-60] minutes per participant
Revisions: Items flagged by 2+ participants will be revised
Timeline: [weeks]
```

### Phase 2: Small-Scale Pilot
```
N: [30-50] participants from target population
Method: Standard administration
Analyses:
- Descriptive statistics per item (M, SD, skewness)
  * Flag items with floor effects (> 80% at minimum) or ceiling effects (> 80% at maximum)
  * Flag items with skewness > |2.0|
- Item-total correlations
  * Remove items with r < 0.30
- Cronbach's alpha per dimension
  * Target: alpha >= 0.70
- Alpha-if-item-deleted
  * Flag items whose removal would increase alpha by > 0.02
Timeline: [weeks]
```

### Phase 3: Validation Study
```
N: [200+] (or [10 per item], whichever is larger)
Method: Full administration with convergent/discriminant measures
Analyses:
- CFA to test factor structure
- Convergent and discriminant validity correlations
- Test-retest reliability (subset of N=[50], 2-week interval)
- Final item selection based on CFA loadings (retain items with lambda >= 0.40)
Timeline: [weeks]
```

---

## Pre-Submission Checklist

- [ ] Construct is precisely defined with theoretical basis
- [ ] Existing instruments have been reviewed and justified why not reused
- [ ] All items follow item writing rules (no double-barreled, no double negatives, etc.)
- [ ] Reverse-coded items present at 20-30% rate
- [ ] Scoring instructions are unambiguous
- [ ] Content validity plan specifies expert panel and CVI thresholds
- [ ] Reliability targets are specified (alpha >= 0.70 minimum)
- [ ] Pilot testing is planned in phases (cognitive pretest -> pilot -> validation)
- [ ] Missing data rules are specified
- [ ] Reading level is appropriate for target population
- [ ] Administration time is estimated
- [ ] For rubrics: all descriptors use observable behaviors (not vague quality terms)
- [ ] For coding schemes: codebook includes inclusion/exclusion criteria and examples
