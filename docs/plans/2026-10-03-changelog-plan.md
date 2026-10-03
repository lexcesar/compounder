---
stage: ready-made-plan
date: 2026-10-03
origin: the owner asked for a changelog after reviewing the 2.7 before/after page; the landing's "Changelog ↗" link points at the raw commit list
---

# Changelog: one source in the plugin, rendered on the site

## Problem
The compounder has shipped versions 2.0.0 through 2.7.0 with no changelog. The landing footer's
"Changelog ↗" (`site/index.html:481`) links to `github.com/lexcesar/compounder/commits/main`, a
commit list that answers "what was committed", not "what changed for me". The release story
lives only in commit bodies.

## Requirements (owner decisions, chat 2026-10-03)
- **R1** — `compounder/CHANGELOG.md` is the single source and ships inside the plugin.
- **R2** — The site gets `/changelog/` in the visual language of the 2.7 release page, rendered
  from `CHANGELOG.md` at deploy; the footer link points there.
- **R3** — One entry per version, 3–6 lines, written from the user's side ("what changes for
  you"), not as a commit dump.
- **R4** — 2.7.0 also gets a public release page (the before/after page, minus anything that only
  made sense inside the authoring session).
- **R5** — History starts at 2.0.0; the 1.x era (named "composto", Portuguese) is one origin line.

## Reconnaissance (files opened while planning)
- `.github/workflows/pages.yml` — deploys `site/` on push to main when `site/**`, the plugin
  manifest, skills, agents, `stamp-site.sh` or the workflow change; runs
  `.github/scripts/stamp-site.sh` before upload.
- `.github/scripts/stamp-site.sh` — writes plugin facts into `data-stamp` elements and **fails the
  deploy** when hand-written page parts disagree with the plugin. The precedent to extend: derive
  at deploy, refuse to ship a contradiction.
- `site/index.html` — English (`lang="en"`), nav brand stamps `version`, footer at lines 476–486.
- `site/style.css` — light-only tokens (`--paper`, `--ink`, `--panel`, `--accent`,
  `--accent-bright`, `--line`, `--line-light`, …), `.nav*` and `.footer*` blocks reusable as-is.
- `site/main.js` — every feature is null-guarded (`if (rail)`, `if (tx)`, cursor checks its
  elements), so new pages can load it for cursor, magnetic buttons and reveal.
- Python 3 stdlib only: `import markdown` fails locally; no Markdown library in the repo.
- Version history (commit subjects carrying `vX.Y.Z`): 2.0.0 `123e888`, 2.1.0 `9418f93`,
  2.2.0 `df84e47`, 2.2.1 `4c088b4`, 2.3.0 `d6123f0`, 2.4.0 `f0225e9`, 2.4.1 `a12e2a3`,
  2.5.0 `7befa45`, 2.6.0 `c8432b8`, 2.7.0 `0c1b6e4` (+ the 2.7 commits before it).
- Source of the 2.7 page: the before/after page built for the owner (Portuguese, self-contained,
  light/dark). The public version is a translation and adaptation, not a copy.

## Work in flight
- This branch starts from `feat/absorb-dsh-method` (2.7.0, unmerged). Merging `feat/changelog`
  brings both; merge order: absorb first, or both together.
- `fix/dispatch-cost-review` and `feat/compounder-tuning` carry 2.6.1 (unmerged). Their entry is
  NOT written here — it would describe code this branch does not contain. Whoever merges them adds
  the `[2.6.1]` entry in the same merge (see Deferred).

## Inherited constraints (verbatim)
- `CLAUDE.md:36` — "Never write personal notes into tracked files. In a public repository `memory/` and
  `MEMORY.md` hold only the format examples; real memory lives in Claude's auto-memory
  outside the repository."
- `CLAUDE.md:39` — "Never `git push`, deploy, migration, or production operation without an explicit order in this session."

