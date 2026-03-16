# APA Results Text Templates

## Purpose

Fill-in templates for generating APA 7th Edition results text for each statistical test. Each template produces a self-contained paragraph that can be inserted directly into a manuscript's Results section. Variables in `{braces}` are replaced with actual values by `report_compiler_agent`.

---

## General Formatting Rules

1. **Italicize test statistics**: *t*, *F*, *r*, *p*, *d*, *M*, *SD*, *N*, *n*, *U*, *W*, *H*, *b*, *SE*, *z*, *R*, chi-sq
2. **No leading zero on p-values**: *p* = .034, not *p* = 0.034
3. **No leading zero on correlations and proportions**: *r* = .45, not *r* = 0.45
4. **Leading zero on other statistics**: *d* = 0.54, *M* = 3.21
5. **Exact p-values**: Report *p* = .034, not *p* < .05 (exception: *p* < .001 for very small values)
6. **Two decimal places** for test statistics, means, SDs
7. **Three decimal places** for p-values
8. **Square brackets for CIs**: 95% CI [0.23, 0.85]
9. **Degrees of freedom**: integers, in parentheses after the test statistic

---

## Independent-Samples t-Test

### Standard Template

```
An independent-samples t-test was conducted to compare {dv_description}
between {group_1_name} and {group_2_name}. {group_1_name} (*M* = {m1},
*SD* = {sd1}) scored {significantly/not significantly}
{higher/lower} than {group_2_name} (*M* = {m2}, *SD* = {sd2}),
*t*({df}) = {t_value}, *p* {p_string}, *d* = {d_value},
95% CI [{ci_lower}, {ci_upper}].
```

### Example (Filled)

```
An independent-samples t-test was conducted to compare exam scores
between the AI-assisted group and the traditional group. The AI-assisted
group (*M* = 78.32, *SD* = 12.14) scored significantly higher than the
traditional group (*M* = 72.08, *SD* = 12.76), *t*(178) = 3.42,
*p* < .001, *d* = 0.51, 95% CI [0.21, 0.81].
```

### With Welch's Correction (Unequal Variances)

```
Because Levene's test indicated unequal variances,
*F*({df1}, {df2}) = {f_value}, *p* = {levene_p}, a Welch's t-test was
used. {group_1_name} (*M* = {m1}, *SD* = {sd1}) scored
{significantly/not significantly} {higher/lower} than {group_2_name}
(*M* = {m2}, *SD* = {sd2}), *t*({welch_df}) = {t_value}, *p* {p_string},
*d* = {d_value}, 95% CI [{ci_lower}, {ci_upper}].
```

---

## Paired-Samples t-Test

### Standard Template

```
A paired-samples t-test was conducted to compare {dv_description} between
{condition_1} and {condition_2}. There was a {significant/non-significant}
difference between {condition_1} (*M* = {m1}, *SD* = {sd1}) and
{condition_2} (*M* = {m2}, *SD* = {sd2}), *t*({df}) = {t_value},
*p* {p_string}, *d* = {d_value}, 95% CI [{ci_lower}, {ci_upper}].
```

### Example (Filled)

```
A paired-samples t-test was conducted to compare anxiety scores before and
after the intervention. There was a significant difference between pre-test
(*M* = 42.15, *SD* = 8.73) and post-test (*M* = 36.82, *SD* = 9.11),
*t*(59) = 4.21, *p* < .001, *d* = 0.54, 95% CI [0.28, 0.80].
```

---

## One-Way ANOVA

### Standard Template

```
A one-way analysis of variance (ANOVA) was conducted to examine differences
in {dv_description} across {group_description} ({k} groups: {group_list}).
The effect was {significant/not significant}, *F*({df_between},
{df_within}) = {f_value}, *p* {p_string}, eta-sq = {eta_sq}.
{Post-hoc text if significant}
```

### Post-Hoc Text (Tukey HSD)

```
Post-hoc comparisons using Tukey's HSD test indicated that
{group_a} (*M* = {m_a}, *SD* = {sd_a}) scored significantly
{higher/lower} than {group_b} (*M* = {m_b}, *SD* = {sd_b}),
*p* = {p_pair}. The difference between {group_c} and {group_d}
was not significant (*p* = {p_pair2}).
```

