# Roadmap

What's built, what's next, and what's deliberately not happening.

The tutorial is **linear**: lessons count upward and every part starts from the editor the
previous part left behind. Parts are a reading aid, not directories — everything lives in
`lessons/`.

**Lessons are written just-in-time.** A part is planned here in one line; its lessons are
written only once the part before it is finished and running. This is not fastidiousness:
every propagation bug in this tutorial's history came from writing lessons ahead of the
working code.

Vocabulary is in [CONTEXT.md](CONTEXT.md); decisions whose reasoning would otherwise
evaporate are in [docs/adr/](docs/adr/).

## Done

| Part | Lessons | What it delivered |
| --- | --- | --- |
| **A working editor** | [1–12](lessons/) | Opens files, edits and saves them without corrupting UTF-8, highlights Rust, tabs across buffers, degrades honestly above 512 KB, keeps its text in a rope with a measured justification, and tests the parts worth testing |
| **1 — Don't lose my work** | [13–15](lessons/0013-knowing-what-changed.html) | The editor cannot silently discard your edits by any route |

| Lesson | Title | What it delivered |
| --- | --- | --- |
| [13](lessons/0013-knowing-what-changed.html) | Knowing What Changed | The buffer knows whether it differs from disk, and says so on the tab and in the status bar |
| [14](lessons/0014-the-index-that-outlived-its-buffer.html) | The Index That Outlived Its Buffer | Closing a buffer, and the stale-index bug lesson 9 predicted |
| [15](lessons/0015-being-asked-first.html) | Being Asked First | A confirmation before closing a modified buffer or the window, and your first hand-written enum |

## Next

| # | Part | Lessons | What you'll learn |
| --- | --- | --- | --- |
| 2 | **Files from inside the editor** | 3 | `fs::read_dir`, `Path` vs `PathBuf`, `OsStr` and names that aren't UTF-8; round-tripping line endings you didn't write |
| 3 | **Buffers that aren't files yet** | 3 | The buffer list stops being fixed at start-up: New, Save As, and an editor that can hold nothing |
| 4 | **Many files, many modules** | 3 | `mod`, `pub`, `use crate::`, visibility, multi-file layout |
| 5 | **Search in file** | 3–4 | Iterator chains, byte and char indices, highlighting a match |
| 6 | **A second language** | 3 | Table-driven vs enum vs trait, `Path::extension` |
| 7 | **Themes** | 3 | `Style`/`Visuals`, `Default`, const tables |
| 8 | **Files on disk** | 3–4 | Recursion and ownership, lazy expansion, tree state across frames |
| 9 | **Command palette** | 4 | Fuzzy matching, command enums, keymaps |
| 10 | **Line numbers** | 3 | Painting a gutter from `galley.rows`; wrapped rows vs real lines |
| 11 | **Git aware** | 5–6 | An FFI-shaped API, lifetimes across a library boundary, diffing, caching |
| 12 | **Projects** | 4 | `serde`, config paths, versioned formats, migration |
| 13 | **Search across a directory** | 4 | The `ignore` crate, parallelism, where `rayon` earns its place |
| 14 | **Diagnostics from `cargo check`** | 5–6 | An async runtime inside a frame loop that sleeps; subprocess lifecycle, streaming, cancellation |
| 15 | **ACP** | 3–4 | JSON-RPC over stdio, protocol versioning |

Terms in bold in that table are defined in [CONTEXT.md](CONTEXT.md), which is the
authority on what **Directory** and **Project** mean. They are different intentions, not
two sizes of one thing, and keeping them apart is why parts 8, 12 and 13 are three parts
rather than an argument.

**Parts 2, 3 and 8 share one seam.** Every route that opens a file — the picker in part 2,
New in part 3, the tree in part 8 — ends at the same `Editor::open_path`. Part 2 builds
it; the others call it. That overlap is the design, not duplication.

**Why part 2 reads disk and part 8 walks it.** Part 2 lists a single directory to put a
picker on screen, which is where `read_dir`, `Path`/`PathBuf` and `OsStr` are taught. Part
8 is what those become when the listing has to nest: recursion, ownership of a tree that
outlives a frame, and reading a directory only when it is expanded. Part 8 is the smaller
part because part 2 paid for the foundations.

A part runs 3–6 lessons. Past six is the signal it was really two parts.

**Why 14 before 15.** ACP is an external, evolving protocol, and this tutorial's whole
method is checking a premise against a compiler or a benchmark before teaching it — which
you cannot do against a spec. Part 14 teaches the same async, subprocess and streaming
Rust against `cargo check`, where every premise is verifiable on your own machine. ACP is
then a small delta on machinery you already understand, and if the spec has moved, only
the last part is affected.

## Unscheduled

**The highlight-cache regression.** A naive cache took idle frames from 26.8 ms to 5.4 ms
and typing from 47.1 ms to 186.2 ms; the parts measured account for 0.15 ms of the 139 ms
gap. See [lesson 8](lessons/0008-knowing-when-to-stop.html). This is held back
deliberately as the **graduation exercise** — a real open problem in code you understand
completely. Nobody knows the answer, so there is no lesson to write until someone finds
it.

**Advanced search.** Filtering a search by anything a **Project** knows and a
**Directory** doesn't. Deliberately parked: part 13 searches a Directory, so this is an
additive change to part 12 if it is ever wanted, not a reason to couple the two.

## Not happening

| Not doing | Why |
| --- | --- |
| **Owning the text rendering** | Reimplementing text input, selection, clipboard and IME is where most hobby editors die. Line numbers and git gutter marks are reachable without it, by painting beside rows egui already positions. Revisit only if multiple cursors becomes a goal |
| **Multiple cursors** | The one feature that genuinely requires owning the rendering |
| **Split panes** | Layout algebra with little Rust in it |
| **Minimap** | Decoration |
| **Autosave** | Needs a timer, a temp-file strategy and a recovery path. If it ever happens it belongs near projects, not in part 1 |
| **Terminal panel** | PTY handling is a project of its own and teaches little about editors |
| **Plugin system** | Ruled out by `MISSION.md`, correctly |
| **LSP** | Optional, and much cheaper after part 14 shares its transport. Pick it up only if wanted |

## Open

**How feedback gets collected**, once this is published — issues, discussions, or something
per-lesson. Deliberately deferred: the right answer depends on where it's published, and
that decision belongs with part 7.

## Publishing

After **part 7**. By then the editor is correct, modular and presentable, and there are
roughly eighteen lessons of material beyond lesson 15. `main` stays the bare `cargo new`
scaffold so a reader starts at lesson 1; the finished editor lives only on the work branch.
