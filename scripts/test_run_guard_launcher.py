"""Launch-layer tests for hooks/run_guard.sh (#454 Windows Python hook portability).

The existing test_ars_write_scope_guard.py drives the guard via [sys.executable, guard]
— it never exercises INTERPRETER RESOLUTION, which is the entire #454 bug class (a Windows
`python3` that is a 0-byte Microsoft Store alias stub, not real Python). These tests cover
the launcher's job: find a REAL python (skipping stubs), run the guard as a SUPERVISED
subprocess, and degrade to pass-through+exit-0 (never block, never spam) when no real python
is found OR the guard subprocess is broken.

Design: docs/design/2026-06-17-454-windows-python-hook-portability-design.md (§3.1–3.6).

Mechanism: each test builds a temp `bin/` dir, puts fake `py`/`python3`/`python` programs
in it, and runs the launcher with PATH=that bin (plus a real python for the cases that need
one). A "stub" is a program that exits non-zero / prints nothing (mimicking the 0-byte Store
alias as the marker probe sees it). The launcher must:
  - emit canonical pass-through JSON {"hookSpecificOutput":{"hookEventName":"PreToolUse"}}
    and exit 0 when no real python verifies, or when the guard subprocess misbehaves;
  - forward the guard's stdout JSON verbatim (deny via permissionDecision:"deny", or
    pass-through) when a real python runs the guard cleanly;
  - stay SILENT on stderr on the degraded paths (PreToolUse is a hot path — any per-call
    stderr is the log spam #454 is about).

NOTE (honest limitation): this is a POSIX-host simulation. The real Windows Store-alias path,
`py.exe -3` under Git Bash, Git Bash path conversion, CRLF, and the no-Git-Bash PowerShell
fallback still need a Windows repro (tracked in the spec §6).
"""

import json
import os
import shutil
import stat
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

# ars_write_scope_guard is a script (no package); scripts/test_ars_write_scope_guard.py
# inserts this same directory onto sys.path before importing it — mirrored here so this
# module's import doesn't depend on collection order.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ars_write_scope_guard as guard

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LAUNCHER = os.path.join(REPO_ROOT, "hooks", "run_guard.sh")
GUARD = os.path.join(REPO_ROOT, "scripts", "ars_write_scope_guard.py")
PASS_THROUGH = {"hookSpecificOutput": {"hookEventName": "PreToolUse"}}

# A real python to hand the launcher when a test needs the guard to actually run.
REAL_PY = sys.executable


def _write_exec(path, body):
    """Write an executable script at `path` with `body` (a /bin/sh script)."""
    with open(path, "w") as fh:
        fh.write(body)
    os.chmod(path, os.stat(path).st_mode | stat.S_IEXEC | stat.S_IXGRP | stat.S_IXOTH)


def _stub(path):
    """A non-executing stub: prints nothing, exits 1 — what the marker probe sees for a
    0-byte Microsoft Store alias when invoked non-interactively."""
    _write_exec(path, "#!/bin/sh\nexit 1\n")


def _fake_real_python(path, real=REAL_PY):
    """A fake `python3`/`python`/`py` that behaves like a real interpreter by delegating to
    an actual python. Handles the marker probe (`-c ...`) and running the guard script.

    `path` may be a specific interpreter file path (existing callers), or an existing bin
    directory — the latter gets a `python3` created inside it (the candidate the launcher
    reaches right after `py -3`, which these callers leave unresolvable on PATH)."""
    if os.path.isdir(path):
        path = os.path.join(path, "python3")
    _write_exec(path, f'#!/bin/sh\nexec "{real}" "$@"\n')


# System dirs that hold sh/cat/grep/command/mktemp/sleep/kill/timeout. bin_dir goes FIRST
# on PATH so our injected fake py/python3/python (and any stub that shadows the system one)
# win interpreter resolution, while the launcher's own shell utilities still resolve.
_SYS_PATH = "/usr/bin:/bin:/usr/sbin:/sbin"
_SH = shutil.which("sh") or "/bin/sh"
_LAUNCHER_TIMEOUT = 45  # generous so a (bounded) hanging-candidate test can't false-fail


