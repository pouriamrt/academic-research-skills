"""Mutation tests for check_prose_tells.py.

Each rule gets a positive case, and every suppression path gets a test that
fails if the suppression is silently dropped. The suppressions matter as much
as the patterns here: without them the scanner floods on ARS's own reference
docs (dense with definition bullets and fenced code) and gets ignored, which
is the same outcome as not shipping it.

Run as a subprocess, mirroring CI invocation via scripts/_ci_pytest_manifest.toml.
"""

from __future__ import annotations

import json
import subprocess
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from tests.test_helpers import load_module_from_path, run_script

SCANNER = Path(__file__).parent / "check_prose_tells.py"


def write_prose(root: Path, body: str, name: str = "draft.md") -> Path:
    path = root / name
    path.write_text(body, encoding="utf-8")
    return path


def scan_text(body: str, *flags: str) -> dict:
    """Run the scanner over `body` and return the parsed --json payload."""
    with TemporaryDirectory() as tmp:
        path = write_prose(Path(tmp), body)
        result = run_script(SCANNER, "--json", *flags, str(path))
        assert result.returncode == 0, result.stdout + result.stderr
        return json.loads(result.stdout)


def ids_in(payload: dict) -> set[str]:
    return {hit["id"] for hit in payload["hits"]}


class RuleDetectionTest(unittest.TestCase):
    """One positive per rule id. A dropped pattern fails here."""

    def test_em_dash_flagged_in_flowing_prose(self) -> None:
        payload = scan_text("The result was clear — the effect held.\n")
        self.assertIn("copy-em-dash", ids_in(payload))

    def test_em_dash_html_entity_flagged(self) -> None:
        payload = scan_text("The result was clear &mdash; the effect held.\n")
        self.assertIn("copy-em-dash", ids_in(payload))

    def test_antithesis_not_just_flagged(self) -> None:
        payload = scan_text("It's not just a tool, it's a paradigm shift.\n")
        self.assertIn("copy-antithesis", ids_in(payload))

    def test_antithesis_not_only_but_flagged(self) -> None:
        payload = scan_text("Not only does it scale, but it also converges.\n")
        self.assertIn("copy-antithesis", ids_in(payload))

    def test_hype_copy_flagged(self) -> None:
        payload = scan_text("This will transform your workflow.\n")
        self.assertIn("hype-copy", ids_in(payload))

    def test_hype_copy_delve_flagged(self) -> None:
        payload = scan_text("We delve into the mechanism below.\n")
        self.assertIn("hype-copy", ids_in(payload))

    def test_servile_opener_flagged(self) -> None:
        payload = scan_text("Great question! The answer is 42.\n")
        self.assertIn("copy-servile", ids_in(payload))

    def test_servile_wrapup_flagged(self) -> None:
        payload = scan_text("In conclusion, the hypothesis was supported.\n")
        self.assertIn("copy-servile", ids_in(payload))

    def test_clean_prose_yields_no_hits(self) -> None:
        payload = scan_text("The intervention reduced latency by 40 percent.\n")
        self.assertEqual(payload["count"], 0)
        self.assertEqual(payload["hits"], [])


