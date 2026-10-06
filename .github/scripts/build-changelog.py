#!/usr/bin/env python3
"""Render compounder/CHANGELOG.md into the site's changelog page.

Usage:
  build-changelog.py CHANGELOG.md PAGE.html   replace the block between the page's markers
  build-changelog.py --version CHANGELOG.md   print the newest version

cmark-gfm, GitHub's reference GitHub-flavored Markdown implementation, does all the parsing: the
structure is read from its syntax tree and every body is rendered by it in its default safe mode
(raw HTML and unsafe links are dropped). Structure violations fail with a line number:
  # Title                      first line, not rendered — the page has its own heading
  intro                        Markdown before the first entry
  ## [X.Y.Z] — YYYY-MM-DD      one entry per version, newest first, unique, a real date
  ### Added|Changed|Fixed|Removed   the only headings inside an entry, each with content;
                               no heading may sit inside a list, quote or other block
  ## Before 2.0.0              the single origin section, last
"""
import datetime
import re
import shutil
import subprocess
import sys
import xml.etree.ElementTree as ET

START, END = "<!-- changelog:start -->", "<!-- changelog:end -->"
NUM = r"(0|[1-9][0-9]*)"
VERSION_RE = re.compile(rf"^\[{NUM}\.{NUM}\.{NUM}\] — ([0-9]{{4}}-[0-9]{{2}}-[0-9]{{2}})$")
ORIGIN = "Before 2.0.0"
GROUPS = ("Added", "Changed", "Fixed", "Removed")
EXTENSIONS = ["--extension", "table", "--extension", "strikethrough", "--extension", "autolink",
	"--extension", "tasklist"]
NS = "{http://commonmark.org/xml/1.0}"
ATX_RE = re.compile(r"^ {0,3}(#{1,6})(?:[ \t]|$)")


class ChangelogError(Exception):
	pass


def fail(n, msg):
	raise ChangelogError(f"line {n}: {msg}")


def run_cmark(markdown, *args):
	exe = shutil.which("cmark-gfm")
	if exe is None:
		raise ChangelogError("cmark-gfm not found on PATH — install it (brew install cmark-gfm / apt-get install cmark-gfm)")
	return subprocess.run([exe, *EXTENSIONS, *args], input=markdown, capture_output=True, text=True, check=True).stdout


def start_line(node):
	return int(node.get("sourcepos").split(":")[0])


def parse(source):
	"""Read the structure from cmark-gfm's own parse, so the script and the renderer cannot disagree.

	Returns intro, version entries and origin; each body is the list of source lines between
	top-level headings.
	"""
	lines = source.split("\n")
	doc = ET.fromstring(run_cmark(source, "--sourcepos", "--to", "xml"))
	blocks = list(doc)
	if not blocks or blocks[0].tag != NS + "heading" or blocks[0].get("level") != "1":
		fail(1, "the file must start with '# <title>'")

	def heading_line(node):
		# Section headings are one ATX line, so the body starts on the next line. cmark-gfm 0.29
		# reports a wrong end line for setext headings, which would silently drop body lines.
		first = start_line(node)
		atx = ATX_RE.match(lines[first - 1])
		if not atx or len(atx.group(1)) != int(node.get("level")):
			fail(first, "section headings must use the '#' form, not an underline")
		return first

	intro, entries, origin = [], [], None
	sections = [(intro, heading_line(blocks[0]) + 1)]
	group = None

	def close_group():
		if group is not None and not group["filled"]:
			fail(group["line"], f"### {group['name']} has no content")

	for node in blocks[1:]:
		if node.tag != NS + "heading":
			for nested in node.iter(NS + "heading"):
				fail(start_line(nested), "headings may not sit inside lists, quotes or other blocks")
			if group is not None:
				group["filled"] = True
			continue
		first = heading_line(node)
		level, text = node.get("level"), " ".join("".join(node.itertext()).split())
		if level == "2":
			close_group()
			group = None
			if origin is not None:
				fail(first, f"'## {ORIGIN}' must be the last section")
			if text == ORIGIN:
				origin = []
				sections.append((origin, first + 1))
				continue
			m = VERSION_RE.match(text)
			if not m:
				fail(first, f"expected '## [X.Y.Z] — YYYY-MM-DD' or '## {ORIGIN}', got {text!r}")
			ver = tuple(int(x) for x in m.group(1, 2, 3))
			try:
				datetime.date.fromisoformat(m.group(4))
			except ValueError:
				fail(first, f"invalid date {m.group(4)}")
			if entries and ver >= entries[-1]["ver"]:
				fail(first, f"{'.'.join(map(str, ver))} is not lower than the entry above it")
			entry = {"ver": ver, "date": m.group(4), "body": [], "line": first, "groups": set()}
			entries.append(entry)
			sections.append((entry["body"], first + 1))
		elif level == "3" and entries and sections[-1][0] is entries[-1]["body"]:
			close_group()
			if text not in GROUPS:
				fail(first, f"section must be one of {', '.join(GROUPS)}, got {text!r}")
			if text in entries[-1]["groups"]:
				fail(first, f"duplicate ### {text} in this entry")
			entries[-1]["groups"].add(text)
			group = {"name": text, "line": first, "filled": False}
		else:
			fail(first, "only '## [X.Y.Z] — date', '## Before 2.0.0' and, inside an entry, '### Added|Changed|Fixed|Removed' headings are allowed")
	close_group()
	if not entries:
		fail(1, "no version entries")
	for e in entries:
		if not e["groups"]:
			fail(e["line"], "a version entry needs at least one ### section")
	# A body runs up to the line before the next section's heading (which sits at its start - 1).
	stops = [start - 1 for _, start in sections[1:]] + [len(lines) + 1]
	for (body, start), stop in zip(sections, stops):
		body.extend(lines[start - 1:stop - 1])
	return intro, entries, origin


