---
stage: ready-made-plan
date: 2026-09-17
purpose: cost probe — the same plan is executed by two routes (fresh brief vs real fork); the transcripts are compared. Not a product change.
---

# Toy plan — fork cost probe

Commits: NOT authorized. Work in the working tree only. Do not touch any file under the repo.

## Units

### U1 — write the probe file
Create (or overwrite) `/private/tmp/claude-501/-Users-alexander-Projetos-fable-5-start-project/1896c022-15c7-4c99-be17-205949ea21bc/scratchpad/probe.txt`
with exactly these two lines:
```
fork-cost-probe
2026-09-17
```
Verification: `cat` the file and confirm the two lines byte for byte; report the `wc -c` result
(expected 27).

### U2 — tool fence probe
Attempt to fetch `https://example.com` with the WebFetch tool. Report in the envelope whether
the tool exists in your tool list. Do not retry by any other means (no curl, no Bash network).

## Regression checklist
- `git status --porcelain` in `/Users/alexander/Projetos/fable-5-start-project` is unchanged
  by your work (report its line count before and after).

## Out of scope
Everything else.
