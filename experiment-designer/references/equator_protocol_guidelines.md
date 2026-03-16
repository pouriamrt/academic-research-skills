# EQUATOR Protocol Guidelines — Reporting Standard Reference

## Purpose

A reference mapping experimental design types to the appropriate EQUATOR Network reporting guidelines. Covers SPIRIT 2013 (trial protocols), CONSORT 2010 (trial reporting), STROBE (observational), TREND (non-randomized interventions), and SCRIBE (single-subject). Used by the protocol_compiler_agent and design_architect_agent.

---

## Design Type to Guideline Mapping

| Design Type | Protocol Stage | Reporting Stage | Notes |
|-------------|---------------|-----------------|-------|
| RCT (parallel) | SPIRIT 2013 | CONSORT 2010 | Gold standard for randomized trials |
| RCT (cluster) | SPIRIT 2013 | CONSORT (cluster extension) | Must report ICC and design effect |
| Factorial | SPIRIT 2013 | CONSORT (factorial extension) | Report all main effects and interactions |
| Crossover | SPIRIT 2013 | CONSORT (crossover extension) | Report washout, carryover, period effects |
| Nonequivalent control group | SPIRIT 2013 (adapted) | TREND | Non-randomized; report selection bias handling |
| Interrupted time series | — | TREND | Report time series analysis details |
| Regression discontinuity | — | TREND | Report bandwidth, manipulation test |
| Single-subject (ABAB, multiple baseline) | — | SCRIBE 2016 | Report visual analysis and effect sizes |
| Correlational (cross-sectional) | — | STROBE | Not a trial; observational reporting |
| Correlational (longitudinal) | — | STROBE | Report attrition and missing data handling |
| Pragmatic trial | SPIRIT-PRO | CONSORT-SPI / PRECIS-2 | Pragmatic extensions |
| Observational cohort | — | STROBE | Prospective or retrospective |
| Survey | — | CHERRIES | Online survey-specific reporting |

---

## SPIRIT 2013: Standard Protocol Items for Interventional Trials

### Purpose
Provides the minimum content for a clinical trial protocol. Applicable to all interventional studies (not just clinical trials).

### 33-Item Checklist (Key Items)

| Section | Item # | Content | Required For |
|---------|--------|---------|-------------|
| **Administrative** | | | |
| | 1 | Descriptive title identifying study design | All |
| | 2a | Trial registration number and registry name | All |
| | 3 | Protocol version number and date | All |
| | 4a | Funding sources and role of funders | All |
| | 5a-d | Contact details, author contributions, sponsor | All |
| **Introduction** | | | |
| | 6a | Background and rationale | All |
| | 7 | Specific objectives or hypotheses | All |
| **Methods: Participants** | | | |
| | 8 | Trial design (parallel, crossover, factorial, etc.) | All |
| | 9 | Eligibility criteria (inclusion/exclusion) | All |
| | 10 | Settings and locations | All |
| **Methods: Interventions** | | | |
| | 11a | Interventions for each group with sufficient detail for replication | All |
| | 11b | Criteria for discontinuing or modifying interventions | All |
| | 11c | Strategies to improve adherence and monitoring | All |
| | 11d | Relevant concomitant care permitted or prohibited | If applicable |
| **Methods: Outcomes** | | | |
| | 12 | Primary and secondary outcomes, measurement methods, time points | All |
| **Methods: Sample Size** | | | |
| | 14 | Estimated sample size with justification (power analysis) | All |
| **Methods: Recruitment** | | | |
| | 15 | Strategies for achieving adequate enrollment | All |
| **Methods: Assignment** | | | |
| | 16a | Method of generating allocation sequence | Randomized studies |
| | 16b | Type of randomization (block, stratified, etc.) | Randomized studies |
| | 16c | Allocation concealment mechanism | Randomized studies |
| | 17a | Who will generate the sequence, enroll, and assign | Randomized studies |
| **Methods: Blinding** | | | |
| | 17b | Who will be blinded and how; unblinding procedures | If applicable |
| **Methods: Data Collection** | | | |
| | 18a | Plans for data collection, instruments, source data verification | All |
| | 18b | Plans to promote data quality | All |
| **Methods: Statistical** | | | |
| | 20a | Statistical methods for primary and secondary outcomes | All |
| | 20b | Methods for additional analyses (subgroup, adjusted) | If applicable |
| | 20c | Definition of the analysis population (ITT, per-protocol) | All |
| **Methods: Monitoring** | | | |
| | 21a | Data monitoring committee composition and role | If applicable |
| | 21b | Interim analysis plan and stopping guidelines | If applicable |
| **Ethics** | | | |
| | 24 | Plans for informed consent | All |
| | 25 | Confidentiality measures | All |
| | 26a | Plans for collection, assessment, reporting of adverse events | If applicable |
| | 29 | Approval by ethics committee | All |
| **Dissemination** | | | |
| | 31a | Plans for results communication | All |
| | 33 | Protocol amendments process | All |

### Using SPIRIT for Non-Clinical Studies

