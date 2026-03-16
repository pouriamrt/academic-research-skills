# Lab Notebook Best Practices — Research Record Standards

## Purpose

Comprehensive reference on maintaining rigorous research records. Covers legal and regulatory requirements, academic standards, the contemporaneous recording principle, electronic notebook considerations, and practical guidelines for what and how to record. Used by all lab-notebook agents as a foundational reference.

---

## Why Research Records Matter

### Intellectual Property Protection

A well-maintained lab notebook is the primary evidence for establishing:

1. **Priority of invention**: The notebook documents when an idea was conceived and reduced to practice. In patent disputes, the first to document with corroborating evidence often prevails.
2. **Inventorship**: The notebook shows who contributed to each aspect of the research, establishing proper inventorship for patent applications.
3. **Due diligence**: Funding agencies and institutional technology transfer offices require documented research records to pursue patent protection.

**Key requirements for IP purposes**:
- Entries must be dated and attributable to a specific author
- Entries should be witnessed (signed or reviewed) by someone who understands but did not perform the work
- Pages should be bound or, for electronic notebooks, entries must be tamper-evident (append-only with timestamps)
- Gaps in the record (missing dates, undocumented experiments) weaken IP claims

### Regulatory Compliance

Research records are subject to regulatory requirements in many contexts:

| Regulation / Standard | Applicable To | Key Requirements |
|----------------------|---------------|------------------|
| FDA 21 CFR Part 11 | Pharmaceutical / clinical research | Electronic records must be attributable, legible, contemporaneous, original, accurate (ALCOA) |
| Good Laboratory Practice (GLP) | Preclinical studies | Raw data preserved, deviations documented, amendments signed and dated |
| Good Clinical Practice (GCP) | Clinical trials | Source data verification, audit trail, informed consent documentation |
| IRB / Ethics Board | Human subjects research | Protocol adherence documented, deviations reported |
| NSF / NIH Data Management Plans | Federally funded research (US) | Data retention (typically 3-7 years post-publication), sharing provisions |
| GDPR Article 30 | Research involving EU personal data | Processing activities recorded, data protection measures documented |
| Taiwan Personal Data Protection Act | Research in Taiwan | Collection purpose, data categories, retention period documented |

### Academic Standards

Beyond legal requirements, rigorous research records support:

1. **Reproducibility**: Other researchers (or your future self) can replicate the work
2. **Transparency**: Reviewers and readers can verify claims against the primary record
3. **Accountability**: Research misconduct investigations rely on primary records
4. **Continuity**: When team members leave, the research record preserves institutional knowledge
5. **Publication support**: Methods sections and supplementary materials are derived from the notebook

---

## The Contemporaneous Recording Principle

**Definition**: Research activities should be recorded at the time they occur, not reconstructed later from memory.

### Why Contemporaneous Recording Matters

1. **Accuracy**: Memory degrades rapidly; details are lost within hours
2. **Legal standing**: Post-hoc reconstructions carry significantly less weight in legal proceedings
3. **Bias prevention**: Recording before knowing the outcome prevents unconscious selective reporting
4. **ALCOA compliance**: The "C" in ALCOA (Attributable, Legible, Contemporaneous, Original, Accurate) specifically requires this

### Practical Guidelines

| Situation | Best Practice |
|-----------|--------------|
| Starting a data collection session | Create the `collection` entry before or during the session, not days later |
| Running an analysis | Log the `analysis` entry immediately after obtaining results |
| Discovering a deviation | Record the `deviation` entry as soon as the deviation is noticed |
| Making a methodological decision | Record the `decision` entry during or immediately after the deliberation |
| Noticing something unusual | Record a `note` entry immediately; you can always elaborate later |

### Acceptable Delays

While immediate recording is ideal, brief delays are acceptable:

