# 01. 直條圖／長條圖（Bar Chart）

> 用於**比較不同類別的數值大小**，是疫情資料最常用的圖表之一。包含直立（column）與水平（horizontal bar）兩種方向。

## 適用情境

| 情境 | 範例 |
|------|------|
| 比較固定類別 | 各部門預算執行率、各醫院床位使用率 |
| 每日新增（時序） | 每日確診數、每日疫苗接種劑次 |
| 排名 | 縣市發生率排序、Top N 國家比較 |
| 分組比較 | 年齡層 × 嚴重度、季別 × 業務量 |

## 不適用情境

- 資料點 ≥ 30 個的長期趨勢（改用折線圖）
- 連續性數值的分布（改用直方圖）
- 比例組成且時間單一（改用水平堆疊條，非圓餅）

---

## 規範重點

### 1. Y 軸必從零開始

長條圖比較的是「長度」，截斷 Y 軸會嚴重誤導比例感受。即使資料變動範圍很小，仍應從零起算；若想凸顯變化，改用折線圖或加註標籤。

### 2. 直條比例（粗細與間距）

| 類型 | matplotlib `width` | Chart.js `barPercentage × categoryPercentage` |
|------|-------------------|----------------------------------------------|
| 單組直條（清楚分隔） | `0.6` | `0.55 × 0.85` |
| 密集時序直條（每日） | `0.75` | `0.75 × 0.9` |
| 水平排名長條 | `0.7`（`height`） | `0.7 × 0.85` |
| 分組直條（組內緊鄰、組間留白） | n/a（用 offset） | `0.85 × 0.75` |

### 3. 顏色策略

**有焦點時：** 焦點用主色 `#739A6D`，其餘用 `Neutral 400 #A2ABA0`（Pattern A）。

**無焦點時：** 全部使用主色，不要為每根長條配不同顏色。

**有警示對象時：** 一般用主色，超標項目用 `Terracotta #B5584A`（不用最強的 Alert Red，避免過度警示）。

### 4. 排序

- **比較類別**（如部門、區域）：依資料數值由大到小排序
- **時序資料**（日期、月份）：依時間順序排列，不可排序
- **有自然順序的類別**（年齡層、嚴重度）：依自然順序，不可重排

### 5. 標籤策略

- 資料標籤直接標於長條末端外側（值在 100 以內時通常更清楚）
- 若資料標籤過多造成擁擠，僅標示首末、極值或關鍵點
- 軸標籤過長時：直條圖優先改為水平長條圖，而非旋轉文字

### 6. 已標數值時可省略軸線

當每根長條上方都已直接標註數值時，**Y 軸刻度與標籤反而是視覺冗餘**，應該移除：

- 隱藏 Y 軸刻度（`ax.tick_params(axis="y", left=False, labelleft=False)`）
- 移除 Y 軸標題（`ax.set_ylabel("")`）
- 隱藏左側軸線（`ax.spines["left"].set_visible(False)`）
- 同時關閉水平格線（`ax.grid(False)`）

本指引提供 `hide_y_axis(ax)` 輔助函式一鍵完成上述設定。**水平長條圖同理可隱藏 X 軸。**

### 7. 網格線

直條圖讀數值的方向是 Y 軸——**只需要水平格線**，垂直格線是視覺噪音。

本指引預設 `axes.grid.axis = "y"`，套用 `apply_style()` 後直條/折線圖自動只顯示水平格線。需要雙向格線的圖表（散佈圖）才手動 `ax.grid(True, axis="both")` 開啟。

### 8. 日期 X 軸（每日新增類圖表必讀）

每日新增直條圖的 X 軸應使用 `datetime.date` 物件而非整數或字串，這樣才能：

- 顯示真實日期格式（`05/14` 而非 `13`）
- 正確處理週末效應的視覺呈現
- 跨月／跨年自動切換格式

本指引提供 `format_date_axis_daily(ax, interval=4)` 一鍵設定每 N 天一個 `MM/DD` 標籤：

```python
from datetime import date, timedelta
from epidemic_palette import format_date_axis_daily

dates = [date(2026, 5, 1) + timedelta(days=i) for i in range(28)]
ax.bar(dates, daily_values, width=0.75)
format_date_axis_daily(ax, interval=4)
```

詳見 `references/02-line-chart.md` 的「日期軸格式化」一節。

---

## 個別重點

### 每日新增（直條 + 7 日移動平均）

這是疫情監測最重要的圖表。要點：

- 資料至少 21–28 天，否則均線會缺一截
- **使用「中心對齊」**均線（i 日 MA = i-3 到 i+3 平均），與直條視覺對齊
- 兩端 3 天使用自適應窗口（短窗口）避免折線斷裂
- 直條主色，均線用主色加深版 `#374C34`
- 直條 width 0.75（密集時序）
- 週末資料偏低為「報告日效應」，**不可截除**——這是真實的訊號

### 水平排名長條

- 長度由上到下遞減（最大在頂部，視覺焦點）
- 若需強調 Top N，僅取前 8–10 名
- 數值標籤標於長條外側右端
- 縣市比較必須**標準化**（如每 10 萬人口）

### 分組直條

- 同組內各條緊鄰（無間距），組間留白較大
- 組數 × 系列數最多 5 × 4，超過建議改為小倍數圖
- 系列順序：本指引類別配色由前至後

---

## 程式碼範例

```python
import matplotlib.pyplot as plt
import numpy as np
from epidemic_palette import (
    PRIMARY, PRIMARY_DARKER, NEUTRAL, ACCENT, apply_style, centered_ma
)
apply_style()

# 範例 A: 凸顯焦點的單組直條
cats = ["教育", "社福", "經發", "環保", "交通", "文化"]
vals = [98, 92, 105, 87, 78, 95]
colors = [NEUTRAL["400"] if i != 2 else PRIMARY for i in range(len(cats))]

fig, ax = plt.subplots(figsize=(8, 4.5))
ax.bar(cats, vals, color=colors, width=0.6)
ax.set_ylabel("執行率（%）")
ax.set_title("各部門年度預算執行率", loc="left")
ax.set_ylim(0, 120)

# 範例 B: 每日新增 + 中心對齊均線
days = np.arange(28)
daily = [...]  # 28 天的每日資料
ma = centered_ma(daily, window=7)
ax.bar(days, daily, color=PRIMARY, width=0.75, label="每日新增")
ax.plot(days, ma, color=PRIMARY_DARKER, linewidth=2.5, label="7 日移動平均")
```

---

## 範例圖

- `01a-bar-single-focus.png` — 凸顯焦點的單組直條
- `01b-bar-daily-with-ma.png` — 每日新增 + 7 日移動平均
- `01c-bar-horizontal-ranking.png` — 水平排名長條（含強調）

## 常見錯誤

| ✗ 錯誤 | ✓ 正確 |
|--------|--------|
| Y 軸從 90 開始放大差異 | Y 軸從 0 開始 |
| 每根長條不同顏色 | 全部同色，或僅焦點變色 |
| 排名圖未排序 | 由大至小排序 |
| 縣市比較用絕對數 | 標準化為每 10 萬人口 |
| 確診長條全部標紅 | 中性色長條 + 紅色標警戒線 |
