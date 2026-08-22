use eframe::egui;
use egui::text::{ByteIndex, CharIndex, LayoutJob};
use ropey::Rope;
use std::char;
use std::env;
use std::fs;
use std::io;
use std::ops::Range;
use std::sync::Arc;
use std::time::Instant;

const PLAIN: egui::Color32 = egui::Color32::from_rgb(0xe8, 0xe5, 0xde);
// Words the highlighter treats as keywords
const KEYWORDS: &[&str] = &[
    "as", "const", "else", "enum", "fn", "for", "if", "impl", "in", "let", "match", "mod", "move",
    "mut", "pub", "return", "self", "struct", "trait", "use", "while",
];
const KEYWORD: egui::Color32 = egui::Color32::from_rgb(0xcf, 0x9b, 0xe0);
const STRING: egui::Color32 = egui::Color32::from_rgb(0xa3, 0xcf, 0x8c);
const COMMENT: egui::Color32 = egui::Color32::from_rgb(0x8b, 0x92, 0x9c);

// Above this size, highlighting costs more than a frame is worth. Chosen from
// measurement: at 427 KB a keystroke costs 7.1 ms, at 1.1 MB it costs 17.4 ms,
// and a 60fps frame is 16.7 ms.
const HIGHLIGHT_LIMIT: usize = 512 * 1024;

// Split `text` into coloured runs and hand egui a ready-made layout.
fn scan(text: &str) -> Vec<(&str, egui::Color32)> {
    let mut runs = Vec::new();
    let mut rest = text;
    while !rest.is_empty() {
        let (chunk, colour) = if rest.starts_with("//") {
            let end = rest.find('\n').unwrap_or(rest.len());
            (&rest[..end], COMMENT)
        } else if let Some(after_quote) = rest.strip_prefix('"') {
            let end = after_quote.find('"').map_or(rest.len(), |i| i + 2);
            (&rest[..end], STRING)
        } else if rest.starts_with(|c: char| c.is_alphanumeric() || c == '_') {
            let end = rest
                .find(|c: char| !(c.is_alphanumeric() || c == '_'))
                .unwrap_or(rest.len());
            let word = &rest[..end];
            let colour = if KEYWORDS.contains(&word) {
                KEYWORD
            } else {
                PLAIN
            };
            (word, colour)
        } else {
            let end = rest.char_indices().nth(1).map_or(rest.len(), |(i, _)| i);
            (&rest[..end], PLAIN)
        };

        runs.push((chunk, colour));
        rest = &rest[chunk.len()..];
    }
    runs
}

// Lay `text` out for egui, colouring it unless the file is too big.
fn highlight(ui: &egui::Ui, text: &str, wrap_width: f32) -> Arc<egui::Galley> {
    let font = egui::TextStyle::Monospace.resolve(ui.style());
    let mut job = LayoutJob::default();
    job.wrap.max_width = wrap_width;

    let runs = if text.len() > HIGHLIGHT_LIMIT {
        vec![(text, PLAIN)]
    } else {
        scan(text)
    };

    for (chunk, colour) in runs {
        job.append(
            chunk,
            0.0,
            egui::TextFormat {
                font_id: font.clone(),
                color: colour,
                ..Default::default()
            },
        );
    }

    ui.ctx().fonts_mut(|f| f.layout_job(job))
}

/// The text of one buffer, backed by a rope.
///
/// A rope stores text as a tree of small chunks, so an edit rewrites one chunk
/// and an index lookup walks the tree instead of the text.
struct Text {
    rope: Rope,
    /// egui's `TextBuffer::as_str` must return a *borrowed contiguous* `&str`,
    /// and a rope has no such slice to lend. So we keep a flattened copy here
    /// and rebuild it on every edit.
    flat: String,
}

impl Text {
    fn new(text: &str) -> Self {
        Self {
            rope: Rope::from_str(text),
            flat: text.to_owned(),
        }
    }
    fn as_str(&self) -> &str {
        &self.flat
    }
    fn len(&self) -> usize {
        self.flat.len()
    }
    fn line_col(&self, char_index: usize) -> (usize, usize) {
        let char_index = char_index.min(self.rope.len_chars());
        let line = self.rope.char_to_line(char_index);
        (line + 1, char_index - self.rope.line_to_char(line) + 1)
    }
    fn sync(&mut self) {
        self.flat = self.rope.to_string();
    }
}