def _run_launcher(bin_dir, payload, extra_env=None, launcher=LAUNCHER):
    """Run the launcher with PATH = bin_dir + system dirs (bin_dir first, so injected
    interpreters shadow the real ones). Returns (exit_code, stdout, stderr).

    `launcher` defaults to the repo's real launcher; pass an alternate path to run a copy from
    a temp plugin layout (the only way to exercise a broken/alternate guard now that the
    ARS_GUARD_PATH_FOR_TEST back door is gone — the guard is ALWAYS resolved from the
    launcher's own ../scripts/, P2-e)."""
    path = os.fspath(bin_dir) + os.pathsep + _SYS_PATH
    env = {
        "PATH": path,
        # Short probe bound keeps the suite fast; a hanging-candidate is killed in ~1s.
        "ARS_PROBE_BOUND": "1",
        # The launcher must resolve the guard from its OWN path, not any var (codex P1).
        # We deliberately do NOT set CLAUDE_PLUGIN_ROOT in most tests.
    }
    if extra_env:
        env.update(extra_env)
    proc = subprocess.run(
        [_SH, launcher],
        input=json.dumps(payload),
        env=env,
        capture_output=True,
        text=True,
        timeout=_LAUNCHER_TIMEOUT,
    )
    return proc.returncode, proc.stdout, proc.stderr


def _make_plugin_layout(base, guard_body):
    """Build a temp plugin layout under `base`: hooks/run_guard.sh (real launcher copy) +
    scripts/ars_write_scope_guard.py (a guard whose body is `guard_body`) + the manifest the
    real guard needs. Returns the path to the copied launcher.

    This is how a test runs an ALTERNATE/broken guard without a production back door: the
    launcher resolves the guard from its OWN ../scripts/, so we plant the guard there (P2-e)."""
    os.makedirs(os.path.join(base, "hooks"))
    os.makedirs(os.path.join(base, "scripts"))
    launcher_copy = os.path.join(base, "hooks", "run_guard.sh")
    shutil.copy(LAUNCHER, launcher_copy)
    with open(os.path.join(base, "scripts", "ars_write_scope_guard.py"), "w") as fh:
        fh.write(guard_body)
    # The real guard reads this manifest; copy it so an unmodified-guard layout also works.
    manifest = os.path.join(os.path.dirname(GUARD), "ars_phase_scope_manifest.json")
    shutil.copy(manifest, os.path.join(base, "scripts", "ars_phase_scope_manifest.json"))
    return launcher_copy


def _bucket_a_payload(workspace, file_path):
    """A Bucket A subagent Write payload (research_architect_agent is Bucket A)."""
    return {
        "tool_name": "Write",
        "cwd": workspace,
        "agent_type": "research_architect_agent",
        "tool_input": {"file_path": file_path, "content": "x"},
    }


class LauncherNoPythonTest(unittest.TestCase):
    """No real python anywhere -> pass-through + exit 0 + silent (Plan A, spec §3.2)."""

    def _assert_clean_passthrough(self, code, out, err):
        self.assertEqual(code, 0, f"must exit 0, got {code}; stderr={err!r}")
        self.assertEqual(
            json.loads(out), PASS_THROUGH, f"must emit canonical pass-through; got {out!r}"
        )
        self.assertEqual(err.strip(), "", f"must be SILENT on hot-path stderr; got {err!r}")

    def test_only_silent_stubs_on_path(self):
        # All three candidates are stubs that exit 1 and print nothing (the marker probe sees
        # exactly what a 0-byte Store alias produces). bin_dir is FIRST on PATH so these
        # shadow any real system python.
        with tempfile.TemporaryDirectory() as bin_dir:
            for name in ("py", "python3", "python"):
                _stub(os.path.join(bin_dir, name))
            code, out, err = _run_launcher(
                bin_dir, {"tool_name": "Bash", "tool_input": {"command": "ls"}}
            )
            self._assert_clean_passthrough(code, out, err)

    def test_stubs_that_print_error_to_stderr(self):
        # A different stub variant: exits 1 AND writes a Windows-style error to stderr (closer
        # to "is not recognized" / Store-stub noise). The marker check is on STDOUT, so these
        # are still rejected. Confirms the launcher keys on the stdout marker, not exit text.
        with tempfile.TemporaryDirectory() as bin_dir:
            for name in ("py", "python3", "python"):
                _write_exec(
                    os.path.join(bin_dir, name),
                    "#!/bin/sh\necho 'not a real python' 1>&2\nexit 9\n",
                )
            code, out, err = _run_launcher(
                bin_dir, {"tool_name": "Write", "tool_input": {"file_path": "/x", "content": "y"}}
            )
            self._assert_clean_passthrough(code, out, err)

    def test_marker_printed_but_nonzero_exit_rejected(self):
        """P1-a: a candidate that PRINTS the exact marker on stdout but EXITS NON-ZERO must be
        rejected (a half-broken interpreter, or a stub that echoes then fails). The probe keys
        on `exit 0 AND marker`, not the marker alone -> no real python -> pass-through."""
        with tempfile.TemporaryDirectory() as bin_dir:
            for name in ("py", "python3", "python"):
                # Print the marker to stdout (what a REAL probe would print) but exit 9.
                # Must still be rejected because the exit status is non-zero.
                _write_exec(os.path.join(bin_dir, name), "#!/bin/sh\nprintf 'ARS_PY_OK'\nexit 9\n")
            code, out, err = _run_launcher(
                bin_dir, {"tool_name": "Bash", "tool_input": {"command": "ls"}}
            )
            self._assert_clean_passthrough(code, out, err)

    def test_no_timeout_binary_present(self):
        """Launcher must still work (and not hang) when the `timeout` binary is bypassed —
        forces the process-group watchdog fallback via ARS_GUARD_FORCE_WATCHDOG."""
        with tempfile.TemporaryDirectory() as bin_dir:
            for name in ("py", "python3", "python"):
                _stub(os.path.join(bin_dir, name))
            code, out, err = _run_launcher(
                bin_dir,
                {"tool_name": "Bash", "tool_input": {"command": "ls"}},
                extra_env={"ARS_GUARD_FORCE_WATCHDOG": "1"},
            )
            self._assert_clean_passthrough(code, out, err)


