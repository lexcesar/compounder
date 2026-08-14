---
name: example-feedback-package-manager
description: EXAMPLE of a type-feedback memory — detect the package manager from the lockfile before any command
metadata:
  type: feedback
---

Before any package install/run command, detect the manager from the
lockfile: `pnpm-lock.yaml` → pnpm; `yarn.lock` → yarn; `package-lock.json` → npm;
`bun.lockb` → bun. Never assume npm by default.

**Why:** 2026-07-06 — I ran `npm install` in a pnpm project; it generated a spurious
`package-lock.json` and version drift; the user had to clean up.
**How to apply:** first package command of the session → check the lockfile first. Applies to
scripts too (`pnpm test`, not `npm test`). Related: [[example-project-context]].
