---
status: accepted
date: 2026-08-28
---

# The editor may hold no buffers

Lesson 14 gave `Editor::close` a guard that refuses to remove the last buffer, so
`buffers` was never empty and `active: usize` was always valid. Part 3 deletes that guard:
closing your last tab leaves the editor holding nothing, and `active` becomes
`Option<usize>`. Most editors keep a buffer alive rather than allow this, so the guard
looks like the safe choice and its removal looks like a regression. It isn't.

## Why

The guard bought an invariant by lying about what the user asked for. Clicking ✕ on the
only open tab did nothing, silently — and in lesson 15 that surfaced as a real bug: the
confirmation dialog's *Discard* button called `close`, which returned early, so the
question vanished and the buffer stayed. Two features behaved correctly and the guard
between them produced a dead end.

Representing "nothing is open" honestly costs one `Option` field, five conditionals in
`fn ui`, and a deleted test. In exchange the editor stops having a state it cannot
describe.

## Consequences

Start-up is a separate decision and is unaffected: bare `cargo run` opens an Untitled
Buffer (part 3), and a Project restores the Buffers it remembers, which may legitimately
be none (part 12). Empty is reachable by closing the last tab, not by launching.

The central panel is drawn from a `match` on `active` that dispatches to a method, rather
than an `if let` wrapped around forty lines. That is partly for the lessons' sake —
re-indenting a block that size rewraps lines at `cargo fmt` and invalidates every
downstream listing — and partly because the extracted method is what part 4 wants anyway.

`the_only_tab_cannot_be_closed` is deleted. The behaviour it protected is the behaviour
being removed.
