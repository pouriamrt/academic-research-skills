# Provenance Tracking Guide — SHA-256 Hashing, Version Tracking, and Dependency Chains

## Purpose

Technical reference for data provenance tracking in the lab notebook system. Covers SHA-256 hashing with Python's `hashlib`, file version tracking strategies, upstream dependency chain management, Material Passport (Schema 9) integration, staleness detection, and automated hash verification. Used primarily by the provenance_auditor_agent.

---

## SHA-256 Hashing

### Why SHA-256

SHA-256 (Secure Hash Algorithm 256-bit) produces a 256-bit (32-byte) hash, represented as a 64-character hexadecimal string. It is used in the lab notebook system because:

1. **Collision resistance**: The probability of two different files producing the same hash is approximately 1 in 2^128 — effectively impossible
2. **Deterministic**: The same file content always produces the same hash
3. **One-way**: You cannot reconstruct the file from the hash (privacy-safe for sensitive data)
4. **Standard**: SHA-256 is widely used (git, SSL/TLS, blockchain, FDA 21 CFR Part 11 compliance)
5. **Available**: Python's `hashlib` includes it in the standard library (no extra dependencies)

### Core Implementation

```python
import hashlib
from pathlib import Path


def compute_sha256(file_path: str) -> str:
    """
    Compute the SHA-256 hash of a file.

    Reads the file in binary mode using 8 KB chunks for memory efficiency.
    Handles files of any size without loading the entire file into memory.

    Args:
        file_path: Absolute or relative path to the file.

    Returns:
        64-character hexadecimal digest string.

    Raises:
        FileNotFoundError: If the file does not exist.
        PermissionError: If the file cannot be read.
        IsADirectoryError: If the path points to a directory.
    """
    sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            sha256.update(chunk)
    return sha256.hexdigest()
```

### Batch Hashing

For generating hashes for all files in a directory:

```python
import hashlib
from pathlib import Path
from datetime import datetime


def compute_sha256(file_path: str) -> str:
    """Compute SHA-256 hash of a single file."""
    sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            sha256.update(chunk)
    return sha256.hexdigest()


def hash_directory(directory: str, extensions: list[str] = None) -> list[dict]:
    """
    Compute SHA-256 hashes for all files in a directory.

    Args:
        directory: Path to the directory to scan.
        extensions: Optional list of file extensions to include
                    (e.g., ['.csv', '.py', '.md']). If None, all files.

    Returns:
        List of dicts with keys: path, hash, size, modified.
    """
    results = []
    dir_path = Path(directory)

    for file_path in sorted(dir_path.rglob("*")):
        if not file_path.is_file():
            continue
        if extensions and file_path.suffix.lower() not in extensions:
            continue

        stat = file_path.stat()
        results.append({
            "path": str(file_path.relative_to(dir_path)),
            "hash": compute_sha256(str(file_path)),
            "size": stat.st_size,
            "modified": datetime.fromtimestamp(
                stat.st_mtime
            ).strftime("%Y-%m-%d %H:%M"),
        })

    return results
```

### Hash Verification

To verify that a file has not changed since it was last hashed:

```python
def verify_file_integrity(
    file_path: str,
    expected_hash: str
) -> dict:
    """
    Verify a file's integrity against an expected hash.

    Args:
        file_path: Path to the file to verify.
        expected_hash: The expected SHA-256 hex digest (64 chars).

    Returns:
        Dict with keys: path, expected, actual, match, status.
    """
    try:
        actual_hash = compute_sha256(file_path)
        match = actual_hash == expected_hash
        return {
            "path": file_path,
            "expected": expected_hash,
            "actual": actual_hash,
            "match": match,
            "status": "VERIFIED" if match else "MODIFIED",
        }
    except FileNotFoundError:
        return {
            "path": file_path,
            "expected": expected_hash,
            "actual": None,
            "match": False,
            "status": "MISSING",
        }
    except PermissionError:
        return {
            "path": file_path,
            "expected": expected_hash,
            "actual": None,
            "match": False,
            "status": "PERMISSION_DENIED",
        }


def verify_manifest(manifest: list[dict]) -> dict:
    """
    Verify all files in a manifest.

    Args:
        manifest: List of dicts, each with 'path' and 'hash' keys.

    Returns:
        Summary dict with counts and detailed results.
    """
    results = []
    verified = 0
    modified = 0
    missing = 0
    errors = 0

    for entry in manifest:
        result = verify_file_integrity(entry["path"], entry["hash"])
        results.append(result)

        if result["status"] == "VERIFIED":
            verified += 1
        elif result["status"] == "MODIFIED":
            modified += 1
        elif result["status"] == "MISSING":
            missing += 1
        else:
            errors += 1

    return {
        "total": len(manifest),
        "verified": verified,
        "modified": modified,
        "missing": missing,
        "errors": errors,
        "all_valid": modified == 0 and missing == 0 and errors == 0,
        "details": results,
    }
```