| Delay | Acceptable? | Condition |
|-------|------------|-----------|
| Same day | Yes | Document by end of the workday |
| Next business day | Acceptable | If end-of-day was impractical; note the delay |
| Within one week | Marginal | Only for administrative entries; flag the delay |
| More than one week | Not acceptable | Reconstructed records should be clearly marked as such |

For entries created after a delay, add a note:
```
**Recording Note**: This entry describes events from [date]. It was recorded on [actual date] due to [reason].
```

---

## What to Record

### The Core Rule

**Record everything that would be needed to understand, evaluate, or reproduce the work.** When in doubt, record it. Excess documentation is a minor inconvenience; insufficient documentation is a serious problem.

### Mandatory Recording Items

| Item | What to Record | Entry Type |
|------|---------------|------------|
| **Date and time** | Every activity with ISO 8601 timestamp | All types |
| **Methods and procedures** | Step-by-step procedures as actually performed (not just "as planned") | collection, preparation, analysis |
| **Observations** | What you observed, including unexpected or negative results | collection, note |
| **Deviations from protocol** | Any departure from the pre-specified plan, no matter how small | deviation |
| **Decisions and rationale** | What you decided and why, including alternatives considered | decision |
| **Data file locations** | Where raw and processed data are stored | collection, preparation |
| **Software and versions** | Exact versions of all software used | environment (note), analysis |
| **Parameter settings** | All configuration parameters, random seeds, thresholds | analysis, simulation |
| **Results** | Statistical results, plots, tables — even preliminary or negative | analysis, simulation |
| **Interpretations** | What you think the results mean (labeled as interpretation) | analysis, decision, note |
| **Errors and corrections** | Mistakes made and how they were corrected | note, deviation |

### Often Overlooked but Important

| Item | Why It Matters |
|------|---------------|
| **Failed attempts** | Prevents others from repeating the same mistakes; may reveal systematic issues |
| **Negative results** | Publication bias toward positive results makes negative findings especially valuable for the record |
| **Environmental conditions** | Temperature, humidity, time of day, participant mood — may explain unexpected variation |
| **Equipment calibration** | Instruments drift; calibration records establish measurement validity |
| **Personnel changes** | Different data collectors may introduce systematic variation |
| **Conversations and advice** | Informal discussions that influenced decisions should be noted |
| **Literature consulted** | Papers or references that informed methodological choices |

---

## The Permanence Principle (Append-Only)

### Definition

Once an entry is written, it is never deleted or modified. Corrections are made by creating a new entry that references the original.

### Rationale

1. **Audit trail integrity**: Modifications destroy the historical record
2. **Legal requirements**: Regulatory frameworks (GLP, GCP, 21 CFR Part 11) prohibit record alteration
3. **Trust**: An append-only record is inherently more trustworthy than one that can be silently edited
4. **Accountability**: The full history of the research process, including mistakes, is part of the scholarly record

### How to Correct Errors

**Wrong approach**: Edit the original entry to fix the error

**Correct approach**: Create a new entry:

```markdown
### Entry [NB-025] -- 2026-04-15 10:30

- **Type**: note
- **Author**: J. Smith
- **Related Entries**: [NB-019 (contains the error)]
- **Related Files**: None

**Correction**: Entry NB-019 reported N=185 participants in Section B. The correct count is N=180.
Five records were duplicate entries from the online system (participant IDs: P112, P134, P156, P178, P190).
The duplicates were identified during data cleaning (see NB-022).
```

### What Constitutes a "Modification"

| Action | Allowed? | Alternative |
|--------|----------|-------------|
| Fix a typo in a recent entry | No (for formal notebooks) | Create a correction note |
| Add information to a past entry | No | Create a new entry with the additional information |
| Delete an entry | Never | Create a note explaining why the entry is superseded |
| Change the entry type | No | Create a new entry with the correct type referencing the original |
| Reorder entries | No | Entries are in chronological order by ID |

---

## Electronic Notebook Considerations

### Advantages Over Paper

