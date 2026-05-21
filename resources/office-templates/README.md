# Office 圖表樣板

從本指引 sample-data 自動生成的 Excel / PowerPoint 樣板。**下載即用,不需 Python 環境。**

## 包含內容

| 檔案 | 圖表類型 | 配色模式 | 資料來源 |
|------|---------|---------|---------|
| `01-bar-daily-cases.xlsx` | 直條 + 7 日 MA | Pattern A(主色 + 強調) | 28 天每日新增(虛構) |
| `02-line-three-waves.xlsx` | 折線(3 條) | Pattern B(類別配色) | 三波疫情同期比較 |
| `03-stacked-variants.xlsx` | 100% 堆疊長條 | Pattern B(類別配色) | 變異株消長 6 個月 |
| `04-stacked-monochrome.xlsx` | 100% 堆疊長條 | **Pattern E(單色,重症在底)** | 年齡 × 嚴重度 |
| `05-pie-age-distribution.xlsx` | 圓餅 | Pattern B + 條件使用註記 | 年齡分布(聚合為 5 組) |
| `epidemic-report-template.pptx` | 6 頁簡報樣板 | — | 嵌入既有範例 PNG |

## 使用方式

### Excel 樣板

1. 下載對應的 `.xlsx`
2. 切到「資料」分頁,改成你的真實資料(欄位結構與表頭請保持不變)
3. 切到「圖表」分頁,圖表自動連動更新
4. 「圖表」分頁頂部的引用註記建議保留,提醒讀者本圖遵循疫情視覺化指引

### PowerPoint 樣板

1. 下載 `epidemic-report-template.pptx`
2. 6 張投影片:封面 + 4 張嵌入範例圖 + 色票/原則摘要
3. 把嵌入的 PNG 換成你自己的圖表(右鍵 → 變更圖片)
4. 標題列主色 `#739A6D` 已套用,可直接調整文字

## 重要原則(套用樣板時請遵守)

- **不要修改主色** `#739A6D` — 這是組織色彩識別
- **紅色 `#BE373C` 僅用於警示**,不可作一般類別色
- **Y 軸從零開始**,不截斷座標軸誤導比例
- **7 日移動平均**使用 trailing(本日含前 6 日,即 i-6 到 i),前 6 天用自適應累積窗口
- **單色色階堆疊**最深色放底部(本範例 04 已示範:重症在底)

## 重新生成

樣板由 `dev-tools/build_office_templates.py` 從 `skill/assets/sample-data/` 生成。色票若調整,重跑:

```bash
pip install openpyxl python-pptx
python3 dev-tools/build_office_templates.py
```

詳見 [`dev-tools/README.md`](../../dev-tools/README.md)。

## 完整指引

線上版:https://drhao.github.io/epi-dataviz-styleguide/
