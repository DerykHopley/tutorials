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
6. ✅ Measure before you optimise — `Instant`, frame-time readout, real numbers
   _(written 2026-08-16; 114 lines; overturned the "String is the bottleneck" plan)_
7. ✅ Colouring the code — `TextEdit::layouter`, `LayoutJob`, a 40-line scanner
   _(written 2026-08-16; 172 lines)_
8. ✅ Knowing when to stop — measure highlighting, degrade above a measured limit
   _(written 2026-08-16; 196 lines; deliberately ships NO cache — see below)_
9. Multiple buffers → `Vec<Buffer>` + tabs. Struct design finally forces itself here
10. Undo/redo — the first thing a reviewer presses after typing _(candidate)_
11. Tests — `line_col` and `open` are pure and beautifully testable _(candidate)_
12. `ropey` — justified by a measurement from lessons 8–9, with the written rationale
13. Polish: README, release profile, `unwrap` audit, remove `request_repaint`

**Estimated total: 12–14.** Floor is 11 if 10 and 11 are dropped.

### Open question: the highlight cache

A naive cache (compare the text, keep the last galley) measured, at 50k lines:
idle 26.80 → 5.39 ms, but typing 47.11 → **186.22 ms**. The parts don't explain it:
`String == String` on 2 MB is 0.039 ms and `to_owned` is 0.107 ms, and holding the
previous galley alive across frames costs nothing measurable (tested in isolation).
egui 0.36 has no `util::cache` helper to fall back on.

**Lesson 8 deliberately ships no cache and says so, with the numbers.** Do not add one
without profiling this properly first — the pathology is real and unexplained. It is
written up in the lesson as an open question, and Deryk has been invited to chase it.

### The fork that decides the number

`TextEdit::layouter(&mut dyn FnMut(&Ui, &dyn TextBuffer, f32) -> Arc<Galley>)` exists in
egui 0.36 (verified in source). That means **syntax highlighting does not require
abandoning `TextEdit`**, which is the single biggest scoping decision left:

- **Stay on `TextEdit`** (planned above): ~12–14 lessons. Keeps egui's text input,
  selection, clipboard and IME for free. Accepts the lesson-6 ceiling — 7 ms/frame while
  typing at 50k lines in release, and under 1.5 ms at 10k, which covers almost all real
  source files.
- **Own the rendering** (paint text ourselves, cull to the viewport): +3 or more lessons,
  ~16 total, and it means reimplementing text input, selection and clipboard from
  scratch. This is where most hobby editors die. Only take it if the mission changes to
  "understand rendering" rather than "ship a portfolio editor".

Lesson 6's closing section currently promises lesson 7 will be "drawing only what you can
see". **If we take the stay-on-`TextEdit` path, that promise must be rewritten** — do not
leave it dangling.

## Plan revisions

- **2026-08-16 (c):** lesson 6 was planned as "feel `String` insertion hurt → introduce
  `ropey`". **Measured, and the premise was false.** On a 2 MB / 50k-line file:
  `String::insert` mid-file = 11 µs (0.2% of frame); `line_col` = 875 µs (12%); egui's
  full-text layout ≈ 6.2 ms (87%). Debug build ≈ 10× slower than release at every size
  (70.61 ms vs 7.10 ms per keystroke at 50k lines). So lesson 6 became a profiling lesson
  and the rope moved to lesson 8, gated on a measurement. **Do not reintroduce the rope
  until a number asks for it** — the lesson explicitly makes that promise.
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
- ~~Lesson 6 owes the immediate-mode performance reckoning~~ — paid in lesson 6.
- Lesson 6 leaves `request_repaint()` in the code so the readout keeps updating. It burns
  CPU when idle, which contradicts lesson 1's praise of egui. The lesson says so; lesson 7
  or the polish lesson should remove it or put it behind a flag.
- Lesson 6's numbers are from this machine. The lesson tells Deryk to expect different
  absolute values and to check the *shape* (linear in size, ~10× debug/release).
- Benchmarks used `Context::run_ui` headlessly. Gotcha: you must call
  `out.textures_delta.clear()` or epaint panics on drop with "Dropped TexturesDelta with
  1 unapplied deltas".
