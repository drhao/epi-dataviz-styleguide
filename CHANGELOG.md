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

#### 規範文件
- 4 項核心原則（清晰優先、誠實呈現、一致性、負責任溝通）
- 9 種圖表類型詳細規範：直條／折線／區域／堆疊／圓餅／散佈／直方盒鬚／人口金字塔／面量
- 4 種配色搭配模式（Pattern A/B/C/D）
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
- 65 個 pytest 案例，雙模式運作（pytest 或直接 python 執行）
- 8 個測試類別：HEX 格式、色彩完整性、色階順序、WCAG 對比度、色覺障礙、移動平均、樣式套用、跨檔案一致性、範例資料完整性
- 三層 WCAG 對比門檻：文字 4.5、圖形 3.0、填色 2.4
- 三種色覺障礙模擬（Protanopia、Deuteranopia、Tritanopia）

### Design Decisions · 設計決策

- **主色選擇 `#739A6D`**：HSL(112°, 18%, 52%) 鼠尾草綠，中明度低彩度自然色系，傳達穩重平和可信賴的調性，適合公部門使用
- **紅色獨立為強調色**：疫情情境中紅色具強烈情緒效應，不可作為一般類別色，僅用於警示
- **配色順序綠藍黃**：避免「紅綠對立」造成的色盲困擾，且綠藍黃在色覺障礙下可區分性最佳
- **折線使用加深版**：主色 500 對白底對比僅 3.20，細線時不夠清楚；折線專用 600 對比 4.52 過 AA
- **中心對齊移動平均**：而非業界常見的「向後看 7 天」，因中心對齊與直條視覺對齊更直觀

---

## [Unreleased] - 暫定計畫

未來可能的擴充方向（依優先順序）：

- [ ] Tableau 主題檔
- [ ] Looker Studio 色票
- [ ] 視覺回歸測試（pytest-mpl）
- [ ] 更多 reference 圖表類型（管制圖、漏斗圖、網絡圖）
- [ ] 真實規模測試資料集（10 萬筆 record）

---

[1.0.0]: https://github.com/drhao/epi-dataviz-styleguide/releases/tag/v1.0.0
