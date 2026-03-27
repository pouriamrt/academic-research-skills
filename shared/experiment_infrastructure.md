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

### Advanced Test Format Strings

```
SEM path coefficient:           beta = X.XX, SE = X.XX, z = X.XX, p = .XXX, 95% CI [X.XX, X.XX]
SEM model fit:                  chi-sq(df) = X.XX, p = .XXX, CFI = .XX, TLI = .XX, RMSEA = .XX, 90% CI [.XX, .XX], SRMR = .XX
CFA factor loading:             lambda = X.XX, SE = X.XX, z = X.XX, p = .XXX
HLM/Multilevel fixed effect:    b = X.XX, SE = X.XX, t(df) = X.XX, p = .XXX, 95% CI [X.XX, X.XX]
HLM/Multilevel random effect:   sigma-sq = X.XX, SD = X.XX, 95% CI [X.XX, X.XX]
HLM ICC:                        ICC = .XX, 95% CI [.XX, .XX]
Cox proportional hazards:       HR = X.XX, 95% CI [X.XX, X.XX], p = .XXX
Kaplan-Meier log-rank:          chi-sq(df) = X.XX, p = .XXX
Bayesian posterior:             M = X.XX, SD = X.XX, 95% HDI [X.XX, X.XX], BF10 = X.XX
Bayesian model comparison:      BF10 = X.XX (evidence: [anecdotal|moderate|strong|very strong|extreme])
Mediation indirect effect:      ab = X.XX, SE = X.XX, 95% CI [X.XX, X.XX] (bootstrap N = XXXXX)
Moderation interaction:         b = X.XX, SE = X.XX, t(df) = X.XX, p = .XXX, Delta-R-sq = .XX
Repeated measures ANOVA:        F(df1, df2) = X.XX, p = .XXX, partial-eta-sq = .XX, Greenhouse-Geisser epsilon = .XX
MANOVA:                         Pillai's V = X.XX, F(df1, df2) = X.XX, p = .XXX, partial-eta-sq = .XX
```

### Non-Significant (Null) Result Format Strings

Null results MUST be reported with the same precision as significant results. Never omit or downplay non-significant findings — this prevents publication bias and supports cumulative science.

```
Non-significant t-test:         t(df) = X.XX, p = .XXX, d = X.XX, 95% CI [X.XX, X.XX]
  Example: "The difference was not statistically significant, t(87) = 1.34, p = .184, d = 0.28, 95% CI [-0.14, 0.71]."

Non-significant ANOVA:          F(df1, df2) = X.XX, p = .XXX, eta-sq = .XX
  Example: "There was no significant main effect of condition, F(2, 87) = 1.12, p = .331, eta-sq = .03."

Non-significant correlation:    r(df) = .XX, p = .XXX
  Example: "The correlation was not statistically significant, r(48) = .12, p = .401."

Non-significant chi-square:     chi-sq(df) = X.XX, p = .XXX, Cramer's V = .XX
  Example: "The association was not statistically significant, chi-sq(2) = 3.45, p = .178, Cramer's V = .13."

Non-significant regression:     b = X.XX, SE = X.XX, t(df) = X.XX, p = .XXX, 95% CI [X.XX, X.XX]
  Example: "The predictor did not significantly predict the outcome, b = 0.08, SE = 0.12, t(95) = 0.67, p = .505, 95% CI [-0.16, 0.32]."

Non-significant Bayesian:       BF10 = X.XX, M = X.XX, SD = X.XX, 95% HDI [X.XX, X.XX] (evidence for null: [anecdotal|moderate|strong])
  Example: "Bayesian analysis provided moderate evidence for the null hypothesis, BF10 = 0.21, M = 0.15, SD = 0.29, 95% HDI [-0.42, 0.73]."
```

> **Reporting rule**: Always report effect sizes and confidence intervals for non-significant results. Frame non-significance as "the evidence was insufficient to detect an effect" — never as "there was no effect." Include equivalence testing when relevant (TOST procedure).

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

---

## 9. Mermaid MCP Diagram Generation

In addition to matplotlib/seaborn statistical plots, experiment agents generate structural diagrams using the Mermaid MCP server (`mcp__mermaid__generate`). These diagrams visualize workflows, designs, and decision logic — complementing the statistical figures.

### When to Use Mermaid MCP vs matplotlib

