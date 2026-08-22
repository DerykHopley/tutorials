#!/usr/bin/env python3
"""Inline shared components into every lesson and reference document, so each
HTML file in this workspace is fully self-contained — one file you can move,
mail, or open from anywhere without breaking its styling.

Layout this expects:

    assets/                       shared components, used by every topic
    build.py                      this script
    LESSON-FORMAT.md              the house standard
    <topic>/<tutorial>/
        assets/                   OPTIONAL — overrides shared files by name
        lessons/*.html
        reference/*.html

Documents are discovered at any depth, so adding a topic needs no config here.

The HTML files are still the source. Each one carries marked regions:

    <!-- @assets:style.css,quiz.css -->
    ...generated...
    <!-- /@assets -->

This script regenerates whatever sits between those markers, so it is
idempotent — run it as often as you like. Anything outside the markers is never
touched.

Asset lookup is nearest-first: starting from the document's own directory, walk
up to the workspace root and use the first `assets/<name>` found. A tutorial can
therefore ship its own component (a pose diagram, a chess board) without
disturbing anything else, and can override a shared one by using its name.

Workflow: edit assets/style.css, then run

    python3 build.py

Editing the generated <style> block inside an HTML file works until the next
build, then gets silently overwritten. Edit the asset instead.
"""

import html
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent
DOC_DIRS = ("lessons", "reference")

BLOCK = re.compile(r"<!-- @assets:([^\s>]+) -->.*?<!-- /@assets -->", re.S)


def find_asset(name: str, start: pathlib.Path) -> pathlib.Path:
    """Nearest `assets/<name>` walking up from `start` to ROOT."""
    here = start.resolve()
    while True:
        candidate = here / "assets" / name
        if candidate.is_file():
            return candidate
        if here == ROOT:
            sys.exit(
                f"error: no assets/{name} found from {start.relative_to(ROOT)} "
                f"up to the workspace root"
            )
        here = here.parent


def render(names: str, doc: pathlib.Path) -> str:
    """Turn 'style.css,quiz.js' into the corresponding inline tags."""
    parts = []
    for raw in names.split(","):
        name = raw.strip()
        path = find_asset(name, doc.parent)
        body = path.read_text().strip()
        tag = "script" if path.suffix == ".js" else "style"

        # A closing tag inside the payload would end the element early.
        if f"</{tag}" in body.lower():
            sys.exit(f"error: {path.relative_to(ROOT)} contains a literal </{tag}>")

        parts.append(
            f"<{tag}>\n"
            f"/* ---- generated from {path.relative_to(ROOT)} — do not edit here ---- */\n"
            f"{body}\n"
            f"</{tag}>"
        )
    return "\n".join(parts)


def build(doc: pathlib.Path) -> bool:
    original = doc.read_text()
    rel = doc.relative_to(ROOT)

    if not BLOCK.search(original):
        print(f"  skip    {rel} (no @assets markers)")
        return False

    updated = BLOCK.sub(
        lambda m: f"<!-- @assets:{m.group(1)} -->\n{render(m.group(1), doc)}\n<!-- /@assets -->",
        original,
    )

    if updated == original:
        print(f"  ok      {rel}")
        return False

    doc.write_text(updated)
    print(f"  built   {rel}")
    return True


WORDS = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7}
COUNT = re.compile(r"\b(one|two|three|four|five|six|seven)\s+edits?\b", re.I)
STAGE = re.compile(r'<section class="stage"[^>]*>(.*?)</section>', re.S)
HEADING = re.compile(r"<h3[^>]*>(.*?)</h3>", re.S)


ACTION = re.compile(r"\b(rm|rmdir|chmod|chown|mkdir|mv|cp|git\s+reset)\b")
RUNBLOCK = re.compile(r'<p class="run">(.*?)</p>', re.S)
NOTE = re.compile(r'<span class="note">(.*?)</span>', re.S)


def check_hidden_actions(docs: list[pathlib.Path]) -> int:
    """A `.run` block lists a command and its expected output. A `.note` inside
    one is commentary — so a command hidden in a note reads as more output and
    gets skipped. Deryk hit this with "Then: rm editor/notes.md", which was a
    prerequisite for the next stage, not a footnote. Actions belong in their own
    run block or a callout.
    """
    problems = 0
    for doc in docs:
        for run in RUNBLOCK.finditer(doc.read_text()):
            for note in NOTE.finditer(run.group(1)):
                text = " ".join(re.sub(r"<[^>]+>", " ", note.group(1)).split())
                if ACTION.search(text):
                    print(
                        f"  WARN    {doc.relative_to(ROOT)}: command hidden in a "
                        f'run-block note — "{text[:60]}"'
                    )
                    problems += 1
    return problems