class LauncherRealPythonForwardsTest(unittest.TestCase):
    """A real python is found -> launcher runs the guard and forwards its JSON decision."""

    def test_in_scope_write_passthrough_forwarded(self):
        with tempfile.TemporaryDirectory() as bin_dir, tempfile.TemporaryDirectory() as ws:
            _fake_real_python(os.path.join(bin_dir, "python3"))
            # research_architect_agent's allowed dir — an in-scope write should pass through.
            # Use the agent's actual allowed glob area; a clearly in-scope path: workspace root file
            # owned by main session is simplest, but we want the guard to RUN and say pass-through.
            payload = {
                "tool_name": "Write",
                "cwd": ws,
                "tool_input": {"file_path": os.path.join(ws, "notes.md"), "content": "x"},
            }
            code, out, err = _run_launcher(bin_dir, payload, extra_env={"CLAUDE_PROJECT_DIR": ws})
            self.assertEqual(code, 0)
            decision = json.loads(out)
            self.assertNotIn("permissionDecision", decision["hookSpecificOutput"])

    def test_out_of_scope_bucket_a_deny_forwarded(self):
        with tempfile.TemporaryDirectory() as bin_dir, tempfile.TemporaryDirectory() as ws:
            _fake_real_python(os.path.join(bin_dir, "python3"))
            # Bucket A agent writing outside its allowed globs -> guard denies via JSON.
            payload = _bucket_a_payload(ws, os.path.join(ws, "totally_out_of_scope_dir", "x.md"))
            code, out, err = _run_launcher(bin_dir, payload, extra_env={"CLAUDE_PROJECT_DIR": ws})
            self.assertEqual(code, 0, f"guard always exits 0; got {code} err={err!r}")
            decision = json.loads(out)
            self.assertEqual(
                decision["hookSpecificOutput"].get("permissionDecision"),
                "deny",
                f"out-of-scope Bucket A write must be denied via forwarded JSON; got {out!r}",
            )

    def test_bash_denied_for_bucket_a_forwarded(self):
        with tempfile.TemporaryDirectory() as bin_dir, tempfile.TemporaryDirectory() as ws:
            _fake_real_python(os.path.join(bin_dir, "python3"))
            payload = {
                "tool_name": "Bash",
                "cwd": ws,
                "agent_type": "research_architect_agent",
                "tool_input": {"command": "rm -rf /"},
            }
            code, out, err = _run_launcher(bin_dir, payload, extra_env={"CLAUDE_PROJECT_DIR": ws})
            self.assertEqual(code, 0)
            decision = json.loads(out)
            self.assertEqual(decision["hookSpecificOutput"].get("permissionDecision"), "deny")


class LauncherStubSkipOrderingTest(unittest.TestCase):
    """First candidate is a stub, a later one is real -> skip the stub, use the real one."""

    def test_py_stub_python3_real(self):
        with tempfile.TemporaryDirectory() as bin_dir, tempfile.TemporaryDirectory() as ws:
            _stub(os.path.join(bin_dir, "py"))  # py -3 fails (stub)
            _fake_real_python(os.path.join(bin_dir, "python3"))  # python3 is real
            payload = _bucket_a_payload(ws, os.path.join(ws, "out_of_scope", "x.md"))
            code, out, err = _run_launcher(bin_dir, payload, extra_env={"CLAUDE_PROJECT_DIR": ws})
            self.assertEqual(code, 0)
            decision = json.loads(out)
            self.assertEqual(
                decision["hookSpecificOutput"].get("permissionDecision"),
                "deny",
                "must skip the py stub and use the real python3",
            )


