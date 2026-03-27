# Quick Reference Card

Academic Research Skills -- "I want to X, use skill Y in mode Z"

## By Task

| I want to... | Skill | Mode | Example prompt |
|---|---|---|---|
| Research a topic in depth | `deep-research` | `full` | "Research the effects of sleep deprivation on cognitive performance" |
| Get a quick research brief | `deep-research` | `quick` | "Quick brief on CRISPR gene therapy for sickle cell disease" |
| Clarify my research question | `deep-research` | `socratic` | "Help me think through my research question on climate migration" |
| Review existing literature | `deep-research` | `lit-review` | "Literature review on transformer architectures in NLP" |
| Fact-check a claim | `deep-research` | `fact-check` | "Fact-check: 10,000 steps per day is clinically optimal for health" |
| Do a systematic review | `deep-research` | `systematic-review` | "Systematic review of CBT efficacy for adolescent anxiety" |
| Design an experiment | `experiment-designer` | `full` | "Design an RCT to test mindfulness on exam anxiety" |
| Get guided help designing | `experiment-designer` | `guided` | "Help me plan an experiment on plant growth under LED spectra" |
| Just calculate sample size | `experiment-designer` | `power-only` | "How many participants for a two-group t-test, d=0.5, power=0.8?" |
| Build a survey/instrument | `experiment-designer` | `instrument` | "Build a 20-item Likert scale for measuring tech self-efficacy" |
| Analyze my data | `data-analyst` | `full` | "Analyze this CSV -- run regression on columns X, Y, Z" |
| Get help choosing tests | `data-analyst` | `guided` | "I have pre/post scores for 3 groups -- what test should I use?" |
| Quick descriptive stats | `data-analyst` | `quick` | "Descriptive statistics for my dataset in data.csv" |
| Check my data's assumptions | `data-analyst` | `assumption-check` | "Check normality and homoscedasticity for my ANOVA data" |
| Explore data (EDA) | `data-analyst` | `exploratory` | "Exploratory analysis of this survey dataset" |
| Replicate a published analysis | `data-analyst` | `replication` | "Replicate the analysis from Smith et al. (2023) Table 2" |
| Run a Monte Carlo simulation | `simulation-runner` | `full` | "Monte Carlo simulation of Type I error under non-normality" |
| Run a power simulation | `simulation-runner` | `power-sim` | "Simulate power for a mixed ANOVA with small effect size" |
| Do sensitivity analysis | `simulation-runner` | `sensitivity` | "Sensitivity analysis across effect sizes d=0.2 to d=0.8" |
| Bootstrap my data | `simulation-runner` | `bootstrap` | "Bootstrap 95% CI for the median difference between groups" |
| Start a lab notebook | `lab-notebook` | `full` | "Create a lab notebook for my priming experiment" |
| Log an experiment entry | `lab-notebook` | `log-entry` | "Log today's data collection session -- 24 participants run" |
| Record a deviation | `lab-notebook` | `deviation` | "Record deviation: room temperature was 5C above protocol" |
| Export lab record | `lab-notebook` | `export` | "Export my lab notebook for the paper Methods section" |
| Audit my notebook | `lab-notebook` | `audit` | "Audit my lab notebook for completeness before submission" |
| Write a full paper | `academic-paper` | `full` | "Write a paper from my deep-research output on sleep and cognition" |
| Plan my paper structure | `academic-paper` | `plan` | "Guide me through planning my paper chapter by chapter" |
| Just get an outline | `academic-paper` | `outline-only` | "Outline an IMRaD paper on social media and body image" |
| Revise with reviewer feedback | `academic-paper` | `revision` | "Revise my paper based on these reviewer comments" |
| Generate abstract only | `academic-paper` | `abstract-only` | "Write a bilingual abstract for my completed paper" |
| Convert citation format | `academic-paper` | `format-convert` | "Convert my paper to LaTeX with IEEE citations" |
| Check my citations | `academic-paper` | `citation-check` | "Verify all citations in my manuscript match the reference list" |
| Get my paper reviewed | `academic-paper-reviewer` | `full` | "Review my paper -- simulate a full editorial board" |
| Quick quality assessment | `academic-paper-reviewer` | `quick` | "Quick assessment of my draft before I send to advisor" |
| Focus on methodology review | `academic-paper-reviewer` | `methodology-focus` | "Review only the methodology section of my paper" |
| Interactive review learning | `academic-paper-reviewer` | `guided` | "Walk me through what reviewers would flag in my paper" |
| Verify revisions addressed | `academic-paper-reviewer` | `re-review` | "Re-review my revised paper against the original comments" |
| Full pipeline (research to paper) | `academic-pipeline` | -- | "Run the full academic pipeline on topic X" |

## By Skill

| Skill | Agents | Modes | Typical duration |
|---|---|---|---|
| `deep-research` | 13 | full, quick, socratic, review, lit-review, fact-check, systematic-review | 5-30 min |
| `experiment-designer` | 6 | full, guided, quick, power-only, instrument | 5-20 min |
| `data-analyst` | 7 | full, guided, quick, assumption-check, exploratory, replication | 5-25 min |
| `simulation-runner` | 5 | full, guided, quick, power-sim, sensitivity, bootstrap | 5-30 min |
| `lab-notebook` | 4 | full, log-entry, deviation, snapshot, export, audit | 2-10 min |
| `academic-paper` | 12 | full, plan, outline-only, revision, abstract-only, lit-review, format-convert, citation-check | 10-45 min |
| `academic-paper-reviewer` | 5 | full, re-review, quick, methodology-focus, guided | 10-30 min |
| `academic-pipeline` | 57 | orchestrates all above | 1-3 hours |

## Decision Flowchart

```
Start here
  |
  v
Do you have data already?
  |                     \
  Yes                    No
  |                       \
  v                        v
Need simulation/bootstrap? Do you need an experiment?
  |           \              |              \
  Yes          No            Yes             No
  |             \            |                \
  v              v           v                 v
simulation-   data-      experiment-       deep-research
runner        analyst    designer               |
                 |           |                  v
                 |           v             academic-paper
                 |      data-analyst or         |
                 |      simulation-runner        v
                 |           |         academic-paper-reviewer
                 v           v
            academic-paper <-+
                 |
                 v
         academic-paper-reviewer

Full pipeline (all stages automated): academic-pipeline
```

## Tips

- **Unclear research question?** Start with `deep-research` in `socratic` mode.
- **Unclear paper structure?** Start with `academic-paper` in `plan` mode.
- **Want to learn from the review?** Use `academic-paper-reviewer` in `guided` mode.
- **Lab notebook** is never an entry point -- it accompanies other experiment skills.
- **Language**: Output defaults to the language of your prompt (English or Traditional Chinese).
