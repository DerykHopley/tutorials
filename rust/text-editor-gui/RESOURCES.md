# Text Editor GUI in Rust — Resources

## Knowledge

### Rust the language

- [The Rust Programming Language — Brown University interactive edition](https://rust-book.cs.brown.edu/)
  **Preferred over the official book.** Same text, plus inline quizzes you retry to
  mastery and Aquascope diagrams that visualise ownership at compile time and runtime.
  The ownership chapter is rewritten based on published research into what learners
  actually get wrong. Use for: every language concept. Start at Ch. 1–4.
- [The Rust Programming Language — official](https://doc.rust-lang.org/book/)
  The canonical text by Klabnik, Nichols & Krycho. Use for: checking that the Brown
  fork hasn't drifted, and for chapters the fork doesn't enhance.
- [The Rust Programming Language, Ch. 9 — Error Handling](https://rust-book.cs.brown.edu/ch09-00-error-handling.html)
  9.1 is `panic!` (what `unwrap()` triggers); 9.2 is `Result` and the `?` operator.
  Use for: anything about failure. Primary source for lesson 2.
- [`std::fs` API docs](https://doc.rust-lang.org/std/fs/)
  Use for: `read_to_string`, `write`, and what each one can fail at.
- [`std::io::Error` API docs](https://doc.rust-lang.org/std/io/struct.Error.html)
  Use for: `ErrorKind`, and matching on *why* a read failed rather than just that it did.
- [Rust by Example](https://doc.rust-lang.org/rust-by-example/)
  Runnable snippets. Use for: "what does the syntax for X look like", fast.
- [The Cargo Book](https://doc.rust-lang.org/cargo/)
  Use for: dependencies, features, workspaces, release profiles.

### egui / eframe (our GUI layer)

- [egui on GitHub — emilk/egui](https://github.com/emilk/egui)
  Source of truth. The README's "immediate mode" section is the clearest explanation
  of the paradigm anywhere. Use for: paradigm, tradeoffs, project status.
- [egui API docs](https://docs.rs/egui/latest/egui/)
  Use for: what a widget is called and what it returns.
- [eframe API docs](https://docs.rs/eframe/latest/eframe/)
  The framework that gives egui a window and an event loop. Current stable: **0.36.1**
  (Aug 2026). Use for: `App` trait, native options, startup.
- [egui web demo](https://www.egui.rs/)
  The whole widget gallery running in-browser, with source. Use for: "is there already
  a widget for this?" — check here before building one.
- [egui examples directory](https://github.com/emilk/egui/tree/main/examples)
  Minimal, compiling, version-matched examples. Use for: correct boilerplate.

### Text buffers & editor internals

- [ropey — cessen/ropey](https://github.com/cessen/ropey)
  The rope crate we'll use. Edits in single-digit microseconds on multi-gigabyte texts,
  and it makes invalid UTF-8 unrepresentable. Stable: **1.6.1**. Use for: buffer design,
  char-index vs byte-index thinking.
- [ropey API docs](https://docs.rs/ropey/latest/ropey/)
  Use for: `Rope`, `RopeSlice`, line/char/byte index conversions.
- [hecto: Build Your Own Text Editor in Rust — Philipp Flenker](https://flenker.blog/hecto/)
  ~3000 lines, terminal-based, built in small observable steps; updated May 2025.
  Use for: editor *logic* — cursor movement, viewport scrolling, file I/O, search.
  Ignore its rendering layer, ours is egui.

## Wisdom (Communities)

- [The Rust Users Forum — users.rust-lang.org](https://users.rust-lang.org/)
  The highest-signal place to ask "is this idiomatic?". Beginners are genuinely
  welcomed and answers often come from compiler contributors. Use for: code review
  requests, borrow-checker fights, design critique. **Best first stop.**
- [The Rust Programming Language Community Discord](https://discord.com/invite/rust-lang-community)
  ~70k members, real-time. Use for: quick unblocking when stuck mid-session.
- [r/rust](https://reddit.com/r/rust)
  Use for: showing finished work (the "what have you been working on" threads are
  ideal for a portfolio project), and ecosystem news.
- [egui GitHub Discussions](https://github.com/emilk/egui/discussions)
  Maintainer-answered. Use for: egui-specific design questions.
- [This Week in Rust](https://this-week-in-rust.org/)
  Weekly newsletter. Use for: staying current; also lists Rust job postings, which
  matters directly to the mission.

## Gaps

- No high-trust tutorial exists for *egui specifically as a text editor frontend*.
  Everything on that seam we derive ourselves from egui docs + editor theory.
  This is a feature, not a bug — it means the portfolio project isn't a clone.
- Need a trusted primary source on syntax highlighting in Rust
  (`syntect` vs `tree-sitter`) before we reach that milestone.
- Need a source on text rendering/glyph layout if we ever outgrow egui's built-in
  text handling.
