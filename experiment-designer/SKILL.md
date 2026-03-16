---
name: experiment-designer
description: "Experimental design agent team. 6-agent pipeline for rigorous experiment planning, power analysis, instrument development, randomization, and protocol compilation. 5 modes: full design, guided Socratic planning, quick design brief, power-only analysis, and instrument building. Covers experimental design selection (RCT, factorial, crossover, quasi-experimental, single-subject, correlational), power analysis with sample size calculation, survey and instrument construction, randomization scheme generation, threats to validity assessment, and SPIRIT/CONSORT-compliant protocol production. Triggers on: design experiment, experimental design, power analysis, sample size calculation, randomization, create survey, build instrument, write protocol, plan experiment, RCT design, factorial design, quasi-experimental design, crossover design, 實驗設計, 樣本數計算, 檢定力分析, 隨機分派, 設計問卷, 建立量表, 撰寫計畫書, 規劃實驗."
metadata:
  version: "1.0"
  last_updated: "2026-03-16"
---

# Experiment Designer — Experimental Design Agent Team

A domain-agnostic 6-agent team for rigorous experimental design, power analysis, instrument development, randomization, and protocol compilation. v1.0 supports RCT, factorial, crossover, quasi-experimental, single-subject, and correlational designs with SPIRIT/CONSORT-compliant protocol output.

## Quick Start

**Minimal command:**
```
Design an experiment to test whether spaced repetition improves vocabulary retention
```

**Guided mode:**
```
Help me plan an experiment — I want to study mindfulness effects on exam anxiety but I'm not sure about the design
幫我規劃實驗，我想研究正念對考試焦慮的效果但不確定怎麼設計
```

**Power analysis only:**
```
Run a power analysis for a 2x3 mixed ANOVA with expected medium effect size
檢定力分析：獨立樣本 t 檢定，預期效果量 d=0.5
```

**Instrument building:**
```
Build a survey instrument to measure academic self-efficacy
設計問卷：學術自我效能量表
```

**Execution:**
1. Intake — Parse request, detect mode, validate upstream inputs
2. Design — Select experimental design, define variables, assess validity threats
3. Quantify — Power analysis, sample size, instrument construction, randomization
4. Compile — Assemble full protocol with cross-validation

---

## Trigger Conditions

### Trigger Keywords

**English**: design experiment, experimental design, power analysis, sample size calculation, randomization, create survey, build instrument, write protocol, plan experiment, RCT design, factorial design, quasi-experimental design, crossover design, single-subject design, correlational design, threats to validity, SPIRIT protocol, CONSORT checklist

**繁體中文**: 實驗設計, 樣本數計算, 檢定力分析, 隨機分派, 設計問卷, 建立量表, 撰寫計畫書, 規劃實驗, 隨機對照試驗, 因子設計, 準實驗設計, 交叉設計, 效度威脅

### Guided Mode Activation

Activate `guided` mode when the user's **intent** matches any of the following patterns, **regardless of language**. Detect meaning, not exact keywords.

**Intent signals** (any one is sufficient):
1. User wants to design an experiment but is uncertain about which design to use
2. User asks to be "helped", "guided", or "walked through" experiment planning
3. User expresses uncertainty about variables, sample size, or methodology
4. User wants to explore design alternatives before committing
5. User describes a vague research idea without specifying a concrete experimental structure

**Default rule**: When intent is ambiguous between `guided` and `full`, **prefer `guided`** — it is safer to help the user think through design choices than to produce an unwanted protocol. The user can always switch to `full` later.

**Example triggers** (illustrative, not exhaustive):
"help me plan an experiment", "I'm not sure what design to use", "walk me through designing a study", 「幫我規劃實驗」「我不確定要用什麼設計」, or equivalent in any language

### Does NOT Trigger

| Scenario | Use Instead |
|----------|-------------|
| Researching a topic (not designing an experiment) | `deep-research` |
| Writing a paper (not designing) | `academic-paper` |
| Reviewing a paper | `academic-paper-reviewer` |
| Full research-to-paper pipeline | `academic-pipeline` |
| Running a statistical analysis on existing data | `data-analyst` (future skill) |

