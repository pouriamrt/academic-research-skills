# Reproducibility Standards — FAIR Principles, TOP Guidelines, and Computational Reproducibility

## Purpose

Reference guide for research reproducibility standards. Covers the FAIR data principles, Transparency and Openness Promotion (TOP) guidelines, a computational reproducibility checklist, file naming conventions, and version control for research. Used by provenance_auditor_agent and entry_writer_agent to ensure experiment records meet modern reproducibility standards.

---

## FAIR Principles

The FAIR principles (Wilkinson et al., 2016) describe how research outputs should be managed to maximize their utility. Originally developed for data, they apply to all research artifacts.

### Findable

Research artifacts must be easy to find for both humans and machines.

| Principle | ID | Description | Lab Notebook Application |
|-----------|----|-------------|-------------------------|
| Globally unique identifier | F1 | Each artifact has a persistent, globally unique identifier | Use experiment IDs (EXP-YYYYMMDD-NNN) and file manifest entry numbers |
| Rich metadata | F2 | Data are described with rich metadata | Every file in the manifest has purpose, producer, creation date, and dependencies |
| Registered in searchable resource | F3 | Metadata are registered or indexed in a searchable resource | Notebook and manifest are searchable plain text; git repository is indexed |
| Identifier in metadata | F4 | Metadata specify the data identifier | SHA-256 hashes uniquely identify file contents |

**Practical actions**:
- Assign experiment IDs at notebook creation (done by notebook_manager_agent)
- Maintain the File Manifest with complete metadata (done by provenance_auditor_agent)
- Use descriptive file names (see File Naming Conventions below)
- Include experiment ID in all output file names

### Accessible

Once found, artifacts must be retrievable through a well-defined protocol.

| Principle | ID | Description | Lab Notebook Application |
|-----------|----|-------------|-------------------------|
| Retrievable by identifier | A1 | Artifacts retrievable using standard protocols | Files accessible via file system paths documented in manifest |
| Open protocol | A1.1 | The retrieval protocol is open, free, and universally implementable | File system and git are open protocols |
| Authentication if needed | A1.2 | Protocol allows authentication/authorization if needed | Git repository access controls |
| Metadata persistence | A2 | Metadata accessible even if data are no longer available | File Manifest preserved even if files are deleted (see manifest maintenance rules) |

**Practical actions**:
- Use relative file paths from project root (portable across systems)
- Store data in non-proprietary formats (CSV, JSON, Markdown, PNG)
- Keep the manifest even if files are archived or relocated
- Document access restrictions (if any) in the notebook Header

### Interoperable

Artifacts must be able to be integrated with other data and work with applications for analysis, storage, and processing.

| Principle | ID | Description | Lab Notebook Application |
|-----------|----|-------------|-------------------------|
| Formal language | I1 | Data use a formal, accessible, shared language | Markdown for text; CSV for tabular data; standard statistical formats |
| FAIR vocabularies | I2 | Data use vocabularies that follow FAIR principles | Schema 10/11/12 field names from shared/handoff_schemas.md |
| Qualified references | I3 | Data include qualified references to other data | Cross-references via NB-XXX IDs and manifest entry numbers |

**Practical actions**:
- Use standard data formats (CSV with header row, UTF-8 encoding)
- Follow Schema 10/11/12 field naming conventions
- Cross-reference entries with explicit NB-XXX links
- Use standard statistical terminology (APA conventions)

### Reusable

Artifacts must be well-described so they can be replicated and combined in different settings.

| Principle | ID | Description | Lab Notebook Application |
|-----------|----|-------------|-------------------------|
| Rich description | R1 | Data are richly described with relevant attributes | Entry templates require structured metadata for each entry type |
| Usage license | R1.1 | Data are released with a clear license | Document license in notebook Header or project README |
| Provenance | R1.2 | Data have detailed provenance | File Manifest tracks producer, dependencies, and creation date |
| Community standards | R1.3 | Data meet domain-relevant community standards | Follow APA, EQUATOR, and discipline-specific standards |

**Practical actions**:
- Complete all required fields in entry templates (never leave blanks)
- Document the license under which data will be shared
- Maintain the dependency chain in the File Manifest
- Follow reporting guidelines (CONSORT, STROBE, PRISMA) as applicable

---

## TOP Guidelines

