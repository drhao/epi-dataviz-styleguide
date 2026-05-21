# 修訂指引的標準流程

本文件說明如何修改、擴充本指引。**所有變動須經內部審議。**

---

## 修改前

1. **確認你有權限**：本 repo 為組織內部資源。外部訪客可閱讀但不可修改。
2. **先閱讀現有指引**：避免重複討論已決議的問題。重點參考：
   - [`docs/guideline.md`](./docs/guideline.md) §1 核心原則
   - [`CHANGELOG.md`](./CHANGELOG.md) 「Design Decisions」段落
3. **討論再動手**：重大變動建議先在內部會議討論並達成共識。

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

### 場景 B：修改規範文字

當需要新增準則、調整建議、修正錯字時。

```bash
# 文字規範的「真實來源」：
# 1. skill/SKILL.md（AI agent 第一手依據）
# 2. skill/references/*.md（特定圖表類型詳細規範）
# 3. docs/guideline.md（人類閱讀的全文版）
# 4. docs/guideline.html（互動視覺版）
# 5. docs/guideline.pdf（列印版）

# 建議的修改順序：
# A. 先改 skill/SKILL.md 或 skill/references/XX.md
# B. 同步調整 docs/guideline.md
# C. 重大變動才動 HTML 與 PDF（HTML 是 PDF 的源檔）
```

**避免規範漂移**：同一條規則出現在多個檔案時，務必全部更新。若不確定哪些檔案有提及，用 `grep` 全文搜尋：

```bash
grep -r "barPercentage" .
grep -r "中心對齊" .
```

### 場景 C：新增圖表類型

當有新的疫情圖表需要納入指引時。

```bash
# 1. 在 skill/references/ 新增 NN-chart-type.md
#    參考既有檔案的結構：適用情境 → 規範 → 個別重點 → 程式碼 → 常見錯誤

# 2. 在 skill/scripts/generate_examples.py 加入該圖的繪製函式

# 3. 若有對應的範例資料,在 skill/scripts/generate_sample_data.py 新增

# 4. 更新 skill/SKILL.md 的 "Reference Files" 表格

# 5. 更新 docs/guideline.{md,html} 的「圖表選用矩陣」與「圖表範例」章節

# 6. 更新 CHANGELOG.md
```

## 重新生成文件版本

當 `docs/guideline.html` 已修改，需要重新生成 PDF：

```bash
# 需要安裝 playwright + chromium（首次設定）
pip install playwright
playwright install chromium

# 執行轉換腳本（在開發環境中保留）
python3 convert_to_pdf.py
```

PDF 轉換邏輯與列印優化 CSS 保存在開發文件中，並非 repo 一部分（避免增加 repo 體積與相依套件）。

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

每次變動上版前確認：

- [ ] `python3 skill/tests/test_palette.py` 全部通過
- [ ] 若改色票：CSV 與 PowerBI JSON 已同步更新
- [ ] 若改規範文字：SKILL.md、references、docs 三處一致
- [ ] 若新增圖表類型：範例 PNG 已重新生成
- [ ] 若是發布版本：`CHANGELOG.md` 已更新版本號與變動清單
- [ ] 文字內容仍符合「4 項核心原則」

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
- ❌ **不要引入新的外部相依**：本 repo 刻意保持極簡，僅依賴 matplotlib + numpy
- ❌ **不要把真實個資放進 sample-data**：所有範例資料必須是虛構的
- ❌ **不要在公開 commit message 中提及內部敏感資訊**：本 repo 公開可見

## 提問

修訂相關疑問請洽 Dr. Hao（[dr.hao.tw@gmail.com](mailto:dr.hao.tw@gmail.com)）。