class SuppressionTest(unittest.TestCase):
    """Every suppression path. Dropping one floods the scanner into uselessness."""

    def test_copy_ignore_marker_suppresses_line(self) -> None:
        payload = scan_text("In conclusion, we stop. copy-ignore\n")
        self.assertEqual(payload["count"], 0)

    def test_copy_ignore_suppresses_all_rules_on_that_line(self) -> None:
        body = "Great question — let's delve in, not just once, but twice. copy-ignore\n"
        self.assertEqual(scan_text(body)["count"], 0)

    def test_definition_bullet_em_dash_suppressed(self) -> None:
        payload = scan_text("- **Suite version** — the pinned release tag.\n")
        self.assertNotIn("copy-em-dash", ids_in(payload))

    def test_comment_and_heading_lines_suppressed_for_em_dash(self) -> None:
        body = "// note — inline comment\n# heading — with dash\n"
        self.assertNotIn("copy-em-dash", ids_in(scan_text(body)))

    def test_fenced_block_body_skipped_for_every_rule(self) -> None:
        """Upstream skipped only the fence delimiter; this port skips the body."""
        body = "```python\nvalue = a — b  # in conclusion, delve\n```\n"
        self.assertEqual(scan_text(body)["count"], 0)

    def test_tilde_fence_recognised(self) -> None:
        self.assertEqual(scan_text("~~~\nIn conclusion, delve.\n~~~\n")["count"], 0)

    def test_prose_after_closing_fence_still_flags(self) -> None:
        body = "```\nIn conclusion, delve.\n```\nIn summary, the effect held.\n"
        payload = scan_text(body)
        self.assertEqual([h["line"] for h in payload["hits"]], [4])

    def test_unterminated_fence_swallows_remainder(self) -> None:
        """Under-reporting is the safe direction for a linter; pin the choice."""
        body = "```\nIn conclusion, delve.\nIn summary, more prose.\n"
        self.assertEqual(scan_text(body)["count"], 0)

    def test_inline_code_span_em_dash_suppressed(self) -> None:
        payload = scan_text("Set the flag to `a — b` before running.\n")
        self.assertNotIn("copy-em-dash", ids_in(payload))

    def test_flowing_prose_in_bullet_still_flags(self) -> None:
        """The definition-bullet carve-out must not exempt every bullet."""
        payload = scan_text("- the effect was clear, so we delve deeper.\n")
        self.assertIn("hype-copy", ids_in(payload))


class ExcludeQuotesTest(unittest.TestCase):
    """--exclude-quotes honours writing_quality_check.md's quoted-source carve-out."""

    QUOTED = "> In conclusion, we delve into the transformative potential.\n"

    def test_blockquote_flagged_by_default(self) -> None:
        self.assertTrue(ids_in(scan_text(self.QUOTED)))

    def test_blockquote_skipped_with_flag(self) -> None:
        self.assertEqual(scan_text(self.QUOTED, "--exclude-quotes")["count"], 0)

    def test_flag_does_not_suppress_unquoted_lines(self) -> None:
        body = self.QUOTED + "In summary, the author overstates the claim.\n"
        payload = scan_text(body, "--exclude-quotes")
        self.assertIn("copy-servile", ids_in(payload))
        self.assertEqual(payload["count"], 1)


class CliContractTest(unittest.TestCase):
    """Exit codes, JSON shape, and stdin — what callers actually depend on."""

    def test_json_payload_shape(self) -> None:
        payload = scan_text("In conclusion, we delve.\n")
        self.assertEqual(set(payload), {"hits", "count"})
        self.assertEqual(payload["count"], len(payload["hits"]))
        for hit in payload["hits"]:
            self.assertEqual(set(hit), {"file", "line", "id", "label", "fix", "match", "text"})
            self.assertIsInstance(hit["line"], int)

    def test_line_numbers_are_one_indexed(self) -> None:
        payload = scan_text("clean first line\nIn conclusion, done.\n")
        self.assertEqual([h["line"] for h in payload["hits"]], [2])

    def test_strict_exits_one_on_hits(self) -> None:
        with TemporaryDirectory() as tmp:
            path = write_prose(Path(tmp), "In conclusion, we delve.\n")
            result = run_script(SCANNER, "--strict", str(path))
            self.assertEqual(result.returncode, 1, result.stdout + result.stderr)

    def test_strict_exits_zero_when_clean(self) -> None:
        with TemporaryDirectory() as tmp:
            path = write_prose(Path(tmp), "Latency fell by 40 percent.\n")
            result = run_script(SCANNER, "--strict", str(path))
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_non_strict_exits_zero_despite_hits(self) -> None:
        with TemporaryDirectory() as tmp:
            path = write_prose(Path(tmp), "In conclusion, we delve.\n")
            result = run_script(SCANNER, str(path))
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_unreadable_file_is_skipped_not_fatal(self) -> None:
        with TemporaryDirectory() as tmp:
            good = write_prose(Path(tmp), "In conclusion, done.\n")
            missing = str(Path(tmp) / "absent.md")
            result = run_script(SCANNER, "--json", missing, str(good))
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertEqual(json.loads(result.stdout)["count"], 1)
            self.assertIn("skip", result.stderr)


