# Experiment Infrastructure — Shared Standards for Experimentation Skills

## Purpose

Provides shared standards, protocols, and conventions used by all 4 experimentation skills (`experiment-designer`, `data-analyst`, `simulation-runner`, `lab-notebook`). All experiment skills MUST reference and follow these standards.

---

## 1. Venv Management Protocol

All Python code execution happens inside a project-local virtual environment.

### Setup Procedure

```
1. Check if ./experiment_env/ exists
   ├── Yes → Activate and check for missing packages
   └── No  → Create: python -m venv ./experiment_env
             Activate: source ./experiment_env/bin/activate (Unix) or ./experiment_env/Scripts/activate (Windows)
             Install core: pip install -r requirements.txt
```

### Core Packages

All experiment skills share these base packages:

| Package | Version | Purpose |
|---------|---------|---------|
| `numpy` | latest | Numerical computation, random number generation |
| `scipy` | latest | Statistical tests, distributions, optimization |
| `pandas` | latest | Data manipulation, I/O |
| `statsmodels` | latest | Statistical models, hypothesis tests, power analysis |
| `matplotlib` | latest | Base plotting library |
| `seaborn` | latest | Statistical visualization |
| `pingouin` | latest | Simplified stats interface, Bayesian tests, effect sizes |
| `scikit-learn` | latest | Machine learning, preprocessing, cross-validation |

### Skill-Specific Extras

| Skill | Extra Packages | Purpose |
|-------|---------------|---------|
| `data-analyst` | `semopy`, `lifelines`, `openpyxl`, `pyreadstat` | SEM/CFA, survival analysis, Excel/SPSS/Stata reading |
| `simulation-runner` | `joblib`, `networkx`, `tqdm` | Parallel execution, graph topologies, progress bars |
| `experiment-designer` | (none beyond core) | — |
| `lab-notebook` | (none beyond core) | Uses only stdlib `hashlib` |

### Requirements File

On first venv creation, generate `./experiment_env/requirements.txt` with pinned versions:

```
pip freeze > ./experiment_env/requirements.txt
```

This file becomes part of the experiment record (tracked by `lab-notebook`).

### Reuse Logic

- If `./experiment_env/` exists, activate it and check for missing packages: `pip install --quiet <missing>`
- Never recreate a venv that already exists (preserves reproducibility)
- If a skill needs extra packages not yet installed, install them incrementally

---

## 2. APA Statistical Formatting Rules

All statistical output MUST follow APA 7th Edition formatting.

### General Rules

| Rule | Standard | Example |
|------|----------|---------|
| Test statistics | Italicize, 2 decimal places | *F*, *t*, *r*, chi-sq |
| *p*-values | No leading zero, 3 decimal places | *p* = .016 |
| *p* < .001 | Report as *p* < .001 | *p* < .001 (not *p* = .000) |
| Effect sizes | 2 decimal places | *d* = 0.54, eta-sq = .09 |
| Confidence intervals | Square brackets, 2 decimal places | 95% CI [0.23, 0.85] |
| Degrees of freedom | Integer for *t*, *F*; report both for *F* | *t*(87), *F*(2, 87) |
| Exact values | Report exact values, not thresholds | *p* = .034 (not *p* < .05) |

### Per-Test Format Strings

```
Independent t-test:  t(df) = X.XX, p = .XXX, d = X.XX, 95% CI [X.XX, X.XX]
Paired t-test:       t(df) = X.XX, p = .XXX, d = X.XX, 95% CI [X.XX, X.XX]
One-way ANOVA:       F(df1, df2) = X.XX, p = .XXX, eta-sq = .XX
Factorial ANOVA:     F(df1, df2) = X.XX, p = .XXX, partial-eta-sq = .XX
Chi-square:          chi-sq(df) = X.XX, p = .XXX, Cramer's V = .XX
Pearson r:           r(df) = .XX, p = .XXX
Spearman rho:        r_s(df) = .XX, p = .XXX
Mann-Whitney:        U = XXXXX, p = .XXX, r = .XX
Wilcoxon:            W = XXXXX, p = .XXX, r = .XX
Kruskal-Wallis:      H(df) = X.XX, p = .XXX, epsilon-sq = .XX
Linear regression:   b = X.XX, SE = X.XX, t(df) = X.XX, p = .XXX, 95% CI [X.XX, X.XX]
Logistic regression: OR = X.XX, 95% CI [X.XX, X.XX], p = .XXX
```

### Effect Size Interpretation Thresholds (Cohen's Conventions)

| Measure | Small | Medium | Large |
|---------|-------|--------|-------|
| Cohen's *d* | 0.20 | 0.50 | 0.80 |
| eta-sq | .01 | .06 | .14 |
| partial eta-sq | .01 | .06 | .14 |
| omega-sq | .01 | .06 | .14 |
| Pearson *r* | .10 | .30 | .50 |
| *R*-sq | .02 | .13 | .26 |
| Cohen's *f* | 0.10 | 0.25 | 0.40 |
| Cramer's *V* (df=1) | .10 | .30 | .50 |
| Odds Ratio | 1.5 | 2.5 | 4.0 |

