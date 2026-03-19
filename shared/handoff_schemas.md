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
**Consumer**: `deep-research/synthesis_agent` | `deep-research/source_verification_agent` | `academic-paper/literature_strategist_agent`

### Required Fields

| Field | Type | Description |
|-------|------|-------------|
| `sources` | list[Source] | All identified sources (minimum 15 for full mode, 5 for quick mode) |
| `search_strategy` | object | `{databases: list[string], keywords: list[string], inclusion_criteria: list[string], exclusion_criteria: list[string], date_range: string}` |
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
| `abstract` | object | `{english: string, chinese: string}` (chinese is required only if bilingual) |
| `authors` | list[Author] | Author information with CRediT roles |
| `keywords` | object | `{en: list[string], zh_tw: list[string]}` bilingual keywords (3-6 each) |
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
| `credit_roles` | list[string] | CRediT taxonomy roles |
| `corresponding` | boolean | Is corresponding author |

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

### ReviewerReport Object

| Field | Type | Description |
|-------|------|-------------|
| `reviewer_id` | string | Reviewer identifier (e.g., `EIC`, `R1`, `R2`, `R3`, `DA`) |
| `role` | string | Reviewer role description |
| `dimension_scores` | object | Per-dimension scores (skill-specific) |
| `strengths` | list[string] | Paper strengths identified |
| `weaknesses` | list[Weakness] | Paper weaknesses identified |
| `questions` | list[string] | Questions for the authors |

### Weakness Object

| Field | Type | Description |
|-------|------|-------------|
| `description` | string | What the weakness is |
| `severity` | enum | `critical` / `major` / `minor` |
| `type` | enum | `methodology` / `theory` / `evidence` / `writing` / `structure` / `ethics` |

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
| `type` | enum | `"Major"` / `"Minor"` / `"Editorial"` |
| `priority` | enum | `"must_fix"` / `"should_fix"` / `"consider"` |
| `target_section` | string | Section of the paper to modify |
| `suggested_action` | string | How to address the item |
| `consensus_level` | enum | `"CONSENSUS-4"` / `"CONSENSUS-3"` / `"SPLIT"` / `"DA-CRITICAL"` |
| `verification_criteria` | string | How to confirm the fix is adequate |

### Optional Fields

| Field | Type | Description |
|-------|------|-------------|
| `deadline_suggestion` | string | Suggested timeline for completion |

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
