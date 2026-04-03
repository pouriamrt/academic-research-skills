---
name: lab-notebook
description: "Research record keeper — 4-agent team for rigorous experiment lifecycle documentation. 6 modes: full notebook creation, log entry, deviation recording, experiment snapshot, notebook export, and audit. Tracks experiment design, data collection, analysis, deviations, decisions, and file provenance with SHA-256 hashing. Produces Schema 12 (Lab Record) for downstream handoff to academic-paper. Triggers on: lab notebook, log experiment, record deviation, experiment log, track experiment, research record, audit notebook, export notebook, experiment snapshot, 實驗紀錄, 記錄偏差, 實驗日誌, 追蹤實驗, 研究紀錄, 審計紀錄, 匯出紀錄."
metadata:
  version: "1.0"
  last_updated: "2026-03-16"
---

# Lab Notebook — Research Record Keeper

Research record keeper — a 4-agent team for rigorous experiment lifecycle documentation. v1.0 provides full notebook creation, structured log entries, protocol deviation tracking, provenance auditing with SHA-256 hashing, and Schema 12 handoff to downstream skills.

## Quick Start

**Create a full notebook from an experiment design:**
```
Create a lab notebook for experiment EXP-20260316-001
```

**Log a single entry to an existing notebook:**
```
Log a data collection entry: collected survey responses from 45 participants in Section A today
```

**Record a deviation:**
```
Record deviation: sample fell below target N=195, actual N=180 due to higher attrition
```

**Audit a notebook:**
```
Audit notebook experiment_outputs/logs/notebook_2026-03-16_ai-assessment.md
```

**Export a notebook:**
```
Export notebook for EXP-20260316-001 as Schema 12 handoff
```

---

## Trigger Conditions

### Trigger Keywords

**English**: lab notebook, log experiment, record deviation, experiment log, track experiment, research record, audit notebook, export notebook, experiment snapshot

**繁體中文**: 實驗紀錄, 記錄偏差, 實驗日誌, 追蹤實驗, 研究紀錄, 審計紀錄, 匯出紀錄

### Does NOT Trigger

| Scenario | Use Instead |
|----------|-------------|
| Designing an experiment (not recording) | `experiment-designer` |
| Running statistical analysis | `data-analyst` |
| Running simulations | `simulation-runner` |
| Writing a paper from results | `academic-paper` |
| Full research-to-paper pipeline | `academic-pipeline` |

### Quick Mode Selection Guide

| Your Situation | Recommended Mode |
|----------------|-----------------|
| Starting a new experiment, need full notebook | `full` |
| Existing notebook, need to add an entry | `log-entry` |
| Protocol deviation occurred | `deviation` |
| Need a point-in-time status capture | `snapshot` |
| Need to hand off to academic-paper | `export` |
| Need to verify notebook completeness | `audit` |

---

## Agent Team (4 Agents)

| # | Agent | Role | Modes |
|---|-------|------|-------|
| 1 | `notebook_manager_agent` | Creates/manages notebook files, mode routing, entry ID sequencing, status tracking | All modes |
| 2 | `entry_writer_agent` | Writes structured log entries, auto-detects entry type, cross-references entries and files | log-entry, full |
| 3 | `deviation_tracker_agent` | Records protocol deviations with impact assessment and severity classification | deviation, full |
| 4 | `provenance_auditor_agent` | Audits completeness, verifies file provenance, computes hashes, produces Schema 12 | audit, export, full |

---

## Notebook Structure (10 Sections)

Every notebook instantiated from `templates/notebook_template.md` contains exactly these sections:

| # | Section | Description |
|---|---------|-------------|
| 1 | Header | Experiment ID, title, authors, dates, status, links to protocol |
| 2 | Design Record | Experiment design summary from Schema 10 (hypotheses, variables, sample plan) |
| 3 | Environment Record | Software versions, hardware specs, OS, random seeds, package manifests |
| 4 | Data Collection Log | Chronological entries for each data collection event |
| 5 | Data Preparation Log | Data cleaning, transformation, exclusion entries |
| 6 | Analysis Log | Statistical analyses performed, assumption checks, results |
| 7 | Simulation Log | Simulation runs, parameter configurations, convergence results |
| 8 | Deviation Log | Protocol deviations with impact assessments |
| 9 | Decision Log | Methodological decisions with rationale and alternatives considered |
| 10 | File Manifest | Inventory of all experiment artifacts with SHA-256 hashes |

An **Audit Trail** section is appended at the end whenever a provenance audit is performed.

---

## Entry Format

All entries across all sections use this canonical format:

