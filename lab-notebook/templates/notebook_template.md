# Lab Notebook — [Experiment Title]

## Header

| Field | Value |
|-------|-------|
| **Experiment ID** | [EXP-YYYYMMDD-NNN] |
| **Title** | [Descriptive experiment title] |
| **Authors** | [Name 1 (role), Name 2 (role)] |
| **Created** | [YYYY-MM-DD HH:MM] |
| **Last Modified** | [YYYY-MM-DD HH:MM] |
| **Status** | [active / completed / archived] |
| **Timezone** | [UTC offset, e.g., UTC+8] |
| **Protocol Reference** | [Path to Schema 10 document or protocol file, if available] |
| **Design Type** | [From Schema 10 design_type, if available] |

**Notebook File**: [experiment_outputs/logs/notebook_YYYY-MM-DD_short-name.md]

---

## Design Record

> This section documents the experiment design as specified at the start of the study. It captures hypotheses, variables, sample plan, analysis plan, and validity considerations. Entries here are primarily sourced from Schema 10 (Experiment Design) or equivalent user specifications.
>
> All entries in this section use entry type: `design`.

---

## Environment Record

> This section documents the computational and physical environment in which the experiment is conducted. Software versions, hardware specifications, operating system, random seeds, and package manifests are recorded here for reproducibility.
>
> All entries in this section use entry type: `note` (subtype: environment).

---

## Data Collection Log

> This section contains chronological entries for each data collection event. Each entry records what was collected, from whom, the count, instrument used, conditions, and any observations during collection.
>
> All entries in this section use entry type: `collection`.

---

## Data Preparation Log

> This section documents data cleaning, transformation, and exclusion steps. Each entry records the input data, transformations applied, exclusions with reasons, and the output data. This creates a traceable lineage from raw data to analysis-ready datasets.
>
> All entries in this section use entry type: `preparation`.

---

## Analysis Log

> This section records each statistical analysis performed. Each entry documents the hypothesis tested, the statistical test used, assumption checks, results, effect sizes, and interpretation. Entries may be sourced from Schema 11 (Experiment Results) or manual analysis.
>
> All entries in this section use entry type: `analysis`.

---

## Simulation Log

> This section records simulation runs including parameter configurations, iteration counts, convergence status, and results. Used when the experiment involves Monte Carlo simulations, bootstrap procedures, power analyses, or other computational studies.
>
> All entries in this section use entry type: `simulation`.
>
> _If no simulations are planned for this experiment, this section may remain empty. Its completeness weight is redistributed to Design Record and Analysis Log during auditing._

---

## Deviation Log

> This section records all protocol deviations — any departure from the original experiment design. Each deviation entry includes what changed, the original plan, what actually happened, the reason, an impact assessment (internal, external, and statistical validity), severity classification, and whether the analysis plan needs updating.
>
> All entries in this section use entry type: `deviation`.
>
> _If no deviations have occurred, this section remains empty (which is a positive finding at audit time)._

---

## Decision Log

> This section records methodological decisions made during the experiment lifecycle. Each entry documents the decision, alternatives considered, rationale, and downstream impact. Decisions may be prompted by deviations, unexpected findings, or practical constraints.
>
> All entries in this section use entry type: `decision`.

---

## File Manifest

> This section provides a complete inventory of all experiment artifacts (data files, scripts, outputs, figures, tables). Each file is recorded with its path, purpose, SHA-256 hash, creation timestamp, producing agent or process, and upstream dependencies.
>
> The manifest is maintained by the provenance_auditor_agent and updated during audits.

| # | File Path | Purpose | SHA-256 Hash | Created | Producer | Dependencies |
|---|-----------|---------|-------------|---------|----------|-------------|
| | | | | | | |

**Hash Generation**: SHA-256 hashes are computed using Python `hashlib` on the raw file bytes. See `references/provenance_tracking_guide.md` for the hashing procedure.

---

_End of notebook. Audit Trail entries are appended below after each provenance audit._