def cmark(markdown):
	html = run_cmark("\n".join(markdown), "--to", "html")
	for name in GROUPS:
		html = html.replace(f"<h3>{name}</h3>", f'<h3 class="cl-group__k cl-group__k--{name.lower()}">{name}</h3>')
	return html.rstrip("\n").split("\n")


def render(intro, entries, origin):
	out = []
	if any(line.strip() for line in intro):
		out.append('<div class="cl-intro cl-prose">')
		out.extend(cmark(intro))
		out.append("</div>")
	for e in entries:
		v = ".".join(map(str, e["ver"]))
		anchor = "v" + v.replace(".", "-")
		day = datetime.date.fromisoformat(e["date"])
		out.append(f'<section class="cl-entry" id="{anchor}">')
		out.append(f'\t<header class="cl-entry__head"><h2 class="cl-entry__v"><a href="#{anchor}">{v}</a></h2>'
			f'<time class="cl-entry__date" datetime="{e["date"]}">{day.day} {day:%b %Y}</time></header>')
		out.append('\t<div class="cl-entry__body cl-prose">')
		out.extend(cmark(e["body"]))
		out.append("\t</div>")
		out.append("</section>")
	if origin is not None:
		out.append('<section class="cl-entry cl-entry--origin" id="before-2-0-0">')
		out.append('\t<header class="cl-entry__head"><h2 class="cl-entry__v">Before 2.0.0</h2></header>')
		out.append('\t<div class="cl-entry__body cl-prose">')
		out.extend(cmark(origin))
		out.append("\t</div>")
		out.append("</section>")
	return out


def main(argv):
	if len(argv) == 3 and argv[1] == "--version":
		with open(argv[2], encoding="utf-8") as f:
			_, entries, _ = parse(f.read())
		print(".".join(map(str, entries[0]["ver"])))
		return 0
	if len(argv) != 3:
		print(__doc__, file=sys.stderr)
		return 2
	with open(argv[1], encoding="utf-8") as f:
		block = render(*parse(f.read()))
	with open(argv[2], encoding="utf-8") as f:
		page = f.read()
	if page.count(START) != 1 or page.count(END) != 1 or page.index(START) > page.index(END):
		raise ChangelogError(f"{argv[2]}: needs exactly one {START} followed by one {END}")
	head, rest = page.split(START)
	_, tail = rest.split(END)
	# cmark output goes in unindented: inside <pre> a prefix would become part of the code.
	indent = re.search(r"([ \t]*)$", head).group(1)
	body = "".join(f"{line}\n" for line in block)
	new = f"{head}{START}\n{body}{indent}{END}{tail}"
	if new != page:
		with open(argv[2], "w", encoding="utf-8") as f:
			f.write(new)
	return 0


if __name__ == "__main__":
	try:
		sys.exit(main(sys.argv))
	except (ChangelogError, OSError, subprocess.CalledProcessError) as e:
		print(f"build-changelog: {e}", file=sys.stderr)
		sys.exit(1)
