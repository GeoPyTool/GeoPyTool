use eframe::egui;
use egui::{CentralPanel, Context, TopBottomPanel};
use serde::{Deserialize, Serialize};
use std::path::PathBuf;

static APP_TITLE: &str = "GeoRusTool";

mod features;
mod geochem;

#[derive(Default, Serialize, Deserialize, Clone)]
pub struct AppState {
    // Data
    raw_table: Table,
    filename: Option<PathBuf>,

    // Language
    language: Language,

    // Status
    status: String,
    // Views
    #[serde(skip)]
    k2o_view: geochem::K2OSiO2ViewState,
    #[serde(skip)]
    tas_view_open: bool,
    #[serde(skip)]
    ree_view_open: bool,
    #[serde(skip)]
    pearson_view_open: bool,
    #[serde(skip)]
    cipw_done: bool,
    #[serde(skip)]
    qapf_view_open: bool,
    #[serde(skip)]
    cipw_results: Vec<geochem::CipwNorm>,
    // Settings
    #[serde(skip)]
    tas_group_by_label: bool,
    #[serde(skip)]
    ree_standard_idx: usize,
    #[serde(skip)]
    tas_mode_is_volcanic: bool,
}

#[derive(Default, Serialize, Deserialize, Clone)]
struct Table {
    headers: Vec<String>,
    rows: Vec<Vec<String>>, // keep as string; typed views can be built atop
}

#[derive(Serialize, Deserialize, Clone, Copy, PartialEq, Eq)]
enum Language {
    #[serde(rename = "en")] 
    English,
    #[serde(rename = "cns")] 
    ChineseS,
    #[serde(rename = "cnt")] 
    ChineseT,
}

impl Default for Language {
    fn default() -> Self { Self::English }
}

impl AppState {
    fn new() -> Self { Self::default() }

    fn open_data(&mut self) {
        if let Some(file) = rfd::FileDialog::new()
            .add_filter("Data", &["csv", "xlsx"]) 
            .pick_file()
        {
            self.filename = Some(file.clone());
            match load_table(&file) {
                Ok(t) => {
                    self.raw_table = t;
                    self.status = format!("Loaded {} rows", self.raw_table.rows.len());
                }
                Err(e) => {
                    self.status = format!("Error: {e}");
                }
            }
        }
    }

    fn save_data(&mut self) {
        if self.raw_table.rows.is_empty() { return; }
        if let Some(path) = rfd::FileDialog::new()
            .set_file_name("output.csv")
            .save_file()
        {
            if let Err(e) = save_table_csv(&self.raw_table, &path) {
                self.status = format!("Save error: {e}");
            } else {
                self.status = format!("Saved to {:?}", path);
            }
        }
    }

    fn geochem_remove_loi(&mut self) {
        geochem::remove_loi_normalize(self);
    }
}

fn load_table(path: &PathBuf) -> anyhow::Result<Table> {
    let ext = path.extension().and_then(|s| s.to_str()).unwrap_or("").to_lowercase();
    if ext == "csv" {
        load_csv(path)
    } else if ext == "xlsx" {
        load_xlsx(path)
    } else {
        anyhow::bail!("Unsupported file format: {ext}")
    }
}

fn load_csv(path: &PathBuf) -> anyhow::Result<Table> {
    let mut rdr = csv::Reader::from_path(path)?;
    let headers = rdr.headers()?.iter().map(|s| s.to_string()).collect::<Vec<_>>();
    let mut rows = Vec::new();
    for r in rdr.records() {
        rows.push(r?.iter().map(|s| s.to_string()).collect());
    }
    Ok(Table { headers, rows })
}

fn load_xlsx(path: &PathBuf) -> anyhow::Result<Table> {
    use calamine::{open_workbook, Reader, Xlsx};
    let mut workbook: Xlsx<_> = open_workbook(path)?;
    let range = workbook
        .worksheet_range_at(0)
        .ok_or_else(|| anyhow::anyhow!("No first sheet"))??;
    let mut rows_iter = range.rows();
    let headers = rows_iter
        .next()
        .map(|r| r.iter().map(|c| c.to_string()).collect())
        .unwrap_or_else(|| Vec::new());
    let rows = rows_iter
        .map(|r| r.iter().map(|c| c.to_string()).collect())
        .collect();
    Ok(Table { headers, rows })
}

