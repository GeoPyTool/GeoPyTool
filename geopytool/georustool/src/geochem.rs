use egui::{Color32, Ui, ColorImage, TextureHandle, TextureOptions, Image};

// Helper function to render plotters plot to egui texture
fn render_plotters_to_texture<F>(
    ctx: &egui::Context,
    plot_fn: F,
    width: u32,
    height: u32,
) -> Option<egui::TextureHandle>
where
    F: FnOnce(DrawingArea<BitMapBackend<'_>, Shift>) -> anyhow::Result<()>,
{
    use plotters::prelude::*;

    // Create a buffer to hold the image data (RGB)
    let mut buffer_rgb = vec![0; (width * height * 3) as usize];

    {
        let root = BitMapBackend::with_buffer(&mut buffer_rgb, (width, height)).into_drawing_area();
        if let Err(e) = plot_fn(root) {
            eprintln!("Failed to render plot: {:?}", e);
            return None;
        }
    }

    // Convert RGB to RGBA
    let mut buffer_rgba = vec![0; (width * height * 4) as usize];
    for i in 0..(width * height) as usize {
        buffer_rgba[i*4] = buffer_rgb[i*3];
        buffer_rgba[i*4+1] = buffer_rgb[i*3+1];
        buffer_rgba[i*4+2] = buffer_rgb[i*3+2];
        buffer_rgba[i*4+3] = 255; // opaque
    }

    // Convert the buffer to an egui ColorImage
    let color_image = egui::ColorImage::from_rgba_unmultiplied(
        [width as usize, height as usize],
        &buffer_rgba,
    );

    // Load the texture
    let texture = ctx.load_texture(
        "plotters_plot",
        color_image,
        egui::TextureOptions::default(),
    );

    Some(texture)
}
use egui_plot::{Line, Plot, PlotPoints, Points, Legend, MarkerShape, Text as PlotText, PlotPoint};
use serde::{Deserialize, Serialize};
use std::collections::HashMap;
use std::fs;

use crate::AppState;
use plotters::prelude::*;
use plotters::coord::Shift;

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
enum UnitType { WtPercent, Ppm, Unknown }

#[derive(Default)]
struct HeaderResolver {
    name_to_index: std::collections::HashMap<String, usize>,
    units_by_index: Vec<UnitType>,
}

fn build_resolver(headers: &[String]) -> HeaderResolver {
    let mut map = std::collections::HashMap::new();
    let mut units = Vec::with_capacity(headers.len());
    for (i, h) in headers.iter().enumerate() {
        // unit detection
        let hl = h.to_lowercase();
        let unit = if hl.contains("ppm") || hl.contains("mg/kg") || hl.contains("mgkg") || hl.contains("μg/g") || hl.contains("ug/g") {
            UnitType::Ppm
        } else if hl.contains("wt%") || hl.contains("%") || hl.contains("质量百分比") {
            UnitType::WtPercent
        } else {
            UnitType::Unknown
        };
        units.push(unit);

        // map canonical names and aliases
        let canonical = canonicalize_name(h);
        map.entry(canonical).or_insert(i);

        // also register alias tokens if present
        for alias in name_aliases(h) { map.entry(alias).or_insert(i); }
    }
    HeaderResolver { name_to_index: map, units_by_index: units }
}

fn canonicalize_name(s: &str) -> String {
    let s = s.trim();
    let mut out = String::with_capacity(s.len());
    for ch in s.chars() {
        // skip spaces and common separators/parentheses marks, both ASCII and CJK variants
        if ch.is_whitespace() { continue; }
        match ch {
            '(' | ')' | '（' | '）' | '[' | ']' | '{' | '}' | '%' | '/' | '\\' | '-' | '_' | ':' => {},
            _ => out.push(ch.to_ascii_lowercase()),
        }
    }
    out
}

fn name_aliases(s: &str) -> Vec<String> {
    let c = canonicalize_name(s);
    // base token without units words
    let mut base = c.replace("wt", "").replace("ppm", "");
    // simple Chinese -> token aliases for majors used here
    let mut aliases = Vec::new();
    let zh_to_en = [
        ("二氧化硅", "sio2"), ("氧化钾", "k2o"), ("氧化钠", "na2o"), ("三氧化二铝", "al2o3"), ("氧化铝", "al2o3"),
        ("二氧化钛", "tio2"), ("三氧化二铁", "fe2o3"), ("一氧化铁", "feo"), ("氧化镁", "mgo"), ("氧化钙", "cao"),
        ("氧化锰", "mno"), ("五氧化二磷", "p2o5"), ("总铁", "tfe2o3"), ("总铁(二价)", "tfeo"), ("总量", "total"),
        ("灼减", "loi"), ("亏损", "loi"), ("总计", "total"), ("全部", "all"), ("全部含量", "all"),
    ];
    for (zh, en) in zh_to_en { if c.contains(zh) { aliases.push(en.to_string()); } }
    if aliases.is_empty() { aliases.push(base); }
    aliases
}

fn is_major_oxide_token(token: &str) -> bool {
    matches!(token,
        "sio2"|"al2o3"|"tio2"|"feo"|"fe2o3"|"mgo"|"cao"|"na2o"|"k2o"|"p2o5"|"mno"|"tfe2o3"|"tfeo"|"total"|"all"|"loi"
    )
}

impl HeaderResolver {
    fn find_index(&self, token: &str) -> Option<usize> {
        let key = canonicalize_name(token);
        if let Some(idx) = self.name_to_index.get(&key) { return Some(*idx); }
        None
    }

    fn parse_value(&self, row: &[String], idx: usize, expect_major_wt: bool) -> Option<f64> {
        let raw = row.get(idx)?.trim();
        if raw.is_empty() { return None; }
        // strip trailing % if any
        let raw = raw.strip_suffix('%').unwrap_or(raw);
        let mut v = raw.parse::<f64>().ok()?;
        let unit = self.units_by_index.get(idx).copied().unwrap_or(UnitType::Unknown);
        match unit {
            UnitType::WtPercent => {}
            UnitType::Ppm => {
                if expect_major_wt { v = v / 10000.0; }
            }
            UnitType::Unknown => {
                // default: majors as wt%, traces as ppm
                if expect_major_wt { /* keep */ } else { /* keep */ }
            }
        }
        Some(v)
    }
}

#[derive(Default, Serialize, Deserialize, Clone)]
pub struct K2OSiO2ViewState {
    pub is_open: bool,
}

#[derive(Default, Serialize, Deserialize, Clone)]
pub struct TASViewState { pub is_open: bool }
#[derive(Default, Serialize, Deserialize, Clone)]
pub struct REEViewState { pub is_open: bool }

pub fn remove_loi_normalize(state: &mut AppState) {
    if state.raw_table.rows.is_empty() { return; }
    let headers = &state.raw_table.headers;
    let resolver = build_resolver(headers);

    let loi_aliases = ["LOI", "loi", "Loi", "灼减", "亏损"]; 
    let total_aliases = ["Total", "total", "TOTAL", "ALL", "All", "all", "总量", "总计", "全部"]; 
    let majors = ["Al2O3","MgO","FeO","Fe2O3","CaO","Na2O","K2O","TiO2","P2O5","SiO2","TFe2O3","MnO","TFeO"];

    for row in &mut state.raw_table.rows {
        // find total first
        let mut de_loi: Option<f64> = None;
        for a in &total_aliases {
            if let Some(idx) = resolver.find_index(a) {
                de_loi = resolver.parse_value(row, idx, true);
                if de_loi.is_some() { break; }
            }
        }

        if de_loi.is_none() {
            // try LOI
            for a in &loi_aliases {
                if let Some(idx) = resolver.find_index(a) {
                    if let Some(loi) = resolver.parse_value(row, idx, true) {
                        de_loi = Some(100.0 - loi);
                        break;
                    }
                }
            }
        }

        if let Some(norm) = de_loi {
            if norm > 0.0 {
                for m in &majors {
                    if let Some(idx) = resolver.find_index(m) {
                        if let Some(v) = resolver.parse_value(row, idx, true) {
                            let new_v = 100.0 * v / norm;
                            row[idx] = format_num(new_v);
                        }
                    }
                }
                continue;
            }
        }

        // fallback: sum majors and normalize if sum!=100
        let mut sum = 0.0;
        let mut present_indices = Vec::new();
        for m in &majors {
            if let Some(idx) = resolver.find_index(m) {
                if let Some(v) = resolver.parse_value(row, idx, true) {
                    sum += v; present_indices.push((idx, v));
                }
            }
        }
        if sum > 0.0 && (sum - 100.0).abs() > 1e-6 {
            for (idx, v) in present_indices { row[idx] = format_num(100.0 * v / sum); }
        }
    }

    state.status = "Remove LOI done".to_string();
}

fn format_num(v: f64) -> String { format!("{:.6}", v) }

pub fn show_k2o_sio2_plot(ui: &mut Ui, state: &crate::AppState) {
    // Extract data columns
    let headers = &state.raw_table.headers;
    let resolver = build_resolver(headers);
    let idx_sio2 = resolver.find_index("SiO2");
    let idx_k2o = resolver.find_index("K2O");
    if idx_sio2.is_none() || idx_k2o.is_none() {
        ui.label("Need columns SiO2 and K2O");
        return;
    }
    let (ix, iy) = (idx_sio2.unwrap(), idx_k2o.unwrap());

    // Group by label/color
    let idx_label = resolver.find_index("Label");
    let idx_color = resolver.find_index("Color");
    use std::collections::BTreeMap;
    let mut groups: BTreeMap<String, Vec<[f64;2]>> = BTreeMap::new();
        let mut group_color: BTreeMap<String, Color32> = BTreeMap::new();
    for r in &state.raw_table.rows {
        if let (Some(x), Some(y)) = (resolver.parse_value(r, ix, true), resolver.parse_value(r, iy, true)) {
            let label = idx_label.and_then(|i| r.get(i)).cloned().unwrap_or_else(|| "Group".to_string());
            groups.entry(label.clone()).or_default().push([x,y]);
            if let Some(i) = idx_color { if let Some(cstr) = r.get(i) { if let Some(c) = parse_egui_color(cstr) { group_color.entry(label.clone()).or_insert(c); } } }
        }
    }

    // Lines from Python logic
    let k1 = (2.9 - 1.2) / (68.0 - 48.0);
    let k2 = (1.2 - 0.3) / (68.0 - 48.0);
    let y1 = |x: f64| 1.2 + (x - 48.0) * k1;
    let y2 = |x: f64| 0.3 + (x - 48.0) * k2;

    // Build line samples
    let mut l1 = Vec::new();
    let mut l2 = Vec::new();
    for x in (45..=85).step_by(1) { let xf = x as f64; l1.push([xf, y1(xf)]); l2.push([xf, y2(xf)]); }

    Plot::new("k2o_sio2").include_x(30.0).include_x(90.0).include_y(0.0).include_y(6.0).view_aspect(1.6).legend(Legend::default()).show(ui, |plot_ui| {
        plot_ui.line(Line::new(l1).color(Color32::from_rgb(200, 0, 0)).name("High/Med boundary"));
        plot_ui.line(Line::new(l2).color(Color32::from_rgb(0, 120, 200)).name("Med/Low boundary"));
        let palette = egui_palette();
        let mut idx = 0usize;
        for (label, pts) in groups {
            let color = group_color.get(&label).cloned().unwrap_or_else(|| { let c = palette[idx % palette.len()]; idx+=1; c });
            let pp: PlotPoints = pts.into();
            let shape = match idx % 4 { 0=>MarkerShape::Circle,1=>MarkerShape::Square,2=>MarkerShape::Diamond, _=>MarkerShape::Cross};
            plot_ui.points(Points::new(pp).color(color).radius(2.5).shape(shape).name(label));
        }
    });
}

fn parse_egui_color(name: &str) -> Option<Color32> {
    let s = name.trim().to_ascii_lowercase();
    let named = match s.as_str() {
        "red"=>Some(Color32::from_rgb(220,0,0)),
        "blue"=>Some(Color32::from_rgb(0,120,220)),
        "green"=>Some(Color32::from_rgb(0,160,0)),
        "black"=>Some(Color32::BLACK),
        "white"=>Some(Color32::WHITE),
        "gray"|"grey"=>Some(Color32::from_gray(160)),
        "orange"=>Some(Color32::from_rgb(255,165,0)),
        "purple"=>Some(Color32::from_rgb(160,32,240)),
        "cyan"=>Some(Color32::from_rgb(0,180,180)),
        "magenta"=>Some(Color32::from_rgb(220,0,220)),
        "yellow"=>Some(Color32::from_rgb(240,200,0)),
        _=>None,
    };
    if named.is_some() { return named; }
    if let Some(hex) = s.strip_prefix('#') { return parse_hex_egui(hex); }
    None
}

fn parse_hex_egui(hex: &str) -> Option<Color32> {
    if hex.len()==6 {
        let r = u8::from_str_radix(&hex[0..2],16).ok()?;
        let g = u8::from_str_radix(&hex[2..4],16).ok()?;
        let b = u8::from_str_radix(&hex[4..6],16).ok()?;
        Some(Color32::from_rgb(r,g,b))
    } else { None }
}

fn egui_palette() -> Vec<Color32> {
    vec![
        Color32::from_rgb(0x1f,0x77,0xb4),
        Color32::from_rgb(0xff,0x7f,0x0e),
        Color32::from_rgb(0x2c,0xa0,0x2c),
        Color32::from_rgb(0xd6,0x27,0x28),
        Color32::from_rgb(0x94,0x67,0xbd),
        Color32::from_rgb(0x8c,0x56,0x4b),
        Color32::from_rgb(0xe3,0x77,0xc2),
        Color32::from_rgb(0x7f,0x7f,0x7f),
        Color32::from_rgb(0xbc,0xbd,0x22),
        Color32::from_rgb(0x17,0xbe,0xcf),
    ]
}

fn parse_plotters_color(name: &str) -> Option<RGBColor> {
    let s = name.trim().to_ascii_lowercase();
    let named = match s.as_str() {
        "red"=>Some(RED),
        "blue"=>Some(BLUE),
        "green"=>Some(GREEN),
        "black"=>Some(BLACK),
        "white"=>Some(WHITE),
        "gray"|"grey"=>Some(RGBColor(160,160,160)),
        "orange"=>Some(RGBColor(255,165,0)),
        "purple"=>Some(RGBColor(160,32,240)),
        "cyan"=>Some(CYAN),
        "magenta"=>Some(MAGENTA),
        "yellow"=>Some(YELLOW),
        _=>None,
    };
    if let Some(c) = named { return Some(c); }
    if let Some(hex) = s.strip_prefix('#') { return parse_hex_plotters(hex); }
    None
}

fn parse_hex_plotters(hex: &str) -> Option<RGBColor> {
    if hex.len()==6 {
        let r = u8::from_str_radix(&hex[0..2],16).ok()?;
        let g = u8::from_str_radix(&hex[2..4],16).ok()?;
        let b = u8::from_str_radix(&hex[4..6],16).ok()?;
        Some(RGBColor(r,g,b))
    } else { None }
}

fn plotters_palette() -> Vec<RGBColor> {
    vec![
        RGBColor(31,119,180), RGBColor(255,127,14), RGBColor(44,160,44), RGBColor(214,39,40),
        RGBColor(148,103,189), RGBColor(140,86,75), RGBColor(227,119,194), RGBColor(127,127,127),
        RGBColor(188,189,34), RGBColor(23,190,207)
    ]
}

#[derive(Deserialize)]
struct TasJson {
    coords: HashMap<String, Vec<[f64;2]>>,
    #[serde(rename = "Volcanic", default)]
    volcanic: HashMap<String, String>,
    #[serde(rename = "Plutonic", default)]
    plutonic: HashMap<String, String>,
}

fn load_tas_json() -> anyhow::Result<TasJson> {
    let s = fs::read_to_string("src/TAS.json")?;
    let v: TasJson = serde_json::from_str(&s)?;
    Ok(v)
}

fn tas_regions() -> Vec<(String, (String, Vec<[f64;2]>))> {
    if let Ok(js) = load_tas_json() {
        let mut v = Vec::new();
        for (abbr, poly) in js.coords {
            let full = js.volcanic.get(&abbr).or_else(|| js.plutonic.get(&abbr)).cloned().unwrap_or(abbr.clone());
            v.push((abbr, (full, poly)));
        }
        v
    } else { Vec::new() }
}

fn classify_tas(x_sio2: f64, y_alk: f64) -> Option<&'static str> {
    let regions = tas_regions();
    for (abbr, (_full, poly)) in regions {
        if point_in_polygon(x_sio2, y_alk, &poly) { return Some(Box::leak(abbr.into_boxed_str())); }
    }
    None
}