SPIRIT was designed for clinical trials but can be adapted for behavioral, educational, and social science experiments:

- Replace "adverse events" with "participant burden" or "unintended negative effects"
- Replace "data monitoring committee" with "research oversight" (PI or advisory board)
- "Interventions" becomes "experimental conditions" or "treatments"
- IRB approval replaces clinical ethics committee approval

---

## CONSORT 2010: Consolidated Standards of Reporting Trials

### Purpose
Provides the minimum reporting requirements for randomized controlled trials. Used when WRITING the final report or paper (not the protocol).

### 25-Item Checklist (Key Items)

| Section | Item | Content |
|---------|------|---------|
| Title/Abstract | 1a, 1b | Identify as randomized; structured abstract |
| Introduction | 2a, 2b | Background, objectives/hypotheses |
| Methods: Design | 3a, 3b | Trial design, changes after trial start |
| Methods: Participants | 4a, 4b | Eligibility criteria, settings |
| Methods: Interventions | 5 | Interventions with sufficient replication detail |
| Methods: Outcomes | 6a, 6b | Primary/secondary outcomes, changes post-trial |
| Methods: Sample Size | 7a, 7b | How sample size was determined |
| Methods: Randomization | 8a, 8b, 9, 10 | Sequence generation, allocation concealment, implementation, blinding |
| Methods: Statistics | 12a, 12b | Statistical methods, subgroup/adjusted analyses |
| Results: Flow | 13a, 13b | **CONSORT flow diagram** — participants at each stage |
| Results: Recruitment | 14a, 14b | Dates, reasons for stopping |
| Results: Baseline | 15 | **Baseline demographic/clinical table** |
| Results: Numbers | 16 | Numbers analyzed per group |
| Results: Outcomes | 17a, 17b | Primary/secondary outcome results with effect sizes and CIs |
| Results: Harms | 19 | All important harms or unintended effects |
| Discussion | 20-22 | Limitations, generalizability, interpretation |
| Other | 23-25 | Registration, protocol access, funding |

### CONSORT Flow Diagram

Every RCT report MUST include a CONSORT flow diagram:

```
Assessed for eligibility (n = )
     |
     +-- Excluded (n = )
     |     - Not meeting criteria (n = )
     |     - Declined (n = )
     |     - Other (n = )
     |
     v
Randomized (n = )
     |
     +------+------+
     |             |
Allocated to      Allocated to
Treatment (n = )  Control (n = )
     |             |
Lost to f/u (n=)  Lost to f/u (n=)
Discontinued (n=) Discontinued (n=)
     |             |
Analyzed (n = )   Analyzed (n = )
Excluded from     Excluded from
analysis (n = )   analysis (n = )
```

---

## CONSORT Extensions

### Cluster Trials Extension

Additional items for cluster-randomized trials:

| Item | Additional Requirement |
|------|----------------------|
| Design | Identify as cluster-randomized; define clusters |
| Sample size | Report ICC assumed and observed; number of clusters |
| Randomization | Describe cluster-level randomization method |
| Baseline | Report cluster-level and individual-level characteristics |
| Results | Report ICC for primary outcome; account for clustering in analysis |
| Flow diagram | Show cluster and individual flow separately |

### Factorial Extension

Additional items:

| Item | Additional Requirement |
|------|----------------------|
| Design | Specify factorial structure (e.g., 2x2) |
| Hypotheses | State hypotheses for main effects AND interaction |
| Sample size | Power for interaction (if primary hypothesis) |
| Analysis | Report all main effects and interactions, even non-significant |
| Results | Use factorial table or figure showing cell means |

### Crossover Extension

Additional items:

| Item | Additional Requirement |
|------|----------------------|
| Design | Identify as crossover; state number of periods and treatments |
| Washout | Describe washout period duration and rationale |
| Carryover | Test for carryover effects; report results |
| Period effects | Test and report period effects |
| Analysis | Use appropriate crossover analysis (paired, mixed model) |

---

## TREND: Transparent Reporting of Evaluations with Nonrandomized Designs

### Purpose
For quasi-experimental and non-randomized intervention studies. Fills the gap where CONSORT does not apply.

### 22-Item Checklist (Key Differences from CONSORT)

| Section | TREND-Specific Requirements |
|---------|---------------------------|
| Design | Describe how units were allocated to study conditions (without randomization) |
| Participants | Describe the method of selection and potential for selection bias |
| Comparability | Describe any methods used to reduce selection bias (matching, propensity scores, statistical adjustment) |
| Baseline data | Report baseline characteristics for each group; assess baseline equivalence |
| Confounders | Identify potential confounders and how they were addressed |
| Analysis | Describe methods for handling potential confounders (ANCOVA, DiD, PSM, etc.) |
| Limitations | Explicitly address threats to internal validity from lack of randomization |

### When to Use TREND

- Nonequivalent control group designs
- Interrupted time series
- Regression discontinuity designs
- Before-after studies without randomization
- Natural experiments
- Program evaluations where randomization was not feasible

---

