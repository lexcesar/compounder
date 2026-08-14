---
name: btw
description: Aside in the middle of work — logs, classifies, and schedules the message without derailing the current task. Also use when receiving a user message while executing another task.
argument-hint: "[message | empty to review the aside inbox]"
---

# /btw — conversation without derailing

Input: `$ARGUMENTS`

The user thinks out loud. Every aside is valuable — and the failure mode is twofold: IGNORE (the
request is lost) or DERAIL (the task is abandoned midway to attend to it). This protocol prevents
both.

## If the input is empty: inbox review
Read `BTW.md` (root). For each item under "Open": still worth it? → propose: do it now / turn into
its own `/goal` / archive under "Done" / discard (with a 1-line why). No `BTW.md` →
say the inbox is empty and explain its use in 2 lines.

## General case: an aside arrives
**Step 1 — Acknowledge in ≤2 lines.** Show you read and understood: "Noted: <½-line summary> → <destination>."
Never spend more than that before going back to work.

**Step 2 — Classify and route (one of four):**
| Class | Test | Action |
|---|---|---|
| **Parallel now** | Independent of the current task AND delegable with a short briefing AND read-only or trivial effect | Dispatch a background subagent NOW (full briefing; return format defined); log it in `BTW.md` as `[running]`; integrate the result when it arrives |
| **Right after** | Quick but conflicts with what you're editing/reasoning about now | "Open" queue in `BTW.md` with the `[this session]` marker; execute BEFORE closing the turn/task |
| **Backlog** | Needs a decision from you with context, or is a big task | `BTW.md` "Open" with a date; mention it in the current task's final report |
| **Game changer** | The message contains an order to stop/switch priority ("stop", "forget that", "before that, do X") or invalidates the current task's premise | THEN yes, interrupt: close the state in 2 lines (what's left half-done) and attend to it |

In doubt between classes: ask in ONE line ("does this jump the queue or can it wait until I finish X?")
and keep working while you wait.

**Step 3 — Return to the current task** exactly where you left off. The aside does not alter the
standing contract except for the "Game changer" class.

## BTW.md format
```markdown
# BTW — aside inbox
## Open
- [ ] 2026-07-06 — <summary> `[running|this session|backlog]` — context: <½ line>
## Done
- [x] 2026-07-06 — <summary> → <what was done / where>
```

## Standing rule (applies without invoking the skill)
A message that arrives WHILE you're executing something else = implicit aside: apply this protocol
(acknowledge in 1–2 lines at the next tool boundary, classify, proceed). The harness delivers
these messages between tool calls — you never lose them; the only thing at stake is the
discipline of not derailing. And converse: one line of narration per phase ("closed X, opening
Y") gives the user the hooks for well-placed asides — working behind closed doors breeds late
asides and rework.

## At the end of every task
Before the final report: sweep `BTW.md` "Open" → execute the `[this session]` items, report the
`[running]` ones (with the result integrated), and list the pending `backlog` items in 1 line each.
