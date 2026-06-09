# 修訂指引的標準流程

本文件說明如何修改、擴充本指引。**所有變動須經內部審議。**

---

## 修改前

1. **確認你有權限**：本 repo 為組織內部資源。外部訪客可閱讀但不可修改。
2. **先閱讀現有指引**：避免重複討論已決議的問題。重點參考：
   - [`docs/guideline.md`](./docs/guideline.md) §1 核心原則
   - [`CHANGELOG.md`](./CHANGELOG.md) 「Design Decisions」段落
3. **討論再動手**：重大變動建議先在內部會議討論並達成共識。

## 規範新增的 RFC-lite 流程

下方「三種典型修改場景」處理**已決定**的變動如何同步到各層。但「**該不該加這個新規範**」屬於前置討論,需要 RFC 機制留存與盤點 ── **避免規範擴張讓既有運作良好的圖表被誤傷**。

### 何時需要 RFC

| 變動類型 | RFC? | 流程 |
|---|---|---|
| 錯字、格式 | ✗ | L1 |
| 補充說明、新範例 | ✗ | L2 |
| 既有規則調整 | △ | BREAKING 必寫;小調整視範圍 |
| **新規範類別**(新圖表、新 pattern、新規則大類) | ✓ | RFC → L3 |
| 新工具支援 / 新依賴 | ✗ | L3 (有先例:office-templates、slides) |

### Stages

#### Stage 0 ── 對話討論
在 GitHub Issue / 維護者對話中發想,確認方向。

#### Stage 1 ── 寫 RFC
在 `docs/rfcs/YYYY-MM-NN-name.md` 用 `0000-template.md` 起草。

**兩段必須完整填寫,缺一不可進 Pilot:**

1. **Affected existing rules** ── 對既有 patterns / references / SKILL.md decision tree 的影響盤點
2. **Regression check** ── 對既有 19 張範例 PNG 標記 `keep / adjust / waive / break`。若 `break` 數量 > 1,**警訊** ── 回 Stage 0 重新檢討方向

#### Stage 2 ── Pilot(試行)

- `skill/references/NN-xxx.md` 寫規範草案,**檔頭加 YAML frontmatter**:
  ```yaml
  ---
  status: draft
  rfc: 2026-06-NN-name
  ---
  ```
- 範例放 `skill/assets/examples/_drafts/`(不混進 active 範例)
- **`skill/SKILL.md` 的 decision tree 暫不更新** ── AI agent 不主動套用 draft 規範
- `dev-tools/check_drift.py` 對 `status: draft` 的 reference 視為 informational(不強制全層同步)

#### Stage 3 ── Promote 至 Active

- 走完整 L1 → L2 → L3 同步流程
- `status: draft` 改 `active`,SKILL.md decision tree 更新
- CHANGELOG 加採納紀錄
- RFC 的 Decision 段勾選 `Active`,更新 `docs/rfcs/README.md` 索引表

#### Stage 4 ── 後續迭代

- 規範錯了 → `status: deprecated` + 寫替代規範指向
- 採用 `check_drift.py` 的 DEPRECATED_TERMS 機制掃描殘留引用

### 寫作 guard rails(對抗規範擴張)

新規範 reference 撰寫時:

1. **必備兩段**:「適用情境」與「不適用情境」 ── 後者跟前者一樣重要
2. **慎用絕對性用語**:「always / never / 一律 / 永遠 / 全部」,改用「除非 X,否則 Y」
3. **盤點與既有規範的衝突**:強迫在 RFC 的 Affected existing rules 段交代

### Pre-RFC 既有規範

v1.0 的所有規範(patterns A-E、9 種圖表、4 項核心原則等)視為 **pre-RFC accepted**,不需回填 RFC 文件。CHANGELOG 的 v1.0.0 條目與 Design Decisions 段即為其紀錄。

僅 v1.0 之後**新增的規範類別**需走 RFC。

## 三種典型修改場景

### 場景 A：修改色票

最常見也最敏感的變動，因為色彩牽動整套指引的一致性。

