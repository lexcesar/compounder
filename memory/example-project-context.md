---
name: example-project-context
description: EXAMPLE of a type-project memory — architecture decision with date, owner, and reason (what the code doesn't tell)
metadata:
  type: project
---

Living decision (EXAMPLE): on 2026-06-20 the user decided to postpone the monorepo migration until
release 2.0 ships (expected 2026-08). Until then: no structural folder changes,
even if they "improve" the layout — structural PRs will be rejected.

**Why:** a mid-release migration already broke the deploy once (user's account).
**How to apply:** reorganization proposals → record in `docs/decisions/` as a proposed ADR
and wait for 2.0. Related: [[example-feedback-package-manager]].
