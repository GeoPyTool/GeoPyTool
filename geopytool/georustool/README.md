GeoRusTool (Rust reimplementation of GeoPyTool)

This crate is a Rust desktop application skeleton intended to fully re-implement the Python app geopytool.

Status: skeleton ready, CSV/XLSX load/save, UI framework, and feature placeholders mapped 1:1 to the Python menus.

Build & Run (Windows)

- Install Rust (stable): https://rustup.rs
- Build: cargo build --release
- Run: cargo run

Tech choices

- UI: eframe/egui
- File dialogs: rfd
- CSV: csv
- Excel: calamine (XLSX)

Feature mapping checklist

- Data File
  - Open Data: implemented (CSV/XLSX)
  - Save Data: implemented (CSV)
  - Set/Fill/Combine/Flatten/Trans/ReFormat/Clear: TODO
- Geochemistry
  - Remove LOI: TODO
  - Auto: TODO (multi-plot PDF report)
  - TAS, Trace, REE, Pearce, Harker, CIPW, QAPF, Saccani, K2O-SiO2, Raman, Fluid Inclusion, Harker Classical, TraceNew, ZrYSrTi, TiAlCaMgMnKNaSi: TODO
- Structure
  - Stereo, Rose: TODO
- Sedimentary
  - QFL, QmFLt, Clastic, CIA: TODO
- Calculation
  - ZirconCe, ZirconCeOld, ZirconTiTemp, RutileZrTemp, Rb-Sr, Sm-Nd, K-Ar IsoTope: TODO
- Additional
  - XY, XYZ, Cluster, MultiDimension, Dist, Statistics, ThreeD, TwoD, TwoD Grey, Histogram, Pie, Bar: TODO
- MachineLearn
  - DT, FA, LDA, PCA, MLP, GAN: TODO
- Language/Help
  - i18n switching, forum/github links, version check: TODO

Code structure

- src/main.rs: app entry, menu, table view, file open/save
- src/features.rs: placeholders for all features, grouped by domain

Porting notes

- Replace each placeholder in features.rs with real logic.
- For plotting, prefer egui_plot or render to images and display in egui.
- Keep data model strongly typed; add typed views atop Table when porting each function.