class HtmlModeTest(unittest.TestCase):
    def test_tags_stripped_before_scanning(self) -> None:
        with TemporaryDirectory() as tmp:
            path = write_prose(
                Path(tmp), "<p>In conclusion, we <b>delve</b>.</p>\n", name="page.html"
            )
            result = run_script(SCANNER, "--json", str(path))
            payload = json.loads(result.stdout)
            self.assertEqual(ids_in(payload), {"copy-servile", "hype-copy"})


class NonAsciiOutputTest(unittest.TestCase):
    """Regression: the human-readable report must survive its own findings.

    Every rendered hit echoes the source line, and the flagship rule matches an
    em dash — so on a cp1252 Windows stdout the report died with UnicodeEncodeError
    and exited 1 on a NON-strict run. The whole earlier suite missed it because
    every non-JSON fixture body was pure ASCII, so `copy-em-dash` never once
    reached the renderer.
    """

    EM_DASH = "The result was clear — the effect held.\n"
    ARROW = "In conclusion, the pipeline runs Stage 2 → Stage 3.\n"

    def _run_plain(self, body: str) -> subprocess.CompletedProcess[str]:
        with TemporaryDirectory() as tmp:
            path = write_prose(Path(tmp), body)
            # Force the failing condition rather than trusting the harness's env.
            return run_script(SCANNER, str(path), extra_env={"PYTHONIOENCODING": "cp1252"})

    def test_em_dash_hit_renders_without_crashing(self) -> None:
        result = self._run_plain(self.EM_DASH)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertNotIn("UnicodeEncodeError", result.stderr)
        self.assertIn("copy-em-dash", result.stdout)

    def test_non_cp1252_char_in_reported_line_renders(self) -> None:
        result = self._run_plain(self.ARROW)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertNotIn("UnicodeEncodeError", result.stderr)
        self.assertIn("copy-servile", result.stdout)

    def test_strict_still_exits_one_on_a_non_ascii_hit(self) -> None:
        with TemporaryDirectory() as tmp:
            path = write_prose(Path(tmp), self.EM_DASH)
            result = run_script(
                SCANNER, "--strict", str(path), extra_env={"PYTHONIOENCODING": "cp1252"}
            )
            self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
            self.assertNotIn("UnicodeEncodeError", result.stderr)


class UnterminatedFenceWarningTest(unittest.TestCase):
    """A fence that never closes hides the rest of the file — say so, don't just pass."""

    def test_warns_on_stderr_naming_the_opening_line(self) -> None:
        with TemporaryDirectory() as tmp:
            path = write_prose(Path(tmp), "intro\n```\nIn conclusion, delve.\n")
            result = run_script(SCANNER, "--json", str(path))
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertEqual(json.loads(result.stdout)["count"], 0)
            self.assertIn("unterminated code fence", result.stderr)
            self.assertIn("line 2", result.stderr)

    def test_balanced_fences_do_not_warn(self) -> None:
        with TemporaryDirectory() as tmp:
            path = write_prose(Path(tmp), "```\ncode\n```\nIn conclusion, done.\n")
            result = run_script(SCANNER, "--json", str(path))
            self.assertNotIn("unterminated", result.stderr)


class ModuleApiTest(unittest.TestCase):
    """The in-process API, used by agents that scan a draft without a subprocess."""

    def setUp(self) -> None:
        self.mod = load_module_from_path("check_prose_tells", SCANNER)

    def test_scan_returns_one_hit_per_rule_per_line(self) -> None:
        rules = self.mod.compile_rules()
        hits = self.mod.scan("In conclusion, we delve deeply.\n", rules, "x.md")
        self.assertEqual({h["id"] for h in hits}, {"copy-servile", "hype-copy"})

    def test_every_rule_compiles(self) -> None:
        rules = self.mod.compile_rules()
        self.assertEqual(len(rules), len(self.mod.RULES))
        self.assertEqual(
            [r["id"] for r in rules],
            ["copy-em-dash", "copy-antithesis", "hype-copy", "copy-servile"],
        )


if __name__ == "__main__":
    unittest.main()