fn point_in_polygon(x: f64, y: f64, poly: &Vec<[f64;2]>) -> bool {
    // Ray casting algorithm
    let mut inside = false;
    let n = poly.len();
    if n < 3 { return false; }
    let mut j = n - 1;
    for i in 0..n {
        let xi = poly[i][0];
        let yi = poly[i][1];
        let xj = poly[j][0];
        let yj = poly[j][1];
        let intersect = ((yi > y) != (yj > y)) && (x < (xj - xi) * (y - yi) / ((yj - yi).max(1e-12)) + xi);
        if intersect { inside = !inside; }
        j = i;
    }
    inside
}

pub const REE_STANDARD_NAMES: [&str; 6] = [
    "C1 Chondrite Sun and McDonough,1989",
    "Chondrite Taylor and McLennan,1985",
    "Chondrite Haskin et al.,1966",
    "Chondrite Nakamura,1977",
    "MORB Sun and McDonough,1989",
    "UCC_Rudnick & Gao2003",
];

// ---------------- Pearson (XY, log-log) ----------------
#[derive(Deserialize)]
struct PearsonSet {
    #[serde(rename = "BaseLines")] baselines: Vec<Vec<[f64;2]>>,
    #[serde(rename = "xLabel")] xlabel: String,
    #[serde(rename = "yLabel")] ylabel: String,
    #[serde(rename = "Labels")] labels: Vec<String>,
    #[serde(rename = "LabelsLocations")] label_locs: Vec<[f64;2]>,
    #[serde(rename = "title", default = "default_title")]
    title: String,
}

fn default_title() -> String {
    "Pearson Diagram".to_string()
}

#[derive(Deserialize)]
struct PearsonJson {
    #[serde(rename = "coords0")] c0: PearsonSet,
    #[serde(rename = "coords1")] c1: PearsonSet,
    #[serde(rename = "coords2")] c2: PearsonSet,
    #[serde(rename = "coords3")] c3: PearsonSet,
}

fn load_pearson_json() -> anyhow::Result<PearsonJson> {
    let s = fs::read_to_string("src/Pearson.json")?;
    Ok(serde_json::from_str(&s)?)
}

fn pearson_variant(idx: usize) -> anyhow::Result<PearsonSet> {
    let js = load_pearson_json()?;
    Ok(match idx { 0=>js.c0, 1=>js.c1, 2=>js.c2, _=>js.c3 })
}

fn pearson_xy_for_row(resolver: &HeaderResolver, row: &[String], variant: usize) -> Option<(f64,f64)> {
    // Compute raw values (ppm). Return log10 if >0 for both.
    let get = |name: &str| resolver.find_index(name).and_then(|i| resolver.parse_value(row, i, false));
    let (x_raw, y_raw) = match variant {
        0 => { // x = Y+Nb, y = Rb
            let x = get("Y").unwrap_or(0.0) + get("Nb").unwrap_or(0.0);
            let y = get("Rb")?; (x, y)
        }
        1 => { // x = Yb+Ta, y = Rb
            let x = get("Yb").unwrap_or(0.0) + get("Ta").unwrap_or(0.0);
            let y = get("Rb")?; (x, y)
        }
        2 => { // x = Y, y = Nb
            (get("Y")?, get("Nb")?)
        }
        _ => { // 3: x = Yb, y = Ta
            (get("Yb")?, get("Ta")?)
        }
    };
    if x_raw > 0.0 && y_raw > 0.0 {
        Some((x_raw.log10(), y_raw.log10()))
    } else { None }
}

pub fn show_pearson_plot(ui: &mut Ui, state: &crate::AppState, variant: usize) {
    let headers = &state.raw_table.headers;
    let resolver = build_resolver(headers);
    let Ok(set) = pearson_variant(variant) else { ui.label("Missing Pearson.json"); return; };
    use std::collections::BTreeMap;
    let mut groups: BTreeMap<String, Vec<[f64;2]>> = BTreeMap::new();
    let mut group_color: BTreeMap<String, Color32> = BTreeMap::new();
    let idx_label = resolver.find_index("Label");
    let idx_color = resolver.find_index("Color");
    for r in &state.raw_table.rows {
        if let Some((x,y)) = pearson_xy_for_row(&resolver, r, variant) {
            let label = idx_label.and_then(|i| r.get(i)).cloned().unwrap_or_else(|| "Group".to_string());
            groups.entry(label.clone()).or_default().push([x,y]);
            if let Some(i) = idx_color { if let Some(cstr) = r.get(i) { if let Some(c) = parse_egui_color(cstr) { group_color.entry(label.clone()).or_insert(c); } } }
        }
    }
    // axis bounds from data and baselines
    let mut minx = f64::INFINITY; let mut maxx = f64::NEG_INFINITY;
    let mut miny = f64::INFINITY; let mut maxy = f64::NEG_INFINITY;
    for (_, pts) in &groups { for p in pts { minx = minx.min(p[0]); maxx = maxx.max(p[0]); miny = miny.min(p[1]); maxy = maxy.max(p[1]); } }
    for seg in &set.baselines { for p in seg { let x=p[0].log10(); let y=p[1].log10(); minx=minx.min(x); maxx=maxx.max(x); miny=miny.min(y); maxy=maxy.max(y); } }
    if !minx.is_finite() { minx = 0.0; maxx = 3.0; miny = 0.0; maxy = 3.0; }

    let plot_id = format!("pearson_{}", variant);
    Plot::new(plot_id)
        .view_aspect(1.0)
        .include_x(minx)
        .include_x(maxx)
        .include_y(miny)
        .include_y(maxy)
        .legend(Legend::default())
        .x_axis_label(set.xlabel.clone())
        .y_axis_label(set.ylabel.clone())
        .show(ui, |plot_ui| {
        // draw baselines
        for seg in &set.baselines {
            let line_pts: Vec<[f64;2]> = seg.iter().map(|p| [p[0].log10(), p[1].log10()]).collect();
            plot_ui.line(Line::new(line_pts).color(Color32::from_gray(120)));
        }
        // region labels at provided log locations
        for (i, lab) in set.labels.iter().enumerate() {
            if let Some(pos) = set.label_locs.get(i) {
                plot_ui.text(PlotText::new(PlotPoint::new(pos[0], pos[1]), lab.as_str()));
            }
        }
        // draw points
        let palette = egui_palette();
        let mut idx = 0usize;
        for (label, pts) in groups {
            let color = group_color.get(&label).cloned().unwrap_or_else(|| { let c = palette[idx % palette.len()]; idx+=1; c });
            let pp: PlotPoints = pts.into();
            plot_ui.points(Points::new(pp).color(color).radius(2.5).name(label));
        }
    });
}

pub fn show_pearson_plot_sized(ui: &mut Ui, state: &crate::AppState, variant: usize, side: f32) {
    let ctx = ui.ctx().clone();
    
    // 创建plotters绘制函数
    let plot_fn = |root: DrawingArea<BitMapBackend<'_>, Shift>| {
        export_pearson_with_area(state, root, variant)
    };
    
    // 计算渲染尺寸
    let width = (side * ui.ctx().pixels_per_point()) as u32;
    let height = (side * ui.ctx().pixels_per_point()) as u32;
    
    // 渲染图表为纹理
    if let Some(texture) = render_plotters_to_texture(&ctx, plot_fn, width, height) {
        // 在egui中显示纹理
        let image = Image::new(egui::load::SizedTexture::from_handle(&texture))  // 修复了类型转换
            .fit_to_original_size(1.0)
            .maintain_aspect_ratio(true);
        
        ui.allocate_ui_with_layout(
            egui::vec2(side, side),
            egui::Layout::top_down(egui::Align::Min),
            |sub_ui| {
                sub_ui.add(image);
            },
        );
    } else {
        ui.label("Failed to render Pearson plot");
    }
}


pub fn show_pearson_grid(ui: &mut Ui, state: &crate::AppState) {
    let avail = ui.available_size();
    
    // 定义边距和间距
    let margin = 10.0;
    let spacing = 5.0;
    
    // 计算可用于子图的总空间（减去边距和间距）
    let usable_width = avail.x - 2.0 * margin - spacing;
    let usable_height = avail.y - 2.0 * margin - spacing;
    
    // 计算每个子图的最大尺寸（确保不超过可用空间的一半）
    let max_side_width = usable_width / 2.0;
    let max_side_height = usable_height / 2.0;
    let side = max_side_width.min(max_side_height).max(50.0); // 设置最小尺寸为50.0
    
    // 添加外边距
    ui.add_space(margin);
    ui.horizontal(|row| {
        row.add_space(margin);
        show_pearson_plot_sized(row, state, 0, side);
        row.add_space(spacing);
        show_pearson_plot_sized(row, state, 1, side);
        row.add_space(margin);
    });
    ui.add_space(spacing);
    ui.horizontal(|row| {
        row.add_space(margin);
        show_pearson_plot_sized(row, state, 2, side);
        row.add_space(spacing);
        show_pearson_plot_sized(row, state, 3, side);
        row.add_space(margin);
    });
    ui.add_space(margin);
}

pub fn export_pearson_png(state: &crate::AppState, path: &std::path::Path, variant: usize) -> anyhow::Result<()> {
    let root: DrawingArea<BitMapBackend<'_>, _> = BitMapBackend::new(path.to_str().unwrap(), (1200, 800)).into_drawing_area();
    export_pearson_with_area(state, root, variant)
}
pub fn export_pearson_svg(state: &crate::AppState, path: &std::path::Path, variant: usize) -> anyhow::Result<()> {
    let root: DrawingArea<SVGBackend<'_>, _> = SVGBackend::new(path.to_str().unwrap(), (1200, 800)).into_drawing_area();
    export_pearson_with_area(state, root, variant)
}