```markdown
### Entry [NB-XXX] -- YYYY-MM-DD HH:MM

- **Type**: [design | collection | preparation | analysis | simulation | deviation | decision | note]
- **Author**: [person or agent that produced this entry]
- **Related Entries**: [NB-YYY, NB-ZZZ] or "None"
- **Related Files**: [file paths] or "None"

[Content — type-specific fields and narrative]
```

**Entry ID rules**:
- Sequential within a notebook: NB-001, NB-002, NB-003, ...
- IDs are never reused or reassigned, even if entries are superseded
- Cross-references use the NB-XXX format

**Timestamp rules**:
- All timestamps in ISO 8601 format: `YYYY-MM-DD HH:MM` (local time with timezone note in Header)
- Entries are append-only; existing entries are never modified (corrections create new entries referencing the original)

---

## Entry Types (8 Types)

| Type | Purpose | Required Fields | Target Section |
|------|---------|----------------|----------------|
| `design` | Record experiment design decisions | Schema 10 fields, hypotheses, variables | Design Record |
| `collection` | Log data collection events | What collected, from whom, N, instrument, conditions | Data Collection Log |
| `preparation` | Log data cleaning/transformation | Transformations applied, exclusions, before/after counts | Data Preparation Log |
| `analysis` | Log analysis execution and results | Test, result, assumption checks, interpretation | Analysis Log |
| `simulation` | Log simulation runs | Parameters, iterations, convergence, results | Simulation Log |
| `deviation` | Record protocol deviations | Original plan, actual, reason, impact assessment, severity | Deviation Log |
| `decision` | Record methodological decisions | Decision, alternatives considered, rationale, impact | Decision Log |
| `note` | Free-form observation or annotation | Content (no required fields beyond the standard header) | Appended to most relevant section |

See `templates/entry_template.md` for type-specific templates.

---

## Mode Definitions

### `full` — Create Complete Notebook

Creates a new notebook from scratch. Requires a Schema 10 (Experiment Design) or equivalent user description of the experiment.

**Agents active**: All 4
**Workflow**:
```
User: "Create a lab notebook for [experiment]"
     |
     +-> [notebook_manager_agent]
     |   - Validate Schema 10 input (or prompt user for key fields)
     |   - Instantiate notebook from templates/notebook_template.md
     |   - Create file: experiment_outputs/logs/notebook_YYYY-MM-DD_name.md
     |   - Set status: active
     |
     +-> [entry_writer_agent]
     |   - Write NB-001: Design Record entry (from Schema 10)
     |   - Write NB-002: Environment Record entry
     |   - Write NB-003+: Any initial entries from user input
     |
     +-> [provenance_auditor_agent]
         - Initial audit: verify Design Record completeness
         - Generate initial file manifest
         - Report initial completeness score
```

**Output**: Notebook file at `experiment_outputs/logs/notebook_YYYY-MM-DD_name.md`

### `log-entry` — Add Entry to Existing Notebook

Adds a single structured entry to an existing notebook.

**Agents active**: notebook_manager_agent, entry_writer_agent
**Precondition**: Notebook file must exist
**Workflow**:
```
User: "Log [entry description]"
     |
     +-> [notebook_manager_agent]
     |   - Locate existing notebook (by experiment ID or path)
     |   - Validate notebook exists and is active
     |   - Determine next entry ID (NB-XXX)
     |
     +-> [entry_writer_agent]
         - Parse input: Schema 10, Schema 11, or free text
         - Auto-detect entry type from content
         - Cross-reference related entries and files
         - Append entry to correct section
```

### `deviation` — Record Protocol Deviation

Records a protocol deviation with full impact assessment.

**Agents active**: notebook_manager_agent, deviation_tracker_agent
**Precondition**: Notebook file must exist
**Workflow**:
```
User: "Record deviation: [description]"
     |
     +-> [notebook_manager_agent]
     |   - Locate existing notebook
     |   - Determine next entry ID
     |
     +-> [deviation_tracker_agent]
         - Extract: what changed, why, when discovered
         - Cross-reference original protocol (Schema 10)
         - Show planned vs. actual
         - Assess impact: internal validity, external validity, statistical validity
         - Classify severity: minor / major / critical
         - Determine if analysis plan needs updating
         - Append to Deviation Log
```

### `snapshot` — Point-in-Time Status Capture

Captures a point-in-time snapshot of the experiment's state.

**Agents active**: notebook_manager_agent, provenance_auditor_agent
**Precondition**: Notebook file must exist
**Workflow**:
```
User: "Snapshot experiment [ID]"
     |
     +-> [notebook_manager_agent]
     |   - Locate existing notebook
     |
     +-> [provenance_auditor_agent]
         - Count entries by type and section
         - List recent entries (last 5)
         - List open deviations
         - Compute current completeness score
         - Report experiment progress status
```

