# Example: One-Way ANOVA — Comparing Exam Scores Across Teaching Methods

## Scenario

A researcher wants to compare exam scores across three teaching methods: Lecture, Flipped Classroom, and Problem-Based Learning (PBL). The study has N = 90 students (30 per group), randomly assigned to conditions.

**Research Question**: Do exam scores differ significantly across the three teaching methods?

**Hypothesis**: H1 (directional): PBL will produce higher exam scores than Lecture, with Flipped Classroom falling in between.

---

## Phase 1: Intake

### Mode Detection

User command: "Analyze my exam data — compare scores across three teaching methods using ANOVA"

**Mode**: `full` (clear analysis plan specified)

### Venv Setup

```python
import subprocess, sys, os

venv_path = "./experiment_env"
if not os.path.exists(venv_path):
    subprocess.run([sys.executable, "-m", "venv", venv_path], check=True)

pip_path = os.path.join(venv_path, "Scripts" if os.name == "nt" else "bin", "pip")
core = ["numpy", "scipy", "pandas", "statsmodels", "matplotlib", "seaborn", "pingouin", "scikit-learn"]
extras = ["semopy", "lifelines", "openpyxl", "pyreadstat"]
subprocess.run([pip_path, "install", "--quiet"] + core + extras, check=True)
```

### Data Loading and Profiling

```python
import pandas as pd
import numpy as np

df = pd.read_csv("exam_scores.csv")
print(f"Shape: {df.shape}")
print(f"Columns: {list(df.columns)}")
print(df.head())
```

**Output**:
```
Shape: (90, 3)
Columns: ['student_id', 'method', 'score']

   student_id          method  score
0           1        Lecture  68.2
1           2        Lecture  72.5
2           3        Lecture  65.1
3           4  Flipped Classroom  78.3
4           5  Flipped Classroom  74.9
```

### Dataset Profile

| Variable | Type | Missing | Missing % | Unique |
|----------|------|---------|-----------|--------|
| student_id | int | 0 | 0% | 90 |
| method | categorical | 0 | 0% | 3 |
| score | float | 0 | 0% | 90 |

### Analysis Plan

- **Primary**: One-way ANOVA — DV: score, IV: method (3 levels)
- **Post-hoc**: Tukey HSD (if ANOVA significant)
- **Alpha**: .05

---

## Phase 2: Data Preparation

### Missing Data

No missing data detected (0%). Cleaning step not needed.

### Outlier Detection

```python
from scipy import stats

for method in df['method'].unique():
    subset = df[df['method'] == method]['score']
    z_scores = np.abs(stats.zscore(subset))
    outliers = (z_scores > 3).sum()
    print(f"{method}: {outliers} outliers (|z| > 3)")
```

**Output**: No outliers detected in any group.

### Cleaned Data

Data is clean as-is. Saved to `experiment_outputs/tables/cleaned_data.csv`.

---

## Phase 3: Assumption Checking

### Assumption 1: Normality (per group)

```python
from scipy import stats

for method in df['method'].unique():
    subset = df[df['method'] == method]['score']
    W, p = stats.shapiro(subset)
    print(f"Shapiro-Wilk ({method}): W = {W:.4f}, p = {p:.4f}")
```

**Results**:

| Group | W | p | Verdict |
|-------|---|---|---------|
| Lecture | 0.9712 | .5621 | Met |
| Flipped Classroom | 0.9685 | .4892 | Met |
| PBL | 0.9743 | .6534 | Met |

**Q-Q plots**: Generated and saved to `experiment_outputs/figures/qq_score_*.png`. All three groups show points closely following the reference line.

### Assumption 2: Homogeneity of Variance

```python
lecture = df[df['method'] == 'Lecture']['score']
flipped = df[df['method'] == 'Flipped Classroom']['score']
pbl = df[df['method'] == 'PBL']['score']

F, p = stats.levene(lecture, flipped, pbl, center='median')
print(f"Levene's test: F = {F:.4f}, p = {p:.4f}")
```

**Result**: Levene's *F*(2, 87) = 0.42, *p* = .658

**Verdict**: Met

### Assumption 3: Independence

By design — students were randomly assigned to conditions. Independence is met.

### Assumption Summary