def check_edit_counts(docs: list[pathlib.Path]) -> int:
    """A stage that says "Three edits" must contain three code blocks.

    Under-counting is the worst defect this format has: a reader tallies the
    edits, stops early, and silently ends up with a file that no longer matches
    the next lesson. It happened for real — lesson 3 claimed four edits and had
    five, so the status label never got added and lesson 4's diff didn't apply.
    """
    problems = 0
    for doc in docs:
        body = doc.read_text()
        for stage in STAGE.finditer(body):
            seg = stage.group(1)
            claim = COUNT.search(re.sub(r"<[^>]+>", " ", seg))
            if not claim:
                continue
            blocks = seg.count('<p class="filename">')
            says = WORDS[claim.group(1).lower()]
            if says != blocks:
                title = HEADING.search(seg)
                title = re.sub(r"<[^>]+>", "", title.group(1)).strip() if title else "?"
                print(
                    f"  WARN    {doc.relative_to(ROOT)}: stage \"{title}\" "
                    f"says {says} edit(s) but has {blocks} code block(s)"
                )
                problems += 1
    return problems


FIELD_USE = re.compile(r"\bself\.([a-z_][a-z0-9_]*)\b")
FIELD_DECL = re.compile(r"^\s*([a-z_][a-z0-9_]*):\s*\S")
OPEN_SPAN = re.compile(r"<span\b")
ADD_SPAN = re.compile(r'<span class="add">')
PRE = re.compile(r"<pre[^>]*>(.*?)</pre>", re.S)


def spans(body: str, opener: re.Pattern[str]):
    """Yield (offset, inner markup) for each matching span, honouring nesting.

    A non-greedy `(.*?)</span>` stops at the first close tag, which inside
    syntax-highlighted code is usually one token in. That regex silently
    truncated this audit's input to the word `Panel` and reported all clear.
    """
    for match in opener.finditer(body):
        i, depth = match.end(), 1
        while depth:
            nxt = body.find("</span>", i)
            if nxt < 0:
                break
            depth += len(OPEN_SPAN.findall(body, i, nxt)) - 1
            i = nxt + len("</span>")
        yield match.start(), body[match.end() : i - len("</span>")]


def plain(markup: str) -> str:
    return html.unescape(re.sub(r"<[^>]+>", "", markup))


def check_field_order(docs: list[pathlib.Path]) -> int:
    """A stage may not use a field that a later stage introduces.

    Stage listings get generated from the finished source, so it is easy to
    paste the end-state version of a line into an early stage and ship code
    that cannot compile yet. Lesson 6 did exactly that: stage 2's status label
    read `self.line_col_us`, a field stage 4 adds, so anyone following along
    hit E0609 at stage 3 with no way to tell whose mistake it was.

    Declarations come from `.add` spans, uses from any code inside a stage.
    Fields inherited from an earlier lesson are already in the reader's file,
    so a lesson that never adds a field never checks it.
    """
    problems = 0
    for doc in docs:
        body = doc.read_text()
        declared: dict[str, int] = {}
        used: dict[str, int] = {}

        # Both are keyed by the offset of the enclosing <pre>, so a field
        # declared and used in the *same* block reads as simultaneous rather
        # than as a use that precedes its declaration.
        for stage in STAGE.finditer(body):
            for block in PRE.finditer(stage.group(1)):
                at = stage.start() + block.start()
                markup = block.group(1)
                for _, added in spans(markup, ADD_SPAN):
                    for line in plain(added).splitlines():
                        decl = FIELD_DECL.match(line)
                        if decl and "(" not in line:
                            declared.setdefault(decl.group(1), at)
                for use in FIELD_USE.finditer(plain(markup)):
                    used.setdefault(use.group(1), at)

        for name, first_use in sorted(used.items(), key=lambda kv: kv[1]):
            if name in declared and first_use < declared[name]:
                print(
                    f"  WARN    {doc.relative_to(ROOT)}: uses self.{name} before "
                    f"the stage that adds the field"
                )
                problems += 1
    return problems


CHECKPOINT = re.compile(r'<h2[^>]*id="where-you-ended-up"[^>]*>(.*?)<h2', re.S)
GAP = re.compile(r'<span class="gap">')
ELISION = re.compile(r'<span class="c">\s*//\s*[…\.]')


