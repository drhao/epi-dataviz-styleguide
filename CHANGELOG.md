# 修訂記錄 ／ Changelog

本檔案記錄疫情資料視覺化指引的版本演進。格式參考 [Keep a Changelog](https://keepachangelog.com/zh-TW/1.1.0/)。

---

## [1.0.0] - 2026-05-21

首次正式發布。

### Added · 新增

#### 色彩系統
- 主色階 10 級（`#F6F9F6` ~ `#253423`），以 `#739A6D` Sage Green 為主色 500
- 中性色階 10 級，帶極微綠色色溫與主色協調
- 類別配色 6 色（綠 → 藍 → 黃 → 鴨綠 → 銅 → 梅）依優先順序
- 強調色家族 4 色（Alert Red、Terracotta、Clay、Caution Amber）
- 序列色階 7 級（單向：低 → 高）
- 發散色階 7 級（雙向：負 ← 中 → 正，中性過渡色 `#F2F3F2` 非純白）
- 語意色 4 種（Success / Warning / Danger / Info）
- 折線專用加深版色彩（解決細線對比不足問題）
- **單色組合 6 組**（`focus_2`、`scale_3` ~ `scale_7`）：用於序數資料（嚴重度、年齡、波次、劑次等）

#### 規範文件
- 4 項核心原則（清晰優先、誠實呈現、一致性、負責任溝通）
- 9 種圖表類型詳細規範：直條／折線／區域／堆疊／圓餅／散佈／直方盒鬚／人口金字塔／面量，**加 1 種橫向規範：單色使用情境**
- 4 種配色搭配模式（Pattern A/B/C/D），**新增 Pattern E（單色色階）**
- HTML/PDF 圖表範例新增 2 張單色 Chart.js 範例（chart11 單色堆疊、chart12 單色折線）
- 新增 `AGENTS.md` — 給 AI agent 的歡迎信,讓 Claude Code 等工具能快速進入狀況
- 新增 `dev-tools/` — 維護者用的開發工具
  - `build_pdf.py`：從 HTML 重新生成 PDF（支援相對路徑與兩步驟流程）
  - `check_drift.py`：跨檔案一致性檢查（自動化 Level 3 階段四的 grep 流程）
  - `chart.umd.js`：Chart.js 4.4.0 本地副本（PDF 渲染用）
- 直條圖比例規範（barPercentage × categoryPercentage）
- 折線可讀性 5 項技巧
- 7 日移動平均的「中心對齊」標準
- 圓餅圖條件使用準則
- 日期軸格式化規範（短期 / 每週 / 跨月跨年）

#### 多格式交付
- HTML 互動式網頁版（22 KB，含 13 張即時繪製圖表）
- PDF 列印版（22 頁 A4）
- Markdown 全文版（便於 Notion／GitHub 引用）
- **GitHub Pages 站台**（`docs/index.html` 作為公開入口頁，含格式選擇、使用者導覽、範例圖預覽）

#### AI Agent Skill 套件
- SKILL.md 主進入點（push-style description 提高觸發率）
- 9 個 references/*.md 詳細圖表規範
- Python 共用色票模組 `epidemic_palette.py`
  - `apply_style()` 一鍵套用 matplotlib 樣式
  - `centered_ma()` 中心對齊移動平均
  - `hide_y_axis()` 隱藏已標註數值的 Y 軸
  - `format_date_axis_daily/weekly/monthly()` 三種日期軸格式
- `generate_examples.py` 自動產生 19 張範例 PNG
- `generate_sample_data.py` 自動產生 12 個 CSV 資料集
- `quickstart_with_sample_data.py` 示範如何整合使用

#### 工具支援
- Excel 用色票對照表（CSV，含 HEX/RGB/用途）
- Power BI 主題檔（JSON，可直接匯入）

#### 範例資料集（虛構）
- 28 天每日新增（含週末填報效應）
- 三波疫情每日數據
- 同期比較含歷史範圍
- 22 縣市發生率與人口
- 變異株消長
- 疫苗 1/2/3 劑覆蓋率
- 年齡 × 嚴重度
- 跨年接種狀態
- 接種率 vs. 重症率
- 年齡 × 性別
- 區域住院天數（1200 筆）
- 縣市 × 月份矩陣

#### 自動化測試
- 72 個 pytest 案例，雙模式運作（pytest 或直接 python 執行）
- 8 個測試類別：HEX 格式、色彩完整性、色階順序、WCAG 對比度、色覺障礙、移動平均、樣式套用、跨檔案一致性、範例資料完整性
- 三層 WCAG 對比門檻：文字 4.5、圖形 3.0、填色 2.4
- 三種色覺障礙模擬（Protanopia、Deuteranopia、Tritanopia）

### Design Decisions · 設計決策

- **主色選擇 `#739A6D`**：HSL(112°, 18%, 52%) 鼠尾草綠，中明度低彩度自然色系，傳達穩重平和可信賴的調性，適合公部門使用
- **紅色獨立為強調色**：疫情情境中紅色具強烈情緒效應，不可作為一般類別色，僅用於警示
- **配色順序綠藍黃**：避免「紅綠對立」造成的色盲困擾，且綠藍黃在色覺障礙下可區分性最佳
- **折線使用加深版**：主色 500 對白底對比僅 3.20，細線時不夠清楚；折線專用 600 對比 4.52 過 AA
- **Trailing 7 日移動平均**:本日含前 6 日(i-6 到 i)。對齊 WHO/CDC/JHU 等公開儀表板的通用慣例,即時 dashboard 場景亦適用(無需未來資料)。前 6 天使用自適應窗口(累積平均)避免線段斷裂。
  - *註:v1.0 初版採 centered MA(i-3 到 i+3),於 Unreleased 階段改為 trailing,理由見下方 Changed 段。*

---

## [Unreleased]

### Added · 新增

- **投影片版指引(對外發布)** — `docs/guideline-slides-*.{html,pdf}`
  - 摘要版 14 張(5 分鐘速覽):4 原則、主色階、類別配色、強調色、Pattern A/B/D/E、6 條鐵則、圖表選用矩陣、4 張 Chart.js 即時範例(直條 + MA、折線、堆疊雙模式)、無障礙、收尾
  - 完整版 22 張(30 分鐘版本):摘要 12 張核心 + 8 張補充(序列/發散色階、MONOCHROME 完整、Pattern C、trailing MA 邊界處理、圓餅條件使用、日期軸格式化、工具支援、AI agent 整合)
  - 1280×720 16:9 landscape PDF,沿用 guideline.html 的設計語言
  - 由新工具 `dev-tools/build_slides_pdf.py` 從 `guideline-slides-summary.html` + `_slides-extra.html` 合併產生完整版
- 新增 `dev-tools/build_slides_pdf.py`:用 Chart.js 內嵌 + playwright landscape 渲染
- 新增 `docs/_slides.css`:投影片共用樣式(主色標題列、色卡、圖表卡、頁尾)
- `dev-tools/check_drift.py` 新增「投影片版指引」CHECK(含對外發布注意事項)

- **Excel/PowerPoint 預生成樣板** — `resources/office-templates/`
  - 5 個 Excel 樣板:直條 + 7 日 trailing MA(Pattern A)、折線 3 條(Pattern B)、類別堆疊(Pattern B)、**單色堆疊 重症在底(Pattern E)**、圓餅 5 組
  - 1 個 PowerPoint 簡報樣板:6 頁(封面 + 4 張嵌入既有 PNG + 色票/原則摘要)
  - 由 `dev-tools/build_office_templates.py` 從 `skill/assets/sample-data/` 與 `epidemic_palette.py` 自動生成,色票若調整重跑即同步
- 新增 `dev-tools/build_office_templates.py`:dev-only 依賴 `openpyxl` + `python-pptx`
- `docs/guideline.html` Chapter 11 新增「方法 C:使用預生成樣板」段落
- `README.md`、`docs/index.html`、`skill/SKILL.md` 同步更新工具支援指引

### Changed · 變更

- **投影片版指引從內部預覽改為對外發布**:`README.md`「我要做會議簡報 / 培訓」段、use case 表、結構樹皆加入入口連結;`docs/index.html` SECTION 01 加入兩張投影片 format card(摘要 14 張 / 完整 22 張),grid 改 `auto-fit` 支援 5 卡 wrap;`check_drift.py` 的 CHECK 從「內部」改為「對外」,`expected_in` 加入 README 與 docs/index.html
- **`apply_style()` 改為 CJK 字型自動 fallback**:`epidemic_palette.py` 內新增 `_build_font_list()`,從候選清單(Noto Sans TC / PingFang TC / Microsoft JhengHei / WenQuanYi Micro Hei 等)動態偵測本機可用字型,不再寫死 `Noto Sans CJK JP`。macOS / Windows / Linux 使用者不需強制安裝特定字型,本機已有的任一 CJK 字型即可用
- **移動平均規範:centered → trailing(BREAKING)**
  - 規範改為 trailing 7 日(本日含前 6 日,即 `i-6` 到 `i`),對齊 WHO/CDC/JHU 等公開儀表板的通用慣例
  - 不再採 centered(`i-3` 到 `i+3`)── 雖然視覺對齊較直觀,但讀者解讀心智負擔較高,且即時 dashboard 場景無未來資料可用
  - `epidemic_palette.centered_ma()` 重命名為 `trailing_ma()`,邏輯改為 trailing 自適應窗口(前 6 天累積平均)
  - 同步更新:`skill/SKILL.md`、`skill/references/01-bar-chart.md`、`docs/guideline.{md,html}`、投影片摘要/完整版、Excel 樣板 `01-bar-daily-cases.xlsx` 內公式、`generate_examples.py` / `quickstart_with_sample_data.py` 內 caller、`AGENTS.md` 鐵則、`CONTRIBUTING.md` 範例、`check_drift.py` CHECK
  - 測試 `TestCenteredMA` 改名為 `TestTrailingMA`,新增 1 個邊界測試(73 個測試全綠)
- **依賴鐵則措辭精煉**:`AGENTS.md` 與 `CONTRIBUTING.md`「不引入新外部相依」精煉為「不引入新 **runtime** 相依」(`skill/` 仍維持 matplotlib + numpy;`dev-tools/` 可使用 playwright / openpyxl / python-pptx 等工具型依賴)
- `README.md`、`SKILL.md` 等 6 處測試數量說法從 65 統一為 72(實際 `test_palette.py` 共 72 個測試)

---

## [planned] - 未來方向

- [ ] Tableau 主題檔
- [ ] Looker Studio 色票
- [ ] 視覺回歸測試（pytest-mpl）
- [ ] 更多 reference 圖表類型（管制圖、漏斗圖、網絡圖）
- [ ] 真實規模測試資料集（10 萬筆 record）

---

[1.0.0]: https://github.com/drhao/epi-dataviz-styleguide/releases/tag/v1.0.0
