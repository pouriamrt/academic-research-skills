# APA Statistical Formatting Guide — APA 7th Edition Reference

## Purpose

Comprehensive reference for formatting statistical results according to APA 7th Edition Publication Manual. Used by `report_compiler_agent` and `analysis_executor_agent` to ensure every reported statistic is correctly formatted.

---

## Master Formatting Rules

### Rule 1: Italicize Statistical Symbols

Italicize all of the following when used as statistical symbols:

| Symbol | Meaning | Example |
|--------|---------|---------|
| *M* | Mean | *M* = 3.42 |
| *SD* | Standard deviation | *SD* = 1.23 |
| *Mdn* | Median | *Mdn* = 3.00 |
| *N* | Total sample size | *N* = 150 |
| *n* | Subsample size | *n* = 75 |
| *t* | t-test statistic | *t*(48) = 2.31 |
| *F* | F-test statistic | *F*(2, 87) = 4.56 |
| *r* | Correlation coefficient | *r* = .45 |
| *p* | p-value | *p* = .023 |
| *d* | Cohen's d | *d* = 0.54 |
| *b* | Unstandardized regression coefficient | *b* = 1.23 |
| *z* | z-score | *z* = 1.96 |
| *U* | Mann-Whitney U | *U* = 1234 |
| *W* | Wilcoxon W / Shapiro-Wilk | *W* = 0.97 |
| *H* | Kruskal-Wallis H | *H*(2) = 8.45 |
| *SE* | Standard error | *SE* = 0.45 |
| *R* | Multiple correlation | *R*-sq = .31 |
| *OR* | Odds ratio | *OR* = 2.34 |
| *HR* | Hazard ratio | *HR* = 1.56 |

Do NOT italicize: chi-sq, df, CI, %, Greek letters (alpha, beta, eta)

### Rule 2: Decimal Places

| Statistic | Decimal Places | Example |
|-----------|----------------|---------|
| Means, SDs | 2 | *M* = 42.15, *SD* = 8.73 |
| Test statistics (*t*, *F*, chi-sq) | 2 | *t*(48) = 2.31 |
| p-values | 3 | *p* = .034 |
| Correlation coefficients | 2-3 | *r* = .45 or *r* = .453 |
| Effect sizes (*d*, eta-sq) | 2 | *d* = 0.54, eta-sq = .09 |
| Percentages | 0-1 | 54% or 54.3% |
| Confidence intervals | 2 | 95% CI [0.23, 0.85] |
| R-squared | 2-3 | *R*-sq = .31 |
| Odds ratios | 2 | *OR* = 2.34 |
| Beta weights | 2 | beta = .45 |

### Rule 3: Leading Zeros

**No leading zero** when a value cannot exceed 1.0 in absolute value:
- *p* = .034 (not *p* = 0.034)
- *r* = .45 (not *r* = 0.45)
- *R*-sq = .31 (not *R*-sq = 0.31)
- eta-sq = .09 (not eta-sq = 0.09)
- beta = .45 (not beta = 0.45)
- Cramer's *V* = .24 (not Cramer's *V* = 0.24)

