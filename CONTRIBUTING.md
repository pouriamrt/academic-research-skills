# Contributing to Academic Research Skills

This guide covers the conventions, structures, and processes that keep the plugin consistent and maintainable.

## Project Overview

Academic Research Skills is a Claude Code plugin covering the full academic research lifecycle. It comprises 8 skills, 58 agents, and 18 handoff schemas orchestrated through a multi-stage pipeline (research, experimentation, writing, review, revision, publication). Shared infrastructure in `shared/` provides cross-skill data contracts and integration specifications.

## Repository Structure

```
academic-research-skills/
  .claude-plugin/
    plugin.json              # Plugin manifest (skill registration, metadata)
  .claude/
    CLAUDE.md                # Project instructions and routing rules
  shared/
    handoff_schemas.md       # Cross-skill data contracts (Schema 1-18)
    experiment_infrastructure.md  # Experiment agent shared infrastructure
    superpowers_integration.md    # Superpowers plugin integration spec
    style_calibration_protocol.md # Style Profile calibration and consumption protocol
    schema_migrations.md          # Schema versioning, migration rules, staleness detection
    mode_spectrum.md              # Fidelity vs Originality mode taxonomy
  <skill-name>/              # Each skill follows this layout:
    SKILL.md                 #   Skill definition (frontmatter, modes, triggers)
    agents/                  #   Agent definitions (one .md per agent)
    examples/                #   Usage examples for each mode
    references/              #   Reference materials (style guides, checklists)
    templates/               #   Output templates (reports, matrices, protocols)
  assets/                    # Images for README
  docs/                      # Supplementary documentation
  tools/                     # Validation scripts
  MODE_REGISTRY.md           # Single source of truth for all 24+ modes
  POSITIONING.md             # Design philosophy and allowed/discouraged uses
```

## How to Submit a Contribution

ARS uses the standard **fork-and-PR** workflow. Fork the repo on GitHub, clone your fork, create a branch, make your changes, push to your fork, then open a PR.

**Important**: You cannot push directly to this repo — you must fork it first and submit a PR from your fork.

## What We Accept

### Community-maintained (fast merge)

These contributions can be merged quickly with minimal review:

- **Typo and formatting fixes** — spelling, broken links, markdown rendering issues
- **New examples** — pipeline output showcases, worked examples for specific disciplines
- **Translation improvements** — better zh-TW or EN phrasing in READMEs or agent definitions

### Requires maintainer review

These need careful review because they affect system behavior:

- **Journal and field reference lists** — additions to `top_journals_by_field.md`, new discipline glossaries
- **Evaluation sets** — gold-standard papers for calibration mode, benchmark data
- **New reference files** — methodology guides, citation format references, domain-specific protocols
- **Bug and drift fixes** — version inconsistencies, broken cross-references, incorrect metadata
- **Mode changes** — new modes, trigger keyword changes, oversight level adjustments

### Requires maintainer approval + discussion

Open an issue first before submitting a PR for these:

- **Agent definition changes** — modifications to any file in `*/agents/*.md`
- **IRON RULE modifications** — any change to rules marked with the IRON RULE marker
- **Ethics and integrity rules** — changes to the failure mode checklist, integrity protocols, or ethics review
- **Handoff schema changes** — modifications to `shared/handoff_schemas.md`
- **New skills or modes** — additions to the pipeline

## How to Add or Modify an Agent

Agent files use the pattern `{domain}_{role}_agent.md` and live in `<skill-name>/agents/`.
Examples: `research_architect_agent.md`, `draft_writer_agent.md`, `execution_engine_agent.md`.

**Required sections** in every agent file:

| Section | Purpose |
|---------|---------|
| `## Role Definition` | One-paragraph description of what the agent does |
| `## Core Principles` | 3-5 numbered principles guiding agent behavior |
| `## Workflow` (or `## Process`) | Step-by-step execution algorithm |
| `## Output Format` | Expected output structure with template |
| `## Quality Criteria` | Acceptance criteria the agent must satisfy |

**Optional sections** (include when applicable): `## Collaboration Rules with Other Agents` (upstream/downstream handoffs), `## Edge Case Handling` (failure paths), `## Required Tools` (MCP tools or Skill invocations).

After creating the file, reference the agent from the skill's `SKILL.md` in the appropriate mode's agent sequence.

## How to Add a New Mode

Modes are defined in each skill's `SKILL.md`. To add one:

1. **Add a mode section** in `SKILL.md` with: mode name, description, agent execution sequence, and entry/exit conditions.
2. **Define trigger keywords** in both English and Traditional Chinese under `## Trigger Conditions`:
   ```
   **English**: assumption-check, check assumptions, verify assumptions
   **繁體中文**: 檢驗假設, 假設檢定, 驗證假設
   ```
3. **Update routing rules** in `.claude/CLAUDE.md` if disambiguation with other modes/skills is needed.
4. **Add an example** in the skill's `examples/` directory.
5. **Update `MODE_REGISTRY.md`** with the new mode entry (spectrum position, output, oversight level, triggers).

## How to Create a New Schema

Handoff schemas live in `shared/handoff_schemas.md`. Schemas 1-18 are defined data contracts. New schemas start at number 19.

Each schema entry requires:

