# Instrument Development Guide — Item Writing, Validity, Reliability, and Pilot Testing

## Purpose

A comprehensive reference for developing measurement instruments (surveys, rubrics, coding schemes). Covers item writing rules, scale types, validity frameworks, reliability methods, pilot testing protocols, and rubric/coding scheme development. Used by the instrument_builder_agent.

---

## Item Writing Rules

### The 15 Cardinal Rules

1. **One idea per item**: Never combine two concepts in a single item.
   - Bad: "I enjoy math and feel confident solving problems"
   - Good: "I enjoy math" (separate item: "I feel confident solving math problems")

2. **No double negatives**: They confuse respondents and reduce reliability.
   - Bad: "I do not disagree that the policy is ineffective"
   - Good: "I believe the policy is effective" (reverse-coded if needed)

3. **No leading questions**: Do not signal the desired response.
   - Bad: "Don't you agree that class sizes should be reduced?"
   - Good: "Class sizes at my institution are appropriate"

4. **No absolutes**: Words like "always", "never", "all", "none" invite disagreement.
   - Bad: "I always complete my homework on time"
   - Good: "I usually complete my homework on time"

5. **Specific timeframes**: Anchor items to a concrete period.
   - Bad: "I exercise regularly"
   - Good: "In the past 7 days, I exercised at least 3 times"

6. **Simple vocabulary**: Match the reading level of the target population.
   - Bad: "I find the pedagogical approach ameliorative"
   - Good: "I find the teaching approach helpful"

7. **Short items**: Aim for 10-20 words per item. Longer items reduce comprehension.

8. **Avoid assumptions**: Do not presuppose an experience or circumstance.
   - Bad: "How satisfied are you with your thesis advisor?" (assumes they have one)
   - Good: Include a filter question first: "Do you have a thesis advisor? [Yes/No]"

9. **Parallel grammar with scale anchors**: If the scale says "Strongly Agree", items should be statements, not questions.
   - Bad: "How much do you enjoy reading?" (with Agree/Disagree scale)
   - Good: "I enjoy reading" (with Agree/Disagree scale)

10. **One dimension per item set**: Group items measuring the same dimension together (or randomize for research purposes).

11. **Include reverse-coded items**: 20-30% of items should be negatively worded to detect acquiescence bias.
    - Forward: "I feel confident in my abilities"
    - Reverse: "I doubt my abilities" (reverse scored)

12. **Avoid "and/or" constructions**: They create ambiguity about what is being endorsed.

13. **Avoid hypothetical items**: "If you were a teacher, how would you..." is harder to answer reliably.

14. **Avoid prestige bias**: Do not reference prestigious sources to bias responses.
    - Bad: "Leading experts recommend X. Do you agree?"
    - Good: "X is a good approach"

15. **Ensure cultural appropriateness**: Avoid idioms, cultural references, or lifestyle assumptions that are specific to one culture or demographic.

---

## Scale Types

### Likert-Type Scales (Agreement)

| Points | Labels | Best For | Trade-off |
|--------|--------|----------|-----------|
| 4-point | SD / D / A / SA | Forced choice (no neutral) | Loses nuance |
| 5-point | SD / D / N / A / SA | General purpose | Most common; good balance |
| 6-point | SD / D / SliD / SliA / A / SA | Forced choice with granularity | Unusual; may confuse |
| 7-point | SD / D / SliD / N / SliA / A / SA | Maximum discrimination | Best for research |

**Recommendation**: 5-point for practical/applied instruments. 7-point for research instruments where maximum sensitivity is needed.

**Labeled endpoints vs fully labeled**: Fully labeling every point improves reliability slightly but requires more cognitive effort. At minimum, label the endpoints and midpoint.

### Frequency Scales

```
Type A (Verbal):
1 = Never, 2 = Rarely, 3 = Sometimes, 4 = Often, 5 = Always

Type B (Numeric):
1 = 0 times per week, 2 = 1-2 times, 3 = 3-4 times, 4 = 5-6 times, 5 = Daily

Type C (Percentage):
1 = 0% of the time, 2 = 25%, 3 = 50%, 4 = 75%, 5 = 100%
```