### Example (Filled)

```
A one-way analysis of variance (ANOVA) was conducted to examine
differences in exam scores across three teaching methods (lecture,
flipped classroom, problem-based learning). The effect was significant,
*F*(2, 87) = 8.45, *p* < .001, eta-sq = .16. Post-hoc comparisons
using Tukey's HSD test indicated that problem-based learning
(*M* = 82.30, *SD* = 10.22) scored significantly higher than lecture
(*M* = 71.47, *SD* = 11.85), *p* < .001. The difference between flipped
classroom (*M* = 76.87, *SD* = 10.91) and lecture was also significant,
*p* = .034. Problem-based learning and flipped classroom did not differ
significantly (*p* = .082).
```

---

## Factorial ANOVA

### Standard Template

```
A {k1} x {k2} between-subjects ANOVA was conducted with {iv1_description}
and {iv2_description} as independent variables and {dv_description} as the
dependent variable. The main effect of {iv1} was {significant/not significant},
*F*({df1}, {df_error}) = {f1}, *p* {p1_string}, partial eta-sq = {pes1}.
The main effect of {iv2} was {significant/not significant},
*F*({df2}, {df_error}) = {f2}, *p* {p2_string}, partial eta-sq = {pes2}.
The interaction between {iv1} and {iv2} was {significant/not significant},
*F*({df_int}, {df_error}) = {f_int}, *p* {p_int_string},
partial eta-sq = {pes_int}.
```

---

## Repeated-Measures ANOVA

### Standard Template

```
A one-way repeated-measures ANOVA was conducted to compare {dv_description}
across {k} time points ({time_list}). {Mauchly's test text if applicable.}
{The main effect was/There was no} significant effect of {within_factor},
*F*({df_between}, {df_within}) = {f_value}, *p* {p_string},
partial eta-sq = {pes}.
```

### Sphericity Violation Addition

```
Mauchly's test indicated that the assumption of sphericity was violated,
chi-sq({df_mauchly}) = {chi2_mauchly}, *p* = {p_mauchly}; therefore, the
Greenhouse-Geisser correction was applied (epsilon = {epsilon}).
```

---

## Chi-Square Test of Independence

### Standard Template

```
A chi-square test of independence was conducted to examine the association
between {var1_description} and {var2_description}. The association was
{significant/not significant}, chi-sq({df}) = {chi2_value}, *p* {p_string},
Cramer's *V* = {v_value}.
```

### Example (Filled)

```
A chi-square test of independence was conducted to examine the association
between gender and program preference. The association was significant,
chi-sq(2) = 11.34, *p* = .003, Cramer's *V* = .24.
```

---

## Pearson Correlation

### Standard Template

```
A Pearson correlation was computed to assess the relationship between
{var1_description} and {var2_description}. There was a
{significant/non-significant} {positive/negative} {strong/moderate/weak}
correlation, *r*({df}) = {r_value}, *p* {p_string},
95% CI [{ci_lower}, {ci_upper}].
```

---

## Spearman Rank Correlation

### Standard Template

```
Due to non-normality, a Spearman rank-order correlation was computed.
There was a {significant/non-significant} {positive/negative}
{strong/moderate/weak} correlation between {var1} and {var2},
*r*_s({df}) = {rs_value}, *p* {p_string}.
```

---

## Multiple Linear Regression

### Standard Template

```
A multiple linear regression was conducted to predict {dv_description}
from {predictor_list}. The overall model was {significant/not significant},
*F*({df_model}, {df_resid}) = {f_value}, *p* {f_p_string},
*R*-sq = {r_sq}, adjusted *R*-sq = {adj_r_sq}. {Individual predictor text}
```

### Individual Predictor Text

```
{Predictor_name} was {a significant/not a significant} predictor,
*b* = {b}, *SE* = {se}, *t*({df_resid}) = {t_value}, *p* {p_string},
95% CI [{ci_lower}, {ci_upper}], beta = {standardized_beta}.
```

