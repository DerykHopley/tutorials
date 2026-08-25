# Mission: Writing a text editor GUI in Rust

## Why

**Deryk is learning Rust.** The editor is the vehicle, not the destination — a problem
with enough genuine depth (data structures, rendering, input handling, performance) that
the language has to be learned properly rather than pattern-matched.

A repo a hiring manager can open, run and be impressed by is a **byproduct** of doing that
well, and worth protecting. It is not what steers the work.

Starting point: **no prior Rust** (2026-08-16). The editor and the language got learned
together, and lessons 1–12 delivered a working one. See [ROADMAP.md](ROADMAP.md) for
what's built and what's next.

## Success looks like

Competences, not features. Features are the excuse.

- **Reads a crate's source to answer a question** rather than guessing at its API — this
  tutorial has been wrong about an API from memory more than once, and checking is the fix
- **Splits a program into modules** without being shown how
- **Reaches for a measurement before an optimisation**, unprompted — roughly one premise
  in three has turned out false when actually checked
- **Can explain any line of the editor** to an interviewer, including the ones they'd now
  write differently
- **Graduation: can add a feature to this editor without a lesson being written for it.**
  The [highlight-cache regression](ROADMAP.md#unscheduled) is the exercise held back for
  exactly this

## Explicit non-goal

**This is not trying to become an editor anyone uses daily.** Better editors exist. The
moment "I want to use this" becomes a goal, the pressure is to ship features rather than
understand them, and lessons get skipped to get to the interesting part. Features earn
their place by what they teach.

## What lessons 1–12 delivered

Kept as a record — these were the original success criteria, and all of them were met:

- A GitHub repo a hiring manager can `cargo run` and immediately type code into ✅
- Opens a real source file, edits it, saves it back without corrupting UTF-8 ✅
- Syntax highlighting for at least one language ✅
- Multiple open buffers with tab switching ✅
- A text buffer backed by a rope, with a written justification of why not `String` ✅
  — and the justification turned out to be a different one than expected
- Idiomatic Rust: no `unwrap()` in the hot path, errors handled deliberately ✅
  — now enforced by a `[lints]` table rather than by good intentions

## Constraints

- Immediate-mode GUI (`egui` / `eframe`), staying on `TextEdit` rather than painting text
  ourselves — see [ROADMAP.md](ROADMAP.md#not-happening)
- Linux, Wayland session (Fedora-based atomic desktop); toolchain via `rustup` in `$HOME`
- Legibility counts as much as features: README, commits and code comments are part of the
  deliverable, and this is published material after part 6
- Lessons are written **just-in-time**, never ahead of the working code

## Out of scope

- Writing our own GPU renderer, text shaper, or window abstraction (winit/wgpu from scratch)
- A plugin system
- Vim modal editing — not the goal unless the mission changes
- Cross-platform packaging for macOS/Windows until the Linux build is genuinely good

The full list of declined features, with reasons, is in [ROADMAP.md](ROADMAP.md#not-happening).
