# Starting point: no Rust, learning-driven, egui chosen

> **Reframed 2026-08-22.** This record was originally written with *portfolio/career* as
> the driver. After lessons 1–12 the driver was reconsidered and settled as **learning**,
> with the portfolio artifact as a byproduct. The starting facts below are unchanged; the
> implications have been rewritten to match. See `MISSION.md` and `ROADMAP.md`.

Deryk has **never written Rust** — not "read the book and forgot it", genuinely zero.
Everything language-level must be taught, including syntax, and no familiarity with
ownership, traits, or Cargo can be assumed.

The driver is **learning Rust properly**. The editor is the vehicle: a problem with enough
real depth that the language has to be understood rather than pattern-matched. A repo a
hiring manager can run and be impressed by is a valuable byproduct, and Deryk needs to be
able to explain every line of it — but comprehension is the goal and the artifact is the
evidence, not the other way round. A working editor built from code they can't explain is
a mission failure, not a partial success.

Target is a **code editor / IDE-lite** (syntax highlighting, multiple buffers), built on
an **immediate-mode GUI** (`egui`/`eframe`), chosen for fastest time-to-runnable.

## Implications

- Teach Rust *through* editor features, never as a separate track — the mission dies if
  the first three weeks are `fn main()` exercises with no window on screen.
- Every lesson must end with something that compiles and runs. Motivation is the scarce
  resource for a beginner on a long project.
- Quiz on *previously written* code, not just new material — the explicability
  requirement means storage strength matters more than usual here.
- **Features earn their place by what they teach.** A feature that adds capability without
  adding understanding is scope creep, however much the editor would benefit.
- No toolchain existed on the machine at workspace creation; installed via `rustup`.
