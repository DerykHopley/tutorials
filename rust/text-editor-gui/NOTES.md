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
6. ✅ Measure before you optimise — `Instant`, frame-time readout, status panel, real numbers
   _(written 2026-08-16; 121 lines; overturned the "String is the bottleneck" plan)_
7. ✅ Colouring the code — `TextEdit::layouter`, `LayoutJob`, a 40-line scanner
   _(written 2026-08-16; 184 lines)_
8. ✅ Knowing when to stop — measure highlighting, degrade above a measured limit
   _(written 2026-08-16; 208 lines; deliberately ships NO cache — see below)_
9. ✅ More than one file — `Buffer`/`Editor` split, `Vec<Buffer>`, tabs, index-not-reference
   _(written 2026-08-16; 246 lines)_
10. ✅ Tests that find something — `#[cfg(test)]`, a real red test, extract `scan` to test it
   _(written 2026-08-16; 331 lines, 10 tests; found and fixed a real `name()` bug)_
11. ✅ Earning the rope — newtype + `egui::TextBuffer`, `ropey`, and the justification doc
   _(written 2026-08-22; 415 lines, 10 tests; the rope is justified by egui's char→byte
   conversion, not by insertion cost)_
12. ✅ Making it a work sample — remove `request_repaint`, `[lints]` table, release
   profile, README _(written 2026-08-22; 415 lines; the tutorial's last lesson)_

**Final total: 12.** Undo/redo was dropped — egui already provides it (see below).

### Parts after lesson 12 (see ROADMAP.md for the plan)

13. ✅ Knowing what changed — `dirty`, a rope snapshot _(444 lines, 13 tests)_
14. ✅ The index that outlived its buffer — `close`, the clamp, Ctrl+W _(508 lines, 14 tests)_
15. ✅ Being asked first — `Modal`, `enum Pending`, `quitting` echo fix _(620 lines, 17 tests)_
16. ✅ The names in a directory — `read_dir`, Ctrl+O picker, `open_path` seam
    _(written 2026-08-31; 700 lines, 20 tests; lesson stated 659, corrected 2026-09-12)_
17. ✅ Paths that aren't strings — `PathBuf`/`Path`/`OsString`, `args_os`, `Entry`/`Picker`,
    directory navigation _(written 2026-09-12; 769 lines, 22 tests; five stages)_
    - Every premise proven before writing: `env::args()` panics on `caf\xe9.txt` (real
      output quoted); the lesson-16 picker reports the file as *new* (headless click, status
      `new file: caf�.txt`, text empty); stage 4's picker opens it (text read back); the end
      state navigates `src/` → `..` → opens `Cargo.toml` (headless probe, harness in the
      session transcript).
    - `DirEntry::file_type()` does **not** follow symlinks — found because the probe crate
      symlinks `target/`, which then listed without a slash. Kept `file_type()?` for the
      third-`?` teaching point; sidenote names `fs::metadata` as the alternative.
    - `browse` on an unreadable directory writes to the status bar *behind* the modal.
      Named in a warn callout as deliberate; a `Picker.error` field is the fix if wanted.
    - The quit-dialog per-file Save and the lesson-14 last-buffer guard are still open
      (part 3 deletes the guard — ADR 0002).
18. ✅ Line endings you didn't write — `enum LineEnding`, `detect`/`label`/`apply`, `Cow`,
    normalise `\r\n` at open and apply the ending at save; closes part 2
    _(written 2026-09-13; 879 lines, 31 tests; five stages)_
    - Premises measured before writing (probe crate `/tmp/l18probe`, harness in the session
      transcript): egui gives `\r` a glyph with a letter's advance (7.83 px) and a 0×0
      texture rect, so the cursor floats one cell past the last letter and `line_col`
      reports Col 5 on a three-letter line; ropey treats `\r\n` as one line break, so line
      numbers were already right; Enter inserts `"\n"` (`egui-0.36.1/src/widgets/text_edit/builder.rs:1166`);
      an edit then save on a CRLF file wrote `one\r\nx\ntwo\r\n`, and `file` reports it as
      "with CRLF, LF line terminators". The untouched round trip was already exact.
    - The obvious `save` (`let contents = self.line_ending.apply(...)` used after
      `mark_saved`) fails with a real E0502 because `Cow::Borrowed` keeps `self.text`
      borrowed; the lesson shows it and fixes it by taking the length first.
    - Open items, named in the lesson: multiline paste goes into the buffer as-is
      (`builder.rs:1119`), so a Windows clipboard can put a `\r` into a buffer that is
      supposed to hold none, and `apply` would then write `\r\r\n`; a lone `\r` is neither
      detected nor normalised; a mixed-ending file becomes uniform on first save; the status
      bar counts buffer bytes while the save message counts disk bytes.
    - Stage sources were built by `l18-tooling/mk.py` — textual edits over `l17.rs` — rather
      than by hand, and `l18-tooling/apply.py` checks nine intermediate states (the two
      compiler-error states and the red test included). Do it this way from now on.

### Three planned premises that measurement killed

Recording these because the pattern matters: **every time I checked a planned premise
against the compiler or a benchmark, roughly one in three was false.**

1. **Lesson 6** was to be "feel `String` insertion hurt → introduce ropey". `String::insert`
   mid-file on 2 MB is 11 µs. Premise false; lesson became profiling.
2. **Lesson 9** was to be where "struct design forces itself / borrow-checker pressure"
   appears. It doesn't. Rust's disjoint closure captures (edition 2021+) accept the naive
   `let buffer = &mut self.buffers[self.active];` inside the panel closure while
   `self.line_col_us` is assigned. **Verified: the naive version compiles clean.** The
   real Rust lesson there is self-referential structs (why `active: usize` not
   `&mut Buffer`), which does produce genuine errors — E0106 then E0505.
3. **Lesson 10** was to be undo/redo. **egui's `TextEdit` already implements it**: it owns
   an `Undoer` and binds Ctrl+Z itself (`egui-0.36.1/src/widgets/text_edit/builder.rs`,
   and `src/util/undoer.rs`). Building our own would duplicate a working feature and fight
   egui for the keybinding. Lesson 10 became tests instead.

**Standing instruction: verify the premise before writing the lesson, not after.**

### RESOLVED 2026-08-22: the rope is justified — but not for the reason anyone says

Measured before writing lesson 11, with `egui::Context::run_ui` driving real frames
(`/tmp/ropebench`, rebuild it if needed). **The textbook argument for a rope is false here,
and a different one is true.**

The textbook argument is "`String::insert` is O(n)". It is, and it does not matter:
12 µs mid-file on 2.3 MB, 0.07% of a frame.

What *does* cost is **`TextBuffer::byte_index_from_char_index`**, which egui calls **3×
per keystroke** and implements as a `char_indices()` walk from the start of the buffer
(`egui-0.36.1/src/text_selection/text_cursor_state.rs:276`; egui's own `impl TextBuffer
for String` uses it at lines 254, 269, 270). At 2.3 MB that is ~1 ms a call.

Typing, 50,000 lines / 2.3 MB, median of 40 frames:

| Buffer | Frame | char→byte | insert | delete |
| --- | --- | --- | --- | --- |
| `String` (egui's own impl) | **12.21 ms** | 3.05 ms | 1.05 | 2.01 |
| `Rope` (ropey 1.6.1) | **7.74 ms** | 0.00 ms | 0.14 | 0.19 |
| `String` + ASCII fast path | **7.33 ms** | 0.00 ms | 0.02 | 0.00 |

Size sweep (typing, ms/frame): 1k lines 0.22/0.16/0.16 · 5k 1.25/0.96/0.91 ·
10k 2.45/2.00/1.86 · 25k 6.17/3.87/3.81 · 50k 12.34/7.82/7.58 (String/Rope/ASCII).

**The ASCII fast path — char index == byte index when the text `is_ascii()` — beats the
rope and is three lines.** It also collapses the moment the file contains one non-ASCII
character:

| 2.3 MB file with one `é` in a comment | Frame |
| --- | --- |
| `String` | 10.70 ms |
| `Rope` | **7.57 ms** |
| `String` + ASCII fast path | 10.39 ms — back to the naive walk |

So the rope's real claim is **it does not care what is in the file**. That is the written
justification the mission asks for, and it is measured rather than asserted.

Two costs to state honestly in the lesson:
- `TextBuffer::as_str` is a *required* method returning a borrowed contiguous `&str`. A
  rope has no such slice to lend, so we keep a flattened `String` beside it and rebuild it
  on every edit — 77 µs on 2.3 MB, and **double the memory**.
- `Rope::from_str` costs 647 µs on 2.3 MB, against ~0 for a `String`. Slower to open.

Bonus, on our own code: `line_col` was a `chars().take()` walk measured at 875 µs in
lesson 6 (1000 µs here). `Rope::char_to_line` + `line_to_char` is **0.23 µs** — 4,000×.
`Rope::clone` is 0.02 µs against 41.72 µs for `String`, which is the undo-snapshot
argument if we ever want it.

### Lesson 12 measurements (2026-08-22)

**`request_repaint()` costs a core.** Probed `FullOutput`'s `repaint_delay` on idle
frames: with the call, `0ns` — redraw immediately, forever. Without it, `Duration::MAX`,
i.e. wait for input. Lesson 1's claim about immediate mode was false in our editor from
lesson 6 until lesson 12 removed it.

**Release profile, clean builds of the editor:**

| Profile | Binary | Build |
| --- | --- | --- |
| default | 26.0 MB | 39.0 s |
| `strip = true` | 19.3 MB | 37.4 s |
| `lto = "thin"` | 25.4 MB | 37.8 s |
| `lto = "fat"` + `codegen-units = 1` + `strip` | **15.5 MB** | 89.1 s |

`strip` is the free win; LTO buys 3.8 MB more for ~50 s. `panic = "abort"` not taken —
it complicates `cargo test` for no measured gain here.

**The unwrap audit found nothing** — there is no `unwrap()`/`expect()` outside the tests,
and `clippy::pedantic` is clean; `clippy::nursery` finds one `missing_const_for_fn`. So
lesson 12 enforces the standard rather than fixing violations. The real finding was that
**`cargo clippy` never checked the test module**: `--all-targets` is required, and with it
the `[lints]` deny fires on the tests' legitimate `.unwrap()`, which is why `mod tests`
carries an `#[allow(..., reason = "…")]`.

**`indexing_slicing` deliberately not enabled** — 5 sites, all safe by construction. A
lint you intend to ignore trains you to ignore lints.

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

## Verified end-state sources

Each lesson's end state is reconstructed from the published checkpoints, compiled, and
used to generate that lesson's listings. **Those reconstructions live in `/tmp` and have
been lost twice.** Rebuilding one is error-prone in a specific way: the obvious shortcut is
to start from Deryk's working copy, which compiles and passes — but it has drifted from the
published checkpoints in ways that are invisible until they reach a listing.

Real drift found while rebuilding for lesson 13, all of it silent:

- Doc comments shortened or turned from `///` into `//` — the lesson 13 checkpoint would
  have published Deryk's wording as if it were the tutorial's.
- Two test names carrying typos (`scan_colours_keyword_only`,
  `scan_resassembles_the_original_text`). Harmless in their file; wrong in a listing.
- The status-bar format string using single spaces around `·` instead of double.
- **A structural difference**: the tab loop sits at the top level of `fn ui` rather than
  inside `CentralPanel`, so every listing touching it was one indent level off.

The fix each time is to splice the canonical region out of the *published checkpoint* and
verify with a set-difference of checkpoint lines against the base. That check is cheap and
catches all four classes above. **Do it before generating any listing from a rebuilt base.**

**They now live in `~/.cache/text-editor-sources/`, not `/tmp`** — `/tmp` was cleaned
three times, and each rebuild is where the drift above creeps in. That directory is outside
the repo, so it breaks no rule about `main`; it just stops the archaeology repeating.

**Lesson 17 added the check that makes this mechanical (2026-09-12).** `/tmp/l17/apply.py`
(in the session transcript; worth promoting into the repo as `sources.py`'s partner) reads
the *rendered* lesson, takes each stage's blocks as patches — `dim`+`del` lines are the
context to find, `dim`+`add` the replacement — applies them in order to the previous
stage's source, and diffs the result against the compiled stage source. Lesson 17's five
stages reproduce `l17_s2`, `l17_s3`, `l17_s4` and `l17` byte for byte, and stage 4's
intermediate states after edits 2 and 5 match the sources that produced the quoted
compiler error and red test. On the first run it caught five blocks whose dimmed context
skipped a blank line or matched the wrong `Self {` — none of which the six `build.py`
audits can see. It needs the stage sources, which is why it is not in `build.py` yet.

Cached sources now: `l13 l14 l14_s1 l14_s2 l14_s2_tests l14_s3 l15 l15_s1 l15_s2 l16
l17_s2 l17_s3 l17_s4_a l17_s4_red l17_s4 l17 l18_s2_nod l18_s2 l18_s3_e0063 l18_s3_fixed l18_s3
l18_s4_red l18_s4_e0502 l18_s4 l18`, with each lesson's `mk.py`/`gen.py`/`apply.py` in
`l17-tooling/` and `l18-tooling/`. `l15.rs` was rebuilt with the `quitting`
fix from 5fadda3 (620 lines); `l16.rs` from lesson 16's checkpoint (700 lines).

Worth doing properly at some point: a `sources.py` that rebuilds every end state from the
checkpoints and compiles it, so this is one command rather than an archaeology session.
Checking the sources in directly would be simpler still, but `main` is meant to hold no
finished lesson code — that needs Deryk's decision before it happens.

## Plan revisions

- **2026-08-22 (b): the tutorial continues as parts, and the driver changed.** A grilling
  session settled the shape of everything after lesson 12. The decisions, and why:
  - **Learning is the driver; portfolio is a byproduct; being a daily driver is an explicit
    non-goal.** Deryk's own framing — "work my way from easiest to more complex features as
    a learning experience". The non-goal is written into `MISSION.md` because it is the
    only thing that stops an unbounded feature backlog.
  - **One tutorial, flat lesson numbering, parts grouped by `ROADMAP.md`.** Not a directory
    per feature: every part edits the same `editor/` crate, which lives *inside* the
    tutorial directory, and a reader genuinely cannot do the git part without having built
    the editor. Linear material should have a linear structure.
    (Note for later: `build.py` requires a document's parent directory to be `lessons/` or
    `reference/` — `README.md`'s "at any depth" refers to the tutorial, not to nesting
    inside `lessons/`. Grouping lessons into sub-directories is a one-line change if flat
    numbering ever gets unwieldy.)
  - **Lessons stay just-in-time.** Never write lesson N+1 before Deryk has finished N.
    Evidence: *every* propagation bug in this tutorial came from writing ahead — lesson 3's
    edit-count bug silently broke lesson 4's diff; the lesson 6 status-bar fix invalidated
    the stages of lessons 7–10; lesson 11 stage 2 used a field stage 4 added. A roadmap
    ahead is fine. Lessons ahead are not.
  - **Lessons 1–12 are not frozen.** The six `build.py` audits made finding these defects
    mechanical, so fixing on contact stays cheap.
  - **Stay on `TextEdit`; do not own the text rendering.** `TextEditOutput` exposes the
    galley and its `galley_pos`, and a galley carries `rows: Vec<PlacedRow>` each with its
    own `pos` — so **line numbers and git gutter marks look reachable without owning
    rendering**, by painting beside rows egui already positions. This contradicts an
    earlier claim in these notes that line numbers force the fork. **Verify by building it
    before writing part 9.** The honest trigger to revisit the fork is multiple cursors,
    which is now out of scope.
  - **ACP is deferred behind `cargo check`.** ACP is an external, evolving spec, and this
    tutorial's method is checking premises against a compiler or benchmark — which cannot
    be done against a spec. Part 13 teaches the same async/subprocess/streaming Rust against
    `cargo check`, fully verifiable locally; ACP becomes a small delta.
  - **The highlight-cache regression becomes the graduation exercise**, unscheduled. It
    cannot be planned as a lesson because nobody knows the answer.
  - **Publishing after part 6.** Feedback mechanism deliberately deferred to that point.
  - Branch model unchanged: `main` stays the bare scaffold, work stays on
    `work/rust-text-editor-gui`.


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
- **Peak-hold on the frame counter: offered 2026-08-16, Deryk declined for now.** The
  raw live number flickers, which confused them until lesson 6 gained a callout saying it
  would. Do not add peak-hold speculatively. It becomes genuinely motivated in two places:
  (a) **lesson 11**, where any rope decision rests on measuring *edit-time spikes* — a raw
  live number is close to unreadable for that, so the instrument would be improved because
  the measurement demands it, which is a better lesson than "here's a nicer widget"; and
  (b) **lesson 12**, where `request_repaint()` comes out and the readout's fate is decided
  anyway (delete it, or put it behind a debug flag).
- **The status bar is a bottom `Panel` as of 2026-08-16**, added to lesson 6 because the
  readout was unreachable on a file taller than the window — Deryk hit this opening
  `big.rs`. Two things this pins down, both measured rather than assumed:
  egui 0.36 has **no `TopBottomPanel`** (the side panels were unified into one `Panel`
  type, so it's `egui::Panel::bottom(id)`); and a bottom panel declared *after* the
  `CentralPanel` gets a height of **zero pixels**, silently. Panels must come first.
  Consequence: the status bar shows the *previous* frame's cursor position, so `Editor`
  carries a `position: String`. Same one-frame lag `frame_ms` already had.
- Lesson 6 leaves `request_repaint()` in the code so the readout keeps updating. It burns
  CPU when idle, which contradicts lesson 1's praise of egui. The lesson says so; lesson 7
  or the polish lesson should remove it or put it behind a flag.
- Lesson 6's numbers are from this machine. The lesson tells Deryk to expect different
  absolute values and to check the *shape* (linear in size, ~10× debug/release).
- Benchmarks used `Context::run_ui` headlessly. Gotcha: you must call
  `out.textures_delta.clear()` or epaint panics on drop with "Dropped TexturesDelta with
  1 unapplied deltas".

- **2026-09-12: the build-first lesson variants are gone.** Deryk asked for them to be
  removed ("they aren't needed now"). Lessons 1, 16 and 17 had one each, plus
  `assets/spoiler.css`, `spoiler.js` and `vocab.css`, which nothing else used. The
  walked-through lessons are unchanged; lesson 1's *concise* variant stays. Don't write a
  build-first variant for new lessons unless asked again.
