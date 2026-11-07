# Abstract Writing Guide

Used by `draft_writer_agent`.

## Abstract Length & Keyword Regime

The table below is the **single source** for abstract length and keyword counts. The abstract is
English-only: `draft_writer_agent` writes one English abstract plus keywords. Surfaces that state
the default figure (150-300 words, 5-7 keywords) are stating the **Standard** row. Three surfaces
still carry a copy of other figures — `apa7_extended_guide.md`, `latex_template_reference.md`, and
`journal_submission_guide.md` — and are reconciled with this table when each is next revised.

<!-- abstract-regime-table:start -->
| Paper type | Abstract length | Keywords |
|------------|-----------------|----------|
| Standard | 150–300 words | 5–7 |
| Conference | 200–500 words | 5–7 |
| Extended abstract | 500–1,000 words | not declared |
| Dissertation | up to 350 words | 5–7 |
<!-- abstract-regime-table:end -->

Read the row for the run's paper type. Lengths are measured per
[`shared/references/word_count_conventions.md`](../../shared/references/word_count_conventions.md)
— whitespace splitting, ARS-marker removal, and the 3–5% buffer rule. That reference is
pointed at, never replaced. A venue-declared limit (#394 venue profile) takes precedence over
the table.

**Paper-type lookup.** The rows above are deliverable regimes, not the Schema-4 `structure_type`
enum, which declares six values: `IMRaD`, `literature_review`, `theoretical`, `case_study`,
`policy_brief`, `conference`. `IMRaD`, `literature_review`, `theoretical`, and `case_study` read
the **Standard** row; `conference` reads the **Conference** row. `policy_brief` has **no abstract
row**: its deliverable is an Executive Summary, not an abstract
(`academic-paper/agents/structure_architect_agent.md`, Paper Type Adjustments), so no length or
keyword figure applies to it. The **Extended abstract** and **Dissertation** rows have no
`structure_type` producer — the first is declared by an extended-abstract submission, and the
second is carried from the earlier guide, since the paper-type enum declares no `dissertation`
value. The Extended abstract row declares no keyword count: the earlier guide carried none for
that deliverable, and the table declares none rather than inventing one. A conference *paper*'s
abstract is the shorter **Conference** row.

**Reconciliation.** The rows above are one table. This guide's earlier word-count list (Standard
150–250, Conference 200–500, Dissertation up to 350 words; 5–7 keywords) is folded into it. The
Standard row carries 150–300 words, the figure `draft_writer_agent` and the quality checklist
below enforce; a journal that asks for less sets a venue-declared limit, which takes precedence.

## Abstract Types

### Structured Abstract
Contains explicit labeled sections. Required by many journals in social sciences and medicine.

**Sections**: Background, Purpose/Objective, Method, Results/Findings, Conclusion/Implications

### Unstructured Abstract
A single flowing paragraph without labels. Common in humanities and some social sciences.

**Flow**: Context → Problem → Purpose → Method → Key Findings → Implications

### Extended Abstract
Longer, used for conference submissions — a conference *paper*'s abstract is the shorter
**Conference** row of the table above; this guide restates no figure. An extended-abstract
submission reads the **Extended abstract** row. May include brief literature review and preliminary results.

## English Abstract Guidelines

### Word Count
See the table above — the row for the run's paper type. This guide restates no figure; a
venue-declared limit (#394 venue profile) takes precedence.

### Structure (5-Component Model)

#### Component 1: Background (1-2 sentences)
Establish context and identify the problem.

**Patterns**:
- "[Topic] has become increasingly important because..."
- "Despite growing interest in [topic], little is known about..."
- "Recent developments in [field] have raised questions about..."

**Avoid**:
- Starting with "This paper..." (too abrupt)
- Generic statements ("Education is important")
- Overly long historical context

#### Component 2: Purpose (1 sentence)
State the specific objective or research question.

**Patterns**:
- "This study examines [what] in [context]."
- "The purpose of this research is to [verb] [object]."
- "This paper proposes [framework/model] for [application]."

#### Component 3: Method (1-2 sentences)
Describe the approach, data, and analysis.

**Patterns**:
- "Using [method], this study analyzed [data] from [source]."
- "A [design] approach was employed, involving [participants/data]."
- "Data were collected through [instrument] and analyzed using [technique]."

#### Component 4: Findings (2-3 sentences)
Present the key results — be specific.

**Patterns**:
- "The results indicate that [finding 1]. Additionally, [finding 2]."
- "Three key findings emerged: (a) [finding 1], (b) [finding 2], and (c) [finding 3]."
- "The analysis revealed [main finding], with [specific metric/detail]."

**Include**:
- Specific numbers when available (percentages, effect sizes)
- The most important findings (not all findings)

**Avoid**:
- "Results will be discussed" (the abstract IS the discussion)
- Vague findings ("significant results were found")

#### Component 5: Implications (1-2 sentences)
State the significance, practical implications, or recommendations.

**Patterns**:
- "These findings have implications for [practice/policy/theory]."
- "The results suggest that [stakeholders] should [action]."
- "This research contributes to [field] by [contribution]."

### Example (Education)

> Declining enrollment poses existential challenges for private higher education institutions in Taiwan, yet institutional responses remain poorly understood. This study examines the strategic adaptation patterns of 12 private universities experiencing enrollment declines exceeding 20% between 2018 and 2023. Using a multiple case study design, we analyzed institutional documents, enrollment data, and 36 semi-structured interviews with administrators. Three distinct adaptation strategies emerged: program consolidation (n = 5), niche specialization (n = 4), and merger pursuit (n = 3). Institutions adopting niche specialization demonstrated the highest enrollment recovery rates (mean = 12.3%). However, successful adaptation was contingent upon early action — institutions that initiated strategic changes within two years of enrollment decline showed significantly better outcomes than late movers (p < .01). These findings suggest that private institutions should adopt proactive monitoring systems and consider niche specialization as a primary survival strategy.
>
> **Keywords**: higher education, enrollment decline, private universities, institutional strategy, Taiwan

## Keywords Selection

1. **Core concepts** — main variables or constructs (2-3)
2. **Context** — geographical, institutional, or temporal (1-2)
3. **Method** — if distinctive (0-1)
4. **Field** — discipline or sub-field (1)

**Rules**:
- Lowercase (unless proper nouns)
- Complement the title (don't repeat title words verbatim)
- Use established terms (check journal's keyword list if available)
- Keyword count: the keywords column of the table above (not restated here)

## Abstract Quality Checklist

| Check | ✓ |
|-------|---|
| Abstract covers all 5 components | |
| Length within the regime table above for the paper type | |
| Quantitative data accurate and consistent with body | |
| Keyword count within the regime table above | |
| Keywords complement (not duplicate) the title | |
| No citations in the abstract | |
| No abbreviations undefined in the abstract | |
