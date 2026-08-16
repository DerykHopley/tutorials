# Learning Workspace

A workspace for learning things properly — one directory per tutorial, sharing a single
set of standards and components so every lesson looks and behaves the same regardless of
subject.

## Topics

| Topic | Tutorial | Mission | Status |
| --- | --- | --- | --- |
| Rust | [text-editor-gui](./rust/text-editor-gui/) | [MISSION](./rust/text-editor-gui/MISSION.md) — a portfolio-grade code editor, from zero Rust | Lesson 1 in progress |

## Layout

```
LESSON-FORMAT.md          the house standard — read before writing any lesson
NOTES.md                  who Deryk is, how they want to be taught, how to verify work
assets/                   shared components: stylesheet, quiz widget
build.py                  inlines assets into every document

<topic>/<tutorial>/
    MISSION.md            why this is being learned — grounds every lesson
    RESOURCES.md          vetted sources, communities, and known gaps
    NOTES.md              decisions and plans specific to this tutorial
    assets/               optional; overrides shared components by filename
    lessons/              0001-name.html … the primary unit of teaching
    reference/            compressed cheat-sheets, built to be printed
    learning-records/     0001-name.md … what's been learned, and what it unlocks
    <project>/            whatever is being built, if anything
```

Nothing here is auto-discovered by filename convention except the documents `build.py`
inlines — anything under a `lessons/` or `reference/` directory, at any depth.

## Working on it

```sh
python3 build.py      # after editing anything in an assets/ directory
```

Every lesson is a self-contained HTML file. Open one directly; there is no server and
nothing to install.

## Adding a topic

```sh
mkdir -p <topic>/<tutorial>/{lessons,reference,learning-records}
```

Then write `MISSION.md` first — the reason for learning it, in concrete terms. Every
later decision about what to teach traces back to that file, and a vague mission produces
lessons that feel abstract. `RESOURCES.md` comes second: find high-trust primary sources
before writing anything, rather than teaching from memory.

The standards in [LESSON-FORMAT.md](./LESSON-FORMAT.md) are deliberately subject-agnostic.
They were derived while building a Rust tutorial, but "stages", "one change per block",
"show the real error output", and "never reveal the finished artifact up front" apply
just as well to a language, an instrument, or a physical skill.

## One mission per tutorial

Each tutorial directory has exactly one `MISSION.md`. If a goal splits into two genuinely
different aims, that is two tutorial directories — a mission that tries to cover both
stops being a compass and becomes a wish list.
