# Schema Migrations — Versioning and Migration Protocol

> This document defines the schema versioning protocol, migration rules, and staleness detection for all handoff artifacts in the academic-research-skills pipeline.

---

## 1. Schema Versioning Protocol

Every schema artifact (Schemas 1-17 as defined in `shared/handoff_schemas.md`) **MUST** include a `schema_version` field at the top level of the artifact.

### Version Format

- **Format**: `MAJOR.MINOR` (e.g., `1.0`, `2.1`)
- **MAJOR bump**: Breaking changes — field removed, field type changed, new required field added, field semantics altered incompatibly
- **MINOR bump**: Backwards-compatible changes — optional field added, description clarified, example updated, enum value added to an existing optional field

### Current Versions

| Schema | Name | Current Version | Established |
|--------|------|-----------------|-------------|
| Schema 1 | RQ Brief | 1.0 | v3.7.0 |
| Schema 2 | Bibliography | 1.0 | v3.7.0 |
| Schema 3 | Synthesis Report | 1.0 | v3.7.0 |
| Schema 4 | Paper Draft | 1.0 | v3.7.0 |
| Schema 5 | Integrity Report | 1.0 | v3.7.0 |
| Schema 6 | Review Report | 1.0 | v3.7.0 |
| Schema 7 | Revision Roadmap | 1.0 | v3.7.0 |
| Schema 8 | Response to Reviewers | 1.0 | v3.7.0 |
| Schema 9 | Material Passport | 1.0 | v3.7.0 |
| Schema 10 | Experiment Design | 1.0 | v3.7.0 |
| Schema 11 | Experiment Results | 1.0 | v3.7.0 |
| Schema 12 | Lab Record | 1.0 | v3.7.0 |
| Schema 13 | Simulation Specification | 1.0 | v3.7.0 |
| Schema 14 | Methodology Blueprint | 1.0 | v3.7.0 |
| Schema 15 | INSIGHT Collection | 1.0 | v3.7.0 |
| Schema 16 | Concept Lineage Report | 1.0 | v3.9.0 |
| Schema 17 | Style Profile | 1.0 | v3.9.0 |

---

## 2. Version Compatibility Matrix

| Plugin Version | Schema 1-13 | Schema 14-15 | Schema 16-17 | Notes |
|----------------|-------------|--------------|--------------|-------|
| v3.7.0 | v1.0 | v1.0 | — | Baseline — Schemas 1-15 established at v1.0 |
| v3.7.1–v3.8.x | v1.0 | v1.0 | — | No schema changes |
| v3.9.0+ | v1.0 | v1.0 | v1.0 | Schema 16 (Concept Lineage) + Schema 17 (Style Profile) added |

> **Reading this table**: Each row shows which schema versions that plugin version can produce and consume. A plugin version supports all schema versions from its row and all previous rows.

---

## 3. Migration Rules

When a consuming agent receives an artifact, it **MUST** check the `schema_version` field and apply the following logic:

### Migration Decision Flow

1. **Read** the `schema_version` field from the incoming artifact
2. **Compare** with the expected version for this schema (from the Current Versions table above)
3. **Decide**:
   - **Versions match**: Proceed normally
   - **Minor version gap** (e.g., received `1.0`, expected `1.1`): Check migration registry for applicable transform. If no migration exists, proceed with `WARN` — the artifact is forwards-compatible
   - **Major version gap** (e.g., received `1.0`, expected `2.0`): Check migration registry for applicable transform. If migration exists, apply it. If no migration exists, `FAIL` with `SCHEMA_VERSION_MISMATCH` — the artifact cannot be processed safely
   - **Missing `schema_version` field**: Treat as `1.0` (pre-versioning artifact from v3.7.0 era) with `WARN`

### Version Gap Direction

| Received vs Expected | Direction | Action |
|---------------------|-----------|--------|
| Received < Expected (minor) | Older minor | WARN, proceed (backwards-compatible) |
| Received < Expected (major) | Older major | Apply migration if available, else FAIL |
| Received = Expected | Match | Proceed |
| Received > Expected (minor) | Newer minor | WARN, proceed (ignore unknown optional fields) |
| Received > Expected (major) | Newer major | FAIL — consumer cannot handle unknown breaking changes |

---

## 4. Migration Registry

> Currently empty. No migrations are needed since all schemas are at v1.0 (baseline).

### Template for Future Migrations

When a schema version changes, add an entry below using this template:

