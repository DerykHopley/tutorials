# Why this editor uses a rope

`Buffer.text` is a `ropey::Rope` behind a `Text` wrapper, not a `String`. This is the
reasoning, with the numbers it came from. Measured on a 2.3 MB / 50,000-line Rust file,
release build, median of 40 frames while typing.

## The reason it is *not*

The usual argument is that `String::insert` is O(n) — inserting mid-file shifts everything
after it. That is true and it does not matter here: **12 µs**, or 0.07% of a 16.7 ms frame.
Copying contiguous memory is fast. If this were the only consideration, a `String` would
win on simplicity.

## The reason it is

egui asks the buffer to convert a character index into a byte index **three times per
keystroke**, and its default implementation walks the text from the start
(`egui-0.36.1/src/text_selection/text_cursor_state.rs:276`).

| Buffer | ms/frame while typing | of which char->byte |
| --- | --- | --- |
| `String` | 12.21 | 3.05 |
| `Rope` | 7.74 | 0.00 |

A rope's nodes carry byte, char and line counts, so the conversion is a descent down a
tree instead of a scan of the text. The same property makes `line_col` — which runs every
frame to draw the Ln/Col readout — go from 1000 µs to 0.23 µs.

## The option I rejected

If the text is pure ASCII, char index and byte index are equal, so both conversions become
`i.min(len)`. Three lines, no dependency, and it measures *better* than the rope: **7.33
ms**. It is also fragile in a way that matters for a code editor:

| 2.3 MB file | pure ASCII | with one `é` in it |
| --- | --- | --- |
| `String` | 12.21 ms | 10.70 ms |
| `String` + ASCII fast path | **7.33 ms** | 10.39 ms |
| `Rope` | 7.74 ms | **7.57 ms** |

One accented character anywhere in the file and every keystroke pays the linear walk
again. The rope has no fast path to fall off, and that predictability is what it is
actually being bought for.

## What it costs

Stated plainly, because it is not free:

- **Double the memory.** `TextBuffer::as_str` must return a borrowed contiguous `&str`,
  which a chunked rope cannot produce, so `Text` keeps a flattened `String` beside the
  rope and rebuilds it on every edit: 0.08 ms per keystroke at 2.3 MB.
- **Slower open.** `Rope::from_str` is 647 µs on 2.3 MB against roughly nothing for a
  `String`.
- **A dependency**, and a data structure a reader has to know to follow the code.

## When this would change

If the editor ever stopped using egui's `TextEdit` and painted text itself, the flattened
copy would go and the rope would get cheaper. If it only ever opened files under ~100 KB,
none of this would be measurable and a `String` would be the better answer.