class LauncherPyDashThreeArgTest(unittest.TestCase):
    """`py -3` must be invoked as command `py` with arg `-3`, not an executable named `py -3`."""

    def test_py_invoked_with_dash_three(self):
        with tempfile.TemporaryDirectory() as bin_dir, tempfile.TemporaryDirectory() as ws:
            argv_log = os.path.join(bin_dir, "py_argv.log")
            # fake `py` that only succeeds when given -3 as the first arg; logs argv.
            _write_exec(
                os.path.join(bin_dir, "py"),
                (
                    "#!/bin/sh\n"
                    f'echo "$@" >> "{argv_log}"\n'
                    'if [ "$1" = "-3" ]; then shift; exec "' + REAL_PY + '" "$@"; fi\n'
                    "exit 1\n"
                ),
            )
            payload = _bucket_a_payload(ws, os.path.join(ws, "out_of_scope", "x.md"))
            code, out, err = _run_launcher(bin_dir, payload, extra_env={"CLAUDE_PROJECT_DIR": ws})
            self.assertEqual(code, 0)
            decision = json.loads(out)
            self.assertEqual(decision["hookSpecificOutput"].get("permissionDecision"), "deny")
            # Confirm py was actually called with -3 (not as a literal "py -3" command, which
            # would have produced no log line at all because no such command exists).
            self.assertTrue(os.path.exists(argv_log), "py was never invoked")
            with open(argv_log) as fh:
                first = fh.readline().strip()
            self.assertTrue(
                first.startswith("-3"), f"py must be called with -3 first; got {first!r}"
            )


class LauncherSelfResolveTest(unittest.TestCase):
    """Launcher resolves the guard from its OWN path; works with CLAUDE_PLUGIN_ROOT unset
    and with a plugin path containing spaces (codex P1)."""

    def test_claude_plugin_root_unset(self):
        with tempfile.TemporaryDirectory() as bin_dir, tempfile.TemporaryDirectory() as ws:
            _fake_real_python(os.path.join(bin_dir, "python3"))
            payload = _bucket_a_payload(ws, os.path.join(ws, "out_of_scope", "x.md"))
            # _run_launcher deliberately does not set CLAUDE_PLUGIN_ROOT.
            code, out, err = _run_launcher(bin_dir, payload, extra_env={"CLAUDE_PROJECT_DIR": ws})
            self.assertEqual(code, 0)
            self.assertEqual(
                json.loads(out)["hookSpecificOutput"].get("permissionDecision"), "deny"
            )

    def test_plugin_path_with_spaces(self):
        # Copy the launcher + guard into a path containing spaces, run from there.
        with (
            tempfile.TemporaryDirectory() as base,
            tempfile.TemporaryDirectory() as bin_dir,
            tempfile.TemporaryDirectory() as ws,
        ):
            spaced = os.path.join(base, "plugin dir with spaces")
            os.makedirs(os.path.join(spaced, "hooks"))
            os.makedirs(os.path.join(spaced, "scripts"))
            shutil.copy(LAUNCHER, os.path.join(spaced, "hooks", "run_guard.sh"))
            shutil.copy(GUARD, os.path.join(spaced, "scripts", "ars_write_scope_guard.py"))
            # the guard imports nothing repo-local except its manifest, which lives in scripts/
            manifest = os.path.join(os.path.dirname(GUARD), "ars_phase_scope_manifest.json")
            shutil.copy(manifest, os.path.join(spaced, "scripts", "ars_phase_scope_manifest.json"))
            _fake_real_python(os.path.join(bin_dir, "python3"))
            payload = _bucket_a_payload(ws, os.path.join(ws, "out_of_scope", "x.md"))
            env = {
                "PATH": bin_dir + os.pathsep + _SYS_PATH,
                "CLAUDE_PROJECT_DIR": ws,
                "ARS_PROBE_BOUND": "1",
            }
            proc = subprocess.run(
                [_SH, os.path.join(spaced, "hooks", "run_guard.sh")],
                input=json.dumps(payload),
                env=env,
                capture_output=True,
                text=True,
                timeout=_LAUNCHER_TIMEOUT,
            )
            self.assertEqual(proc.returncode, 0, f"stderr={proc.stderr!r}")
            self.assertEqual(
                json.loads(proc.stdout)["hookSpecificOutput"].get("permissionDecision"),
                "deny",
                "launcher must resolve guard via its own path even under spaces",
            )