> **Note**: Cohen's conventions are benchmarks, not rigid thresholds. Domain-specific norms should take precedence when available (e.g., Hattie's zone of desired effects *d* > 0.4 in education).

### Table Formatting (APA 7)

- No vertical lines
- Horizontal rules: top of table, below header row, bottom of table only
- Column headers: bold, centered
- Numbers: right-aligned, consistent decimal places within a column
- Table number: "Table 1" (bold, above table)
- Table title: italicized, title case, below table number
- Notes: below bottom rule, prefixed with "Note."

---

## 3. Plot Generation Standards

All figures MUST be publication-quality and follow these standards.

### Style Configuration

```python
import matplotlib.pyplot as plt
import seaborn as sns

# Apply publication style
sns.set_theme(style="whitegrid")
plt.rcParams.update({
    'font.family': 'serif',
    'font.serif': ['Times New Roman'],
    'font.size': 12,
    'axes.titlesize': 14,
    'axes.labelsize': 12,
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
    'legend.fontsize': 10,
    'figure.dpi': 300,
    'savefig.dpi': 300,
    'savefig.bbox': 'tight',
    'figure.figsize': (8, 6),
})

# Colorblind-safe palette
PALETTE = sns.color_palette("colorblind")
sns.set_palette(PALETTE)
```

### Output Format

- Save as both PNG (for preview/Markdown embedding) and PDF (for LaTeX inclusion)
- Save to `./experiment_outputs/figures/`
- Naming: `figure_NN_description.png` and `figure_NN_description.pdf` (e.g., `figure_01_group_comparison.png`)

### Figure Requirements

- Clear axis labels with units
- Legend when multiple groups/conditions
- No chartjunk (unnecessary grid lines, 3D effects, gradient fills)
- Error bars: SEM or 95% CI (always specify which)
- Caption: APA format — "Figure N. *Description.*" below figure

### Common Plot Types

| Analysis | Recommended Plot | Library Call |
|----------|-----------------|-------------|
| Group comparison | Box plot or violin plot | `sns.boxplot()` / `sns.violinplot()` |
| Correlation | Scatter with regression line | `sns.regplot()` |
| Distribution | Histogram + KDE | `sns.histplot(kde=True)` |
| Interaction | Line plot with error bars | `sns.pointplot()` |
| Effect sizes | Forest plot | Custom matplotlib |
| Regression diagnostics | Residual vs fitted | `sns.residplot()` |
| Correlation matrix | Heatmap | `sns.heatmap()` |
| Q-Q plot | Probability plot | `scipy.stats.probplot()` |
| Power curve | Line plot | `matplotlib.pyplot.plot()` |

---

## 4. Output Directory Convention

All experiment artifacts are stored in a standardized directory structure.

```
./experiment_outputs/
├── figures/          # Plots: PNG + PDF pairs
│   ├── figure_01_group_comparison.png
│   ├── figure_01_group_comparison.pdf
│   └── ...
├── tables/           # Data tables: CSV (raw) + Markdown (formatted)
│   ├── table_01_descriptive_stats.csv
│   ├── table_01_descriptive_stats.md
│   └── ...
├── scripts/          # Generated Python scripts (reproducibility record)
│   ├── analysis.py
│   ├── simulation.py
│   └── ...
├── logs/             # Lab notebook entries
│   └── notebook_2026-03-16_experiment-name.md
└── reports/          # Analysis and simulation reports
    ├── analysis_report.md
    ├── simulation_report.md
    └── ...
```

### Rules

- Create `./experiment_outputs/` on first use (any experiment skill)
- Subdirectories created as needed
- Files numbered sequentially within each subdirectory
- All paths in handoff schemas are relative to project root

---

## 5. Agent Naming Convention

Agent names are scoped to their skill directory. Multiple skills may have agents with the same name (e.g., `intake_agent`).

### Cross-Skill References

When referencing agents across skills, **always** use the fully-qualified path:

```
skill-name/agent_name
```

Examples:
- `experiment-designer/intake_agent` (not just `intake_agent`)
- `data-analyst/report_compiler_agent` (not just `report_compiler_agent`)
- `simulation-runner/report_compiler_agent` (different agent, same name)

This convention is used in:
- `shared/handoff_schemas.md` Producer/Consumer fields
- `.claude/CLAUDE.md` routing rules
- Cross-skill references within agent files

### Within-Skill References

Within a skill's own files, short names are acceptable (e.g., `intake_agent` in `data-analyst/agents/visualization_agent.md` refers to `data-analyst/agents/intake_agent.md`).

---

## 6. Auto-Logging Protocol

When experiment skills execute within the academic pipeline, they automatically log their activities to the lab notebook.

### How It Works