## Decisions
- **D1 — How the site gets the changelog.** Winner: a stdlib Python generator
  (`.github/scripts/build-changelog.py`) renders `CHANGELOG.md` into `site/changelog/index.html`
  between two marker comments; `stamp-site.sh` runs it at deploy, so the published page is always
  derived from the source. Lost: fetch-and-parse in the browser — an empty page without JS and a
  second parser to own. Lost: a hand-written HTML page next to the MD — two copies, guaranteed
  drift. Lost: pandoc or a Markdown package on the runner — a new dependency for ~6 constructs.
- **D2 — The Markdown subset.** The generator accepts only: `# ` title, intro paragraph,
  `## [X.Y.Z] — YYYY-MM-DD`, `### Added|Changed|Fixed|Removed`, `- ` bullets (one line each),
  inline `` `code` ``, `**bold**`, `[text](url)`. Anything else fails loudly with the line number.
  Lost: a permissive parser — silently mis-rendered input is the drift D1 exists to prevent.
- **D3 — Release gate.** `stamp-site.sh` fails the deploy when the top `## [X.Y.Z]` heading is not
  the version in `plugin.json`. A version bump without its changelog entry cannot ship. Lost:
  checking every historical version against git — the Actions checkout is shallow, so that check
  runs once in U2 instead.
- **D4 — URLs.** `site/changelog/index.html` → `/changelog/` and
  `site/changelog/2.7.0/index.html` → `/changelog/2.7.0/`. Directory indexes resolve on any static
  host without relying on extensionless-URL behavior. Lost: `changelog.html` at root — an uglier
  URL, and release pages need a folder anyway.
- **D5 — Look.** Light only, reusing `site/style.css` (nav, footer, tokens) plus one
  `site/changelog/changelog.css` for the page components ported from the 2.7 page. Lost: the 2.7
  page's own light/dark token set — the landing is light-only; a second theme on two pages would
  make the site inconsistent.
- **D6 — Language.** English, like the site and the plugin. The owner reviewed a Portuguese page;
  the public one is translated and the session-vantage test (simplicity lens item 7) runs on it.
- **D7 — Where release pages link from.** The 2.7.0 entry ends with a `[Release notes](…)` link the
  generator renders like any link. Lost: a special "release page" field in the format — a schema
  extension for one page.

## Implementation units

### U1: Generator + release gate, proven on a two-entry fixture (risk spike)
- Files: `.github/scripts/build-changelog.py` (new), `.github/scripts/stamp-site.sh`
- Change: `build-changelog.py <changelog.md> <page.html>` replaces the content between
  `<!-- changelog:start -->` and `<!-- changelog:end -->`; `--version` prints the top version.
  `stamp-site.sh` calls it and compares the top version with `plugin.json`.
- Tests (scratch fixture, 2 entries): renders headings, section labels, bullets, code, bold,
  links; HTML-escapes `<` `>` `&` in text; a stray construct (`> quote`, nested list) fails with
  its line number; missing markers fail; top version ≠ plugin version fails the stamp step.
- Verification: each failing case exits non-zero with a message (red-proof); the page without
  markers and a missing `CHANGELOG.md` both fail loud (fail-closed); a second run on its own
  output is a no-op (idempotent: `git diff --exit-code` after two runs).
- Risk: the stamp script edits `site/index.html` in place → run it only in a throwaway worktree.
- Depends on: nothing.

### U2: `compounder/CHANGELOG.md`, 2.0.0 → 2.7.0
- Files: `compounder/CHANGELOG.md` (new)
- Change: Keep-a-Changelog style within D2's subset; one entry per version from the commit bodies
  listed in Reconnaissance, 3–6 bullets each, user-facing; an origin line for the 1.x "composto"
  era; 2.7.0 links to `https://compounder.alexcesar.com/changelog/2.7.0/`.
- Tests: version set check — every `vX.Y.Z` ≥ 2.0.0 in `git log` subjects of this branch has
  exactly one heading, and no heading lacks a commit; dates match the commit dates.
