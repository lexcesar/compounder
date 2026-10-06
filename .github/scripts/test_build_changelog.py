"""Tests for build-changelog.py — run: python3 .github/scripts/test_build_changelog.py

The script owns the changelog's structure; cmark-gfm owns the Markdown. Structure violations must
fail with a line number, and a missing cmark-gfm must fail loudly.
"""
import importlib.util
import os
import pathlib
import re
import subprocess
import sys
import tempfile
import unittest

HERE = pathlib.Path(__file__).resolve().parent
SCRIPT = pathlib.Path(os.environ.get("BUILD_CHANGELOG", HERE / "build-changelog.py"))
spec = importlib.util.spec_from_file_location("build_changelog", SCRIPT)
bc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bc)

HEAD = "# Changelog\n\n## [1.0.0] — 2026-01-01\n### Added\n"


def render(source):
	return "\n".join(bc.render(*bc.parse(source)))


class Structure(unittest.TestCase):
	def test_entries_and_newest_version(self):
		_, entries, origin = bc.parse("# C\n\nIntro.\n\n## [2.0.0] — 2026-01-02\n### Added\n- b\n\n## [1.0.0] — 2026-01-01\n### Fixed\n- a\n\n## Before 2.0.0\nOld.\n")
		self.assertEqual([e["ver"] for e in entries], [(2, 0, 0), (1, 0, 0)])
		self.assertEqual(origin, ["Old.", ""])

	def test_crlf(self):
		self.assertEqual(bc.parse((HEAD + "- a\n").replace("\n", "\r\n"))[1][0]["ver"], (1, 0, 0))

	REJECT = {
		"no title": "Changelog\n\n## [1.0.0] — 2026-01-01\n### Added\n- a\n",
		"no entries": "# C\n\nOnly intro.\n",
		"hyphen heading": "# C\n\n## [1.0.0] - 2026-01-01\n### Added\n- a\n",
		"trailing text on heading": "# C\n\n## [1.0.0] — 2026-01-01 extra\n### Added\n- a\n",
		"leading zero": "# C\n\n## [01.0.0] — 2026-01-01\n### Added\n- a\n",
		"non-ascii digit": "# C\n\n## [١.0.0] — 2026-01-01\n### Added\n- a\n",
		"invalid date": "# C\n\n## [1.0.0] — 2026-02-30\n### Added\n- a\n",
		"versions out of order": HEAD + "- a\n\n## [2.0.0] — 2026-01-02\n### Added\n- b\n",
		"duplicate version": HEAD + "- a\n\n## [1.0.0] — 2026-01-02\n### Added\n- b\n",
		"unknown group": "# C\n\n## [1.0.0] — 2026-01-01\n### Security\n- a\n",
		"duplicate group": HEAD + "- a\n### Added\n- b\n",
		"h4 inside entry": HEAD + "- a\n#### deep\n",
		"h1 inside entry": HEAD + "- a\n# again\n",
		"heading in intro": "# C\n\n### Added\n\n## [1.0.0] — 2026-01-01\n### Added\n- a\n",
		"heading in origin": HEAD + "- a\n\n## Before 2.0.0\n### Fixed\n- b\n",
		"entry without section": "# C\n\n## [1.0.0] — 2026-01-01\n- a\n",
		"origin not last": HEAD + "- a\n\n## Before 2.0.0\nx\n\n## [0.9.0] — 2025-01-01\n### Added\n- b\n",
		"setext h2 in body": HEAD + "- a\n\nTitle\n---\n",
		"setext h1 in body": HEAD + "- a\n\nTitle\n===\n",
		"indented h2": HEAD + "- a\n\n  ## Sneaky\n",
		"indented h1": HEAD + "- a\n\n   # Sneaky\n",
		"bare hash": HEAD + "- a\n\n#\n",
		"heading in quote": HEAD + "- a\n\n> ## quoted\n",
		"heading in list": HEAD + "- ## in list\n",
		"indented duplicate group": HEAD + "- a\n\n  ### Added\n- b\n",
		"empty group": HEAD + "### Fixed\n- a\n",
		"setext title": "Changelog\n===\n\n## [1.0.0] — 2026-01-01\n### Added\n- a\n",
		"setext title starting with hash": "#T\n===\n## [1.0.0] — 2026-01-01\n### Added\n- a\n",
		"setext version": "# C\n\n[1.0.0] — 2026-01-01\n---\n### Added\n- a\n",
		"setext origin": HEAD + "- a\n\nBefore 2.0.0\n---\nold line\n",
	}

	def test_each_violation_fails_with_a_line_number(self):
		for name, source in self.REJECT.items():
			with self.subTest(name):
				with self.assertRaisesRegex(bc.ChangelogError, r"^line \d+: "):
					bc.parse(source)

	def test_messages_name_the_rule(self):
		cases = {
			"Changelog\n\n## [1.0.0] — 2026-01-01\n### Added\n- a\n": "must start with '# <title>'",
			"## [2.0.0] — 2026-01-02\n### Added\n- a\n\n## [1.0.0] — 2026-01-01\n### Added\n- b\n": "must start with '# <title>'",
			HEAD + "- a\n\n## Before 2.0.0\nx\n\n## [0.9.0] — 2025-01-01\n### Added\n- b\n": "must be the last section",
		}
		for source, message in cases.items():
			with self.subTest(message):
				with self.assertRaisesRegex(bc.ChangelogError, re.escape(message)):
					bc.parse(source)

	def test_headings_inside_code_are_code(self):
		out = render(HEAD + "- a\n\n```\n## not a heading\n### Added\n```\n")
		self.assertIn("## not a heading\n### Added", out)

	def test_hashtag_is_not_a_heading(self):
		self.assertIn("#hashtag", render(HEAD + "- a\n\n#hashtag starts a paragraph\n"))