class LauncherGuardBrokeTest(unittest.TestCase):
    """Found real python BUT the guard subprocess misbehaves -> pass-through + exit 0,
    do NOT block (maintainer decision §3.2.1), do NOT spam stderr.

    Mechanism (P2-e): the launcher resolves the guard from its OWN ../scripts/ — no test-only
    path override exists in production. So each test plants a broken guard in a temp plugin
    layout (real launcher copy + broken scripts/ars_write_scope_guard.py) and runs that copy."""

    def _run_with_broken_guard(self, guard_body):
        with tempfile.TemporaryDirectory() as bin_dir, tempfile.TemporaryDirectory() as base:
            _fake_real_python(os.path.join(bin_dir, "python3"))
            launcher_copy = _make_plugin_layout(base, guard_body)
            return _run_launcher(
                bin_dir,
                {"tool_name": "Bash", "tool_input": {"command": "ls"}},
                launcher=launcher_copy,
            )

    def test_guard_exits_nonzero(self):
        code, out, err = self._run_with_broken_guard("import sys\nsys.exit(3)\n")
        self.assertEqual(code, 0, f"must not propagate guard crash as block/error; err={err!r}")
        self.assertEqual(json.loads(out), PASS_THROUGH)
        self.assertEqual(err.strip(), "")

    def test_guard_prints_nothing(self):
        code, out, err = self._run_with_broken_guard("pass\n")  # exits 0, no stdout
        self.assertEqual(code, 0)
        self.assertEqual(json.loads(out), PASS_THROUGH)
        self.assertEqual(err.strip(), "")

    def test_guard_prints_invalid_json(self):
        code, out, err = self._run_with_broken_guard("print('not json at all')\n")
        self.assertEqual(code, 0)
        self.assertEqual(json.loads(out), PASS_THROUGH)
        self.assertEqual(err.strip(), "")

    def test_guard_prints_substring_not_json(self):
        """P1-c: stdout CONTAINS the literal 'hookSpecificOutput' but is NOT valid JSON. A
        substring grep would false-accept and forward garbage; the real json.load parse must
        reject it and degrade to pass-through."""
        code, out, err = self._run_with_broken_guard(
            "print('not json but mentions \"hookSpecificOutput\" in prose')\n"
        )
        self.assertEqual(code, 0, f"non-JSON substring match must NOT be forwarded; err={err!r}")
        self.assertEqual(json.loads(out), PASS_THROUGH)
        self.assertEqual(err.strip(), "")

    def test_guard_script_missing(self):
        # A plugin layout with the launcher but NO scripts/ars_write_scope_guard.py: the
        # launcher resolves a guard path that doesn't exist -> the run_bounded exec fails ->
        # broken-path degrade. Build the layout, then delete the guard the helper planted.
        with tempfile.TemporaryDirectory() as bin_dir, tempfile.TemporaryDirectory() as base:
            _fake_real_python(os.path.join(bin_dir, "python3"))
            launcher_copy = _make_plugin_layout(base, "pass\n")
            os.remove(os.path.join(base, "scripts", "ars_write_scope_guard.py"))
            code, out, err = _run_launcher(
                bin_dir,
                {"tool_name": "Bash", "tool_input": {"command": "ls"}},
                launcher=launcher_copy,
            )
            self.assertEqual(code, 0, f"missing guard -> pass-through, not block; err={err!r}")
            self.assertEqual(json.loads(out), PASS_THROUGH)