| Assumption | Test | Statistic | p | Verdict | Action |
|------------|------|-----------|---|---------|--------|
| Normality (Lecture) | Shapiro-Wilk | W = 0.97 | .562 | Met | Proceed |
| Normality (Flipped) | Shapiro-Wilk | W = 0.97 | .489 | Met | Proceed |
| Normality (PBL) | Shapiro-Wilk | W = 0.97 | .653 | Met | Proceed |
| Homogeneity | Levene's | F = 0.42 | .658 | Met | Proceed |
| Independence | By design | — | — | Met | Proceed |

**Overall Recommendation**: PROCEED with parametric one-way ANOVA. All assumptions met.

---

## Phase 4: Analysis Execution

### Descriptive Statistics

```python
desc = df.groupby('method')['score'].agg(['mean', 'std', 'count'])
print(desc)
```

| Method | M | SD | n |
|--------|---|----|----|
| Lecture | 71.47 | 11.85 | 30 |
| Flipped Classroom | 76.87 | 10.91 | 30 |
| PBL | 82.30 | 10.22 | 30 |

### One-Way ANOVA

```python
import pingouin as pg

aov = pg.anova(data=df, dv='score', between='method', detailed=True)
print(aov)
```

**Result**: *F*(2, 87) = 8.45, *p* < .001

### Post-Hoc: Tukey HSD

```python
posthoc = pg.pairwise_tukey(data=df, dv='score', between='method')
print(posthoc)
```

| Comparison | Mean Diff | p-tukey | Hedges' g |
|------------|-----------|---------|-----------|
| Lecture vs Flipped | -5.40 | .034 | 0.47 |
| Lecture vs PBL | -10.83 | < .001 | 0.98 |
| Flipped vs PBL | -5.43 | .033 | 0.51 |

### Reproducibility Script

Saved to `experiment_outputs/scripts/analysis.py` with seed = 42.

---

## Phase 5: Effect Sizes

### Eta-Squared

```python
ss_between = aov.loc[0, 'SS']
ss_total = aov['SS'].sum()
eta_sq = ss_between / ss_total
print(f"Eta-squared: {eta_sq:.4f}")
```

**Result**: eta-sq = .163

### Omega-Squared (Less Biased)

```python
ss_between = aov.loc[0, 'SS']
ms_within = aov.loc[1, 'MS']
df_between = aov.loc[0, 'DF']
omega_sq = (ss_between - df_between * ms_within) / (ss_total + ms_within)
print(f"Omega-squared: {omega_sq:.4f}")
```

**Result**: omega-sq = .143

### Bootstrap 95% CI for Eta-Squared

```python
np.random.seed(42)
boot_eta = []
for _ in range(2000):
    idx = np.random.choice(len(df), size=len(df), replace=True)
    boot_df = df.iloc[idx]
    groups = [boot_df[boot_df['method'] == m]['score'].values for m in df['method'].unique()]
    f_stat, _ = stats.f_oneway(*groups)
    eta = (2 * f_stat) / (2 * f_stat + 87)
    boot_eta.append(eta)

ci_lower = np.percentile(boot_eta, 2.5)
ci_upper = np.percentile(boot_eta, 97.5)
print(f"95% CI: [{ci_lower:.4f}, {ci_upper:.4f}]")
```

**Result**: eta-sq = .163, 95% CI [.04, .28]

### Pairwise Effect Sizes (Cohen's d)

| Comparison | d | 95% CI | Magnitude |
|------------|---|--------|-----------|
| Lecture vs Flipped | 0.47 | [0.05, 0.90] | Small-to-medium |
| Lecture vs PBL | 0.98 | [0.53, 1.43] | Large |
| Flipped vs PBL | 0.51 | [0.09, 0.94] | Medium |

### Interpretation

Teaching method accounts for 16.3% of the variance in exam scores (eta-sq = .163), representing a large effect by Cohen's conventions (eta-sq > .14). By Hattie's education-specific benchmark, the PBL vs Lecture effect (*d* = 0.98) is well within the "zone of desired effects" (*d* > 0.40).

---

## Phase 6: Visualization

### Figure 1: Box Plot