```
### Migration: Schema N vX.Y -> vX.Z

**Date**: YYYY-MM-DD
**Plugin Version**: vA.B.C
**Reason**: [What changed and why]

**Transform**:
- Added field `new_field`: default value = "..."
- Renamed field `old_name` -> `new_name`
- Removed field `deprecated_field`: no replacement
- Changed field `field_name` type from X to Y: conversion rule = "..."
- Added enum value `new_value` to field `field_name`

**Affected Agents**:
- Producers: [list of agents that produce this schema]
- Consumers: [list of agents that consume this schema]

**Rollback**: [How to revert if migration causes issues]
```

### Example (for reference only — not an actual migration)

```
### Migration: Schema 1 v1.0 -> v2.0

**Date**: 2026-04-01
**Plugin Version**: v3.8.0
**Reason**: Added mandatory `paradigm` field to RQ Brief to support multi-paradigm research

**Transform**:
- Added field `paradigm`: default value = "not_specified"
- Renamed field `methodology_type` -> `methodology_approach`
- Removed field `exclusion_criteria`: moved to Schema 14 (Methodology Blueprint)

**Affected Agents**:
- Producers: deep-research/research_question_agent, deep-research/socratic_mentor_agent
- Consumers: deep-research/research_architect_agent, academic-paper/intake_agent, experiment-designer/intake_agent

**Rollback**: Revert to v3.7.x plugin; artifacts produced with v2.0 can be downgraded by removing `paradigm` field and renaming `methodology_approach` back to `methodology_type`
```

---

## 5. Adding Schema Version to Existing Artifacts

### Where the Field Goes

The `schema_version` field is a **top-level metadata field** in every schema artifact. It should appear immediately after the schema header.

### Format in Markdown Artifacts

```markdown
## RQ Brief

**Schema Version**: 1.0

**Research Question**: ...
```

### Format in Structured Objects

When the artifact is represented as structured data (e.g., in JSON-like handoff):

```
schema_version: "1.0"
research_question: "..."
sub_questions: [...]
```

### Producer Responsibility

Every agent that produces a schema artifact **MUST**:
1. Include `schema_version` as the first field after the artifact header
2. Set it to the current version from the Current Versions table in Section 1
3. Validate that all required fields for that schema version are present before handoff

### Consumer Responsibility

Every agent that consumes a schema artifact **MUST**:
1. Read `schema_version` before processing any other fields
2. Apply the Migration Decision Flow from Section 3
3. Log a warning if `schema_version` is missing (treat as `1.0`)
4. Reject the artifact with `SCHEMA_VERSION_MISMATCH` if a major version gap exists with no migration available

---

## 6. Staleness Detection Protocol

### Content Hash Verification

The Material Passport (Schema 9) includes an optional `content_hash` field. This protocol makes its use mandatory for staleness detection.

**Producer side**:
1. After producing the artifact content, compute SHA-256 hash of the full artifact text (excluding the Material Passport itself)
2. Store the hash in the Material Passport's `content_hash` field

**Consumer side**:
1. On receipt, compute SHA-256 hash of the received artifact content (excluding Material Passport)
2. Compare with `content_hash` in the accompanying Material Passport
3. If **mismatch**: the artifact was modified after the passport was issued -> emit `CONTENT_INTEGRITY_WARN`
4. If **match**: content integrity confirmed

### Freshness Rules

| Condition | Status | Action |
|-----------|--------|--------|
| Artifact age < 24 hours in active pipeline | FRESH | Proceed normally |
| Artifact age >= 24 hours in active pipeline | STALE | Emit `STALE_ARTIFACT_WARN`; recommend re-verification |
| Upstream artifact version changed after downstream was produced | STALE | Mark downstream as stale; recommend regeneration |
| `content_hash` mismatch | TAMPERED | Emit `CONTENT_INTEGRITY_WARN`; require re-verification |

### Refresh Policy

When an upstream artifact is updated (its `version_label` in the Material Passport changes):

1. **Identify** all downstream artifacts that consumed the previous version (check `upstream_dependencies` in their Material Passports)
2. **Mark** each downstream artifact's Material Passport as `verification_status: "STALE"`
3. **Notify** the pipeline orchestrator that regeneration may be needed
4. **Decision**: The pipeline orchestrator (or user) decides whether to regenerate downstream artifacts or accept them as-is with a stale warning

### Cascade Rules

- A stale artifact that is consumed by further downstream stages propagates staleness: if artifact B depends on artifact A, and A is stale, then B is also stale
- Staleness does not automatically trigger regeneration — it is an advisory signal
- The pipeline orchestrator logs all stale artifacts in the Progress Dashboard
- Final integrity verification (Stage 4.5) treats stale artifacts as requiring full re-verification

---

## Change Log

| Date | Change | Author |
|------|--------|--------|
| 2026-03-26 | Initial schema migration protocol established (all schemas at v1.0) | Pouria Mortezaagha |