class LauncherHangingCandidateTest(unittest.TestCase):
    """A candidate interpreter that hangs must be killed within a bound, then move on —
    the hot path must never hang (spec §3.3 watchdog)."""

    def test_hanging_py_then_real_python3(self):
        with tempfile.TemporaryDirectory() as bin_dir, tempfile.TemporaryDirectory() as ws:
            # py hangs on the marker probe; python3 is real. Launcher must kill py's probe
            # and fall through to python3 within the test's 30s subprocess timeout.
            _write_exec(os.path.join(bin_dir, "py"), "#!/bin/sh\nsleep 60\n")
            _fake_real_python(os.path.join(bin_dir, "python3"))
            payload = _bucket_a_payload(ws, os.path.join(ws, "out_of_scope", "x.md"))
            code, out, err = _run_launcher(bin_dir, payload, extra_env={"CLAUDE_PROJECT_DIR": ws})
            self.assertEqual(code, 0, f"must not hang/error on a hanging candidate; err={err!r}")
            self.assertEqual(
                json.loads(out)["hookSpecificOutput"].get("permissionDecision"),
                "deny",
                "must kill the hanging py and use the real python3",
            )

    def test_hanging_py_killed_via_watchdog_path(self):
        """P2-d: same hanging-candidate scenario, but ARS_GUARD_FORCE_WATCHDOG=1 forces the
        no-`timeout` process-group watchdog instead of the `timeout` binary. Confirms the
        watchdog (setsid + kill -TERM/-KILL on the negative pid) actually reaps a hung probe
        so the launcher still falls through to the real python3 within the bound. A candidate
        that hangs AND spawns a child grandprocess exercises the process-GROUP kill."""
        with tempfile.TemporaryDirectory() as bin_dir, tempfile.TemporaryDirectory() as ws:
            # py spawns a long-sleeping grandchild then waits — a bare-pid TERM would leak the
            # child; the process-group kill must take down the whole group.
            _write_exec(os.path.join(bin_dir, "py"), "#!/bin/sh\nsleep 60 &\nwait\n")
            _fake_real_python(os.path.join(bin_dir, "python3"))
            payload = _bucket_a_payload(ws, os.path.join(ws, "out_of_scope", "x.md"))
            code, out, err = _run_launcher(
                bin_dir,
                payload,
                extra_env={"CLAUDE_PROJECT_DIR": ws, "ARS_GUARD_FORCE_WATCHDOG": "1"},
            )
            self.assertEqual(code, 0, f"watchdog must reap the hung probe; err={err!r}")
            self.assertEqual(
                json.loads(out)["hookSpecificOutput"].get("permissionDecision"),
                "deny",
                "watchdog must kill the hanging py and fall through to python3",
            )


class LauncherWatchdogRobustnessTest(unittest.TestCase):
    """Round-6 gemini track: the no-`timeout` watchdog must not fail OPEN under (a) a private-
    temp allocation failure or (b) the pid-reuse race that would false-report a timeout."""

    def test_mktemp_failure_degrades_to_passthrough_not_fail_open(self):
        """gemini P1: if `mktemp` can't hand out a private temp, the launcher must NOT fall back
        to a predictable /tmp path (symlink-attack surface whose redirect failure would read as a
        broken guard and fail OPEN). It must degrade to a clean pass-through: exit 0, canonical
        JSON, silent. We force mktemp to fail by shadowing it on PATH and force the watchdog path
        (where the temp files live) via ARS_GUARD_FORCE_WATCHDOG."""
        with tempfile.TemporaryDirectory() as bin_dir, tempfile.TemporaryDirectory() as ws:
            _fake_real_python(os.path.join(bin_dir, "python3"))
            _write_exec(
                os.path.join(bin_dir, "mktemp"), "#!/bin/sh\nexit 1\n"
            )  # mktemp always fails
            # A Bucket A out-of-scope write would normally be DENIED — proving we don't fail open,
            # the launcher must NOT emit deny here (it can't run the guard without a temp), it must
            # cleanly pass through instead of erroring or blocking.
            payload = _bucket_a_payload(ws, os.path.join(ws, "out_of_scope", "x.md"))
            code, out, err = _run_launcher(
                bin_dir,
                payload,
                extra_env={"CLAUDE_PROJECT_DIR": ws, "ARS_GUARD_FORCE_WATCHDOG": "1"},
            )
            self.assertEqual(code, 0, f"mktemp failure must not crash/block; err={err!r}")
            self.assertEqual(
                json.loads(out),
                PASS_THROUGH,
                "mktemp failure must degrade to canonical pass-through, never a "
                "predictable-temp path that fails open",
            )
            self.assertEqual(err.strip(), "", f"degraded path must be silent; got {err!r}")

    def test_fast_guard_not_falsely_timed_out_on_watchdog_path(self):
        """gemini P1 (pid-reuse race): on the forced watchdog path, a guard that answers WELL
        within the bound must have its real decision forwarded — the done-file handshake must not
        let the watchdog false-flag a timeout (which would fail open to pass-through). Run the
        deny case several times; a single false-timeout would surface as a pass-through."""
        with tempfile.TemporaryDirectory() as bin_dir, tempfile.TemporaryDirectory() as ws:
            _fake_real_python(os.path.join(bin_dir, "python3"))
            payload = _bucket_a_payload(ws, os.path.join(ws, "out_of_scope", "x.md"))
            for i in range(5):
                code, out, err = _run_launcher(
                    bin_dir,
                    payload,
                    extra_env={"CLAUDE_PROJECT_DIR": ws, "ARS_GUARD_FORCE_WATCHDOG": "1"},
                )
                self.assertEqual(code, 0, f"run {i}: err={err!r}")
                self.assertEqual(
                    json.loads(out)["hookSpecificOutput"].get("permissionDecision"),
                    "deny",
                    f"run {i}: fast guard decision must be forwarded, not lost to a "
                    f"false timeout; got {out!r}",
                )


