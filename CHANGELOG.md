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

- **主色選擇 `#739A6D`**：HSL(112°, 18%, 52%) 鼠尾草綠，中明度低彩度自然色系，傳達穩重平和可信賴的調性，適合需要嚴謹、不引發恐慌的正式溝通場景
- **紅色獨立為強調色**：疫情情境中紅色具強烈情緒效應，不可作為一般類別色，僅用於警示
- **配色順序綠藍黃**：避免「紅綠對立」造成的色盲困擾，且綠藍黃在色覺障礙下可區分性最佳
- **折線使用加深版**：主色 500 對白底對比僅 3.20，細線時不夠清楚；折線專用 600 對比 4.52 過 AA
- **Trailing 7 日移動平均**:本日含前 6 日(i-6 到 i)。對齊 WHO/CDC/JHU 等公開儀表板的通用慣例,即時 dashboard 場景亦適用(無需未來資料)。前 6 天使用自適應窗口(累積平均)避免線段斷裂。
  - *註:v1.0 初版採 centered MA(i-3 到 i+3),於 Unreleased 階段改為 trailing,理由見下方 Changed 段。*

---

## [Unreleased]

### Added · 新增(色彩系統擴充)

- **6 個類別色完整 10 級色階** ── `skill/scripts/epidemic_palette.py` 新增 `SLATE_SCALE` / `MUSTARD_SCALE` / `TEAL_SCALE` / `BRONZE_SCALE` / `PLUM_SCALE` 5 個常數,加上 `CATEGORICAL_SCALES` dict lookup(`sage` 對應既有 PRIMARY_SCALE)
  - 每個色階 10 級 50/100/200/300/400/**500**/600/700/800/900,**500 為 CATEGORICAL 對應 base**
  - 用途:多序列 emphasis(淺色背景帶 + 深色主線)、KPI dashboard 三層色、跨類別保持 design system 一致性
  - 生成方法:淺階(50-400)用 PRIMARY 各級 lightness 為模板,Mustard / Bronze / Plum 在淺階套微 hue shift 避免「米色家族」相近;500 為 base;深階(600-900)用該類別 base lightness × PRIMARY 比例;50/100 lightness 比 PRIMARY 對應級略低(0.93/0.88 vs 0.97/0.92)讓 hue 有色感空間
  - 新增 `dev-tools/generate_categorical_scales.py` 一次性生成工具 + 色卡對照 PNG(輸出 `docs/examples/categorical-scales.png`)
  - 同步:`skill/scripts/epidemic_palette.R` 加 `EPI_*_SCALE` 5 個常數 + `EPI_CATEGORICAL_SCALES` list、`skill/SKILL.md` §1.2.1、`docs/guideline.md` §3.1.1、`resources/palette.csv` 加 50 個 entries
  - 測試:`test_palette.py` 新增 3 個驗證(各色階 10 級、500 必為 base、單調 luminance 遞減)── 80 → 83 個測試
  - `dev-tools/check_drift.py` 新增「類別色完整 10 級色階」CHECK

## [1.1.0] - 2026-06-09

繼 v1.0.0 後的第一個 MINOR 版本。重點:**2 個新規範 modifier(M1 不確定性、M2 small multiples)+ RFC-lite governance framework + R/Quarto/Streamlit 工具支援 + GitHub Actions CI + 互動式 chart 決策樹**。

### ⚠ 對 Python `import` 用戶的遷移指引

> 規範精神不變(MA 仍是 MA),但 Python 函式 rename。對「讀規範套用」的多數使用者無影響;若你的程式碼有 `from epidemic_palette import centered_ma`,跑這條 sed:
>
> ```bash
> grep -rln "centered_ma" your/code/ | xargs sed -i 's/centered_ma/trailing_ma/g'
> ```
>
> 演算法差異:centered(`i-3` 到 `i+3`)→ trailing(`i-6` 到 `i`)。圖表上 MA 線會往右平移約 3 天。詳見 RFC 2026-06-01 與 `references/M1-uncertainty-modifier.md` §相關說明。

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