impl egui::TextBuffer for Text {
    fn type_id(&self) -> std::any::TypeId {
        std::any::TypeId::of::<Self>()
    }
    fn is_mutable(&self) -> bool {
        true
    }
    fn as_str(&self) -> &str {
        &self.flat
    }
    fn insert_text(&mut self, text: &str, char_index: CharIndex) -> usize {
        self.rope
            .insert(char_index.0.min(self.rope.len_chars()), text);
        self.sync();
        text.chars().count()
    }
    fn delete_char_range(&mut self, char_range: Range<CharIndex>) {
        let end = self.rope.len_chars();
        self.rope
            .remove(char_range.start.0.min(end)..char_range.end.0.min(end));
        self.sync();
    }
    fn byte_index_from_char_index(&self, char_index: CharIndex) -> ByteIndex {
        ByteIndex(
            self.rope
                .char_to_byte(char_index.0.min(self.rope.len_chars())),
        )
    }
    fn char_index_from_byte_index(&self, byte_index: ByteIndex) -> CharIndex {
        CharIndex(
            self.rope
                .byte_to_char(byte_index.0.min(self.rope.len_bytes())),
        )
    }
}

struct Buffer {
    path: String,
    text: Text,
    status: String,
}

impl Buffer {
    // Open a file into a new editor. A file that doesn't exist yet is not an
    // error - it's a new file, and starts empty.
    fn open(path: &str) -> Self {
        let (text, status) = match fs::read_to_string(path) {
            Ok(contents) => (contents, String::new()),
            Err(error) if error.kind() == io::ErrorKind::NotFound => {
                (String::new(), format!("new file: {path}"))
            }
            Err(error) => (String::new(), format!("could not open {path}: {error}")),
        };
        Self {
            path: path.to_owned(),
            text: Text::new(&text),
            status,
        }
    }
    // Write the buffer back to the file it came from
    fn save(&mut self) -> io::Result<()> {
        fs::write(&self.path, self.text.as_str())?;
        self.status = format!("saved {} bytes to {}", self.text.len(), self.path);
        Ok(())
    }
    // Turn a character offset into a 1-based line and column.
    fn line_col(&self, char_index: usize) -> (usize, usize) {
        self.text.line_col(char_index)
    }

    fn name(&self) -> &str {
        self.path
            .trim_end_matches('/')
            .rsplit('/')
            .next()
            .filter(|name| !name.is_empty())
            .unwrap_or(&self.path)
    }
}

struct Editor {
    buffers: Vec<Buffer>,
    active: usize,
    position: String,
    frame_ms: f32,
    line_col_us: f32,
}

impl Editor {
    fn open(paths: &[String]) -> Self {
        let buffers = paths.iter().map(|p| Buffer::open(p)).collect();
        Self {
            buffers,
            active: 0,
            position: "no cursor".to_owned(),
            frame_ms: 0.0,
            line_col_us: 0.0,
        }
    }
}

