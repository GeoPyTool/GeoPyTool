use egui::{Color32, Ui};
use egui_plot::{Line, Plot, PlotPoints, Points, Legend, MarkerShape, Text as PlotText, PlotPoint};
use serde::{Deserialize, Serialize};

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

fn tas_regions() -> Vec<(&'static str, Vec<[f64;2]>)> {
    // Ported from geopytool TAS.py LocationAreas / boundaries for plutonic/volcanic mix
    vec![
        ("Foidolite", vec![[41.0, 3.0], [37.0, 3.0], [35.0, 9.0], [37.0, 14.0], [52.5, 18.0], [52.5, 14.0], [48.4, 11.5], [45.0, 9.4], [41.0, 7.0]]),
        ("Peridotgabbro", vec![[41.0, 0.0], [41.0, 3.0], [45.0, 3.0], [45.0, 0.0]]),
        ("Foid Gabbro", vec![[41.0, 3.0], [41.0, 7.0], [45.0, 9.4], [49.4, 7.3], [45.0, 5.0], [45.0, 3.0]]),
        ("Foid Monzodiorite", vec![[45.0, 9.4], [48.4, 11.5], [53.0, 9.3], [49.4, 7.3]]),
        ("Foid Monzosyenite", vec![[48.4, 11.5], [52.5, 14.0], [57.6, 11.7], [53.0, 9.3]]),
        ("Foid Syenite", vec![[52.5, 14.0], [52.5, 18.0], [57.0, 18.0], [63.0, 16.2], [61.0, 13.5], [57.6, 11.7]]),
        ("Gabbro Bs", vec![[45.0, 0.0], [45.0, 2.0], [52.0, 5.0], [52.0, 0.0]]),
        ("Gabbro Ba", vec![[45.0, 2.0], [45.0, 5.0], [52.0, 5.0]]),
        ("Monzogabbro", vec![[45.0, 5.0], [49.4, 7.3], [52.0, 5.0]]),
        ("Monzodiorite", vec![[49.4, 7.3], [53.0, 9.3], [57.0, 5.9], [52.0, 5.0]]),
        ("Monzonite", vec![[53.0, 9.3], [57.6, 11.7], [61.0, 8.6], [63.0, 7.0], [57.0, 5.9]]),
        ("Syenite", vec![[57.6, 11.7], [61.0, 13.5], [63.0, 16.2], [71.8, 13.5], [61.0, 8.6]]),
        ("Quartz Monzonite", vec![[61.0, 8.6], [71.8, 13.5], [69.0, 8.0], [63.0, 7.0]]),
        ("Gabbroic Diorite", vec![[52.0, 0.0], [52.0, 5.0], [57.0, 5.9], [57.0, 0.0]]),
        ("Diorite", vec![[57.0, 0.0], [57.0, 5.9], [63.0, 7.0], [63.0, 0.0]]),
        ("Granodiorite", vec![[63.0, 0.0], [63.0, 7.0], [69.0, 8.0], [77.3, 0.0]]),
        ("Granite", vec![[77.3, 0.0], [69.0, 8.0], [71.8, 13.5], [85.9, 6.8], [87.5, 4.7]]),
        ("Quartzolite", vec![[77.3, 0.0], [87.5, 4.7], [90.0, 4.7], [90.0, 0.0]]),
    ]
}

fn classify_tas(x_sio2: f64, y_alk: f64) -> Option<&'static str> {
    let regions = tas_regions();
    for (name, poly) in regions {
        if point_in_polygon(x_sio2, y_alk, &poly) { return Some(name); }
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
        for (name, poly) in regions.iter() {
            let mut closed = poly.clone(); if let Some(first) = closed.first().cloned() { closed.push(first); }
            plot_ui.line(Line::new(closed).color(Color32::from_gray(120)).name(format!("{}", name)));
        }
        // Abbreviation labels placed similar to original
        let labels = vec![
            ("F", [39.0,10.0]), ("Pc", [43.0,1.5]), ("U1", [44.0,6.0]), ("Ba", [47.5,3.5]), ("Bs", [49.5,1.5]),
            ("S1", [49.0,5.2]), ("U2", [49.0,9.5]), ("O1", [54.0,3.0]), ("S2", [53.0,7.0]), ("U3", [53.0,12.0]),
            ("O2", [60.0,4.0]), ("S3", [57.6,11.7]), ("Ph", [61.0,8.6]), ("O3", [67.0,5.0]), ("T", [65.0,12.0]),
            ("Td", [67.0,9.0]), ("R", [75.0,9.0]), ("Q", [85.0,1.0]), ("S/N/L", [55.0,18.5])
        ];
        for (t, [x,y]) in labels { plot_ui.text(PlotText::new(PlotPoint::new(x, y), t)); }
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
        .label_style(axis_font.clone()).axis_desc_style(axis_font.clone()).draw()?;

    // boundary demo line
    // TAS region outlines (closed)
    for (_name, poly) in tas_regions() {
        let mut closed: Vec<(f64,f64)> = poly.iter().copied().map(|p| (p[0],p[1])).collect();
        if let Some(first) = closed.first().cloned() { closed.push(first); }
        chart.draw_series(LineSeries::new(closed.into_iter(), RGBColor(120,120,120)))?;
    }

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
    let mut chart = ChartBuilder::on(&root).margin(20).caption("REE pattern", title_font)
        .set_label_area_size(LabelAreaPosition::Left, 60)
        .set_label_area_size(LabelAreaPosition::Bottom, 60)
        .build_cartesian_2d(1.0..15.0, -3.0..3.0)?;
    chart.configure_mesh().x_desc("La..Lu index").y_desc("log10(value)")
        .label_style(axis_font.clone()).axis_desc_style(axis_font.clone()).draw()?;

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
    for (label, pts) in groups {
        let col = gcolors.get(&label).cloned().unwrap_or(BLACK);
        chart.draw_series(LineSeries::new(pts.into_iter(), col))?.label(label)
            .legend(move |(x,y)| PathElement::new(vec![(x,y), (x+20,y)], &col));
    }
    chart.configure_series_labels().border_style(&BLACK).background_style(&WHITE.mix(0.8)).label_font(legend_font)
        .position(SeriesLabelPosition::UpperRight).draw()?;
    root.present()?; Ok(())
}