```bash
# 1. 編輯 Python 色票模組
vim skill/scripts/epidemic_palette.py

# 2. 立即跑測試（最重要的一步）
cd skill/tests
python3 test_palette.py

# 3. 若測試通過,同步更新 CSV 與 PowerBI 主題
vim skill/epidemic-dataviz-palette.csv
vim skill/epidemic-dataviz-theme.json
cp skill/epidemic-dataviz-palette.csv resources/palette.csv
cp skill/epidemic-dataviz-theme.json resources/powerbi-theme.json

# 4. 重新跑跨檔案一致性測試
python3 test_palette.py

# 5. 重新生成範例 PNG（視覺確認新色票效果）
cd ../scripts
python3 generate_examples.py

# 6. 重新生成 quickstart 圖（確認從 sample-data 出圖仍正確）
python3 quickstart_with_sample_data.py
```

**測試失敗時怎麼辦？**

測試失敗通常代表新色票破壞了某項承諾。可能的處理方式：

| 失敗類型 | 處理 |
|---------|------|
| 對比度不足（WCAG） | 加深該色，或將該色從「文字／線條」用途中移除 |
| 色覺障礙下難區分 | 調整其中一色的色相／明度／飽和度 |
| 主色被誤改 | 確認 `PRIMARY = "#739A6D"`，這是組織主色，不可變動 |
| 跨檔案不一致 | 同步更新 CSV/JSON/SKILL.md，確保多處引用一致 |

絕對不要為了讓測試通過而調整測試門檻。**測試是承諾的化身**，調門檻等於降低指引品質。

**色票變動 = 跨文件變動**：色彩 HEX 值出現在 `docs/guideline.html` 的色卡、`docs/guideline.md` 的色票表格、`docs/index.html` 的 Pages 色票區。完成色票本身的修改後，請接續執行「場景 B Level 3」階段二、階段三的 checklist，把新色票同步到所有展示文件。

### 場景 B：修改規範文字

當需要新增準則、調整建議、修正錯字時。**規範文字散落在多個檔案中,務必使用以下 checklist 確保不漏改。**

#### 規範變動 Checklist

根據變動的「影響範圍」選擇 checklist 等級——**重大規範變動必須跑完整版**，避免文件層級之間漂移。

##### Level 1：錯字／格式調整（影響範圍 = 單一檔案）

僅修正錯字、標點、Markdown 格式問題,不涉及語意變更：

- [ ] 修改該檔案
- [ ] commit & push

##### Level 2：補充說明、範例調整（影響範圍 = 1-2 個檔案）

新增程式碼範例、補充某條規則的細節說明,但不改變核心觀念：

- [ ] 修改主要檔案（通常是 `skill/references/XX.md`）
- [ ] 若該規則也出現在 `docs/guideline.md`,同步更新
- [ ] 用 `grep -r "關鍵字" .` 確認沒漏改
- [ ] commit & push

##### Level 3：規範新增或語意變更（影響範圍 = 全部 6 層文件）

**這是最常見也最容易出錯的層級**——新增模式、修改原則、調整判斷標準等。**請完整跑完以下流程，不要跳步驟。**

###### 階段一：規範核心修改

- [ ] **`skill/scripts/epidemic_palette.py`**（若涉及色票、輔助函式）
  - 新增/修改 dict、常數、function
  - 跑 `python tests/test_palette.py` 確認 80 個測試全過
- [ ] **`skill/references/XX-name.md`**（圖表類型詳細規範）
  - 規則描述、適用情境、不適用情境、常見錯誤、程式碼範例
- [ ] **`skill/SKILL.md`**（AI agent 第一手依據）
  - Combination Patterns 章節
  - Reference Files 表格
  - Decision tree 描述

###### 階段二：人類閱讀文件同步

- [ ] **`docs/guideline.md`**（Markdown 全文版）
  - 同步階段一的概念到對應章節
  - 「選擇順序」決策樹更新（若有新模式）
- [ ] **`docs/guideline.html`**（互動視覺版）
  - 段落內容（與 .md 一致）
  - 視覺色卡（若新增配色組合）
  - DECISION TREE callout 更新
  - Python 程式碼範例區更新
  - 命名慣例列表更新
