# Audit Checklist Template — Notebook Completeness Verification

## Purpose

This template is used by the provenance_auditor_agent to perform a structured completeness audit of a lab notebook. The checklist covers section presence, content adequacy, cross-referencing integrity, file provenance, and a weighted completeness score calculation.

---

## Audit Metadata

| Field | Value |
|-------|-------|
| **Notebook Path** | [experiment_outputs/logs/notebook_YYYY-MM-DD_name.md] |
| **Experiment ID** | [EXP-YYYYMMDD-NNN] |
| **Audit Date** | [YYYY-MM-DD HH:MM] |
| **Auditor** | provenance_auditor_agent |
| **Notebook Status** | [active / completed / archived] |
| **Total Entries** | [count] |
| **Previous Audit Date** | [date or "First audit"] |

---

## Section 1: Header Completeness

- [ ] Experiment ID is present and matches expected format (EXP-YYYYMMDD-NNN)
- [ ] Title is descriptive and non-empty
- [ ] Authors are listed with roles
- [ ] Created timestamp is ISO 8601 format
- [ ] Last Modified timestamp is ISO 8601 format and >= Created
- [ ] Status is one of: active, completed, archived
- [ ] Timezone is declared
- [ ] Protocol Reference is present (if Schema 10 exists)
- [ ] Design Type is present (if Schema 10 exists)

**Header Score**: [fields_present / total_applicable] = [0.0-1.0]

---

## Section 2: Design Record

- [ ] Section heading exists
- [ ] At least one `design` type entry is present
- [ ] Experiment design type is documented
- [ ] Hypotheses are listed with IDs, statements, and directions
- [ ] Variables are documented (IV, DV, controls with operationalization)
- [ ] Sample plan is documented (target N, power, alpha, effect size)
- [ ] Analysis plan is documented (primary analysis per hypothesis)
- [ ] Validity threats are documented (at least 2 with mitigations)
- [ ] Timeline milestones are documented

**Schema 10 Required Fields Check**:
| Field | Present | Notes |
|-------|---------|-------|
| experiment_id | [ ] | |
| design_type | [ ] | |
| hypotheses | [ ] | Count: [N] |
| variables (IV) | [ ] | Count: [N] |
| variables (DV) | [ ] | Count: [N] |
| variables (control) | [ ] | Count: [N] |
| sample.target_n | [ ] | |
| sample.power | [ ] | |
| sample.alpha | [ ] | |
| analysis_plan.primary | [ ] | |
| validity_threats | [ ] | Count: [N] |
| timeline | [ ] | |

**Design Record Score**: [fields_present / 12] = [0.0-1.0]
**Section Weight**: 20% (25% if no simulations planned)

---

## Section 3: Environment Record

- [ ] Section heading exists
- [ ] At least one environment entry is present
- [ ] Python version documented
- [ ] Key package versions documented (e.g., pandas, scipy, statsmodels)
- [ ] Operating system documented
- [ ] Random seed(s) documented (if applicable)
- [ ] Hardware specifications documented (if relevant)

**Environment Record Score**: [criteria_met / applicable_criteria] = [0.0-1.0]
**Section Weight**: 5%

---

## Section 4: Data Collection Log

- [ ] Section heading exists
- [ ] At least one `collection` type entry is present
- [ ] Each planned data source has at least one collection entry
- [ ] Collection entries include: instrument, participants, count, conditions
- [ ] Total collected N is documented

**Expected data sources**: [list from Design Record]
**Documented data sources**: [list from collection entries]
**Coverage**: [documented / expected] = [0.0-1.0]

**Data Collection Log Score**: [coverage ratio] = [0.0-1.0]
**Section Weight**: 15%

---

## Section 5: Data Preparation Log

- [ ] Section heading exists
- [ ] At least one `preparation` type entry is present (if data was collected)
- [ ] Input -> output data lineage is documented
- [ ] Exclusion criteria and counts are documented
- [ ] Missing data strategy is documented
- [ ] Final analysis-ready N is documented

**Data Preparation Log Score**:
- If data was collected and preparation entries exist: [criteria_met / total_criteria] = [0.0-1.0]
- If data was collected but no preparation entries: 0.0
- If no data collected yet: N/A (score = 1.0, not penalized)

**Section Weight**: 10%

---

## Section 6: Analysis Log

- [ ] Section heading exists
- [ ] At least one `analysis` type entry is present (if analyses have been run)
- [ ] Each primary hypothesis has at least one analysis entry
- [ ] Analysis entries include assumption checks
- [ ] Analysis entries include effect sizes with CIs
- [ ] APA-formatted result strings are present

**Primary hypothesis coverage**:
| Hypothesis | Analysis Entry | Status |
|-----------|---------------|--------|
| H1 | [NB-XXX or "Missing"] | [covered / missing] |
| H2 | [NB-XXX or "Missing"] | [covered / missing] |
| ... | ... | ... |

**Analysis Log Score**: [hypotheses_covered / total_primary_hypotheses] = [0.0-1.0]
**Section Weight**: 20% (25% if no simulations planned)

---

## Section 7: Simulation Log

- [ ] Section heading exists
- [ ] Simulations were planned in Design Record: [yes / no]
- [ ] If planned: at least one `simulation` type entry is present
- [ ] Simulation entries include parameters, iterations, convergence status
- [ ] Simulation entries include results with interpretation