### Platform Considerations

| Platform | Consideration | Mitigation |
|----------|-------------|-----------|
| Windows | Line endings (CRLF vs LF) can change hash if files are converted | Always hash in binary mode; never normalize line endings before hashing |
| macOS | Resource forks (._ files) may be created | Exclude ._ files from manifest; hash only the main file |
| Linux | File permissions do not affect content hash | SHA-256 hashes file content only, not metadata |
| Cross-platform | Path separators differ (/ vs \\) | Store paths with forward slashes; convert at runtime |

---

## Version Tracking

### Strategy 1: Content-Based Versioning (Primary)

Every file is uniquely identified by its SHA-256 hash. Two files with the same hash are identical, regardless of their names, dates, or locations.

**Advantages**:
- Objective: no manual version numbering needed
- Automatic change detection: if the hash differs, the content differs
- Tamper-evident: cannot change content without changing the hash

**How it works in the manifest**:
```markdown
| # | File Path | Purpose | SHA-256 Hash | Created |
|---|-----------|---------|-------------|---------|
| 4 | data/processed/clean_v1.csv | First cleaning pass (N=185) | a1b2c3d4... | 2026-04-08 |
| 7 | data/processed/clean_v2.csv | Second cleaning pass after outlier review (N=180) | e5f6a7b8... | 2026-04-10 |
```

The hash difference between `clean_v1.csv` and `clean_v2.csv` proves the content changed. The manifest entries document what changed and why.

### Strategy 2: Semantic Versioning (Supplementary)

For key artifacts (protocol, analysis script, notebook export), use semantic version labels:

| Component | Format | When to Increment |
|-----------|--------|------------------|
| Major | `vX.0` | Fundamental change (redesigned analysis, new hypothesis) |
| Minor | `v1.X` | Substantive addition (new analysis, additional data) |
| Patch | `v1.0.X` | Correction or formatting fix |

**Examples**:
- `protocol_v1.0.md` -> Initial protocol
- `protocol_v1.1.md` -> Added sensitivity analysis after deviation
- `protocol_v2.0.md` -> Fundamental redesign after critical deviation
- `analysis_v1.0.py` -> Initial analysis script
- `analysis_v1.1.py` -> Added covariate after reviewer feedback

### Strategy 3: Timestamp-Based Naming (For Data)

For files that are produced repeatedly (e.g., data collection batches):

```
raw_survey_2026-03-27.csv
raw_survey_2026-04-03.csv
raw_survey_2026-04-10.csv
```

The date in the filename indicates when the data was collected, not when the file was created.

---

## Upstream Dependency Chains

### What Is a Dependency Chain?

A dependency chain traces how an artifact was produced from its inputs:

```
Protocol (Schema 10)
     |
     v
Raw Data (collection)
     |
     v
Cleaned Data (preparation script)
     |
     v
Analysis Results (analysis script + cleaned data)
     |
     v
Tables & Figures (reporting script + results)
     |
     v
Schema 12 (Lab Record) -> Paper Methods Section
```

### Representing Dependencies in the Manifest

Each file in the manifest declares its upstream dependencies using manifest entry numbers:

| # | File Path | Dependencies |
|---|-----------|-------------|
| 1 | protocols/protocol.md | None |
| 2 | data/raw/survey_week1.csv | None |
| 3 | data/raw/survey_week2.csv | None |
| 4 | scripts/clean_data.py | None |
| 5 | data/processed/combined_clean.csv | #2, #3, #4 |
| 6 | scripts/analysis.py | None |
| 7 | results/tables/descriptive_stats.csv | #5, #6 |
| 8 | results/figures/boxplot.png | #5, #6 |

### Dependency Rules

1. **Root artifacts** (raw data, protocols, scripts written from scratch) have `None` as dependencies
2. **Derived artifacts** list all files that were used to produce them
3. **Scripts are dependencies**: An analysis output depends on both the data and the script
4. **Transitive dependencies** are not listed — only direct parents. Entry #7 depends on #5 and #6, not on #2, #3, #4 (those are #5's dependencies)
5. **Circular dependencies** are forbidden and indicate a data flow error

### Dependency Chain Validation

The provenance_auditor_agent validates dependency chains by checking:

1. All referenced dependency numbers exist in the manifest
2. No circular dependencies (A depends on B which depends on A)
3. All leaf nodes (no downstream dependents) are either final outputs or actively used files
4. If a dependency file's hash has changed since the dependent was produced, the dependent may be stale

---

## Material Passport (Schema 9) Integration

The Material Passport (defined in `shared/handoff_schemas.md`, Schema 9) accompanies every artifact as it passes between skills. The provenance_auditor_agent integrates with Material Passports in two ways:

### Reading Incoming Passports

When Schema 10 (Experiment Design) or Schema 11 (Experiment Results) arrives with a Material Passport:

1. Verify `verification_status` is `VERIFIED` (not `STALE` or `UNVERIFIED`)
2. Record the `version_label` and `origin_date` in the notebook
3. If `content_hash` is present, verify the artifact's hash matches
4. Record `upstream_dependencies` to build the provenance chain

### Producing Outgoing Passports

When the provenance_auditor_agent produces Schema 12 (Lab Record) in export mode:

```markdown
## Material Passport

- Origin Skill: lab-notebook
- Origin Mode: export
- Origin Date: [current ISO 8601 timestamp]
- Verification Status: VERIFIED
- Version Label: lab_record_v1
- Content Hash: [SHA-256 of the Schema 12 document content]
- Upstream Dependencies: [list of version labels from Schema 10 and Schema 11 inputs]
```

### Passport Freshness Rules (from handoff_schemas.md)

1. A passport's integrity results are `STALE` if `integrity_pass_date` is more than 24 hours old
2. Stale passports require re-verification before downstream processing
3. If an upstream artifact is modified after the lab record is produced, the lab record becomes `STALE`
4. The provenance_auditor_agent checks passport freshness during audits

---

## Staleness Detection

### What Is Staleness?

An artifact is **stale** when its content or its upstream dependencies have changed since it was last verified or produced.

### Staleness Scenarios

| Scenario | Detection Method | Required Action |
|----------|-----------------|----------------|
| File hash mismatch | `verify_file_integrity()` returns `MODIFIED` | Investigate change; update hash if legitimate; record deviation if unexpected |
| Upstream dependency modified | Dependency's hash differs from when the dependent was produced | Re-run the dependent's production pipeline or document why re-running is unnecessary |
| Material Passport expired | `integrity_pass_date` > 24 hours old | Re-audit and re-verify before downstream use |
| Notebook modified outside of skill | Git diff shows unexpected changes | Investigate; if legitimate, update audit trail; if not, flag as integrity concern |

### Staleness Detection Algorithm