- Verification: the version-set check prints an empty difference; the generator renders the file
  without error; session-vantage battery (from the absorb plan's U1) over the file is clean and
  every hit is judged by reading.
- Depends on: U1 (format accepted by the generator).

### U3: `/changelog/` page and the footer link
- Files: `site/changelog/index.html` (new), `site/changelog/changelog.css` (new),
  `site/index.html` (footer link at line 481)
- Change: page shell with the landing's nav and footer, markers for the generator, head metadata
  (title, description, canonical `https://compounder.alexcesar.com/changelog/`, og image reuse);
  each version a block with date and section labels; footer link → `changelog/`.
- Tests: page renders with the generated content; links resolve (`../style.css`, `../main.js`,
  `../favicon.svg`, release link); no console errors.
- Verification: local `python3 -m http.server` from `site/`, one screenshot each at 1280 and 390
  px wide; `document.documentElement.scrollWidth <= innerWidth` at 390.
- Depends on: U1, U2.

### U4: 2.7.0 release page
- Files: `site/changelog/2.7.0/index.html` (new)
- Change: English adaptation of the before/after page on the D5 look — change explorer, refresh
  simulator, review findings, "worth it", "after the models get better". Drop what only fit the
  session: branch name, "no push yet", merge-pending lines, links to private artifacts.
- Tests: the inline script passes `node --check`; explorer, simulator and comparison toggles work;
  fixture ids stay masked.
- Verification: session-vantage battery + a full read of the page text; screenshots at 1280 and
  390; same overflow check as U3.
- Depends on: U3 (shared CSS and shell).

### U5: Deploy wiring and README pointer
- Files: `.github/workflows/pages.yml`, `compounder/README.md`
- Change: add `compounder/CHANGELOG.md` and `.github/scripts/**` to the workflow's `paths`;
  README gains one line linking `CHANGELOG.md`.
- Verification: in a throwaway worktree, `bash .github/scripts/stamp-site.sh` succeeds and the
  rendered `site/changelog/index.html` matches the committed one; bump `plugin.json` to 2.7.1
  there → the script fails naming the version mismatch (red-proof).
- Depends on: U1–U4.

## Regression checklist
- Landing `/`: renders, stamps still apply (`stamp-site.sh` output line), footer link → `/changelog/`.
- `/changelog/` and `/changelog/2.7.0/`: served by local `http.server`, no 404 for any asset.
- `pages.yml`: valid YAML (`python3 -c "import yaml"` unavailable → check with `ruby -ryaml` or a
  careful read), path filters include the new sources.
- Plugin: `claude plugin validate compounder` passes (CHANGELOG.md inside the plugin dir).

## Pre-mortem
1. The changelog reads like a commit log → R3's user-side rule; each bullet answers "what is
   different when I use it".
2. The generator grows into a Markdown engine → D2 fixes the subset; new constructs fail loudly
   and require a decision, not a quiet parser extension.
3. The release page leaks session context or private material → D6 battery + full read; no link
   to the private artifact.
4. 2.6.1 lands later with no entry → Deferred item below; D3 only guards the top entry.

## Out of scope
- Release pages for versions before 2.7.0.
- Push, merge, deploy (CLAUDE.md:39).
- The 2.6.1 entry (its code is not on this branch).
- Dark mode for the site.

## Deferred to execution
- Exact wording of each entry (from commit bodies; U2).
- Whether `main.js` reveal markers (`data-reveal`) are worth using on the new pages or the pages
  stay static.
- At the merge of `fix/dispatch-cost-review` / `feat/compounder-tuning`: add `## [2.6.1]` between
  2.6.0 and 2.7.0 in the same merge.

## Done
- R1–R5 each traced to a unit with its verification run in the session.
- Generator red-proofs and fail-closed proofs recorded; release gate proven red on 2.7.1.
- Screenshots of `/changelog/` and `/changelog/2.7.0/` at both widths, no horizontal overflow.
- `claude plugin validate compounder` green; nothing pushed.
