# Epidemic Data Visualization Skill 套件

組織內疫情資料視覺化指引的 AI agent skill 套件。相容於 Claude Code、Codex、Google Antigravity 等工具。

## 套件結構

```
epidemic-dataviz/
├── SKILL.md                          ← 主進入點（agent 一定會讀）
│
├── references/                       ← 各圖表類型詳細規範
│   ├── 01-bar-chart.md
│   ├── 02-line-chart.md
│   ├── 03-area-chart.md
│   ├── 04-stacked-chart.md
│   ├── 05-pie-chart.md
│   ├── 06-scatter-chart.md
│   ├── 07-histogram-boxplot.md
│   ├── 08-pyramid-chart.md
│   └── 09-choropleth-map.md
│
├── scripts/                          ← 可執行的 Python 程式
│   ├── epidemic_palette.py           ← 共用色票模組（可 import）
│   ├── generate_examples.py          ← 一鍵產生所有範例 PNG
│   ├── generate_sample_data.py       ← 產生 12 個範例 CSV 資料集
│   └── quickstart_with_sample_data.py ← 示範：讀資料 + 套用指引
│
├── tests/                            ← 自動化測試（72 案例）
│   ├── test_palette.py
│   ├── color_utils.py
│   └── README.md
│
├── assets/
│   ├── examples/                     ← 19 張標準範例 PNG
│   │   └── quickstart/               ← 4 張從 sample-data 產生的示範
│   └── sample-data/                  ← 12 個範例 CSV + 資料字典
│       ├── 01-daily-cases.csv
│       ├── 02-weekly-waves.csv
│       ├── ... (共 12 個 CSV)
│       ├── _manifest.json
│       └── README.md                 ← 完整資料字典
│
├── epidemic-dataviz-palette.csv      ← Excel 用色票對照表
└── epidemic-dataviz-theme.json       ← Power BI 主題檔
```

## 使用方式

### 對 AI agent（自動觸發）

把整包資料夾放到 agent 工具的 skills 目錄。當開發者問「幫我畫每日確診直條圖」、「做變異株比例圖」時，agent 會自動讀取相關內容並套用指引。

**Claude Code：**
```bash
# 全域使用
mkdir -p ~/.claude/skills/
cp -r epidemic-dataviz ~/.claude/skills/

# 或專案內使用
mkdir -p .claude/skills/
cp -r epidemic-dataviz .claude/skills/
```

**Google Antigravity / Codex：** 將整個資料夾放入該工具的 skills 路徑。

### 對人類使用者

#### 撰寫疫情圖表程式時

```python
import sys
sys.path.append("path/to/epidemic-dataviz/scripts")
from epidemic_palette import (
    PRIMARY, CATEGORICAL, LINE_COLORS, ACCENT, NEUTRAL,
    SEMANTIC, apply_style, trailing_ma,
)

apply_style()  # 一次套用所有 matplotlib 樣式
```

#### 產生所有範例圖

```bash
cd epidemic-dataviz/scripts
python generate_examples.py
# 輸出至 ../assets/examples/
```

#### 查詢特定圖表規範

直接打開 `references/` 中對應的 .md 檔閱讀。

## Progressive Disclosure 設計

本 skill 採三層揭露設計：

1. **第一層** — `SKILL.md` 的 metadata（description）：agent 永遠在 context，用以判斷是否觸發
2. **第二層** — `SKILL.md` 本文：觸發後 agent 載入，提供整體規範
3. **第三層** — `references/*.md`：依任務需要才讀取，提供深入細節

這避免一次塞入過多資訊，讓 agent 能根據實際需求調用對應檔案。

## 與其他格式的關係

本套件是「AI agent 工具用版本」。同一份指引另有：

- `dataviz-guideline.html` — 完整互動式網頁版（人類閱讀）
- `dataviz-guideline.pdf` — 列印版（22 頁 A4）
- `dataviz-guideline.md` — Markdown 全文版（GitHub / Notion）

當組織需要更新指引時，建議**先修改 SKILL.md 與 references/**（agent 用），再同步至 HTML / PDF 版本。

**修改色票時的驗證流程：**

```bash
# 1. 修改 scripts/epidemic_palette.py
# 2. 執行測試
cd tests/
python test_palette.py        # 或 pytest test_palette.py -v
# 3. 同步更新 CSV / JSON
# 4. 重新生成範例圖
cd ../scripts/
python generate_examples.py
```

測試會自動檢查 55 個案例：HEX 格式、WCAG 對比度、色覺障礙友善、移動平均正確性、跨檔案一致性。詳見 `tests/README.md`。

## 版本

v1.0 · 2026.05 · 疫情分析應用版
