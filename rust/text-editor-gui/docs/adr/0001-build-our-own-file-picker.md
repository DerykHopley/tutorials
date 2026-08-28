---
status: accepted
date: 2026-08-28
---

# Build our own file picker rather than calling a native dialog

Part 2 needs "Open file…" at runtime, and the obvious answer is `rfd`, which hands back a
`PathBuf` for a few lines of code. We are writing the picker ourselves instead — listing a
directory with `fs::read_dir` and drawing it in egui — because this repo exists to learn
Rust, and a dependency that removes the `Path`/`PathBuf`/`OsStr` work removes the lesson
along with it.

## Considered options

**`rfd` (rejected).** Measured, not guessed: two crates (`rfd` and `pollster`) on top of
the 417 already in the lockfile, because the wayland and portal machinery arrives with
`eframe`/`winit` and the GTK features are off by default. It resolves to
`xdg-desktop-portal` over D-Bus — the correct Wayland-native route on this machine. So the
dependency cost was never the problem, and the honest reason to reject it is the one
above.

**A path-entry modal (rejected).** Type a path, press Enter. No dependency and no
`read_dir`, which would have kept part 2 at three lessons. Rejected because part 2 would
then ship an "Open file" that part 8 immediately supersedes.

## Consequences

Part 2 grew past its original budget and was split: part 2 (the picker and the filesystem
types) and part 3 (New, Save As and the empty state). Everything below shifted by one.

Part 8 — **Files on disk** — is correspondingly smaller, 3–4 lessons rather than 4–6. It
no longer teaches `read_dir`, `Path` vs `PathBuf` or `OsStr`, because part 2 did; it
teaches what those become when the listing has to nest — recursion, ownership of a tree
that outlives a frame, and lazy expansion. This is deliberate. A future reader looking at
part 8 and asking why the foundations are missing should look at part 2.

We give up one lesson we would otherwise have had: driving a blocking OS call from inside
an immediate-mode frame loop without stalling it. An in-app picker is immediate-mode and
never blocks, so the problem does not arise. If it is wanted later, part 14 covers the
same ground with more at stake.