- [ ] **`docs/guideline.pdf`**（列印版）
  - 重新生成：`python dev-tools/build_pdf.py`（從 repo 根目錄執行,會自動覆寫 `docs/guideline.pdf`）
  - 視覺驗證：模式段落出現、無多餘空白頁、聯絡資訊在最後一頁

###### 階段三：對外展示與資產

- [ ] **`docs/index.html`**（GitHub Pages 首頁）
  - 若涉及色彩展示,更新色票區
  - 若涉及新類型範例,更新 SECTION 04 範例圖網格
  - 若涉及 prompt 相關,更新 SECTION 03 範例
- [ ] **範例 PNG**（若新增圖表類型或情境）
  - `python skill/scripts/generate_examples.py` 重新生成
  - 視覺驗證 1-3 張代表性圖
  - 若首頁要用,複製到 `docs/examples/`

###### 階段四：測試與紀錄

- [ ] **`skill/tests/test_palette.py`**
  - 新增 dict/常數 → 補對應的 `TestXxx` class
  - 跑全部測試確認 100% 通過
- [ ] **`CHANGELOG.md`**
  - 加入「Unreleased」段落（若還沒發版）或新增版本號
  - 列出本次新增、修改、移除的項目
- [ ] **跨文件一致性檢查**
  - `grep -r "新關鍵字" .` 確認所有應出現的檔案都更新了
  - `grep -r "舊用詞" .` 確認沒有被取代的舊用詞殘留

#### 避免規範漂移的最重要原則

> **同一條規則出現在多個檔案時，務必全部更新。「重大變動才同步 HTML/PDF」是錯誤觀念——任何規範變動都該同步。**

不確定哪些檔案有提及某個概念？用 grep 全文搜尋：

```bash
# 找所有提及某個關鍵字的檔案
grep -rln "barPercentage" .
grep -rln "trailing_ma\|移動平均" .
grep -rln "MONOCHROME\|單色" .

# 排除測試輸出和範例圖,只看文件
grep -rln "關鍵字" . --include="*.md" --include="*.html"
```

### 場景 C：新增圖表類型

當有新的疫情圖表需要納入指引時。**這是場景 B Level 3 的最高強度版本——除了規範文字，還涉及新範例圖、新測試、新資料集。**

```bash
# 1. 在 skill/references/ 新增 NN-chart-type.md
#    參考既有檔案的結構：適用情境 → 規範 → 個別重點 → 程式碼 → 常見錯誤

# 2. 在 skill/scripts/generate_examples.py 加入該圖的繪製函式

# 3. 若有對應的範例資料,在 skill/scripts/generate_sample_data.py 新增

# 4. 更新 skill/SKILL.md 的 "Reference Files" 表格

# 5. 更新 docs/guideline.{md,html} 的「圖表選用矩陣」與「圖表範例」章節

# 6. 更新 CHANGELOG.md
```

**完整流程**：執行上述 6 步後，**請接續跑「場景 B Level 3」的所有 checklist**，因為新增圖表類型本質上是「規範新增 + 程式碼 + 範例 + 測試」的綜合變動。

## 重新生成文件版本

當 `docs/guideline.html` 已修改，需要重新生成 PDF：

```bash
# 首次使用需安裝依賴
pip install playwright
playwright install chromium

# 從 repo 根目錄執行,會自動覆寫 docs/guideline.pdf
python3 dev-tools/build_pdf.py
```

詳細說明見 [`dev-tools/README.md`](./dev-tools/README.md)。

## 跨檔案一致性檢查

完成 Level 3 變動後,跑自動化檢查確認沒漏改：

```bash
python3 dev-tools/check_drift.py
```

工具會掃描關鍵概念（如「Pattern E」、「主色 #739A6D」、「trailing MA」等）在各文件層級的覆蓋情況,並警告過時用詞殘留。

新增規範時,記得在 `dev-tools/check_drift.py` 的 `CHECKS` 列表加入對應檢查項目,這樣未來的變動就會自動驗證。

### 更新 GitHub Pages 站台

repo 已配置 `docs/index.html` 作為 GitHub Pages 入口頁。Pages 從 `main` 分支 `/docs` 路徑自動部署。

