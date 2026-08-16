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
3. ✅ Saving — `#[must_use]`, `?`, `if let`, Ctrl+S, and `main`'s deferred boilerplate
   _(written 2026-08-16; ends at 65 lines; lesson 1's promise now paid)_
4. ✅ Where is the cursor — `Option`, `TextEdit::show`, byte vs char index
   _(written 2026-08-16; 89 lines; Ln/Col readout)_
5. ✅ Open any file — CLI args, `unwrap_or_else`, match guards, `ErrorKind::NotFound`
   _(written 2026-08-16; 97 lines; fixes the lesson-2 "error text in the buffer" bug)_
6. Feel `String` insertion hurt on a large file → introduce `ropey`
7. Custom painting: stop using `TextEdit`, draw our own text and caret
8. Multiple buffers → `Vec<Buffer>`, tabs, and borrow-checker pressure
9. Syntax highlighting
10. Polish, README, release build

## Plan revisions

- **2026-08-16 (b):** planned lesson 5 was "struct design pressure". Replaced by
  "open any file" — the CLI-arg change is one line but it exposes a real bug (a missing
  file's error text landing in the save buffer), and fixing a bug the learner already
  shipped beats an abstract refactor. Struct design will arrive on its own once multiple
  buffers force it.
- **2026-08-16 (a):** lesson 2 was going to be "struct design, `Vec<String>` of lines".
  Dropped — `TextEdit` binds to a `&mut String`, so a line-vector can't work until we
  paint text ourselves. A lines-based buffer is a lesson-6-or-later idea, and lesson 1's
  own footer already promised file opening. Teach the thing the code can actually do.

## Things to watch for

- Never-written-Rust + ambitious project is the classic setup for a stalled repo.
  Prioritise *runnable at every step* over correct architecture.
- Watch for copy-paste comprehension. The mission says "can explain every line in an
  interview" — quiz on code written two lessons ago, not just today's.
- ~~Lesson 3 owes an explanation of `main`'s boilerplate~~ — paid in lesson 3's
  "The boilerplate lesson 1 deferred" section.
- **The editor can now write to disk.** Lesson 3 points it at `editor/scratch.md`
  precisely so a stray keystroke can't overwrite `src/main.rs`. Never move it back to
  opening its own source now that saving exists.
- Lesson 3 uses a let-chain (`if a && let Err(e) = ...`), which clippy asked for. It is
  edition-2024 syntax; if Deryk finds it alien, the nested form plus an extracted
  `save_and_report` method is the fallback — it compiles clean too, at 75 lines.
- `?` earns its place in lesson 3 because `save` does a fallible write *then* a
  follow-up. Don't retro-fit `?` into single-operation functions just to show it off.
- Lesson 4 deliberately defers grapheme clusters (tabs, emoji) to the custom-painting
  lesson. It says so in a sidenote — don't quietly drop that promise.
- Lesson 5's checkpoint is **abridged** (elides unchanged fns) — the first one that is.
  Its `open` and `main` were diffed against the verified 97-line file. If Deryk dislikes
  abridged checkpoints, revert to full listings; the lesson's ask-block invites that.
- `move` is NOT needed on eframe's app-creator closure: `AppCreator<'app>` carries a
  lifetime, so it can borrow a local. I had planned a lesson-5 teaching moment around
  the missing-`move` error; it does not exist. Verified against eframe 0.36.1 source.
- Lesson 6 owes the immediate-mode performance reckoning — lesson 1 promises a fight
  with egui when a 50,000-line file meets a naive redraw.