fn save_table_csv(table: &Table, path: &PathBuf) -> anyhow::Result<()> {
    let mut w = csv::Writer::from_path(path)?;
    if !table.headers.is_empty() { w.write_record(&table.headers)?; }
    for row in &table.rows { w.write_record(row)?; }
    w.flush()?;
    Ok(())
}

fn main() -> eframe::Result<()> {
    let native_options = eframe::NativeOptions::default();
    eframe::run_native(
        APP_TITLE,
        native_options,
        Box::new(|_cc| Box::new(GeoRusToolApp { state: AppState::new() })),
    )
}

struct GeoRusToolApp {
    state: AppState,
}

impl eframe::App for GeoRusToolApp {
    fn update(&mut self, ctx: &Context, _frame: &mut eframe::Frame) {
        TopBottomPanel::top("menu").show(ctx, |ui| {
            ui.horizontal_wrapped(|ui| {
                if ui.button("Open Data").clicked() { self.state.open_data(); }
                if ui.button("Load Geochemistry.csv").clicked() {
                    use std::path::PathBuf;
                    let p = PathBuf::from("Geochemistry.csv");
                    if p.exists() {
                        match load_table(&p) {
                            Ok(t) => { self.state.filename = Some(p.clone()); self.state.raw_table = t; self.state.status = format!("Loaded {} rows from Geochemistry.csv", self.state.raw_table.rows.len()); }
                            Err(e) => { self.state.status = format!("Load failed: {e}"); }
                        }
                    } else { self.state.status = "Geochemistry.csv not found in current directory".to_string(); }
                }
                if ui.button("Save Data").clicked() { self.state.save_data(); }
                if ui.button("Remove LOI").clicked() { self.state.geochem_remove_loi(); }
                ui.separator();
                ui.label("Geochemistry: TAS/Trace/REE/Pearce/Harker/CIPW/QAPF/Saccani/K2O-SiO2/Raman/Fluid/HarkerOld/TraceNew/ZrYSrTi/TiAl... (todo)");
                if ui.button("View K2O-SiO2").clicked() { self.state.k2o_view.is_open = true; }
                if ui.button("Export K2O-SiO2 PNG").clicked() {
                    if let Some(path) = rfd::FileDialog::new().set_file_name("k2o_sio2.png").save_file() {
                        if let Err(e) = geochem::export_k2o_sio2_png(&self.state, &path) { self.state.status = format!("Export error: {e}"); }
                        else { self.state.status = format!("Saved PNG to {:?}", path); }
                    }
                }
                if ui.button("TAS").clicked() { self.state.tas_view_open = true; }
                ui.label("TAS Mode:");
                ui.selectable_value(&mut self.state.tas_mode_is_volcanic, true, "VOL");
                ui.selectable_value(&mut self.state.tas_mode_is_volcanic, false, "PLT");
                if ui.button("Export TAS PNG").clicked() {
                    if let Some(path) = rfd::FileDialog::new().set_file_name("tas.png").save_file() {
                        if let Err(e) = geochem::export_tas_png(&self.state, &path) { self.state.status = format!("Export error: {e}"); } else { self.state.status = format!("Saved PNG to {:?}", path); }
                    }
                }
                if ui.button("Export TAS SVG").clicked() {
                    if let Some(path) = rfd::FileDialog::new().set_file_name("tas.svg").save_file() {
                        if let Err(e) = geochem::export_tas_svg(&self.state, &path) { self.state.status = format!("Export error: {e}"); } else { self.state.status = format!("Saved SVG to {:?}", path); }
                    }
                }

                if ui.button("REE").clicked() { self.state.ree_view_open = true; }
                ui.label("REE Standard:");
                egui::ComboBox::from_label("")
                    .selected_text(format!("{}", geochem::REE_STANDARD_NAMES.get(self.state.ree_standard_idx).copied().unwrap_or(geochem::REE_STANDARD_NAMES[0])))
                    .show_ui(ui, |ui| {
                        for (i, name) in geochem::REE_STANDARD_NAMES.iter().enumerate() {
                            if ui.selectable_label(self.state.ree_standard_idx==i, *name).clicked() { self.state.ree_standard_idx=i; }
                        }
                    });
                if ui.button("Export REE PNG").clicked() {
                    if let Some(path) = rfd::FileDialog::new().set_file_name("ree.png").save_file() {
                        if let Err(e) = geochem::export_ree_png(&self.state, &path) { self.state.status = format!("Export error: {e}"); } else { self.state.status = format!("Saved PNG to {:?}", path); }
                    }
                }
                if ui.button("Export REE SVG").clicked() {
                    if let Some(path) = rfd::FileDialog::new().set_file_name("ree.svg").save_file() {
                        if let Err(e) = geochem::export_ree_svg(&self.state, &path) { self.state.status = format!("Export error: {e}"); } else { self.state.status = format!("Saved SVG to {:?}", path); }
                    }
                }
                ui.separator();
                if ui.button("Pearson (4 views)").clicked() { self.state.pearson_view_open = true; }
                ui.menu_button("Pearson Export", |ui| {
                    if ui.button("Export PNG (Y+Nb, Rb)").clicked() {
                        if let Some(path) = rfd::FileDialog::new().set_file_name("pearson0.png").save_file() {
                            if let Err(e) = geochem::export_pearson_png(&self.state, &path, 0) { self.state.status = format!("Export error: {e}"); } else { self.state.status = format!("Saved PNG to {:?}", path); }
                        }
                    }
                    if ui.button("Export SVG (Y+Nb, Rb)").clicked() {
                        if let Some(path) = rfd::FileDialog::new().set_file_name("pearson0.svg").save_file() {
                            if let Err(e) = geochem::export_pearson_svg(&self.state, &path, 0) { self.state.status = format!("Export error: {e}"); } else { self.state.status = format!("Saved SVG to {:?}", path); }
                        }
                    }
                    ui.separator();
                    if ui.button("Export PNG (Yb+Ta, Rb)").clicked() {
                        if let Some(path) = rfd::FileDialog::new().set_file_name("pearson1.png").save_file() {
                            if let Err(e) = geochem::export_pearson_png(&self.state, &path, 1) { self.state.status = format!("Export error: {e}"); } else { self.state.status = format!("Saved PNG to {:?}", path); }
                        }
                    }
                    if ui.button("Export SVG (Yb+Ta, Rb)").clicked() {
                        if let Some(path) = rfd::FileDialog::new().set_file_name("pearson1.svg").save_file() {
                            if let Err(e) = geochem::export_pearson_svg(&self.state, &path, 1) { self.state.status = format!("Export error: {e}"); } else { self.state.status = format!("Saved SVG to {:?}", path); }
                        }
                    }
                    ui.separator();
                    if ui.button("Export PNG (Y, Nb)").clicked() {
                        if let Some(path) = rfd::FileDialog::new().set_file_name("pearson2.png").save_file() {
                            if let Err(e) = geochem::export_pearson_png(&self.state, &path, 2) { self.state.status = format!("Export error: {e}"); } else { self.state.status = format!("Saved PNG to {:?}", path); }
                        }
                    }
                    if ui.button("Export SVG (Y, Nb)").clicked() {
                        if let Some(path) = rfd::FileDialog::new().set_file_name("pearson2.svg").save_file() {
                            if let Err(e) = geochem::export_pearson_svg(&self.state, &path, 2) { self.state.status = format!("Export error: {e}"); } else { self.state.status = format!("Saved SVG to {:?}", path); }
                        }
                    }
                    ui.separator();
                    if ui.button("Export PNG (Yb, Ta)").clicked() {
                        if let Some(path) = rfd::FileDialog::new().set_file_name("pearson3.png").save_file() {
                            if let Err(e) = geochem::export_pearson_png(&self.state, &path, 3) { self.state.status = format!("Export error: {e}"); } else { self.state.status = format!("Saved PNG to {:?}", path); }
                        }
                    }
                    if ui.button("Export SVG (Yb, Ta)").clicked() {
                        if let Some(path) = rfd::FileDialog::new().set_file_name("pearson3.svg").save_file() {
                            if let Err(e) = geochem::export_pearson_svg(&self.state, &path, 3) { self.state.status = format!("Export error: {e}"); } else { self.state.status = format!("Saved SVG to {:?}", path); }
                        }
                    }
                    if ui.button("Export 4-in-1 PNG").clicked() {
                        if let Some(path) = rfd::FileDialog::new().set_file_name("pearson_4in1.png").save_file() {
                            if let Err(e) = geochem::export_pearson_4in1_png(&self.state, &path) { self.state.status = format!("Export error: {e}"); } else { self.state.status = format!("Saved PNG to {:?}", path); }
                        }
                    }
                    if ui.button("Export 4-in-1 SVG").clicked() {
                        if let Some(path) = rfd::FileDialog::new().set_file_name("pearson_4in1.svg").save_file() {
                            if let Err(e) = geochem::export_pearson_4in1_svg(&self.state, &path) { self.state.status = format!("Export error: {e}"); } else { self.state.status = format!("Saved SVG to {:?}", path); }
                        }
                    }
                });
                ui.separator();
                if ui.button("Ti/100-Zr-3Y").clicked() { geochem::show_tizry_plot(ui, &self.state); }
                if ui.button("Export TiZrY PNG").clicked() {
                    if let Some(path) = rfd::FileDialog::new().set_file_name("tizry.png").save_file() {
                        if let Err(e) = geochem::export_tizry_png(&self.state, &path) { self.state.status = format!("Export error: {e}"); } else { self.state.status = format!("Saved PNG to {:?}", path); }
                    }
                }
                ui.separator();
                if ui.button("Ab-Or-An").clicked() { geochem::show_aboran_plot(ui, &self.state); }
                if ui.button("Export Ab-Or-An PNG").clicked() {
                    if let Some(path) = rfd::FileDialog::new().set_file_name("aboran.png").save_file() {
                        if let Err(e) = geochem::export_aboran_png(&self.state, &path) { self.state.status = format!("Export error: {e}"); } else { self.state.status = format!("Saved PNG to {:?}", path); }
                    }
                }
                if ui.button("Export Ab-Or-An SVG").clicked() {
                    if let Some(path) = rfd::FileDialog::new().set_file_name("aboran.svg").save_file() {
                        if let Err(e) = geochem::export_aboran_svg(&self.state, &path) { self.state.status = format!("Export error: {e}"); } else { self.state.status = format!("Saved SVG to {:?}", path); }
                    }
                }
                if ui.button("Al-FeTi-Mg").clicked() { geochem::show_alfetimg_plot(ui, &self.state); }
                if ui.button("Export Al-FeTi-Mg PNG").clicked() {
                    if let Some(path) = rfd::FileDialog::new().set_file_name("alfetimg.png").save_file() {
                        if let Err(e) = geochem::export_alfetimg_png(&self.state, &path) { self.state.status = format!("Export error: {e}"); } else { self.state.status = format!("Saved PNG to {:?}", path); }
                    }
                }
                if ui.button("Export Al-FeTi-Mg SVG").clicked() {
                    if let Some(path) = rfd::FileDialog::new().set_file_name("alfetimg.svg").save_file() {
                        if let Err(e) = geochem::export_alfetimg_svg(&self.state, &path) { self.state.status = format!("Export error: {e}"); } else { self.state.status = format!("Saved SVG to {:?}", path); }
                    }
                }
                if ui.button("Export TiZrY SVG").clicked() {
                    if let Some(path) = rfd::FileDialog::new().set_file_name("tizry.svg").save_file() {
                        if let Err(e) = geochem::export_tizry_svg(&self.state, &path) { self.state.status = format!("Export error: {e}"); } else { self.state.status = format!("Saved SVG to {:?}", path); }
                    }
                }
                if ui.button("Export K2O-SiO2 SVG").clicked() {
                    if let Some(path) = rfd::FileDialog::new().set_file_name("k2o_sio2.svg").save_file() {
                        if let Err(e) = geochem::export_k2o_sio2_svg(&self.state, &path) { self.state.status = format!("Export error: {e}"); }
                        else { self.state.status = format!("Saved SVG to {:?}", path); }
                    }
                }
                ui.separator();
                ui.label("Structure: Stereo/Rose (todo)");
                ui.separator();
                ui.label("Sedimentary: QFL/QmFLt/Clastic/CIA (todo)");
                ui.separator();
                ui.label("Calculation: CIPW/QAPF/ZirconCe/ZirconTiTemp/RutileZrTemp/Isotope (todo)");
                if ui.button("Compute CIPW").clicked() { geochem::compute_cipw_and_store(&mut self.state); self.state.cipw_done = true; }
                if ui.button("QAPF").clicked() { self.state.qapf_view_open = true; }
                if ui.button("Export CIPW CSV").clicked() {
                    if let Some(path) = rfd::FileDialog::new().set_file_name("cipw.csv").save_file() {
                        if let Err(e) = geochem::export_cipw_csv(&self.state, &path) { self.state.status = format!("Export error: {e}"); } else { self.state.status = format!("Saved CSV to {:?}", path); }
                    }
                }
                if ui.button("Export QAPF PNG").clicked() {
                    if let Some(path) = rfd::FileDialog::new().set_file_name("qapf.png").save_file() {
                        if let Err(e) = geochem::export_qapf_png(&self.state, &path) { self.state.status = format!("Export error: {e}"); } else { self.state.status = format!("Saved PNG to {:?}", path); }
                    }
                }
                if ui.button("Export QAPF SVG").clicked() {
                    if let Some(path) = rfd::FileDialog::new().set_file_name("qapf.svg").save_file() {
                        if let Err(e) = geochem::export_qapf_svg(&self.state, &path) { self.state.status = format!("Export error: {e}"); } else { self.state.status = format!("Saved SVG to {:?}", path); }
                    }
                }
                ui.separator();
                ui.label("Additional: XY/XYZ/Cluster/Multi/Dist/Sta/TwoD/Grey/Hist/Pie/Bar (todo)");
                ui.separator();
                ui.label("ML: DT/FA/LDA/PCA/MLP/GAN (todo)");
            });
        });

        CentralPanel::default().show(ctx, |ui| {
            ui.heading(APP_TITLE);
            ui.separator();
            if let Some(name) = self.state.filename.as_ref().and_then(|p| p.file_name()).and_then(|s| s.to_str()) {
                ui.label(format!("File: {}", name));
            }
            ui.label(&self.state.status);
            ui.separator();

            let num_cols = {
                let mut n = self.state.raw_table.headers.len();
                if n == 0 {
                    n = self.state.raw_table.rows.first().map(|r| r.len()).unwrap_or(0);
                }
                n.max(1)
            };

            let mut table = egui_extras::TableBuilder::new(ui)
                .striped(true)
                .resizable(true);
            for _ in 0..num_cols { table = table.column(egui_extras::Column::auto()); }

            table
                .header(20.0, |mut header| {
                    if self.state.raw_table.headers.is_empty() {
                        for i in 0..num_cols { header.col(|ui| { ui.label(format!("Col {}", i+1)); }); }
                    } else {
                        for h in &self.state.raw_table.headers { header.col(|ui| { ui.label(h); }); }
                    }
                })
                .body(|mut body| {
                    for row in &self.state.raw_table.rows {
                        body.row(18.0, |mut r| {
                            for i in 0..num_cols {
                                let cell = row.get(i).map(|s| s.as_str()).unwrap_or("");
                                r.col(|ui| { ui.label(cell); });
                            }
                        });
                    }
                });
        });

        // Floating panels
        if self.state.k2o_view.is_open {
            // Take snapshot before borrowing mutably for window open flag
            let state_snapshot = self.state.clone();
            let mut open_flag = self.state.k2o_view.is_open;
            egui::Window::new("K2O-SiO2").open(&mut open_flag).show(ctx, |ui| {
                geochem::show_k2o_sio2_plot(ui, &state_snapshot);
            });
            self.state.k2o_view.is_open = open_flag;
        }

        if self.state.tas_view_open {
            let state_snapshot = self.state.clone();
            let mut open_flag = self.state.tas_view_open;
            egui::Window::new("TAS").open(&mut open_flag).show(ctx, |ui| {
                geochem::show_tas_plot(ui, &state_snapshot);
            });
            self.state.tas_view_open = open_flag;
        }

        if self.state.ree_view_open {
            let state_snapshot = self.state.clone();
            let mut open_flag = self.state.ree_view_open;
            egui::Window::new("REE").open(&mut open_flag).show(ctx, |ui| {
                geochem::show_ree_plot(ui, &state_snapshot);
            });
            self.state.ree_view_open = open_flag;
        }

        if self.state.pearson_view_open {
            let state_snapshot = self.state.clone();
            let mut open_flag = self.state.pearson_view_open;
            egui::Window::new("Pearson (Pearce) 4 views").open(&mut open_flag).show(ctx, |ui| {
                geochem::show_pearson_grid(ui, &state_snapshot);
            });
            self.state.pearson_view_open = open_flag;
        }

        if self.state.qapf_view_open {
            let state_snapshot = self.state.clone();
            let mut open_flag = self.state.qapf_view_open;
            egui::Window::new("QAPF").open(&mut open_flag).show(ctx, |ui| {
                geochem::show_qapf_plot(ui, &state_snapshot);
            });
            self.state.qapf_view_open = open_flag;
        }
    }
}