## STROBE: Strengthening the Reporting of Observational Studies in Epidemiology

### Purpose
For observational (non-interventional) studies: cross-sectional, cohort, and case-control designs.

### 22-Item Checklist (Key Items)

| Section | Key Requirements |
|---------|-----------------|
| Design | State the study design with commonly used terms |
| Setting | Describe setting, locations, dates, follow-up |
| Participants | Eligibility criteria, sources, selection methods |
| Variables | Define all outcomes, exposures, predictors, confounders |
| Measurement | Sources of data, instrument details, comparability |
| Bias | Describe efforts to address potential sources of bias |
| Sample size | Explain how sample size was determined |
| Statistical | Describe all statistical methods, confounding control, missing data handling |
| Results | Report numbers at each study stage (flow); baseline characteristics; main results with CIs |
| Limitations | Discuss limitations, direction of bias |

### When to Use STROBE

- Correlational studies (cross-sectional, longitudinal)
- Survey research
- Secondary data analyses
- Epidemiological studies
- Any non-interventional, non-experimental design

---

## SCRIBE 2016: Single-Case Reporting Guideline in Behavioural Interventions

### Purpose
For single-subject experimental designs (ABAB, multiple baseline, alternating treatments, etc.).

### Key Items

| Section | Requirements |
|---------|-------------|
| Design | Identify specific single-case design; describe phase sequence |
| Participants | Detailed description of participant(s) including relevant characteristics |
| Setting | Describe setting in detail (clinical, educational, home) |
| Baseline | Describe baseline measurement procedures; report baseline stability criteria |
| Intervention | Describe intervention with sufficient detail for replication |
| Outcome measures | Define target behavior, measurement method, data collection procedures |
| Inter-observer agreement | Report inter-rater reliability for behavioral observations |
| Procedural fidelity | Describe how intervention fidelity was monitored |
| Visual analysis | Present data graphically; describe visual analysis procedures |
| Effect size | Report appropriate effect size (PND, Tau-U, BC-SMD, or other) |
| Replication | Describe replication logic (within-participant or across participants) |

---

## CHERRIES: Checklist for Reporting Results of Internet E-Surveys

### Purpose
Specific to online/web-based surveys. Complements STROBE.

### Key Items

| Item | Requirement |
|------|------------|
| Design | Open survey vs closed survey (known population vs open internet) |
| Recruitment | How respondents were invited (email, social media, website) |
| Survey development | Pilot testing, cognitive pretesting |
| Technical | Survey platform, cookies/IP address checking to prevent duplicates |
| Response rate | Unique visitors, started survey, completed survey |
| Completeness | Handling of incomplete responses |
| Analysis | Analysis of non-response bias |

---

## Guideline Selection Decision Tree

```
What type of study are you reporting?
|
+-- Randomized experiment (any type)
|   |
|   +-- Protocol (before the study)? --> SPIRIT 2013
|   |
|   +-- Report (after the study)?
|       +-- Standard RCT --> CONSORT 2010
|       +-- Cluster RCT --> CONSORT + Cluster extension
|       +-- Factorial --> CONSORT + Factorial extension
|       +-- Crossover --> CONSORT + Crossover extension
|       +-- Pragmatic trial --> CONSORT + PRECIS-2
|
+-- Non-randomized intervention study
|   +-- TREND
|
+-- Observational (no intervention)
|   +-- STROBE
|   +-- Online survey? Also use CHERRIES
|
+-- Single-subject design
|   +-- SCRIBE 2016
|
+-- Systematic review / Meta-analysis
    +-- PRISMA 2020 (see deep-research references)
```

---

## Practical Application

### For the Protocol Stage (experiment-designer output)

The protocol_compiler_agent should:

1. Identify the correct guideline based on design type
2. Map protocol sections to guideline items
3. Include a compliance checklist in the protocol appendix
4. Note which items are "not applicable" with justification

### For the Reporting Stage (academic-paper output)

When the experiment results are written up, the draft_writer_agent should:

1. Follow the identified reporting guideline
2. Complete the full checklist
3. Include the checklist as supplementary material
4. Ensure the flow diagram (CONSORT) or phase diagram (SCRIBE) is included

---

## Key Resources

| Guideline | URL | Key Publication |
|-----------|-----|-----------------|
| SPIRIT 2013 | spirit-statement.org | Chan et al. (2013). Ann Intern Med, 158(3), 200-207 |
| CONSORT 2010 | consort-statement.org | Schulz et al. (2010). BMJ, 340, c332 |
| STROBE | strobe-statement.org | von Elm et al. (2007). Lancet, 370(9596), 1453-1457 |
| TREND | cdc.gov/trendstatement | Des Jarlais et al. (2004). Am J Public Health, 94(3), 361-366 |
| SCRIBE | — | Tate et al. (2016). Arch Sci Psychol, 4(1), 1-9 |
| CHERRIES | — | Eysenbach (2004). J Med Internet Res, 6(3), e34 |
| EQUATOR Network | equator-network.org | Hub for all reporting guidelines |