The Transparency and Openness Promotion (TOP) guidelines (Nosek et al., 2015) define 8 transparency standards at 4 levels.

### TOP Standards Overview

| Standard | Level 0 (Not Implemented) | Level 1 (Disclosure) | Level 2 (Requirement) | Level 3 (Verification) |
|----------|--------------------------|---------------------|----------------------|----------------------|
| **Citation standards** | No policy | Cite all data, code, materials | Require citation of all sources | Verify all citations are accurate |
| **Data transparency** | No policy | Disclose whether data available | Require data posting | Verify data are accessible and usable |
| **Analytic code transparency** | No policy | Disclose whether code available | Require code posting | Verify code reproduces results |
| **Materials transparency** | No policy | Disclose whether materials available | Require materials posting | Verify materials are complete |
| **Design transparency** | No policy | Disclose key design elements | Require adherence to reporting guidelines | Verify reporting guideline compliance |
| **Study preregistration** | No policy | Disclose whether preregistered | Require preregistration | Verify analysis matches preregistration |
| **Analysis plan preregistration** | No policy | Disclose analysis plan status | Require detailed analysis plan | Verify analysis follows plan; flag deviations |
| **Replication** | No policy | Encourage replication | Require replication evidence | Independent replication by journal/reviewer |

### Lab Notebook Contribution to TOP Compliance

The lab notebook directly supports TOP compliance at Level 2-3:

| TOP Standard | How the Lab Notebook Helps |
|-------------|---------------------------|
| Data transparency | File Manifest documents all data files with hashes and locations |
| Analytic code transparency | Analysis scripts are tracked in the manifest with dependencies |
| Materials transparency | Instruments and protocols are documented in Design Record and manifest |
| Design transparency | Design Record captures the full experiment design (Schema 10 fields) |
| Study preregistration | Pre-registration status documented in Design Record |
| Analysis plan preregistration | Analysis plan documented in Design Record; deviations tracked in Deviation Log |
| Replication | Environment Record + File Manifest + analysis scripts enable computational replication |

---

## Computational Reproducibility Checklist

A study is computationally reproducible if another researcher can re-run the analysis code on the provided data and obtain the same results. The following checklist covers the four pillars of computational reproducibility.

### Pillar 1: Code

- [ ] All analysis scripts are included in the project repository
- [ ] Scripts are documented (comments explaining each major step)
- [ ] Scripts can be run end-to-end without manual intervention
- [ ] Script execution order is documented (e.g., `01_clean.py` -> `02_analyze.py` -> `03_figures.py`)
- [ ] Hard-coded file paths are replaced with relative paths or configuration variables
- [ ] Random seeds are set and documented for all stochastic processes
- [ ] No manual data manipulation steps exist outside of scripts (all transformations are scripted)

### Pillar 2: Data

- [ ] Raw data are preserved in their original form (never overwritten)
- [ ] Processed data are stored separately from raw data
- [ ] Data dictionary / codebook is provided (variable names, types, value labels)
- [ ] Missing data encoding is documented (e.g., `NA`, `-999`, empty cell)
- [ ] Data files use non-proprietary formats (CSV, JSON, TSV)
- [ ] Character encoding is documented (UTF-8 preferred)
- [ ] If data cannot be shared (privacy, licensing), a synthetic dataset is provided

### Pillar 3: Environment

- [ ] Programming language and version are documented (e.g., Python 3.12.3)
- [ ] All package dependencies are listed with exact versions (e.g., `requirements.txt` or `environment.yml`)
- [ ] Operating system is documented (may affect numerical precision)
- [ ] Hardware specifications are documented if relevant (e.g., GPU for deep learning)
- [ ] A virtual environment or container specification is provided
- [ ] Instructions for setting up the environment are included

### Pillar 4: Documentation

- [ ] A README file in the project root explains the project structure
- [ ] The lab notebook provides a complete narrative of the research process
- [ ] The File Manifest links all artifacts with provenance
- [ ] Schema 12 (Lab Record) provides a condensed methods summary
- [ ] Deviations from the pre-registered plan are documented
- [ ] Known limitations of the reproducibility package are acknowledged

---

## File Naming Conventions

Consistent file naming makes artifacts findable and sortable.

### General Rules