class LauncherInfraProtectionTest(unittest.TestCase):
    """A Bucket A subagent writing to hooks/run_guard.sh itself must be denied — confirms
    the hooks/*.sh infra glob covers the new launcher end-to-end through the launcher."""

    def test_subagent_write_to_launcher_denied(self):
        with tempfile.TemporaryDirectory() as bin_dir:
            _fake_real_python(os.path.join(bin_dir, "python3"))
            # plugin_root defaults to the repo root (launcher's ../). Target the real launcher
            # path inside this repo so it resolves inside plugin_root and matches hooks/*.sh.
            payload = {
                "tool_name": "Write",
                "cwd": REPO_ROOT,
                "agent_type": "research_architect_agent",
                "tool_input": {"file_path": LAUNCHER, "content": "evil"},
            }
            code, out, err = _run_launcher(
                bin_dir, payload, extra_env={"CLAUDE_PLUGIN_ROOT": REPO_ROOT}
            )
            self.assertEqual(code, 0)
            self.assertEqual(
                json.loads(out)["hookSpecificOutput"].get("permissionDecision"),
                "deny",
                "writing the launcher itself must be infra-denied",
            )


class LauncherFastPathTest(unittest.TestCase):
    """v2 fast path: skip Python when no deny is reachable.

    The guard inspects only INSPECTED_TOOLS = STRUCTURED_WRITE_TOOLS | {"Bash"}.
    For Bash the sole deny needs Bucket A gating (agent_type). So `not a
    structured write tool AND no agent_type` => allow is the only outcome.
    """

    def _bucket_a_agent(self):
        # REPO_ROOT is a plain str (os.path.dirname(...)), not a Path, so join via the
        # Path(...) constructor rather than the `/` operator.
        manifest = json.loads(
            Path(REPO_ROOT, "scripts", "ars_phase_scope_manifest.json").read_text(encoding="utf-8")
        )
        return sorted(manifest["agents"])[0]

    def test_main_session_bash_spawns_no_python(self):
        """Proves the fast path FIRED, not merely that the answer was right."""
        with tempfile.TemporaryDirectory() as td:
            bin_dir = Path(td) / "bin"
            bin_dir.mkdir()
            counter = Path(td) / "spawns.txt"
            # Every python candidate on PATH records an invocation.
            for name in ("py", "python3", "python"):
                _write_exec(
                    bin_dir / name, f'#!/bin/sh\necho x >> "{counter.as_posix()}"\nexit 1\n'
                )
            code, out, err = _run_launcher(
                bin_dir, {"tool_name": "Bash", "tool_input": {"command": "ls -la"}}
            )
            self.assertEqual(code, 0)
            self.assertEqual(
                json.loads(out), {"hookSpecificOutput": {"hookEventName": "PreToolUse"}}
            )
            self.assertFalse(
                counter.exists(),
                "fast path did not fire — Python was spawned for a main-session Bash call",
            )

    def test_bucket_a_bash_still_denied(self):
        with tempfile.TemporaryDirectory() as td:
            bin_dir = Path(td) / "bin"
            bin_dir.mkdir()
            _fake_real_python(bin_dir)
            code, out, err = _run_launcher(
                bin_dir,
                {
                    "tool_name": "Bash",
                    "tool_input": {"command": "ls"},
                    "cwd": str(REPO_ROOT),
                    "agent_type": self._bucket_a_agent(),
                },
                extra_env={
                    "CLAUDE_PROJECT_DIR": str(REPO_ROOT),
                    "CLAUDE_PLUGIN_ROOT": str(REPO_ROOT),
                },
            )
            self.assertEqual(json.loads(out)["hookSpecificOutput"]["permissionDecision"], "deny")

    def test_schema_drift_write_without_file_path_still_denied(self):
        """The case that killed the v1 predicate: the schema-drift deny fires
        precisely BECAUSE file_path is absent, so such a payload carries neither
        `agent_type` nor `file_path`. Keying on the tool name is what closes it."""
        for tool, tool_input in (
            ("Write", {"path": "x.txt", "content": "y"}),
            ("Edit", {"old": "a", "new": "b"}),
            ("MultiEdit", {"edits": []}),
        ):
            with self.subTest(tool=tool), tempfile.TemporaryDirectory() as td:
                bin_dir = Path(td) / "bin"
                bin_dir.mkdir()
                _fake_real_python(bin_dir)
                code, out, err = _run_launcher(
                    bin_dir,
                    {"tool_name": tool, "tool_input": tool_input, "cwd": str(REPO_ROOT)},
                    extra_env={
                        "CLAUDE_PROJECT_DIR": str(REPO_ROOT),
                        "CLAUDE_PLUGIN_ROOT": str(REPO_ROOT),
                    },
                )
                self.assertEqual(
                    json.loads(out)["hookSpecificOutput"]["permissionDecision"],
                    "deny",
                    f"{tool} without file_path must still be denied",
                )

    def test_main_session_write_to_infra_still_denied(self):
        with tempfile.TemporaryDirectory() as td:
            bin_dir = Path(td) / "bin"
            bin_dir.mkdir()
            _fake_real_python(bin_dir)
            code, out, err = _run_launcher(
                bin_dir,
                {
                    "tool_name": "Write",
                    "tool_input": {"file_path": "hooks/run_guard.sh", "content": "x"},
                    "cwd": str(REPO_ROOT),
                },
                extra_env={
                    "CLAUDE_PROJECT_DIR": str(REPO_ROOT),
                    "CLAUDE_PLUGIN_ROOT": str(REPO_ROOT),
                },
            )
            self.assertEqual(json.loads(out)["hookSpecificOutput"]["permissionDecision"], "deny")


