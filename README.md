# 疫情資料視覺化指引

> **Epidemic Data Visualization Style Guide**
> 公部門疫情資料分析、流行病學報告、儀表板與對外公告的視覺化標準

[![Version](https://img.shields.io/badge/version-1.0-739A6D)](./CHANGELOG.md)
[![Tests](https://img.shields.io/badge/tests-72%20passing-739A6D)](./skill/tests/)
[![License](https://img.shields.io/badge/license-Internal%20Use-A2ABA0)](./LICENSE)
[![Pages](https://img.shields.io/badge/site-online-739A6D)](https://drhao.github.io/epi-dataviz-styleguide/)

> 🌐 **線上瀏覽完整指引**：https://drhao.github.io/epi-dataviz-styleguide/
>
> 不用 clone repo，直接在瀏覽器中閱讀互動版指引、查看範例圖、下載 PDF。

---

## 這是什麼

本指引提供組織內疫情視覺化的完整標準，包含：

- **色彩系統**：以 `#739A6D` 為主色的完整色票，涵蓋類別配色、強調色、序列／發散色階
- **9 種圖表類型規範**：每種圖式的適用情境、設計準則、常見錯誤
- **無障礙標準**：WCAG AA 對比度、色覺障礙友善
- **多格式交付**：HTML 互動版、PDF 列印版、Markdown 全文版
- **AI Agent Skill**：可直接放入 Claude Code、Codex、Google Antigravity 的 SKILL.md
- **工具支援**：Python 色票模組、Power BI 主題檔、Excel 對照表
- **範例資料集**：12 個虛構但合理的疫情 CSV 資料，可實際練習

## 使用情境

| 你是 | 從這裡開始 |
|------|----------|
| 想閱讀完整指引（一般使用者）  | 🌐 [線上指引](https://drhao.github.io/epi-dataviz-styleguide/)（GitHub Pages）|
| 想列印或存檔給長官審閱        | [`docs/guideline.pdf`](./docs/guideline.pdf) |
| 想在 Notion / Wiki 引用       | [`docs/guideline.md`](./docs/guideline.md) |
| 寫 Python / R 程式畫圖        | [`skill/scripts/epidemic_palette.py`](./skill/scripts/) |
| Excel 使用者                   | [`resources/palette.csv`](./resources/palette.csv) |
| Power BI 開發者               | [`resources/powerbi-theme.json`](./resources/powerbi-theme.json) |
| 用 Claude Code / Codex 開發  | [`skill/`](./skill/) 整個資料夾 |
| 想看某個圖表類型的詳細規範    | [`skill/references/`](./skill/references/) 9 個 .md 檔 |
| 想要範例疫情資料測試         | [`skill/assets/sample-data/`](./skill/assets/sample-data/) |

## Repo 結構

```
epi-dataviz-styleguide/
├── README.md              ← 你現在看到的這份
├── AGENTS.md              ← 給 AI agent 的歡迎信
├── LICENSE                ← 使用條款
├── CHANGELOG.md           ← 版本記錄
├── CONTRIBUTING.md        ← 修改指引的標準流程
│
├── docs/                  ← GitHub Pages 站台與文字指引
│   ├── index.html         ← Pages 首頁（landing page）
│   ├── guideline.html     ← 完整互動式指引
│   ├── guideline.pdf      ← 列印版
│   ├── guideline.md       ← Markdown 全文
│   └── examples/          ← 首頁引用的範例圖
│
├── skill/                 ← AI agent skill 套件
│   ├── SKILL.md
│   ├── SKILL-README.md
│   ├── references/        ← 10 種圖表的詳細規範
│   ├── scripts/           ← Python 色票模組 + 範例腳本
│   ├── tests/             ← 72 個自動化測試
│   └── assets/
│       ├── examples/      ← 預生成範例 PNG
│       └── sample-data/   ← 12 個範例 CSV 資料集
│
├── dev-tools/             ← 維護者用的開發工具
│   ├── README.md
│   ├── build_pdf.py       ← 從 HTML 重生 PDF
│   ├── check_drift.py     ← 跨檔案一致性檢查
│   └── chart.umd.js       ← Chart.js 本地副本
│
└── resources/             ← 工具直接匯入用
    ├── palette.csv
    └── powerbi-theme.json
```

## 5 分鐘快速上手

### 我要看指引

**最快的方式**：直接訪問 GitHub Pages 站台 → https://drhao.github.io/epi-dataviz-styleguide/

或在本地：點開 [`docs/guideline.html`](./docs/guideline.html)（含互動範例圖表），或 [`docs/guideline.pdf`](./docs/guideline.pdf)（22 頁列印版）。

### 我要在 Python 程式中套用色彩

```bash
git clone <repo-url>
cd epi-dataviz-styleguide/skill/scripts
python3 -c "
from epidemic_palette import PRIMARY, CATEGORICAL, apply_style
import matplotlib.pyplot as plt

apply_style()
fig, ax = plt.subplots()
ax.bar(['A', 'B', 'C'], [10, 20, 15])
plt.savefig('test.png')
"
```

### 我要用 Power BI

1. 下載 [`resources/powerbi-theme.json`](./resources/powerbi-theme.json)
2. Power BI Desktop → 檢視 → 佈景主題 → 瀏覽佈景主題 → 選擇該 JSON
3. 整份報告自動套用本指引色彩

### 我要用 Excel

1. 開啟 [`resources/palette.csv`](./resources/palette.csv) 作為色票對照表
2. 在 Excel → 頁面配置 → 色彩 → 自訂色彩，依 CSV 中 RGB 值填入 Accent 1–6

### 我要讓 AI 自動遵守指引

把 `skill/` 整個資料夾放到 Claude Code、Codex 或 Google Antigravity 的 skills 目錄。當開發者問「畫每日確診直條圖」、「做變異株比例圖」時，AI 會自動讀取規範並套用。

詳細安裝步驟見 [`skill/SKILL-README.md`](./skill/SKILL-README.md)。

### 我要請 AI 幫我畫圖（含 prompt 範例）

不論你是用裝了 skill 的 AI 工具，還是 ChatGPT / Claude.ai / Gemini 等網頁 AI，都有對應的現成 prompt 模板，**直接複製貼上、填空換成你的資料即可**。

完整內容見 📖 [`docs/prompt-examples.md`](./docs/prompt-examples.md)（GitHub 會直接渲染 Markdown）。

**最常用的網頁 AI 簡短版**（複製到 ChatGPT 等對話框）：

```
請依以下規範用 Python matplotlib 畫圖:
- 主色 #739A6D(Sage Green),類別配色:#587A9D, #C8A041, #49888D
- 紅色僅警示用,不作一般類別色
- Y 軸從零開始,移除頂部右側邊框
- 中文字體支援
- 折線寬 2.5px,長條 width=0.6

資料:[貼上你的資料]
我要:[簡述需求]
```

## 重新生成資源

所有圖表與資料都可從原始碼重現：

```bash
cd skill/scripts

# 重新生成 19 張範例 PNG
python3 generate_examples.py

# 重新生成 12 個範例 CSV
python3 generate_sample_data.py

# 跑 quickstart（讀 sample-data 並繪圖）
python3 quickstart_with_sample_data.py
```

## 跑測試

```bash
cd skill/tests

# 方式 A：直接執行（不需 pytest）
python3 test_palette.py

# 方式 B：使用 pytest
pip install pytest
pytest test_palette.py -v
```

72 個測試涵蓋 8 個面向：HEX 格式、色彩完整性、色階順序、WCAG 對比度、色覺障礙、移動平均、樣式套用、跨檔案一致性、範例資料完整性。

修改色票時 **務必先跑測試**，避免破壞核心承諾。

## 修改指引時

請參考 [`CONTRIBUTING.md`](./CONTRIBUTING.md)，重點：

1. **改色票** → 編輯 `skill/scripts/epidemic_palette.py` → 跑測試 → 同步更新 CSV/JSON
2. **改規範文字** → 編輯 `skill/SKILL.md` 與對應的 `skill/references/*.md`
3. **重大改版** → 同步更新 `docs/guideline.{html,pdf,md}` 三種格式
4. **更新版本** → 更新 `CHANGELOG.md`

## 設計理念

| 原則 | 說明 |
|------|------|
| **清晰優先** | 每個視覺元素都必須服務於訊息，移除不傳達資訊的裝飾 |
| **誠實呈現** | Y 軸從零開始、不截斷座標軸、不挑選有利時間區間 |
| **負責任溝通** | 紅色僅用於關鍵警示，避免在疫情情境中過度引發焦慮 |
| **普惠可及** | WCAG AA 對比、色覺障礙友善、不單靠顏色傳達 |

完整原則見 [`docs/guideline.md`](./docs/guideline.md) 第 1 章。

## GitHub Pages 設定（首次上版時做一次即可）

本 repo 已準備好 Pages 用的 `docs/index.html` 與相關資源。發布後啟用步驟：

1. push repo 到 GitHub
2. 進入 repo → Settings → Pages
3. **Source** 選擇「Deploy from a branch」
4. **Branch** 選擇 `main`，路徑選擇 `/docs`
5. 點 Save，等待約 1–2 分鐘
6. Pages URL：`https://drhao.github.io/epi-dataviz-styleguide/`

之後每次 push 到 `main` 的 `docs/` 內容變動，會自動重新部署。

## 授權

本指引為組織內部使用文件，公開於本 repo 僅供透明審視。詳見 [`LICENSE`](./LICENSE)。

## 聯絡

關於本指引的疑問、修訂建議：請洽 Dr. Hao（[dr.hao.tw@gmail.com](mailto:dr.hao.tw@gmail.com)）。
