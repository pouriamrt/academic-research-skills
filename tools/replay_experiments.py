#!/usr/bin/env python3
"""
Replay Experiments — Computational Reproducibility Verification Tool

Re-executes reproducibility scripts produced by data-analyst and simulation-runner,
compares outputs to stored results, and flags divergence. Supports the gold standard
of computational reproducibility.

Discovers scripts in ./experiment_outputs/scripts/, re-executes each in an isolated
subprocess (optionally using the experiment venv), compares outputs against previously
stored artifacts, and generates a reproducibility report.

Usage:
    python tools/replay_experiments.py                     # run all scripts
    python tools/replay_experiments.py --script analysis.py  # run specific script
    python tools/replay_experiments.py --tolerance 1e-3    # custom numeric tolerance
    python tools/replay_experiments.py --timeout 300       # custom timeout (seconds)
    python tools/replay_experiments.py --dry-run           # show what would run
    python tools/replay_experiments.py --report-only       # regenerate from cache

Author: academic-research-skills pipeline tooling
License: CC-BY-NC 4.0
"""

from __future__ import annotations

import argparse
import csv
import difflib
import json
import math
import os
import platform
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

DEFAULT_TIMEOUT_SECONDS = 600  # 10 minutes
DEFAULT_RTOL = 1e-5
DEFAULT_ATOL = 1e-8
FIGURE_SIZE_TOLERANCE_PERCENT = 10.0

SCRIPTS_DIR = Path("experiment_outputs/scripts")
REPORTS_DIR = Path("experiment_outputs/reports")
CACHE_PATH = Path("experiment_outputs/reports/.replay_cache.json")
EXPERIMENT_ENV_DIR = Path("experiment_env")

# File categories by extension
NUMERIC_EXTENSIONS = {".csv"}
FIGURE_EXTENSIONS = {".png", ".pdf"}
TEXT_EXTENSIONS = {".md", ".txt"}

# Regex for APA-formatted statistics embedded in text outputs
APA_STAT_PATTERNS = {
    "t_test": re.compile(
        r"t\((\d+(?:\.\d+)?)\)\s*=\s*(-?\d+\.\d+),\s*p\s*=\s*([.<]?\s*\.?\d+)"
    ),
    "f_test": re.compile(
        r"F\((\d+),\s*(\d+)\)\s*=\s*(-?\d+\.\d+),\s*p\s*=\s*([.<]?\s*\.?\d+)"
    ),
    "chi_square": re.compile(
        r"chi-sq\((\d+)\)\s*=\s*(-?\d+\.\d+),\s*p\s*=\s*([.<]?\s*\.?\d+)"
    ),
    "correlation": re.compile(
        r"r\((\d+)\)\s*=\s*(-?\.?\d+),\s*p\s*=\s*([.<]?\s*\.?\d+)"
    ),
    "effect_size_d": re.compile(r"d\s*=\s*(-?\d+\.\d+)"),
    "effect_size_eta": re.compile(r"eta-sq\s*=\s*(\.?\d+)"),
    "p_value": re.compile(r"p\s*=\s*(\.?\d+)"),
    "ci": re.compile(r"95%\s*CI\s*\[(-?\d+\.?\d*),\s*(-?\d+\.?\d*)\]"),
}


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------


@dataclass
class ScriptMetadata:
    """Metadata parsed from a reproducibility script header."""

    script_path: Path
    script_name: str
    execution_date: str | None = None
    python_version: str | None = None
    seed: str | None = None
    data_path: str | None = None
    packages: dict[str, str] = field(default_factory=dict)


@dataclass
class FileDivergence:
    """Records a single divergence between expected and actual output."""

    file_path: str
    divergence_type: str  # "numeric", "figure_size", "text_diff", "apa_stat", "missing"
    details: str
    expected: str | None = None
    actual: str | None = None


@dataclass
class ScriptResult:
    """Result of replaying a single script."""

    script_name: str
    status: str  # "REPRODUCED", "DIVERGED", "FAILED", "SKIPPED"
    execution_time_seconds: float = 0.0
    exit_code: int | None = None
    stdout: str = ""
    stderr: str = ""
    error_message: str = ""
    divergences: list[FileDivergence] = field(default_factory=list)
    metadata: ScriptMetadata | None = None


# ---------------------------------------------------------------------------
# Metadata parsing
# ---------------------------------------------------------------------------