```markdown
## Schema N: <Name> (<producer-skill> -> <consumer-skill>)

**Producer**: `<skill>/<agent_name>`
**Consumer**: `<skill>/<agent_name>`

### Required Fields
| Field | Type | Description |
|-------|------|-------------|

### Optional Fields
| Field | Type | Description |
|-------|------|-------------|

### Example
(Complete Markdown example with all required fields populated)
```

Guidelines:
- Every field must declare its type (`string`, `list[string]`, `object`, `enum`, `number`, `boolean`).
- Missing required fields trigger `HANDOFF_INCOMPLETE` in the consuming agent.
- Include a realistic example -- consuming agents use it as a reference format.
- Update all producer and consumer agents to reference the new schema.

## How to Add a New Skill

1. **Create the directory** with at minimum `SKILL.md` and `agents/`. Add `examples/`, `references/`, and `templates/` as needed.

2. **Write SKILL.md** with YAML frontmatter:
   ```yaml
   ---
   name: new-skill
   description: "Include mode list, agent count, and trigger keywords (English + Traditional Chinese)."
   metadata:
     version: "1.0"
     last_updated: "YYYY-MM-DD"
     status: active
     related_skills:
       - <related-skill>
   ---
   ```
   The body should include: Quick Start, Trigger Conditions (bilingual), Mode Definitions, Agent Pipeline, and Output Schemas.

3. **Register in plugin.json** -- add the skill path to the `skills` array in `.claude-plugin/plugin.json`.

4. **Add routing rules** to `.claude/CLAUDE.md` explaining when the new skill triggers versus existing skills.

5. **Define handoff schemas** in `shared/handoff_schemas.md` if the skill produces or consumes cross-skill artifacts.

## How to Add References and Templates

- **References** go in `<skill-name>/references/` using descriptive snake_case names (`apa7_style_guide.md`, `irb_decision_tree.md`). Agents reference them with: `> Reference: references/<filename>.md`
- **Templates** go in `<skill-name>/templates/` with names matching the output type (`research_brief_template.md`, `prisma_report_template.md`).

## Code and Documentation Standards

- **Markdown**: ATX-style headers, pipe tables with header rows, fenced code blocks with language identifiers, one blank line between sections, no trailing whitespace.
- **Bilingual**: Trigger keywords must be in both English and Traditional Chinese. Output language defaults to the user's input language.
- **Version tracking**: Each skill tracks its version in `SKILL.md` frontmatter (`metadata.version`, `metadata.last_updated`). The plugin version is in `.claude-plugin/plugin.json` and `.claude/CLAUDE.md`. Bump the version and update `last_updated` when modifying a skill.

## Testing and Validation

Run validation before submitting a PR:
- `python tools/self_test.py` -- structural integrity check (plugin structure, agent completeness, shared infrastructure, version consistency, documentation health). Run this first.
- `python tools/validate_schemas.py` -- validates handoff schema consistency (fields, producer/consumer declarations, cross-references).
- `python tools/check_schema_versions.py` -- validates schema versioning and migration registry.
- `python tools/generate_dependency_graph.py --output file` -- regenerates the agent dependency graph to verify pipeline connectivity.
- `python tools/generate_dashboard.py --init` -- verifies the dashboard template and state JSON generation.
- `python tools/replay_experiments.py --dry-run` -- checks that reproducibility scripts are discoverable (only relevant if experiment outputs exist).

Manual checks:
- YAML frontmatter in `SKILL.md` is valid.
- Trigger keywords include both English and Traditional Chinese.

## PR Guidelines

- **One concern per PR** — don't mix unrelated changes
- **Describe what and why** — explain the motivation, not just the change
- **Reference issues** — if your PR addresses an open issue, link it
- **Test your changes** — if you're modifying agent definitions, try running the skill to confirm it works as expected
- **Keep READMEs in sync** — if your change affects user-facing documentation, update both `README.md` and `README.zh-TW.md`

## Commit Message Format

Use [conventional commits](https://www.conventionalcommits.org/): `<type>: <description>`

| Type | Use For |
|------|---------|
| `feat` | New skill, agent, mode, or schema |
| `fix` | Bug fix in agent logic, schema correction |
| `docs` | README, CONTRIBUTING, examples, references |
| `refactor` | Restructuring without behavior change |
| `chore` | Plugin manifest, CI, tooling |

Examples: `feat: add bootstrap mode to simulation-runner`, `fix: correct Schema 11 required fields for effect size reporting`

## Governance

### Decision principles

1. **Accuracy over completeness** — we'd rather have fewer, verified journal entries than a long unvetted list
2. **Human-in-the-loop always** — contributions that reduce human oversight or enable fully autonomous paper generation will be declined
3. **No detection evasion** — features designed to make AI-generated text harder to detect (as opposed to higher quality) are out of scope
4. **Discipline diversity welcome** — ARS aims to be domain-agnostic across all academic fields. Discipline-specific modules are encouraged.

## Academic Integrity Policy

This repo is designed to be **assistive, not deceptive**. See [POSITIONING.md](POSITIONING.md) for the full design philosophy. Contributors must not add features designed to evade AI detection tools. If unsure, open an issue to discuss before submitting a PR.

## Credit

Contributors are credited in commit messages, CHANGELOG entries, and the Contributors section of the README. For significant contributions (new features, major reference files), we also add a mention in the relevant release notes.

## License

[CC-BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/) -- free to share and adapt with attribution for non-commercial use. By contributing, you agree that your contributions will be licensed under the same terms.

**Author**: Pouria Mortezaagha