| Use Mermaid MCP | Use matplotlib/seaborn |
|-----------------|----------------------|
| Experiment design structure (groups, conditions, flow) | Statistical plots (box plots, scatter, histograms) |
| Participant flow / CONSORT diagrams | Data distributions and comparisons |
| Analysis workflow (which tests ran, decision points) | Regression lines, confidence bands |
| Simulation architecture (DGP → analysis → performance) | Convergence trace plots, diagnostic plots |
| Assumption check decision trees | Power curves, sensitivity plots |
| Pipeline/handoff diagrams | Forest plots, effect size plots |

### Tool Invocation

```
mcp__mermaid__generate(
    code: "<mermaid diagram code>",
    name: "<descriptive-name>",
    folder: "./experiment_outputs/figures",
    theme: "default",
    backgroundColor: "white"
)
```

### Output Convention

- **Location**: `experiment_outputs/figures/` (same directory as matplotlib figures)
- **Naming**: `diagram_<type>_<description>.png` (e.g., `diagram_consort_participant_flow.png`, `diagram_analysis_workflow.png`)
- **Format**: PNG (generated by MCP server)
- **Numbering**: Mermaid diagrams are numbered in the same sequence as matplotlib figures (use `fig_counter`)
- **Caption**: APA-format caption: "Figure N. *Description in italics.*"

### Diagram Types by Agent

| Agent | Diagram Type | Mermaid Chart Type | When to Generate |
|-------|--------------|--------------------|-----------------|
| `protocol_compiler_agent` | Experiment design structure | `flowchart TB` | Always — shows groups, conditions, measurement points |
| `protocol_compiler_agent` | CONSORT participant flow | `flowchart TB` | RCT and quasi-experimental designs |
| `protocol_compiler_agent` | Timeline / Gantt | `gantt` | When protocol includes timeline |
| `analysis_executor_agent` | Analysis decision flowchart | `flowchart TB` | When assumption checks redirect to alternative tests |
| `visualization_agent` | Analysis overview | `flowchart LR` | Always — shows what analyses were run and their relationships |
| `report_compiler_agent` (data-analyst) | Results summary diagram | `flowchart TB` | When 3+ analyses form a logical chain |
| `model_builder_agent` | DGP architecture | `flowchart LR` | Always — shows data generation → analysis → measurement flow |
| `execution_engine_agent` | Execution plan | `flowchart TB` | When parallelization or multi-chain execution is used |
| `diagnostics_agent` | Convergence status | `flowchart LR` | Always — per-estimand PASS/MARGINAL/FAIL status |
| `report_compiler_agent` (simulation-runner) | Simulation architecture | `flowchart TB` | Always — shows the full ADEMP structure |

### Style Guidelines

- Use colored subgraphs to distinguish stages: `style <id> fill:#<color>,color:#fff`
- Use consistent color scheme across all diagrams in a single experiment:
  - Design/Input: `#4A90D9` (blue)
  - Execution/Process: `#F5A623` (orange)
  - Results/Output: `#2ECC71` (green)
  - Verification/Quality: `#E74C3C` (red)
  - Decision points: `#9B59B6` (purple)
- Keep diagrams focused — one concept per diagram, not the entire pipeline
- Use `<br/>` for line breaks in node labels (not `\n`)

---

## 10. PaperBanana MCP — Publication-Quality Methodology Diagrams

The PaperBanana MCP server (`mcp__paperbanana__generate_diagram`) generates publication-quality methodology diagrams from natural-language descriptions. It is used **exclusively for methodology/workflow diagrams** — not for statistical plots (use matplotlib/seaborn) or structural flowcharts (use Mermaid MCP).

### Scope — What PaperBanana Is and Is NOT For

| Use PaperBanana `generate_diagram` | Do NOT use PaperBanana |
|-------------------------------------|------------------------|
| Research methodology overview diagrams | Statistical plots (bar, scatter, box, forest) — use matplotlib/seaborn |
| Conceptual framework visualizations | Structural flowcharts (CONSORT, DGP, decision trees) — use Mermaid MCP |
| Theoretical model diagrams | Data distribution plots — use matplotlib/seaborn |
| Multi-phase research design illustrations | Convergence diagnostics — use matplotlib/seaborn |
| Intervention logic models | Simple process flows — use Mermaid MCP |