1. **Searchability**: Full-text search across all entries
2. **Linking**: Cross-references between entries are clickable and verifiable
3. **Computational integration**: Code, outputs, and analysis results can be directly embedded
4. **Backup and recovery**: Digital files can be backed up automatically
5. **Collaboration**: Multiple researchers can contribute to the same notebook
6. **Version control**: Git provides a tamper-evident change history

### Challenges and Mitigations

| Challenge | Mitigation |
|-----------|-----------|
| Digital records can be silently modified | Use append-only structure; leverage git history for tamper evidence |
| File format obsolescence | Use plain text / Markdown (human-readable, format-agnostic) |
| Data loss from hardware failure | Regular backups; cloud storage; git remote repository |
| Metadata loss (timestamps, authorship) | Embed timestamps and author in every entry; git commit metadata |
| Difficulty establishing authenticity | SHA-256 hashes of key files; git commit signatures (if available) |
| Screen fatigue during collection | Brief entries during collection; elaborate afterward (same day) |

### Git as an Audit Trail

When the notebook is stored in a git repository (as in this skill suite), every commit provides:
- **Timestamp**: When the change was committed
- **Author**: Who made the change
- **Diff**: Exactly what was added (since entries are append-only, diffs should only show additions)
- **Hash**: Git commit hash provides tamper detection

This is not a substitute for the notebook's internal audit trail, but it provides an additional layer of provenance.

### Plain Text / Markdown as the Preferred Format

This skill uses Markdown for notebooks because:
1. **Human-readable**: No special software needed to read the file
2. **Diff-friendly**: Git diffs are meaningful and readable
3. **Portable**: Works on any platform, any editor
4. **Future-proof**: Plain text will be readable for decades; proprietary formats may not
5. **Structured**: Markdown headings, tables, and lists provide sufficient structure without complexity

---

## Witnessing and Review

### Traditional Witnessing

In regulated environments, notebook entries are witnessed by a qualified individual who:
- Understands the work described
- Did not perform the work
- Signs and dates the entry (confirming they have read and understood it)

### Electronic Equivalent

For electronic notebooks in academic research:
1. **Peer review of entries**: A co-investigator reviews key entries (especially design and deviation entries)
2. **Git commit co-authorship**: Using `Co-Authored-By` in commit messages
3. **Audit trail**: The provenance_auditor_agent serves as an automated reviewer
4. **Supervisor sign-off**: Principal investigator reviews the notebook at key milestones

---

## Retention and Archiving

### Retention Periods

| Context | Minimum Retention |
|---------|------------------|
| Federally funded research (US) | 3 years after final report (or longer per grant terms) |
| Clinical research | 15 years (per ICH GCP) |
| Patent-related research | Life of patent + 6 years |
| General academic research | 5-10 years after publication (institutional policy) |
| Student research | Per institutional policy (often 5 years minimum) |

### Archiving Procedure

1. Set notebook status to `completed` when all analyses are finished
2. Run a final `audit` to document the end state
3. Export Schema 12 for downstream use
4. Set notebook status to `archived` for long-term storage
5. Ensure the git repository is backed up to at least one remote location
6. Record the archival date and storage location in the notebook Header

---

## Common Mistakes to Avoid

| Mistake | Problem | Correct Practice |
|---------|---------|-----------------|
| Recording only successful experiments | Survivorship bias; incomplete record | Record all experiments, including failures |
| Writing "see protocol" without specifics | Protocol may change; entry is incomplete | Summarize key procedural details in the entry |
| Using vague language ("some participants") | Not reproducible | Use specific numbers and identifiers |
| Batch recording after weeks | Memory degradation; not contemporaneous | Record at least same-day |
| Modifying old entries | Destroys audit trail | Create correction entries |
| Omitting negative results | Publication bias; wastes future effort | Record all results |
| Not recording environmental details | May explain unexpected variation | Note versions, conditions, settings |
| Mixing interpretation with observation | Conflates data with analysis | Label interpretations explicitly |