impl eframe::App for Editor {
    fn ui(&mut self, ui: &mut egui::Ui, _frame: &mut eframe::Frame) {
        let frame_start = Instant::now();

        egui::Panel::bottom("status").show(ui, |ui| {
            let highlighting = if self.buffers[self.active].text.len() > HIGHLIGHT_LIMIT {
                "highlighting off (file too large)"
            } else {
                "highlighting on"
            };
            ui.label(format!(
                "{} · {} bytes · {highlighting} · line_col {:.0} µs · {:.2} ms/frame",
                self.position,
                self.buffers[self.active].text.len(),
                self.line_col_us,
                self.frame_ms,
            ));
            ui.label(&self.buffers[self.active].status);
        });
        ui.horizontal(|ui| {
            for index in 0..self.buffers.len() {
                let selected = index == self.active;
                if ui
                    .selectable_label(selected, self.buffers[index].name())
                    .clicked()
                {
                    self.active = index;
                }
            }
        });
        let buffer = &mut self.buffers[self.active];
        egui::CentralPanel::default().show(ui, |ui| {
            let save_requested = ui.input(|i| i.modifiers.command && i.key_pressed(egui::Key::S));
            if save_requested && let Err(error) = buffer.save() {
                buffer.status = format!("save failed; {error}");
            }

            ui.heading(&buffer.path);
            egui::ScrollArea::vertical().show(ui, |ui| {
                let mut layouter =
                    |ui: &egui::Ui, buffer: &dyn egui::TextBuffer, wrap_width: f32| {
                        highlight(ui, buffer.as_str(), wrap_width)
                    };
                let output = egui::TextEdit::multiline(&mut buffer.text)
                    .desired_width(f32::INFINITY)
                    .layouter(&mut layouter)
                    .show(ui);

                self.position = match output.cursor_range {
                    Some(range) => {
                        let started = Instant::now();
                        let (line, column) = buffer.line_col(range.primary.index.0);
                        self.line_col_us = started.elapsed().as_secs_f32() * 1_000_000.0;
                        format!("Ln {line}, Col {column}")
                    }
                    None => "no cursor".to_owned(),
                };
            });
        });

        self.frame_ms = frame_start.elapsed().as_secs_f32() * 1000.0;
    }
}

fn main() -> eframe::Result {
    let paths: Vec<String> = env::args().skip(1).collect();
    let paths = if paths.is_empty() {
        vec!["scratch.md".to_owned()]
    } else {
        paths
    };

    let options = eframe::NativeOptions {
        viewport: egui::ViewportBuilder::default().with_inner_size([800.0, 600.0]),
        ..Default::default()
    };

    eframe::run_native(
        "editor",
        options,
        Box::new(|_cc| Ok(Box::new(Editor::open(&paths)))),
    )
}

#[cfg(test)]
#[allow(clippy::unwrap_used, reason = "a panic is how a test reports failure")]
mod tests {
    use super::*;

    fn buffer_with(text: &str) -> Buffer {
        Buffer {
            path: "test.rs".to_owned(),
            text: Text::new(text),
            status: String::new(),
        }
    }

    #[test]
    fn line_col_starts_at_one_one() {
        assert_eq!(buffer_with("abc").line_col(0), (1, 1));
    }

    #[test]
    fn line_col_counts_newlines() {
        let b = buffer_with("ab\ncd");
        assert_eq!(b.line_col(2), (1, 3));
        assert_eq!(b.line_col(3), (2, 1));
        assert_eq!(b.line_col(5), (2, 3));
    }

    #[test]
    fn line_col_counts_characters_not_bytes() {
        let b = buffer_with("caf\u{e9}x");
        assert_eq!(b.line_col(5), (1, 6));
    }

    #[test]
    fn line_col_past_the_end_is_the_end() {
        assert_eq!(buffer_with("ab").line_col(999), (1, 3));
    }

    #[test]
    fn name_of_a_bare_filename() {
        assert_eq!(buffer_with("").name(), "test.rs");
    }

    #[test]
    fn name_of_a_nested_path() {
        let mut b = buffer_with("");
        b.path = "src/widgets/main.rs".to_owned();
        assert_eq!(b.name(), "main.rs");
    }

    #[test]
    fn name_of_a_trailing_slash() {
        let mut b = buffer_with("");
        b.path = "src/".to_owned();
        assert_eq!(b.name(), "src");
    }

    #[test]
    fn scan_colours_keyword_only() {
        let runs = scan("let x");
        assert_eq!(runs[0], ("let", KEYWORD));
        assert_eq!(runs[2], ("x", PLAIN));
    }

    #[test]
    fn scan_handles_an_unterminated_string() {
        let runs = scan("s = \"oops");
        assert_eq!(runs.last().unwrap(), &("\"oops", STRING));
    }

    #[test]
    fn scan_resassembles_the_original_text() {
        let text = "fn a() { // hi\n let s = \"x\";\n}\n";
        let joined: String = scan(text).iter().map(|(c, _)| *c).collect();
        assert_eq!(joined, text);
    }
}