**Best practice**: Use numeric anchors (Type B) when precision matters. Verbal anchors (Type A) are more intuitive but less precise.

### Semantic Differential

Bipolar adjective pairs with a numerical scale between them:

```
Boring    1---2---3---4---5---6---7    Interesting
Easy      1---2---3---4---5---6---7    Difficult
Useless   1---2---3---4---5---6---7    Useful
Passive   1---2---3---4---5---6---7    Active
```

**Best for**: Measuring attitudes toward a specific object, concept, or stimulus. Based on Osgood's semantic space (evaluation, potency, activity dimensions).

### Visual Analog Scale (VAS)

```
No pain at all |________________________________| Worst pain imaginable
               0                                 100
```

**Best for**: Continuous subjective experiences (pain, satisfaction, mood, anxiety). Scored as the distance from the left anchor (0-100mm).

**Advantage**: True continuous data (not ordinal like Likert).
**Disadvantage**: Harder to administer on paper; requires ruler for scoring. Digital versions solve this.

### Forced Choice (Ipsative)

```
For each pair, select the statement that best describes you:
(a) I prefer to work independently  OR  (b) I prefer to work in teams
```

**Best for**: Reducing social desirability bias. Respondents must choose between equally desirable options.
**Limitation**: Ipsative data cannot be compared between individuals using standard statistics. Requires specialized analysis.

---

## Validity Framework

### Content Validity

**Definition**: The degree to which the instrument items adequately sample the domain of the construct.

**Method**: Expert panel review (NOT statistical — this is a judgment-based assessment).

**Procedure**:
1. Define the construct domain (dimensions, boundaries)
2. Recruit 3-5 subject matter experts
3. Each expert independently rates each item on relevance (1-4 scale):
   - 1 = Not relevant
   - 2 = Somewhat relevant (needs major revision)
   - 3 = Relevant (needs minor revision)
   - 4 = Highly relevant
4. Calculate Item-level CVI (I-CVI): proportion of experts rating 3 or 4
   - **Threshold**: I-CVI >= 0.78 (for 3-5 experts)
5. Calculate Scale-level CVI (S-CVI/Ave): mean of all I-CVIs
   - **Threshold**: S-CVI/Ave >= 0.90
6. Have experts verify item-to-dimension mapping

### Construct Validity

**Definition**: The degree to which the instrument measures the theoretical construct it claims to measure.

**Sub-types**:

| Type | Method | Evidence |
|------|--------|---------|
| Convergent | Correlate with measures of similar constructs | r >= 0.50 with related instrument |
| Discriminant | Correlate with measures of unrelated constructs | r < 0.30 with unrelated instrument |
| Factorial | Confirmatory Factor Analysis (CFA) | CFI > 0.95, RMSEA < 0.06, SRMR < 0.08 |
| Known-groups | Compare scores across groups known to differ | Significant difference in expected direction |

**CFA Model Fit Criteria**:

| Index | Acceptable | Good | Interpretation |
|-------|-----------|------|----------------|
| CFI (Comparative Fit Index) | > 0.90 | > 0.95 | Higher is better |
| TLI (Tucker-Lewis Index) | > 0.90 | > 0.95 | Higher is better |
| RMSEA (Root Mean Square Error of Approximation) | < 0.08 | < 0.06 | Lower is better |
| SRMR (Standardized Root Mean Square Residual) | < 0.10 | < 0.08 | Lower is better |
| Chi-square/df | < 3.0 | < 2.0 | Lower is better (sensitive to N) |

**Minimum sample for CFA**: N >= 200, or 10 cases per estimated parameter, whichever is larger.

### Criterion Validity

**Definition**: The degree to which the instrument predicts an external criterion.

| Type | Design | Timing |
|------|--------|--------|
| Concurrent | Correlate instrument with criterion measured at the same time | Same session |
| Predictive | Correlate instrument with criterion measured in the future | T1 -> T2 |