**Rule**: PaperBanana is for **rich, publication-quality methodology diagrams** that benefit from visual sophistication beyond what Mermaid box-and-arrow diagrams can offer. If a Mermaid flowchart would suffice, prefer Mermaid (it's faster and always available).

### Prerequisites

PaperBanana requires a Google API key. Before invoking, agents MUST check availability:

```
Availability Check (mandatory before first use in a session):

1. Check if mcp__paperbanana__generate_diagram is available as a tool
   ├── Not available → SKIP. Fall back to Mermaid MCP for structural diagrams.
   └── Available → Check GOOGLE_API_KEY
       ├── GOOGLE_API_KEY not set → WARN user:
       │   "PaperBanana MCP requires a Google API key. Set GOOGLE_API_KEY in your
       │    environment to enable publication-quality methodology diagrams.
       │    Falling back to Mermaid MCP for this session."
       │   → Fall back to Mermaid MCP.
       └── GOOGLE_API_KEY set → Proceed with PaperBanana.
```

### Tool Invocation

```
mcp__paperbanana__generate_diagram(
    source_context: "<methodology section text or relevant paper excerpt>",
    caption: "<Figure N. Descriptive caption for the methodology diagram>",
    iterations: 3
)
```

**Parameters**:
- `source_context`: The methodology text describing the research design, phases, participant flow, or conceptual framework. Provide enough context for the diagram to be self-explanatory.
- `caption`: APA-format figure caption. Must start with "Figure N." followed by an italic descriptive title.
- `iterations`: Refinement iterations (default 3). Use 2 for simple diagrams, 3 for standard, 4-5 for complex multi-phase designs.

### Output Convention

- **Location**: `experiment_outputs/figures/` (same directory as matplotlib and Mermaid figures)
- **Naming**: `methodology_<description>.png` (e.g., `methodology_research_design.png`, `methodology_conceptual_framework.png`)
- **Format**: PNG (returned directly by MCP server)
- **Numbering**: Numbered in the same sequence as all other figures (use `fig_counter`)
- **Caption**: APA-format: "**Figure N.** *Description in italics.*"

### When Agents Should Generate Methodology Diagrams

| Agent | Context | Trigger |
|-------|---------|---------|
| `draft_writer_agent` (academic-paper) | Writing the Methods section | When the methodology has 3+ phases, mixed methods, or a conceptual framework that benefits from visual representation |
| `protocol_compiler_agent` (experiment-designer) | Compiling experiment protocol | When the experiment design involves multi-stage interventions or complex participant allocation |

### Graceful Degradation

If PaperBanana is unavailable (MCP not connected or no API key):
1. Fall back to Mermaid MCP for a simplified structural diagram
2. Add a note in the figure caption: "Diagram generated using Mermaid; a higher-fidelity methodology diagram can be produced with PaperBanana MCP."
3. Continue the pipeline without blocking — PaperBanana is always optional

---

## 11. Google Colab MCP — GPU-Accelerated Computation

The Google Colab MCP server (`mcp__colab-proxy-mcp__open_colab_browser_connection`) enables offloading heavy computational workloads to Google Colab with GPU acceleration. This is used when local execution would be impractically slow or when GPU is required.

### Scope — When to Offload to Colab

| Offload to Colab | Keep Local |
|-------------------|------------|
| Monte Carlo simulations with >50,000 iterations AND complex DGPs | Simple bootstrap (N < 10,000) |
| Parameter sweeps with >1,000 grid cells | Standard statistical tests (t-test, ANOVA, regression) |
| SEM/CFA with >50 parameters or N > 10,000 | Descriptive statistics, assumption checks |
| Bootstrap resampling with N > 100,000 | Single-run simulations in `quick` mode |
| Agent-based models with >10,000 agents | Standard power analysis via `statsmodels` |
| Any workload estimated to exceed 10 minutes locally | Visualization/plotting code |
| Deep learning or neural network model fitting | Data cleaning and transformation |

**Rule**: Default to local execution. Only suggest Colab when the workload clearly exceeds local capacity. When in doubt, try locally first — if it fails or takes too long, then suggest Colab.

### Human-in-the-Loop Protocol (MANDATORY)

Colab requires human authentication and manual GPU runtime configuration. The agent CANNOT do this autonomously. Follow this exact protocol:

```
COLAB OFFLOAD PROTOCOL — Human-in-the-Loop

Step 1: NOTIFY — Alert the user that GPU computation is needed
  ├── Play an audible alert:
  │   Bash: powershell -c "[console]::beep(800,300); Start-Sleep -m 200; [console]::beep(1000,300); Start-Sleep -m 200; [console]::beep(1200,500)"
  │   (Three ascending beeps: 800Hz, 1000Hz, 1200Hz)
  │
  ├── Display a prominent message:
  │   ┌─────────────────────────────────────────────────────┐
  │   │  🔔 HUMAN ACTION REQUIRED — Google Colab Setup      │
  │   │                                                     │
  │   │  The upcoming computation is too heavy for local    │
  │   │  execution and needs GPU acceleration via Colab.    │
  │   │                                                     │
  │   │  Please complete these steps:                       │
  │   │  1. Open Google Colab in your browser               │
  │   │  2. Sign in with your Google account                │
  │   │  3. Change runtime: Runtime → Change runtime type   │
  │   │     → Select GPU (T4 or higher)                     │
  │   │  4. Connect to the runtime (click "Connect")        │
  │   │  5. Come back here and confirm: "ready" or "skip"   │
  │   │                                                     │
  │   │  Estimated compute time: [X minutes]                │
  │   │  Reason: [why local won't work]                     │
  │   └─────────────────────────────────────────────────────┘
  │
  └── PAUSE — Wait for user response. Do NOT proceed until user says "ready" or "skip".

Step 2: BRANCH on user response
  ├── User says "ready" / "done" / "go" / "yes" →
  │   └── Call mcp__colab-proxy-mcp__open_colab_browser_connection()
  │       ├── Returns true → Proceed to Step 3
  │       └── Returns false → Report connection failure, ask user to retry or skip
  │
  ├── User says "skip" / "no" / "local" →
  │   └── Fall back to local execution with warnings:
  │       - "Running locally. This may take [estimated time]. Consider Colab for faster results."
  │       - Reduce iterations if possible (e.g., 10,000 → 2,000 with wider MCSE threshold)
  │       - Log in lab notebook that local execution was used despite GPU recommendation
  │
  └── User says "cancel" →
      └── Abort the computation step, continue pipeline without results

Step 3: EXECUTE on Colab
  ├── Transfer the simulation/analysis script to the Colab notebook
  ├── Ensure all dependencies are installed (pip install in first cell)
  ├── Run the computation
  ├── Retrieve results back to local experiment_outputs/
  └── Log execution environment in Material Passport:
      - runtime: "Google Colab"
      - gpu_type: [as reported by Colab]
      - execution_time: [actual]
```

### Beep Sound Cross-Platform Reference

The notification beep must work on the user's platform:

```
Windows (PowerShell):
  powershell -c "[console]::beep(800,300); Start-Sleep -m 200; [console]::beep(1000,300); Start-Sleep -m 200; [console]::beep(1200,500)"

macOS:
  osascript -e 'beep 3'

Linux:
  for freq in 800 1000 1200; do (speaker-test -t sine -f $freq -l 1 &) ; sleep 0.3 ; kill $! 2>/dev/null; done

Fallback (if none work):
  printf '\a\a\a'
```

Agents should detect the platform from the environment and use the appropriate command. On Windows, use the PowerShell variant.

### Workload Estimation Heuristic

Before suggesting Colab, estimate local execution time:

```
Estimated local time (rough heuristic):

Monte Carlo:
  time ≈ (n_iterations × single_iteration_ms) / (n_cores × 0.7)
  → If time > 10 min → suggest Colab

Bootstrap:
  time ≈ (n_bootstrap × n_observations × 0.001ms) / (n_cores × 0.7)
  → If time > 10 min → suggest Colab

Parameter sweep:
  time ≈ (n_cells × n_per_cell × single_iteration_ms) / (n_cores × 0.7)
  → If time > 10 min → suggest Colab

SEM/CFA:
  → If n_parameters > 50 AND n_observations > 10,000 → suggest Colab
  → If model fails to converge locally → suggest Colab with more memory

Agent-based model:
  → If n_agents > 10,000 → suggest Colab
```

### Graceful Degradation

If Colab is unavailable (MCP not connected, user skips, connection fails):
1. Fall back to local execution
2. Reduce computational load where safe (fewer iterations with wider thresholds, smaller parameter grids)
3. Log the degradation in the lab notebook and Material Passport
4. Add a note in the report: "Computation was performed locally; results may benefit from increased iterations with GPU acceleration."
5. Never block the pipeline — Colab is always optional