def parse_script_metadata(script_path: Path) -> ScriptMetadata:
    """Parse header comments from a reproducibility script for metadata.

    Recognises the header format produced by data-analyst and simulation-runner:
        - Triple-quoted docstrings at the top of the file
        - Lines like ``Date: 2026-03-16 14:30``
        - Lines like ``Seed: 42``
        - Lines like ``Data: path/to/data.csv``
        - Lines like ``Python: 3.12.3``
        - Lines like ``Key packages: numpy 1.26.4, scipy 1.13.0``
        - Comment lines (``#``) with similar key: value pairs
    """

    meta = ScriptMetadata(
        script_path=script_path,
        script_name=script_path.name,
    )

    try:
        content = script_path.read_text(encoding="utf-8")
    except OSError:
        return meta

    # Gather header lines from the docstring and leading comments
    header_lines: list[str] = []
    in_docstring = False
    for line in content.splitlines()[:60]:  # only scan the first 60 lines
        stripped = line.strip()
        if stripped.startswith('"""') or stripped.startswith("'''"):
            if in_docstring:
                # Closing delimiter — capture this line too, then stop
                header_lines.append(stripped)
                break
            in_docstring = True
            # If the opening and closing delimiters are on the same line
            if stripped.count('"""') >= 2 or stripped.count("'''") >= 2:
                header_lines.append(stripped)
                break
            header_lines.append(stripped)
            continue
        if in_docstring:
            header_lines.append(stripped)
            continue
        if stripped.startswith("#"):
            header_lines.append(stripped.lstrip("#").strip())
            continue
        if not stripped:
            continue
        # Skip import statements (e.g., from __future__ import annotations)
        if stripped.startswith(("import ", "from ")):
            continue
        # If we hit non-comment, non-docstring, non-import code, stop scanning
        if not in_docstring:
            break

    combined = "\n".join(header_lines)

    # Date
    date_match = re.search(
        r"(?:Date|Execution Date|Generated|Created)\s*:\s*(.+)", combined, re.IGNORECASE
    )
    if date_match:
        meta.execution_date = date_match.group(1).strip()

    # Python version
    py_match = re.search(
        r"Python(?:\s+Version)?\s*:\s*(\d[\d.]+)", combined, re.IGNORECASE
    )
    if py_match:
        meta.python_version = py_match.group(1).strip()

    # Seed
    seed_match = re.search(r"Seed\s*:\s*(\S+)", combined, re.IGNORECASE)
    if seed_match:
        meta.seed = seed_match.group(1).strip()

    # Data path
    data_match = re.search(r"Data\s*:\s*(.+)", combined, re.IGNORECASE)
    if data_match:
        meta.data_path = data_match.group(1).strip()

    # Packages — line like "Key packages: numpy 1.26.4, scipy 1.13.0"
    pkg_match = re.search(
        r"(?:Key\s+)?[Pp]ackages?\s*:\s*(.+)", combined, re.IGNORECASE
    )
    if pkg_match:
        raw_pkgs = pkg_match.group(1).strip()
        for token in re.split(r"[,;]\s*", raw_pkgs):
            parts = token.strip().split()
            if len(parts) >= 2:
                meta.packages[parts[0]] = parts[1]
            elif len(parts) == 1:
                meta.packages[parts[0]] = "unknown"

    return meta


# ---------------------------------------------------------------------------
# Script discovery
# ---------------------------------------------------------------------------


def discover_scripts(
    scripts_dir: Path,
    filter_name: str | None = None,
) -> list[ScriptMetadata]:
    """Discover reproducibility scripts in the scripts directory."""

    if not scripts_dir.is_dir():
        return []

    scripts: list[ScriptMetadata] = []
    for py_file in sorted(scripts_dir.glob("*.py")):
        if filter_name and py_file.name != filter_name:
            continue
        meta = parse_script_metadata(py_file)
        scripts.append(meta)

    return scripts


# ---------------------------------------------------------------------------
# Execution
# ---------------------------------------------------------------------------


def _find_python_executable(experiment_env: Path) -> str:
    """Return the Python executable path, preferring the experiment venv."""

    if experiment_env.is_dir():
        # Windows: Scripts/python.exe  |  Unix: bin/python
        candidates = [
            experiment_env / "Scripts" / "python.exe",
            experiment_env / "Scripts" / "python",
            experiment_env / "bin" / "python",
            experiment_env / "bin" / "python3",
        ]
        for candidate in candidates:
            if candidate.is_file():
                return str(candidate)

    return sys.executable


def _collect_output_snapshot(outputs_dir: Path) -> dict[str, float]:
    """Snapshot file modification times + sizes under experiment_outputs (excluding scripts/ and reports/)."""

    snapshot: dict[str, float] = {}
    if not outputs_dir.is_dir():
        return snapshot

    skip_dirs = {"scripts", "reports"}
    for item in outputs_dir.rglob("*"):
        if item.is_file():
            # Skip files in scripts/ and reports/ subdirectories
            relative = item.relative_to(outputs_dir)
            if relative.parts and relative.parts[0] in skip_dirs:
                continue
            snapshot[str(relative)] = item.stat().st_mtime
    return snapshot


