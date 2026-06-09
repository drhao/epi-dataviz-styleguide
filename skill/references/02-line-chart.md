# 02. 折線圖（Line Chart）

> 用於**呈現時間序列或連續變數的趨勢**。是疫情長期監測、波次分析的主要圖表。

## 適用情境

| 情境 | 範例 |
|------|------|
| 長期趨勢 | 數週或數月的疫情走向 |
| 波次比較 | 歷次疫情波段疊加比較 |
| 同期比較 | 今年 vs. 去年同期 |
| 多指標監測 | 確診→住院→重症的時滯關係 |
| 模型預測 | 實際值 vs. 預測值（含信賴區間） |

## 不適用情境

- 資料點 < 5 個（改用直條圖）
- X 軸為類別而非連續變數（會誤導為時間關係）
- 多於 5 條線（改用小倍數圖 small multiples）

---

## 規範重點

### 1. 折線比長條淺，需用加深版

折線比長條纖細，**同樣顏色畫成折線會明顯偏淺**。這是疫情圖表中最常被忽略的問題。

| 用途 | 長條圖／填色 | 折線圖建議 | 原因 |
|------|-------------|-----------|------|
| 主要序列 | `#739A6D`（500） | **`#5D7F58`**（600） | 500 對比僅 3.20，細線不清楚 |
| 第二序列 | `#587A9D` | `#587A9D` 同色 | 原色對比 4.48，足夠 |
| 第三序列 | `#C8A041` | **`#A8821F`** | Mustard 原色對比 2.45，未過 WCAG |
| 對照／背景線 | `#A2ABA0` | `#A2ABA0` 同色 | 對照線本就應退為背景 |

### 2. 線寬

- 主要序列：**2.5–3 px**
- 次要序列：2 px
- 對照／參考線：1.5 px（常用虛線 `dashed`）
- 警戒閾值線：1.5 px，**虛線 + 紅色**

### 3. 資料點標記

不要每個點都標記，會造成視覺噪音。**在關鍵位置才標記：**

- 起點與終點
- 局部極大、極小值
- 趨勢轉折處
- 需要凸顯的特定時點（如政策實施日）

點的大小：3–5 px。

### 4. 多序列色覺友善

當有 3 條以上折線時，**同時用顏色與形狀區分**：

```python
ax.plot(x, y1, marker="o", ...)  # 圓
ax.plot(x, y2, marker="s", ...)  # 方
ax.plot(x, y3, marker="^", ...)  # 三角
```

這對紅綠色盲使用者特別重要。

### 5. 直接標籤優於圖例

若線條數量 ≤ 3，**將類別名稱直接標在線條末端**，可移除圖例，視覺更清楚：

```python
ax.annotate("本機關", xy=(years[-1], ours[-1]),
            xytext=(8, 0), textcoords="offset points",
            color=PRIMARY_DARK, fontweight="bold")
```

### 6. 日期軸格式化

X 軸為時間時，**請使用 `datetime.date` 物件而非字串**，這樣 matplotlib 才能：

- 正確處理時間間距（即使某天缺失資料）
- 自動選擇合適的刻度密度
- 套用日期格式器（locale、月份名）

本指引提供三個輔助函式對應常見情境：

| 時間範圍 | 函式 | 顯示樣式 |
|---------|------|---------|
| 短期（≤ 5 週） | `format_date_axis_daily(ax, interval=N)` | `04/26, 04/30, 05/04, ...` 每 N 天一標 |
| 中期（1–6 個月） | `format_date_axis_weekly(ax)` | 每週一標記，`MM/DD` |
| 跨月／跨年 | `format_date_axis_monthly(ax)` | `2025 1月, 2月, 3月... 12月`（1 月顯示年份）|

```python
from datetime import date, timedelta
from epidemic_palette import format_date_axis_daily

dates = [date(2026, 5, 1) + timedelta(days=i) for i in range(28)]
ax.bar(dates, values, width=0.75)
format_date_axis_daily(ax, interval=4)  # 每 4 天一個標籤
```

**為什麼不用字串**："2026-05-01" 等字串會被 matplotlib 視為等距類別，看不出星期幾的週期、無法套用時間軸算法。日期物件才能正確呈現「週末效應」、「假日缺報」等時序特徵。

---

## 個別重點

### 波次比較

對齊方式有兩種：
- **按日曆對齊**（X 軸 = 日期）：適合呈現「同一時間點各波的表現」
- **按波峰對齊**（X 軸 = 相對日數）：適合呈現「各波形狀」的比較

當前波段使用深色主色 + 較粗線寬凸顯，歷史波段以中性灰退為背景。建議加上「警戒閾值」紅虛線作為參考。