### Added · 新增(使用者體驗)

- **互動式圖表決策樹 widget** ── `docs/index.html` 新增 SECTION 03「不知道用什麼圖?」
  - 2 階段 wizard:資料形態(6 大類)→ 細節(4-5 個 follow-up) → 推薦結果(chart type + Pattern + 連結到 reference)
  - 涵蓋 6 種資料形態 × 平均 4 細節 = 24 個 decision endpoint,對應 SKILL.md §3 Chart Selection 文字版 decision tree
  - 純 vanilla JS,無 framework / 無外部依賴;CSS 沿用 index.html 主色 + 字型風格
  - 推薦結果含:chart 名稱、Pattern、文字描述、cross-link 按鈕到對應 reference / modifier(M1 / M2)
  - 後續 SECTION 編號 03 → 04 → 05 → 06 → 07 重編
  - `dev-tools/check_drift.py` 新增「互動式 chart 決策樹 widget」CHECK

- **5 分鐘入門 by role** ── `docs/quickstart-by-role.md`
  - 4 個典型角色 × 5 步驟入門路徑:
    - 🎨 設計師 / 分析師(Excel / Power BI / Tableau 套用色票)
    - 💻 工程師(Python / R / JS 程式 + AI agent 整合)
    - 📋 PM / 培訓 / 簡報製作(濃縮為 brief / 教材)
    - 🎯 長官 / 決策者(5 分鐘理解規範精神 + 審圖速覽)
  - 每個角色含「進階方向」段補充
  - 入口:
    - `docs/index.html` SECTION 02 標題下加 lead text 連結到 quickstart
    - 各 audience card 第一個 li 加「⚡ 5 分鐘入門」連結到對應角色 section
    - `README.md`「使用情境」段前加 quote box
  - `dev-tools/check_drift.py` 新增「5 分鐘入門 by role」CHECK
  - 解決原本入門路徑散落在 README / SKILL.md / Pages 各處的問題,提供統一收斂入口

### Added · 新增(教學線上頁)

- **Do / Don't 對照範例庫展示頁** ── `docs/dont-vs-do.html`
  - 把既有 8 對 ✗/✓ PNG 做成單一網頁,GitHub Pages 訪客可直接瀏覽
  - 頁面結構:hero + 8 段對照(每段含對應規則 tag、PNG、說明)+ 頁尾連結
  - 沿用 `docs/guideline.html` 設計風格:主色標題列、無斜體、Noto Serif + Sans TC、響應式
  - PNG 副本放 `docs/examples/dont-vs-do/`(8 張,因 GitHub Pages 僅 serve docs/ 路徑)── 更新源 PNG 後須一併 `cp` 至 docs 副本
  - 與 `docs/guideline.html` Ch.9 定位互補:
    - Ch.9:3 對「核心原則」+ Chart.js 動態(主指引內沉浸式 onboarding)
    - dont-vs-do.html:8 對「具體規則」+ 靜態 PNG(獨立頁、培訓 / review 引用)
  - 入口:
    - `docs/guideline.html` Ch.9 章末新增 callout「更多視覺對照見 dont-vs-do.html」
    - `docs/index.html` 設計師卡片新增連結
    - `skill/assets/examples/dont-vs-do/README.md` 補上線上瀏覽連結與定位差異說明
  - `dev-tools/check_drift.py`「Do/Don't 對照範例庫」CHECK 擴充 expected_in 含 dont-vs-do.html、guideline.html、index.html

### Added · 新增(governance)

- **版本策略明確化(semver)** ── `CONTRIBUTING.md` 新增「版本策略」段
  - 採用 Semantic Versioning 簡化版,適用「規範性文件 + 工具支援」混合 repo:
    - MAJOR:BREAKING(例:trailing MA 取代 centered MA)
    - MINOR:新規範類別 / 新工具支援 / 重要文字精細化
    - PATCH:錯字、格式、bug、範例重生、CI/build 流程
  - 明定 BREAKING change 通報格式(標記、原狀→新狀對照、遷移指引)
  - 明定 RFC 流程與版本策略的正交關係:RFC 決定「採納與否」,版本決定「採納後如何打 tag」
  - Git tag 慣例 `vMAJOR.MINOR.PATCH`