def execute_script(
    meta: ScriptMetadata,
    timeout_seconds: int,
    experiment_env: Path,
    project_root: Path,
) -> ScriptResult:
    """Execute a reproducibility script in an isolated subprocess."""

    python_exe = _find_python_executable(experiment_env)
    script_path = meta.script_path.resolve()

    result = ScriptResult(
        script_name=meta.script_name,
        status="FAILED",
        metadata=meta,
    )

    start_time = datetime.now(timezone.utc)
    try:
        proc = subprocess.run(
            [python_exe, str(script_path)],
            capture_output=True,
            text=True,
            timeout=timeout_seconds,
            cwd=str(project_root),
            env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
        )
        elapsed = (datetime.now(timezone.utc) - start_time).total_seconds()
        result.exit_code = proc.returncode
        result.stdout = proc.stdout
        result.stderr = proc.stderr
        result.execution_time_seconds = round(elapsed, 2)

        if proc.returncode != 0:
            result.status = "FAILED"
            result.error_message = _truncate(proc.stderr, max_lines=30)
        else:
            result.status = "REPRODUCED"  # provisional; comparison may downgrade

    except subprocess.TimeoutExpired:
        elapsed = (datetime.now(timezone.utc) - start_time).total_seconds()
        result.execution_time_seconds = round(elapsed, 2)
        result.status = "FAILED"
        result.error_message = (
            f"Script timed out after {timeout_seconds} seconds (EXECUTION_TIMEOUT)."
        )
    except OSError as exc:
        result.status = "FAILED"
        result.error_message = f"OS error executing script: {exc}"

    return result


# ---------------------------------------------------------------------------
# Output comparison
# ---------------------------------------------------------------------------


def compare_csv_files(
    original: Path,
    replay: Path,
    rtol: float,
    atol: float,
) -> list[FileDivergence]:
    """Compare two CSV files with numeric tolerance."""

    divergences: list[FileDivergence] = []
    rel_path = str(original)

    if not replay.is_file():
        divergences.append(
            FileDivergence(
                file_path=rel_path,
                divergence_type="missing",
                details=f"Replay did not produce expected file: {original.name}",
            )
        )
        return divergences

    try:
        orig_rows = _read_csv(original)
        replay_rows = _read_csv(replay)
    except Exception as exc:
        divergences.append(
            FileDivergence(
                file_path=rel_path,
                divergence_type="numeric",
                details=f"Error reading CSV: {exc}",
            )
        )
        return divergences

    # Compare row counts
    if len(orig_rows) != len(replay_rows):
        divergences.append(
            FileDivergence(
                file_path=rel_path,
                divergence_type="numeric",
                details=(
                    f"Row count mismatch: expected {len(orig_rows)}, "
                    f"got {len(replay_rows)}"
                ),
                expected=str(len(orig_rows)),
                actual=str(len(replay_rows)),
            )
        )
        return divergences

    # Compare cell-by-cell
    for row_idx, (orig_row, replay_row) in enumerate(zip(orig_rows, replay_rows)):
        if len(orig_row) != len(replay_row):
            divergences.append(
                FileDivergence(
                    file_path=rel_path,
                    divergence_type="numeric",
                    details=(
                        f"Column count mismatch at row {row_idx}: "
                        f"expected {len(orig_row)}, got {len(replay_row)}"
                    ),
                )
            )
            continue

        for col_idx, (orig_val, replay_val) in enumerate(zip(orig_row, replay_row)):
            if orig_val == replay_val:
                continue

            # Try numeric comparison
            orig_num = _try_float(orig_val)
            replay_num = _try_float(replay_val)

            if orig_num is not None and replay_num is not None:
                if not _is_close(orig_num, replay_num, rtol, atol):
                    divergences.append(
                        FileDivergence(
                            file_path=rel_path,
                            divergence_type="numeric",
                            details=(
                                f"Row {row_idx}, Col {col_idx}: "
                                f"values differ beyond tolerance "
                                f"(rtol={rtol}, atol={atol})"
                            ),
                            expected=orig_val,
                            actual=replay_val,
                        )
                    )
            else:
                # String comparison
                if orig_val.strip() != replay_val.strip():
                    divergences.append(
                        FileDivergence(
                            file_path=rel_path,
                            divergence_type="numeric",
                            details=f"Row {row_idx}, Col {col_idx}: text values differ",
                            expected=orig_val,
                            actual=replay_val,
                        )
                    )

    return divergences


def compare_figure_files(original: Path, replay: Path) -> list[FileDivergence]:
    """Compare figure files by size (exact pixel comparison is fragile)."""

    divergences: list[FileDivergence] = []
    rel_path = str(original)

    if not replay.is_file():
        divergences.append(
            FileDivergence(
                file_path=rel_path,
                divergence_type="missing",
                details=f"Replay did not produce expected figure: {original.name}",
            )
        )
        return divergences

    orig_size = original.stat().st_size
    replay_size = replay.stat().st_size

    if orig_size == 0:
        if replay_size != 0:
            divergences.append(
                FileDivergence(
                    file_path=rel_path,
                    divergence_type="figure_size",
                    details="Original file is empty but replay produced non-empty file",
                    expected="0 bytes",
                    actual=f"{replay_size} bytes",
                )
            )
        return divergences

    pct_diff = abs(replay_size - orig_size) / orig_size * 100.0
    if pct_diff > FIGURE_SIZE_TOLERANCE_PERCENT:
        divergences.append(
            FileDivergence(
                file_path=rel_path,
                divergence_type="figure_size",
                details=(
                    f"File size differs by {pct_diff:.1f}% "
                    f"(threshold: {FIGURE_SIZE_TOLERANCE_PERCENT}%)"
                ),
                expected=f"{orig_size} bytes",
                actual=f"{replay_size} bytes",
            )
        )

    return divergences