**Simulation Log Score**:
- If simulations planned and entries exist: [criteria_met / total_criteria] = [0.0-1.0]
- If simulations planned but no entries: 0.0
- If no simulations planned: N/A (weight redistributed)

**Section Weight**: 10% if simulations planned; 0% if not (redistributed: +5% Design Record, +5% Analysis Log)

---

## Section 8: Deviation Log

- [ ] Section heading exists
- [ ] All known deviations are documented
- [ ] Each deviation entry has a severity classification
- [ ] Each deviation entry has an impact assessment (all 3 validity types)
- [ ] Each deviation entry has planned vs. actual comparison
- [ ] If compound deviations exist: compound assessment is documented
- [ ] If analysis plan updates required: updates are documented

**Known deviations** (from entries, team reports, audit findings): [count]
**Documented deviations**: [count]
**Deviation coverage**: [documented / known] = [0.0-1.0]

**Deviation Log Score**: [deviation_coverage] = [0.0-1.0]
- If no deviations known AND no deviations documented: 1.0 (no deviations is a valid state)

**Section Weight**: 10%

---

## Section 9: Decision Log

- [ ] Section heading exists
- [ ] At least one `decision` type entry is present
- [ ] Decision entries include alternatives considered
- [ ] Decision entries include rationale

**Decision Log Score**:
- If at least one decision entry with required fields: 1.0
- If decision entries exist but lack required fields: 0.5
- If no decision entries: 0.0

**Section Weight**: 5%

---

## Section 10: File Manifest

- [ ] Section heading exists
- [ ] File manifest table is present and non-empty
- [ ] All files referenced in notebook entries appear in the manifest
- [ ] All manifest entries have: path, purpose, SHA-256 hash, created date, producer
- [ ] No orphaned manifest entries (files in manifest but never referenced)

**File provenance check**:
| File | In Manifest | Has Hash | Hash Valid | Has Date | Has Producer |
|------|------------|----------|-----------|----------|-------------|
| [path] | [Y/N] | [Y/N] | [Y/N/Unchecked] | [Y/N] | [Y/N] |

**Files with complete provenance**: [count] / [total referenced files]
**Files missing from manifest**: [count] (list paths)
**Orphaned manifest entries**: [count] (list paths)
**Hash mismatches detected**: [count] (list paths)

**File Manifest Score**: [files_with_complete_provenance / total_referenced_files] = [0.0-1.0]
**Section Weight**: 15%

---

## Cross-Reference Integrity

- [ ] All `NB-XXX` references in entries point to existing entries
- [ ] All file paths in "Related Files" fields exist (or are in File Manifest)
- [ ] Deviation entries reference the original Design Record
- [ ] Analysis entries reference their input Preparation entries
- [ ] Decision entries reference the entries that prompted them

**Broken entry references**: [count] (list: [NB-XXX referenced in NB-YYY but does not exist])
**Broken file references**: [count] (list: [path referenced in NB-XXX but does not exist])

---

## Completeness Score Calculation

### Weight Table

| Section | Base Weight | Adjusted Weight (no sims) | Section Score | Weighted Score |
|---------|-----------|--------------------------|---------------|---------------|
| Design Record | 20% | 25% | [0.0-1.0] | [weight * score] |
| Environment Record | 5% | 5% | [0.0-1.0] | [weight * score] |
| Data Collection Log | 15% | 15% | [0.0-1.0] | [weight * score] |
| Data Preparation Log | 10% | 10% | [0.0-1.0] | [weight * score] |
| Analysis Log | 20% | 25% | [0.0-1.0] | [weight * score] |
| Simulation Log | 10% | 0% | [0.0-1.0] | [weight * score] |
| Deviation Log | 10% | 10% | [0.0-1.0] | [weight * score] |
| Decision Log | 5% | 5% | [0.0-1.0] | [weight * score] |
| File Manifest | 15% | 15% | [0.0-1.0] | [weight * score] |
| **Total** | **100%** | **100%** | | **[sum]** |

### Completeness Score: **[0.00]**

### Interpretation

| Score Range | Interpretation | Recommendation |
|------------|---------------|----------------|
| 0.90 - 1.00 | Excellent | Ready for Schema 12 export and paper writing |
| 0.70 - 0.89 | Good | Minor gaps; acceptable for most purposes; address gaps if time permits |
| 0.50 - 0.69 | Incomplete | Significant gaps; address before proceeding to paper writing |
| Below 0.50 | Poor | Substantial work needed; list all gaps and prioritize |

---

## Recommendations

Priority actions to improve completeness:

1. **[HIGH]** [Specific action, e.g., "Add analysis entry for H2 — no analysis of self-efficacy outcome documented"]
2. **[HIGH]** [Specific action]
3. **[MEDIUM]** [Specific action]
4. **[LOW]** [Specific action]

---

## Audit Trail Entry

_The following entry is appended to the notebook's Audit Trail section:_

```markdown
## Audit Trail

### Audit [YYYY-MM-DD HH:MM]

- **Completeness Score**: [score]
- **Interpretation**: [Excellent / Good / Incomplete / Poor]
- **Files Verified**: [count]
- **Hash Mismatches**: [count]
- **Broken References**: [count]
- **Recommendations**: [count] ([HIGH]: [N], [MEDIUM]: [N], [LOW]: [N])
- **Previous Score**: [score or "First audit"]
- **Score Change**: [+/- delta or "N/A"]
```
