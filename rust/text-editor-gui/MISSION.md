# Mission: Writing a text editor GUI in Rust

## Why

Deryk wants a serious, demonstrable systems project for their portfolio — something
that proves real engineering ability to employers and collaborators, not another CRUD
app. A code editor is the vehicle: it is a problem with genuine depth (data structures,
rendering, input handling, performance) that a reviewer can open, run, and judge in
sixty seconds. Rust is the language because it makes the systems thinking visible.

Starting point: **no prior Rust**. The editor and the language get learned together.

## Success looks like

- A GitHub repo a hiring manager can `cargo run` and immediately type code into
- Opens a real source file, edits it, saves it back without corrupting UTF-8
- Syntax highlighting for at least one language
- Multiple open buffers with tab switching
- A text buffer backed by a rope, with a written justification of why not `String`
- Deryk can explain every line of it in an interview — no copy-pasted mystery code
- Written in idiomatic Rust: no `unwrap()` in the hot path, errors handled deliberately

## Constraints

- Zero Rust experience at the outset — ownership and borrowing must be earned, not skipped
- Immediate-mode GUI (`egui` / `eframe`) — fastest route to a runnable artifact
- Linux, Wayland session (Fedora-based atomic desktop); toolchain via `rustup` in `$HOME`
- Portfolio pressure means the repo's legibility counts as much as its features:
  README, commits, and code comments are part of the deliverable

## Out of scope

- Writing our own GPU renderer, text shaper, or window abstraction (winit/wgpu from scratch)
- LSP integration and a plugin system — revisit only once editing is solid
- Vim modal editing — not the goal unless the mission changes
- Cross-platform packaging for macOS/Windows until the Linux build is genuinely good