def compare_text_files(original: Path, replay: Path) -> list[FileDivergence]:
    """Compare text files with exact diff."""

    divergences: list[FileDivergence] = []
    rel_path = str(original)

    if not replay.is_file():
        divergences.append(
            FileDivergence(
                file_path=rel_path,
                divergence_type="missing",
                details=f"Replay did not produce expected text file: {original.name}",
            )
        )
        return divergences

    try:
        orig_lines = original.read_text(encoding="utf-8").splitlines(keepends=True)
        replay_lines = replay.read_text(encoding="utf-8").splitlines(keepends=True)
    except OSError as exc:
        divergences.append(
            FileDivergence(
                file_path=rel_path,
                divergence_type="text_diff",
                details=f"Error reading file: {exc}",
            )
        )
        return divergences

    diff = list(
        difflib.unified_diff(
            orig_lines,
            replay_lines,
            fromfile=f"original/{original.name}",
            tofile=f"replay/{original.name}",
            n=3,
        )
    )

    if diff:
        diff_text = "".join(diff[:80])  # truncate large diffs
        if len(diff) > 80:
            diff_text += f"\n... ({len(diff) - 80} more diff lines truncated)"
        divergences.append(
            FileDivergence(
                file_path=rel_path,
                divergence_type="text_diff",
                details=f"Text content differs:\n{diff_text}",
            )
        )

    return divergences


def compare_apa_statistics(
    original_text: str,
    replay_text: str,
    source_file: str,
    rtol: float,
    atol: float,
) -> list[FileDivergence]:
    """Parse APA-formatted statistics from text and compare within tolerance."""

    divergences: list[FileDivergence] = []

    for stat_name, pattern in APA_STAT_PATTERNS.items():
        orig_matches = pattern.findall(original_text)
        replay_matches = pattern.findall(replay_text)

        if len(orig_matches) != len(replay_matches):
            divergences.append(
                FileDivergence(
                    file_path=source_file,
                    divergence_type="apa_stat",
                    details=(
                        f"APA stat '{stat_name}': found {len(orig_matches)} "
                        f"in original, {len(replay_matches)} in replay"
                    ),
                    expected=str(len(orig_matches)),
                    actual=str(len(replay_matches)),
                )
            )
            continue

        for idx, (orig_groups, replay_groups) in enumerate(
            zip(orig_matches, replay_matches)
        ):
            # Normalize groups to tuples
            if isinstance(orig_groups, str):
                orig_groups = (orig_groups,)
            if isinstance(replay_groups, str):
                replay_groups = (replay_groups,)

            for g_idx, (o_val, r_val) in enumerate(zip(orig_groups, replay_groups)):
                o_num = _try_float(_normalize_p_value(o_val))
                r_num = _try_float(_normalize_p_value(r_val))

                if o_num is not None and r_num is not None:
                    if not _is_close(o_num, r_num, rtol, atol):
                        divergences.append(
                            FileDivergence(
                                file_path=source_file,
                                divergence_type="apa_stat",
                                details=(
                                    f"APA stat '{stat_name}' occurrence {idx + 1}, "
                                    f"group {g_idx}: values differ "
                                    f"(rtol={rtol}, atol={atol})"
                                ),
                                expected=o_val.strip(),
                                actual=r_val.strip(),
                            )
                        )

    return divergences


def compare_outputs(
    outputs_dir: Path,
    pre_snapshot: dict[str, float],
    rtol: float,
    atol: float,
) -> list[FileDivergence]:
    """Compare original output files against replayed versions.

    The strategy: we back up original files before replay, then after replay
    compare the fresh files to the backups. This function compares the backup
    (original) against the current file (replay output).
    """

    divergences: list[FileDivergence] = []

    backup_dir = outputs_dir / ".replay_backup"
    if not backup_dir.is_dir():
        return divergences

    skip_dirs = {"scripts", "reports", ".replay_backup"}

    for backup_file in backup_dir.rglob("*"):
        if not backup_file.is_file():
            continue

        relative = backup_file.relative_to(backup_dir)
        if relative.parts and relative.parts[0] in skip_dirs:
            continue

        current_file = outputs_dir / relative
        suffix = backup_file.suffix.lower()

        if suffix in NUMERIC_EXTENSIONS:
            divergences.extend(compare_csv_files(backup_file, current_file, rtol, atol))
        elif suffix in FIGURE_EXTENSIONS:
            divergences.extend(compare_figure_files(backup_file, current_file))
        elif suffix in TEXT_EXTENSIONS:
            divergences.extend(compare_text_files(backup_file, current_file))
            # Also check for APA statistics in text files
            if current_file.is_file():
                try:
                    orig_text = backup_file.read_text(encoding="utf-8")
                    replay_text = current_file.read_text(encoding="utf-8")
                    divergences.extend(
                        compare_apa_statistics(
                            orig_text,
                            replay_text,
                            str(relative),
                            rtol,
                            atol,
                        )
                    )
                except OSError:
                    pass

    return divergences


