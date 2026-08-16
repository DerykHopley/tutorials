# Starting point: no Rust, portfolio-driven, egui chosen

Deryk has **never written Rust** — not "read the book and forgot it", genuinely zero.
Everything language-level must be taught, including syntax, and no familiarity with
ownership, traits, or Cargo can be assumed.

The driver is **portfolio/career**: the artifact needs to be a repo a hiring manager can
run and be impressed by, and Deryk needs to be able to explain every line in an
interview. This raises the bar on comprehension over coverage — a working editor built
from code they can't explain is a mission failure, not a partial success.

Target is a **code editor / IDE-lite** (syntax highlighting, multiple buffers), built on
an **immediate-mode GUI** (`egui`/`eframe`), chosen for fastest time-to-runnable.

## Implications

- Teach Rust *through* editor features, never as a separate track — the mission dies if
  the first three weeks are `fn main()` exercises with no window on screen.
- Every lesson must end with something that compiles and runs. Motivation is the scarce
  resource for a beginner on a long project.
- Quiz on *previously written* code, not just new material — the interview-explicability
  requirement means storage strength matters more than usual here.
- No toolchain existed on the machine at workspace creation; installed via `rustup`.