**關於 docs/ 的內容**：
- `index.html` — Pages 首頁（landing page），列出格式、使用者導覽、設計原則
- `guideline.html` — 完整互動式指引
- `guideline.pdf` — 列印版
- `guideline.md` — Markdown 全文
- `examples/*.png` — Pages 首頁中引用的範例圖（從 `skill/assets/examples/` 複製）
- `.nojekyll` — 告訴 GitHub Pages 不要用 Jekyll 處理（保留所有檔案原樣 serve）

**修改 `index.html` 時的注意事項**：
- 引用 GitHub 內部資源時，連結用絕對 URL（`https://github.com/drhao/...`）
- 引用 Pages 內部資源時，連結用相對路徑（`guideline.html`、`examples/xxx.png`）
- 修改後本地驗證：用 `python3 -m http.server` 在 `docs/` 啟動本地伺服器，瀏覽器訪問 `localhost:8000` 確認連結都正確
- push 後等 GitHub Pages 重新部署（約 1–2 分鐘）

**新增範例圖到 Pages 首頁**：
- 先在 `skill/scripts/generate_examples.py` 中新增繪製函式
- 執行腳本產生 PNG 至 `skill/assets/examples/`
- 複製需要在首頁顯示的圖到 `docs/examples/`
- 更新 `docs/index.html` 中對應的 `<img>` 標籤

## 提交檢查清單

每次 commit 上版前確認:

> **CI 自動化**:對 `main` 的 push / PR 會由 GitHub Actions 自動跑
> `test_palette.py` 與 `check_drift.py`(見 `.github/workflows/test.yml`)。
> 失敗會在 PR 內顯示紅勾。下面 checklist 是本機 pre-flight,可降低
> push 後才發現問題的成本。

**必跑:**

- [ ] `python3 skill/tests/test_palette.py` 全部通過(目前 80 個測試)
- [ ] `python3 dev-tools/check_drift.py` 18/18 概念覆蓋 + 0 過時用詞
- [ ] `grep -rn "TODO\|FIXME\|XXX" .` 沒有殘留未完成標記
- [ ] 文字內容仍符合「4 項核心原則」

**依變動類型補跑：**

- [ ] 若改色票：CSV 與 PowerBI JSON 已同步、`resources/` 目錄已 `cp` 對應檔
- [ ] 若改規範文字：場景 B Level 3 的所有 checklist 已跑完（**特別是 HTML/PDF 是否同步**）
- [ ] 若新增/修改圖表：範例 PNG 已重新生成,必要時複製到 `docs/examples/`
- [ ] 若涉及 SKILL.md：跨參考表格、決策樹、Reference Files 表格三處一致
- [ ] 若是發布版本：`CHANGELOG.md` 已更新版本號與變動清單

**最後跨檔案一致性檢查：**

```bash
# 找新增關鍵字,確認所有應出現的檔案都更新了
grep -rln "你新增的關鍵字" . --include="*.md" --include="*.html" --include="*.py"

# 確認沒有舊用詞殘留(若有取代)
grep -rln "被取代的舊用詞" .
```

## 版本策略(Versioning)

