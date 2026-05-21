# dev-tools/

維護這份規範時用的開發工具。**不是給規範使用者用的**——一般使用者只需要看 `docs/` 與 `skill/`。

## 工具一覽

| 工具 | 用途 | 何時使用 |
|------|------|---------|
| `build_pdf.py` | 從 `docs/guideline.html` 重新生成 `docs/guideline.pdf` | 改了 HTML 之後 |
| `check_drift.py` | 跨檔案一致性檢查 | 重大規範變動後（Level 3） |
| `chart.umd.js` | Chart.js 4.4.0 函式庫副本 | `build_pdf.py` 內部使用 |

## build_pdf.py

把 `docs/guideline.html` 加上列印優化 CSS，輸出 A4 直式 PDF。

**首次使用需安裝依賴：**

```bash
pip install playwright
playwright install chromium
```

**執行：**

```bash
# 從 repo 根目錄
python dev-tools/build_pdf.py

# 或從本目錄
cd dev-tools && python build_pdf.py
```

**輸出：**`docs/guideline.pdf`（覆寫既有檔案）

**工作流程：**
1. 把 `chart.umd.js` 內嵌進 HTML（避免 PDF 渲染時受 CDN 阻擋影響）
2. 用 Playwright 載入嵌入版,套用列印 CSS
3. 等所有 Chart.js 圖表完成繪製
4. 輸出 PDF
5. 清掉暫存檔

**修改列印樣式：**直接編輯 `build_pdf.py` 內的 `PRINT_CSS` 常數。

## check_drift.py

掃描關鍵概念在各文件層級的覆蓋情況，找出規範變動後可能漏改的檔案。

**執行：**

```bash
python dev-tools/check_drift.py
```

**輸出：**

```
✓ Pattern E / 模式 E（單色色階）
✓ MONOCHROME 字典
...
通過 9/9

✓ 沒有過時用詞殘留

✓ 所有檢查通過
```

**新增檢查項目：**直接編輯 `check_drift.py` 的 `CHECKS` 列表。每個 `Check` 物件包含：

- `name` — 顯示名稱
- `keywords` — 任一出現即視為「有提及」
- `expected_in` — 必須出現的檔案清單
- `optional_in` — 出現也好沒出現也 OK
- `description` — 為什麼檢查這個

**新增黑名單用詞：**編輯 `DEPRECATED_TERMS` 列表，列出取代後不該再出現的舊用詞。

**Exit codes：**
- `0` = 所有檢查通過
- `1` = 有檢查項目失敗（適合用於 CI hook 或 pre-commit）

## chart.umd.js

Chart.js 4.4.0 的 UMD bundle，從 [npmjs](https://www.npmjs.com/package/chart.js/v/4.4.0) 下載。

**用途：** `build_pdf.py` 把這個檔案內嵌進 HTML，避免渲染 PDF 時受 CDN 影響（沙箱環境常擋 CDN）。

**更新 Chart.js 版本：**
1. 從 npm 下載新版 `chart.umd.js`
2. 替換本檔案
3. 同步更新 `docs/guideline.html` 內的 `<script src="...chart.js@X.Y.Z...">` 版本號
4. 同步更新 `build_pdf.py` 內 `CHARTJS_CDN_PATTERN` 字串
5. 重跑 `python dev-tools/build_pdf.py` 驗證仍正常

## 為什麼這些工具不放在 skill/scripts/？

`skill/scripts/` 是**規範的一部分**——使用本指引的人會引用、執行裡面的腳本（如 `epidemic_palette.py`、`generate_examples.py`）。

`dev-tools/` 是**規範維護者的工具**——只有在改規範本身、重新生成 PDF、檢查跨檔案一致性時才用到。一般使用者完全不需要碰。

兩者用途完全不同，所以分開放。