def check_checkpoints(docs: list[pathlib.Path]) -> int:
    """A checkpoint listing must be a whole file, minus marked gaps.

    Two things go wrong here, and both did. A listing can get truncated when a
    generator writes it — lessons 7 and 8 each shipped one that stopped in the
    middle of a closure, so the reader had nothing to diff the end of their
    file against. And a gap can get marked with a `// … unchanged …` comment
    instead of a `.gap` span, which reads as a line to type.

    The brace test is the cheap version of "is this a whole file": every
    marked gap can swallow at most a few, so a large imbalance means the
    listing simply stops.
    """
    problems = 0
    for doc in docs:
        body = doc.read_text()
        seg = CHECKPOINT.search(body)
        if not seg:
            continue
        seg = seg.group(1)
        gaps = len(GAP.findall(seg))
        depth = 0
        for block in PRE.finditer(seg):
            code = plain(block.group(1))
            depth += code.count("{") - code.count("}")
        if depth > gaps + 1:
            print(
                f"  WARN    {doc.relative_to(ROOT)}: checkpoint has {depth} unclosed "
                f"brace(s) but only {gaps} marked gap(s) — a listing is truncated"
            )
            problems += 1
        for hit in ELISION.finditer(seg):
            print(
                f"  WARN    {doc.relative_to(ROOT)}: checkpoint elides code with a "
                f"comment — use <span class=\"gap\"> so it can't be mistaken for code"
            )
            problems += 1
    return problems


BAND = re.compile(r'<span class="(?:add|del)">')
ONE_LINE_BAND = re.compile(r'^<span class="(?:add|del)">.*</span>$')


def check_band_lines(docs: list[pathlib.Path]) -> int:
    """A `.add` or `.del` band must start at the beginning of its line.

    Both are `display: inline-block; width: 100%` — a full-width row, because
    that is what makes a diff readable at a glance. Open one in the middle of a
    line and the fragment claims a row of its own, so a single line of code
    renders as two or three stacked bands. Lesson 7 shipped one: `let (chunk,
    colour) = ` was dimmed and the `if` that followed it on the same line
    opened a green band.

    The fix is always the same — band whole lines. If only part of a line
    changed, show the old line as `.del` and the new one as `.add`.
    """
    problems = 0
    for doc in docs:
        body = doc.read_text()
        for pre in PRE.finditer(body):
            first = body[: pre.start(1)].count("\n") + 1
            run, run_at = 0, 0
            for offset, line in enumerate(pre.group(1).split("\n")):
                for band in BAND.finditer(line):
                    before = re.sub(r"<[^>]+>", "", line[: band.start()])
                    if before.strip():
                        print(
                            f"  WARN    {doc.relative_to(ROOT)}:{first + offset}: band "
                            f'opens mid-line, after "{before.strip()[:40]}"'
                        )
                        problems += 1

                # A band per line draws a left bar and a box per line, so a
                # block of new code comes out striped instead of as one panel.
                # Deryk spotted it in lesson 11, where every line had its own.
                if ONE_LINE_BAND.match(line):
                    if run == 0:
                        run_at = first + offset
                    run += 1
                else:
                    if run > 2:
                        print(
                            f"  WARN    {doc.relative_to(ROOT)}:{run_at}: {run} "
                            f"consecutive one-line bands — wrap the run in one span"
                        )
                        problems += 1
                    run = 0
            if run > 2:
                print(
                    f"  WARN    {doc.relative_to(ROOT)}:{run_at}: {run} consecutive "
                    f"one-line bands — wrap the run in one span"
                )
                problems += 1
    return problems


def main() -> None:
    docs = sorted(
        p
        for p in ROOT.rglob("*.html")
        if p.parent.name in DOC_DIRS and "node_modules" not in p.parts
    )
    if not docs:
        sys.exit(f"error: found no .html under any {'/ '.join(DOC_DIRS)} directory")

    print(f"Inlining assets into {len(docs)} document(s):")
    changed = sum(build(p) for p in docs)
    print(f"\n{changed} updated, {len(docs) - changed} already current.")

    problems = check_edit_counts(docs)
    print(
        "Edit counts: all stages agree with their code blocks."
        if not problems
        else f"Edit counts: {problems} stage(s) disagree — fix before publishing."
    )

    hidden = check_hidden_actions(docs)
    print(
        "Run blocks: no commands hidden in notes."
        if not hidden
        else f"Run blocks: {hidden} hidden command(s) — move them to a callout."
    )

    early = check_field_order(docs)
    print(
        "Field order: no stage uses a field a later stage adds."
        if not early
        else f"Field order: {early} forward reference(s) — a stage won't compile."
    )

    cut = check_checkpoints(docs)
    print(
        "Checkpoints: every listing runs to the end of its file."
        if not cut
        else f"Checkpoints: {cut} listing(s) truncated or elided with a comment."
    )

    bands = check_band_lines(docs)
    print(
        "Diff bands: every add/del covers a whole line, one span per run."
        if not bands
        else f"Diff bands: {bands} problem(s) — a band will render broken or striped."
    )


if __name__ == "__main__":
    main()
