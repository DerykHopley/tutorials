# Roadmap

What's built, what's next, and what's deliberately not happening.

The tutorial is **linear**: lessons count upward and every part starts from the editor the
previous part left behind. Parts are a reading aid, not directories — everything lives in
`lessons/`.

**Lessons are written just-in-time.** A part is planned here in one line; its lessons are
written only once the part before it is finished and running. This is not fastidiousness:
every propagation bug in this tutorial's history came from writing lessons ahead of the
working code.

## Done

| Part | Lessons | What it delivered |
| --- | --- | --- |
| **A working editor** | [1–12](lessons/) | Opens files, edits and saves them without corrupting UTF-8, highlights Rust, tabs across buffers, degrades honestly above 512 KB, keeps its text in a rope with a measured justification, and tests the parts worth testing |

## In progress

**Part 1 — Don't lose my work.** The editor loses unsaved edits silently when the window
closes, and has since lesson 3.

| Lesson | Title | What it delivered |
| --- | --- | --- |
| [13](lessons/0013-knowing-what-changed.html) | Knowing What Changed | The buffer knows whether it differs from disk, and says so on the tab and in the status bar |
| 14 | — | Closing a buffer, and being asked first |

## Next

| # | Part | Lessons | What you'll learn |
| --- | --- | --- | --- |
| 1 | **Don't lose my work** | 3–4 | Change detection, close and quit callbacks, modal state in immediate mode, and buffer removal — lesson 9's index-invalidation hazard, finally triggered |
| 2 | **Files from inside the editor** | 4–5 | Opening and creating files without the command line; round-tripping line endings you didn't write |
| 3 | **Many files, many modules** | 3 | `mod`, `pub`, `use crate::`, visibility, multi-file layout |
| 4 | **Search** | 3–4 | Iterator chains, byte and char indices, highlighting a match |
| 5 | **A second language** | 3 | Table-driven vs enum vs trait, `Path::extension` |
| 6 | **Themes** | 3 | `Style`/`Visuals`, `Default`, const tables |
| 7 | **File tree** | 4–6 | `Path` vs `PathBuf`, recursion and ownership, lazy expansion |
| 8 | **Command palette** | 4 | Fuzzy matching, command enums, keymaps |
| 9 | **Line numbers** | 3 | Painting a gutter from `galley.rows`; wrapped rows vs real lines |
| 10 | **Git aware** | 5–6 | An FFI-shaped API, lifetimes across a library boundary, diffing, caching |
| 11 | **Projects** | 4 | `serde`, config paths, versioned formats, migration |
| 12 | **Workspace search** | 4 | The `ignore` crate, parallelism, where `rayon` earns its place |
| 13 | **Diagnostics from `cargo check`** | 5–6 | An async runtime inside a frame loop that sleeps; subprocess lifecycle, streaming, cancellation |
| 14 | **ACP** | 3–4 | JSON-RPC over stdio, protocol versioning |

A part runs 3–6 lessons. Past six is the signal it was really two parts.

**Why 13 before 14.** ACP is an external, evolving protocol, and this tutorial's whole
method is checking a premise against a compiler or a benchmark before teaching it — which
you cannot do against a spec. Part 13 teaches the same async, subprocess and streaming
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
| **LSP** | Optional, and much cheaper after part 13 shares its transport. Pick it up only if wanted |

## Open

**How feedback gets collected**, once this is published — issues, discussions, or something
per-lesson. Deliberately deferred: the right answer depends on where it's published, and
that decision belongs with part 6.

## Publishing

After **part 6**. By then the editor is correct, modular and presentable, and there are
roughly seventeen lessons of material. `main` stays the bare `cargo new` scaffold so a
reader starts at lesson 1; the finished editor lives only on the work branch.