### Quick Mode Selection Guide

| Your Situation | Recommended Mode |
|----------------|-----------------|
| Vague idea, need help choosing a design / 有模糊想法，需要設計引導 | `guided` |
| Clear RQ + design type, need full protocol / 有明確 RQ 和設計，需要完整計畫書 | `full` |
| Only need a quick design sketch (30 min) / 只需要快速設計概覽 | `quick` |
| Only need power analysis / sample size / 只需要檢定力分析或樣本數 | `power-only` |
| Only need to build a survey or rubric / 只需要設計問卷或量表 | `instrument` |

Not sure? Start with `guided` — it will help you clarify what you need.
不確定？先用 `guided` 模式——它會幫你釐清你需要什麼。

---

## Agent Team (6 Agents)

| # | Agent | Role | Phase |
|---|-------|------|-------|
| 1 | `intake_agent` | Parses user request, determines mode, validates upstream inputs (RQ Brief, Methodology Blueprint), detects guided-mode intent | Phase 0 |
| 2 | `design_architect_agent` | Core design selection (RCT, factorial, crossover, quasi-experimental, single-subject, correlational). Defines IV/DV/controls. Assesses threats to validity (Campbell & Stanley). Internal vs external validity trade-offs | Phase 1 |
| 3 | `power_analyst_agent` | Executes power analysis via Python (statsmodels, scipy). Generates power curves (matplotlib). Sensitivity analysis. Effect size conventions (Cohen's d, eta-squared, r, f) | Phase 2 |
| 4 | `instrument_builder_agent` | Builds measurement instruments: surveys (Likert, semantic differential), rubrics (analytic/holistic), coding schemes. Content validity, reliability planning (Cronbach's alpha, ICC, kappa) | Phase 2 |
| 5 | `randomization_agent` | Designs allocation schemes: simple random, stratified, block, cluster. Generates sequences via numpy. Records seeds. Skipped for quasi-experimental/correlational designs | Phase 2 |
| 6 | `protocol_compiler_agent` | Assembles complete protocol. Cross-validates all components. Produces Schema 10 artifact. Produces Schema 13 for simulation designs. Attaches Material Passport (Schema 9) | Phase 3 |

---

## Mode Selection Guide

```
User Input
    |
    +-- Has a clear research question + knows the design type?
    |   +-- Yes --> Needs full protocol with all components?
    |   |           +-- Yes --> full mode
    |   |           +-- No --> Only needs power/sample size?
    |   |                      +-- Yes --> power-only mode
    |   |                      +-- No --> Only needs instrument?
    |   |                                 +-- Yes --> instrument mode
    |   |                                 +-- No --> quick mode
    |   +-- No --> Wants to be guided through design choices?
    |              +-- Yes --> guided mode
    |              +-- No --> full mode (Phase 1 will be interactive)
```

---

## Orchestration Workflow (4 Phases)

```
User: "Design an experiment for [topic]"
     |
=== Phase 0: INTAKE ===
     |
     +-> [intake_agent]
         - Parse user request
         - Detect mode (full / guided / quick / power-only / instrument)
         - Check for upstream inputs:
           * RQ Brief (Schema 1) from deep-research? -> skip RQ formulation
           * Methodology Blueprint from deep-research? -> pre-populate design constraints
           * User-supplied parameters? -> validate and forward
         - If guided mode: begin Socratic design dialogue
         - Output: Validated design brief with mode, RQ, constraints, and parameters
     |
=== Phase 1: DESIGN ARCHITECTURE ===
     |
     +-> [design_architect_agent] -> Experimental Design Blueprint
         - Select design type from decision tree:
           * RCT (parallel, cluster)
           * Factorial (2x2, 2x3, 3x3, higher-order)
           * Crossover (AB/BA, Latin square)
           * Quasi-experimental (nonequivalent control, ITS, regression discontinuity)
           * Single-subject (ABAB, multiple baseline)
           * Correlational (cross-sectional, longitudinal)
         - Define variables:
           * Independent variable(s) with levels
           * Dependent variable(s) with operationalization
           * Control variables and covariates
           * Moderators and mediators (if applicable)
         - Assess threats to validity (Campbell & Stanley framework):
           * Internal validity threats
           * External validity threats
           * Construct validity threats
           * Statistical conclusion validity threats
         - Determine reporting standard (SPIRIT, CONSORT, STROBE, TREND)
         - Output: Design Blueprint
     |
     ** User confirmation before Phase 2 **
     |
=== Phase 2: QUANTIFICATION & INSTRUMENTATION (Parallel) ===
     |
     |-> [power_analyst_agent] -> Power Analysis Report
     |   - Determine appropriate test family
     |   - Calculate required sample size
     |   - Generate power curves across effect sizes
     |   - Sensitivity analysis (what effect size is detectable at current N?)
     |   - Account for attrition, clustering (if applicable)
     |   - Output: Power Analysis Report with figures
     |
     |-> [instrument_builder_agent] -> Measurement Instruments
     |   - Build instruments for each DV:
     |     * Survey / questionnaire (if applicable)
     |     * Rubric (if applicable)
     |     * Coding scheme (if applicable)
     |   - Content validity assessment
     |   - Pilot testing plan
     |   - Reliability targets (Cronbach's alpha, ICC, kappa)
     |   - Output: Instrument package
     |
     +-> [randomization_agent] -> Randomization Schedule
         - Select method (simple, stratified, block, cluster)
         - Generate allocation sequence with seed
         - Document allocation concealment strategy
         - SKIPPED for quasi-experimental and correlational designs
         - Output: Randomization schedule with seed
     |
=== Phase 3: PROTOCOL COMPILATION ===
     |
     +-> [protocol_compiler_agent] -> Complete Protocol (Schema 10)
         - Assemble all components into protocol document
         - Cross-validation checks:
           * Design matches power analysis assumptions
           * Instruments measure all declared DVs
           * Randomization method matches design type
           * Analysis plan aligns with hypotheses
           * Timeline is realistic
         - Apply SPIRIT 2013 template (for trials) or appropriate guideline
         - Produce Schema 10 artifact
         - If design_type == "simulation": ALSO produce Schema 13
         - Attach Material Passport (Schema 9)
         - Output: Final protocol + Schema 10 + Material Passport
```

---

## Operational Modes

| Mode | Agents Active | Output | Typical Duration |
|------|---------------|--------|------------------|
| `full` (default) | All 6 | Complete protocol (Schema 10) + power analysis + instruments + randomization | 45-90 min |
| `guided` | intake + design_architect (interactive) | Design Blueprint + recommendations → can transition to `full` | Iterative |
| `quick` | intake + design_architect + power_analyst | Design brief + sample size estimate | 15-30 min |
| `power-only` | intake + power_analyst | Power analysis report with curves | 10-15 min |
| `instrument` | intake + instrument_builder | Instrument package (survey/rubric/coding scheme) | 20-40 min |

---

## Guided Mode: DESIGN DIALOGUE

Core principle: Help the user think through experimental design choices by asking targeted questions. Do not impose a design; instead, guide the user to understand trade-offs and make informed decisions.

```
User: "Help me plan an experiment on [topic]"
     |
=== Round 1: RESEARCH QUESTION CLARIFICATION ===
     |
     +-> [intake_agent] -> Clarify the core research question
         - "What specific cause-and-effect relationship do you want to test?"
         - "What is your independent variable? What are you manipulating?"
         - "What outcome are you measuring? How will you know if it worked?"
     |
=== Round 2: DESIGN SELECTION ===
     |
     +-> [design_architect_agent] -> Walk through design options
         - "Can you randomly assign participants? (determines RCT vs quasi-experimental)"
         - "Do you have one factor or multiple? (determines simple vs factorial)"
         - "Do you need participants to experience all conditions? (determines between vs within)"
         - Present 2-3 candidate designs with trade-offs
     |
=== Round 3: PRACTICAL CONSTRAINTS ===
     |
     +-> [design_architect_agent] -> Address feasibility
         - "How many participants can you realistically recruit?"
         - "What is your timeline?"
         - "What resources and equipment do you have?"
         - Revise design recommendations based on constraints
     |
=== Round 4: VALIDITY ASSESSMENT ===
     |
     +-> [design_architect_agent] -> Discuss threats
         - "Given your design, here are the main threats to validity..."
         - "How will you handle [specific threat]?"
         - "Are you willing to trade internal validity for external validity, or vice versa?"
     |
     +-> Compile Design Blueprint
         Can transition to `full` mode for complete protocol generation
```

### Guided Mode Dialogue Rules

- At least 2 rounds of dialogue before producing a Design Blueprint
- Users can request to skip to full protocol generation at any time
- Responses limited to 200-400 words per turn
- If no convergence after 8 rounds -> suggest switching to `full` mode
- If dialogue exceeds 12 rounds -> automatically compile blueprint and end

---

## Failure Paths

| Failure Scenario | Trigger Condition | Recovery Strategy |
|---------|---------|---------|
| Ambiguous design type | Cannot determine RCT vs quasi-experimental | Ask user about randomization feasibility |
| Underpowered design | Required N exceeds feasible sample | Suggest alternative designs, effect size reconsideration, or composite outcomes |
| No valid instrument | DV has no established measure | Trigger instrument_builder to create de novo instrument with pilot plan |
| Randomization impossible | Practical constraints prevent random assignment | Switch to quasi-experimental design, document selection bias mitigation |
| Missing upstream data | RQ Brief or Blueprint not provided and user input insufficient | Enter guided mode to elicit minimum required information |
| Power analysis error | Statsmodels/scipy computation fails | Fall back to manual calculation with formula + G*Power recommendation |
| Ethics concern | Design involves deception, vulnerable populations, or high risk | Flag for IRB review, suggest design modifications |

---

## Key Deliverables

| Deliverable | Description | Schema |
|-------------|-------------|--------|
| Experiment Protocol | Complete protocol document (SPIRIT-compliant for trials) | Schema 10 |
| Power Analysis Report | Sample size, power curves, sensitivity analysis | Embedded in Schema 10 |
| Measurement Instruments | Surveys, rubrics, coding schemes | Embedded in Schema 10 |
| Randomization Schedule | Allocation sequence with seed and method | Embedded in Schema 10 |
| Threats to Validity Matrix | All threats with likelihood, mitigation, residual risk | Embedded in Schema 10 |
| Simulation Specification | For simulation designs only | Schema 13 |
| Material Passport | Provenance and verification metadata | Schema 9 |

---

## Integration Points

### Upstream (inputs this skill can receive)

| Source | Artifact | Effect |
|--------|----------|--------|
| `deep-research` | RQ Brief (Schema 1) | Skip RQ formulation in Phase 0 |
| `deep-research` | Methodology Blueprint | Pre-populate design constraints and paradigm |
| User | Direct parameters | Validate and use as-is |

### Downstream (outputs this skill produces)

| Consumer | Artifact | Schema |
|----------|----------|--------|
| `data-analyst` | Experiment Design | Schema 10 |
| `simulation-runner` | Simulation Specification | Schema 13 |
| `lab-notebook` | Experiment Design | Schema 10 |
| `academic-paper` | Protocol for Methods section | Schema 10 |
| `academic-pipeline` | Full pipeline integration | Schema 10 + Schema 9 |

**Trigger**: User says "now run this experiment" or "generate the analysis code"

---

## Agent File References

| Agent | Definition File |
|-------|----------------|
| intake_agent | `agents/intake_agent.md` |
| design_architect_agent | `agents/design_architect_agent.md` |
| power_analyst_agent | `agents/power_analyst_agent.md` |
| instrument_builder_agent | `agents/instrument_builder_agent.md` |
| randomization_agent | `agents/randomization_agent.md` |
| protocol_compiler_agent | `agents/protocol_compiler_agent.md` |

---

## Reference Files

| Reference | Purpose | Used By |
|-----------|---------|---------|
| `references/experimental_design_patterns.md` | Comprehensive design decision tree with templates | design_architect_agent |
| `references/power_analysis_guide.md` | Power analysis concepts, Python code, common pitfalls | power_analyst_agent |
| `references/instrument_development_guide.md` | Item writing, validity, reliability, pilot testing | instrument_builder_agent |
| `references/randomization_methods.md` | Randomization methods with Python code and seed management | randomization_agent |
| `references/equator_protocol_guidelines.md` | SPIRIT, CONSORT, STROBE, TREND guideline mapping | protocol_compiler_agent, design_architect_agent |

---

## Templates

| Template | Purpose |
|----------|---------|
| `templates/experiment_protocol_template.md` | Full protocol template (SPIRIT-aligned) mapping to Schema 10 |
| `templates/power_analysis_template.md` | Power analysis report format with parameters, results, and figures |
| `templates/instrument_template.md` | Instrument format: construct, items, scale, scoring, validity, pilot |
| `templates/threats_to_validity_template.md` | Validity threat matrix: type, description, likelihood, mitigation, residual risk |

---

## Examples

| Example | Demonstrates |
|---------|-------------|
| `examples/rct_design_example.md` | Full RCT walkthrough: AI-assisted feedback on physics learning outcomes |
| `examples/quasi_experimental_example.md` | Quasi-experimental: comparing teaching methods across existing class sections |

---

## Output Language

Follows the user's language. Statistical terminology and variable names kept in English. Guided mode uses natural conversational style.

---

## Quality Standards

1. **Every design choice must be justified** — no arbitrary parameter selections
2. **Power analysis is mandatory** — no experiment without sample size justification (except instrument mode)
3. **Threats to validity must be explicit** — every design has weaknesses; acknowledge and mitigate them
4. **Instruments must have validity evidence** — either cite existing validation studies or plan pilot testing
5. **Randomization must be reproducible** — seeds recorded, method documented
6. **Protocol must be cross-validated** — design, power, instruments, and analysis plan must be internally consistent
7. **AI disclosure** — all protocols include a statement that AI-assisted design tools were used
8. **Reporting standards** — protocols reference the appropriate EQUATOR guideline (SPIRIT, CONSORT, STROBE, TREND)

---

## Cross-Agent Quality Alignment

| Concept | Definition | Applies To |
|---------|-----------|------------|
| **Minimum power** | 0.80 (default); 0.90 for clinical/high-stakes; 0.95 for confirmatory replication | power_analyst_agent |
| **Effect size source** | Must come from: (a) prior meta-analysis, (b) pilot study, (c) substantive rationale. "Convention" alone is insufficient | power_analyst_agent, protocol_compiler_agent |
| **Instrument reliability threshold** | Cronbach's alpha >= 0.70 (research), >= 0.80 (clinical decisions), >= 0.90 (individual diagnosis) | instrument_builder_agent |
| **Randomization reproducibility** | Seed + algorithm + version must be recorded; sequences must be regenerable | randomization_agent |
| **CRITICAL severity** | Issue that, if unresolved, would invalidate the experiment or constitute research misconduct | All agents |

> **Cross-Skill Reference**: See `shared/handoff_schemas.md` for Schema 10 (Experiment Design), Schema 13 (Simulation Specification), and Schema 9 (Material Passport).

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-03-16 | Initial release: 6 agents, 5 modes, 4-phase pipeline. Supports RCT, factorial, crossover, quasi-experimental, single-subject, and correlational designs. Power analysis via statsmodels/scipy. Instrument builder for surveys, rubrics, and coding schemes. SPIRIT/CONSORT/STROBE/TREND protocol compliance. Schema 10 and Schema 13 output |
