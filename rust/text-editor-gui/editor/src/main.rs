use eframe::egui;

struct Editor {
    text: String,
}

impl Default for Editor {
    fn default() -> Self {
        Self {
            text: "Hello, editor.\n".to_owned(),
        }
    }
}

impl eframe::App for Editor {
    fn ui(&mut self, ui: &mut egui::Ui, _frame: &mut eframe::Frame) {
        egui::CentralPanel::default().show(ui, |ui| {
            ui.heading("editor");
            ui.add(
                egui::TextEdit::multiline(&mut self.text)
                    .font(egui::TextStyle::Monospace)
                    .desired_width(f32::INFINITY),
            );
            ui.label(format!("{} bytes", self.text.len()));
        });
    }
}

fn main() -> eframe::Result {
    let options = eframe::NativeOptions {
        viewport: egui::ViewportBuilder::default().with_inner_size([800.0, 600.0]),
        ..Default::default()
    };

    eframe::run_native(
        "editor",
        options,
        Box::new(|_cc| Ok(Box::new(Editor::default()))),
    )
}
