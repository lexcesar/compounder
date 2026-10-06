# Goal: ship a changelog — one source in the plugin, rendered on the site
Created: 2026-10-03 | Original request: "a changelog would be nice to have" (owner chose: MD + site page, short entries + a detailed 2.7 page, history from 2.0.0)
Plan: `docs/plans/2026-10-03-changelog-plan.md`

## Why (value)
The landing's "Changelog ↗" links to a raw commit list. Users cannot see what changed for them
between versions, and nothing stops a version bump from shipping without one.

## Acceptance criteria
- [x] `compounder/CHANGELOG.md` has exactly one entry per version 2.0.0–2.7.0 found in this
      branch's commit subjects — verification: version-set diff script prints nothing.
- [x] `/changelog/` is rendered from that file by `.github/scripts/build-changelog.py` — verification:
      generator run is idempotent (`git diff --exit-code` after a second run) and a construct
      outside the subset fails with its line number.
- [x] The deploy refuses a version without its entry — verification: in a throwaway worktree,
      `stamp-site.sh` passes on 2.7.0 and fails on `plugin.json` 2.7.1.
- [x] `/changelog/` and `/changelog/2.7.0/` render at 1280 and 390 px with no horizontal overflow and
      no missing assets — verification: local `http.server` + screenshots + scrollWidth check.
- [x] Public text passes the session-vantage test — verification: battery over the new files,
      every hit judged by reading.

## Non-goals
- Push, merge, deploy. Release pages before 2.7.0. The 2.6.1 entry. Dark mode for the site.

## Declared assumptions
- Local commits per unit are authorized (owner chose "commit local por unidade, sem push").
- English for all public text, like the site and plugin.

## Result
Delivered locally on `feat/changelog` (no push). Evidence, all run on 2026-10-06:
- Version set: the ten `vX.Y.Z` releases in the commit subjects equal the ten `## [X.Y.Z]`
  headings of `compounder/CHANGELOG.md`, dates matching the release commits.
- Generator: `python3 .github/scripts/test_build_changelog.py` → 19 tests OK; every structural
  guard was mutated in a copy and each mutation failed the suite. The second render of the real
  changelog is byte-identical to the committed page.
- Deploy gate (`stamp-site.sh`, run in throwaway copies): green on 2.7.0; red on plugin 2.7.1
  ("add the [2.7.1] entry"); red with full output on a failing test, with or without `pipefail`;
  red without `cmark-gfm`.
- Pages: `/changelog/` and `/changelog/2.7.0/` served locally — no 4xx, no console messages, no
  horizontal overflow at 1280 and 390 px.
- Public text: the leak battery finds only masked fixture strings and pattern lists.

Deviation from the contract as written: criterion 2 said "a construct outside the subset fails";
four adversarial passes refuted every own-parser design, and the owner chose cmark-gfm (D9).
The criterion now reads: structure violations fail with a line number; Markdown is rendered the
way GitHub renders it.

Not verified: the `apt-get install cmark-gfm` step on the Ubuntu runner (needs a CI run).