**Example**: A new academic motivation scale (T1) should predict semester GPA (T2, 4 months later).

### Face Validity

**Definition**: Whether the instrument appears to measure what it claims (subjective judgment by respondents).

**Note**: Face validity is NOT a formal psychometric property. However, poor face validity can reduce response rates and participant engagement.

---

## Reliability Framework

### Internal Consistency

**Cronbach's Alpha** (alpha):

| alpha Range | Interpretation | Action |
|-------------|---------------|--------|
| < 0.50 | Unacceptable | Redesign the scale |
| 0.50 - 0.60 | Poor | Review items; remove those with item-total r < 0.30 |
| 0.60 - 0.70 | Questionable | Acceptable for exploratory research only |
| 0.70 - 0.80 | Acceptable | Adequate for group-level comparisons |
| 0.80 - 0.90 | Good | Suitable for most research purposes |
| > 0.90 | Excellent (check for redundancy) | May indicate item redundancy; consider shortening |

**McDonald's Omega** (omega): Preferred over alpha when items have unequal factor loadings (which is almost always the case). Uses CFA-based composite reliability.

**Rule**: Report both alpha and omega. If they differ substantially (> 0.05), note the discrepancy and prefer omega.

### Test-Retest Reliability

**Method**: Administer the same instrument to the same participants twice, 2-4 weeks apart.

**Metric**: Intraclass Correlation Coefficient (ICC)

| ICC Model | When to Use |
|-----------|------------|
| ICC(2,1) — two-way random, single measures | Single rater, raters are random sample |
| ICC(3,1) — two-way mixed, single measures | Single rater, raters are fixed |
| ICC(2,k) — two-way random, average measures | Average of k raters, raters are random |

**Interpretation**:

| ICC | Interpretation |
|-----|---------------|
| < 0.50 | Poor |
| 0.50 - 0.75 | Moderate |
| 0.75 - 0.90 | Good |
| > 0.90 | Excellent |

**Timing**: Too short (< 1 week) -> memory effects inflate reliability. Too long (> 6 weeks) -> true change reduces apparent reliability.

### Inter-Rater Reliability

**Cohen's Kappa** (for 2 raters, categorical codes):

| Kappa | Interpretation |
|-------|---------------|
| < 0.00 | Less than chance |
| 0.01 - 0.20 | Slight |
| 0.21 - 0.40 | Fair |
| 0.41 - 0.60 | Moderate |
| 0.61 - 0.80 | Substantial |
| 0.81 - 1.00 | Almost perfect |

**Threshold**: kappa >= 0.60 for research; kappa >= 0.80 for high-stakes coding.

**Weighted Kappa**: For ordinal categories (e.g., rubric scores), use weighted kappa (linear or quadratic weights).

**ICC for Continuous Ratings**: When multiple raters provide continuous scores (e.g., rubric dimension scores), use ICC instead of kappa.

### Fleiss' Kappa (for 3+ raters, categorical)

Extension of Cohen's kappa for multiple raters. Same interpretation thresholds.

---

## Pilot Testing Protocol

### Phase 1: Cognitive Pretesting (N = 5-10)

**Purpose**: Ensure items are understood as intended.

**Method**: Think-aloud protocol

**Procedure**:
1. Recruit 5-10 participants from the target population
2. Ask them to complete the instrument while verbalizing their thought process
3. After each item, probe:
   - "What did this question mean to you?"
   - "Was anything confusing?"
   - "How did you decide on your answer?"
   - "Can you put this in your own words?"
4. Take notes on confusion, misinterpretation, or unexpected interpretations
5. Revise problematic items

**Decision rules**:
- If 2+ participants misinterpret an item -> revise the item
- If 3+ participants find the instructions unclear -> revise instructions
- If completion time > 150% of target -> shorten the instrument

### Phase 2: Small-Scale Pilot (N = 30-50)

**Purpose**: Identify problematic items statistically.

**Analyses**:

1. **Descriptive statistics per item**:
   - Mean, SD, skewness, kurtosis
   - Flag: items with M < 1.5 or M > 4.5 (on 5-point scale) — floor/ceiling effect
   - Flag: items with SD < 0.50 — insufficient variability
   - Flag: items with |skewness| > 2.0 — non-normal distribution

2. **Item-total correlations**:
   - Corrected item-total correlation (correlation of item with sum of remaining items)
   - **Retain**: r >= 0.30
   - **Review**: 0.20 <= r < 0.30
   - **Remove**: r < 0.20

3. **Cronbach's alpha**:
   - Overall and per dimension
   - Target: alpha >= 0.70
   - Examine "alpha if item deleted" — flag items whose removal increases alpha by > 0.02

4. **Inter-item correlations**:
   - Average inter-item correlation: 0.15 - 0.50 is ideal
   - If average > 0.50, items may be redundant
   - If average < 0.15, items may not measure the same construct

### Phase 3: Validation Study (N = 200+)

**Purpose**: Establish construct validity and finalize the instrument.

**Analyses**:
1. Confirmatory Factor Analysis (CFA)
2. Convergent and discriminant validity
3. Test-retest reliability (on subset of N = 50)
4. Known-groups validity (if applicable)
5. Measurement invariance across groups (if applicable)

---

## Rubric Development

### Analytic vs Holistic Rubrics

| Feature | Analytic | Holistic |
|---------|----------|---------|
| Structure | Multiple dimensions, each scored separately | Single overall score |
| Diagnostic value | High — identifies specific strengths/weaknesses | Low — overall impression only |
| Scoring time | Longer | Shorter |
| Inter-rater reliability | Higher (clearer criteria per dimension) | Lower |
| Best for | Formative assessment, research | Screening, summative ranking |

### Rubric Development Steps

1. **Identify the task**: What performance or product is being assessed?
2. **Define dimensions**: 3-6 dimensions that capture the important aspects of quality
3. **Define performance levels**: 3-5 levels per dimension (e.g., Beginning, Developing, Proficient, Exemplary)
4. **Write descriptors**: For each cell (dimension x level), write observable, specific behaviors
5. **Test with exemplars**: Score 5-10 actual performances and verify the rubric discriminates
6. **Calibrate raters**: Have 2+ raters score the same performances; calculate agreement
7. **Revise**: Modify descriptors where raters disagree

### Descriptor Writing Rules

- Use **observable behaviors**, not vague quality terms
  - Bad: "Excellent understanding"
  - Good: "Correctly identifies and explains all key concepts with relevant examples"
- Each level should be **clearly distinguishable** from adjacent levels
- Use **parallel grammatical structure** across levels
- Avoid **negative-only descriptors** at low levels (say what they DO, not just what they don't)
- Include **quantity and quality indicators** where possible ("3 or more examples" vs "few examples")

---

## Coding Scheme Development

### Steps

1. **Define the research question** the coding addresses
2. **Determine the unit of analysis**: sentence, paragraph, speaking turn, episode, document
3. **Develop initial codes**: Deductive (theory-driven), inductive (data-driven), or hybrid
4. **Write the codebook**: Each code gets a label, definition, inclusion criteria, exclusion criteria, and example
5. **Train coders**: 2-4 hours of training with practice examples
6. **Pilot code**: Both coders independently code the same 10-20 units
7. **Calculate reliability**: Cohen's kappa >= 0.60
8. **Revise and recode**: If kappa < 0.60, revise problematic codes and retrain

### Codebook Quality Checklist

- [ ] Every code has a clear, non-overlapping definition
- [ ] Inclusion AND exclusion criteria are specified for each code
- [ ] At least 2 examples per code (one clear case, one borderline case)
- [ ] Decision rules for ambiguous cases are documented
- [ ] A catch-all "Other" code exists (with instructions for when to use it)
- [ ] The coding unit is clearly defined
- [ ] Mutual exclusivity or co-occurrence rules are specified