---

## Logistic Regression

### Standard Template

```
A binary logistic regression was performed to predict {dv_description}
from {predictor_list}. The model was {significant/not significant},
chi-sq({df}) = {llr_chi2}, *p* {p_string}, Nagelkerke *R*-sq = {r_sq}.
{Individual predictor text with OR}
```

### Individual Predictor (Logistic)

```
{Predictor_name} was {a significant/not a significant} predictor,
*b* = {b}, *SE* = {se}, Wald chi-sq = {wald}, *p* {p_string},
OR = {or_value}, 95% CI [{or_ci_lower}, {or_ci_upper}].
```

---

## Mann-Whitney U Test

### Standard Template

```
Due to violation of normality, a Mann-Whitney U test was conducted.
{Group_1} (Mdn = {mdn1}) {did/did not} differ significantly from
{group_2} (Mdn = {mdn2}), *U* = {u_value}, *p* {p_string},
*r* = {effect_r}.
```

---

## Kruskal-Wallis H Test

### Standard Template

```
Due to violation of normality, a Kruskal-Wallis H test was conducted.
There was a {significant/non-significant} difference across groups,
*H*({df}) = {h_value}, *p* {p_string}, epsilon-sq = {eps_sq}.
{Post-hoc text: Dunn's test with Bonferroni correction}
```

---

## Mediation Analysis

### Standard Template

```
A mediation analysis was conducted to test whether {mediator_description}
mediated the relationship between {iv_description} and {dv_description}
(5,000 bootstrap resamples). The total effect was {significant/not significant},
*c* = {c}, *p* {p_c}. The direct effect was {significant/not significant},
*c'* = {c_prime}, *p* {p_cprime}. The indirect effect through {mediator}
was {significant/not significant}, *ab* = {ab}, 95% bootstrap CI
[{ci_lower}, {ci_upper}]. {The mediator accounted for {pct_mediated}%
of the total effect, suggesting {partial/full} mediation.}
```

---

## Survival Analysis

### Kaplan-Meier + Log-Rank

```
Kaplan-Meier survival curves were estimated for each group. The median
survival time was {median_1} for {group_1} and {median_2} for {group_2}.
A log-rank test indicated a {significant/non-significant} difference in
survival distributions, chi-sq({df}) = {chi2}, *p* {p_string}.
```

### Cox Proportional Hazards

```
A Cox proportional hazards regression was conducted. {Predictor} was
{a significant/not a significant} predictor of survival,
HR = {hr}, 95% CI [{ci_lower}, {ci_upper}], *p* {p_string}.
```

---

## SEM / CFA

### CFA Template

```
A confirmatory factor analysis was conducted using maximum likelihood
estimation. The model demonstrated {good/adequate/poor} fit:
chi-sq({df}) = {chi2}, *p* {p_string}, CFI = {cfi}, TLI = {tli},
RMSEA = {rmsea}, 90% CI [{rmsea_ci_lower}, {rmsea_ci_upper}],
SRMR = {srmr}.
```

### SEM Fit Criteria Reference

| Index | Good Fit | Acceptable Fit |
|-------|----------|---------------|
| CFI | >= .95 | >= .90 |
| TLI | >= .95 | >= .90 |
| RMSEA | <= .06 | <= .08 |
| SRMR | <= .08 | <= .10 |
| chi-sq/df | <= 2.0 | <= 3.0 |

---

## Quick Reference: p-Value Formatting

| Raw p-value | Formatted |
|-------------|-----------|
| 0.00003 | *p* < .001 |
| 0.0012 | *p* = .001 |
| 0.034 | *p* = .034 |
| 0.050 | *p* = .050 |
| 0.087 | *p* = .087 |
| 0.456 | *p* = .456 |

---

## Quick Reference: Significance Language

| Result | Language |
|--------|----------|
| p < .001 | "was significant" / "significantly" |
| p < .05 | "was significant" / "significantly" |
| p = .05-.10 | "approached significance" / "marginally significant" (use sparingly) |
| p > .10 | "was not significant" / "did not significantly differ" |
