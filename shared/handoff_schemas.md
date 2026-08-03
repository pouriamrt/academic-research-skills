# Handoff Schemas — Cross-Skill Data Contracts

## Purpose

Defines the exact data structure for every artifact passed between pipeline stages.
All agents that produce or consume these artifacts MUST conform to these schemas.
Consuming agents should validate input and request re-generation if schema violations are found.

> **Convention**: All schemas use Markdown-based structured output. Agents MUST validate required fields before accepting a handoff. Missing required fields trigger a `HANDOFF_INCOMPLETE` failure path.

---

## Schema 1: RQ Brief (deep-research -> academic-paper)

**Producer**: `deep-research/research_question_agent` | `deep-research/socratic_mentor_agent`
**Consumer**: `deep-research/research_architect_agent` | `academic-paper/intake_agent`

### Required Fields

| Field | Type | Description |
|-------|------|-------------|
| `research_question` | string | The finalized research question (single sentence, interrogative form) |
| `sub_questions` | list[string] | 2-5 decomposed sub-questions |
| `finer_scores` | object | `{feasible: 1-10, interesting: 1-10, novel: 1-10, ethical: 1-10, relevant: 1-10}` |
| `scope` | object | `{in_scope: list[string], out_of_scope: list[string], domain: string, timeframe: string, geography: string, population: string}` |
| `methodology_type` | enum | `"qualitative"` / `"quantitative"` / `"mixed"` |
| `theoretical_framework` | string | Name of the selected or emergent theoretical framework |
| `keywords` | list[string] | 5-10 search terms for literature search |

### Optional Fields