```python
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="whitegrid")
plt.rcParams.update({'font.family': 'serif', 'font.serif': ['Times New Roman'],
                     'font.size': 12, 'figure.dpi': 300, 'savefig.dpi': 300})

fig, ax = plt.subplots(figsize=(8, 6))
sns.boxplot(data=df, x='method', y='score', palette='colorblind',
            order=['Lecture', 'Flipped Classroom', 'PBL'],
            showmeans=True, meanprops={'marker': 'D', 'markerfacecolor': 'red',
                                       'markeredgecolor': 'black', 'markersize': 8})
sns.stripplot(data=df, x='method', y='score', color='black', alpha=0.3, size=3, jitter=True,
              order=['Lecture', 'Flipped Classroom', 'PBL'])
ax.set_xlabel("Teaching Method")
ax.set_ylabel("Exam Score")

plt.savefig("experiment_outputs/figures/figure_01_group_comparison.png", dpi=300, bbox_inches='tight')
plt.savefig("experiment_outputs/figures/figure_01_group_comparison.pdf", bbox_inches='tight')
plt.close()
```

**Figure 1.** *Distribution of exam scores by teaching method. Diamonds represent group means. Individual data points shown as jittered dots.*

---

## Phase 7: Report Compilation

### APA Results Text

A one-way analysis of variance (ANOVA) was conducted to examine differences in exam scores across three teaching methods (Lecture, Flipped Classroom, and Problem-Based Learning). Descriptive statistics indicated that PBL students scored highest (*M* = 82.30, *SD* = 10.22), followed by Flipped Classroom (*M* = 76.87, *SD* = 10.91) and Lecture (*M* = 71.47, *SD* = 11.85). The main effect of teaching method was significant, *F*(2, 87) = 8.45, *p* < .001, eta-sq = .16, indicating that teaching method accounted for 16.3% of the variance in exam scores — a large effect.

Post-hoc comparisons using Tukey's HSD indicated that PBL students scored significantly higher than Lecture students (*p* < .001, *d* = 0.98) and Flipped Classroom students (*p* = .033, *d* = 0.51). Flipped Classroom students also scored significantly higher than Lecture students (*p* = .034, *d* = 0.47).

### Table 1: Descriptive Statistics

**Table 1**

*Descriptive Statistics by Teaching Method*

| | Lecture | Flipped Classroom | PBL |
|---|---|---|---|
| *n* | 30 | 30 | 30 |
| *M* | 71.47 | 76.87 | 82.30 |
| *SD* | 11.85 | 10.91 | 10.22 |

*Note.* PBL = problem-based learning.

---

## Schema 11 Handoff Artifact

```markdown
## Experiment Results

**Experiment ID**: EXP-20260316-ANOVA-DEMO
**Result Type**: statistical_analysis

**Dataset Info**:
- Original N: 90
- Analyzed N: 90 (0 excluded)
- Missing strategy: None (no missing data)

**Assumption Checks**:
| Assumption | Test | Statistic | p | Verdict | Action |
|------------|------|-----------|---|---------|--------|
| Normality (Lecture) | Shapiro-Wilk | W = 0.97 | .562 | Met | Proceed |
| Normality (Flipped) | Shapiro-Wilk | W = 0.97 | .489 | Met | Proceed |
| Normality (PBL) | Shapiro-Wilk | W = 0.97 | .653 | Met | Proceed |
| Homogeneity | Levene's | F = 0.42 | .658 | Met | Proceed |

**Primary Results**:
- H1: F(2, 87) = 8.45, p < .001, eta-sq = .163, 95% CI [.04, .28]

**Effect Sizes**:
| Measure | Value | 95% CI | Magnitude |
|---------|-------|--------|-----------|
| eta-sq | .163 | [.04, .28] | Large |
| d (Lecture vs PBL) | 0.98 | [0.53, 1.43] | Large |
| d (Lecture vs Flipped) | 0.47 | [0.05, 0.90] | Small-medium |
| d (Flipped vs PBL) | 0.51 | [0.09, 0.94] | Medium |

**Tables**: Table 1 at experiment_outputs/tables/table_01_descriptives.csv
**Figures**: Figure 1 at experiment_outputs/figures/figure_01_group_comparison.png

**Reproducibility**: script at experiment_outputs/scripts/analysis.py, seed=42
```

---

## Key Takeaways from This Example

1. **All assumptions tested before running ANOVA** — normality per group, homogeneity, independence
2. **Post-hoc tests included** because the omnibus ANOVA was significant
3. **Multiple effect size measures** — eta-squared, omega-squared, and pairwise Cohen's d
4. **Bootstrap CI** for eta-squared (no simple analytical formula)
5. **Domain-specific benchmark** cited (Hattie's zone of desired effects)
6. **Complete Schema 11** artifact ready for handoff to academic-paper