```
Pipeline orchestrator creates notebook (Stage 1.5 start)
  │
  ├── Passes notebook_path to each experiment skill
  │
  ├── experiment-designer executes
  │   └── At end of Phase 3: appends design record entry to notebook
  │
  ├── data-analyst executes
  │   ├── At end of Phase 1: appends data preparation entry
  │   ├── At end of Phase 3: appends analysis entry
  │   └── At end of Phase 5: appends results summary entry
  │
  ├── simulation-runner executes
  │   ├── At end of Phase 2: appends execution entry
  │   └── At end of Phase 4: appends results summary entry
  │
  └── lab-notebook provenance_auditor validates all entries
```

### Rules

1. **Pipeline orchestrator** passes `notebook_path` parameter to each experiment skill at dispatch
2. At the **end of each agent phase**, the skill appends a structured entry to the notebook file using the entry format defined in `lab-notebook` Section 5.5
3. Entries are **appended directly** (file append operation) — `lab-notebook` agents are NOT invoked mid-execution to avoid circular dependencies
4. The `lab-notebook/provenance_auditor_agent` validates all auto-logged entries during `audit` or `export` mode
5. If **no notebook exists** and the pipeline is active, the pipeline orchestrator creates one via `lab-notebook` (full mode) at the start of Stage 1.5 before dispatching other experiment skills

### Standalone Behavior

When experiment skills run **standalone** (outside the pipeline), auto-logging is disabled. Users can manually invoke `lab-notebook` (log-entry mode) to record results after the fact.

---

## 7. Failure Paths

Common failure scenarios across all experiment skills. Each skill's SKILL.md references this section and adds skill-specific failures.

| Failure Code | Trigger | Severity | Recovery |
|-------------|---------|----------|----------|
| `VENV_CREATE_FAILED` | Cannot create virtual environment (permissions, disk space) | BLOCKING | Report error with OS-specific message. Suggest: manual venv creation, check permissions, check disk space. Provide `requirements.txt` for manual install. |
| `PACKAGE_INSTALL_FAILED` | pip install fails (network, version conflict) | BLOCKING | Report specific package and error. Suggest: check network, try `pip install --upgrade pip`, pin to compatible version. Continue with available packages if non-critical package fails. |
| `DATA_FILE_NOT_FOUND` | User-specified data file does not exist | BLOCKING | Prompt user for correct path. List files matching common data extensions (*.csv, *.xlsx, *.sav, *.dta) in current directory and subdirectories. |
| `DATA_FORMAT_UNREADABLE` | File format not recognized or corrupted | BLOCKING | Report detected format and error. List supported formats. Suggest conversion tools or alternative file. |
| `EXECUTION_TIMEOUT` | Python script exceeds 10 minutes execution time | BLOCKING | Kill process. Report last output line. Suggest: reduce iterations, subsample data, simplify model. Offer to retry with smaller parameters. |
| `CONVERGENCE_FAILURE` | Simulation or optimization does not converge after max iterations | MAJOR | Report convergence diagnostics (current MCSE, R-hat, trace plot). Suggest: increase iterations, adjust starting values, simplify model, use different algorithm. Do NOT proceed with non-converged results. |
| `ALL_ASSUMPTIONS_VIOLATED` | Every statistical assumption fails for chosen test | MAJOR | Report which assumptions failed and by how much. Recommend non-parametric alternative. Present options to user. Do NOT proceed with parametric test without user confirmation. |
| `POWER_TOO_LOW` | Computed power < 0.80 for feasible sample size | WARNING | Report power table showing power at various N. Suggest: increase N, target larger effect, change design. Warn but do NOT block — user may accept lower power with justification. |
| `NOTEBOOK_CORRUPTED` | Lab notebook file is malformed or unreadable | MAJOR | Create backup of corrupted file (append `.bak`). Start fresh notebook. Attempt to salvage individual entries from corrupted file. Report what was recovered. |
| `HANDOFF_INCOMPLETE` | Required schema fields missing in upstream handoff | BLOCKING | Report specific missing fields with schema reference. Request re-generation from upstream skill. Do NOT proceed with partial data. |
| `SCHEMA_VALIDATION_FAILED` | Handoff artifact does not conform to schema type/enum constraints | BLOCKING | Report specific violations (field, expected type/value, actual value). Request correction from producing skill. |

### Severity Levels

| Severity | Meaning | Action |
|----------|---------|--------|
| BLOCKING | Cannot proceed at all | Stop, report, wait for resolution |
| MAJOR | Can proceed with degraded quality | Warn user, offer alternatives, require confirmation to continue |
| WARNING | Informational concern | Report to user, continue unless user objects |


---

## 8. Superpowers Integration

All code-writing experiment agents follow the superpowers integration protocol for disciplined code development. This ensures complex code is brainstormed, planned, test-driven, and verified before being declared complete.

**Reference**: See `shared/superpowers_integration.md` for the complete protocol.

**Key rule**: Before writing any code, consult the complexity classification table in `shared/superpowers_integration.md`. SIMPLE tasks execute directly. COMPLEX tasks go through the adaptive superpowers workflow (brainstorming → planning → TDD → verification).

**Prerequisite**: The superpowers plugin must be installed (`claude plugin install superpowers@claude-plugins-official`).