class Markdown(unittest.TestCase):
	def test_gfm_constructs_render_like_github(self):
		out = render(HEAD + "- **`/compound`** and _x_ and the _id field\n- [ ] task\n\nline one  \nline two\n")
		self.assertIn("<strong><code>/compound</code></strong>", out)
		self.assertIn("<em>x</em> and the _id field", out)
		self.assertIn('<input type="checkbox" disabled="" /> task', out)
		self.assertIn("line one<br />", out)

	def test_safe_mode_drops_raw_html_and_unsafe_links(self):
		out = render(HEAD + "- [a](javascript:alert(1)) <script>x</script>\n")
		self.assertIn('<a href="">a</a>', out)
		self.assertNotIn("<script>", out)

	def test_each_body_stops_before_the_next_heading(self):
		out = render("# C\n\n## [2.0.0] — 2026-01-02\n### Added\n- b\n\n## [1.0.0] — 2026-01-01\n### Added\n- a\n\n## Before 2.0.0\nOld.\n")
		self.assertEqual(out.count("<h2"), 3)
		self.assertNotIn("<h2>", out)

	def test_last_line_before_next_heading_is_kept(self):
		out = render("# C\n## [2.0.0] — 2026-01-02\n### Added\n- b\n## [1.0.0] — 2026-01-01\n### Added\n- a\n## Before 2.0.0\nOld.")
		self.assertIn("<li>b</li>", out)
		self.assertIn("<li>a</li>", out)
		self.assertIn("<p>Old.</p>", out)

	def test_group_headings_get_classes(self):
		out = render(HEAD + "- a\n### Fixed\n- b\n")
		self.assertIn('<h3 class="cl-group__k cl-group__k--added">Added</h3>', out)
		self.assertIn('<h3 class="cl-group__k cl-group__k--fixed">Fixed</h3>', out)

	def test_intro_and_origin(self):
		out = render("# C\n\nIntro **text**.\n\n## [1.0.0] — 2026-01-01\n### Added\n- a\n\n## Before 2.0.0\nThe 1.x line.\n")
		self.assertIn('<div class="cl-intro cl-prose">', out)
		self.assertIn("<strong>text</strong>", out)
		self.assertIn('id="before-2-0-0"', out)
		self.assertIn("<p>The 1.x line.</p>", out)


class Page(unittest.TestCase):
	def run_cli(self, *args, env=None):
		return subprocess.run([sys.executable, str(SCRIPT), *args], capture_output=True, text=True, env=env)

	def page_with(self, d, markdown):
		src, page = pathlib.Path(d, "c.md"), pathlib.Path(d, "p.html")
		src.write_text(markdown)
		page.write_text("<main>\n\t<!-- changelog:start -->\n\told\n\t<!-- changelog:end -->\n</main>\n")
		return src, page

	def test_idempotent_and_code_blocks_untouched(self):
		with tempfile.TemporaryDirectory() as d:
			src, page = self.page_with(d, HEAD + "- a\n\n```\nx\n  y\n```\n")
			self.assertEqual(self.run_cli(str(src), str(page)).returncode, 0)
			first = page.read_text()
			self.assertIn("<pre><code>x\n  y\n</code></pre>", first)
			self.assertEqual(self.run_cli(str(src), str(page)).returncode, 0)
			self.assertEqual(page.read_text(), first)

	def test_end_marker_keeps_its_indentation(self):
		with tempfile.TemporaryDirectory() as d:
			src, page = self.page_with(d, HEAD + "- a\n")
			self.assertEqual(self.run_cli(str(src), str(page)).returncode, 0)
			self.assertIn("</section>\n\t<!-- changelog:end -->\n</main>", page.read_text())

	def test_marker_checks(self):
		with tempfile.TemporaryDirectory() as d:
			src, page = self.page_with(d, HEAD + "- a\n")
			for broken in ("<main>no markers</main>", "<!-- changelog:end --><!-- changelog:start -->"):
				page.write_text(broken)
				res = self.run_cli(str(src), str(page))
				self.assertEqual(res.returncode, 1)
				self.assertIn("needs exactly one", res.stderr)

	def test_missing_cmark_fails_loud(self):
		with tempfile.TemporaryDirectory() as d:
			src, page = self.page_with(d, HEAD + "- a\n")
			res = self.run_cli(str(src), str(page), env={"PATH": d})
			self.assertEqual(res.returncode, 1)
			self.assertIn("cmark-gfm not found", res.stderr)

	def test_missing_source_fails(self):
		self.assertEqual(self.run_cli("/nonexistent/CHANGELOG.md", "/nonexistent/p.html").returncode, 1)

	def test_version_flag(self):
		with tempfile.TemporaryDirectory() as d:
			src, _ = self.page_with(d, HEAD + "- a\n")
			res = self.run_cli("--version", str(src))
			self.assertEqual((res.returncode, res.stdout.strip()), (0, "1.0.0"))


if __name__ == "__main__":
	unittest.main()
