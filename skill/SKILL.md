---
name: epidemic-dataviz
description: Apply the organization's epidemic data visualization standards when creating ANY chart, plot, dashboard, or visualization related to epidemic, public health, or disease surveillance data. Use this skill whenever the user requests visualizations involving case counts, mortality, vaccination, variants, hospitalization, age distribution, geographic spread, R/Rt values, or any other epidemiological metric — even if they don't explicitly mention "guideline" or "standards". This skill covers color palettes (sage green primary #739A6D with strict ordering: green → blue → yellow → neutral → red accents), chart proportions (bar widths, line thickness), chart type selection, accessibility requirements (WCAG AA), and tool-specific implementations for Python (matplotlib/seaborn/plotly), JavaScript (Chart.js, D3, Plotly.js), R (ggplot2), Excel/PowerBI themes, and HTML/CSS.
---

# Epidemic Data Visualization Guideline

This skill encodes the organization's standards for visualizing epidemic and public health data. All charts produced for internal reports, dashboards, presentations, and public-facing materials must conform to these standards.

## How to Use This Skill

1. **For specific chart types**, read the corresponding file in `references/` first — they contain detailed rules, common pitfalls, and ready-to-use code patterns specific to that chart type. See the "Reference Files" table at the bottom of this document.
2. **For general principles** (color system, combination patterns, accessibility), read this SKILL.md.
3. **For Python implementations**, import from `scripts/epidemic_palette.py`:
   ```python
   from epidemic_palette import PRIMARY, CATEGORICAL, apply_style, trailing_ma
   apply_style()
   ```
4. **For visual reference**, see `assets/examples/*.png` (pre-generated examples).

## Quick Decision Tree

When asked to create a chart, follow this order:

1. **Identify the question type** (comparison, trend, composition, distribution, ranking, etc.) → choose chart type from §3
2. **Pick a combination pattern** based on whether there's a focus object AND whether series are ordinal → §2
3. **Apply colors in the prescribed priority order** (green → blue → yellow → neutral) → §1
4. **Apply proportions and styling** specific to that chart type → §4
5. **If data carries estimates with intervals** (predictions, sampling CIs, asymmetric ratios) → apply uncertainty modifier → §4.6
6. **Verify accessibility** (contrast, color blindness, direct labels) → §6

## 1. Color System

### 1.1 Primary Color (Sage Green)

The organizational primary color is **`#739A6D`** (Sage Green). All other colors derive from or harmonize with it.

Primary scale (use `*-500` as base, `*-600`+ for text, `*-300`- for backgrounds):
```
p-50:  #F6F9F6   p-100: #E8EEE7   p-200: #D1DECF   p-300: #B4C9B1
p-400: #91B08C   p-500: #739A6D ← PRIMARY
p-600: #5D7F58   p-700: #496345   p-800: #374C34   p-900: #253423
```

**Important**: `#739A6D` has only 3.20 contrast ratio against white. Use `#5D7F58` (p-600) or darker for text and thin lines.

### 1.2 Categorical Palette (Priority Order)

Use in this exact order. Take only what you need (2 categories → use first 2; never skip).

| Order | Name | HEX | When |
|-------|------|-----|------|
| 1 | Sage (Primary) | `#739A6D` | Always the "main" object |
| 2 | Slate Blue | `#587A9D` | Second category |
| 3 | Mustard | `#C8A041` | Third (for lines, use `#A8821F` instead — see §4.2) |
| 4 | Teal | `#49888D` | Fourth |
| 5 | Bronze | `#916E46` | Fifth |
| 6 | Plum | `#955F71` | Sixth |

**Maximum 6 categories.** Beyond that, merge to "Other" (use Neutral `#CACFC9`).

### 1.3 Accent Colors (NEVER use as a regular categorical)

Red/orange family is reserved for emphasis. Use sparingly (< 20% of elements in a chart).

| Intensity | Name | HEX | When |
|-----------|------|-----|------|
| Strongest | Alert Red | `#BE373C` | Above warning threshold; critical anomaly |
| Strong | Terracotta | `#B5584A` | Diverging palette negative end; strong contrast |
| Soft | Clay | `#B87B61` | Gentle emphasis; reverse trend without alarm |
| Soft | Caution Amber | `#D2962D` | Approaching threshold; advisory |

**Epidemic context rule**: Do NOT color entire bars red even when case counts are high. Red on case-count bars amplifies panic. Color only the portion exceeding threshold, or use a separate threshold line.

### 1.4 Neutral Scale

Slightly warm gray with green undertone, harmonizes with primary:
```
n-50:  #FAFAFA   n-100: #F2F3F1   n-200: #E4E7E4   n-300: #CACFC9
n-400: #A2ABA0   n-500: #7A8778   n-600: #5D675B   n-700: #444C43
n-800: #2C312B   n-900: #181B18
```

Use `n-400` for reference/comparison lines, `n-700` for body text, `n-300` for gridlines.

### 1.5 Semantic Colors (KPI / status only)

| Status | HEX | Use |
|--------|-----|-----|
| Success | `#54734F` | Target met; positive indicator |
| Warning | `#D2962D` | Near threshold |
| Danger | `#BE373C` | Below target; anomaly |
| Info | `#477A9E` | Reference; neutral note |

### 1.6 Sequential & Diverging (heatmaps, choropleth)

Sequential (low → high):
```
#F1F5F0 → #D4E0D2 → #AEC5AB → #8BAC86 → #6A9164 → #506D4B → #354832
```

Diverging (negative ← center → positive):
```
#476043 → #71936C → #B2BFB0 → #F2F3F2 → #D8C5C0 → #BC8776 → #965440
```

**Diverging center must NOT be pure white** (`#F2F3F2` gray-green instead) — zero-value cells would otherwise look like "no data".

## 2. Combination Patterns

Pick one pattern per chart based on intent.

### Pattern A — Primary + Neutral (most common)
Highlight ONE object against background. Use for: focus vs. average, this-wave vs. historical, our-region vs. others.

```
Focus:     #739A6D (or #5D7F58 for lines)
Reference: #A2ABA0 (Neutral 400, often dashed)
```

### Pattern B — 2 Primary + Neutral
Two main objects + one baseline. Use for: two key metrics + a reference line.

```
Object 1:  #739A6D
Object 2:  #587A9D (or another cat color)
Baseline:  #A2ABA0
```

### Pattern C — Pure Categorical
All categories equal weight. Use cat-1 through cat-N in order.

### Pattern D — Categorical + Accent
Most categories normal + one needs warning. Use cat colors + Alert Red / Terracotta for the warning subset.

### Pattern E — Monochrome Scale (few categories or ordinal)
Use the primary-color scale instead of categorical hues. Two main triggers:

1. **Series have a natural order** (severity, age, time periods, doses) — color depth = magnitude
2. **2–3 categories where you want subdued visuals** — fewer hues = more focus on data shape

For ordinal data, light→dark MUST correspond to weak→strong / past→present.

```python
from epidemic_palette import MONOCHROME
MONOCHROME["focus_2"]    # focus + reference (2 series)
MONOCHROME["scale_3"]    # 3 series (ordered or just minimalist)
MONOCHROME["scale_4"]    # 4 ordered series (waves over time)
MONOCHROME["scale_5"]    # 5 series
MONOCHROME["scale_6"]    # 6 series (with deliberate luminance gaps)
MONOCHROME["scale_7"]    # full week / 7 age bins
```

**Decision tree**:
1. Are categories ordinal (severity/age/time/doses)? → Pattern E
2. Are there 2–3 categories and you want subdued visuals? → Pattern E
3. Are there 6+ categories with no natural order? → Pattern C (categorical)
4. Do categories need to feel "opposed/independent"? → Pattern C

Examples:
- Severity (mild/moderate/severe) → Pattern E (ordinal)
- Doses (1st/2nd/3rd) → Pattern E (ordinal)
- Waves over time → Pattern E (current deepest, thickest)
- Male vs Female (2 categories) → Pattern E (few + subdued)
- Variants (JN.1/KP.2/KP.3) → Pattern C (treated as distinct strains)
- 6 departments → Pattern C (parallel, no order)
- Cities → Pattern C, or Pattern A focusing one

**When stacking with Pattern E**: place the **darkest color at the base**. Deep colors anchor the chart visually, and the "intensity baseline" makes cross-category comparison (e.g., severity gradient across ages) immediate.

**When in doubt, default to Pattern A.** It's the safest choice and works for most epidemic charts.

## 3. Chart Selection (Epidemic Context)

| Question | Recommended | Avoid |
|----------|-------------|-------|
| Daily new (cases, deaths) | Column chart + 7-day MA line | Pure line (hides daily variation) |
| Long-term trend / waves | Line chart, area chart | Bars (>30 points get crowded) |
| Year-over-year same period | Line chart with historical range band | Side-by-side bars |
| Region comparison | Horizontal bar (sorted), choropleth | Unnormalized absolute counts |
| Variant / vaccine composition | 100% stacked bar over time | Single pie chart |
| Age × severity | Pyramid chart, grouped bars | 3D charts |
| Single-time composition | Horizontal stacked bar (preferred), pie (2–4 categories only) | 3D pie; >4 category pie |
| Key KPI | Big number + small trend | Gauge |
| Excess mortality / baseline | Line + reference line + shaded historical range | Solo current-year line |

## 4. Chart-Specific Standards

### 4.1 Bar Chart Proportions (Chart.js / matplotlib width)

`barPercentage × categoryPercentage` = actual bar width as fraction of category slot.

| Type | `barPercentage` | `categoryPercentage` | matplotlib `width` |
|------|----------------|---------------------|-------------------|
| Single bars (clear separation) | 0.55 | 0.85 | 0.6 |
| Dense daily time-series | 0.75 | 0.9 | 0.75 |
| Stacked bars | 0.6 | 0.85 | 0.65 |
| Grouped bars (intra-group gap + larger inter-group) | 0.85 | 0.75 | bar_w=0.23, offset=0.25 (3 bars) |
| Horizontal ranking | 0.7 | 0.85 | 0.7 |

**Grouped bar spacing**: bars within a group must have a small 1–2px gap (not flush together — otherwise they read as a single multicolor bar). Inter-group spacing should be visibly larger. In matplotlib, set `bar_w` slightly smaller than `offset`, e.g. `bar_w=0.23, offset=0.25` for 3 bars per group.

### 4.1.5 Grid Lines

- **Default**: horizontal-only grid (Y-axis reading direction for bars/lines)
- Scatter, bubble, and other charts with continuous X & Y need both-axis grid — enable manually with `ax.grid(True, axis="both")`
- The `apply_style()` helper in `epidemic_palette.py` sets `axes.grid.axis = "y"` by default

### 4.1.6 Omit Y-axis When Bars Are Labelled

If every bar shows its value as a direct label, the Y-axis ticks and label become visual redundancy. Hide them:

```python
from epidemic_palette import hide_y_axis
# After drawing labelled bars:
hide_y_axis(ax)  # hides Y ticks, label, axis line, and horizontal gridlines
```

For horizontal bars with labels at bar ends, hide the X-axis equivalently.

### 4.1.7 Date Axes (time-series charts)

For any chart with a time axis, **always use `datetime.date` or `datetime.datetime` objects, never strings or integers**. Strings get treated as equidistant categories and lose all temporal meaning (e.g. weekend effects, gaps).

Use the provided helpers:

```python
from datetime import date, timedelta
from epidemic_palette import (
    format_date_axis_daily,    # ≤ 5 weeks of daily data: "MM/DD" every N days
    format_date_axis_weekly,   # 1-6 months: weekly markers, "MM/DD"
    format_date_axis_monthly,  # cross-month/year: "2025\n1月, 2月, 3月..."
)

dates = [date(2026, 5, 1) + timedelta(days=i) for i in range(28)]
ax.bar(dates, values, width=0.75)
format_date_axis_daily(ax, interval=4)  # label every 4 days
```

These helpers use `matplotlib.dates` internally and handle locale-appropriate formatting (Chinese month names with year on January).

### 4.2 Line Chart Visibility

Lines look thinner than bars at the same color. Use darkened variants:

| Series | Bar/fill color | Line color | Reason |
|--------|--------------|-----------|--------|
| Primary | `#739A6D` (p-500) | **`#5D7F58`** (p-600) | p-500 only 3.20 contrast |
| Slate Blue | `#587A9D` | `#587A9D` | Original OK (4.48) |
| Mustard | `#C8A041` | **`#A8821F`** | Original only 2.45 contrast — FAILS for lines |
| Reference | `#A2ABA0` | `#A2ABA0` | Reference should recede |

Line widths:
- Primary series: 2.5–3px
- Secondary: 2px
- Reference / comparison: 1.5px, often dashed

Add point markers at: start, end, extremes. For multi-series, use **different point shapes** (circle, square, triangle) to aid color-blind users.

### 4.3 Moving Average

For "daily cases + 7-day MA" charts:

- Use **trailing** moving average (i-day MA = mean of `i-6` to `i`, i.e. today + previous 6 days) — matches WHO/CDC/JHU conventions and works for live dashboards (no future data required)
- Need at least **3 weeks (21+ days) of data** for the MA to be meaningful
- For the first `window-1` days, use an adaptive shorter window (cumulative from day 1) rather than `null` to avoid line breaks
- MA line color: use the DARK variant of primary (`#374C34`, p-800) for strong layering over light bars

```python
# Python: trailing MA with adaptive early window
def trailing_ma(data, window=7):
    n = len(data)
    return [
        round(sum(data[max(0, i - window + 1):i + 1]) /
              min(window, i + 1))
        for i in range(n)
    ]
```

### 4.4 Y-axis Rules

- Bar charts: Y-axis MUST start at zero. Truncating exaggerates differences and is dishonest.
- Line charts: zero baseline preferred but optional if the variation is what matters (annotate the choice).
- Percentage data: 0–100 fixed, or 0–max if max < 30%.

### 4.5 Pie Charts (CONDITIONAL USE)

Only use when ALL of these hold:
- 2–4 categories
- Sums to 100%
- Single time point
- Differences between slices ≥ 5%

Otherwise use horizontal 100% stacked bar. Requirements when used:
- Direct labels on slices (category + %), no reliance on legend
- No 3D effects
- Sort slices largest → smallest, clockwise from 12 o'clock
- Use categorical palette in order (don't pick "pretty" colors)

### 4.6 Uncertainty Modifier (RFC 2026-06-01)

When data carries estimates with intervals (predictions with 50/95% CI, sampling estimates, log-space ratios), **apply the uncertainty modifier on top of existing Pattern A/B/D**. Do NOT create a separate "uncertainty pattern".

Two main visual forms:

- **Gradient fill band** for **time-series + forecasts**. Use the series' light shade (e.g. `PRIMARY_LIGHT` `#B4C9B1` at alpha 0.30 for the 95% CI; alpha 0.40 inner for 50% CI). Forecast segment uses dashed point-estimate line (`dashes=[6,3]`) + vertical annotation marking the forecast start. Past observations remain solid line, NO band on observed segment.
- **Error bars** for **few-category point estimates** (< 6 groups). Bar uses series primary; error bar uses `PRIMARY_DARKER` `#374C34` (NOT neutral grey — visually indistinguishable from bar). matplotlib `capsize=4` recommended; cap width visually 20-50% of bar width.

**MUST**: For asymmetric CIs (log-space estimates like RR/OR/HR), pass upper and lower bounds **separately** (`yerr=[lower_dist, upper_dist]`). NEVER force-symmetrize — doing so can flip a significant result (lower bound 1.4 → 0.95, crossing the null line of 1.0).

Full rules, code examples, and the don't/do table: `references/M1-uncertainty-modifier.md`.

## 5. Typography

Sizes (for charts):

| Element | Size | Weight |
|---------|------|--------|
| Chart title | 16–18px | 600 |
| Axis label | 12–13px | 500 |
| Axis tick | 11–12px | 400 |
| Legend | 12px | 400 |
| Data label | 11px | 500 |
| Source/footnote | 10–11px | 400 |

Fonts:
- Chinese: Noto Sans TC (body), Noto Serif TC (titles only)
- English/digits: Noto Sans, Inter, IBM Plex Sans
- **Always use `tabular-nums` for numeric data** so columns align:
  ```css
  font-variant-numeric: tabular-nums;
  font-feature-settings: "tnum";
  ```

## 6. Accessibility (WCAG AA)

- **Body text contrast ≥ 4.5:1** against background
- **Non-text (lines, bars) contrast ≥ 3:1**
- **Don't rely on color alone** — use shapes, patterns, direct labels in addition to color
- The categorical palette has been tested against common color-blindness types (Protanopia, Deuteranopia, Tritanopia); it remains distinguishable
- Avoid red+green opposition (common in epidemic charts) — pair with shape or label
- Provide alt text for charts describing the **finding**, not the visual ("Cases peaked at 4,020 on 5/21" not "A bar chart with green bars")

## 7. Tool-Specific Implementations

### 7.1 Python (matplotlib, seaborn, plotly)

```python
# epidemic_palette.py
PRIMARY      = "#739A6D"
LINE_PRIMARY = "#5D7F58"  # darker variant for thin lines
LINE_MUSTARD = "#A8821F"  # darker yellow for lines

CATEGORICAL = [
    "#739A6D", "#587A9D", "#C8A041",
    "#49888D", "#916E46", "#955F71",
]
ACCENT = {
    "alert":      "#BE373C",
    "terracotta": "#B5584A",
    "clay":       "#B87B61",
    "caution":    "#D2962D",
}
SEMANTIC = {
    "success": "#54734F", "warning": "#D2962D",
    "danger":  "#BE373C", "info":    "#477A9E",
}

# matplotlib setup
import matplotlib.pyplot as plt
plt.rcParams["axes.prop_cycle"]  = plt.cycler(color=CATEGORICAL)
plt.rcParams["font.family"]      = "Noto Sans TC"
plt.rcParams["axes.spines.top"]   = False
plt.rcParams["axes.spines.right"] = False
plt.rcParams["axes.grid"]        = True
plt.rcParams["grid.color"]       = "#E4E7E4"
plt.rcParams["grid.linewidth"]   = 0.6
```

For matplotlib bars, use `width=0.6` (single) or `width=0.75` (dense daily).
For line plots with the primary series, pass `color=LINE_PRIMARY, linewidth=2.5`.

### 7.2 JavaScript (Chart.js)

```javascript
const PRIMARY      = '#739A6D';
const PRIMARY_DARK = '#5D7F58';
const PRIMARY_800  = '#374C34';
const CAT = ['#739A6D','#587A9D','#C8A041','#49888D','#916E46','#955F71'];

Chart.defaults.font.family = "'Noto Sans TC', sans-serif";
Chart.defaults.font.size = 11;
Chart.defaults.color = '#444C43';
Chart.defaults.borderColor = '#E4E7E4';
Chart.defaults.plugins.legend.labels.usePointStyle = true;

// Daily column dataset
{ type:'bar', backgroundColor: PRIMARY,
  barPercentage: 0.75, categoryPercentage: 0.9 }

// 7-day MA line dataset (centered)
{ type:'line', borderColor: PRIMARY_800,
  borderWidth: 2.5, tension: 0.35, pointRadius: 0 }
```

### 7.3 R (ggplot2)

```r
epi_colors <- c("#739A6D", "#587A9D", "#C8A041",
                "#49888D", "#916E46", "#955F71")

library(ggplot2)
theme_epi <- function() {
  theme_minimal(base_family = "Noto Sans TC", base_size = 11) +
  theme(
    panel.grid.major = element_line(color = "#E4E7E4"),
    panel.grid.minor = element_blank(),
    axis.line = element_line(color = "#CACFC9"),
    plot.title = element_text(family = "Noto Serif TC",
                              face = "bold", size = 16)
  )
}

# scale_*_manual(values = epi_colors)
```

### 7.4 Excel / Office

Theme Colors → Custom Colors → set Accents 1–6 to:
```
Accent 1: #739A6D  Accent 2: #587A9D  Accent 3: #C8A041
Accent 4: #49888D  Accent 5: #916E46  Accent 6: #955F71
```

Once configured, the entire Office suite (Word, Excel, PowerPoint) applies these by default.

### 7.5 Power BI

Use the `epidemic-dataviz-theme.json` file (in the skill's assets):

```json
{
  "name": "Epidemic Data Viz Theme",
  "dataColors": ["#739A6D","#587A9D","#C8A041","#49888D",
                 "#916E46","#955F71","#B5584A","#B87B61"],
  "background": "#FFFFFF",  "foreground": "#181B18",
  "good": "#54734F", "neutral": "#A2ABA0", "bad": "#BE373C",
  "maximum": "#374C34", "center": "#F2F3F2", "minimum": "#965440"
}
```

Import via: View → Themes → Browse for themes.

## 8. Do & Don't Checklist

✓ DO:
- Start Y-axis at zero for bar charts
- Highlight focus with primary color, recede others to neutral
- Remove top/right chart borders
- Use direct labels on lines when possible
- Use centered 7-day moving average for daily data
- Use `tabular-nums` for digit alignment

✗ DON'T:
- Truncate Y-axis to exaggerate differences
- Assign different colors to every bar when color carries no meaning
- Use 3D effects, gradients, or shadows
- Use solid red for entire data series (panic-inducing)
- Use pure white as the center of a diverging palette
- Use pie charts with > 4 categories
- Rely on color alone — add shape, label, or pattern

## 9. Workflow When Creating a Chart

1. Ask: what question does this answer? (comparison, trend, composition, etc.)
2. Pick chart type from §3
3. Pick combination pattern from §2 (default: Pattern A)
4. Apply colors in priority order from §1.2
5. Apply chart-specific proportions from §4
6. For lines, use the dark variants from §4.2
7. Add direct labels where possible (axis, data points, line ends)
8. Verify contrast against white background ≥ 3:1 (non-text) or ≥ 4.5:1 (text)
9. Add a meaningful title and a source attribution at the bottom

## Reference Files

When working with a specific chart type, **read the corresponding reference file** for detailed rules, edge cases, and code patterns:

| Chart type | File | Read when |
|------------|------|-----------|
| Bar / column chart | `references/01-bar-chart.md` | daily cases, rankings, departmental comparisons |
| Line chart | `references/02-line-chart.md` | trends, wave comparison, year-over-year |
| Area chart | `references/03-area-chart.md` | cumulative coverage, accumulated totals |
| Stacked / grouped | `references/04-stacked-chart.md` | variant composition, age × severity |
| Pie / donut | `references/05-pie-chart.md` | single-time composition (use sparingly) |
| Scatter / bubble | `references/06-scatter-chart.md` | correlation between variables |
| Histogram / boxplot | `references/07-histogram-boxplot.md` | age distribution, hospital stay distribution |
| Population pyramid | `references/08-pyramid-chart.md` | age × gender comparison |
| Choropleth / heatmap | `references/09-choropleth-map.md` | geographic spread, time × region matrices |
| **Monochrome usage** | `references/10-monochrome-usage.md` | **ordinal data (severity, age, doses, waves) — when categories have natural order** |
| **Uncertainty modifier** | `references/M1-uncertainty-modifier.md` | **data carries estimates with intervals — predictions, sampling CIs, asymmetric ratios (RR/OR/HR)** |

Each reference includes: when to use / when NOT to use; specific styling rules; key per-chart pitfalls; concise Python code examples; and named PNG examples in `assets/examples/`.

Resource files in the skill:
- `scripts/epidemic_palette.py` — importable color module + `apply_style()` for matplotlib
- `scripts/generate_examples.py` — runnable script that produces all reference example PNGs
- `scripts/generate_sample_data.py` — produces the 12 sample CSV datasets
- `scripts/quickstart_with_sample_data.py` — runnable demo: reads sample-data, applies guideline
- `tests/test_palette.py` — 72 automated tests (palette correctness + sample-data integrity)
- `assets/examples/*.png` — pre-generated reference images (19 canonical examples)
- `assets/examples/quickstart/*.png` — examples produced by reading sample-data
- `assets/sample-data/*.csv` — 12 realistic-but-fictional datasets covering all chart types
- `assets/sample-data/README.md` — data dictionary explaining every column
- `epidemic-dataviz-palette.csv` — full color table for Excel users
- `epidemic-dataviz-theme.json` — Power BI theme file
- `resources/office-templates/*.xlsx` — pre-built Excel chart templates (5 patterns: bar, line, stacked, mono-stacked, pie)
- `resources/office-templates/epidemic-report-template.pptx` — PowerPoint report template (6 slides, embedded PNGs)
- `docs/guideline-slides-summary.html` / `.pdf` — slide-format guide, summary version (14 slides, 5-min skim)
- `docs/guideline-slides-full.html` / `.pdf` — slide-format guide, full version (22 slides, 30-min walkthrough)
- `dataviz-guideline.html` — interactive visual reference (full document)
- `dataviz-guideline.pdf` — printable full document

**When modifying the palette**, always run the tests first (`python tests/test_palette.py`) — they catch contrast violations, missing colors, color-blindness regressions, AND sample-data inconsistencies (sum-to-100 violations, monotonicity breaks, encoding issues).

**When users ask for example data**, point them to `assets/sample-data/`. Each CSV corresponds to chart types in the reference files. See `quickstart_with_sample_data.py` for canonical usage patterns.
