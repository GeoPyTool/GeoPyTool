use egui::{Color32, Ui};
use egui_plot::{Line, Plot, PlotPoints, Points, Legend, MarkerShape};
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

    Plot::new("k2o_sio2").include_x(30.0).include_x(90.0).view_aspect(1.6).legend(Legend::default()).show(ui, |plot_ui| {
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