本指引採用 [Semantic Versioning](https://semver.org/) 簡化版 ── 適用「規範性文件 + 工具支援」混合 repo 的語境。

### 版號規則

`MAJOR.MINOR.PATCH` 三段式,語意:

| 段 | 何時遞增 | 範例 |
|---|---|---|
| **MAJOR** | **規範精神大幅變動** ── 顛覆性改變,既有圖表必須大幅重做 | 主色廢除;4 項核心原則改寫;reference 結構重組(chart-type 重編號);Pattern 系統廢除 / 重建 |
| **MINOR** | **新規範類別 / 新工具支援 / 演算法精細化** | 新 modifier(M1、M2);新 reference;新 chart-type;新範例庫;新交付格式;**MA 演算法調整**(centered → trailing 屬此級) |
| **PATCH** | 錯字、格式調整、bug 修正、範例 PNG 重生、CI/build 流程改進 | 字型 fallback;CSS 微調;commit message 規範化 |

> **Note · 為何 Python 函式 rename 不升 MAJOR**:本指引是「**規範文件 + 工具支援**」混合 repo,不是純 lib。Python 函式 rename(例 `centered_ma` → `trailing_ma`)雖對 import 用戶是 breaking,但對「讀規範套用」的多數使用者(設計師 / 分析師 / PM / 長官)衝擊有限,分類為 **MINOR**(CHANGELOG 內明示遷移 sed 指令即可)。嚴格 lib semver 的「任何 API rename = MAJOR」不直接套用 ── 我們關注的是「規範精神是否變動」。

### 何時 release(打 tag)

- **PATCH**(1.0.x):隨時可發,無強制節奏。視需要批次出版
- **MINOR**(1.x.0):累積 ≥ 1 個新規範或工具支援時發版
- **MAJOR**(x.0.0):有 BREAKING change 必發。CHANGELOG 須明示遷移路徑

### Breaking change 通報

任何 BREAKING change 必須在 CHANGELOG 內:
1. 標記 `**BREAKING**`(粗體)
2. 提供「原狀 → 新狀」對照
3. 提供遷移指引(替代寫法、grep 命令、替換腳本)

例:Unreleased 段內「移動平均規範:centered → trailing」即採此格式記錄。

### Pre-RFC 規範如何升版

v1.0 採納的規範(patterns A-E、9 種 chart types、4 核心原則等)視為 pre-RFC accepted。後續修訂依「影響範圍」決定版號:

- 文字精細化(Y 軸「從零」→「直條必從零、折線視情境」)→ PATCH(語意未變)
- 規範條目調整(MA 演算法 centered → trailing)→ MINOR(規範精神不變,仍是 MA;CHANGELOG 內提供 sed 遷移指令)
- 新規範類別(M1、M2)→ MINOR(擴充)

### 與 RFC 流程的關係

- RFC 只決定**該規範是否採納**(governance)
- 版本策略決定**已採納後如何打 tag**
- 兩者正交:可以有 MINOR release 含多個 RFC,也可以一個 RFC 累積到 MAJOR 才釋出

### Git tag 命名

`vMAJOR.MINOR.PATCH`(例:`v1.0.0`、`v1.1.0`)。Tag 後 CHANGELOG 對應段標題加版號 + 日期(`## [1.1.0] - 2026-XX-XX`)。

## 命名與風格慣例

### Git commit message

採用 [Conventional Commits](https://www.conventionalcommits.org/) 簡化版：

```
feat: 新增管制圖（control chart）規範
fix: 修正主色階 700 對白底對比度計算
docs: 補充 quickstart 腳本說明
test: 新增疫苗覆蓋率單調性測試
refactor: 將色覺障礙模擬抽出為共用工具
```

### 檔案命名

- Markdown：kebab-case（`bar-chart.md`）
- Python：snake_case（`epidemic_palette.py`）
- 範例資料 CSV：編號-描述（`01-daily-cases.csv`）
- 圖片：編號-字母-描述（`01a-bar-single-focus.png`）

### Python 風格

- 遵循 PEP 8（4 空格縮排、79 字元行寬）
- 函式 docstring 用中文撰寫（讀者主要為內部團隊）
- 公開函式：型別註記與參數說明

## 不要做的事

- ❌ **不要繞過測試**：測試失敗時不能直接刪除測試或調低門檻
- ❌ **不要修改主色 `#739A6D`**：這是組織色彩識別的核心，須經高階決議
- ❌ **不要引入新的 runtime 相依**：`skill/scripts/` 與 `skill/tests/` 維持 matplotlib + numpy。`dev-tools/` 可視需要使用工具型依賴（playwright 用於 PDF、openpyxl + python-pptx 用於 Office 樣板），但須在 `dev-tools/README.md` 標示為 dev-only 安裝
- ❌ **不要把真實個資放進 sample-data**：所有範例資料必須是虛構的
- ❌ **不要在公開 commit message 中提及內部敏感資訊**：本 repo 公開可見

## 提問

修訂相關疑問請洽 Dr. Hao（[dr.hao.tw@gmail.com](mailto:dr.hao.tw@gmail.com)）。