# ---------------------------------------------------------------------------
# Backup / restore helpers
# ---------------------------------------------------------------------------


def backup_outputs(outputs_dir: Path) -> Path:
    """Create a backup of current output files (excluding scripts/ and reports/)."""

    backup_dir = outputs_dir / ".replay_backup"
    if backup_dir.is_dir():
        shutil.rmtree(backup_dir)
    backup_dir.mkdir(parents=True, exist_ok=True)

    skip_dirs = {"scripts", "reports", ".replay_backup"}

    for item in outputs_dir.rglob("*"):
        if not item.is_file():
            continue
        relative = item.relative_to(outputs_dir)
        if relative.parts and relative.parts[0] in skip_dirs:
            continue

        dest = backup_dir / relative
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(item, dest)

    return backup_dir


def cleanup_backup(outputs_dir: Path) -> None:
    """Remove the temporary backup directory."""

    backup_dir = outputs_dir / ".replay_backup"
    if backup_dir.is_dir():
        shutil.rmtree(backup_dir, ignore_errors=True)


# ---------------------------------------------------------------------------
# Environment comparison
# ---------------------------------------------------------------------------


def get_current_environment(experiment_env: Path) -> dict[str, str]:
    """Capture current Python version and installed packages."""

    python_exe = _find_python_executable(experiment_env)
    env_info: dict[str, str] = {}

    # Python version
    try:
        proc = subprocess.run(
            [python_exe, "--version"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        version_str = proc.stdout.strip() or proc.stderr.strip()
        # "Python 3.12.3" -> "3.12.3"
        match = re.search(r"(\d[\d.]+)", version_str)
        if match:
            env_info["python_version"] = match.group(1)
    except (subprocess.TimeoutExpired, OSError):
        env_info["python_version"] = platform.python_version()

    # Installed packages via pip freeze
    try:
        proc = subprocess.run(
            [python_exe, "-m", "pip", "freeze", "--quiet"],
            capture_output=True,
            text=True,
            timeout=30,
        )
        if proc.returncode == 0:
            for line in proc.stdout.strip().splitlines():
                if "==" in line:
                    pkg, ver = line.split("==", 1)
                    env_info[pkg.strip().lower()] = ver.strip()
    except (subprocess.TimeoutExpired, OSError):
        pass

    return env_info


# ---------------------------------------------------------------------------
# Report generation
# ---------------------------------------------------------------------------


def generate_report(
    results: list[ScriptResult],
    env_current: dict[str, str],
    project_root: Path,
    rtol: float,
    atol: float,
    timeout_seconds: int,
) -> str:
    """Generate a reproducibility report in Markdown format."""

    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    n_total = len(results)
    n_reproduced = sum(1 for r in results if r.status == "REPRODUCED")
    n_diverged = sum(1 for r in results if r.status == "DIVERGED")
    n_failed = sum(1 for r in results if r.status == "FAILED")
    n_skipped = sum(1 for r in results if r.status == "SKIPPED")

    lines: list[str] = []
    lines.append("# Reproducibility Report")
    lines.append("")
    lines.append(f"**Generated**: {now}")
    lines.append(f"**Project Root**: `{project_root}`")
    lines.append(f"**Tolerance**: rtol={rtol}, atol={atol}")
    lines.append(f"**Timeout**: {timeout_seconds}s")
    lines.append("")

    # Summary
    lines.append("## Summary")
    lines.append("")
    lines.append("| Metric | Count |")
    lines.append("|--------|-------|")
    lines.append(f"| Total scripts | {n_total} |")
    lines.append(f"| REPRODUCED | {n_reproduced} |")
    lines.append(f"| DIVERGED | {n_diverged} |")
    lines.append(f"| FAILED | {n_failed} |")
    lines.append(f"| SKIPPED | {n_skipped} |")
    lines.append("")

    # Overall verdict
    if n_total == 0:
        verdict = "NO SCRIPTS FOUND"
    elif n_reproduced == n_total:
        verdict = "ALL REPRODUCED"
    elif n_failed > 0:
        verdict = "REPRODUCIBILITY CHECK INCOMPLETE (failures present)"
    else:
        verdict = "DIVERGENCES DETECTED"

    lines.append(f"**Overall Verdict**: {verdict}")
    lines.append("")

    # Environment comparison
    lines.append("## Environment")
    lines.append("")
    current_py = env_current.get("python_version", "unknown")
    lines.append(f"**Current Python**: {current_py}")
    lines.append("")

    # Check if any scripts recorded a different Python version
    env_mismatches: list[str] = []
    for r in results:
        if r.metadata and r.metadata.python_version:
            if r.metadata.python_version != current_py:
                env_mismatches.append(
                    f"- `{r.script_name}`: original Python {r.metadata.python_version}, "
                    f"current {current_py}"
                )

    if env_mismatches:
        lines.append("### Python Version Mismatches")
        lines.append("")
        lines.extend(env_mismatches)
        lines.append("")

    # Package version comparison
    pkg_mismatches: list[str] = []
    for r in results:
        if r.metadata and r.metadata.packages:
            for pkg, orig_ver in r.metadata.packages.items():
                current_ver = env_current.get(pkg.lower(), "not installed")
                if orig_ver != "unknown" and current_ver != orig_ver:
                    pkg_mismatches.append(
                        f"- `{pkg}`: original {orig_ver}, current {current_ver} "
                        f"(script: `{r.script_name}`)"
                    )

    if pkg_mismatches:
        lines.append("### Package Version Mismatches")
        lines.append("")
        lines.extend(pkg_mismatches)
        lines.append("")

    # Per-script details
    lines.append("---")
    lines.append("")
    lines.append("## Per-Script Results")
    lines.append("")

    for r in results:
        status_icon = {
            "REPRODUCED": "REPRODUCED",
            "DIVERGED": "DIVERGED",
            "FAILED": "FAILED",
            "SKIPPED": "SKIPPED",
        }.get(r.status, r.status)

        lines.append(f"### `{r.script_name}` — {status_icon}")
        lines.append("")

        if r.metadata:
            meta_items: list[str] = []
            if r.metadata.execution_date:
                meta_items.append(
                    f"Original Execution Date: {r.metadata.execution_date}"
                )
            if r.metadata.python_version:
                meta_items.append(f"Original Python: {r.metadata.python_version}")
            if r.metadata.seed:
                meta_items.append(f"Seed: {r.metadata.seed}")
            if r.metadata.data_path:
                meta_items.append(f"Data: `{r.metadata.data_path}`")
            if r.metadata.packages:
                pkg_str = ", ".join(f"{k} {v}" for k, v in r.metadata.packages.items())
                meta_items.append(f"Packages: {pkg_str}")

            if meta_items:
                for item in meta_items:
                    lines.append(f"- {item}")
                lines.append("")

        lines.append(f"- **Status**: {r.status}")
        lines.append(f"- **Execution Time**: {r.execution_time_seconds}s")
        if r.exit_code is not None:
            lines.append(f"- **Exit Code**: {r.exit_code}")
        lines.append("")

        if r.status == "FAILED" and r.error_message:
            lines.append("**Error**:")
            lines.append("")
            lines.append("```")
            lines.append(r.error_message)
            lines.append("```")
            lines.append("")

        if r.status == "DIVERGED" and r.divergences:
            lines.append("**Divergences**:")
            lines.append("")
            for div in r.divergences:
                lines.append(
                    f"- **{div.divergence_type}** in `{div.file_path}`: {div.details}"
                )
                if div.expected is not None and div.actual is not None:
                    lines.append(f"  - Expected: `{div.expected}`")
                    lines.append(f"  - Actual: `{div.actual}`")
            lines.append("")

    # Footer
    lines.append("---")
    lines.append("")
    lines.append(
        "*Report generated by `tools/replay_experiments.py` — "
        "academic-research-skills pipeline*"
    )
    lines.append("")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Cache (for --report-only)
# ---------------------------------------------------------------------------


def save_cache(results: list[ScriptResult], cache_path: Path) -> None:
    """Serialize results to JSON cache for --report-only regeneration."""

    cache_path.parent.mkdir(parents=True, exist_ok=True)

    serializable = []
    for r in results:
        entry = {
            "script_name": r.script_name,
            "status": r.status,
            "execution_time_seconds": r.execution_time_seconds,
            "exit_code": r.exit_code,
            "stdout_preview": _truncate(r.stdout, max_lines=10),
            "stderr_preview": _truncate(r.stderr, max_lines=10),
            "error_message": r.error_message,
            "divergences": [
                {
                    "file_path": d.file_path,
                    "divergence_type": d.divergence_type,
                    "details": d.details,
                    "expected": d.expected,
                    "actual": d.actual,
                }
                for d in r.divergences
            ],
        }
        if r.metadata:
            entry["metadata"] = {
                "script_path": str(r.metadata.script_path),
                "script_name": r.metadata.script_name,
                "execution_date": r.metadata.execution_date,
                "python_version": r.metadata.python_version,
                "seed": r.metadata.seed,
                "data_path": r.metadata.data_path,
                "packages": r.metadata.packages,
            }
        serializable.append(entry)

    cache_path.write_text(
        json.dumps(serializable, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )


def load_cache(cache_path: Path) -> list[ScriptResult]:
    """Deserialize results from JSON cache."""

    if not cache_path.is_file():
        return []

    try:
        data = json.loads(cache_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return []

    results: list[ScriptResult] = []
    for entry in data:
        meta = None
        if "metadata" in entry:
            m = entry["metadata"]
            meta = ScriptMetadata(
                script_path=Path(m.get("script_path", "")),
                script_name=m.get("script_name", ""),
                execution_date=m.get("execution_date"),
                python_version=m.get("python_version"),
                seed=m.get("seed"),
                data_path=m.get("data_path"),
                packages=m.get("packages", {}),
            )
        divergences = [
            FileDivergence(
                file_path=d["file_path"],
                divergence_type=d["divergence_type"],
                details=d["details"],
                expected=d.get("expected"),
                actual=d.get("actual"),
            )
            for d in entry.get("divergences", [])
        ]
        results.append(
            ScriptResult(
                script_name=entry["script_name"],
                status=entry["status"],
                execution_time_seconds=entry.get("execution_time_seconds", 0.0),
                exit_code=entry.get("exit_code"),
                stdout=entry.get("stdout_preview", ""),
                stderr=entry.get("stderr_preview", ""),
                error_message=entry.get("error_message", ""),
                divergences=divergences,
                metadata=meta,
            )
        )

    return results


# ---------------------------------------------------------------------------
# Utility helpers
# ---------------------------------------------------------------------------


def _read_csv(path: Path) -> list[list[str]]:
    """Read a CSV file and return rows as lists of strings."""

    rows: list[list[str]] = []
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        for row in reader:
            rows.append(row)
    return rows


def _try_float(value: str) -> float | None:
    """Attempt to parse a string as float, returning None on failure."""

    try:
        return float(value.strip())
    except (ValueError, AttributeError):
        return None


def _is_close(a: float, b: float, rtol: float, atol: float) -> bool:
    """Check if two floats are close within relative and absolute tolerance.

    Mirrors numpy.isclose logic: |a - b| <= atol + rtol * |b|
    Also handles NaN and infinity.
    """

    if math.isnan(a) and math.isnan(b):
        return True
    if math.isnan(a) or math.isnan(b):
        return False
    if math.isinf(a) and math.isinf(b):
        return (a > 0) == (b > 0)
    if math.isinf(a) or math.isinf(b):
        return False
    return abs(a - b) <= atol + rtol * abs(b)


def _normalize_p_value(raw: str) -> str:
    """Normalize APA p-value strings for numeric parsing.

    Handles cases like '< .001', '.034', '< .05'.
    """

    cleaned = raw.strip().lstrip("<").strip()
    # Add leading zero if needed: '.034' -> '0.034'
    if cleaned.startswith("."):
        cleaned = "0" + cleaned
    return cleaned


def _truncate(text: str, max_lines: int = 30) -> str:
    """Truncate text to a maximum number of lines."""

    lines = text.splitlines()
    if len(lines) <= max_lines:
        return text
    return "\n".join(lines[:max_lines]) + f"\n... ({len(lines) - max_lines} more lines)"


# ---------------------------------------------------------------------------
# Main orchestrator
# ---------------------------------------------------------------------------


def run_replay(
    project_root: Path,
    filter_script: str | None = None,
    rtol: float = DEFAULT_RTOL,
    atol: float = DEFAULT_ATOL,
    timeout_seconds: int = DEFAULT_TIMEOUT_SECONDS,
    dry_run: bool = False,
    report_only: bool = False,
) -> list[ScriptResult]:
    """Orchestrate the full replay-and-compare pipeline."""

    scripts_dir = project_root / SCRIPTS_DIR
    reports_dir = project_root / REPORTS_DIR
    outputs_dir = project_root / "experiment_outputs"
    experiment_env = project_root / EXPERIMENT_ENV_DIR
    cache_path = project_root / CACHE_PATH

    # --report-only: regenerate from cache
    if report_only:
        cached_results = load_cache(cache_path)
        if not cached_results:
            print("No cached results found. Run without --report-only first.")
            return []
        env_current = get_current_environment(experiment_env)
        report_text = generate_report(
            cached_results,
            env_current,
            project_root,
            rtol,
            atol,
            timeout_seconds,
        )
        reports_dir.mkdir(parents=True, exist_ok=True)
        report_path = reports_dir / "reproducibility_report.md"
        report_path.write_text(report_text, encoding="utf-8")
        print(f"Report regenerated from cache: {report_path}")
        return cached_results

    # Discover scripts
    scripts = discover_scripts(scripts_dir, filter_name=filter_script)

    if not scripts:
        if filter_script:
            print(f"Script not found: {filter_script} in {scripts_dir}")
        else:
            print(f"No reproducibility scripts found in {scripts_dir}")
        return []

    print(f"Found {len(scripts)} reproducibility script(s) in {scripts_dir}")
    for meta in scripts:
        print(f"  - {meta.script_name}", end="")
        if meta.execution_date:
            print(f"  (original: {meta.execution_date})", end="")
        print()

    # --dry-run: stop here
    if dry_run:
        print("\n[DRY RUN] No scripts were executed.")
        env_current = get_current_environment(experiment_env)
        print(f"Python executable: {_find_python_executable(experiment_env)}")
        print(f"Current Python version: {env_current.get('python_version', 'unknown')}")
        if experiment_env.is_dir():
            print(f"Experiment venv: {experiment_env} (found)")
        else:
            print(f"Experiment venv: {experiment_env} (not found, using system Python)")
        return [
            ScriptResult(script_name=m.script_name, status="SKIPPED", metadata=m)
            for m in scripts
        ]

    # Backup existing outputs before replay
    print("\nBacking up existing outputs...")
    backup_outputs(outputs_dir)

    # Execute each script and compare
    results: list[ScriptResult] = []

    try:
        for meta in scripts:
            print(f"\nReplaying: {meta.script_name} ...", end=" ", flush=True)

            # Take pre-execution snapshot
            pre_snapshot = _collect_output_snapshot(outputs_dir)

            # Execute
            result = execute_script(meta, timeout_seconds, experiment_env, project_root)

            if result.status == "REPRODUCED":
                # Compare outputs
                divergences = compare_outputs(outputs_dir, pre_snapshot, rtol, atol)

                # Compare stdout APA statistics against backup report files
                if result.stdout.strip():
                    backup_dir = outputs_dir / ".replay_backup" / "reports"
                    if backup_dir.is_dir():
                        for report_file in backup_dir.glob("*.md"):
                            original_text = report_file.read_text(encoding="utf-8")
                            apa_divergences = compare_apa_statistics(
                                original_text, result.stdout, rtol
                            )
                            divergences.extend(apa_divergences)

                if divergences:
                    result.status = "DIVERGED"
                    result.divergences = divergences

            print(result.status, end="")
            if result.execution_time_seconds > 0:
                print(f" ({result.execution_time_seconds}s)", end="")
            print()

            if result.status == "FAILED":
                # Print a brief error
                err_preview = result.error_message[:200] if result.error_message else ""
                if err_preview:
                    print(f"  Error: {err_preview}")

            if result.status == "DIVERGED":
                print(f"  {len(result.divergences)} divergence(s) found")

            results.append(result)
    finally:
        # Restore backups (clean up) — even on KeyboardInterrupt or exceptions
        cleanup_backup(outputs_dir)

    # Get environment info
    env_current = get_current_environment(experiment_env)

    # Generate report
    report_text = generate_report(
        results,
        env_current,
        project_root,
        rtol,
        atol,
        timeout_seconds,
    )
    reports_dir.mkdir(parents=True, exist_ok=True)
    report_path = reports_dir / "reproducibility_report.md"
    report_path.write_text(report_text, encoding="utf-8")
    print(f"\nReport written to: {report_path}")

    # Cache results for --report-only
    save_cache(results, cache_path)

    # Print summary
    n_total = len(results)
    n_reproduced = sum(1 for r in results if r.status == "REPRODUCED")
    n_diverged = sum(1 for r in results if r.status == "DIVERGED")
    n_failed = sum(1 for r in results if r.status == "FAILED")

    print(f"\n{'=' * 50}")
    print(f"SUMMARY: {n_reproduced}/{n_total} REPRODUCED", end="")
    if n_diverged:
        print(f", {n_diverged} DIVERGED", end="")
    if n_failed:
        print(f", {n_failed} FAILED", end="")
    print()
    print(f"{'=' * 50}")

    return results


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def build_parser() -> argparse.ArgumentParser:
    """Build the command-line argument parser."""

    parser = argparse.ArgumentParser(
        description=(
            "Re-execute reproducibility scripts and compare outputs to "
            "verify computational reproducibility."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  python tools/replay_experiments.py\n"
            "  python tools/replay_experiments.py --script analysis.py\n"
            "  python tools/replay_experiments.py --tolerance 1e-3\n"
            "  python tools/replay_experiments.py --timeout 300\n"
            "  python tools/replay_experiments.py --dry-run\n"
            "  python tools/replay_experiments.py --report-only\n"
        ),
    )

    parser.add_argument(
        "--script",
        type=str,
        default=None,
        help="Run only the specified script (filename, not path).",
    )
    parser.add_argument(
        "--tolerance",
        type=float,
        default=DEFAULT_RTOL,
        help=(
            f"Relative tolerance for numeric comparisons "
            f"(default: {DEFAULT_RTOL}). Also sets atol = tolerance * 1e-3."
        ),
    )
    parser.add_argument(
        "--atol",
        type=float,
        default=None,
        help=f"Absolute tolerance for numeric comparisons (default: {DEFAULT_ATOL}).",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=DEFAULT_TIMEOUT_SECONDS,
        help=f"Per-script timeout in seconds (default: {DEFAULT_TIMEOUT_SECONDS}).",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be re-executed without running.",
    )
    parser.add_argument(
        "--report-only",
        action="store_true",
        help="Regenerate report from last run's cached results.",
    )
    parser.add_argument(
        "--project-root",
        type=str,
        default=None,
        help="Project root directory (default: current working directory).",
    )

    return parser


def main() -> int:
    """Entry point for the replay_experiments tool."""

    parser = build_parser()
    args = parser.parse_args()

    # Resolve project root
    if args.project_root:
        project_root = Path(args.project_root).resolve()
    else:
        project_root = Path.cwd()

    # Resolve tolerances
    rtol = args.tolerance
    atol = args.atol if args.atol is not None else rtol * 1e-3

    results = run_replay(
        project_root=project_root,
        filter_script=args.script,
        rtol=rtol,
        atol=atol,
        timeout_seconds=args.timeout,
        dry_run=args.dry_run,
        report_only=args.report_only,
    )

    # Exit code: 0 if all reproduced or skipped, 1 if diverged/failed
    if any(r.status in ("DIVERGED", "FAILED") for r in results):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