**Output**: Status summary (not written to notebook; displayed to user)

### `export` — Generate Schema 12 Handoff

Produces the Schema 12 (Lab Record) artifact for handoff to academic-paper or academic-pipeline.

**Agents active**: notebook_manager_agent, provenance_auditor_agent
**Precondition**: Notebook file must exist
**Workflow**:
```
User: "Export notebook for [experiment ID]"
     |
     +-> [notebook_manager_agent]
     |   - Locate existing notebook
     |   - Validate notebook status (active or completed)
     |
     +-> [provenance_auditor_agent]
         - Full audit (see audit mode)
         - Generate file manifest with SHA-256 hashes
         - Generate methods_summary narrative
         - Produce Schema 12 artifact
         - Attach Material Passport (Schema 9)
```

**Output**: Schema 12 Lab Record artifact

### `audit` — Verify Notebook Completeness

Performs a full completeness and provenance audit of the notebook.

**Agents active**: notebook_manager_agent, provenance_auditor_agent
**Precondition**: Notebook file must exist
**Workflow**:
```
User: "Audit notebook [path or experiment ID]"
     |
     +-> [notebook_manager_agent]
     |   - Locate existing notebook
     |
     +-> [provenance_auditor_agent]
         - Check all 10 sections for content
         - Verify all data files have provenance (hash, source, date)
         - Verify Schema 10 fields in Design Record
         - Compute completeness score (0.0-1.0, weighted)
         - Generate audit report (templates/audit_checklist_template.md)
         - Append Audit Trail entry to notebook
```

**Output**: Audit report with completeness score

---

## Operational Modes Summary

| Mode | Agents Active | Output | Precondition |
|------|---------------|--------|--------------|
| `full` | All 4 | New notebook file + initial entries + audit | Schema 10 or user description |
| `log-entry` | Manager + Entry Writer | Appended entry in notebook | Existing notebook |
| `deviation` | Manager + Deviation Tracker | Deviation entry with impact assessment | Existing notebook |
| `snapshot` | Manager + Auditor | Status summary (displayed) | Existing notebook |
| `export` | Manager + Auditor | Schema 12 Lab Record artifact | Existing notebook |
| `audit` | Manager + Auditor | Audit report + completeness score | Existing notebook |

---

## "Never the Entry Point" Rule

The `lab-notebook` skill is **never the entry point** for a new research project. It is a record-keeping companion.

- **`full` mode** is used to create a notebook for an experiment that has already been designed (via `experiment-designer` or manual specification).
- **All other modes** (`log-entry`, `deviation`, `snapshot`, `export`, `audit`) operate on an **existing notebook only**.
- If a user asks to "start an experiment," route them to `experiment-designer` first, then return to `lab-notebook` (full mode) with the Schema 10 output.

Exception: Users may create a notebook from a free-text experiment description (without a formal Schema 10), but the notebook_manager_agent will prompt for key missing fields.

---

## Completeness Score Calculation

The provenance_auditor_agent computes a weighted completeness score:

| Section | Weight | Scoring Criteria |
|---------|--------|-----------------|
| Design Record | 20% | Schema 10 fields present: hypotheses, variables, sample, analysis plan |
| Environment Record | 5% | Software versions, OS, seeds documented |
| Data Collection Log | 15% | At least one collection entry per planned data source |
| Data Preparation Log | 10% | At least one preparation entry if data was collected |
| Analysis Log | 20% | At least one analysis entry per primary hypothesis |
| Simulation Log | 0% (conditional) | Weight redistributed if no simulations planned; 10% if planned |
| Deviation Log | 10% | All known deviations documented with impact assessments |
| Decision Log | 5% | Key methodological decisions documented |
| File Manifest | 15% | All referenced files have hashes; no orphaned references |

**Score interpretation**:
- **0.90-1.00**: Excellent — ready for export and paper writing
- **0.70-0.89**: Good — minor gaps, acceptable for most purposes
- **0.50-0.69**: Incomplete — significant gaps that should be addressed
- **Below 0.50**: Poor — notebook needs substantial work before use

---

## Dependencies

### Python Packages

No additional virtual environment packages required. Uses only Python standard library:
- `hashlib` — SHA-256 file hashing for provenance verification

### Integration

**Upstream (inputs)**:
- **Schema 10** (Experiment Design) from `experiment-designer` — used to populate Design Record
- **Schema 11** (Experiment Results) from `data-analyst` or `simulation-runner` — used to write analysis/simulation entries