| Field | Type | Description |
|-------|------|-------------|
| `socratic_insights` | list[string] | Key insights from Socratic dialogue (if socratic mode) |
| `hypothesis` | string | Preliminary hypothesis (if applicable) |
| `exclusion_criteria` | list[string] | What is explicitly out of scope |
| `sub_question_bindings` | list[object] | Per-sub-question inherited scope constraints (#547): `{sub_question: 1-based index, inherits: subset of scope keys (population/timeframe/geography/domain) with values, deviations: list[string] of user-approved divergences (default empty)}`. Effective-scope semantics: axes named in `inherits` use those values; omitted axes inherit the parent `scope` value; each approved deviation replaces the bound on its axis. Absent field = every sub-question inherits the full `scope` object unchanged. External motivation: Ren et al. arXiv:2607.13104 §5.1 (decomposition that stops preserving the parent task's constraints). |
| `stakeholders` | list[string] | Key stakeholders affected by the research |
| `ethical_flags` | list[string] | Preliminary ethical considerations |

### Example

```markdown
## RQ Brief

**Research Question**: How does AI-assisted formative assessment affect undergraduate learning outcomes in STEM courses at Taiwanese universities?

**Sub-Questions**:
1. What types of AI-assisted formative assessment tools are currently used in Taiwan HEI STEM courses?
2. What measurable learning outcome improvements have been documented?
3. What student and faculty perceptions exist regarding AI-assisted assessment?

**Sub-Question Bindings** (#547, optional):
1. inherits: population=Undergraduate STEM students; timeframe=2018-2025; geography=Taiwan — deviations: none
2. inherits: same as parent scope — deviations: none
3. inherits: same as parent scope — deviations: extends population to faculty (user-approved)

**FINER Scores**: Feasible: 8, Interesting: 9, Novel: 7, Ethical: 9, Relevant: 10

**Scope**:
- In scope: AI-assisted formative assessment, STEM undergraduate courses, Taiwan HEIs, 2018-2025
- Out of scope: K-12 education, summative assessment only, non-STEM disciplines
- Domain: Higher Education, Educational Technology
- Timeframe: 2018-2025
- Geography: Taiwan (with international comparisons)
- Population: Undergraduate STEM students

**Methodology Type**: Mixed methods (quasi-experimental + survey)

**Theoretical Framework**: Technology Acceptance Model (TAM) + Hattie's Feedback Framework

**Keywords**: AI assessment, formative assessment, STEM education, Taiwan higher education, learning outcomes, educational technology, automated feedback
```

---

## Schema 2: Bibliography (deep-research -> academic-paper)

**Producer**: `deep-research/bibliography_agent`
**Consumer**: `deep-research/synthesis_agent` | `deep-research/source_verification_agent` | `deep-research/concept_lineage_agent` | `academic-paper/literature_strategist_agent`

### Required Fields

| Field | Type | Description |
|-------|------|-------------|
| `sources` | list[Source] | All identified sources (minimum 15 for full mode, 5 for quick mode) |
| `search_strategy` | object | `{databases: list[string], keywords: list[string], inclusion_criteria: list[string], exclusion_criteria: list[string], date_range: string, last_searched_at?: ISO date (#548 — when the search was last executed; producers SHOULD record it: E5 requires it for SUPPORTED_WITHIN_SEARCH, and the search-bounded novelty template consumes it)}` |
| `coverage_assessment` | string | Self-assessment of literature coverage completeness |
| `minimum_sources` | integer | 15 (full mode), 5 (quick mode) |

### Source Object

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | string | Yes | Unique identifier (e.g., `[S01]`) |
| `title` | string | Yes | Source title |
| `authors` | string | Yes | Author(s) |
| `year` | integer | Yes | Publication year |
| `doi` | string | Yes* | DOI if available (*required for journal articles) |
| `citation` | string | Yes | Full APA 7 citation |
| `type` | enum | Yes | `journal_article` / `book` / `chapter` / `conference` / `report` / `thesis` / `preprint` / `web` |
| `evidence_tier` | integer | Yes | 1-7 (1 = systematic review/meta-analysis, 7 = expert opinion) |
| `quality_tier` | enum | Yes | `tier_1` (peer-reviewed top journal) / `tier_2` (peer-reviewed) / `tier_3` (other academic) / `tier_4` (grey literature) |
| `relevance` | enum | Yes | `core` (directly addresses RQ) / `supporting` (provides context) / `peripheral` (tangential) |
| `relevance_score` | integer | Yes | 1-10 relevance to the research question |
| `annotation` | string | Yes | 2-3 sentence summary of key findings and relevance |
| `verified` | boolean | No | Whether DOI/existence has been verified |
| `retraction_check` | boolean | No | Whether checked against Retraction Watch |
| `semantic_scholar_id` | string / null | No | Semantic Scholar paper ID (v3.3). Null if S2 lookup failed or API unavailable. Used for deduplication and re-verification. |

### Optional Fields

| Field | Type | Description |
|-------|------|-------------|
| `prisma_counts` | object | `{identified: int, screened: int, eligible: int, included: int}` (if systematic review) |

### Example

```markdown
## Bibliography

**Search Strategy**:
- Databases: Scopus, Web of Science, ERIC, Airiti Library
- Keywords: "AI assessment" AND "higher education" AND "Taiwan"; "formative assessment" AND "artificial intelligence"
- Inclusion: Peer-reviewed, English or Chinese, empirical or review, 2018-2025
- Exclusion: K-12, non-STEM, editorials
- Date Range: 2018-2025

**Coverage Assessment**: Strong coverage of English-language literature. Moderate coverage of Chinese-language sources (Airiti). Gap: limited grey literature from Taiwan MOE reports.

**Minimum Sources**: 15

### Sources

[S01] Wang, L., & Chen, H. (2023). AI-powered formative assessment in undergraduate physics... *Computers & Education*, 195, 104721. https://doi.org/10.xxxx
- Type: journal_article | Evidence Tier: 2 | Quality: tier_1 | Relevance: core | Score: 9
- Annotation: RCT with 240 students showing 15% improvement in exam scores with AI feedback. Directly addresses RQ sub-question 2.
```

---

## Schema 3: Synthesis Report (deep-research -> academic-paper)

**Producer**: `deep-research/synthesis_agent`
**Consumer**: `deep-research/report_compiler_agent` | `academic-paper/argument_builder_agent`

### Required Fields

| Field | Type | Description |
|-------|------|-------------|
| `themes` | list[Theme] | 3-7 synthesized themes (NOT per-source summaries) |
| `research_gaps` | list[string] | What the literature does NOT address |
| `key_debates` | list[Debate] | Where sources disagree, with analysis |
| `methodology_recommendations` | list[string] | Recommended methodological approaches based on gaps |
| `theoretical_implications` | list[string] | How the synthesis informs theoretical understanding |
| `consensus_areas` | list[string] | Where sources agree |

### Theme Object

| Field | Type | Description |
|-------|------|-------------|
| `name` | string | Theme label |
| `description` | string | 3-5 sentence synthesis across multiple sources |
| `supporting_sources` | list[string] | Source IDs that contribute to this theme |
| `contradicting_sources` | list[string] | Source IDs that challenge this theme (if any) |
| `strength` | enum | `strong` (5+ sources) / `moderate` (3-4) / `emerging` (1-2) |

### Debate Object

| Field | Type | Description |
|-------|------|-------------|
| `position_a` | string | First position |
| `position_b` | string | Opposing position |
| `sources_a` | list[string] | Source IDs supporting position A |
| `sources_b` | list[string] | Source IDs supporting position B |
| `evidence_balance` | string | Analysis of which position has stronger evidence and why |

### Example

```markdown
## Synthesis

### Theme 1: Immediate Feedback Loop as Primary Mechanism
AI-assisted assessment's primary advantage lies in the immediacy of feedback, reducing the gap between student action and corrective input. Multiple studies [S01, S04, S07, S12] converge on feedback latency as the key variable, with effect sizes ranging from d=0.3 to d=0.8. This aligns with Hattie's (2009) feedback framework...

**Strength**: Strong (5 sources)
**Supporting**: [S01, S04, S07, S12, S15]
**Contradicting**: [S09] (argues quality matters more than speed)

### Research Gaps
1. No longitudinal studies (>1 year) in Taiwan context
2. Limited data on AI assessment in laboratory courses

### Key Debates
| Position A | Position B | Evidence Balance |
|------------|------------|-----------------|
| AI feedback improves all STEM equally [S01, S04] | Effects concentrated in math/physics, weaker in biology [S08, S11] | Position B has stronger evidence; likely due to assessment type differences |
```

---

## Schema 4: Paper Draft (academic-paper -> integrity/reviewer)

**Producer**: `academic-paper/draft_writer_agent`
**Consumer**: `academic-pipeline/integrity_verification_agent` | `academic-paper-reviewer/*`

### Required Fields

| Field | Type | Description |
|-------|------|-------------|
| `title` | string | Paper title |
| `abstract` | string | English abstract (150-300 words, structured). Emitted inline by `draft_writer_agent` during Phase 4 (v3.17.0+). |
| `authors` | list[Author] | Author information with CRediT roles |
| `keywords` | list[string] | 5-7 English keywords. Emitted inline by `draft_writer_agent` during Phase 4 (v3.17.0+). |
| `sections` | list[Section] | Ordered paper sections |
| `references` | list[Reference] | Full reference list with cross-referencing |
| `total_word_count` | integer | Total word count (excluding references) |
| `citation_format` | enum | `"APA7"` / `"Chicago"` / `"MLA"` / `"IEEE"` / `"Vancouver"` |
| `structure_type` | enum | `"IMRaD"` / `"literature_review"` / `"theoretical"` / `"case_study"` / `"policy_brief"` / `"conference"` |

### Section Object

| Field | Type | Description |
|-------|------|-------------|
| `heading` | string | Section heading |
| `level` | integer | Heading level (1-4) |
| `content` | string | Full section text |
| `word_count` | integer | Word count for this section |
| `citation_count` | integer | Number of in-text citations in this section |
| `argument_strength` | enum | `compelling` / `strong` / `adequate` / `weak` (see argument_builder scoring) |

### Reference Object

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique reference ID (e.g., `[R01]`) |
| `full_citation` | string | Full formatted citation |
| `doi` | string | DOI if available |
| `cited_in_sections` | list[string] | Section headings where this reference is cited |

### Author Object

| Field | Type | Description |
|-------|------|-------------|
| `name` | string | Full name |
| `affiliation` | string | Institution |
| `email` | string | Contact email (corresponding author only) |
| `credit_roles` | list[CRediTRole] | CRediT taxonomy roles (see enum below) |
| `corresponding` | boolean | Is corresponding author |

### CRediT Role Enum

The `credit_roles` field MUST use values from the [CRediT (Contributor Roles Taxonomy)](https://credit.niso.org/):

| Value | Description |
|-------|-------------|
| `Conceptualization` | Ideas; formulation of overarching research goals and aims |
| `Data curation` | Annotation, scrubbing, and maintenance of research data |
| `Formal analysis` | Application of statistical, mathematical, or computational techniques |
| `Funding acquisition` | Acquisition of financial support for the project |
| `Investigation` | Conducting the research and investigation process |
| `Methodology` | Development or design of methodology |
| `Project administration` | Management and coordination responsibility |
| `Resources` | Provision of study materials, reagents, patients, laboratory samples, instrumentation, or computing resources |
| `Software` | Programming, software development, implementation of code |
| `Supervision` | Oversight and leadership responsibility |
| `Validation` | Verification of results/experiments reproducibility |
| `Visualization` | Preparation and presentation of published work, specifically visualization |
| `Writing – original draft` | Preparation of the initial draft |
| `Writing – review & editing` | Critical review, commentary, or revision of the draft |

> **Validation rule**: Any value in `credit_roles` not matching the 14 values above triggers a `SCHEMA_VALIDATION_FAILED` error. Agents MUST use exact string matches (case-sensitive).

---

## Schema 5: Integrity Report (integrity_verification_agent -> pipeline)

**Producer**: `academic-pipeline/integrity_verification_agent`
**Consumer**: `academic-pipeline/pipeline_orchestrator_agent` | `academic-paper/draft_writer_agent` (for revision)

### Required Fields

| Field | Type | Description |
|-------|------|-------------|
| `verdict` | enum | `"PASS"` / `"PASS_WITH_CONDITIONS"` / `"FAIL"` |
| `mode` | enum | `"pre-review"` / `"final-check"` |
| `phases` | object | See Phase Structure below |
| `overall_issues` | object | `{SERIOUS: integer, MEDIUM: integer, MINOR: integer}` |
| `citation_integrity_score` | float | 0.0-1.0 score for citation accuracy |
| `fabrication_risk_score` | float | 0.0-1.0 score (0 = no risk detected) |
| `score_trajectory` | object / null | Review score delta tracking (v3.3, optional). Present only during re-review. See Score Trajectory Structure below. |
| `timestamp` | string | ISO 8601 timestamp of verification |

### Phase Structure

```
phases: {
  A_references: {
    checked: integer,
    passed: integer,
    failed: integer,
    issues: [{ref_id: string, issue_type: string, severity: enum, detail: string}]
  },
  B_citation_context: {
    sampled: integer,
    verified: integer,
    issues: [{ref_id: string, section: string, issue: string}]
  },
  C_data: {
    claims_checked: integer,
    verified: integer,
    issues: [{claim: string, expected: string, actual: string, severity: enum}]
  },
  D_originality: {
    checked: boolean,
    issues: [{type: string, severity: enum, detail: string}]
  },
  E_claims: {
    checked: integer,
    verified: integer,
    distortions: [{claim: string, source: string, verdict: string, detail: string}]
  }
}
```

### Score Trajectory Structure (v3.3, optional)

Present only when the integrity report is for a re-review (Stage 3' or 4'). Tracks rubric score changes across revision rounds.

Dimension names match the 7 universal review dimensions from `academic-paper-reviewer/references/review_criteria_framework.md` plus an overall score. The scoring scale is **0-100**, per `academic-paper-reviewer/references/quality_rubrics.md` — the scale the report template instructs reviewers to score on, and the scale the SKILL.md Early-Stopping Criterion ("delta < 3 points on the 0-100 rubric") and the delta thresholds below assume (#399 reconciliation; an earlier comment here said 1-5, which never matched either producer or consumer):

```
score_trajectory: {
  round: integer,          // revision round number (1 or 2)
  previous_scores: {       // rubric scores from prior review (0-100 scale per quality_rubrics.md)
    originality: float,
    methodological_rigor: float,
    evidence_sufficiency: float,
    argument_coherence: float,
    writing_quality: float,
    literature_integration: float,
    significance_impact: float,
    overall: float
  },
  current_scores: {        // rubric scores from this review (0-100 scale per quality_rubrics.md)
    originality: float,
    methodological_rigor: float,
    evidence_sufficiency: float,
    argument_coherence: float,
    writing_quality: float,
    literature_integration: float,
    significance_impact: float,
    overall: float
  },
  deltas: {                // current - previous for each dimension
    originality: float,
    methodological_rigor: float,
    evidence_sufficiency: float,
    argument_coherence: float,
    writing_quality: float,
    literature_integration: float,
    significance_impact: float,
    overall: float
  },
  regression_detected: boolean,  // true if any delta < -3
  regressed_dimensions: list[string],  // names of dimensions where delta < -3
  early_stop_eligible: boolean   // true if overall delta < 3 AND no P0 issues (existing criterion)
}
```

**Consumer**: `pipeline_orchestrator_agent` uses `regression_detected` to trigger a warning checkpoint. `editorial_synthesizer_agent` includes trajectory in re-review reports.

### Issue Severity Levels

| Severity | Meaning | Pipeline Impact |
|----------|---------|-----------------|
| `SERIOUS` | Fabricated reference, falsified data, gross distortion | Blocks pipeline; MUST fix |
| `MEDIUM` | Wrong DOI, incorrect page number, misattribution | Blocks pipeline; MUST fix |
| `MINOR` | Missing co-author, formatting inconsistency | Does NOT block; advisory |

---

## Schema 6: Review Report (academic-paper-reviewer -> pipeline)

**Producer**: `academic-paper-reviewer/editorial_synthesizer_agent`
**Consumer**: `academic-pipeline/pipeline_orchestrator_agent` | `academic-paper/draft_writer_agent`

### Required Fields

| Field | Type | Description |
|-------|------|-------------|
| `editorial_decision` | enum | `"Accept"` / `"Minor Revision"` / `"Major Revision"` / `"Reject"` |
| `reviewer_reports` | list[ReviewerReport] | Individual review reports |
| `consensus` | enum | `"CONSENSUS-4"` / `"CONSENSUS-3"` / `"SPLIT"` / `"DA-CRITICAL"` |
| `revision_roadmap` | list[RoadmapItem] | Prioritized list of required changes |
| `confidence_score` | integer | 0-100 editorial confidence |

### Optional Fields

| Field | Type | Description |
|-------|------|-------------|
| `judge_record` | object | #539 judge transparency: `{verification_judge, round1_panel_provenance, cross_model_pass: "ran"|"partial"|"not_configured"|"failed", cross_model_items_judged?: int, cross_model_items_total?: int (required when partial), cross_model_id?, failure_reason?, prompt_rubric_surfaces, reviewer_configuration?, evidence_seen, judging_budget_note, precommitment_hash?, routing_status?, apply_chain_witness?}`. `round1_panel_provenance` is copied seat-level from the #540 Review Panel Provenance block ("unknown (provenance block absent)" when absent — a singular revision-driving judge is not well-defined for a mixed-family panel). `reviewer_configuration` (optional, #574/#576 pre-work) records yardstick continuity: `"round1_cards_reused"` or the verbatim `[YARDSTICK-REGENERATED: <original|revised> manuscript — <reason>]` marker per `re_review_mode_protocol.md` § Yardstick Continuity; absent = pre-yardstick-continuity report. Three #576 optional fields (absent = pre-#576 report): `precommitment_hash` (sha256 of the Phase-1 pre-commitment artifact the verdicts were committed against — the judge's fixed reference); `routing_status` (`oneOf`: the three CONSTANTS `"card_mapped"` / `"[ROUTING-DEGRADED: cards unparsable]"` / `"[ROUTING-DEGRADED: no round-1 cards]"` + one PATTERN for the parameterized unmapped-labels form `[ROUTING-DEGRADED: unmapped labels — <payload>]` per the §10 payload grammar — the payload is accountability content, never collapsed to a bare enum; `reviewer_configuration` is untouched and keeps its own two values); `apply_chain_witness` (the §11 closed composite `"pass"` / `"fail"` / `"first_link_not_run"` / `"not_run_no_reports"`). Emitted by re-review (Stage 3'); absent = pre-#539 report. External motivation: Ren et al. arXiv:2607.13104 §8.1.2. |

### ReviewerReport Object

| Field | Type | Description |
|-------|------|-------------|
| `reviewer_id` | string | Reviewer identifier (e.g., `EIC`, `R1`, `R2`, `R3`, `DA`) |
| `role` | string | Reviewer role description |
| `dimension_scores` | object | Per-dimension scores (skill-specific) |
| `strengths` | list[string \| Strength] | Paper strengths identified. Current-format cards emit Strength objects `{description: string, evidence_anchor: object}` — the same typed-anchor shape as Weakness, since A2's every-finding rule covers both polarities (#574 A2; a section-level locator suffices for a strength). A bare string = legacy card (consumers treat it as description-only). |
| `weaknesses` | list[Weakness] | Paper weaknesses identified |
| `questions` | list[string] | Questions for the authors |
| `coverage_receipt` | object | *(conditional, #574 A1)* REQUIRED when `strengths` or `weaknesses` is EMPTY: `{covers: "strengths" \| "weaknesses" \| "both", rows: [{dimension: string, checked: string, basis: string}]}` — preserves the reviewer's Coverage Receipt so consumers can distinguish a reviewed-empty list from a thin or truncated review. Absent with empty lists = legacy/invalid current-format card |
| `reviewer_confidence` | integer | *(optional, #574 A3)* The reviewer's report-level Confidence Score, 1-5 (template § Confidence Score) — the legacy-card fallback target when a weakness lacks per-finding `confidence` (`[CONFIDENCE-SOURCE: report-level]`). Deliberately distinct from the TOP-LEVEL `confidence_score`, which is 0-100 EDITORIAL confidence — the two scales never interchange. |

### Weakness Object

| Field | Type | Description |
|-------|------|-------------|
| `description` | string | What the weakness is |
| `severity` | enum | `critical` / `major` / `minor` — the CANONICAL single source for finding severity across the reviewer stack (#574 A3). Reviewer cards and templates carry it explicitly per finding (title-case `Critical`/`Major`/`Minor` on prose surfaces maps to this enum; the DA's `OBSERVATION` category is a non-defect channel that never enters `weaknesses[]`). Consumers transport it, never re-derive it; a legacy card without per-finding tags is marked `[SEVERITY-SOURCE: letter-fallback]` by the synthesizer. |
| `type` | enum | `methodology` / `theory` / `evidence` / `writing` / `structure` / `ethics` |
| `evidence_anchor` | object | *(optional, #574 A2)* Typed anchor: `{anchor_type: "text" \| "table" \| "figure" \| "equation" \| "dataset" \| "absence", locator: string, quote: string, absence_scope: string, check_performed: string}`. Conditional members: `quote` (≤ 25 words) is REQUIRED when `anchor_type = "text"`; `absence_scope` and `check_performed` are REQUIRED when `anchor_type = "absence"`; all three are omitted for other types. Critical/major weaknesses are expected to carry an adequate, applicable anchor; absent field = legacy card. |
| `confidence` | integer | *(optional, #574 A3)* Per-finding confidence 1-5 from the reporting reviewer. Absent = legacy card; consumers fall back to the report-level Confidence Score and mark `[CONFIDENCE-SOURCE: report-level]`. |
| `competence_basis` | string | *(optional, #574 A3)* One-phrase basis for `confidence` (e.g. `"core expertise: psychometrics"`, `"adjacent field: applying general standards"`). |

---

## Schema 7: Revision Roadmap (reviewer -> academic-paper revision)

**Producer**: `academic-paper-reviewer/editorial_synthesizer_agent`
**Consumer**: `academic-paper/draft_writer_agent` | `academic-pipeline/pipeline_orchestrator_agent`

### Required Fields

| Field | Type | Description |
|-------|------|-------------|
| `items` | list[RoadmapItem] | Ordered list of revision items |
| `total_items` | integer | Total number of items |
| `must_fix_count` | integer | Number of `must_fix` priority items |
| `editorial_decision` | enum | `"Accept"` / `"Minor Revision"` / `"Major Revision"` / `"Reject"` |
| `consensus_summary` | string | Summary of reviewer consensus |
| `dissenting_opinions` | list[string] | Notable disagreements among reviewers |

### RoadmapItem Object

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique revision ID (e.g., `REV-001`) |
| `description` | string | What needs to change |
| `reviewer` | string | Which reviewer(s) raised this (e.g., `R1, R3`) |
| `type` | enum | `"Major"` / `"Minor"` / `"Editorial"` — the revision-MAGNITUDE label (how big the change is), deliberately distinct from finding severity (#574 A3): a Critical finding's fix can be a small change and vice versa |
| `priority` | enum | `"must_fix"` / `"should_fix"` / `"consider"` |
| `severity` | enum | *(optional, #574 A3)* Transported Schema 6 finding severity (`critical`/`major`/`minor`) of the driving sub-claim; absent = legacy roadmap |
| `severity_source` | string | *(optional, #574 A3)* Fallback provenance for `severity` — the verbatim tag, e.g. `[SEVERITY-SOURCE: letter-fallback]`; absent = direct per-finding seat tag (the enum value alone cannot carry the tag) |
| `evidence_anchor` | object | *(optional, #574 A2)* The driving finding's typed anchor — same shape as the Schema 6 Weakness `evidence_anchor`; absent = legacy roadmap |
| `confidence` | integer | *(optional, #574 A3)* The driving finding's per-finding confidence 1-5; absent = legacy roadmap |
| `competence_basis` | string | *(optional, #574 A3)* The driving finding's one-phrase competence basis — the rationale half of the emitted `[n — basis]` cell; absent = legacy roadmap |
| `confidence_source` | string | *(optional, #574 A3)* Fallback provenance for `confidence` — the verbatim tag, e.g. `[CONFIDENCE-SOURCE: report-level]`; absent = per-finding value |
| `corroborating_sources` | list[object] | *(optional, #574 A2/A3)* When an item consolidates MULTIPLE corroborating findings: the singular `severity`/`evidence_anchor`/`confidence` fields carry the DRIVING finding (highest severity; ties broken by confidence), and each remaining source rides here as `{reviewer, severity, evidence_anchor, confidence, competence_basis?, severity_source?, confidence_source?}` — nothing is dropped or merged |
| `source_kind` | enum | *(optional, #574 A3)* `"question"` / `"editorial"` — an item with NO driving finding (author-question follow-up, aggregated editorial task) sets this and legitimately omits ALL transported fields. Absent transported fields WITHOUT `source_kind` = legacy roadmap |
| `target_section` | string | Section of the paper to modify |
| `suggested_action` | string | How to address the item |
| `consensus_level` | enum | `"CONSENSUS-4"` / `"CONSENSUS-3"` / `"SPLIT"` / `"DA-CRITICAL"` / `"SINGLE-VERIFIER"` (#576 §8 — a Stage 3' previously-missed forward-seed item (`REV-PM-<n>`), observed by a single verifier seat; no panel-consensus value truthfully applies. Additive: existing producers unaffected) |
| `verification_criteria` | string | How to confirm the fix is adequate |

### Optional Fields

| Field | Type | Description |
|-------|------|-------------|
| `deadline_suggestion` | string | Suggested timeline for completion |
| `requires_new_experiment` | boolean | `true` if this revision item cannot be addressed by text revision alone and requires new data collection, experiment execution, or simulation. Default: `false`. When `true`, the pipeline orchestrator re-enters Stage 1.5 before proceeding with text revision |
| `experiment_type` | enum | Only present when `requires_new_experiment = true`. One of: `"new_experiment"` (design + execute from scratch), `"additional_analysis"` (re-analyze existing data with new tests), `"replication"` (repeat experiment with modifications), `"simulation"` (new/modified simulation). Informs which sub-stage of 1.5 to re-enter |
| `experiment_scope` | string | Only present when `requires_new_experiment = true`. Brief description of what experiment/analysis is needed (e.g., "Conduct robustness check with alternative DV operationalization") |

---

## Schema 8: Response to Reviewers (academic-paper revision -> reviewer re-review)

**Producer**: `academic-paper/draft_writer_agent` (revision mode)
**Consumer**: `academic-paper-reviewer/editorial_synthesizer_agent` (re-review)

### Required Fields

| Field | Type | Description |
|-------|------|-------------|
| `revision_round` | integer | Which revision round (1, 2, ...) |
| `items` | list[ResponseItem] | Response to each revision roadmap item |
| `summary` | object | `{resolved: integer, limitations: integer, unresolvable: integer, disagreed: integer}` |
| `word_count_delta` | integer | Net word count change (positive = added, negative = removed) |
| `new_references_added` | integer | Count of new references added during revision |
| `summary_of_changes` | string | High-level summary of all modifications |
| `new_content_highlight` | list[string] | Sections with substantial new content |

### ResponseItem Object

| Field | Type | Description |
|-------|------|-------------|
| `roadmap_item_id` | string | Corresponds to RoadmapItem.id (e.g., `REV-001`) |
| `reviewer_comment` | string | Original reviewer comment (quoted) |
| `author_response` | string | Detailed response to the reviewer |
| `change_location` | string | Where in the paper the change was made (section + paragraph) |
| `change_block_ids` | list[string] | *(optional, #390 patch-mode rounds)* Block IDs the change landed in (`B0042`-form), the machine-checkable sibling of the free-text `change_location` — cross-checkable against the apply report's op list. **Populated by the orchestrator from the apply report, never by the writer** (spec §3.5 role split: inserted blocks get fresh IDs only at apply time, so the writer cannot know them; it emits provisional response items and the orchestrator completes the mechanical fields). Absent field = pre-patch-era or escalated full re-emission round (valid). |
| `status` | enum | `"RESOLVED"` / `"DELIBERATE_LIMITATION"` / `"UNRESOLVABLE"` / `"REVIEWER_DISAGREE"` |
| `decline_justification` | string | Required if status is `DELIBERATE_LIMITATION`, `UNRESOLVABLE`, or `REVIEWER_DISAGREE`; must cite evidence |

### Example

```markdown
## Response to Reviewers — Round 1

**Summary**: We have addressed all 12 revision items. 10 were fully addressed, 1 marked as deliberate limitation with explanation, and 1 respectfully declined with justification.

**Word Count Delta**: +420 words
**New References Added**: 3

### REV-001 (R1, R2 — CONSENSUS-3, must_fix)
**Reviewer Comment**: "The sample size justification is insufficient for the claimed effect size."
**Status**: RESOLVED
**Response**: We have added a formal power analysis (G*Power 3.1) in Section 3.2, paragraph 2. The analysis confirms that our sample of N=240 provides 0.85 power to detect a medium effect (d=0.5) at alpha=0.05...
**Changes**: Section 3.2 paragraph 2 (new content, +180 words)

### REV-007 (DA — DA-CRITICAL, must_fix)
**Reviewer Comment**: "Selective reporting of outcomes suggests confirmation bias."
**Status**: RESOLVED
**Response**: We acknowledge this valid concern. We have now reported ALL pre-registered outcomes including the two non-significant results (peer interaction frequency, self-efficacy subscale)...
**Changes**: Section 4.1 Table 3 (expanded), Section 5 paragraph 4 (new discussion of null results)
```

---

## Schema 9: Material Passport (cross-stage metadata)

**Purpose**: Accompanies every artifact as it passes between stages, providing provenance and verification tracking.

### Required Fields

| Field | Type | Description |
|-------|------|-------------|
| `origin_skill` | string | Which skill produced this artifact (e.g., `deep-research`, `academic-paper`) |
| `origin_mode` | string | Which mode was used (e.g., `full`, `socratic`, `pre-review`) |
| `origin_date` | string | ISO 8601 timestamp of production |
| `verification_status` | enum | `"VERIFIED"` / `"UNVERIFIED"` / `"STALE"` |
| `version_label` | string | Version identifier. **Format**: `{origin_skill}_v{major}.{minor}[-{variant}]` (e.g., `deep_research_v1.0`, `data_analyst_v1.1-revised`, `academic_paper_v2.0`) |

### Optional Fields

| Field | Type | Description |
|-------|------|-------------|
| `integrity_pass_date` | string | ISO 8601 timestamp of last integrity verification pass (if applicable) |
| `content_hash` | string | SHA-256 hash of the content (for change detection) |
| `upstream_dependencies` | list[string] | Version labels of artifacts this one depends on |
| `repro_lock` | object \| null | configuration lockfile for artifact reproducibility. See [`artifact_reproducibility_pattern.md`](artifact_reproducibility_pattern.md). `null` = honest opt-out. Required from v3.3.5+ — omitted key fails lint. |
| `compliance_history` | list[object] | Append-only audit trail of `compliance_report` entries (Schema 19, renumbered from upstream Schema 12 in fork v3.16.0). Added v3.4.0+. See [Schema 19](#schema-19--compliance-report-v340-renumbered-from-upstream-schema-12-to-avoid-collision-with-forks-schema-12-lab-record) and [`shared/compliance_report.schema.json`](compliance_report.schema.json). |
| `reset_boundary` | list[object] | Append-only ledger. Two entry kinds: `boundary` (recorded at FULL checkpoints when `ARS_PASSPORT_RESET=1`) and `resume` (recorded when `resume_from_passport` consumes a boundary). Added v3.6.3+. Entry shape: [`shared/contracts/passport/reset_ledger_entry.schema.json`](contracts/passport/reset_ledger_entry.schema.json). See [`academic-pipeline/references/passport_as_reset_boundary.md`](../academic-pipeline/references/passport_as_reset_boundary.md). |
| `literature_corpus` | list[object] | Optional append-friendly literature corpus. Each entry conforms to [`shared/contracts/passport/literature_corpus_entry.schema.json`](contracts/passport/literature_corpus_entry.schema.json). Produced by user-written adapters (see [`academic-pipeline/references/adapters/overview.md`](../academic-pipeline/references/adapters/overview.md)); ARS does not produce these entries itself. Added v3.6.4+. |
| `audit_artifact` | list[object] | Optional append-only ledger of cross-model audit runs for v3.6.7 downstream-agent deliverables. Each entry conforms to [`shared/contracts/passport/audit_artifact_entry.schema.json`](contracts/passport/audit_artifact_entry.schema.json). Produced by the pipeline orchestrator after Layer 2 + Layer 3 verification of wrapper-emitted proposal entries; only `persisted` entries are stored here. Added v3.6.7+. |
| `slr_lineage` | boolean | Run-level provenance flag set by `pipeline_orchestrator_agent` at the Stage 1 → Stage 2 handoff. `true` iff any stage in this run history was produced by `deep-research` in systematic-review mode. Consumed by `disclosure` mode renderer (`--policy-anchor=prisma-trAIce` track gate per `policy_anchor_disclosure_protocol.md` §3.1). Absence = `false` = cold-start path (renderer requires explicit `mode=` per §4.3 G2 invariant fallback rule). Added v3.7.4+. See [Run-level lineage signal (v3.7.4)](#run-level-lineage-signal-v374) below. |
| `pipeline_state.mode` | enum | Resolved AUTO/INTERACTIVE mode cached at session start from `ARS_INTERACTIVE`. Values: `auto` (env unset or `!=1`) \| `interactive` (env `=1`). Persisted so resume sessions inherit the original mode unless explicitly overridden via `mode_override=` at resume time. Added v3.17.0+. See [`academic-pipeline/agents/pipeline_orchestrator_agent.md`](../academic-pipeline/agents/pipeline_orchestrator_agent.md) §0 IRON RULE 1. |
| `auto_retry_history` | list[object] | Append-only ledger of AUTO-mode retry rounds at Stage 2.5 / 4.5 integrity FAIL. Each entry records `{stage: <2.5\|4.5>, round: <i>, max_rounds: <N>, fail_category: <hallucinated_citation\|hallucinated_claim\|data_mismatch\|citation_context\|compliance_tier2_or_3>, fix_agent: <agent_name>, verifier: <agent_name>, verdict: <PASS\|FAIL>, started_at: <ISO8601-UTC>, completed_at: <ISO8601-UTC>, fail_reason: <string-or-null>}`. Used by Stage 6 PROCESS SUMMARY's "Failure Mode Audit Log" section. Added v3.17.0+. |
| `experiment_intake_declaration` | object | Passport-level intake decision (#260, D7). `status` ∈ `{experiments_declared, no_experiments_declared, legacy_unknown}` + `declared_at` + `declared_by: scholar`. Set by whichever agent owns Stage 1 intake (the intake/orchestrator layer — NOT the three manifest writers). **Fail-closed**: a passport treated-as-post-#260 (the default — only a `repro_lock.ars_version` proven `< the #260 constant` is `legacy_unknown`) with this field ABSENT is a gate FAIL. Even a literature-only run must carry `{status: no_experiments_declared}`. EP-INV-4 enforces declaration↔provenance symmetry. See [Experiment Provenance Intake (#260)](#experiment-provenance-intake-260) below. |
| `experiment_provenance` | list[object] | Optional scholar-entered ledger of experiments run EXTERNALLY (#260, D1). Each entry conforms to [`shared/contracts/passport/experiment_provenance_entry.schema.json`](contracts/passport/experiment_provenance_entry.schema.json) — `experiment_id` (passport-flat, frozen at intake) + nested `repro_lock` + `planned_vs_executed[]` + `negative_results[]` + `known_limitations[]`. ARS does not run experiments, does not auto-fill provenance, does not judge experiment correctness. Joined from claims via `claim_intent_manifest.planned_experiment_ids[]`. Gated at the integrity verification stage (Stage 2.5/4.5, D6). Added #260. |
| `experiment_alignment_results` | list[object] | Optional aggregate of claim→experiment alignment verdicts (#260, D4) — the FOURTH ref_slug-less claim-finding aggregate (alongside `uncited_assertions` / `claim_drifts` / `constraint_violations`). Each entry conforms to [`shared/contracts/passport/experiment_alignment_result.schema.json`](contracts/passport/experiment_alignment_result.schema.json); `alignment_verdict` ∈ `{ALIGNED, OVERSTATED, NOT_SUPPORTED_BY_PROVENANCE, PROVENANCE_INSUFFICIENT}`. **Produced by the integrity verification agent AT the gate** (mirrors #261 C3), NOT by the claim-alignment audit agent. EA-INV-1/2 enforce id-uniqueness + reference resolution. Carried forward by `pipeline_orchestrator_agent`'s aggregate hand-off. Added #260. |

### Example

```markdown
## Material Passport

- Origin Skill: academic-paper
- Origin Mode: full
- Origin Date: 2026-03-08T14:30:00Z
- Verification Status: VERIFIED
- Version Label: academic_paper_v2.0
- Integrity Pass Date: 2026-03-08T15:45:00Z
- Content Hash: a3f2b7c9...
- Upstream Dependencies: [deep_research_v1.0, deep_research_v1.0, deep_research_v1.0]
```

### Reset Boundary Extension (v3.6.3)

When `ARS_PASSPORT_RESET=1`, Schema 9 gains an append-only `reset_boundary[]` ledger with two entry kinds: `boundary` (recorded at FULL checkpoints) and `resume` (recorded when a boundary is consumed):

```yaml
reset_boundary:
  # Kind 1: boundary entry at Stage 2 FULL checkpoint
  - kind: boundary
    hash: a3f2b7c9d0e1
    stage: "2"
    next: "2.5"
    generated_at: 2026-04-23T14:00:00Z
    session_marker: sess-20260423-1a2b
    version_label: paper_draft_v1
    mode: full
    verification_status: VERIFIED

  # Kind 1 with pending_decision: Stage 3 rejection case
  - kind: boundary
    hash: b4c2d8e7f0a1
    stage: "3"
    next: "4"
    generated_at: 2026-04-24T10:00:00Z
    session_marker: sess-20260424-3c4d
    version_label: paper_draft_v2
    mode: full
    pending_decision:
      question: "Stage 3 reviewer decision"
      options:
        - value: revise
          next_stage: "4"
          next_mode: revision
        - value: restructure
          next_stage: "2"
          next_mode: plan
        - value: abort
          next_stage: null   # null = terminate pipeline

  # Kind 2: resume event consuming the first boundary (Stage 2 → 2.5)
  - kind: resume
    consumes_hash: a3f2b7c9d0e1
    generated_at: 2026-04-23T15:00:00Z
    session_marker: sess-20260423-5e6f
  # append-only; never overwrite, never reorder
```

Consumers match `resume_from_passport=<hash>` against `boundary` entries. A `boundary` is **awaiting resume** iff no later `resume` entry carries `consumes_hash == <boundary hash>`. Hash mismatch on resume is a hard error.

See [`academic-pipeline/references/passport_as_reset_boundary.md`](../academic-pipeline/references/passport_as_reset_boundary.md) for the full protocol.

### Literature Corpus Input Port (v3.6.4)

The optional `literature_corpus[]` field is Schema 9's input port for user-owned literature. Each entry is a bibliographic record conforming to `literature_corpus_entry.schema.json` (CSL-JSON author format, β required set).

ARS does not produce these entries. User-written adapters read their own corpus source (Zotero, Obsidian, folder, Notion, etc.) and emit a passport with `literature_corpus[]` populated. Three reference adapters ship with v3.6.4 under [`scripts/adapters/`](../scripts/adapters/).

Consumer integration ships in v3.6.5: `bibliography_agent` (deep-research, Phase 1) and `literature_strategist_agent` (academic-paper, Phase 1) read `literature_corpus[]` via the corpus-first, search-fills-gap flow. See [`academic-pipeline/references/literature_corpus_consumers.md`](../academic-pipeline/references/literature_corpus_consumers.md) for the full consumer protocol, the four Iron Rules, and per-consumer reading instructions.

See [`academic-pipeline/references/adapters/overview.md`](../academic-pipeline/references/adapters/overview.md) for the adapter contract.

### Audit Artifact Ledger (v3.6.7)

Schema 9 gains an optional append-only `audit_artifact[]` ledger recording cross-model audit runs that gate the three v3.6.7 downstream agents (`synthesis_agent`, `research_architect_agent` survey-designer mode, `report_compiler_agent` abstract-only mode). Each entry conforms to [`shared/contracts/passport/audit_artifact_entry.schema.json`](contracts/passport/audit_artifact_entry.schema.json).

The ledger stores only `persisted` entries — those merged by `pipeline_orchestrator_agent` after Layer 2 (JSONL schema) + Layer 3 (sidecar metadata) anti-fake-audit checks pass per the eleven gating checks at [`docs/design/2026-04-30-ars-v3.6.7-step-6-orchestrator-hooks-spec.md`](../docs/design/2026-04-30-ars-v3.6.7-step-6-orchestrator-hooks-spec.md) §5.2. Wrapper-emitted `proposal` entries live under `audit_artifacts/<run_id>.audit_artifact_entry.json` until orchestrator consumes them; they never reach the passport.

```yaml
audit_artifact:
  - stage: 2                                   # destination stage gated by this audit
    agent: synthesis_agent                     # one of the three v3.6.7 agents
    deliverable_path: chapter_4/synthesis.md
    deliverable_sha: a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2
    run_id: 2026-04-30T15-22-04Z-d8f3
    bundle_id: phase2-chapter4-2026-04-30
    bundle_manifest_sha: 9a8b7c6d5e4f3b2a1c0d9e8f7a6b5c4d3e2f1a0b9c8d7e6f5a4b3c2d1e0f9876
    artifact_paths:
      jsonl: audit_artifacts/2026-04-30T15-22-04Z-d8f3.jsonl
      sidecar: audit_artifacts/2026-04-30T15-22-04Z-d8f3.meta.json
      verdict: audit_artifacts/2026-04-30T15-22-04Z-d8f3.verdict.yaml
    verdict:
      status: MINOR                            # persisted enum: PASS | MINOR | MATERIAL
      round: 2
      target_rounds: 3
      finding_counts:
        p1: 0
        p2: 0
        p3: 1
      verified_at: "2026-04-30T15:23:11.847Z"  # RFC 3339 UTC string, ms precision (quoted: schema is `string` + regex, not YAML datetime); strict-monotonic per scripts/_next_verified_at_ms.py
      verified_by: pipeline_orchestrator_agent
  # append-only; never overwrite, never reorder
```

**Semantics:**

- `stage` is the **destination stage** the just-completed deliverable is about to enter (synthesis_agent → 2, research_architect_agent survey-designer → 2, report_compiler_agent abstract-only → 5).
- `verdict.status` enum is `["PASS", "MINOR", "MATERIAL"]` for persisted entries. `AUDIT_FAILED` is reachable only in the proposal arm and never persists; see [`audit_artifact_entry.schema.json`](contracts/passport/audit_artifact_entry.schema.json) Lifecycle-conditional fields for the rationale.
- `verdict.verified_at` and `verdict.verified_by` are required on persisted entries (orchestrator-written) and forbidden on proposal entries (wrapper-emitted).
- Multiple entries for the same `(stage, agent, deliverable_sha)` represent multiple audit rounds; orchestrator selects the latest by `verified_at` for verdict reads.
- If `deliverable_sha` changes (deliverable mutated), prior entries become stale but remain as audit history; orchestrator only honors entries whose `deliverable_sha` matches the current deliverable.

**This mirrors the v3.6.3 `reset_boundary[]` append-only pattern**: history preserved, freshness computed by ledger scan. Deletion or reordering is forbidden; lint at `scripts/check_audit_artifact_consistency.py` enforces the invariant family at [`docs/design/2026-04-30-ars-v3.6.7-step-6-orchestrator-hooks-spec.md`](../docs/design/2026-04-30-ars-v3.6.7-step-6-orchestrator-hooks-spec.md) §3.7.

For the orchestrator-side gate procedure (Path A latest-by-`verified_at` selection, Path B proposal merge after Layer 2 + Layer 3 verification), the canonical contract is [`docs/design/2026-04-30-ars-v3.6.7-step-6-orchestrator-hooks-spec.md`](../docs/design/2026-04-30-ars-v3.6.7-step-6-orchestrator-hooks-spec.md) §5.6 (Path A/B fall-through with the §5.6 A1.5 superseding-proposal preflight) plus §5.2 (eleven Layer 2 + Layer 3 gating checks). Implementation lands as a subsection of `academic-pipeline/agents/pipeline_orchestrator_agent.md` (Phase 6.6 deliverable). For the resume-time re-verification semantics, see [`academic-pipeline/references/passport_as_reset_boundary.md`](../academic-pipeline/references/passport_as_reset_boundary.md).

### Experiment Provenance Intake (#260)

Schema 9 gains the **intake + alignment** layer for experiments — NOT an execution layer. ARS keeps experiment execution outside the pipeline: the scholar runs experiments externally and brings results back. This extension records disclosure and lets manuscript claims be audited against declared provenance. It does **not** run experiments, judge experiment correctness, auto-fill provenance, or require provenance for literature-only pipelines.

**Three additions** (all under the Optional-Fields table above):

1. `experiment_intake_declaration` (passport-level object) — the Stage 1 intake decision, set by the intake/orchestrator layer (the agent that owns Stage 1 for that entry path), never by the three manifest writers:

   ```yaml
   experiment_intake_declaration:
     status: experiments_declared        # | no_experiments_declared | legacy_unknown
     declared_at: "2026-06-08T10:00:00Z"
     declared_by: scholar                # always scholar — an intake decision, not an agent emission
   ```

   **Fail-closed legacy boundary (D7).** The default is treat-as-post-#260, NOT treat-as-legacy. A passport is `legacy_unknown` (advisory) ONLY with positive proof it predates #260 — `repro_lock.ars_version` present AND `< the #260 release constant` (frozen in the gate at ship time). Everything else — including a passport with no `repro_lock` or a `repro_lock` with no `ars_version` — is treated as post-#260, so the declaration is REQUIRED and its absence is a gate FAIL. Version-unprovable ≠ legacy. This shuts the back door: a new run cannot dodge the declaration by omitting `repro_lock` to make its version unprovable. Even a pure-literature run (e.g. `deep-research lit-review`) must emit `{status: no_experiments_declared}`.

2. `experiment_provenance[]` (scholar-entered list) — one [`experiment_provenance_entry.schema.json`](contracts/passport/experiment_provenance_entry.schema.json) per experiment:

   ```yaml
   experiment_provenance:
     - experiment_id: exp-ablation-A      # passport-flat, FROZEN at intake (a rename is a re-intake event)
       title: "Ablation: remove head pruning"
       repro_lock: { schema_version: "1.0", ... }   # same inline shape as the passport-level repro_lock
       planned_vs_executed:
         - planned: "macro-F1 on held-out test, pruning removed"
           executed: true
           result_file: results/ablation_A.json
           metric: macro-F1
           value: 0.842
       negative_results: []               # KEY MUST be present (absent = malformed FAIL); empty [] is well-formed
       known_limitations: []              # KEY MUST be present; empty [] routes to the D6 check-4 advisory
   ```

   The `experiment_id` values are FROZEN once `status == experiments_declared` is set; writers reference that key space via `claim_intent_manifest.planned_experiment_ids[]`. A post-intake rename is a re-intake event (re-run the manifest emitters), caught by EP-INV-2 if it dangles.

3. `experiment_alignment_results[]` (integrity-agent-produced list) — the fourth ref_slug-less claim-finding aggregate. Each [`experiment_alignment_result.schema.json`](contracts/passport/experiment_alignment_result.schema.json) row carries an `alignment_verdict` computed by the integrity verification agent **at the gate** (Stage 2.5/4.5), mirroring #261's Phase C3. A mixed-evidence claim (carrying BOTH `planned_refs` and `planned_experiment_ids`) gets one `claim_audit_results[]` row AND one `experiment_alignment_results[]` row; the gate combines them worst-verdict-wins.

**Invariants** (lint-enforced in `scripts/check_claim_audit_consistency.py`): EP-INV-1 (experiment_id unique/passport) · EP-INV-2 (planned_experiment_ids resolve; rename + forward-reference guard) · EP-INV-3 (experiment ids ⟹ empirical; mixed literature+experiment allowed) · EP-INV-4 (declaration↔provenance symmetry) · EA-INV-1 (finding_id unique) · EA-INV-2 (alignment row references resolve; dangling id = structural FAIL, never a verdict). Shape-only validation of a single entry is also available via `scripts/check_experiment_provenance.py`.

See [`docs/design/2026-06-08-260-experiment-provenance-intake-spec.md`](../docs/design/2026-06-08-260-experiment-provenance-intake-spec.md) for the full design (7 decisions D1–D7) and [`examples/passport_with_experiment_provenance.yaml`](../examples/passport_with_experiment_provenance.yaml) for a worked passport.

### Run-level lineage signal (v3.7.4)

Schema 9 gains an optional boolean `slr_lineage` field carrying run-level provenance for downstream renderers that need to know whether the pipeline run included a systematic-review stage.

```yaml
slr_lineage: true   # any pipeline stage was deep-research in systematic-review mode
```

**Semantics:**

- `true` iff `bool(incoming_passport.slr_lineage) or any(stage.skill == "deep-research" and stage.mode in {"systematic-review", "slr"} for stage in state_tracker.stages.values())` at the time the passport is written. The OR is monotonic — a true value persists across resume / mid-entry passports whose `state_tracker.stages` was reconstructed from the ledger and may be empty. Run-level, not artifact-level — distinct from `origin_mode` which records the directly-producing skill's mode.
- Producer: `pipeline_orchestrator_agent` writes the field at every handoff transition; in practice only the Stage 1 → Stage 2 transition can flip `false` → `true`, and the OR keeps the value monotonic thereafter. Reference helper: `scripts/slr_lineage.py` `emit(stages, incoming_slr_lineage)` (or the underlying `resolve_from_stages(stages)` when callers need the pre-OR fragment alone).
- Consumer: `disclosure` mode renderer reads it as `RendererInput.slr_lineage` to dispatch `--policy-anchor=prisma-trAIce` per the §4.3 G2 invariant track gate documented in [`academic-paper/references/policy_anchor_disclosure_protocol.md`](../academic-paper/references/policy_anchor_disclosure_protocol.md) §3.1.
- Backward compat: passports written before v3.7.4 lack the field; renderer treats absence as `false` (cold-start path requiring explicit `mode_param='systematic-review'`). Identical to pre-v3.7.4 behavior.
- G1 boundary: this is a passport-level (run-level provenance) field, distinct from corpus-entry-level fields. The §4.4 #11 G1 invariant scope is `literature_corpus_entry.schema.json` (corpus entry data schema, frozen by Decision Doc §2.1); passport-schema extensions follow the v3.6.3 / v3.6.4 / v3.6.7 precedent and are permitted per Decision Doc §4.4 #11.

Spec: [`docs/design/2026-05-15-issue-111-slr-lineage-emission-design.md`](../docs/design/2026-05-15-issue-111-slr-lineage-emission-design.md). Conformance test: `scripts/test_slr_lineage_emission.py`.

---

## Schema 10: Experiment Design (experiment-designer -> data-analyst / simulation-runner / lab-notebook)

**Producer**: `experiment-designer/protocol_compiler_agent`
**Consumer**: `data-analyst/intake_agent` | `simulation-runner/intake_agent` | `lab-notebook/entry_writer_agent`

### Required Fields

| Field | Type | Description |
|-------|------|-------------|
| `experiment_id` | string | Unique experiment identifier (format: `EXP-YYYYMMDD-NNN`) |
| `design_type` | enum | `"RCT"` / `"quasi_experimental"` / `"factorial"` / `"crossover"` / `"single_subject"` / `"correlational"` / `"simulation"` / `"mixed"` |
| `hypotheses` | list[Hypothesis] | Pre-registered hypotheses with direction |
| `variables` | object | `{independent: list[Variable], dependent: list[Variable], control: list[Variable], moderator: list[Variable], mediator: list[Variable]}` |
| `sample` | object | `{target_n: int, power: float, alpha: float, effect_size: string, attrition_buffer: float}` |
| `analysis_plan` | object | `{primary: list[AnalysisSpec], secondary: list[AnalysisSpec], exploratory: list[AnalysisSpec]}` |
| `validity_threats` | list[Threat] | Identified threats with mitigation strategies |
| `protocol_document` | string | Path to full protocol file |
| `timeline` | list[Milestone] | Data collection and analysis milestones |

### Conditional Fields

| Field | Type | Condition | Description |
|-------|------|-----------|-------------|
| `randomization` | object | Required if design_type is `RCT` or `factorial` | `{method: string, seed: int, allocation_ratio: string, schedule: list}` |
| `instruments` | list[Instrument] | Required if primary data collection | Measurement instruments (surveys, rubrics, coding schemes) |

### Hypothesis Object

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique identifier (e.g., `H1`, `H2`) |
| `statement` | string | The hypothesis in declarative form |
| `direction` | enum | `"positive"` / `"negative"` / `"non-directional"` |
| `primary` | boolean | Whether this is a primary or secondary hypothesis |

### Variable Object

| Field | Type | Description |
|-------|------|-------------|
| `name` | string | Variable name |
| `type` | enum | `"continuous"` / `"categorical"` / `"ordinal"` / `"binary"` |
| `operationalization` | string | How the variable is measured |
| `levels` | list[string] | For categorical/ordinal: the levels |

### AnalysisSpec Object

| Field | Type | Description |
|-------|------|-------------|
| `test` | string | Statistical test name (e.g., `"independent_t_test"`, `"one_way_anova"`) |
| `iv` | list[string] | Independent variable(s) for this analysis |
| `dv` | string | Dependent variable |
| `covariates` | list[string] | Covariates (if any) |
| `hypothesis_id` | string | Which hypothesis this analysis tests |

### Threat Object

| Field | Type | Description |
|-------|------|-------------|
| `type` | enum | `"internal"` / `"external"` / `"construct"` / `"statistical"` |
| `name` | string | Specific threat (e.g., `"selection bias"`, `"maturation"`) |
| `likelihood` | enum | `"high"` / `"medium"` / `"low"` |
| `mitigation` | string | Strategy to address the threat |
| `residual_risk` | string | Risk remaining after mitigation |

### Example

```markdown
## Experiment Design

**Experiment ID**: EXP-20260316-001

**Design Type**: quasi_experimental

**Hypotheses**:
- H1 (primary, positive): Students receiving AI-assisted formative assessment will show significantly higher exam scores than the control group
- H2 (secondary, positive): Students in the treatment group will report higher self-efficacy

**Variables**:
- Independent: Teaching method (AI-assisted vs traditional), categorical, 2 levels
- Dependent: Exam score (continuous, 0-100), Self-efficacy (continuous, Likert composite)
- Control: Prior GPA, Gender, Year of study

**Sample**: target_n=180 (90 per group), power=0.80, alpha=0.05, effect_size="d=0.50", attrition_buffer=0.15

**Analysis Plan**:
- Primary: Independent t-test (H1), ANCOVA controlling for prior GPA (H1 robustness)
- Secondary: Independent t-test (H2)
- Exploratory: Moderation analysis (prior GPA x treatment)
```

---

## Schema 11: Experiment Results (data-analyst / simulation-runner -> academic-paper / lab-notebook)

**Producer**: `data-analyst/report_compiler_agent` | `simulation-runner/report_compiler_agent`
**Consumer**: `academic-paper/draft_writer_agent` | `lab-notebook/entry_writer_agent`

### Required Fields

| Field | Type | Description |
|-------|------|-------------|
| `experiment_id` | string | Links to Schema 10 experiment_id |
| `result_type` | enum | `"statistical_analysis"` / `"simulation"` / `"bootstrap"` / `"exploratory"` |
| `dataset_info` | object | `{n_original: int, n_analyzed: int, exclusions: list[string], missing_strategy: string}` |
| `assumption_checks` | list[AssumptionCheck] | Each assumption tested with result and decision |
| `primary_results` | list[AnalysisResult] | Primary analysis results |
| `effect_sizes` | list[EffectSize] | All effect sizes with confidence intervals |
| `tables` | list[Table] | Formatted tables with file paths |
| `figures` | list[Figure] | Publication-quality figures with file paths |
| `apa_results_text` | object | `{primary: string, secondary: string, exploratory: string}` — ready-to-insert APA text |
| `reproducibility` | object | `{script_path: string, seed: int, environment: string, requirements_path: string}` |

### Optional Fields

| Field | Type | Description |
|-------|------|-------------|
| `secondary_results` | list[AnalysisResult] | Secondary analysis results |

### AssumptionCheck Object

| Field | Type | Description |
|-------|------|-------------|
| `assumption` | string | Which assumption (e.g., `"normality"`, `"homogeneity_of_variance"`) |
| `test_used` | string | Statistical test (e.g., `"Shapiro-Wilk"`, `"Levene's"`) |
| `statistic` | float | Test statistic value |
| `p_value` | float | p-value |
| `diagnostic_plot` | string | Path to diagnostic plot file |
| `verdict` | enum | `"met"` / `"violated"` / `"marginal"` |
| `action` | string | Action taken (e.g., `"proceed with parametric"`, `"switch to non-parametric"`) |

### AnalysisResult Object

| Field | Type | Description |
|-------|------|-------------|
| `hypothesis_id` | string | Links to Schema 10 hypothesis (e.g., `H1`) |
| `test` | string | Statistical test used |
| `statistic` | float | Test statistic value |
| `df` | string | Degrees of freedom (e.g., `"2, 87"`) |
| `p_value` | float | p-value |
| `significant` | boolean | Whether p < alpha |
| `apa_string` | string | Full APA-formatted result string |

### EffectSize Object

| Field | Type | Description |
|-------|------|-------------|
| `measure` | string | Effect size type (e.g., `"Cohen's d"`, `"eta_squared"`) |
| `value` | float | Effect size value |
| `ci_lower` | float | 95% CI lower bound |
| `ci_upper` | float | 95% CI upper bound |
| `magnitude` | enum | `"negligible"` / `"small"` / `"medium"` / `"large"` |

### Table Object

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Table identifier (e.g., `"Table 1"`) |
| `caption` | string | APA-formatted table caption |
| `csv_path` | string | Path to CSV file |
| `markdown_path` | string | Path to formatted Markdown file |
| `apa_formatted` | string | Inline APA-formatted table (Markdown) |

### Figure Object

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Figure identifier (e.g., `"Figure 1"`) |
| `caption` | string | APA-formatted figure caption |
| `png_path` | string | Path to PNG file |
| `pdf_path` | string | Path to PDF file |

### Example

```markdown
## Experiment Results

**Experiment ID**: EXP-20260316-001
**Result Type**: statistical_analysis

**Dataset Info**:
- Original N: 195
- Analyzed N: 180 (15 excluded: 8 incomplete data, 7 failed attention checks)
- Missing strategy: Listwise deletion (< 5% missing, MCAR confirmed by Little's test)

**Assumption Checks**:
| Assumption | Test | Statistic | p | Verdict | Action |
|------------|------|-----------|---|---------|--------|
| Normality (treatment) | Shapiro-Wilk | W = 0.98 | .142 | Met | Proceed |
| Normality (control) | Shapiro-Wilk | W = 0.97 | .089 | Met | Proceed |
| Homogeneity of variance | Levene's | F = 1.23 | .269 | Met | Proceed |

**Primary Results**:
- H1: t(178) = 3.42, p < .001, d = 0.51, 95% CI [0.21, 0.81]
  → Significant: Students with AI-assisted assessment scored higher (M = 78.3, SD = 12.1) than control (M = 72.1, SD = 12.8)

**Reproducibility**: script at `experiment_outputs/scripts/analysis.py`, seed=42, environment at `experiment_env/requirements.txt`
```

---

## Schema 12: Lab Record (lab-notebook -> academic-paper / academic-pipeline)

**Producer**: `lab-notebook/provenance_auditor_agent`
**Consumer**: `academic-paper/draft_writer_agent` | `academic-pipeline/pipeline_orchestrator_agent`

### Required Fields

| Field | Type | Description |
|-------|------|-------------|
| `experiment_id` | string | Links to Schema 10 experiment_id |
| `notebook_path` | string | Path to the notebook Markdown file |
| `entry_count` | integer | Total number of entries in the notebook |
| `deviation_count` | integer | Number of protocol deviation entries |
| `file_manifest` | list[FileRecord] | Complete inventory of all experiment artifacts |
| `completeness_score` | float | 0.0-1.0 audit completeness score |
| `environment_snapshot` | object | `{python_version: string, packages: dict, os: string}` |
| `methods_summary` | string | Condensed narrative suitable for paper Methods section |

### Conditional Fields

| Field | Type | Condition | Description |
|-------|------|-----------|-------------|
| `deviations_summary` | list[string] | Required if deviation_count > 0 | One-line summary of each deviation |
| `completeness_gaps` | list[string] | Required if completeness_score < 1.0 | Sections that are incomplete |

### FileRecord Object

| Field | Type | Description |
|-------|------|-------------|
| `path` | string | Relative file path |
| `purpose` | string | What the file contains / is used for |
| `hash` | string | SHA-256 hash of file contents |
| `created` | string | ISO 8601 creation timestamp |

### Example

```markdown
## Lab Record

**Experiment ID**: EXP-20260316-001
**Notebook**: experiment_outputs/logs/notebook_2026-03-16_ai-assessment.md
**Entries**: 14
**Deviations**: 1 (sample fell short of target by 15 students; adjusted power analysis)
**Completeness**: 0.90 (missing: pilot test results not documented)

**Methods Summary**: A quasi-experimental study was conducted with 180 undergraduate physics students across 4 sections at National Taiwan University during Spring 2026. Two sections (n=90) received AI-assisted formative assessment via the XLearn platform; two sections (n=90) received traditional assessment. Data were collected over 16 weeks. One protocol deviation occurred: final sample (N=180) fell below the target (N=195) due to higher-than-expected attrition; post-hoc power analysis confirmed adequate power (0.82) for the observed effect.

**Environment**: Python 3.12.3, pandas 2.2.1, scipy 1.13.0, statsmodels 0.14.1, pingouin 0.5.4
```

---

## Schema 13: Simulation Specification (experiment-designer -> simulation-runner)

**Producer**: `experiment-designer/protocol_compiler_agent` (only when Schema 10 `design_type` is `"simulation"`)
**Consumer**: `simulation-runner/model_builder_agent`

### Required Fields

| Field | Type | Description |
|-------|------|-------------|
| `experiment_id` | string | Links to Schema 10 experiment_id |
| `simulation_type` | enum | `"monte_carlo"` / `"bootstrap"` / `"power_sim"` / `"agent_based"` / `"parameter_sweep"` / `"stochastic_process"` |
| `model_definition` | object | `{description: string, dgp: string, parameters: dict, distributions: dict}` |
| `execution_plan` | object | `{n_iterations: int, burn_in: int, convergence_criterion: string, seeds: list[int]}` |
| `performance_measures` | list[string] | What to measure (e.g., `["bias", "MSE", "coverage", "power"]`) |
| `ademp_checklist` | object | `{aims: string, dgp: string, estimands: list, methods: list, performance: list}` |

### Optional Fields

| Field | Type | Description |
|-------|------|-------------|
| `parameter_grid` | object | For parameter sweeps: `{param_name: [values]}` |

### Example

```markdown
## Simulation Specification

**Experiment ID**: EXP-20260316-002
**Simulation Type**: power_sim

**Model Definition**:
- Description: Simulate power for a 2x3 mixed ANOVA with one between-subjects factor (treatment: 2 levels) and one within-subjects factor (time: 3 levels)
- DGP: Y_ij = mu + alpha_i + beta_j + (alpha*beta)_ij + epsilon_ij, where epsilon ~ N(0, sigma^2)
- Parameters: {mu: 50, alpha: [0, 5], beta: [0, 2, 4], interaction: [0, 0, 0, 0, 1, 3], sigma: 10}
- Distributions: {epsilon: "normal(0, 10)", group_assignment: "uniform(2 levels)"}

**Execution Plan**:
- n_iterations: 10000
- burn_in: 0
- convergence_criterion: MCSE < 0.01
- seeds: [42, 123, 456, 789, 1011]

**Performance Measures**: ["power", "type_I_error", "effect_size_bias"]

**ADEMP Checklist**:
- Aims: Estimate statistical power for a 2x3 mixed ANOVA across a range of sample sizes (N = 30 to 300)
- DGP: Normal errors, balanced groups, compound symmetry covariance
- Estimands: Power to detect interaction effect at alpha = .05
- Methods: Mixed ANOVA via statsmodels
- Performance: Power (proportion of significant results), Type I error rate, bias of eta-squared estimate
```

---

## Schema 14: Methodology Blueprint (deep-research -> academic-pipeline / experiment-designer)

**Producer**: `deep-research/research_architect_agent`
**Consumer**: `academic-pipeline/pipeline_orchestrator_agent` | `experiment-designer/intake_agent` | `academic-paper/intake_agent`

> The Methodology Blueprint is a critical routing artifact that determines whether Stage 1.5 (EXPERIMENT) is triggered. The `pipeline_orchestrator_agent` reads the routing flags to decide the pipeline path.

### Required Fields

| Field | Type | Description |
|-------|------|-------------|
| `research_paradigm` | object | `{selected: string, justification: string}` |
| `method` | object | `{type: enum["qualitative"/"quantitative"/"mixed"], specific_method: string, justification: string}` |
| `data_strategy` | object | `{data_type: enum["primary"/"secondary"/"both"], sources: list[string], sampling: string, time_frame: string}` |
| `analytical_framework` | object | `{technique: string, steps: list[string], tools: list[string]}` |
| `validity_criteria` | list[object] | `[{criterion: string, strategy: string}]` |
| `methodology_subtype` | enum | `"experimental"` / `"quasi_experimental"` / `"simulation"` / `"correlational"` / `"secondary_data_analysis"` / `"survey"` / `"case_study"` / `"content_analysis"` / `"literature_review"` / `"theoretical"` / `"mixed_methods"` |
| `requires_experiment_design` | boolean | Triggers `experiment-designer` at Stage 1.5a when `true` |
| `requires_data_collection` | boolean | Informs `experiment-designer` instrument building |
| `requires_simulation` | boolean | Triggers `simulation-runner` (instead of `data-analyst`) at Stage 1.5b when `true` |
| `routing_justification` | string | 1-2 sentences explaining why routing flags were set |

### Optional Fields

| Field | Type | Description |
|-------|------|-------------|
| `limitations` | list[string] | Known limitations by design, with mitigations |
| `ethical_considerations` | list[string] | Relevant ethical issues |
| `irb_plan` | object | `{level: enum["Exempt"/"Expedited"/"Full Board"], consent_strategy: string, deidentification: string}` |
| `reporting_standard` | string | PRISMA / CONSORT / STROBE / COREQ / SQUIRE |
| `preregistration` | object | `{recommended: boolean, platform: string, status: string}` |

### Example

```markdown
## Methodology Blueprint

### Research Paradigm
**Selected**: Post-positivist
**Justification**: The RQ seeks to measure causal effects of an intervention, requiring controlled comparison

### Method
**Type**: quantitative
**Specific Method**: Quasi-experimental pre-post with comparison group
**Justification**: Random assignment is not feasible at the course-section level

### Data Strategy
**Data Type**: primary
**Sources**: [Undergraduate STEM students at 3 Taiwanese universities]
**Sampling**: Cluster sampling by course section (n=180 target)
**Time Frame**: Spring 2026 semester (16 weeks)

### Analytical Framework
**Technique**: Mixed ANOVA + mediation analysis
**Steps**: [1. Descriptive stats, 2. Assumption checks, 3. 2x3 mixed ANOVA, 4. Mediation via bootstrapped CI]
**Tools**: [Python, statsmodels, pingouin]

### Validity Criteria
| Criterion | Strategy to Ensure |
|-----------|-------------------|
| Internal validity | Pre-test equivalence check, propensity score matching |
| Construct validity | Validated instruments with reported reliability |

### Experiment Pipeline Routing (Required)
**Methodology Subtype**: quasi_experimental
**Requires Experiment Design**: true
**Requires Data Collection**: true
**Requires Simulation**: false
**Routing Justification**: The study requires designing a quasi-experimental protocol with pre/post assessments and primary data collection from students.
```

---

## Schema 15: INSIGHT Collection (deep-research socratic -> deep-research full / academic-paper)

**Producer**: `deep-research/socratic_mentor_agent`
**Consumer**: `deep-research/research_question_agent` (full mode) | `academic-paper/intake_agent`

> The INSIGHT Collection captures key insights discovered during Socratic dialogue. Each insight represents a moment where the user's thinking crystallized around an important aspect of their research.

### Required Fields

| Field | Type | Description |
|-------|------|-------------|
| `session_id` | string | Unique identifier for the Socratic session |
| `insights` | list[Insight] | Ordered list of insights from the dialogue |
| `convergence_status` | enum | `"converged"` / `"partially_converged"` / `"diverged"` |
| `total_rounds` | integer | Number of dialogue rounds completed |
| `rq_summary` | object | The RQ Summary produced at convergence (see `research_question_agent` Socratic Mode output) |

### Insight Object

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique identifier (e.g., `INS-001`) |
| `round` | integer | Which dialogue round this insight emerged from |
| `type` | enum | `"scope_decision"` / `"methodology_choice"` / `"theoretical_anchor"` / `"feasibility_constraint"` / `"novelty_claim"` / `"ethical_consideration"` |
| `content` | string | The insight statement |
| `user_quote` | string | The user's own words that triggered or confirmed this insight |
| `finer_dimension` | enum | Which FINER dimension this insight primarily relates to: `"F"` / `"I"` / `"N"` / `"E"` / `"R"` |

### Example

```markdown
## INSIGHT Collection

**Session ID**: SOC-20260316-001
**Convergence Status**: converged
**Total Rounds**: 8

### Insights

1. **INS-001** (Round 2, Scope Decision, F):
   - Content: Research should focus on formative assessment specifically, not all AI in education
   - User Quote: "I want to know if AI assessment actually helps students learn, not just whether teachers like it"

2. **INS-002** (Round 4, Methodology Choice, F):
   - Content: Quasi-experimental design is most feasible given institutional constraints
   - User Quote: "We can't randomly assign students to different sections — the registrar controls that"

3. **INS-003** (Round 6, Novelty Claim, N):
   - Content: No existing study examines AI formative assessment in Taiwan's STEM context
   - User Quote: "Most studies are from the US or UK, nobody has looked at how this works with our exam-oriented culture"

### RQ Summary
**Research Question Direction**: How does AI-assisted formative assessment affect undergraduate learning outcomes in STEM courses at Taiwanese universities?
**Preliminary FINER Assessment**: [see research_question_agent Socratic Mode output]
```

---

## Schema 16: Concept Lineage Report (deep-research -> academic-paper)

**Producer**: `deep-research/concept_lineage_agent`
**Consumer**: `deep-research/report_compiler_agent` | `academic-paper/literature_strategist_agent`

### Required Fields

| Field | Type | Description |
|-------|------|-------------|
| `concepts` | list[ConceptLineage] | 3-5 central concepts with lineage traced |
| `api_coverage` | object | `{semantic_scholar: "available"/"unavailable", openalex: "available"/"unavailable", api_calls_made: int, fallback_used: bool}` |
| `cross_concept_relationships` | string | How the traced concepts relate to each other |
| `lineage_limitations` | list[string] | Gaps in coverage, inference disclaimers |

### ConceptLineage Object

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `concept_name` | string | Yes | Short label for the concept |
| `definition` | string | Yes | 1-2 sentence working definition as used in this literature |
| `origin` | SourceRef | Yes | Seminal paper that introduced the concept |
| `challengers` | list[ChallengeEntry] | Yes | Papers that challenged or contradicted the concept (may be empty) |
| `refiners` | list[RefinementEntry] | Yes | Papers that extended or modified the concept (may be empty) |
| `current_consensus` | ConsensusAssessment | Yes | Current state of the concept in the field |
| `lineage_tree` | string | Yes | Text-based tree visualization (see agent output format) |
| `verification_method` | enum | Yes | `"api_verified"` / `"bibliography_inferred"` / `"mixed"` |

### SourceRef Object

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `authors` | string | Yes | Author(s) |
| `year` | integer | Yes | Publication year |
| `title` | string | Yes | Paper title |
| `doi` | string | No | DOI if available |
| `citation_count` | integer | No | Total citations (from API) |
| `influential_citations` | integer | No | Influential citations (Semantic Scholar only) |
| `source_id` | string | No | Bibliography source ID if paper is in the corpus (e.g., `[S01]`) |

### ChallengeEntry Object

| Field | Type | Description |
|-------|------|-------------|
| `paper` | SourceRef | The challenging paper |
| `challenge` | string | What specifically was challenged |
| `reason` | string | Why they disagreed (methodology, dataset, context, theoretical lens) |

### RefinementEntry Object

| Field | Type | Description |
|-------|------|-------------|
| `paper` | SourceRef | The refining paper |
| `refinement` | string | What was added or modified |
| `how_concept_evolved` | string | How the concept changed as a result |

### ConsensusAssessment Object

| Field | Type | Description |
|-------|------|-------------|
| `status` | enum | `"established"` / `"contested"` / `"evolving"` / `"superseded"` |
| `statement` | string | 1-2 sentence current consensus |
| `key_evidence` | list[string] | Source IDs or citations supporting this assessment |
| `remaining_disputes` | string | Active disagreements, if any |

### Example

```markdown
## Concept Lineage Report

### API Coverage
- **Semantic Scholar**: Available — 28 API calls made
- **OpenAlex**: Available — 15 API calls made
- **Fallback methods used**: No

### Concept 1: Technology Acceptance Model (TAM)

**Definition**: A theoretical framework predicting user acceptance of technology based on perceived usefulness and perceived ease of use.

**Lineage Tree**:
CONCEPT: Technology Acceptance Model (TAM)
│
├─ ORIGIN (1989)
│  Davis, F.D. — "Perceived Usefulness, Perceived Ease of Use, and User Acceptance"
│  Introduced: Two-factor model (PU + PEOU) predicting behavioral intention
│  Citations: 45,231 total, 8,412 influential
│
├─ CHALLENGES
│  ├─ Bagozzi (2007) — TAM oversimplifies; ignores social/emotional factors
│  └─ Benbasat & Barki (2007) — TAM creates "illusion of progress" via citation without insight
│
├─ REFINEMENTS
│  ├─ Venkatesh et al. (2003) — UTAUT: unified 4 models into single framework
│  ├─ Venkatesh & Bala (2008) — TAM3: added determinants of PU and PEOU
│  └─ Dwivedi et al. (2019) — Re-examination with meta-analysis; confirmed core but added context moderators
│
└─ CURRENT CONSENSUS (2024)
   Status: established
   "TAM's core constructs remain valid but insufficient alone; modern applications require context-specific extensions (UTAUT2, cultural moderators)."
   Based on: [S03, S07, S15]

**Verification Method**: api_verified
```

---

## Schema 17: Style Profile (intake -> draft_writer / report_compiler)

**Producer**: `academic-paper/intake_agent` (Step 10)
**Consumer**: `academic-paper/draft_writer_agent` | `deep-research/report_compiler_agent`
**Carried by**: `academic-pipeline` Material Passport (optional field)

### Required Fields

| Field | Type | Description |
|-------|------|-------------|
| `calibration_source` | list[string] | Filenames or titles of the analyzed writing samples |
| `sample_count` | integer | Number of samples analyzed (minimum 1, recommended 3+) |
| `sentence_length` | object | `{mean: float, stddev: float, rhythm_pattern: string}` |
| `paragraph_length` | object | `{mean_sentences: float, variation: string}` |
| `vocabulary_preferences` | object | `{hedging_words: list[string], transition_words: list[string], preferred_verbs: list[string], formality: string}` |
| `citation_style` | object | `{narrative_ratio: float, parenthetical_ratio: float, density: float, placement: string}` |
| `modifier_style` | enum | `"minimal"` / `"moderate"` / `"elaborate"` |
| `register_shifts` | list[object] | `[{section_name: string, assertiveness_level: string}]` |

### Optional Fields

| Field | Type | Description |
|-------|------|-------------|
| `conflicts_with_discipline` | list[string] | Noted conflicts between personal style and discipline/journal norms |
| `partial_profile` | boolean | `true` if < 3 samples were analyzed (lower confidence) |
| `language_mismatch` | boolean | `true` if samples are in a different language than the target paper |

### Consumption Priority System

```
Priority 1 (HARD):   Discipline conventions — cannot be violated
Priority 2 (STRONG): Target journal conventions — if specified
Priority 3 (SOFT):   Author's personal style — only where it does not conflict with 1 or 2
```

See `shared/style_calibration_protocol.md` for full consumption rules and conflict resolution.

### Example

```markdown
## Style Profile

**Calibration Source**: ["Chen_2024_AI_assessment.pdf", "Chen_2023_formative_feedback.pdf", "Chen_2022_STEM_pedagogy.pdf"]
**Sample Count**: 3

**Sentence Length**: mean: 22, stddev: 8, rhythm: "variable — mixes 10-word punchy sentences with 35-word complex ones"
**Paragraph Length**: mean 5 sentences, variation: "moderate — 3-7 sentences, shorter in Methods"
**Vocabulary Preferences**:
  - Hedging: suggests, appears to, may
  - Transitions: However, In contrast, Yet
  - Reporting verbs: found, argued, noted
  - Formality: moderate-formal
**Citation Style**: narrative 40%, parenthetical 60%, density 2.3/paragraph, placement: mixed
**Modifier Style**: minimal
**Register Shifts**: [Methods: neutral, Results: descriptive, Discussion: assertive, Conclusion: personal]
**Conflicts**: "Author prefers passive voice (68% in samples), but Education discipline conventions favor active voice — using active voice per convention."
```

---

## Schema 18: R&R Traceability Matrix

> #539 optional per-row fields: `cross_model_verdict` (FULLY_ADDRESSED / PARTIALLY_ADDRESSED / NOT_ADDRESSED / MADE_WORSE; present only on `diverges`/`agree` rows) + `cross_model_status` (`agree` / `diverges` / `unavailable` / `not_configured`). Scope: the independent pass evaluates PRIORITY 1 rows only — #539-era Priority 1 rows ALWAYS carry `cross_model_status` (`not_configured` when cross-model is not active); Priority 2/3 rows omit both fields (not evaluated). A Priority 1 row with neither field = pre-#539.

> **Machine-readable sidecar (#576 Spec B):** a contract-mode Stage 3' re-review emits, alongside this human-surface matrix, the machine-readable traceability sidecar defined by [`shared/contracts/re_review/traceability.schema.json`](contracts/re_review/traceability.schema.json) — per-row `phase2a_verdict`/`final_verdict`, typed adjustment chains, frozen new-issue records, dissent/resolution/escalation records, and `decision_inputs`. The sidecar is what `scripts/check_re_review_synthesis.py` recomputes from; Schema 11 prose remains the human surface. Under the contract, `verified` and `status` are DERIVED mechanically from the sidecar's `final_verdict` (`FULLY_ADDRESSED → YES`, `PARTIALLY_ADDRESSED → PARTIAL`, `NOT_ADDRESSED → NO`, `MADE_WORSE → NO`, `CANNOT_VERIFY → CANNOT_VERIFY`). A `[LEGACY-NO-CONTRACT]` run emits no sidecar.

**Producer (multi-stage, Kong A1 / v3.11)**:
- `concern_id` / `priority` / `original_comment` / `reviewer_source`: academic-paper-reviewer (first-round review)
- `commitment_extracted`: revision_coach_agent (Step 3.5 Commitment Extraction Pass)
- `authors_claim` / `revision_location` / `fulfillment_status` / `unfulfilled_rationale` / `residual_action`: academic-paper revision execution (authored), then independently confirmed by re-review
- `verified` / `status` / `quality_assessment`: academic-paper-reviewer (re-review mode)

**Consumer**: academic-paper (revision mode, if further revision needed), pipeline orchestrator. Schema 11 is carried forward via Material Passport (Schema 9) for cross-stage audit.

**Purpose**: Maps every reviewer concern through the full revision cycle — what was raised, what the author claims to have done, where the change is, and whether it was independently verified.

**Required fields**:
- `concern_id`: Unique ID (R1, R2, S1, S2, N1...)
- `priority`: `MUST_FIX` / `SHOULD_FIX` / `CONSIDER`
- `original_comment`: The reviewer's original concern text
- `authors_claim`: What the author states they did (from Response to Reviewers)
- `revision_location`: Section/page/paragraph reference in revised manuscript
- `verified`: `YES` (✅) / `PARTIAL` (⚠️) / `NO` (❌) / `CANNOT_VERIFY` (🔍)
- `status`: `FULLY_ADDRESSED` / `PARTIALLY_ADDRESSED` / `NOT_ADDRESSED` / `MADE_WORSE` / `CANNOT_VERIFY` (#576 — mirrors the contract verdict vocabulary; the `verified` field already carried it)
- `quality_assessment`: Free-text evaluation

**Optional fields**:
- `reviewer_source`: Which reviewer originally raised the concern (EIC, R1, R2, R3, DA)
- `residual_action`: What remains to be done if not fully addressed. This is a single concern-level string (one per Schema 11 row), distinct from the per-commitment `unfulfilled_rationale` field nested inside each `commitment_extracted` object below. Two coherence conventions govern how the two interact:
  - **(a) Semantic relationship on a partial / multi-commitment row.** A commitment's `unfulfilled_rationale` is diagnostic and per-commitment — it explains *why that commitment fell short* (backward-looking, carried on the commitment object itself). `residual_action` is forward-looking and concern-level — it states *what still remains to be done for the whole concern*. They are different granularity and different tense, so a row may legitimately carry both at once; this is neither redundancy nor contradiction. Example: a commitment object with `unfulfilled_rationale: "3-seed std error only; 5-seed deferred per §6"` (why) alongside the row-level `residual_action: "Run 5-seed replication in camera-ready"` (what remains).
  - **(b) Multi-commitment shape convention.** When one concern decomposes into N commitments, `residual_action` stays a single concern-level string (an aggregate of what remains across the concern); it is **not** expanded into a list or split per commitment. The per-commitment "why" lives on each commitment object's `unfulfilled_rationale`; the concern-level "what remains" stays on the row's `residual_action`.
- `commitment_extracted`: (Kong A1 / v3.11; nested-object shape since #268) List of objects extracted from `original_comment` by `revision_coach_agent` Step 3.5. Each object carries three **extraction** fields plus two optional **lifecycle** fields. The extraction fields are written at Step 3.5: `commitment_text` (string, verbatim or minimally normalized promise), `commitment_type` ∈ `{add_experiment, add_analysis, add_clarification, add_citation, restructure, other}`, and `required_evidence_type` ∈ `{new_section, new_figure, new_table, new_citation, methods_paragraph, discussion_paragraph, prose_edit, acknowledgment_only, other}`. Of these nine, seven are **manuscript-evidence** types verified at `revision_location` in the revised manuscript (`new_section`, `new_figure`, `new_table`, `new_citation`, `methods_paragraph`, `discussion_paragraph`, `prose_edit`); `acknowledgment_only` is the one **response-letter-evidence** type verified in the Response to Reviewers (Schema 8); `other` is an underspecified escape hatch that triggers a soft advisory at re-review (see `re_review_mode_protocol` Commitment Ledger Verification). `prose_edit` covers sentence- or paragraph-level prose changes too granular to bucket into the section/figure/table/etc. categories (typo fixes, terminology clarifications, equation formatting, citation-style corrections). The lifecycle fields (`fulfillment_status`, `unfulfilled_rationale`, defined next) are **absent at extraction time** and appended per-object during revision execution. Empty list `[]` is valid (comment carried no extractable commitment, e.g., positive feedback).
  - `commitment_extracted[].fulfillment_status`: (Kong A1 / v3.11; per-object since #268) Optional lifecycle field nested **inside each `commitment_extracted` object** (not a top-level Schema 11 field), ∈ `{fulfilled, partial, not-fulfilled, explicitly-rejected-with-rationale}`. Absent on a commitment object until revision execution fills it. Nesting it inside the object (rather than carrying a separate parallel list) makes index desynchronization between commitment and status structurally impossible (the failure mode #268 closes).
  - `commitment_extracted[].unfulfilled_rationale`: (Kong A1 / v3.11; per-object since #268) Optional lifecycle field nested **inside each `commitment_extracted` object** (not a top-level Schema 11 field): a free-text rationale required iff that object's `fulfillment_status` ∈ `{partial, not-fulfilled, explicitly-rejected-with-rationale}`. **Omitted** (not the empty string) when `fulfillment_status == fulfilled` or absent — the old `""` placeholder existed only to keep the parallel lists aligned and is dead weight in the nested shape. Three valid rationale forms: (a) "done elsewhere, see §X" pointer, (b) "rejected, reasons: …" rationale, (c) "deferred to future work" acknowledgment.

**Validation**:
- Every item from the original Revision Roadmap (Schema 7) must appear in the matrix
- `authors_claim` cannot be empty for Priority 1 items. The flag-as-`CANNOT_VERIFY` CONSEQUENCE of a missing claim is LEGACY-MODE-SCOPED (#576): in contract mode the requirement itself still stands — satisfied by the §11 letter-absent `"—"` fill as the recorded value — but `verified` derives from the sidecar's `final_verdict`, and letter absence travels via the visible §11 markers (`[COMMITMENT-EVIDENCE-ABSENT: ...]` etc.), not via a verified-column flag
- Matrix is carried forward in Material Passport (Schema 9) for audit trail
- Each object in `commitment_extracted` MUST carry the three extraction fields (`commitment_text`, `commitment_type`, `required_evidence_type`). The two lifecycle fields are nested per-object: `fulfillment_status` is optional (absent before revision execution); `unfulfilled_rationale` MUST be present and non-empty iff that object's `fulfillment_status` ∈ `{partial, not-fulfilled, explicitly-rejected-with-rationale}`, and MUST be absent when `fulfillment_status == fulfilled` or absent. There is no separate top-level `fulfillment_status` / `unfulfilled_rationale` list — the equal-length invariant the parallel-list shape needed is retired because length mismatch is now structurally impossible (#268). Empty list `commitment_extracted: []` stays valid (comment carried no extractable commitment). Violations (a non-`fulfilled` commitment object missing its `unfulfilled_rationale`) surface as `COMMITMENT_GAP` advisory at re-review (advisory only — author retains final responsibility).
- **Legacy normalization (pre-#268 artifacts).** If an artifact still carries the old top-level parallel arrays (`fulfillment_status` / `unfulfilled_rationale` as separate lists alongside `commitment_extracted`), normalize them into the nested objects before re-review. **First verify all three were the same length** — a pre-#268 artifact may already be desynchronized (the exact failure mode #268 closes), so do NOT auto-zip a length-mismatched ledger; flag it for manual reconciliation against the source comments instead. Only for an equal-length legacy row: copy the i-th `fulfillment_status` onto the i-th commitment object, and copy the i-th `unfulfilled_rationale` only when non-empty (an empty `""` or missing entry on a non-`fulfilled` status normalizes to an *absent* nested `unfulfilled_rationale` — i.e. the nested COMMITMENT_GAP case, not a literal empty string). Re-review agents then verify ONLY the nested per-object shape; they do not walk parallel top-level arrays.

---

## Schema 19 — Compliance Report (v3.4.0+, renumbered from upstream Schema 12 to avoid collision with fork's Schema 12 Lab Record)

**Source of truth:** [`shared/compliance_report.schema.json`](compliance_report.schema.json)

Mode-aware output of [`compliance_agent`](agents/compliance_agent.md). Three top-level subtrees: `prisma_trAIce` (null for primary research), `raise` (always present), and decision aggregation fields.

- **Emitted by:** `compliance_agent` at Stage 2.5 / 4.5 (pipeline) or pre-finalize (standalone skills)
- **Consumed by:** orchestrator (for checkpoint dashboard), `report_compiler_agent` (for AI Self-Reflection Report compliance summary at Stage 6)
- **Appended to:** `material_passport.compliance_history[]` (append-only)

### Key fields

- `mode`: dispatches payload (see [`shared/agents/compliance_agent.md`](agents/compliance_agent.md) §Dispatch logic)
- `stage`: `"2.5"` or `"4.5"`
- `prisma_trAIce`: `null` when `mode != "systematic_review"`; otherwise tier-bucketed item results
- `prisma_trAIce.protocol_maturity` *(optional, added per issue #95)*: snapshot of the upstream protocol's self-described maturity status (`foundational_proposal` / `delphi_consensus` / `empirically_validated`) plus citation, snapshot date, and a one-paragraph caveat summary. Populated by `compliance_agent` from [`shared/prisma_trAIce_protocol.md`](prisma_trAIce_protocol.md) — its frontmatter (`citation`, `snapshot_date`) is the deterministic source for `upstream_citation` and `snapshot_date`; `status` is derived from the protocol authors' self-description (currently `foundational_proposal` per Holst et al. 2025, until upstream graduates the checklist via formal consensus); `caveat_summary` is composed from the protocol's framing. (Issue #93 / PR #94 add a `§ Status disclaimer` section to the protocol file as the canonical prose source for `caveat_summary`; until that PR lands, agents derive the summary from the Holst 2025 framing.) Omittable for byte-equivalent compatibility with pre-#95 entries (zero-touch).
- `raise.mode`: `"full"` (SR + other_evidence_synthesis) or `"principles_only"` (primary_research)
- `raise.principles`: 4 keys, each with `pass` / `warn` / `fail`
- `raise.roles`: 8 keys, populated only when `raise.mode == "full"`
- `overall_decision`: aggregate across compliance + legacy integrity + v3.2 failure mode
- `user_override`: only present after a user overrides a block; rationale required
- `upstream_sync_status`: `"current"` or `"stale"` (from freshness check)

Full field spec: [`shared/compliance_report.schema.json`](compliance_report.schema.json).

### Material Passport extension

Schema 9 Material Passport gains one optional field, `compliance_history`:

```yaml
compliance_history:
  - <compliance_report entry>
  - <compliance_report entry>
  # append-only; never overwrite, never reorder
```

Ordering: chronological by `generated_at`. A Stage 2.5 FAIL followed by backfill + retry-pass produces two adjacent entries for Stage 2.5 — both preserved.

---

## Schema 20 — Sprint Contract (v3.6.2+, renumbered from upstream Schema 13/13.1 to avoid collision with fork's Schema 13 Simulation Specification)

**Source of truth:** [`shared/sprint_contract.schema.json`](sprint_contract.schema.json)

Machine-checkable pre-registered acceptance criterion for reviewer / writer / evaluator runs. Phase 1 (paper-content-blind) commits the scoring plan; Phase 2 (paper-visible) executes the scored review. Schema 20.1 (v3.6.6) adds writer/evaluator modes via mode-conditional `allOf` branches.

- **Emitted by:** orchestrator (loads template, inlines `generated_at` + optional `agent_amendments`)
- **Consumed by:** reviewer agents (`eic_agent`, `methodology_reviewer_agent`, `domain_reviewer_agent`, `perspective_reviewer_agent`, `devils_advocate_reviewer_agent`), `editorial_synthesizer_agent`, `draft_writer_agent` (`writer_full` mode), evaluator agents (`evaluator_full` mode)
- **Templates:** `shared/contracts/<domain>/<mode>.json` (reviewer/full, reviewer/methodology_focus, writer/full, evaluator/full)

See `academic-paper-reviewer/references/sprint_contract_protocol.md` for orchestration reference.

---

## Validation Rules

1. **Required field check**: All schema fields marked without "(optional)" or "No" in the Required column are REQUIRED. Consumer agents MUST verify all required fields are present before proceeding
2. **Type check**: Fields must match declared types (e.g., `enum` values must be from the allowed set)
3. **Cross-reference check**: Source IDs referenced in Synthesis must exist in Bibliography; RevisionItem IDs in Response to Reviewers must match the Revision Roadmap
4. **Version tracking**: Each handoff artifact MUST carry a Material Passport (Schema 9) with a version label. Version labels must be monotonically increasing within a pipeline run
5. **Failure on missing**: If a required field is missing, return `HANDOFF_INCOMPLETE` with a list of missing fields; do NOT proceed with partial data
6. **Producer validation**: Producing agent must validate output against its schema BEFORE handoff
7. **Consumer validation**: Consuming agent should validate input on receipt and request re-generation if schema violations are found
8. **Integrity gating**: Artifacts that have passed through integrity verification (Schema 5) must have their Material Passport updated with `verification_status: "VERIFIED"` and `integrity_pass_date`
9. **Staleness detection**: If an upstream artifact is modified after a downstream artifact was produced, the downstream artifact's Material Passport should be updated to `verification_status: "STALE"`
10. **Passport freshness**: A Material Passport's integrity results are considered STALE if `integrity_pass_date` is more than 24 hours old relative to the current timestamp. Stale passports require re-verification before proceeding
11. **Stage-skip eligibility via passport**: A passport allows skipping Stage 2.5 (pre-review integrity) ONLY when ALL of the following conditions are met: (a) `verification_status` = `"VERIFIED"`, (b) `integrity_pass_date` is within the current session or less than 24 hours old, (c) `version_label` matches the current artifact version (content has not been modified since verification), and (d) the user explicitly confirms the skip. If any condition fails, full Stage 2.5 re-verification is required
12. **Passport does not grant Stage 4.5 skip**: The final integrity check (Stage 4.5) can NEVER be skipped via Material Passport, regardless of passport status. Stage 4.5 always requires full Mode 2 verification
13. **Experiment ID uniqueness**: Schema 10 `experiment_id` must be unique within a pipeline run. Schemas 11, 12, and 13 must reference an existing Schema 10 `experiment_id`
14. **Schema 13 conditionality**: Schema 13 (Simulation Specification) is only produced when Schema 10 `design_type` is `"simulation"`. It is never produced for other design types
15. **Experiment file cross-reference**: Figures and tables referenced in Schema 11 must have corresponding files at the declared paths in `experiment_outputs/`. Consumer agents should verify file existence before proceeding
16. **Reproducibility script validity**: Schema 11 `reproducibility.script_path` must point to a valid Python file. The integrity verification agent (Stage 2.5, Phase F) re-executes this script to verify results match

---

## Schema Versioning

All handoff artifacts MUST include a `schema_version` field at the top level.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `schema_version` | string | Yes | Version of the schema this artifact conforms to (format: `MAJOR.MINOR`) |

Current version for all schemas: `1.0`

See `shared/schema_migrations.md` for the complete versioning protocol, migration rules, and staleness detection.

---

## `data_access_level` (v3.3.2+, from upstream)

Every top-level `SKILL.md` declares `metadata.data_access_level` with one of three values:

- `raw` — consumes unverified sources; must assume adversarial/hallucinated input
- `redacted` — operates on sanitized material; no new raw ingestion
- `verified_only` — runs only after upstream integrity gates

This is a declarative signal (not a runtime permission system). Enforced by `scripts/check_data_access_level.py` in CI. When adding a new skill, pick the value matching the *dirtiest* input the skill may legitimately consume.

## `task_type` (v3.3.2+, from upstream)

Every top-level `SKILL.md` declares `metadata.task_type` with one of two values:

- `outcome-gradable` — the task has an objective scalar metric the skill optimizes against; a third party can score the output without deep context
- `open-ended` — the task's quality depends on domain judgment, interpretive work, or context no metric captures

This is a declarative truth-in-advertising signal. All current ARS skills are `open-ended` because ARS targets humanities/QA/policy work, not benchmark tasks. When adding a new skill, do not invent a third value; if the skill genuinely spans both, split it into two skills.

Enforced by `scripts/check_task_type.py` in CI.

See [`ground_truth_isolation_pattern.md`](ground_truth_isolation_pattern.md) for the rationale and rules behind this annotation.


## v3.3.5 additions (from upstream)

- `benchmark_report.schema.json` + [`benchmark_report_pattern.md`](benchmark_report_pattern.md) — schema for publishing ARS benchmark comparisons with required human baseline + independence fields.
- `repro_lock` sub-block on Material Passport + [`artifact_reproducibility_pattern.md`](artifact_reproducibility_pattern.md) — configuration lockfile (NOT replay guarantee).
