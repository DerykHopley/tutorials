# Working Notes — Text Editor GUI in Rust

Topic-specific. Workspace-wide preferences and verification rules live in the
root [NOTES.md](../../NOTES.md).

## Environment

- Rust installed via `rustup` into `$HOME/.cargo` — **not** `rpm-ostree install rust`.
  `rustc 1.97.1` as of 2026-08-16. `source ~/.cargo/env` if a shell can't find cargo.
- The cargo project is at `rust/text-editor-gui/editor/`, and has its own git repo
  (created by `cargo new`). Nothing committed yet as of the restructure.

## Standing decisions

- **GUI layer:** `eframe` + `egui` 0.36.1 (immediate mode). Chosen 2026-08-16 for the
  fastest path to a runnable artifact. Revisit only if egui's text handling becomes the
  bottleneck.
  **API note:** 0.36 uses `fn ui(&mut self, ui: &mut egui::Ui, frame: &mut eframe::Frame)`,
  *not* the `update(&mut self, ctx: &Context, ...)` that every older tutorial shows.
  Assume anything found online is stale; compile before believing it.
- **Buffer:** `ropey` — but *not until Deryk has felt why `String` hurts*. Teaching the
  rope before the pain is answering an unasked question.
- **Portfolio framing:** every lesson should leave the repo commit-worthy and explicable
  in an interview. Legibility is part of the deliverable.

## Pedagogical plan (rough, revise freely)

The tension in this mission: zero Rust, but an ambitious target. Resolution is to teach
Rust *through* the editor rather than before it — each lesson introduces exactly the
language concept the next editor feature demands.

1. ✅ Window + owned `String` state + `&mut self` — the immediate-mode loop
   _(Deryk completed it 2026-08-16)_
2. ✅ Opening a real file — `Result`, `match`, why not `unwrap()`
   _(written 2026-08-16; ends at 45 lines with `Editor::open(path)`)_
3. Saving + the `?` operator + `main`'s deferred boilerplate (promised in lesson 1)
4. Cursor as (line, col) — the index-vs-grapheme problem appears here
5. Struct design pressure: what the `Editor` state needs to become
6. Custom painting: stop using `TextEdit`, draw our own text and caret
7. Feel `String` insertion hurt on a large file → introduce `ropey`
8. Multiple buffers → `Vec<Buffer>`, tabs, and borrow-checker pressure
9. Syntax highlighting
10. Polish, README, release build

## Plan revisions

- **2026-08-16:** lesson 2 was going to be "struct design, `Vec<String>` of lines".
  Dropped — `TextEdit` binds to a `&mut String`, so a line-vector can't work until we
  paint text ourselves. A lines-based buffer is a lesson-6-or-later idea, and lesson 1's
  own footer already promised file opening. Teach the thing the code can actually do.

## Things to watch for

- Never-written-Rust + ambitious project is the classic setup for a stalled repo.
  Prioritise *runnable at every step* over correct architecture.
- Watch for copy-paste comprehension. The mission says "can explain every line in an
  interview" — quiz on code written two lessons ago, not just today's.
- Lesson 3 owes an explanation of `main`'s boilerplate (`NativeOptions`, `Box::new`,
  the `|_cc|` closure, `..Default::default()`). Lesson 1 explicitly promises this.
- Lesson 6 owes the immediate-mode performance reckoning — lesson 1 promises a fight
  with egui when a 50,000-line file meets a naive redraw.