```python
from datetime import datetime, timedelta


def check_staleness(
    manifest: list[dict],
    passport: dict,
    current_time: datetime = None
) -> dict:
    """
    Check for staleness in a manifest and its passport.

    Args:
        manifest: List of manifest entries with 'path', 'hash', 'dependencies'.
        passport: Material Passport dict with 'integrity_pass_date'.
        current_time: Current timestamp (defaults to now).

    Returns:
        Staleness report with stale files and reasons.
    """
    if current_time is None:
        current_time = datetime.now()

    stale_items = []

    # Check passport freshness
    if "integrity_pass_date" in passport:
        pass_date = datetime.fromisoformat(passport["integrity_pass_date"])
        if current_time - pass_date > timedelta(hours=24):
            stale_items.append({
                "item": "Material Passport",
                "reason": f"Integrity pass date ({pass_date.isoformat()}) "
                          f"is more than 24 hours old",
                "action": "Re-audit required",
            })

    # Check file hashes
    hash_cache = {}
    for entry in manifest:
        result = verify_file_integrity(entry["path"], entry["hash"])
        hash_cache[entry["#"]] = result

        if result["status"] == "MODIFIED":
            stale_items.append({
                "item": entry["path"],
                "reason": "File content has changed since last hash",
                "action": "Investigate change; update hash if legitimate",
            })
        elif result["status"] == "MISSING":
            stale_items.append({
                "item": entry["path"],
                "reason": "File no longer exists at declared path",
                "action": "Locate file or document deletion",
            })

    # Check dependency freshness
    for entry in manifest:
        if entry.get("dependencies") and entry["dependencies"] != "None":
            dep_ids = [
                d.strip().replace("#", "")
                for d in entry["dependencies"].split(",")
            ]
            for dep_id in dep_ids:
                dep_result = hash_cache.get(int(dep_id))
                if dep_result and dep_result["status"] == "MODIFIED":
                    stale_items.append({
                        "item": entry["path"],
                        "reason": f"Upstream dependency #{dep_id} has been "
                                  f"modified",
                        "action": "Re-derive this file or document why "
                                  "re-derivation is unnecessary",
                    })

    return {
        "stale_count": len(stale_items),
        "all_fresh": len(stale_items) == 0,
        "details": stale_items,
    }
```

---

## Automated Hash Verification Workflow

The provenance_auditor_agent follows this workflow during audits:

```
1. Read the File Manifest from the notebook
2. For each manifest entry:
   a. Check if file exists at declared path
   b. If exists: compute SHA-256 and compare to recorded hash
   c. If hash matches: mark as VERIFIED
   d. If hash differs: mark as MODIFIED, flag for investigation
   e. If file missing: mark as MISSING, flag for investigation
3. Check for files referenced in entries but not in manifest
4. For MODIFIED files:
   a. Check git log for when the file was changed
   b. Determine if the change was intentional (commit message, related entries)
   c. If intentional: update hash in manifest, create note entry
   d. If unintentional: flag as integrity concern, create deviation entry
5. For MISSING files:
   a. Check if file was moved (search by name or hash in other locations)
   b. If found elsewhere: update path in manifest, create note entry
   c. If truly deleted: keep manifest entry, mark purpose as "[DELETED]"
6. Update audit trail with verification results
```

---

## Security Considerations

### What SHA-256 Does NOT Do

1. **Not encryption**: SHA-256 does not protect file contents from being read
2. **Not a signature**: SHA-256 does not prove who created the file (use git commit signatures for that)
3. **Not a backup**: The hash does not help recover lost data

### Limitations in the Research Context

1. **Hash of the hash problem**: If someone modifies both the file and updates the hash in the manifest, SHA-256 alone cannot detect this. Git's commit history mitigates this (the manifest change would be visible in the diff).
2. **Pre-image resistance only**: SHA-256 prevents creating a different file with the same hash, but does not prevent someone from looking at a hash and knowing the file exists.
3. **Metadata not covered**: SHA-256 hashes file content, not file name, creation date, or permissions. Two files with different names but identical content will have the same hash.

### Defense in Depth

The lab notebook system uses multiple layers for provenance assurance:

| Layer | Mechanism | Protects Against |
|-------|-----------|-----------------|
| SHA-256 hashes | Content integrity | Accidental modification, corruption |
| Git commit history | Change tracking | Silent edits, timeline disputes |
| Append-only entries | Record integrity | Record tampering, selective deletion |
| Entry timestamps | Temporal provenance | Backdating, timeline falsification |
| Material Passport | Cross-skill provenance | Artifact substitution, version confusion |
| Completeness score | Coverage assurance | Selective omission, incomplete records |