pub fn export_pearson_4in1_png(state: &crate::AppState, path: &std::path::Path) -> anyhow::Result<()> {
    let root: DrawingArea<BitMapBackend<'_>, _> = BitMapBackend::new(path.to_str().unwrap(), (1600, 1600)).into_drawing_area();
    export_pearson_4in1_with_area(state, root)
}
pub fn export_pearson_4in1_svg(state: &crate::AppState, path: &std::path::Path) -> anyhow::Result<()> {
    let root: DrawingArea<SVGBackend<'_>, _> = SVGBackend::new(path.to_str().unwrap(), (1600, 1600)).into_drawing_area();
    export_pearson_4in1_with_area(state, root)
}

fn export_pearson_with_area<B: DrawingBackend>(state: &crate::AppState, root: DrawingArea<B, Shift>, variant: usize) -> anyhow::Result<()>
where <B as DrawingBackend>::ErrorType: 'static {
    root.fill(&WHITE)?;
    let title_font = ("Microsoft YaHei, Arial, SimHei, DejaVu Sans", 28).into_font();
    let axis_font = ("Microsoft YaHei, Arial, SimHei, DejaVu Sans", 14).into_font();
    let legend_font = ("Microsoft YaHei, Arial, SimHei, DejaVu Sans", 14).into_font();
    let set = pearson_variant(variant)?;
    // Gather points and ranges
    let headers = &state.raw_table.headers; let resolver = build_resolver(headers);
    use std::collections::BTreeMap; let idx_label = resolver.find_index("Label"); let idx_color = resolver.find_index("Color");
    let mut groups: BTreeMap<String, Vec<(f64,f64)>> = BTreeMap::new(); let mut gcolors: BTreeMap<String, RGBColor> = BTreeMap::new();
    let palette = plotters_palette(); let mut n = 0usize;
    let mut minx = f64::INFINITY; let mut maxx = f64::NEG_INFINITY; let mut miny = f64::INFINITY; let mut maxy = f64::NEG_INFINITY;
    for r in &state.raw_table.rows { if let Some((x,y)) = pearson_xy_for_row(&resolver, r, variant) {
        let label = idx_label.and_then(|i| r.get(i)).cloned().unwrap_or_else(|| "Group".to_string()); groups.entry(label.clone()).or_default().push((x,y));
        if let Some(i) = idx_color { if let Some(cstr) = r.get(i) { if let Some(c) = parse_plotters_color(cstr) { gcolors.entry(label.clone()).or_insert(c); } } }
        if !gcolors.contains_key(&label) { gcolors.insert(label.clone(), palette[n % palette.len()].clone()); n+=1; }
        minx=minx.min(x); maxx=maxx.max(x); miny=miny.min(y); maxy=maxy.max(y);
    }}
    for seg in &set.baselines { for p in seg { let x=p[0].log10(); let y=p[1].log10(); minx=minx.min(x); maxx=maxx.max(x); miny=miny.min(y); maxy=maxy.max(y); } }
    if !minx.is_finite() { minx=0.0; maxx=3.0; miny=0.0; maxy=3.0; }

    let mut chart = ChartBuilder::on(&root).margin(20).caption("Pearson Diagram", title_font)
        .set_label_area_size(LabelAreaPosition::Left, 60).set_label_area_size(LabelAreaPosition::Bottom, 60)
        .build_cartesian_2d(minx..maxx, miny..maxy)?;
    chart.configure_mesh().x_desc(set.xlabel).y_desc(set.ylabel).label_style(axis_font.clone()).axis_desc_style(axis_font.clone())
        .disable_x_mesh().disable_y_mesh().draw()?;

    // baselines
    for seg in &set.baselines {
        let pts: Vec<(f64,f64)> = seg.iter().map(|p| (p[0].log10(), p[1].log10())).collect();
        chart.draw_series(LineSeries::new(pts.into_iter(), RGBColor(120,120,120)))?;
    }
    // region labels
    let lab_font = ("Microsoft YaHei, Arial, SimHei, DejaVu Sans", 14).into_font();
    chart.draw_series(set.labels.iter().enumerate().filter_map(|(i, s)| set.label_locs.get(i).map(|p| (s, p))).map(|(s,p)| Text::new(s.clone(), (p[0], p[1]), lab_font.clone())))?;

    for (label, pts) in groups {
        let col = gcolors.get(&label).cloned().unwrap_or(BLACK);
        chart.draw_series(pts.into_iter().map(|(x,y)| Circle::new((x,y), 3, col.filled())))?.label(label)
            .legend(move |(x,y)| Circle::new((x,y), 4, col.filled()));
    }
    chart.configure_series_labels().border_style(&BLACK).background_style(&WHITE.mix(0.8)).label_font(legend_font)
        .position(SeriesLabelPosition::UpperRight).draw()?;
    root.present()?; Ok(())
}

fn export_pearson_4in1_with_area<B: DrawingBackend>(state: &crate::AppState, root: DrawingArea<B, Shift>) -> anyhow::Result<()>
where <B as DrawingBackend>::ErrorType: 'static {
    root.fill(&WHITE)?;
    // split 2x2 using split_horizontally and split_vertically to create equal squares
    let (left, right) = root.split_horizontally(root.dim_in_pixel().0 / 2);
    let (tl, bl) = left.split_vertically(left.dim_in_pixel().1 / 2);
    let (tr, br) = right.split_vertically(right.dim_in_pixel().1 / 2);
    let areas = [tl, tr, bl, br];
    for (i, area) in areas.into_iter().enumerate() { export_pearson_with_area(state, area, i)?; }
    root.present()?; Ok(())
}

// ---------------- Ternary helpers (for AbOrAn, AlFeTiMg, TiZrY) ----------------
fn ternary_to_cartesian(a: f64, b: f64, c: f64) -> (f64, f64) {
    // Equilateral triangle with height 1, convert barycentric (sum=100) to 2D
    let s = a + b + c; let (a, b, c) = if s == 0.0 { (0.0,0.0,0.0) } else { (a/s, b/s, c/s) };
    let x = 0.5*(2.0*b + c);
    let y = (3.0f64).sqrt()/2.0 * c;
    (x, y)
}

// ---------------- Ti/100 - Zr - 3*Y ternary (TiZrY.json) ----------------
#[derive(Deserialize)]
struct TernaryRegionsJson { coords: HashMap<String, Vec<[f64;3]>> }

