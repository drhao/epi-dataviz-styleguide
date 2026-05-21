# 致 AI Agent

> 你好。這份檔案是給 AI agent（Claude Code、Codex、Antigravity 等）的入門指南。**請先讀這份再做事**。

## 這個 repo 是什麼

公部門疫情資料視覺化指引——以 `#739A6D` Sage Green 為主色的完整色彩系統 + 10 種圖表規範 + AI agent skill 套件。

**它不是給人畫圖用的工具，而是「規範本身的源代碼」**。每次修改都要當作軟體變更處理：跑測試、更新 CHANGELOG、保持跨檔案一致性。

## 你來做什麼

維護者（Dr. Hao, dr.hao.tw@gmail.com）會請你做以下類型的工作：

- **規範微調**：修錯字、補充說明、調整既有規則措辭
- **規範擴充**：新增配色模式、新增圖表類型、新增工具支援（Tableau、Looker 等）
- **流程改進**：新增測試、自動化檢查、開發工具
- **內容深化**：新增 reference 範例、補充教學文件

維護者**不會**請你用這份指引去畫疫情圖表——那是給組織內分析師的事情，不是這個 repo 的目的。

## 第一次接觸時必讀

依序讀這 3 份檔案,**讀完後跟維護者確認你的理解**再開始動作：

1. **`README.md`** — repo 整體結構、各檔案用途
2. **`CONTRIBUTING.md`** — Level 1/2/3 修改流程,**這份最重要**
3. **`CHANGELOG.md`** — 已做過的設計決策（特別是「Design Decisions」段落）

## 修改流程的鐵則

### 1. 判斷變動等級

依照 `CONTRIBUTING.md` 的 Level 1/2/3 分類：

| Level | 判斷 | 流程 |
|-------|------|------|
| **L1** | 錯字、格式問題 | 1 個檔案就好 |
| **L2** | 補充說明、範例調整 | 1-2 個檔案 |
| **L3** | 規範新增或語意變更 | **全部 6 層文件,跑完整 4 階段流程** |

**判斷不準時,當作 L3 處理**。多做不會錯,少做會導致文件漂移。

### 2. 永遠先跑測試

任何變動上版前都要：

```bash
python3 skill/tests/test_palette.py
```

期望輸出：「共 72 個測試 ✓ 72 ✗ 0 ⊘ 0」

**測試失敗時不要為了讓測試通過而調整測試門檻**。測試是承諾的化身,門檻是用來捍衛規範品質的。

### 3. 跨文件同步

最容易犯的錯：改了 `skill/SKILL.md`,忘了同步 `docs/guideline.html`、`docs/guideline.pdf`、`docs/index.html`。

每次規範變動完成後,跑：

```bash
python3 dev-tools/check_drift.py
```

這個工具會掃描關鍵概念在各文件中的出現,提醒你哪裡可能漏改。

### 4. 重新生成 PDF

只要動了 `docs/guideline.html`,就要重新生成 PDF：

```bash
python3 dev-tools/build_pdf.py
```

首次使用需安裝 `playwright` 與 `chromium`（腳本會提示）。

## Repo 心智模型

把 repo 想成三層：

```
┌─────────────────────────────────────────┐
│  L1: 規範權威源 (給 AI agent 看)         │
│  skill/SKILL.md + skill/references/     │
│  skill/scripts/epidemic_palette.py      │
└─────────────────────────────────────────┘
                  ↓ 同步
┌─────────────────────────────────────────┐
│  L2: 人類閱讀層 (給人看)                  │
│  docs/guideline.{md,html,pdf}           │
└─────────────────────────────────────────┘
                  ↓ 同步
┌─────────────────────────────────────────┐
│  L3: 對外展示層 (給訪客看)                │
│  docs/index.html (GitHub Pages)         │
│  資源檔 resources/, skill/assets/        │
└─────────────────────────────────────────┘
```

**修改規範時,務必由上往下同步**——先改 L1 的權威源,再層層往下擴散。反向修改會導致權威源失去 single source of truth 地位。

## 重要設計決策（不可違反）

這些是維護者經過深思熟慮的決定,**不要在沒徵詢前修改**：

- **主色 `#739A6D`** 是組織色彩識別,不可變動
- **紅色家族**（`#BE373C` 等）僅用於警示,**不可作為一般類別配色**
- **Y 軸**必須從零開始,**不可截斷座標軸誤導比例**
- **移動平均**用「中心對齊」,不用 trailing
- **單色色階堆疊**最深色放底部（重症為視覺基底）
- **LICENSE** 是「內部使用授權」,不採開源授權——不可改為 MIT/Apache 等

完整設計理由見 `CHANGELOG.md` 的「Design Decisions」段落。

## 不要做的事

- ❌ 不要為了讓測試通過而調整測試門檻
- ❌ 不要修改主色 `#739A6D`
- ❌ 不要引入新的外部相依（保持 matplotlib + numpy 即可）
- ❌ 不要把真實個資放進 `skill/assets/sample-data/`（所有範例資料必須虛構）
- ❌ 不要在公開 commit message 中提及敏感資訊（repo 公開可見）
- ❌ 不要直接修改 `docs/guideline.pdf`——它從 HTML 自動生成,改 HTML 後跑 `build_pdf.py`

## 開發工具速查

| 工具 | 路徑 | 用途 |
|------|------|------|
| 跑測試 | `python3 skill/tests/test_palette.py` | 驗證色彩規範 |
| 重生 PDF | `python3 dev-tools/build_pdf.py` | HTML 改了之後同步 PDF |
| 跨檔案漂移檢查 | `python3 dev-tools/check_drift.py` | L3 變動後確認沒漏改 |
| 重生範例 PNG | `python3 skill/scripts/generate_examples.py` | 色票或範例改了之後 |
| 重生範例資料 | `python3 skill/scripts/generate_sample_data.py` | 範例 CSV 需更新時 |
| 跑 quickstart | `python3 skill/scripts/quickstart_with_sample_data.py` | 驗證讀資料+繪圖整合 |

## 跟維護者互動的建議

維護者已經把 repo 設計得很完整,**他通常知道自己要什麼**。建議：

- 提案重大變動前,先列出影響的檔案清單給他確認
- 跑完 L3 流程後,**主動回報「完成了哪些階段、修改了哪些檔案、測試結果」**
- 遇到設計決策歧義時,參考 `CHANGELOG.md` 的歷史脈絡,別憑直覺猜
- 維護者中英文混用,你可以用繁體中文回應（這是他的偏好）

## 結語

這個 repo 的精神是「規範也該像軟體一樣可演進、可驗證、可追溯」。你的工作就是維護這份精神——讓每次變動都更精確、更一致、更可靠。

有任何不清楚的地方,直接問維護者。**不要猜。**

— *本檔案最後更新：2026 年 5 月，版本對應 v1.0*