**Downstream (outputs)**:
- **Schema 12** (Lab Record) to `academic-paper` or `academic-pipeline` — produced by `provenance_auditor_agent` in export mode

---

## Failure Paths

| # | Failure Scenario | Trigger Condition | Recovery Strategy |
|---|---------|---------|---------|
| F1 | Notebook not found | User references non-existent notebook (non-full modes) | Prompt user for correct path or experiment ID; offer to create new notebook |
| F2 | Schema 10 missing critical fields | full mode input lacks hypotheses or variables | Prompt user for missing fields; proceed with partial notebook if user confirms |
| F3 | File hash mismatch | Audit detects file content changed since last hash | Flag file as MODIFIED, update hash, log deviation if content change is substantive |
| F4 | Duplicate entry ID | ID collision (should not happen with sequential logic) | Re-scan notebook, find max ID, assign next sequential |
| F5 | Notebook status is archived | User tries to add entry to archived notebook | Warn user; require explicit confirmation to reactivate |
| F6 | Referenced file missing | File in manifest no longer exists at declared path | Flag in audit report; do not remove from manifest (preserve provenance record) |

---

## Agent File References

| Agent | Definition File |
|-------|----------------|
| notebook_manager_agent | `agents/notebook_manager_agent.md` |
| entry_writer_agent | `agents/entry_writer_agent.md` |
| deviation_tracker_agent | `agents/deviation_tracker_agent.md` |
| provenance_auditor_agent | `agents/provenance_auditor_agent.md` |

---

## Template Files

| Template | Purpose |
|----------|---------|
| `templates/notebook_template.md` | Master notebook scaffold with all 10 sections |
| `templates/entry_template.md` | Per-type entry templates for all 8 entry types |
| `templates/audit_checklist_template.md` | Completeness checklist with weighted scoring |
| `templates/file_manifest_template.md` | Artifact inventory table with hash instructions |

---

## Reference Files

| Reference | Purpose | Used By |
|-----------|---------|---------|
| `references/lab_notebook_best_practices.md` | Research record standards, legal requirements, contemporaneous recording | All agents |
| `references/reproducibility_standards.md` | FAIR principles, TOP guidelines, computational reproducibility | provenance_auditor, entry_writer |
| `references/deviation_handling_guide.md` | Deviation types, impact assessment, corrective actions | deviation_tracker |
| `references/provenance_tracking_guide.md` | SHA-256 hashing, version tracking, staleness detection | provenance_auditor |

---

## Examples

| Example | Demonstrates |
|---------|-------------|
| `examples/full_notebook_example.md` | Complete notebook lifecycle: design through audit with Schema 12 export |

---

## Output Language

Follows the user's language. Technical terminology (entry types, section names, field names) kept in English for cross-skill interoperability.

---

## Quality Standards

1. **Append-only** — existing entries are never modified; corrections create new entries referencing the original
2. **Contemporaneous recording** — entries should be created as close to the event as possible
3. **Complete provenance** — every data file must have a hash, source, and creation timestamp in the manifest
4. **Cross-referencing** — entries reference related entries (NB-XXX) and related files
5. **Schema compliance** — Design Record must contain all Schema 10 required fields; export must produce valid Schema 12
6. **Audit trail** — every audit appends a timestamped Audit Trail entry to the notebook
7. **Deviation accountability** — every protocol deviation must have an impact assessment and severity classification

---

## Integration with Other Skills

```
experiment-designer (Schema 10) -> lab-notebook (full)     -> Create notebook from design
data-analyst (Schema 11)        -> lab-notebook (log-entry) -> Log analysis results
simulation-runner (Schema 11)   -> lab-notebook (log-entry) -> Log simulation results
lab-notebook (export, Schema 12) -> academic-paper          -> Methods section + provenance
lab-notebook (export, Schema 12) -> academic-pipeline       -> Pipeline orchestration
```

### Auto-Logging Protocol (Pipeline Mode)

When experiment skills execute within the academic-pipeline, they automatically log their activities to the active notebook via append-only file operations at designated phase endpoints. This auto-logging happens **without invoking lab-notebook agents**, avoiding circular dependencies. The `provenance_auditor_agent` validates all auto-logged entries during `audit` or `export` mode. When running standalone (outside the pipeline), auto-logging is disabled. See `shared/experiment_infrastructure.md` Section 6 for the full protocol.

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-03-16 | Initial release: 4 agents, 6 modes, 10-section notebook structure, Schema 10/11 intake, Schema 12 export, SHA-256 provenance, weighted completeness scoring |