class GuardConstantsMirrorTest(unittest.TestCase):
    """Pins the two guard constants the shell fast path hand-mirrors (hooks/run_guard.sh,
    the `case $PAYLOAD in ... esac` block right after `PAYLOAD=$(cat)`). Nothing else
    cross-checks them: the guard's own comment flags NotebookEdit as a deliberate future
    candidate, and if a later change widened either constant, the shell fast path would
    keep matching only the OLD tool names — silently skipping Python (and any new deny)
    for the newly-inspected tool while the rest of the suite stayed green. This converts
    that latent fail-open into a red test instead of a comment."""

    def test_structured_write_tools_unchanged(self):
        self.assertEqual(
            guard.STRUCTURED_WRITE_TOOLS,
            {"Write", "Edit", "MultiEdit"},
            "scripts/ars_write_scope_guard.py: STRUCTURED_WRITE_TOOLS changed — update the "
            "`*'\"Write\"'* | *'\"Edit\"'* | *'\"MultiEdit\"'*` arm of the fast-path "
            "`case $PAYLOAD in` block in hooks/run_guard.sh to match, or the launcher will "
            "silently skip Python for the added/removed tool.",
        )

    def test_inspected_tools_is_structured_write_tools_plus_bash(self):
        self.assertEqual(
            guard.INSPECTED_TOOLS,
            guard.STRUCTURED_WRITE_TOOLS | {"Bash"},
            "scripts/ars_write_scope_guard.py: INSPECTED_TOOLS no longer equals "
            "STRUCTURED_WRITE_TOOLS | {'Bash'} — the fast path's safety argument in "
            "hooks/run_guard.sh (the `case $PAYLOAD in` block after `PAYLOAD=$(cat)`) "
            "depends on exactly this relationship; update both its arms to match.",
        )


class RenderShapeContractTest(unittest.TestCase):
    """The launcher validates guard output with an ANCHORED PREFIX match
    (case $GUARD_OUT in '{"hookSpecificOutput"'*). That avoids the substring
    false-accept the old is_valid_hook_json() comment warned about, but it couples to
    render_hook_output()'s exact wire shape: an indent=2, or any key emitted before
    "hookSpecificOutput", would make the launcher treat EVERY decision as broken and
    silently degrade each deny to a pass-through. Pin the contract."""

    def test_render_hook_output_wire_shape(self):
        for decision in ({"decision": "allow", "reason": ""}, {"decision": "deny", "reason": "x"}):
            out = guard.render_hook_output(decision)
            self.assertTrue(
                out.startswith('{"hookSpecificOutput"'),
                "render_hook_output() no longer starts with the hookSpecificOutput key — "
                "the prefix match in hooks/run_guard.sh would reject every decision and "
                "degrade denies to pass-throughs. Update both together.",
            )
            self.assertNotIn(chr(10), out, "must stay single-line for the prefix match")


if __name__ == "__main__":
    unittest.main()