**Use leading zero** when a value can exceed 1.0:
- *M* = 0.54 (means can be any value)
- *SD* = 0.23
- *d* = 0.80 (Cohen's d can exceed 1)
- *b* = 0.34 (unstandardized coefficients)
- *OR* = 0.67
- *SE* = 0.12
- *t* = 0.34

### Rule 4: p-Value Reporting

| Raw p-value | Report as |
|-------------|-----------|
| < .001 | *p* < .001 |
| .001 to .999 | Exact value: *p* = .034 |
| = 1.000 | *p* > .999 |

**Never** report: *p* = .000, *p* < .05 (without exact value), *p* = n.s.

### Rule 5: Degrees of Freedom

- Report as integers in parentheses after the test statistic
- For *t*: *t*(df) — e.g., *t*(48)
- For *F*: *F*(df1, df2) — e.g., *F*(2, 87)
- For chi-sq: chi-sq(df) — e.g., chi-sq(4)
- For Welch's t: report decimal df — e.g., *t*(43.21)

### Rule 6: Confidence Intervals

- Use square brackets: 95% CI [lower, upper]
- Specify the confidence level: 95% CI, 99% CI
- Same decimal places as the statistic: *d* = 0.54, 95% CI [0.24, 0.84]
- Place after the relevant statistic, not at the end of the sentence

### Rule 7: Spaces and Symbols

- Space before and after equals sign: *p* = .034, not *p*=.034
- Space before and after inequality: *p* < .001, not *p*<.001
- No space between statistic and opening parenthesis: *t*(48), not *t* (48)
- Comma separating df values: *F*(2, 87), not *F*(2,87) or *F*(2;87)

---

## Per-Test Format Strings

### Independent-Samples t-Test

```
t(df) = X.XX, p = .XXX, d = X.XX, 95% CI [X.XX, X.XX]
```

Full sentence:
```
An independent-samples t-test indicated that [group 1] (M = X.XX, SD = X.XX)
scored significantly [higher/lower] than [group 2] (M = X.XX, SD = X.XX),
t(df) = X.XX, p = .XXX, d = X.XX, 95% CI [X.XX, X.XX].
```

### Paired-Samples t-Test

```
t(df) = X.XX, p = .XXX, d = X.XX, 95% CI [X.XX, X.XX]
```

### Welch's t-Test

```
t(df.XX) = X.XX, p = .XXX, d = X.XX, 95% CI [X.XX, X.XX]
```

Note: Welch's df is not an integer.

### One-Way ANOVA

```
F(df_between, df_within) = X.XX, p = .XXX, eta-sq = .XX
```

With post-hoc:
```
F(df1, df2) = X.XX, p = .XXX, eta-sq = .XX. Post-hoc Tukey HSD comparisons
indicated that [group A] (M = X.XX) differed significantly from [group B]
(M = X.XX), p = .XXX.
```

### Factorial ANOVA

Report each effect separately:
```
Main effect of [IV1]: F(df1, df_error) = X.XX, p = .XXX, partial eta-sq = .XX
Main effect of [IV2]: F(df2, df_error) = X.XX, p = .XXX, partial eta-sq = .XX
Interaction [IV1 x IV2]: F(df_int, df_error) = X.XX, p = .XXX, partial eta-sq = .XX
```

### Repeated-Measures ANOVA

Without sphericity correction:
```
F(df_between, df_within) = X.XX, p = .XXX, partial eta-sq = .XX
```

With Greenhouse-Geisser:
```
Mauchly's test indicated a violation of sphericity, chi-sq(df) = X.XX, p = .XXX.
Using the Greenhouse-Geisser correction (epsilon = .XX),
F(df_corrected, df_corrected) = X.XX, p = .XXX, partial eta-sq = .XX.
```

### ANCOVA

```
After controlling for [covariate], there was a significant effect of [IV] on [DV],
F(df1, df2) = X.XX, p = .XXX, partial eta-sq = .XX.
```

### Chi-Square Test of Independence

```
chi-sq(df) = X.XX, p = .XXX, Cramer's V = .XX
```

Note: "chi-sq" is NOT italicized in APA style.

### Fisher's Exact Test

```
Fisher's exact test indicated a significant association, p = .XXX, OR = X.XX,
95% CI [X.XX, X.XX].
```

### Pearson Correlation

```
r(df) = .XX, p = .XXX
```

Where df = N - 2.

### Spearman Rank Correlation

```
r_s(df) = .XX, p = .XXX
```

### Partial Correlation

```
r_partial(df) = .XX, p = .XXX, controlling for [variables]
```

### Multiple Linear Regression

Overall model:
```
F(df_model, df_resid) = X.XX, p = .XXX, R-sq = .XX, adjusted R-sq = .XX
```

Individual predictor:
```
b = X.XX, SE = X.XX, t(df) = X.XX, p = .XXX, 95% CI [X.XX, X.XX], beta = .XX
```

### Logistic Regression

Overall model:
```
chi-sq(df) = X.XX, p = .XXX, Nagelkerke R-sq = .XX
```

Individual predictor:
```
b = X.XX, SE = X.XX, Wald = X.XX, p = .XXX, OR = X.XX, 95% CI [X.XX, X.XX]
```

### Mann-Whitney U

```
U = XXXXX, p = .XXX, r = .XX
```

Report medians, not means:
```
A Mann-Whitney U test indicated that [group 1] (Mdn = X.XX) [did/did not] differ
significantly from [group 2] (Mdn = X.XX), U = XXXXX, p = .XXX, r = .XX.
```

### Wilcoxon Signed-Rank

```
W = XXXXX, p = .XXX, r = .XX
```

### Kruskal-Wallis H

```
H(df) = X.XX, p = .XXX, epsilon-sq = .XX
```

### Friedman Test

```
chi-sq(df) = X.XX, p = .XXX
```

### HLM / Mixed-Effects Model

Fixed effects:
```
b = X.XX, SE = X.XX, t = X.XX, p = .XXX
```

Model fit:
```
AIC = XXXX.XX, BIC = XXXX.XX, -2LL = XXXX.XX
```

### SEM / CFA

Fit indices:
```
chi-sq(df) = X.XX, p = .XXX, CFI = .XX, TLI = .XX, RMSEA = .XX,
90% CI [.XX, .XX], SRMR = .XX
```

Path coefficients:
```
beta = .XX, p = .XXX (standardized)
```

### Mediation

```
Indirect effect: ab = X.XX, 95% bootstrap CI [X.XX, X.XX]
Direct effect: c' = X.XX, p = .XXX
Total effect: c = X.XX, p = .XXX
```

### Survival Analysis (Cox PH)

```
HR = X.XX, 95% CI [X.XX, X.XX], p = .XXX
```

---

## Table Formatting (APA 7)

### Rules

1. **No vertical lines** — ever
2. **Horizontal rules only**: top of table, below header row, bottom of table
3. **Table number**: Bold, above table ("**Table 1**")
4. **Table title**: Italics, title case, on line below number ("*Descriptive Statistics by Group*")
5. **Column headers**: Bold, centered
6. **Numbers**: Right-aligned, consistent decimal places within column
7. **Notes**: Below bottom rule, starts with "Note." in italics

### Example

```
**Table 1**

*Descriptive Statistics by Teaching Method*

| | Lecture | Flipped | PBL |
|---|---|---|---|
| *n* | 30 | 30 | 30 |
| *M* | 71.47 | 76.87 | 82.30 |
| *SD* | 11.85 | 10.91 | 10.22 |

*Note.* PBL = problem-based learning.
```

---

## Figure Formatting (APA 7)

### Rules

1. **Figure number**: Bold, above figure ("**Figure 1**")
2. **Figure title**: Italics, on line below number
3. **No title on the figure itself** — the caption IS the title
4. **Axis labels**: Clear, with units in parentheses
5. **Legend**: When multiple groups/conditions
6. **Error bars**: Always specify in caption (SEM or 95% CI)

### Caption Format

```
**Figure 1**

*Distribution of Exam Scores by Teaching Method*

Note. Error bars represent 95% confidence intervals. Diamonds indicate group means.
```

---

## Common Mistakes to Avoid

| Mistake | Correct |
|---------|---------|
| *p* = 0.034 | *p* = .034 (no leading zero) |
| *p* < .05 (without exact value) | *p* = .034 |
| *p* = .000 | *p* < .001 |
| *r* = 0.45 | *r* = .45 (no leading zero) |
| *F* (2, 87) = 4.56 | *F*(2, 87) = 4.56 (no space before paren) |
| t = 2.31, p = .034 | *t* = 2.31, *p* = .034 (italicize) |
| 95% CI (0.23-0.85) | 95% CI [0.23, 0.85] (square brackets, comma) |
| df = 2, 87 | Report in parens: *F*(2, 87) |
| chi-squared | chi-sq (or the symbol if supported) |
| n.s. | *p* = .456 (report exact value) |
| p = .05 (claiming significant) | *p* = .050 (borderline; do not claim significance) |
