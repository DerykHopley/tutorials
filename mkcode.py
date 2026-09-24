#!/usr/bin/env python3
"""Turn real Rust or TypeScript source into the lesson stylesheet's span markup.

Authoring aid, not part of the build. Generating checkpoint markup from the
file that was actually compiled beats hand-transcribing it: the listing cannot
drift from the code, and the verbatim diff in the review pass then passes by
construction.

    python3 mkcode.py <file.rs|file.ts> [first_line] [last_line] [--numbered]

The language comes from the file extension.
"""

import html
import re
import sys

KEYWORDS = {
    "as", "const", "else", "enum", "fn", "for", "if", "impl", "in", "let", "match", "mod",
    "move", "mut", "pub", "return", "self", "Self", "struct", "trait", "use", "while",
    "true", "false", "dyn", "where", "crate",
    # Primitives, marked like keywords to match how the lessons were written by hand.
    "char", "str", "usize", "bool",
}

# TypeScript's primitive type names are marked like keywords too, for the same reason.
TS_KEYWORDS = {
    "as", "async", "await", "break", "const", "continue", "else", "export", "false", "for",
    "from", "function", "if", "import", "in", "let", "new", "null", "of", "return", "true",
    "type", "typeof", "undefined",
    "boolean", "number", "string",
}


def char_literal(line: str, i: int) -> str | None:
    """Return the char literal starting at `i`, or None if that quote is a lifetime.

    `'a'`, `'\\n'` and `'"'` are literals; `'static` and `&'a str` are not.
    """
    if line.startswith("'\\", i):
        end = line.find("'", i + 2)
        return line[i : end + 1] if end != -1 else None
    if len(line) > i + 2 and line[i + 2] == "'":
        return line[i : i + 3]
    return None


def markup(line: str, ts: bool = False) -> str:
    keywords = TS_KEYWORDS if ts else KEYWORDS
    # Rust quotes strings with " only; TypeScript also uses ' and `, and has no
    # char literals or lifetimes for a single quote to be confused with.
    quotes = "\"'`" if ts else '"'
    stripped = line.lstrip()
    if stripped.startswith("//"):
        indent = line[: len(line) - len(stripped)]
        return f'{indent}<span class="c">{html.escape(stripped)}</span>'

    out, i = [], 0
    while i < len(line):
        ch = line[i]
        if not ts and ch == "'" and (lit := char_literal(line, i)):
            # Must come before the string case: `'"'` is a char literal whose
            # content is a quote, and reading that quote as the start of a
            # string mangles the rest of the line.
            out.append(f'<span class="s">{html.escape(lit)}</span>')
            i += len(lit)
        elif ch in quotes:
            j = i + 1
            while j < len(line):
                if line[j] == "\\":
                    j += 2
                    continue
                if line[j] == ch:
                    j += 1
                    break
                j += 1
            out.append(f'<span class="s">{html.escape(line[i:j])}</span>')
            i = j
        elif line.startswith("//", i):
            out.append(f'<span class="c">{html.escape(line[i:])}</span>')
            i = len(line)
        elif ch.isalnum() or ch == "_":
            j = i
            while j < len(line) and (line[j].isalnum() or line[j] == "_"):
                j += 1
                # A decimal point belongs to the number — but only when a digit
                # follows it, so Rust's `0..n` stays a range.
                if (
                    ch.isdigit()
                    and line[j : j + 1] == "."
                    and line[j + 1 : j + 2].isdigit()
                ):
                    j += 1
            word, after = line[i:j], line[j : j + 1]
            if word in keywords:
                out.append(f'<span class="k">{html.escape(word)}</span>')
            elif after == "(" or line[j : j + 2] == "!(":
                out.append(f'<span class="f">{html.escape(word)}</span>')
            elif word[0].isupper():
                out.append(f'<span class="t">{html.escape(word)}</span>')
            elif word[0].isdigit():
                out.append(f'<span class="s">{html.escape(word)}</span>')
            else:
                out.append(html.escape(word))
            i = j
        else:
            out.append(html.escape(ch))
            i += 1
    return "".join(out)


def render(lines: list[str], numbered: bool = False, ts: bool = False) -> str:
    rows = [markup(l, ts) for l in lines]
    if numbered:
        rows = [f'<span class="l">{r}</span>' for r in rows]
    return "\n".join(rows)


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if a != "--numbered"]
    numbered = "--numbered" in sys.argv
    src = open(args[0]).read().split("\n")
    if src and src[-1] == "":
        src.pop()
    a = int(args[1]) if len(args) > 1 else 1
    b = int(args[2]) if len(args) > 2 else len(src)
    print(render(src[a - 1 : b], numbered, ts=args[0].endswith(".ts")))