1. **Lowercase**: Use lowercase for all file names
2. **Hyphens for word separation**: Use hyphens (`-`) not underscores (`_`) or spaces
3. **Date prefix for temporal files**: `YYYY-MM-DD_description.ext`
4. **Version suffix when needed**: `filename_v2.ext` (avoid `final`, `final_final`)
5. **Descriptive but concise**: Balance clarity with brevity (20-60 characters)
6. **No special characters**: Avoid `!@#$%^&*()+=` and non-ASCII characters in file names

### Naming Patterns by File Type

| File Type | Pattern | Example |
|-----------|---------|---------|
| Raw data | `raw_{source}_{date}.csv` | `raw_survey_2026-03-27.csv` |
| Cleaned data | `clean_{description}.csv` | `clean_combined_no-outliers.csv` |
| Analysis script | `{NN}_{action}.py` | `01_clean-data.py`, `02_primary-analysis.py` |
| Result table | `table_{N}_{description}.csv` | `table_1_descriptive-stats.csv` |
| Figure | `figure_{N}_{description}.png` | `figure_1_boxplot-scores.png` |
| Protocol | `protocol_{exp-id}.md` | `protocol_EXP-20260316-001.md` |
| Notebook | `notebook_{date}_{name}.md` | `notebook_2026-03-16_ai-assessment.md` |

### Directory Structure Convention

```
experiment_outputs/
  protocols/           # Experiment design, IRB, consent forms
  data/
    raw/               # Original data (never modified)
    processed/         # Cleaned, transformed data
    codebooks/         # Variable definitions and coding schemes
  scripts/             # All analysis and processing code
  results/
    tables/            # Output tables (CSV + Markdown)
    figures/           # Output figures (PNG + PDF)
    diagnostics/       # Diagnostic plots, assumption checks
  logs/                # Lab notebooks, audit reports
  reports/             # Final reports, Schema 12 exports
experiment_env/        # Environment specification (requirements.txt, etc.)
```

---

## Version Control for Research

### Git Best Practices for Research

1. **Commit frequently**: Each logical unit of work gets its own commit
2. **Write descriptive commit messages**: Explain *why*, not just *what*
3. **Never commit sensitive data**: Use `.gitignore` for credentials, personal data
4. **Tag milestones**: Tag commits at key experiment milestones (e.g., `v1.0-data-collection-complete`)
5. **Branch for experiments**: Use branches for exploratory analyses that may not be kept

### What to Track in Git

| Track | Do Not Track |
|-------|-------------|
| Analysis scripts | Raw data (if large or sensitive — use git-lfs or external storage) |
| Notebooks | Credentials, API keys |
| Configuration files | Compiled files, caches |
| Requirements files | Virtual environment directories |
| Small data files (< 10 MB) | Large binary files (> 100 MB) |
| Documentation | Temporary files |

### .gitignore Recommendations for Research Projects

```gitignore
# Environment
experiment_env/venv/
__pycache__/
*.pyc

# Large data (track via manifest, not git)
experiment_outputs/data/raw/*.csv
experiment_outputs/data/raw/*.xlsx

# Sensitive
.env
credentials.json

# OS artifacts
.DS_Store
Thumbs.db

# Editor
*.swp
*.swo
.vscode/settings.json
```

### Versioning Strategy

| Milestone | Version Tag | Description |
|-----------|-------------|-------------|
| Protocol finalized | `v0.1-protocol` | Experiment design complete |
| Data collection complete | `v0.2-data-collected` | All data gathered |
| Data cleaning complete | `v0.3-data-cleaned` | Analysis-ready dataset |
| Primary analysis complete | `v0.4-analysis` | All primary hypotheses tested |
| Notebook audit passed | `v0.5-audited` | Completeness score >= 0.90 |
| Schema 12 exported | `v1.0-exported` | Ready for paper writing |

---

## References

- Wilkinson, M. D. et al. (2016). The FAIR Guiding Principles for scientific data management and stewardship. *Scientific Data*, 3, 160018. https://doi.org/10.1038/sdata.2016.18
- Nosek, B. A. et al. (2015). Promoting an open research culture. *Science*, 348(6242), 1422-1425. https://doi.org/10.1126/science.aab2374
- National Academies of Sciences, Engineering, and Medicine. (2019). *Reproducibility and Replicability in Science*. National Academies Press.
- Stodden, V., McNutt, M., Bailey, D. H., et al. (2016). Enhancing reproducibility for computational methods. *Science*, 354(6317), 1240-1241.