fn load_tizry_json() -> anyhow::Result<TernaryRegionsJson> {
    let s = fs::read_to_string("src/TiZrY.json")?;
    #[derive(Deserialize)]
    struct Root { #[serde(rename="coords")] coords: HashMap<String, Vec<[f64;3]>> }
    let root: Root = serde_json::from_str(&s)?;
    Ok(TernaryRegionsJson { coords: root.coords })
}

fn load_aboran_json() -> anyhow::Result<TernaryRegionsJson> {
    let s = fs::read_to_string("src/AbOrAn.json")?;
    #[derive(Deserialize)]
    struct Root { #[serde(rename="coords")] coords: HashMap<String, Vec<[f64;3]>> }
    let root: Root = serde_json::from_str(&s)?;
    Ok(TernaryRegionsJson { coords: root.coords })
}

fn load_alfetimg_json() -> anyhow::Result<TernaryRegionsJson> {
    let s = fs::read_to_string("src/AlFeTiMg.json")?;
    #[derive(Deserialize)]
    struct Root { #[serde(rename="coords")] coords: HashMap<String, Vec<[f64;3]>> }
    let root: Root = serde_json::from_str(&s)?;
    Ok(TernaryRegionsJson { coords: root.coords })
}

pub fn show_tizry_plot(ui: &mut Ui, state: &crate::AppState) {
    // Build groups from data
    let headers = &state.raw_table.headers;
    let resolver = build_resolver(headers);
    let idx_ti = resolver.find_index("Ti").or_else(|| resolver.find_index("TiO2"));
    let idx_zr = resolver.find_index("Zr");
    let idx_y = resolver.find_index("Y");
    if idx_ti.is_none() || idx_zr.is_none() || idx_y.is_none() { ui.label("Need Ti/Zr/Y columns"); return; }
    use std::collections::BTreeMap;
    let mut groups: BTreeMap<String, Vec<[f64;2]>> = BTreeMap::new();
    let mut group_color: BTreeMap<String, Color32> = BTreeMap::new();
    let idx_label = resolver.find_index("Label");
    let idx_color = resolver.find_index("Color");
    for r in &state.raw_table.rows {
        let ti = idx_ti.and_then(|i| resolver.parse_value(r, i, false));
        let zr = idx_zr.and_then(|i| resolver.parse_value(r, i, false));
        let yv = idx_y.and_then(|i| resolver.parse_value(r, i, false));
        if let (Some(mut ti), Some(zr), Some(yv)) = (ti, zr, yv) {
            // If Ti column is TiO2 wt%, convert approximately to Ti ppm? Lacking unit clarity; follow JSON note: Ti/100 used
            // Here we assume if values are large (>100), they are ppm; we still apply /100 as defined.
            ti = ti / 100.0;
            let y3 = yv * 3.0;
            let (x,y) = ternary_to_cartesian(ti, zr, y3);
            let label = idx_label.and_then(|i| r.get(i)).cloned().unwrap_or_else(|| "Group".to_string());
            groups.entry(label.clone()).or_default().push([x,y]);
            if let Some(i) = idx_color { if let Some(cstr) = r.get(i) { if let Some(c) = parse_egui_color(cstr) { group_color.entry(label.clone()).or_insert(c); } } }
        }
    }
    // Load region boundaries
    let Ok(js) = load_tizry_json() else { ui.label("Missing TiZrY.json"); return; };
    Plot::new("tizry").view_aspect(1.0).include_x(0.0).include_x(1.0).include_y(0.0).include_y((3.0f64).sqrt()/2.0)
        .legend(Legend::default()).show(ui, |plot_ui| {
        // outer triangle
        let h = (3.0f64).sqrt()/2.0; let tri = vec![[0.0,0.0],[1.0,0.0],[0.5,h],[0.0,0.0]];
        plot_ui.line(Line::new(tri).color(Color32::from_gray(120)));
        // regions
        for (_name, poly3) in js.coords.iter() {
            let mut poly2 = Vec::new(); for p in poly3 { let (x,y) = ternary_to_cartesian(p[0], p[1], p[2]); poly2.push([x,y]); }
            let mut closed = poly2.clone(); if let Some(first) = closed.first().cloned() { closed.push(first); }
            plot_ui.line(Line::new(closed).color(Color32::from_gray(100)));
        }
        // points
        let palette = egui_palette(); let mut idx = 0usize;
        for (label, pts) in groups {
            let color = group_color.get(&label).cloned().unwrap_or_else(|| { let c = palette[idx % palette.len()]; idx+=1; c });
            let pp: PlotPoints = pts.into(); plot_ui.points(Points::new(pp).color(color).radius(2.5).name(label));
        }
    });
}

pub fn export_tizry_png(state: &crate::AppState, path: &std::path::Path) -> anyhow::Result<()> {
    let root: DrawingArea<BitMapBackend<'_>, _> = BitMapBackend::new(path.to_str().unwrap(), (1200, 1200)).into_drawing_area();
    export_tizry_with_area(state, root)
}
pub fn export_tizry_svg(state: &crate::AppState, path: &std::path::Path) -> anyhow::Result<()> {
    let root: DrawingArea<SVGBackend<'_>, _> = SVGBackend::new(path.to_str().unwrap(), (1200, 1200)).into_drawing_area();
    export_tizry_with_area(state, root)
}

fn export_tizry_with_area<B: DrawingBackend>(state: &crate::AppState, root: DrawingArea<B, Shift>) -> anyhow::Result<()>
where <B as DrawingBackend>::ErrorType: 'static {
    root.fill(&WHITE)?;
    let axis_font = ("Microsoft YaHei, Arial, SimHei, DejaVu Sans", 14).into_font();
    let mut chart = ChartBuilder::on(&root).margin(20)
        .set_label_area_size(LabelAreaPosition::Left, 40)
        .set_label_area_size(LabelAreaPosition::Bottom, 40)
        .build_cartesian_2d(0.0..1.0, 0.0..(3.0f64).sqrt()/2.0)?;
    chart.configure_mesh().label_style(axis_font.clone()).axis_desc_style(axis_font.clone())
        .disable_x_mesh().disable_y_mesh().draw()?;
    // draw outer triangle
    let h = (3.0f64).sqrt()/2.0; let tri = vec![(0.0,0.0),(1.0,0.0),(0.5,h),(0.0,0.0)];
    chart.draw_series(LineSeries::new(tri.into_iter(), RGBColor(120,120,120)))?;
    // regions
    let js = load_tizry_json()?;
    for (_name, poly3) in js.coords.iter() {
        let mut poly2: Vec<(f64,f64)> = Vec::new(); for p in poly3 { let (x,y) = ternary_to_cartesian(p[0], p[1], p[2]); poly2.push((x,y)); }
        let mut closed = poly2.clone(); if let Some(first) = closed.first().cloned() { closed.push(first); }
        chart.draw_series(LineSeries::new(closed.into_iter(), RGBColor(100,100,100)))?;
    }
    // points
    let headers = &state.raw_table.headers; let resolver = build_resolver(headers);
    let idx_ti = resolver.find_index("Ti").or_else(|| resolver.find_index("TiO2"));
    let idx_zr = resolver.find_index("Zr"); let idx_y = resolver.find_index("Y");
    use std::collections::BTreeMap; let idx_label = resolver.find_index("Label"); let idx_color = resolver.find_index("Color");
    let mut groups: BTreeMap<String, Vec<(f64,f64)>> = BTreeMap::new(); let mut gcolors: BTreeMap<String, RGBColor> = BTreeMap::new();
    let palette = plotters_palette(); let mut n = 0usize;
    for r in &state.raw_table.rows {
        let ti = idx_ti.and_then(|i| resolver.parse_value(r, i, false));
        let zr = idx_zr.and_then(|i| resolver.parse_value(r, i, false));
        let yv = idx_y.and_then(|i| resolver.parse_value(r, i, false));
        if let (Some(mut ti), Some(zr), Some(yv)) = (ti, zr, yv) {
            ti = ti/100.0; let y3 = yv*3.0; let (x,y) = ternary_to_cartesian(ti, zr, y3);
            let label = idx_label.and_then(|i| r.get(i)).cloned().unwrap_or_else(|| "Group".to_string());
            groups.entry(label.clone()).or_default().push((x,y));
            if let Some(i) = idx_color { if let Some(cstr) = r.get(i) { if let Some(c) = parse_plotters_color(cstr) { gcolors.entry(label.clone()).or_insert(c); } } }
            if !gcolors.contains_key(&label) { gcolors.insert(label.clone(), palette[n % palette.len()].clone()); n+=1; }
        }
    }
    for (label, pts) in groups {
        let col = gcolors.get(&label).cloned().unwrap_or(BLACK);
        chart.draw_series(pts.into_iter().map(|(x,y)| Circle::new((x,y), 3, col.filled())))?.label(label)
            .legend(move |(x,y)| Circle::new((x,y), 4, col.filled()));
    }
    chart.configure_series_labels().border_style(&BLACK).background_style(&WHITE.mix(0.8))
        .label_font(("Microsoft YaHei, Arial, SimHei, DejaVu Sans", 14).into_font())
        .position(SeriesLabelPosition::UpperRight).draw()?;
    root.present()?; Ok(())
}

pub fn show_aboran_plot(ui: &mut Ui, state: &crate::AppState) {
    let headers = &state.raw_table.headers; let resolver = build_resolver(headers);
    let idx_ab = resolver.find_index("Ab").or_else(|| resolver.find_index("Na2O"));
    let idx_or = resolver.find_index("Or").or_else(|| resolver.find_index("K2O"));
    let idx_an = resolver.find_index("An").or_else(|| resolver.find_index("CaO"));
    if idx_ab.is_none() || idx_or.is_none() || idx_an.is_none() { ui.label("Need Ab/Or/An (or Na2O/K2O/CaO)"); return; }
    use std::collections::BTreeMap; let mut groups: BTreeMap<String, Vec<[f64;2]>> = BTreeMap::new();
    let mut group_color: BTreeMap<String, Color32> = BTreeMap::new();
    let idx_label = resolver.find_index("Label"); let idx_color = resolver.find_index("Color");
    for r in &state.raw_table.rows { let ab = resolver.parse_value(r, idx_ab.unwrap(), false); let orv = resolver.parse_value(r, idx_or.unwrap(), false); let an = resolver.parse_value(r, idx_an.unwrap(), false);
        if let (Some(ab), Some(orv), Some(an)) = (ab, orv, an) { let (x,y) = ternary_to_cartesian(ab, orv, an); let label = idx_label.and_then(|i| r.get(i)).cloned().unwrap_or_else(|| "Group".to_string()); groups.entry(label.clone()).or_default().push([x,y]); if let Some(i)=idx_color { if let Some(cstr)=r.get(i) { if let Some(c)=parse_egui_color(cstr) { group_color.entry(label.clone()).or_insert(c); } } } }
    }
    let Ok(js)=load_aboran_json() else { ui.label("Missing AbOrAn.json"); return; };
    Plot::new("aboran").view_aspect(1.0).include_x(0.0).include_x(1.0).include_y(0.0).include_y((3.0f64).sqrt()/2.0).legend(Legend::default()).show(ui, |plot_ui| {
        let h=(3.0f64).sqrt()/2.0; let tri=vec![[0.0,0.0],[1.0,0.0],[0.5,h],[0.0,0.0]]; plot_ui.line(Line::new(tri).color(Color32::from_gray(120)));
        for (_name, poly3) in js.coords.iter() { let mut poly2=Vec::new(); for p in poly3 { let (x,y)=ternary_to_cartesian(p[0],p[1],p[2]); poly2.push([x,y]); } let mut closed=poly2.clone(); if let Some(first)=closed.first().cloned(){ closed.push(first);} plot_ui.line(Line::new(closed).color(Color32::from_gray(100))); }
        let palette=egui_palette(); let mut idx=0usize; for (label, pts) in groups { let color=group_color.get(&label).cloned().unwrap_or_else(|| { let c=palette[idx%palette.len()]; idx+=1; c }); let pp:PlotPoints=pts.into(); plot_ui.points(Points::new(pp).color(color).radius(2.5).name(label)); }
    });
}

pub fn export_aboran_png(state: &crate::AppState, path: &std::path::Path) -> anyhow::Result<()> { let root: DrawingArea<BitMapBackend<'_>, _>=BitMapBackend::new(path.to_str().unwrap(), (1200,1200)).into_drawing_area(); export_aboran_with_area(state, root) }
pub fn export_aboran_svg(state: &crate::AppState, path: &std::path::Path) -> anyhow::Result<()> { let root: DrawingArea<SVGBackend<'_>, _>=SVGBackend::new(path.to_str().unwrap(), (1200,1200)).into_drawing_area(); export_aboran_with_area(state, root) }

fn export_aboran_with_area<B: DrawingBackend>(state: &crate::AppState, root: DrawingArea<B, Shift>) -> anyhow::Result<()>
where <B as DrawingBackend>::ErrorType: 'static { root.fill(&WHITE)?; let mut chart=ChartBuilder::on(&root).margin(20).set_label_area_size(LabelAreaPosition::Left,40).set_label_area_size(LabelAreaPosition::Bottom,40).build_cartesian_2d(0.0..1.0, 0.0..(3.0f64).sqrt()/2.0)?; chart.configure_mesh().disable_x_mesh().disable_y_mesh().draw()?; let h=(3.0f64).sqrt()/2.0; let tri=vec![(0.0,0.0),(1.0,0.0),(0.5,h),(0.0,0.0)]; chart.draw_series(LineSeries::new(tri.into_iter(), RGBColor(120,120,120)))?; let js=load_aboran_json()?; for (_name, poly3) in js.coords.iter(){ let mut poly2:Vec<(f64,f64)>=Vec::new(); for p in poly3 { let (x,y)=ternary_to_cartesian(p[0],p[1],p[2]); poly2.push((x,y)); } let mut closed=poly2.clone(); if let Some(first)=closed.first().cloned(){ closed.push(first);} chart.draw_series(LineSeries::new(closed.into_iter(), RGBColor(100,100,100)))?; } let headers=&state.raw_table.headers; let resolver=build_resolver(headers); let idx_ab=resolver.find_index("Ab").or_else(|| resolver.find_index("Na2O")); let idx_or=resolver.find_index("Or").or_else(|| resolver.find_index("K2O")); let idx_an=resolver.find_index("An").or_else(|| resolver.find_index("CaO")); use std::collections::BTreeMap; let idx_label=resolver.find_index("Label"); let idx_color=resolver.find_index("Color"); let mut groups:BTreeMap<String, Vec<(f64,f64)>>=BTreeMap::new(); let mut gcolors:BTreeMap<String, RGBColor>=BTreeMap::new(); let palette=plotters_palette(); let mut n=0usize; for r in &state.raw_table.rows { let ab=idx_ab.and_then(|i| resolver.parse_value(r,i,false)); let orv=idx_or.and_then(|i| resolver.parse_value(r,i,false)); let an=idx_an.and_then(|i| resolver.parse_value(r,i,false)); if let (Some(ab),Some(orv),Some(an))=(ab,orv,an){ let (x,y)=ternary_to_cartesian(ab,orv,an); let label=idx_label.and_then(|i| r.get(i)).cloned().unwrap_or_else(|| "Group".to_string()); groups.entry(label.clone()).or_default().push((x,y)); if let Some(i)=idx_color { if let Some(cstr)=r.get(i) { if let Some(c)=parse_plotters_color(cstr) { gcolors.entry(label.clone()).or_insert(c); } } } if !gcolors.contains_key(&label){ gcolors.insert(label.clone(), palette[n%palette.len()].clone()); n+=1; } } } for (label, pts) in groups { let col=gcolors.get(&label).cloned().unwrap_or(BLACK); chart.draw_series(pts.into_iter().map(|(x,y)| Circle::new((x,y),3,col.filled())))?.label(label).legend(move |(x,y)| Circle::new((x,y),4,col.filled())); } chart.configure_series_labels().border_style(&BLACK).background_style(&WHITE.mix(0.8)).label_font(("Microsoft YaHei, Arial, SimHei, DejaVu Sans", 14).into_font()).position(SeriesLabelPosition::UpperRight).draw()?; root.present()?; Ok(()) }

pub fn show_alfetimg_plot(ui: &mut Ui, state: &crate::AppState) {
    let headers = &state.raw_table.headers; let resolver = build_resolver(headers);
    let idx_al = resolver.find_index("Al").or_else(|| resolver.find_index("Al2O3"));
    let idx_feti = resolver.find_index("FeTi").or_else(|| resolver.find_index("FeO"));
    let idx_mg = resolver.find_index("Mg").or_else(|| resolver.find_index("MgO"));
    if idx_al.is_none() || idx_feti.is_none() || idx_mg.is_none() { ui.label("Need Al/Fe+Ti/Mg (or Al2O3/FeO/MgO)"); return; }
    use std::collections::BTreeMap; let mut groups: BTreeMap<String, Vec<[f64;2]>> = BTreeMap::new(); let mut group_color: BTreeMap<String, Color32> = BTreeMap::new(); let idx_label=resolver.find_index("Label"); let idx_color=resolver.find_index("Color");
    for r in &state.raw_table.rows { let al = resolver.parse_value(r, idx_al.unwrap(), false); let feti = resolver.parse_value(r, idx_feti.unwrap(), false); let mg = resolver.parse_value(r, idx_mg.unwrap(), false); if let (Some(al),Some(feti),Some(mg))=(al,feti,mg){ let (x,y)=ternary_to_cartesian(al,feti,mg); let label=idx_label.and_then(|i| r.get(i)).cloned().unwrap_or_else(|| "Group".to_string()); groups.entry(label.clone()).or_default().push([x,y]); if let Some(i)=idx_color { if let Some(cstr)=r.get(i) { if let Some(c)=parse_egui_color(cstr) { group_color.entry(label.clone()).or_insert(c); } } } } }
    let Ok(js)=load_alfetimg_json() else { ui.label("Missing AlFeTiMg.json"); return; };
    Plot::new("alfetimg").view_aspect(1.0).include_x(0.0).include_x(1.0).include_y(0.0).include_y((3.0f64).sqrt()/2.0).legend(Legend::default()).show(ui, |plot_ui| {
        let h=(3.0f64).sqrt()/2.0; let tri=vec![[0.0,0.0],[1.0,0.0],[0.5,h],[0.0,0.0]]; plot_ui.line(Line::new(tri).color(Color32::from_gray(120)));
        for (_name, poly3) in js.coords.iter() { let mut poly2=Vec::new(); for p in poly3 { let (x,y)=ternary_to_cartesian(p[0],p[1],p[2]); poly2.push([x,y]); } let mut closed=poly2.clone(); if let Some(first)=closed.first().cloned(){ closed.push(first);} plot_ui.line(Line::new(closed).color(Color32::from_gray(100))); }
        let palette=egui_palette(); let mut idx=0usize; for (label, pts) in groups { let color=group_color.get(&label).cloned().unwrap_or_else(|| { let c=palette[idx%palette.len()]; idx+=1; c }); let pp:PlotPoints=pts.into(); plot_ui.points(Points::new(pp).color(color).radius(2.5).name(label)); }
    });
}

pub fn export_alfetimg_png(state: &crate::AppState, path: &std::path::Path) -> anyhow::Result<()> { let root: DrawingArea<BitMapBackend<'_>, _>=BitMapBackend::new(path.to_str().unwrap(), (1200,1200)).into_drawing_area(); export_alfetimg_with_area(state, root) }
pub fn export_alfetimg_svg(state: &crate::AppState, path: &std::path::Path) -> anyhow::Result<()> { let root: DrawingArea<SVGBackend<'_>, _>=SVGBackend::new(path.to_str().unwrap(), (1200,1200)).into_drawing_area(); export_alfetimg_with_area(state, root) }

fn export_alfetimg_with_area<B: DrawingBackend>(state: &crate::AppState, root: DrawingArea<B, Shift>) -> anyhow::Result<()>
where <B as DrawingBackend>::ErrorType: 'static { root.fill(&WHITE)?; let mut chart=ChartBuilder::on(&root).margin(20).set_label_area_size(LabelAreaPosition::Left,40).set_label_area_size(LabelAreaPosition::Bottom,40).build_cartesian_2d(0.0..1.0, 0.0..(3.0f64).sqrt()/2.0)?; chart.configure_mesh().disable_x_mesh().disable_y_mesh().draw()?; let h=(3.0f64).sqrt()/2.0; let tri=vec![(0.0,0.0),(1.0,0.0),(0.5,h),(0.0,0.0)]; chart.draw_series(LineSeries::new(tri.into_iter(), RGBColor(120,120,120)))?; let js=load_alfetimg_json()?; for (_name, poly3) in js.coords.iter(){ let mut poly2:Vec<(f64,f64)>=Vec::new(); for p in poly3 { let (x,y)=ternary_to_cartesian(p[0],p[1],p[2]); poly2.push((x,y)); } let mut closed=poly2.clone(); if let Some(first)=closed.first().cloned(){ closed.push(first);} chart.draw_series(LineSeries::new(closed.into_iter(), RGBColor(100,100,100)))?; } let headers=&state.raw_table.headers; let resolver=build_resolver(headers); let idx_al=resolver.find_index("Al").or_else(|| resolver.find_index("Al2O3")); let idx_feti=resolver.find_index("FeTi").or_else(|| resolver.find_index("FeO")); let idx_mg=resolver.find_index("Mg").or_else(|| resolver.find_index("MgO")); use std::collections::BTreeMap; let idx_label=resolver.find_index("Label"); let idx_color=resolver.find_index("Color"); let mut groups:BTreeMap<String, Vec<(f64,f64)>>=BTreeMap::new(); let mut gcolors:BTreeMap<String, RGBColor>=BTreeMap::new(); let palette=plotters_palette(); let mut n=0usize; for r in &state.raw_table.rows { let al=idx_al.and_then(|i| resolver.parse_value(r,i,false)); let feti=idx_feti.and_then(|i| resolver.parse_value(r,i,false)); let mg=idx_mg.and_then(|i| resolver.parse_value(r,i,false)); if let (Some(al),Some(feti),Some(mg))=(al,feti,mg){ let (x,y)=ternary_to_cartesian(al,feti,mg); let label=idx_label.and_then(|i| r.get(i)).cloned().unwrap_or_else(|| "Group".to_string()); groups.entry(label.clone()).or_default().push((x,y)); if let Some(i)=idx_color { if let Some(cstr)=r.get(i) { if let Some(c)=parse_plotters_color(cstr) { gcolors.entry(label.clone()).or_insert(c); } } } if !gcolors.contains_key(&label){ gcolors.insert(label.clone(), palette[n%palette.len()].clone()); n+=1; } } } for (label, pts) in groups { let col=gcolors.get(&label).cloned().unwrap_or(BLACK); chart.draw_series(pts.into_iter().map(|(x,y)| Circle::new((x,y),3,col.filled())))?.label(label).legend(move |(x,y)| Circle::new((x,y),4,col.filled())); } chart.configure_series_labels().border_style(&BLACK).background_style(&WHITE.mix(0.8)).label_font(("Microsoft YaHei, Arial, SimHei, DejaVu Sans", 14).into_font()).position(SeriesLabelPosition::UpperRight).draw()?; root.present()?; Ok(()) }

// ---------------- CIPW (simplified normative) and QAPF ----------------
#[derive(Clone, Debug)]
pub struct CipwNorm {
    pub label: String,
    pub q_mol: f64,
    pub a_mol: f64,
    pub p_mol: f64,
    pub f_mol: f64,
}

fn molar_mass(oxide: &str) -> Option<f64> {
    match oxide {
        "SiO2"=>Some(60.083), "Al2O3"=>Some(101.960077), "Fe2O3"=>Some(159.687), "FeO"=>Some(71.844),
        "MgO"=>Some(40.304), "CaO"=>Some(56.077), "Na2O"=>Some(61.97853856), "K2O"=>Some(94.1956),
        "TiO2"=>Some(79.865), "P2O5"=>Some(141.942524), _=>None
    }
}

fn parse_major(resolver: &HeaderResolver, row: &[String], name: &str) -> f64 {
    resolver.find_index(name).and_then(|i| resolver.parse_value(row, i, true)).unwrap_or(0.0)
}

fn cipw_qapf_for_row(resolver: &HeaderResolver, row: &[String]) -> Option<CipwNorm> {
    // Read majors (wt%) and convert to moles of oxides
    let sio2_w = parse_major(resolver, row, "SiO2");
    let tio2_w = parse_major(resolver, row, "TiO2");
    let mut al2o3_w = parse_major(resolver, row, "Al2O3");
    let mut fe2o3_w = parse_major(resolver, row, "Fe2O3");
    let mut feo_w = parse_major(resolver, row, "FeO");
    let mno_w = parse_major(resolver, row, "MnO");
    let mut mgo_w = parse_major(resolver, row, "MgO");
    let mut cao_w = parse_major(resolver, row, "CaO");
    let mut na2o_w = parse_major(resolver, row, "Na2O");
    let mut k2o_w = parse_major(resolver, row, "K2O");
    let mut p2o5_w = parse_major(resolver, row, "P2O5");
    // Accessory/volatile proxies
    let co2_w = parse_major(resolver, row, "CO2");
    let so3_w = parse_major(resolver, row, "SO3");
    let s_w = parse_major(resolver, row, "S");
    let f_w = parse_major(resolver, row, "F");
    let cl_w = parse_major(resolver, row, "Cl");
    let zr_w = parse_major(resolver, row, "Zr");
    let cr_w = parse_major(resolver, row, "Cr");
    let ni_w = parse_major(resolver, row, "Ni");
    let ba_w = parse_major(resolver, row, "Ba");
    let sr_w = parse_major(resolver, row, "Sr");

    // Moles of oxides/elements
    let mut m_sio2 = sio2_w / molar_mass("SiO2")?;
    let mut m_tio2 = tio2_w / molar_mass("TiO2").unwrap_or(79.865);
    let mut m_al2o3 = al2o3_w / molar_mass("Al2O3")?;
    let mut m_fe2o3 = fe2o3_w / molar_mass("Fe2O3")?;
    let mut m_feo = feo_w / molar_mass("FeO")?;
    let mut m_mno = mno_w / molar_mass("MnO").unwrap_or(70.937044);
    let mut m_mgo = mgo_w / molar_mass("MgO")?;
    let mut m_cao = cao_w / molar_mass("CaO")?;
    let mut m_na2o = na2o_w / molar_mass("Na2O")?;
    let mut m_k2o = k2o_w / molar_mass("K2O")?;
    let mut m_p2o5 = p2o5_w / molar_mass("P2O5")?;
    let mut m_co2 = if co2_w>0.0 { co2_w / molar_mass("CO2").unwrap_or(44.009) } else { 0.0 };
    let mut m_so3 = if so3_w>0.0 { so3_w / molar_mass("SO3").unwrap_or(80.057) } else { 0.0 };
    let mut m_s = if s_w>0.0 { s_w / molar_mass("S").unwrap_or(32.06) } else { 0.0 };
    let mut m_f = if f_w>0.0 { f_w / molar_mass("F").unwrap_or(18.9984) } else { 0.0 };
    let mut m_cl = if cl_w>0.0 { cl_w / molar_mass("Cl").unwrap_or(35.45) } else { 0.0 };
    let mut m_zr = if zr_w>0.0 { zr_w / molar_mass("Zr").unwrap_or(91.224) } else { 0.0 };
    let mut m_cr = if cr_w>0.0 { cr_w / molar_mass("Cr").unwrap_or(51.9961) } else { 0.0 };
    let mut m_ni = if ni_w>0.0 { ni_w / molar_mass("Ni").unwrap_or(58.6934) } else { 0.0 };
    let mut m_ba = if ba_w>0.0 { ba_w / molar_mass("Ba").unwrap_or(137.327) } else { 0.0 };
    let mut m_sr = if sr_w>0.0 { sr_w / molar_mass("Sr").unwrap_or(87.62) } else { 0.0 };

    // 1) Apatite: CaO and P2O5 with ratio 10/3, and P2O5 -> 2/3
    let need_cao = (10.0/3.0) * m_p2o5;
    let take_cao = m_cao.min(need_cao);
    m_cao -= take_cao;
    let apatite = m_p2o5; // track if needed
    m_p2o5 = m_p2o5 / 1.5;

    // 2) Halides: F reduces P2O5 twice (as in python), Cl consumes Na2O -> Halite
    if m_f > 0.0 { let d = m_f.min(m_p2o5); m_f -= d; m_p2o5 -= d; }
    if m_f > 0.0 { let d = m_f.min(m_p2o5); m_f -= d; m_p2o5 -= d; }
    let halite = m_cl.min(m_na2o); m_na2o -= halite; let _halite = halite; // NaCl
    // CaO + 0.5 F -> reduces CaO further; F halves
    let d = m_cao.min(0.5*m_f); m_cao -= d; m_f -= 2.0*d;
    let fluorite = (m_f*0.5).max(0.0);

    // 3) SO3 distribution: Thenardite vs Anhydrite depending on Na2O, CaO
    let a_or_t = if m_so3 <= 0.0 { 0 } else if m_na2o >= m_so3 { 1 } else if m_na2o > 0.0 { 2 } else { 3 }; // 1 Thenardite, 2 Both, 3 Anhydrite
    let mut anhydrite = 0.0; let mut thenardite = 0.0;
    match a_or_t {
        1 => { thenardite = m_so3; m_so3 = 0.0; }
        2 => { thenardite = m_so3 - m_cao; anhydrite = m_cao; }
        3 => { anhydrite = m_so3; }
        _ => {}
    }
    m_cao -= anhydrite; m_na2o -= thenardite; if m_na2o < 0.0 { m_na2o = 0.0; }

    // 4) Pyrite consumes FeO: FeO -= 0.5*S
    let pyrite = 0.5*m_s; let d = m_feo.min(pyrite); m_feo -= d; let _ = d; // track if needed

    // 5) Chromite vs Magnesiochromite using FeO vs Cr
    let cor_m = if m_cr > 0.0 { if m_feo >= m_cr { 1 } else if m_feo > 0.0 { 2 } else { 3 } } else { 0 }; //1 Chromite,2 Both,3 Magnesio
    let mut chromite = 0.0; let mut magnesiochromite = 0.0;
    match cor_m {
        1 => { chromite = m_cr; m_cr = 0.0; }
        2 => { chromite = m_feo; magnesiochromite = m_cr - m_feo; m_cr = 0.0; }
        3 => { magnesiochromite = m_cr; m_cr = 0.0; }
        _ => {}
    }
    m_mgo -= magnesiochromite; if m_mgo < 0.0 { m_mgo = 0.0; }
    m_feo -= chromite; if m_feo < 0.0 { m_feo = 0.0; }

    // 6) Ilmenite vs Sphene using FeO vs TiO2
    let i_or_s = if m_tio2 <= 0.0 { 0 } else if m_feo >= m_tio2 { 1 } else if m_feo > 0.0 { 2 } else { 3 }; //1 Ilmenite,2 Both,3 Sphene
    let mut ilmenite = 0.0; let mut sphene = 0.0;
    match i_or_s {
        1 => { ilmenite = m_tio2; m_tio2 = 0.0; }
        3 => { sphene = m_tio2; m_tio2 = 0.0; }
        2 => { sphene = m_tio2 - m_feo; ilmenite = m_feo; m_tio2 = 0.0; }
        _ => {}
    }
    m_feo -= ilmenite; if m_feo < 0.0 { m_feo = 0.0; }

    // 7) Carbonate: Calcite vs Na2CO3 using CaO vs CO2
    let c_or_n = if m_co2 <= 0.0 { 0 } else if m_cao >= m_co2 { 1 } else if m_cao > 0.0 { 2 } else { 3 }; //1 Calcite,2 Both,3 Na2CO3
    let mut calcite = 0.0; let mut na2co3 = 0.0;
    match c_or_n {
        1 => { calcite = m_co2; m_co2 = 0.0; }
        3 => { na2co3 = m_co2; m_co2 = 0.0; }
        2 => { calcite = m_cao; na2co3 = m_co2 - m_cao; m_co2 = 0.0; m_cao = 0.0; }
        _ => { m_co2 = 0.0; m_so3 = 0.0; }
    }
    m_cao -= calcite; if m_cao < 0.0 { m_cao = 0.0; }
    // SO3 removes Na2O further
    if m_so3 > 0.0 { if m_na2o >= m_so3 { m_na2o -= m_so3; } else { m_na2o = 0.0; } }

    // 8) Zircon: consumes SiO2 equal to Zr
    m_sio2 -= m_zr; if m_sio2 < 0.0 { m_sio2 = 0.0; }

    // 9) K-feldspar vs K2SiO3 using Al2O3
    let mut m_or = m_k2o.min(m_al2o3); // Orthoclase
    let mut k2sio3 = 0.0;
    if m_k2o > 0.0 {
        if m_al2o3 >= m_k2o { /* Orthoclase fully */ }
        else if m_al2o3 > 0.0 { // Both
            k2sio3 = m_k2o - m_al2o3; m_or = m_al2o3; m_k2o = 0.0; m_al2o3 = 0.0;
        } else { k2sio3 = m_k2o; m_k2o = 0.0; }
    }
    m_al2o3 -= m_or; if m_al2o3 < 0.0 { m_al2o3 = 0.0; } m_k2o -= m_or; if m_k2o < 0.0 { m_k2o = 0.0; }

    // 10) Albite vs Na2SiO3
    let mut m_ab = m_na2o.min(m_al2o3);
    let mut na2sio3 = 0.0;
    if m_na2o > 0.0 {
        if m_al2o3 >= m_na2o { /* Albite fully */ }
        else if m_al2o3 > 0.0 { // Both
            na2sio3 = m_na2o - m_al2o3; m_ab = m_al2o3; m_na2o = 0.0; m_al2o3 = 0.0;
        } else { na2sio3 = m_na2o; m_na2o = 0.0; }
    }
    m_al2o3 -= m_ab; if m_al2o3 < 0.0 { m_al2o3 = 0.0; } m_na2o -= m_ab; if m_na2o < 0.0 { m_na2o = 0.0; }

    // 11) Anorthite vs Corundum
    let mut m_an = 0.0; let mut corundum = 0.0;
    if m_al2o3 > 0.0 {
        if m_cao > 0.0 { m_an = m_cao.min(m_al2o3); m_cao -= m_an; m_al2o3 -= m_an; }
        if m_al2o3 > 0.0 { corundum = m_al2o3; m_al2o3 = 0.0; }
    }

    // 12) Sphene vs Rutile using CaO vs MnO
    let mut rutile = 0.0;
    if m_mno > 0.0 {
        if m_cao >= m_mno { sphene += m_mno; m_mno = 0.0; }
        else if m_cao > 0.0 { rutile = m_mno - m_cao; m_mno = m_cao; m_cao = 0.0; }
        else { rutile = m_mno; m_mno = 0.0; }
        m_cao -= m_mno; if m_cao < 0.0 { m_cao = 0.0; }
    }

    // 13) Acmite vs Na2SiO3 using Fe2O3 vs Na2SiO3 proxy (Cl in python)
    let mut acmite = 0.0;
    if na2sio3 > 0.0 {
        if m_fe2o3 >= na2sio3 { acmite = na2sio3; na2sio3 = 0.0; }
        else if m_fe2o3 > 0.0 { acmite = m_fe2o3; na2sio3 -= m_fe2o3; m_fe2o3 = 0.0; }
    }
    m_fe2o3 -= acmite; if m_fe2o3 < 0.0 { m_fe2o3 = 0.0; }

    // 14) Magnetite vs Hematite using FeO vs Fe2O3
    let mut magnetite = 0.0; let mut hematite = 0.0;
    if m_fe2o3 > 0.0 {
        if m_feo >= m_fe2o3 { magnetite = m_fe2o3; m_fe2o3 = 0.0; }
        else if m_feo > 0.0 { magnetite = m_feo; hematite = m_fe2o3 - m_feo; m_fe2o3 = 0.0; }
        else { hematite = m_fe2o3; m_fe2o3 = 0.0; }
        m_feo -= magnetite; if m_feo < 0.0 { m_feo = 0.0; }
    }

    // 15) Merge FeO + MgO for pyroxenes later
    m_feo += m_mgo; m_mgo = 0.0;

    // 16) Diopside vs Wollastonite using CaO vs FeO(Mg)
    let mut diopside = 0.0; let mut wollastonite = 0.0;
    if m_cao > 0.0 {
        if m_feo >= m_cao { diopside = m_cao; m_cao = 0.0; }
        else if m_feo > 0.0 { diopside = m_feo; wollastonite = m_cao - m_feo; m_cao = 0.0; }
        else { wollastonite = m_cao; m_cao = 0.0; }
        m_feo -= diopside; if m_feo < 0.0 { m_feo = 0.0; }
    }

    // 17) Build quartz from silica balance after feldspars and others
    // Consume SiO2 for Or(6), Ab(6), An(2), Acmite(4), Diopside(2), Sphene(1), Hypersthene(1), Albite(6), Orthoclase(6), Wollastonite(1)
    let mut quartz = m_sio2 - (6.0*m_or + 6.0*m_ab + 2.0*m_an + 4.0*acmite + 2.0*diopside + sphene + m_ab*6.0 + m_or*6.0 + wollastonite);
    if quartz.is_nan() { quartz = 0.0; }

    // 18) Hypersthene/Olivine depending on quartz sign
    let mut hypersthene = m_feo; let mut olivine = 0.0;
    let old_hyp = hypersthene;
    if hypersthene <= 0.0 { hypersthene = 0.0; }
    else if quartz > 0.0 { /* hypersthene */ }
    else if hypersthene + 2.0*quartz > 0.0 { hypersthene = hypersthene + 2.0*quartz; olivine = quartz.abs(); quartz = 0.0; }
    else { olivine = hypersthene/2.0; hypersthene = 0.0; }
    quartz = quartz + old_hyp - (hypersthene + olivine);

    // 19) Sphene/Perovskite adjustment with quartz
    let mut perovskite = 0.0; let old_sph = sphene;
    if sphene > 0.0 {
        if quartz >= 0.0 { /* sphene */ }
        else if sphene + quartz > 0.0 { sphene += quartz; /* both */ }
        else { perovskite = sphene; sphene = 0.0; }
        quartz += old_sph - sphene;
    }
    
    // 20) Albite/Nepheline with quartz
    let old_ab = m_ab; let mut nepheline = 0.0;
    if m_ab > 0.0 {
        if quartz >= 0.0 { /* albite */ }
        else if m_ab + quartz/4.0 > 0.0 { m_ab += quartz/4.0; nepheline = old_ab - m_ab; }
        else { nepheline = m_ab; m_ab = 0.0; }
        quartz += (6.0*old_ab) - (6.0*m_ab) - (2.0*nepheline);
    }

    // 21) Orthoclase/Leucite with quartz
    let old_or = m_or; let mut leucite = 0.0; let mut kalsilite = 0.0; let mut larnite = 0.0; let mut perovskite = 0.0;
    if m_or > 0.0 {
        if quartz >= 0.0 { /* orthoclase */ }
        else if m_or + quartz/2.0 > 0.0 { m_or += quartz/2.0; leucite = old_or - m_or; }
        else { leucite = m_or; m_or = 0.0; }
        quartz += (6.0*old_or) - (6.0*m_or) - (4.0*leucite);
    }

    // 22) Wollastonite/Larnite with quartz
    let old_w = wollastonite;
    if wollastonite > 0.0 {
        if quartz >= 0.0 { /* wollastonite */ }
        else if wollastonite + quartz/2.0 > 0.0 { wollastonite += quartz*2.0; larnite = (old_w - wollastonite)/2.0; }
        else { larnite = wollastonite/2.0; wollastonite = 0.0; }
        quartz += old_w - wollastonite - larnite;
    }

    // 23) Diopside/Larnite/Olivine with quartz
    let old_d = diopside; let old_l = larnite; let old_o = olivine;
    if diopside > 0.0 {
        if quartz >= 0.0 { /* diopside */ }
        else if diopside + quartz > 0.0 { diopside += quartz; larnite += old_d - diopside; olivine += old_d - diopside; }
        else { larnite += diopside/2.0; olivine += diopside/2.0; diopside = 0.0; }
        quartz += (2.0*old_d) + old_o + old_l - larnite - (2.0*diopside) - olivine;
    }

    // 24) Leucite/Kalsilite with quartz
    let old_le = leucite;
    if leucite > 0.0 {
        if quartz >= 0.0 { /* leucite */ }
        else if leucite + quartz/2.0 > 0.0 { leucite += quartz/2.0; kalsilite = old_le - leucite; }
        else { kalsilite = leucite; leucite = 0.0; }
        quartz += (4.0*old_le) - (4.0*leucite) - (2.0*kalsilite);
    }

    // Normative Q-A-P-F
    let q = quartz.max(0.0);
    let a = m_or.max(0.0);
    let p = (m_an + m_ab).max(0.0);
    let f = (nepheline + leucite + kalsilite).max(0.0);
    let label = resolver.find_index("Label").and_then(|i| row.get(i)).cloned().unwrap_or_else(|| "Group".to_string());
    Some(CipwNorm{ label, q_mol: q, a_mol: a, p_mol: p, f_mol: f })
}

pub fn compute_cipw_and_store(state: &mut crate::AppState) {
    let resolver = build_resolver(&state.raw_table.headers);
    let mut results = Vec::new();
    for row in &state.raw_table.rows { if let Some(r) = cipw_qapf_for_row(&resolver, row) { results.push(r); } }
    state.cipw_results = results;
    state.status = format!("CIPW computed for {} rows", state.cipw_results.len());
}

fn qapf_point(q: f64, a: f64, p: f64, f: f64) -> (f32, f32) {
    // Use Q-A-P triangle when F < 10% of (Q+A+P+F); otherwise F-A-P
    let sum = q + a + p + f; if sum <= 0.0 { return (0.0,0.0); }
    let qn = q / sum * 100.0; let an = a / sum * 100.0; let pn = p / sum * 100.0; let f_n = f / sum * 100.0;
    let (x,y) = if f_n < 10.0 { // Q-A-P
        let (x,y) = ternary_to_cartesian(qn, an, pn);
        (x as f32, y as f32)
    } else { // F-A-P
        let (x,y) = ternary_to_cartesian(f_n, an, pn);
        (x as f32, y as f32)
    };
    (x,y)
}

pub fn show_qapf_plot(ui: &mut Ui, state: &crate::AppState) {
    if state.cipw_results.is_empty() { ui.label("Please run CIPW first"); return; }
    Plot::new("qapf").view_aspect(1.0).include_x(0.0).include_x(1.0).include_y(0.0).include_y((3.0f64).sqrt()/2.0)
        .legend(Legend::default()).show(ui, |plot_ui| {
        let h = (3.0f64).sqrt()/2.0; let tri = vec![[0.0,0.0],[1.0,0.0],[0.5,h],[0.0,0.0]];
        plot_ui.line(Line::new(tri).color(Color32::from_gray(120)));
        let palette = egui_palette(); let mut idx = 0usize;
        use std::collections::BTreeMap; let mut by_label: BTreeMap<String, Vec<[f64;2]>> = BTreeMap::new();
        for r in &state.cipw_results {
            let (x,y) = qapf_point(r.q_mol, r.a_mol, r.p_mol, r.f_mol); by_label.entry(r.label.clone()).or_default().push([x as f64, y as f64]);
        }
        for (label, pts) in by_label {
            let color = palette[idx % palette.len()]; idx+=1; let pp: PlotPoints = pts.into();
            plot_ui.points(Points::new(pp).color(color).radius(2.5).name(label));
        }
    });
}

pub fn export_qapf_png(state: &crate::AppState, path: &std::path::Path) -> anyhow::Result<()> {
    let root: DrawingArea<BitMapBackend<'_>, _> = BitMapBackend::new(path.to_str().unwrap(), (1200, 1200)).into_drawing_area();
    export_qapf_with_area(state, root)
}
pub fn export_qapf_svg(state: &crate::AppState, path: &std::path::Path) -> anyhow::Result<()> {
    let root: DrawingArea<SVGBackend<'_>, _> = SVGBackend::new(path.to_str().unwrap(), (1200, 1200)).into_drawing_area();
    export_qapf_with_area(state, root)
}

fn export_qapf_with_area<B: DrawingBackend>(state: &crate::AppState, root: DrawingArea<B, Shift>) -> anyhow::Result<()>
where <B as DrawingBackend>::ErrorType: 'static {
    root.fill(&WHITE)?;
    let mut chart = ChartBuilder::on(&root).margin(20)
        .set_label_area_size(LabelAreaPosition::Left, 40)
        .set_label_area_size(LabelAreaPosition::Bottom, 40)
        .build_cartesian_2d(0.0..1.0, 0.0..(3.0f64).sqrt()/2.0)?;
    chart.configure_mesh().disable_x_mesh().disable_y_mesh().draw()?;
    let h = (3.0f64).sqrt()/2.0; let tri = vec![(0.0,0.0),(1.0,0.0),(0.5,h),(0.0,0.0)];
    chart.draw_series(LineSeries::new(tri.into_iter(), RGBColor(120,120,120)))?;
    use std::collections::BTreeMap; let mut by_label: BTreeMap<String, Vec<(f64,f64)>> = BTreeMap::new();
    for r in &state.cipw_results { let (x,y) = qapf_point(r.q_mol, r.a_mol, r.p_mol, r.f_mol); by_label.entry(r.label.clone()).or_default().push((x as f64,y as f64)); }
    let palette = plotters_palette(); let mut n = 0usize;
    for (label, pts) in by_label {
        let col = palette[n % palette.len()].clone(); n+=1;
        chart.draw_series(pts.into_iter().map(|(x,y)| Circle::new((x,y), 3, col.filled())))?.label(label)
            .legend(move |(x,y)| Circle::new((x,y), 4, col.filled()));
    }
    chart.configure_series_labels().border_style(&BLACK).background_style(&WHITE.mix(0.8))
        .label_font(("Microsoft YaHei, Arial, SimHei, DejaVu Sans", 14).into_font())
        .position(SeriesLabelPosition::UpperRight).draw()?;
    root.present()?; Ok(())
}

// ---------------- CIPW result export ----------------
pub fn export_cipw_csv(state: &crate::AppState, path: &std::path::Path) -> anyhow::Result<()> {
    let mut w = csv::Writer::from_path(path)?;
    w.write_record(["Label","Q_mol","A_mol","P_mol","F_mol"])?;
    for r in &state.cipw_results {
        w.write_record(&[r.label.as_str(), &format!("{:.6}", r.q_mol), &format!("{:.6}", r.a_mol), &format!("{:.6}", r.p_mol), &format!("{:.6}", r.f_mol)])?;
    }
    w.flush()?; Ok(())
}

fn ree_standard_values(idx: usize) -> std::collections::HashMap<&'static str, f64> {
    use std::collections::HashMap; let mut m = HashMap::new();
    match idx {
        0 => { m.insert("La",0.237); m.insert("Ce",0.612); m.insert("Pr",0.095); m.insert("Nd",0.467); m.insert("Sm",0.153); m.insert("Eu",0.058); m.insert("Gd",0.2055); m.insert("Tb",0.0374); m.insert("Dy",0.254); m.insert("Ho",0.0566); m.insert("Er",0.1655); m.insert("Tm",0.0255); m.insert("Yb",0.17); m.insert("Lu",0.0254); }
        1 => { m.insert("La",0.367); m.insert("Ce",0.957); m.insert("Pr",0.137); m.insert("Nd",0.711); m.insert("Sm",0.231); m.insert("Eu",0.087); m.insert("Gd",0.306); m.insert("Tb",0.058); m.insert("Dy",0.381); m.insert("Ho",0.0851); m.insert("Er",0.249); m.insert("Tm",0.0356); m.insert("Yb",0.248); m.insert("Lu",0.0381); }
        2 => { m.insert("La",0.32); m.insert("Ce",0.787); m.insert("Pr",0.112); m.insert("Nd",0.58); m.insert("Sm",0.185); m.insert("Eu",0.071); m.insert("Gd",0.256); m.insert("Tb",0.05); m.insert("Dy",0.343); m.insert("Ho",0.07); m.insert("Er",0.225); m.insert("Tm",0.03); m.insert("Yb",0.186); m.insert("Lu",0.034); }
        3 => { m.insert("La",0.33); m.insert("Ce",0.865); m.insert("Pr",0.112); m.insert("Nd",0.63); m.insert("Sm",0.203); m.insert("Eu",0.077); m.insert("Gd",0.276); m.insert("Tb",0.047); m.insert("Dy",0.343); m.insert("Ho",0.07); m.insert("Er",0.225); m.insert("Tm",0.03); m.insert("Yb",0.22); m.insert("Lu",0.034); }
        4 => { m.insert("La",2.5); m.insert("Ce",7.5); m.insert("Pr",1.32); m.insert("Nd",7.3); m.insert("Sm",2.63); m.insert("Eu",1.02); m.insert("Gd",3.68); m.insert("Tb",0.67); m.insert("Dy",4.55); m.insert("Ho",1.052); m.insert("Er",2.97); m.insert("Tm",0.46); m.insert("Yb",3.05); m.insert("Lu",0.46); }
        5 => { m.insert("La",31.0); m.insert("Ce",63.0); m.insert("Pr",7.1); m.insert("Nd",27.0); m.insert("Sm",4.7); m.insert("Eu",1.0); m.insert("Gd",4.0); m.insert("Tb",0.7); m.insert("Dy",3.9); m.insert("Ho",0.83); m.insert("Er",2.3); m.insert("Tm",0.3); m.insert("Yb",1.96); m.insert("Lu",0.31); }
        _ => {}
    }
    m
}

pub fn classify_k2o_sio2(x_sio2: f64, y_k2o: f64) -> &'static str {
    let k1 = (2.9 - 1.2) / (68.0 - 48.0);
    let k2 = (1.2 - 0.3) / (68.0 - 48.0);
    let y1 = 1.2 + (x_sio2 - 48.0) * k1;
    let y2 = 0.3 + (x_sio2 - 48.0) * k2;
    if y_k2o >= y1 { "High K" }
    else if y_k2o >= y2 { "Medium K" }
    else { "Low K" }
}

pub fn export_k2o_sio2_png(state: &crate::AppState, path: &std::path::Path) -> anyhow::Result<()> {
    export_k2o_sio2(state, path, false)
}

pub fn export_k2o_sio2_svg(state: &crate::AppState, path: &std::path::Path) -> anyhow::Result<()> {
    export_k2o_sio2(state, path, true)
}

fn export_k2o_sio2(state: &crate::AppState, path: &std::path::Path, svg: bool) -> anyhow::Result<()> {
    let headers = &state.raw_table.headers;
    let resolver = build_resolver(headers);
    let idx_sio2 = resolver.find_index("SiO2");
    let idx_k2o = resolver.find_index("K2O");
    if idx_sio2.is_none() || idx_k2o.is_none() { anyhow::bail!("Need SiO2/K2O"); }
    let (ix, iy) = (idx_sio2.unwrap(), idx_k2o.unwrap());

    let mut pts = Vec::<(f64, f64)>::new();
    for r in &state.raw_table.rows {
        if let (Some(x), Some(y)) = (resolver.parse_value(r, ix, true), resolver.parse_value(r, iy, true)) {
            pts.push((x, y));
        }
    }
    let k1 = (2.9 - 1.2) / (68.0 - 48.0);
    let k2 = (1.2 - 0.3) / (68.0 - 48.0);


    if svg {
        let root: DrawingArea<SVGBackend<'_>, _> = SVGBackend::new(path.to_str().unwrap(), (1200, 800)).into_drawing_area();
        return export_k2o_sio2_with_area(state, root, k1, k2);
    } else {
        let root: DrawingArea<BitMapBackend<'_>, _> = BitMapBackend::new(path.to_str().unwrap(), (1200, 800)).into_drawing_area();
        return export_k2o_sio2_with_area(state, root, k1, k2);
    }
}

fn export_k2o_sio2_with_area<B: DrawingBackend>(state: &crate::AppState, root_drawing: DrawingArea<B, Shift>, k1: f64, k2: f64) -> anyhow::Result<()>
where <B as DrawingBackend>::ErrorType: 'static {
    root_drawing.fill(&WHITE)?;

    let title_font = ("Microsoft YaHei, Arial, SimHei, DejaVu Sans", 28).into_font();
    let axis_font = ("Microsoft YaHei, Arial, SimHei, DejaVu Sans", 14).into_font();
    let legend_font = ("Microsoft YaHei, Arial, SimHei, DejaVu Sans", 14).into_font();

    let mut chart = ChartBuilder::on(&root_drawing)
        .margin(20)
        .caption("K2O-SiO2", title_font)
        .set_label_area_size(LabelAreaPosition::Left, 60)
        .set_label_area_size(LabelAreaPosition::Bottom, 60)
        .build_cartesian_2d(30.0..90.0, 0.0..6.0)?;

    chart.configure_mesh()
        .x_desc("SiO2 wt%")
        .y_desc("K2O wt%")
        .label_style(axis_font.clone())
        .axis_desc_style(axis_font.clone())
        .disable_x_mesh().disable_y_mesh()
        .draw()?;

    chart.draw_series(LineSeries::new((45..=85).map(|x| {
        let xf = x as f64; (xf, 1.2 + (xf - 48.0) * k1)
    }), &RED))?.label("High/Med 边界").legend(|(x,y)| PathElement::new(vec![(x,y), (x+20,y)], &RED));

    chart.draw_series(LineSeries::new((45..=85).map(|x| {
        let xf = x as f64; (xf, 0.3 + (xf - 48.0) * k2)
    }), &BLUE))?.label("Med/Low 边界").legend(|(x,y)| PathElement::new(vec![(x,y), (x+20,y)], &BLUE));

    // Recompute points and draw
    let headers = &state.raw_table.headers;
    let resolver = build_resolver(headers);
    let idx_sio2 = resolver.find_index("SiO2").unwrap();
    let idx_k2o = resolver.find_index("K2O").unwrap();
    // Grouped by label with colors
    let idx_label = resolver.find_index("Label");
    let idx_color = resolver.find_index("Color");
    use std::collections::BTreeMap;
    let mut groups: BTreeMap<String, Vec<(f64,f64)>> = BTreeMap::new();
    let mut gcolors: BTreeMap<String, RGBColor> = BTreeMap::new();
    let palette = plotters_palette();
    let mut n = 0usize;
    for r in &state.raw_table.rows {
        if let (Some(x), Some(y)) = (resolver.parse_value(r, idx_sio2, true), resolver.parse_value(r, idx_k2o, true)) {
            let label = idx_label.and_then(|i| r.get(i)).cloned().unwrap_or_else(|| "Group".to_string());
            groups.entry(label.clone()).or_default().push((x,y));
            if let Some(i) = idx_color { if let Some(cstr) = r.get(i) { if let Some(c) = parse_plotters_color(cstr) { gcolors.entry(label.clone()).or_insert(c); } } }
            if !gcolors.contains_key(&label) { gcolors.insert(label.clone(), palette[n % palette.len()].clone()); n+=1; }
        }
    }
    for (label, pts) in groups {
        let col = gcolors.get(&label).cloned().unwrap_or(BLACK);
        chart.draw_series(pts.into_iter().map(|(x,y)| Circle::new((x,y), 3, col.filled())))?
            .label(label)
            .legend(move |(x,y)| Circle::new((x,y), 4, col.filled()));
    }

    chart.configure_series_labels()
        .border_style(&BLACK)
        .background_style(&WHITE.mix(0.8))
        .label_font(legend_font)
        .position(SeriesLabelPosition::UpperRight)
        .draw()?;

    root_drawing.present()?;
    Ok(())
}

// ---------------- TAS ----------------
// Simplified TAS (total alkali vs SiO2) with same grouping/legend/export strategy

pub fn show_tas_plot(ui: &mut Ui, state: &crate::AppState) {
    let headers = &state.raw_table.headers;
    let resolver = build_resolver(headers);
    let ix = match resolver.find_index("SiO2") { Some(i)=>i, None=>{ ui.label("Need SiO2, Na2O, K2O"); return; } };
    let inao = match resolver.find_index("Na2O") { Some(i)=>i, None=>{ ui.label("Need Na2O"); return; } };
    let iko = match resolver.find_index("K2O") { Some(i)=>i, None=>{ ui.label("Need K2O"); return; } };

    use std::collections::BTreeMap;
    let mut groups: BTreeMap<String, Vec<[f64;2]>> = BTreeMap::new();
    let mut group_color: BTreeMap<String, Color32> = BTreeMap::new();
    let idx_label = resolver.find_index("Label");
    let idx_color = resolver.find_index("Color");
    for r in &state.raw_table.rows {
        let x = resolver.parse_value(r, ix, true);
        let y = resolver.parse_value(r, inao, true).zip(resolver.parse_value(r, iko, true)).map(|(a,b)| a+b);
        if let (Some(x), Some(y)) = (x,y) {
            let label = idx_label.and_then(|i| r.get(i)).cloned().unwrap_or_else(|| "Group".to_string());
            groups.entry(label.clone()).or_default().push([x,y]);
            if let Some(i) = idx_color { if let Some(cstr) = r.get(i) { if let Some(c) = parse_egui_color(cstr) { group_color.entry(label.clone()).or_insert(c); } } }
        }
    }

    let regions = tas_regions();

    Plot::new("tas").include_x(30.0).include_x(90.0).include_y(0.0).include_y(20.0).view_aspect(1.6).legend(Legend::default()).show(ui, |plot_ui| {
        for (_abbr, (_fullname, poly)) in regions.iter() {
            let mut closed = poly.clone(); if let Some(first) = closed.first().cloned() { closed.push(first); }
            plot_ui.line(Line::new(closed).color(Color32::from_gray(120)));
        }
        // place labels at polygon centroids; label text from TAS.json mapping per mode
        let mode_is_vol = state.tas_mode_is_volcanic;
        for (abbr, (_full, poly)) in &regions {
            if poly.is_empty() { continue; }
            let (mut cx, mut cy, mut n) = (0.0f64,0.0f64,0.0f64);
            for p in poly { cx += p[0]; cy += p[1]; n += 1.0; }
            cx /= n.max(1.0); cy /= n.max(1.0);
            // show abbreviation; tooltip can show full name if desired (future)
            plot_ui.text(PlotText::new(PlotPoint::new(cx, cy), abbr.as_str()));
        }
        let palette = egui_palette();
        let mut idx = 0usize;
        for (label, pts) in groups {
            let color = group_color.get(&label).cloned().unwrap_or_else(|| { let c = palette[idx % palette.len()]; idx+=1; c });
            // build points, compute classification and reflect in legend label
            let mut legend_label = label.clone();
            if let Some(p) = pts.first() { if let Some(class) = classify_tas(p[0], p[1]) { legend_label = format!("{} ({})", legend_label, class); } }
            let pp: PlotPoints = pts.into();
            plot_ui.points(Points::new(pp).color(color).radius(2.5).name(legend_label));
        }
    });
}

pub fn export_tas_png(state: &crate::AppState, path: &std::path::Path) -> anyhow::Result<()> { export_tas(state, path, false) }
pub fn export_tas_svg(state: &crate::AppState, path: &std::path::Path) -> anyhow::Result<()> { export_tas(state, path, true) }

fn export_tas(state: &crate::AppState, path: &std::path::Path, svg: bool) -> anyhow::Result<()> {
    let headers = &state.raw_table.headers;
    let resolver = build_resolver(headers);
    let ix = resolver.find_index("SiO2").ok_or_else(|| anyhow::anyhow!("Need SiO2"))?;
    let inao = resolver.find_index("Na2O").ok_or_else(|| anyhow::anyhow!("Need Na2O"))?;
    let iko = resolver.find_index("K2O").ok_or_else(|| anyhow::anyhow!("Need K2O"))?;
    if svg {
        let root: DrawingArea<SVGBackend<'_>, _> = SVGBackend::new(path.to_str().unwrap(), (1200, 800)).into_drawing_area();
        export_tas_with_area(state, root, ix, inao, iko)
    } else {
        let root: DrawingArea<BitMapBackend<'_>, _> = BitMapBackend::new(path.to_str().unwrap(), (1200, 800)).into_drawing_area();
        export_tas_with_area(state, root, ix, inao, iko)
    }
}

fn export_tas_with_area<B: DrawingBackend>(state: &crate::AppState, root: DrawingArea<B, Shift>, ix: usize, inao: usize, iko: usize) -> anyhow::Result<()>
where <B as DrawingBackend>::ErrorType: 'static {
    root.fill(&WHITE)?;
    let title_font = ("Microsoft YaHei, Arial, SimHei, DejaVu Sans", 28).into_font();
    let axis_font = ("Microsoft YaHei, Arial, SimHei, DejaVu Sans", 14).into_font();
    let legend_font = ("Microsoft YaHei, Arial, SimHei, DejaVu Sans", 14).into_font();
    let mut chart = ChartBuilder::on(&root).margin(20).caption("TAS", title_font)
        .set_label_area_size(LabelAreaPosition::Left, 60)
        .set_label_area_size(LabelAreaPosition::Bottom, 60)
        .build_cartesian_2d(30.0..90.0, 0.0..20.0)?;
    chart.configure_mesh().x_desc("SiO2 wt%").y_desc("Na2O+K2O wt%")
        .label_style(axis_font.clone()).axis_desc_style(axis_font.clone())
        .disable_x_mesh().disable_y_mesh()
        .draw()?;

    // boundary demo line
    // TAS region outlines (closed)
    for (_abbr, (_full, poly)) in tas_regions() {
        let mut closed: Vec<(f64,f64)> = poly.iter().copied().map(|p| (p[0],p[1])).collect();
        if let Some(first) = closed.first().cloned() { closed.push(first); }
        chart.draw_series(LineSeries::new(closed.into_iter(), RGBColor(120,120,120)))?;
    }
    // Abbreviation labels on export – use polygon centroid
    let mut text_elems: Vec<Text<'_, _, _>> = Vec::new();
    for (abbr, (_full, poly)) in tas_regions() {
        if poly.is_empty() { continue; }
        let (mut cx, mut cy, mut n) = (0.0f64,0.0f64,0.0f64);
        for p in &poly { cx += p[0]; cy += p[1]; n += 1.0; }
        cx /= n.max(1.0); cy /= n.max(1.0);
        text_elems.push(Text::new(abbr, (cx,cy), ("Microsoft YaHei, Arial, SimHei, DejaVu Sans", 12).into_font()));
    }
    chart.draw_series(text_elems)?;

    use std::collections::BTreeMap;
    let resolver = build_resolver(&state.raw_table.headers);
    let idx_label = resolver.find_index("Label");
    let idx_color = resolver.find_index("Color");
    let mut groups: BTreeMap<String, Vec<(f64,f64)>> = BTreeMap::new();
    let mut gcolors: BTreeMap<String, RGBColor> = BTreeMap::new();
    let palette = plotters_palette();
    let mut n = 0usize;
    for r in &state.raw_table.rows {
        let x = resolver.parse_value(r, ix, true);
        let y = resolver.parse_value(r, inao, true).zip(resolver.parse_value(r, iko, true)).map(|(a,b)| a+b);
        if let (Some(x), Some(y)) = (x,y) {
            let label = idx_label.and_then(|i| r.get(i)).cloned().unwrap_or_else(|| "Group".to_string());
            groups.entry(label.clone()).or_default().push((x,y));
            if let Some(i) = idx_color { if let Some(cstr) = r.get(i) { if let Some(c) = parse_plotters_color(cstr) { gcolors.entry(label.clone()).or_insert(c); } } }
            if !gcolors.contains_key(&label) { gcolors.insert(label.clone(), palette[n % palette.len()].clone()); n+=1; }
        }
    }
    for (label, pts) in groups {
        let col = gcolors.get(&label).cloned().unwrap_or(BLACK);
        chart.draw_series(pts.into_iter().map(|(x,y)| Circle::new((x,y), 3, col.filled())))?.label(label)
            .legend(move |(x,y)| Circle::new((x,y), 4, col.filled()));
    }
    chart.configure_series_labels().border_style(&BLACK).background_style(&WHITE.mix(0.8)).label_font(legend_font)
        .position(SeriesLabelPosition::UpperRight).draw()?;
    root.present()?; Ok(())
}

// ---------------- REE ----------------
// REE normalized spider plot (log-scale-like labelling simulated by ticks)

pub fn show_ree_plot(ui: &mut Ui, state: &crate::AppState) {
    // Minimal: plot La..Lu as 1..14 x, y as value (assume already normalized by user)
    let headers = &state.raw_table.headers;
    let resolver = build_resolver(headers);
    let elems = ["La","Ce","Pr","Nd","Sm","Eu","Gd","Tb","Dy","Ho","Er","Tm","Yb","Lu"];
    // quick presence check
    if !elems.iter().any(|e| resolver.find_index(e).is_some()) { ui.label("Need REE columns La..Lu"); return; }

    use std::collections::BTreeMap;
    let mut groups: BTreeMap<String, Vec<[f64;2]>> = BTreeMap::new();
    let mut group_color: BTreeMap<String, Color32> = BTreeMap::new();
    let idx_label = resolver.find_index("Label");
    let idx_color = resolver.find_index("Color");
    let std = ree_standard_values(state.ree_standard_idx);
    for r in &state.raw_table.rows {
        let label = idx_label.and_then(|i| r.get(i)).cloned().unwrap_or_else(|| "Group".to_string());
        let mut series = Vec::new();
        for (i, e) in elems.iter().enumerate() {
            if let Some(ix) = resolver.find_index(e) { if let Some(mut v) = resolver.parse_value(r, ix, false) {
                let denom = std.get(*e).copied().unwrap_or(1.0); if denom>0.0 { v /= denom; }
                if v>0.0 { series.push([i as f64 + 1.0, v.log10()]); }
            } }
        }
        if !series.is_empty() { groups.entry(label.clone()).or_default().extend(series); }
        if let Some(i) = idx_color { if let Some(cstr) = r.get(i) { if let Some(c) = parse_egui_color(cstr) { group_color.entry(label.clone()).or_insert(c); } } }
    }
    // Determine y-range and draw element names on x-axis
    let mut miny = 1e9f64; let mut maxy = -1e9f64;
    for (_l, pts) in &groups { for p in pts { miny = miny.min(p[1]); maxy = maxy.max(p[1]); } }
    let axis_y = (miny - 0.2);
    Plot::new("ree").include_x(0.5).include_x(14.5).include_y(miny).include_y(maxy).legend(Legend::default()).show(ui, |plot_ui| {
        // x labels
        let names = ["La","Ce","Pr","Nd","Sm","Eu","Gd","Tb","Dy","Ho","Er","Tm","Yb","Lu"];
        for (i, name) in names.iter().enumerate() { plot_ui.text(PlotText::new(PlotPoint::new((i as f64)+1.0, axis_y), *name)); }
        // standard name annotation
        let std_name = REE_STANDARD_NAMES.get(state.ree_standard_idx).copied().unwrap_or(REE_STANDARD_NAMES[0]);
        plot_ui.text(PlotText::new(PlotPoint::new(1.2, (maxy + 0.1)), format!("Standard: {}", std_name)));
        let palette = egui_palette();
        let mut idx = 0usize;
        for (label, pts) in groups {
            let color = group_color.get(&label).cloned().unwrap_or_else(|| { let c = palette[idx % palette.len()]; idx+=1; c });
            let pp: PlotPoints = pts.into();
            plot_ui.line(Line::new(pp).color(color).name(label));
        }
    });
}

pub fn export_ree_png(state: &crate::AppState, path: &std::path::Path) -> anyhow::Result<()> { export_ree(state, path, false) }
pub fn export_ree_svg(state: &crate::AppState, path: &std::path::Path) -> anyhow::Result<()> { export_ree(state, path, true) }

fn export_ree(state: &crate::AppState, path: &std::path::Path, svg: bool) -> anyhow::Result<()> {
    let headers = &state.raw_table.headers;
    let resolver = build_resolver(headers);
    let elems = ["La","Ce","Pr","Nd","Sm","Eu","Gd","Tb","Dy","Ho","Er","Tm","Yb","Lu"];
    if svg {
        let root: DrawingArea<SVGBackend<'_>, _> = SVGBackend::new(path.to_str().unwrap(), (1200, 800)).into_drawing_area();
        export_ree_with_area(state, root, &resolver, &elems)
    } else {
        let root: DrawingArea<BitMapBackend<'_>, _> = BitMapBackend::new(path.to_str().unwrap(), (1200, 800)).into_drawing_area();
        export_ree_with_area(state, root, &resolver, &elems)
    }
}

fn export_ree_with_area<B: DrawingBackend>(state: &crate::AppState, root: DrawingArea<B, Shift>, resolver: &HeaderResolver, elems: &[&str]) -> anyhow::Result<()>
where <B as DrawingBackend>::ErrorType: 'static {
    root.fill(&WHITE)?;
    let title_font = ("Microsoft YaHei, Arial, SimHei, DejaVu Sans", 28).into_font();
    let axis_font = ("Microsoft YaHei, Arial, SimHei, DejaVu Sans", 14).into_font();
    let legend_font = ("Microsoft YaHei, Arial, SimHei, DejaVu Sans", 14).into_font();
    // Build groups first to compute dynamic y-range and paint x tick labels as element names
    use std::collections::BTreeMap;
    let idx_label = resolver.find_index("Label");
    let idx_color = resolver.find_index("Color");
    let mut groups: BTreeMap<String, Vec<(f64,f64)>> = BTreeMap::new();
    let mut gcolors: BTreeMap<String, RGBColor> = BTreeMap::new();
    let palette = plotters_palette();
    let mut n = 0usize;
    let std = ree_standard_values(state.ree_standard_idx);
    for r in &state.raw_table.rows {
        let mut series: Vec<(f64,f64)> = Vec::new();
        for (i, e) in elems.iter().enumerate() {
            if let Some(ix) = resolver.find_index(e) {
                if let Some(mut v) = resolver.parse_value(r, ix, false) {
                    let denom = std.get(e).copied().unwrap_or(1.0);
                    if denom>0.0 { v /= denom; }
                    if v>0.0 { v = v.max(1e-12); series.push((i as f64 + 1.0, v.log10())); }
                }
            }
        }
        if series.is_empty() { continue; }
        let label = idx_label.and_then(|i| r.get(i)).cloned().unwrap_or_else(|| "Group".to_string());
        groups.entry(label.clone()).or_default().extend(series);
        if let Some(i) = idx_color { if let Some(cstr) = r.get(i) { if let Some(c) = parse_plotters_color(cstr) { gcolors.entry(label.clone()).or_insert(c); } } }
        if !gcolors.contains_key(&label) { gcolors.insert(label.clone(), palette[n % palette.len()].clone()); n+=1; }
    }

    // dynamic y range from UI-equivalent data
    let mut miny = 1e9f64; let mut maxy = -1e9f64;
    for (_l, pts) in &groups { for p in pts { miny = miny.min(p.1); maxy = maxy.max(p.1); } }
    if !(miny < maxy) { miny = -3.0; maxy = 3.0; }

    let mut chart = ChartBuilder::on(&root).margin(20).caption("REE pattern", title_font)
        .set_label_area_size(LabelAreaPosition::Left, 60)
        .set_label_area_size(LabelAreaPosition::Bottom, 60)
        .build_cartesian_2d(0.5..14.5, miny..maxy)?;
    chart.configure_mesh().x_desc("La..Lu")
        .y_desc("log10(value/standard)")
        .label_style(axis_font.clone()).axis_desc_style(axis_font.clone())
        .disable_x_mesh().disable_y_mesh()
        .x_labels(0)
        .draw()?;
    // draw x-axis element labels explicitly at each integer position
    let x_label_font = ("Microsoft YaHei, Arial, SimHei, DejaVu Sans", 12).into_font();
    chart.draw_series((1..=14).map(|i| {
        let name = elems[i-1];
        Text::new(name.to_string(), (i as f64, miny), x_label_font.clone())
    }))?;

    // groups already prepared above
    for (label, pts) in groups {
        let col = gcolors.get(&label).cloned().unwrap_or(BLACK);
        chart.draw_series(LineSeries::new(pts.into_iter(), col))?.label(label)
            .legend(move |(x,y)| PathElement::new(vec![(x,y), (x+20,y)], &col));
    }
    // annotate chosen standard name near the top-left inside plot area
    let std_name = REE_STANDARD_NAMES.get(state.ree_standard_idx).copied().unwrap_or(REE_STANDARD_NAMES[0]);
    let annot_font = ("Microsoft YaHei, Arial, SimHei, DejaVu Sans", 14).into_font();
    let y_annot = maxy - (maxy - miny) * 0.05;
    chart.draw_series(std::iter::once(Text::new(format!("Standard: {}", std_name), (1.0f64, y_annot), annot_font)))?;
    chart.configure_series_labels().border_style(&BLACK).background_style(&WHITE.mix(0.8)).label_font(legend_font)
        .position(SeriesLabelPosition::UpperRight).draw()?;
    root.present()?; Ok(())
}


