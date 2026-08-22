# editor

A small code editor in Rust, written to be read.

It opens files, edits them, saves them, highlights Rust syntax, and switches between
several open buffers. It is about 400 lines. Every decision in it was measured before it
was made, and the ones that were measured and *rejected* are written down too.

```
cargo run -- src/main.rs
```

## What it does

- Opens any file named on the command line; several at once become tabs
- Edits and saves with `Ctrl+S`, without corrupting UTF-8
- Highlights Rust keywords, strings and comments with a hand-written scanner
- Reports cursor position, file size and frame time in a status bar
- Falls back to plain text above 512 KB, and says so

## What it does not do

No LSP, no plugins, no modal editing, no search, no line numbers. The scope is
deliberately small: an editor you can read in a sitting is more useful as a work sample
than a half-finished IDE.

## Decisions worth reading

**The buffer is a rope, and the reason is not the one you'd expect.**
`String::insert` on a 2.3 MB file costs 12 µs — the textbook argument for a rope does not
apply here. What does cost is egui's character-index-to-byte-index conversion, which runs
three times per keystroke and walks the buffer. That is 3.05 ms of a 13 ms frame, and a
rope answers it in O(log n). The full argument, including the cheaper option I rejected
and what the rope costs in memory, is in [docs/why-a-rope.md](docs/why-a-rope.md).

**Syntax highlighting stops at 512 KB.** Measured: highlighting costs 4–5× plain layout
and crosses the 16.7 ms frame budget between 10,000 and 25,000 lines. Above the limit the
editor draws plain text and puts "highlighting off (file too large)" in the status bar,
because an editor that silently degrades looks broken.

**There is no highlight cache.** The obvious one — compare the text, keep the last galley
— took idle frames from 26.8 ms to 5.4 ms and typing from 47.1 ms to 186.2 ms. The parts I
measured account for 0.15 ms of that 139 ms regression, so I do not know what causes it.
Shipping an optimisation I cannot explain seemed worse than shipping none.

**`active: usize`, not `&mut Buffer`.** A struct cannot own a `Vec` and hold a reference
into it at the same time; that is a self-referential struct, and safe Rust rejects it.
Owning the collection and referring to a member by index is the shape that survives being
moved, which is why arenas and ECS libraries all look like this.

## Layout

`src/main.rs` is the whole program, in reading order: the highlighter, then `Text` (the
rope and egui's `TextBuffer` implementation), then `Buffer` (one open file), then `Editor`
(the app), then `main`, then the tests.

## Testing

```
cargo test
cargo clippy --all-targets
```

Ten unit tests. `--all-targets` matters: without it, clippy skips the test module
entirely. `Cargo.toml` denies `unwrap` and `expect` outside tests, so the mission's "no
`unwrap()` in the hot path" is enforced by the build rather than by good intentions.

## Built with

[`eframe`/`egui`](https://github.com/emilk/egui) 0.36 for the window and immediate-mode
UI, and [`ropey`](https://github.com/cessen/ropey) 1.6 for the text buffer.
