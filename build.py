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


if __name__ == "__main__":
    main()