### 同期比較（含歷史範圍）

呈現方式：今年（主色深粗線）+ 去年同期（中性灰虛線）+ 歷史 ±1 SD（淺灰填色區帶）。

- X 軸用「相對週」（W1–W52）而非絕對日期，便於跨年比較
- 當今年資料明顯偏離歷史範圍時，於該點加註標籤
- 填色區帶透明度 0.20–0.25，避免遮蓋主線

### 多指標監測

呈現「確診→住院→重症」的時間延遲關係。各指標需**標準化**（如各自以期內最大值 = 100），否則尺度差異會掩蓋時滯訊號。

- 同圖內最多 4 條線
- 用形狀區分（圓、方、三角）增強辨識
- 主要指標 2.5px，其餘 2px

### 平滑度（tension）

`tension` 參數控制曲線圓滑度：

- `0`：直接連線（資料點少時可用）
- `0.3–0.35`：適度平滑（**本指引預設**）
- `> 0.5`：過度平滑，會扭曲資料真實樣貌（避免）

---

## 程式碼範例

```python
import matplotlib.pyplot as plt
import numpy as np
from epidemic_palette import (
    LINE_COLORS, PRIMARY_DARK, NEUTRAL, ACCENT, apply_style
)
apply_style()

# 焦點對照：本機關 vs. 平均
years = list(range(2020, 2026))
ours = [12.4, 13.2, 13.8, 15.1, 16.2, 17.5]
avg  = [12.1, 12.7, 13.1, 13.8, 14.4, 14.9]

fig, ax = plt.subplots(figsize=(8, 4.5))
ax.plot(years, ours, color=PRIMARY_DARK, linewidth=2.5,
        marker="o", markersize=5, label="本機關")
ax.plot(years, avg, color=NEUTRAL["400"], linewidth=1.5,
        linestyle="--", marker="s", markersize=4, label="同類機關平均")

# 同期比較含歷史範圍
ax.fill_between(weeks, hist_low, hist_high,
                color=NEUTRAL["400"], alpha=0.22,
                label="歷史範圍（±1 SD）")
ax.plot(weeks, last_year, color=NEUTRAL["400"], linewidth=1.5,
        linestyle="--", label="去年同期")
ax.plot(weeks, this_year, color=PRIMARY_DARK, linewidth=3,
        label="今年")
```

---

## 範例圖

- `02a-line-focus-vs-average.png` — Pattern A 焦點對照
- `02b-line-multi-metric.png` — 多指標監測（色 + 形狀雙重編碼）
- `02c-line-year-over-year.png` — 同期比較含歷史範圍

## 相關規範

折線圖**多 panel 並排比較**(22 縣市、各年齡組、5-6 年以上跨年同期等)時,套用 `M2-small-multiples.md`:統一 Y/X scale、共用圖例與軸標、panel 標題左上、焦點 panel 用 PRIMARY 非焦點 NEUTRAL.300。範例:`m2a-small-multiples-cities.png`、`m2b-small-multiples-yearly-with-uncertainty.png`。**跨年度同期比較**:< 4 年用本檔 02c 風格(疊一張 + 灰色歷史範圍),≥ 5-6 年用 M2。

折線圖加上 **預測區間 / 信賴區間** 時,套用 `M1-uncertainty-modifier.md`(modifier 規範):
- 漸層填充帶(50%/95% 兩層)疊在點估計線上
- 預測段切換虛線(`dashes=[6,3]`),觀測段保持實線
- 預測起點加垂直 annotation line 標示
- Rt、再生數等估計值,Y 軸可從合理 lower bound 起算(caption 註明)

範例:`m1a-uncertainty-trailing-band.png`

## 常見錯誤

| ✗ 錯誤 | ✓ 正確 |
|--------|--------|
| 用主色 500 畫折線（太淺） | 用主色 600 `#5D7F58` |
| Mustard 原色畫折線（對比 2.45） | 用加深版 `#A8821F` |
| 5+ 條線擠在一張圖 | 改用小倍數圖（一指標一圖） |
| 每個資料點都標記 | 只標關鍵點（起終、極值） |
| 用 tension > 0.5 過度平滑 | 用 0.3–0.35 |
| 圖例文字塞滿圖表 | 線條末端直接標籤 |

**視覺對照圖**(`skill/assets/examples/dont-vs-do/`):

- `02-red-as-categorical.png` ── 折線都用紅色家族 vs Pattern B 類別配色
- `06-spaghetti-vs-small-multiples.png` ── 22 條疊一張 spaghetti vs M2 small multiples
- `07-chartjunk-vs-minimal.png` ── 多餘框線/格線 vs 極簡