### Added · 新增(automation)

- **GitHub Actions CI** ── `.github/workflows/test.yml`
  - 對 `main` 的 push / PR 自動跑 `test_palette.py`(80 個測試)+ `check_drift.py`(18 個概念覆蓋 + 過時用詞檢查)
  - 失敗會在 PR 內 block(視 GitHub branch protection 設定而定)
  - 補上 `README.md` CI badge(dynamic,反映 main 分支 build 狀態,取代原靜態「tests-80 passing」)
  - `CONTRIBUTING.md` 提交檢查清單前面加 CI 說明,明確「本機 pre-flight + CI 自動化」雙重保險
  - 預期防止規範漂移與測試 regression,降低 maintainer 在 PR 階段才發現問題的成本
  - Python 3.11 + matplotlib + numpy(沿用既有 runtime 鐵則)

### Added · 新增(教學資源)

- **Do / Don't 對照範例庫** ── `skill/assets/examples/dont-vs-do/`
  - 8 對 ✗ DON'T / ✓ DO 並排 PNG,對應既有規則的常見誤用:
    - `01-truncated-yaxis` — Y 軸從零(SKILL §4.4 / 01-bar 規則 1)
    - `02-red-as-categorical` — 紅色僅警示(SKILL §1.3)
    - `03-rainbow-bars` — 顏色傳達資訊(01-bar §3)
    - `04-decorated-pie` — 平面 2D + 直接標籤(05-pie)
    - `05-too-many-pie-slices` — 改用排序橫條(05-pie 條件使用)
    - `06-spaghetti-vs-small-multiples` — 多 panel 拆 M2(M2 適用)
    - `07-chartjunk-vs-minimal` — 移除頂右框 + 僅水平格線(SKILL §4.1.5/4.1.6)
    - `08-sort-by-name-vs-value` — 排名按數值大小(01-bar 規則 4)
  - 新增 `skill/scripts/generate_dont_vs_do.py` 獨立生成腳本(色票若變動可重生)
  - 新增 `skill/assets/examples/dont-vs-do/README.md` 索引與使用情境說明
  - 既有 references 補 cross-link「視覺對照圖」段:`01-bar-chart.md`、`02-line-chart.md`、`05-pie-chart.md`、`M2-small-multiples.md`
  - `skill/SKILL.md` Resource files 條目補上 dont-vs-do 描述
  - `dev-tools/check_drift.py` 新增「Do/Don't 對照範例庫」CHECK
  - 用途:AI agent review 時的視覺證據、設計師培訓教材、跨機關採用推廣
  - 走 L2/L3 跨層同步,**不開 RFC**(無新規範語意,純既有規則的視覺化)

### Added · 新增(規範)

