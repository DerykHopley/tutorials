#!/usr/bin/env python3
"""Turn real Rust source into the lesson stylesheet's span markup.

Authoring aid, not part of the build. Generating checkpoint markup from the
file that was actually compiled beats hand-transcribing it: the listing cannot
drift from the code, and the verbatim diff in the review pass then passes by
construction.

    python3 mkcode.py <file.rs> [first_line] [last_line] [--numbered]
"""

import html
import re
import sys

KEYWORDS = {
    "as", "const", "else", "enum", "fn", "for", "if", "impl", "in", "let", "match", "mod",
    "move", "mut", "pub", "return", "self", "Self", "struct", "trait", "use", "while",
    "true", "false", "dyn", "where", "crate",
}


def markup(line: str) -> str:
    stripped = line.lstrip()
    if stripped.startswith("//"):
        indent = line[: len(line) - len(stripped)]
        return f'{indent}<span class="c">{html.escape(stripped)}</span>'

    out, i = [], 0
    while i < len(line):
        ch = line[i]
        if ch == '"':
            j = i + 1
            while j < len(line):
                if line[j] == "\\":
                    j += 2
                    continue
                if line[j] == '"':
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
            word, after = line[i:j], line[j : j + 1]
            if word in KEYWORDS:
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


def render(lines: list[str], numbered: bool = False) -> str:
    rows = [markup(l) for l in lines]
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
    print(render(src[a - 1 : b], numbered))
