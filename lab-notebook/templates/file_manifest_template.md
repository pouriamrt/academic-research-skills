# File Manifest Template — Artifact Inventory with Provenance Tracking

## Purpose

This template defines the structure for the File Manifest section of the lab notebook. The manifest provides a complete inventory of all experiment artifacts (data files, scripts, outputs, figures, tables) with SHA-256 hashes for integrity verification, creation timestamps, producer attribution, and upstream dependency tracking.

The provenance_auditor_agent maintains this manifest. It is updated during audits and can be verified at any time.

---

## Manifest Table Structure

| # | File Path | Purpose | SHA-256 Hash | Created | Producer | Dependencies |
|---|-----------|---------|-------------|---------|----------|-------------|
| 1 | [relative path from project root] | [what the file contains or is used for] | [64-char hex digest] | [ISO 8601 timestamp] | [agent name, skill name, or person] | [list of upstream file #s or "None"] |

### Column Definitions

| Column | Description | Example |
|--------|-------------|---------|
| **#** | Sequential manifest entry number (1, 2, 3, ...) | `1` |
| **File Path** | Relative path from the project root directory | `experiment_outputs/data/raw/survey_section_a.csv` |
| **Purpose** | Brief description of the file's role in the experiment | `Raw survey responses from Section A participants` |
| **SHA-256 Hash** | SHA-256 hex digest of the file contents (64 characters) | `a3f2b7c9d8e1f0...` (full 64 chars) |
| **Created** | ISO 8601 timestamp when the file was first created | `2026-03-20 14:30` |
| **Producer** | The agent, skill, or person that generated the file | `data-analyst/cleaning_agent` |
| **Dependencies** | Manifest entry numbers of files this file depends on | `#1, #2` or `None` |

---

## File Categories

Organize files in the manifest by category for readability. Use sub-headings within the File Manifest section if the manifest exceeds 10 entries.

### Category: Protocol and Design

Files related to experiment design and pre-registration.

| Typical Files | Purpose |
|--------------|---------|
| `experiment_outputs/protocols/protocol_EXP-*.md` | Full experiment protocol (Schema 10) |
| `experiment_outputs/protocols/preregistration_*.md` | Pre-registration document |
| `experiment_outputs/protocols/irb_approval_*.pdf` | IRB approval letter |
| `experiment_outputs/protocols/consent_form_*.pdf` | Informed consent form |
| `experiment_outputs/protocols/instruments/*.pdf` | Survey instruments, rubrics |

### Category: Raw Data

Original, unmodified data as collected.

| Typical Files | Purpose |
|--------------|---------|
| `experiment_outputs/data/raw/*.csv` | Raw data files |
| `experiment_outputs/data/raw/*.json` | Raw data in JSON format |
| `experiment_outputs/data/raw/codebook_*.md` | Variable codebook |

### Category: Processed Data

Data after cleaning, transformation, and exclusion.

| Typical Files | Purpose |
|--------------|---------|
| `experiment_outputs/data/processed/*.csv` | Cleaned, analysis-ready data |
| `experiment_outputs/data/processed/exclusion_log.md` | Record of excluded cases |

### Category: Scripts

Code used for data processing, analysis, and simulation.

| Typical Files | Purpose |
|--------------|---------|
| `experiment_outputs/scripts/clean_data.py` | Data cleaning script |
| `experiment_outputs/scripts/analysis.py` | Primary analysis script |
| `experiment_outputs/scripts/simulation.py` | Simulation script |
| `experiment_outputs/scripts/figures.py` | Figure generation script |
| `experiment_env/requirements.txt` | Python package requirements |

### Category: Analysis Outputs

Results of statistical analyses and simulations.

| Typical Files | Purpose |
|--------------|---------|
| `experiment_outputs/results/tables/*.csv` | Result tables in CSV |
| `experiment_outputs/results/tables/*.md` | APA-formatted result tables |
| `experiment_outputs/results/figures/*.png` | Publication-quality figures |
| `experiment_outputs/results/figures/*.pdf` | Vector-format figures |
| `experiment_outputs/results/diagnostics/*.png` | Diagnostic plots |
| `experiment_outputs/results/simulation_results.csv` | Simulation output data |

### Category: Notebook and Audit

The notebook itself and audit artifacts.

| Typical Files | Purpose |
|--------------|---------|
| `experiment_outputs/logs/notebook_*.md` | This lab notebook |
| `experiment_outputs/logs/audit_*.md` | Audit report snapshots |
| `experiment_outputs/logs/schema12_*.md` | Schema 12 export artifact |

---

## SHA-256 Hash Generation

### Python Implementation

Use Python's `hashlib` standard library to compute SHA-256 hashes:

```python
import hashlib
from pathlib import Path


def compute_sha256(file_path: str) -> str:
    """
    Compute the SHA-256 hash of a file.

    Reads the file in binary mode using chunked reading
    for memory efficiency with large files.

    Args:
        file_path: Path to the file to hash.

    Returns:
        The 64-character hexadecimal digest string.

    Raises:
        FileNotFoundError: If the file does not exist.
        PermissionError: If the file cannot be read.
    """
    sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            sha256.update(chunk)
    return sha256.hexdigest()


def verify_hash(file_path: str, expected_hash: str) -> bool:
    """
    Verify a file's integrity by comparing its current hash
    to an expected hash value.

    Args:
        file_path: Path to the file to verify.
        expected_hash: The expected SHA-256 hex digest.

    Returns:
        True if the hashes match, False otherwise.
    """
    actual_hash = compute_sha256(file_path)
    return actual_hash == expected_hash


def generate_manifest_entry(
    file_path: str,
    purpose: str,
    producer: str,
    dependencies: str = "None"
) -> dict:
    """
    Generate a manifest entry for a file.

    Args:
        file_path: Relative path from project root.
        purpose: Description of the file's role.
        producer: Agent, skill, or person that created the file.
        dependencies: Comma-separated manifest entry numbers or 'None'.

    Returns:
        Dictionary with all manifest fields.
    """
    from datetime import datetime

    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    return {
        "file_path": str(file_path),
        "purpose": purpose,
        "sha256": compute_sha256(file_path),
        "created": datetime.fromtimestamp(
            path.stat().st_ctime
        ).strftime("%Y-%m-%d %H:%M"),
        "producer": producer,
        "dependencies": dependencies,
    }
```

### Hash Computation Rules

1. **Binary mode**: Always read files in binary mode (`"rb"`) to ensure consistent hashing across platforms
2. **Chunked reading**: Use 8192-byte chunks to handle large files without excessive memory use
3. **Full digest**: Store the complete 64-character hexadecimal digest; never truncate
4. **Deterministic**: The same file content always produces the same hash, regardless of filename, timestamp, or platform
5. **File-level granularity**: Hash individual files, not directories or archives

### Special Cases

| Situation | Action |
|-----------|--------|
| File is too large (> 1 GB) | Hash normally; chunked reading handles large files |
| File is a symlink | Hash the target file, not the link itself |
| File is binary (images, PDFs) | Hash normally; binary mode handles all file types |
| File does not exist | Record `HASH_UNAVAILABLE: File not found` |
| File is permission-restricted | Record `HASH_UNAVAILABLE: Permission denied` |
| File was deleted after creation | Keep the original hash in the manifest; note file status |

---

## Dependency Tracking

Dependencies create a provenance chain showing how files relate to each other:

```
Protocol (#1)
  |
  +-> Raw data (#2, #3)
        |
        +-> Cleaned data (#4)
              |
              +-> Analysis script (#5) uses cleaned data
              |     |
              |     +-> Result tables (#6, #7)
              |     +-> Figures (#8, #9)
              |
              +-> Simulation script (#10) uses cleaned data
                    |
                    +-> Simulation results (#11)
```

### Dependency Rules

1. Raw data files have `None` as dependencies (they are the root of the data chain)
2. Processed data files depend on the raw data files they were derived from
3. Analysis output files depend on both the script that produced them and the data they consumed
4. Figures and tables depend on the analysis scripts and data that generated them
5. The notebook file itself is not listed as a dependency (it is the container, not an artifact)

---

## Manifest Maintenance

### When to Update

| Event | Action |
|-------|--------|
| New file created during experiment | Add entry to manifest |
| File content modified | Recompute hash, record new hash, note modification in a `note` entry |
| File deleted | Do NOT remove from manifest; mark status as "DELETED" in Purpose column |
| Audit performed | Verify all hashes, add new files discovered, flag missing files |

### Staleness Detection

A manifest entry is considered **stale** if:
1. The file's current SHA-256 hash does not match the recorded hash
2. The file's modification timestamp is later than the manifest's last update

Stale entries indicate the file has been modified since the hash was recorded. This is not necessarily an error (files may be legitimately updated), but it must be investigated and documented.

---

## Example Manifest

| # | File Path | Purpose | SHA-256 Hash | Created | Producer | Dependencies |
|---|-----------|---------|-------------|---------|----------|-------------|
| 1 | experiment_outputs/protocols/protocol_EXP-20260316-001.md | Experiment protocol (Schema 10) | a1b2c3d4e5f6... | 2026-03-16 09:00 | experiment-designer | None |
| 2 | experiment_outputs/data/raw/survey_section_a.csv | Raw survey responses, Section A (N=48) | b2c3d4e5f6a7... | 2026-03-27 16:30 | qualtrics_export | None |
| 3 | experiment_outputs/data/raw/survey_section_b.csv | Raw survey responses, Section B (N=45) | c3d4e5f6a7b8... | 2026-04-03 15:45 | qualtrics_export | None |
| 4 | experiment_outputs/data/processed/combined_clean.csv | Cleaned and merged dataset (N=180) | d4e5f6a7b8c9... | 2026-04-10 11:20 | data-analyst/cleaning_agent | #2, #3 |
| 5 | experiment_outputs/scripts/analysis.py | Primary analysis script (t-test, ANCOVA) | e5f6a7b8c9d0... | 2026-04-11 09:00 | data-analyst | None |
| 6 | experiment_outputs/results/tables/descriptive_stats.csv | Descriptive statistics table | f6a7b8c9d0e1... | 2026-04-11 09:15 | data-analyst/report_compiler | #4, #5 |
| 7 | experiment_outputs/results/figures/boxplot_scores.png | Box plot of exam scores by group | a7b8c9d0e1f2... | 2026-04-11 09:20 | data-analyst/report_compiler | #4, #5 |
| 8 | experiment_env/requirements.txt | Python environment specification | b8c9d0e1f2a3... | 2026-03-16 09:00 | researcher | None |