- **Small multiples 版面 modifier(M2)** ── [RFC 2026-06-02](docs/rfcs/2026-06-02-small-multiples.md),**2026-06-09 採納為 Active**
  - 新規範 `skill/references/M2-small-multiples.md`(12 條規則 + 程式碼範例 + Don't/Do 表)
  - 定位為 **layout modifier**,套在既有 chart-type(line / bar / area)上;與 M1 並列,都是 modifier
  - 規則重點:
    - **統一 Y/X scale**(`sharex=True, sharey=True`),共用圖例與軸標
    - **Panel 標題左上**(`loc="left"`),色 `NEUTRAL.700`
    - **Grid 推薦表**:4-6 → 2×3;7-9 → 3×3;17-22 → 4×6 或 5×5;> 25 強制重新分組
    - **焦點 panel 機制**(Pattern A 兼容):焦點 PRIMARY,非焦點預設 NEUTRAL.300(可讀性需求高改 N400)── 經兩次視覺對照定稿
    - **與 M1 兼容**:每 panel 內可獨立套用 uncertainty,共用圖例只標一次
    - **跨年度同期門檻**:< 4 年用 02c 風格(疊一張),≥ 5-6 年用 M2,兩者並存
  - `SKILL.md` Quick Decision Tree 新增 step 6(small multiples 偵測)、§4.7 新章節、Reference Files 表新增 M2
  - 既有 references 補 cross-link:`01-bar-chart.md`(排名並排)、`02-line-chart.md`(主場 + 跨年度門檻說明)、`03-area-chart.md`(多地區累計圖)、`M1-uncertainty-modifier.md`(規則 1 邊界補一句指向 M2 規則 11)
  - 新增 2 張範例 PNG(透過 `generate_examples.py`):`m2a-small-multiples-cities.png`、`m2b-small-multiples-yearly-with-uncertainty.png`
  - `docs/guideline.{md,html}` 各加章節介紹
  - 走完完整 RFC framework:Draft v1 → v2(grid / Open Q3 / Q4 resolved)→ v3(規則 7 視覺對照定稿,兩階段:焦點顏色 + 非焦點淺度)→ Pilot + Active 同日

- **不確定性視覺化 modifier(M1)** ── [RFC 2026-06-01](docs/rfcs/2026-06-01-uncertainty.md),**2026-06-09 採納為 Active**
  - 新規範 `skill/references/M1-uncertainty-modifier.md`(13 條規則 + 程式碼範例 + Don't/Do 表)
  - 兩種主要視覺形式:
    - **漸層填充帶**(時序預測、CI 帶):`PRIMARY_LIGHT` `#B4C9B1` + alpha 0.20-0.40;50% 內層 + 95% 外層;預測段虛線、觀測段實線;預測起點 annotation
    - **Error bar**(少量類別 < 6):`PRIMARY_DARKER` `#374C34`(不用中性灰);`capsize=4`;**規則 13 強制 ── 對數空間估計(RR/OR/HR)CI 不可強制對稱**
  - 定位為 **modifier**,套在既有 Pattern A/B/D 上,**不創新獨立 pattern**
  - `SKILL.md` Quick Decision Tree 新增 step 5(uncertainty 偵測)、§4.6 新章節、Reference Files 表新增 M1 條目
  - 既有 references 補 cross-link:`01-bar-chart.md` / `02-line-chart.md` / `03-area-chart.md` / `06-scatter-chart.md`
  - 新增 2 張範例 PNG(透過 `generate_examples.py`):`m1a-uncertainty-trailing-band.png`、`m1b-uncertainty-errorbar-asymmetric.png`
  - `docs/guideline.{md,html}` 各加章節介紹
  - 走完完整 RFC-lite framework:Draft v1 → v2 → v3(視覺對照定稿)→ Pilot → Active 同日完成(無實作疑慮)

### Added · 新增(工具支援)

- **R / Quarto / Streamlit 工具支援** — 三者皆有實際可匯入的交付檔,色票值與 `epidemic_palette.py` 完全一致
  - `skill/scripts/epidemic_palette.R`:R / ggplot2 色票模組,對等 Python 版。提供 `EPI_*` 色票常數、`scale_fill_epi()` / `scale_colour_epi()`、單色 `scale_*_epi_mono(key)`(Pattern E)、`scale_*_epi_sequential()` / `_diverging()`、`theme_epi()`、`trailing_ma()`。採 `scale_*_manual` 相容各版本 ggplot2(>= 3.4)
  - `resources/quarto/_brand.yml`:Quarto >= 1.6 統一品牌,同時套用文件主題與圖表(ggplot2 經 thematic、matplotlib 經 brand)
  - `resources/quarto/epidemic.scss`:相容所有 Quarto 版本的 HTML 主題,覆寫 Bootstrap `$primary`、字型、連結/標題色,並提供 `--epi-cat-1` ~ `--epi-cat-6` CSS 變數
  - `resources/quarto/README.md`、`resources/streamlit/README.md`:兩種工具的完整使用說明(含圖表配色做法)
  - `resources/streamlit/config.toml`:Streamlit app 佈景主題(chrome)。圖表配色透過 matplotlib `apply_style()` 或 Plotly/Altair 指定 `CATEGORICAL` 達成
  - 同步更新六層文件:`skill/SKILL.md` frontmatter + §7.3 R 擴充 + §7.6 Quarto + §7.7 Streamlit + 資源清單、`skill/SKILL-README.md` scripts 樹加 R 模組、`docs/guideline.md` §12.3/12.7/12.8、`docs/guideline.html` Ch.11 新增 R/Quarto/Streamlit 段、`docs/index.html` 開發者導覽卡 + 頁尾工具資源 + meta、`README.md` 使用情境表 + 結構樹 + 快速上手段
  - **`dev-tools/check_drift.py`**:「主色 #739A6D」CHECK 的 `expected_in` 擴充涵蓋三個新檔;新增「R ggplot2 模組」「Quarto 支援」「Streamlit 支援」三項 CHECK;`Check` 新增 `match_all` 選項並新增「類別配色完整一致(值級)」CHECK——驗證 6 個類別 HEX 完整出現在 R / Quarto 交付檔,擋下非主色(藍/黃/鴨綠/銅/梅)漂移
  - **`skill/tests/test_palette.py`**:`TestCrossFileConsistency` 新增 7 個值級測試——R 模組(類別配色順序、主色/折線黃/警示紅、MONOCHROME 各組)、Quarto(`_brand.yml` 類別配色完整 + sage 為主色 + primary 角色、`epidemic.scss` 類別配色完整)、Streamlit(`config.toml` primaryColor 為主色),與既有 PowerBI 逐色比對同強度
  - 測試數量與 drift CHECK 數說法同步更新(README badge、結構樹、各 SKILL/AGENTS/CONTRIBUTING、投影片、docs/index.html hero stat)

### Added · 新增(governance)

- **RFC-lite 規範新增流程** ── `docs/rfcs/`
  - 新增 `docs/rfcs/README.md`(流程說明、何時要寫 RFC、命名 `YYYY-MM-NN-name.md`、索引表)
  - 新增 `docs/rfcs/0000-template.md`(RFC 模板)
  - 關鍵 mechanism:
    - 對既有 patterns / references / 19 張範例 PNG 強制盤點影響(Affected existing rules + Regression check 段)
    - Stages:Draft → Pilot(status: draft)→ Active → 後續迭代
    - Pilot 期間 `SKILL.md` decision tree 不更新,AI agent 不主動套用 draft 規範
  - `CONTRIBUTING.md` 加「規範新增的 RFC-lite 流程」章節(含寫作 guard rails:避免絕對性用語、必備「適用 / 不適用」兩段)
  - `dev-tools/check_drift.py` 新增:
    - `parse_frontmatter()` 解析 reference YAML frontmatter
    - `report_draft_references()` 列出 status: draft 的規範清單
    - 主流程多一個「Pilot 試行中的規範」report
  - **v1.0 既有規範視為 pre-RFC accepted**,不需回填 RFC

### Changed · 變更

- **說明文字一律不再點明「公部門」使用者身份**:13 處(README、AGENTS、SKILL-README、CHANGELOG Design Decisions、docs/index.html meta + hero、docs/guideline.html 三處、docs/prompt-examples.md、skill/references/07-histogram-boxplot.md)改為中性描述「正式報告/對外溝通/組織內部正式溝通」等。讓本指引適用範圍不再侷限於特定機關屬性
- **網頁一律不使用斜體**:`docs/index.html`(9 處)、`docs/guideline.html`(4 處)的 `font-style: italic` 全部移除;三個樣式檔(index.html、guideline.html、_slides.css)新增全域 reset `em, i, address { font-style: normal; }` 覆寫瀏覽器預設,確保 `<em>` 也不斜體。`check_drift.py` 加入「公部門」與「font-style: italic」為 deprecated terms,擴大掃描範圍至 .css
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

[1.1.0]: https://github.com/drhao/epi-dataviz-styleguide/releases/tag/v1.1.0
[1.0.0]: https://github.com/drhao/epi-dataviz-styleguide/releases/tag/v1.0.0
