# 07. 直方圖／盒鬚圖（Histogram &amp; Boxplot）

> 用於**觀察單一變數的分布**。直方圖呈現完整形狀；盒鬚圖凸顯關鍵統計量並便於跨組比較。

## 適用情境對照

| 目的 | 圖式 |
|------|------|
| 看分布的**形狀**（峰、偏態、雙峰） | 直方圖 |
| 看**中位數、四分位、離群值** | 盒鬚圖 |
| **跨多組**比較分布（≥ 4 組） | 盒鬚圖（並列） |
| **單一群體**深入觀察 | 直方圖（或 + 密度曲線） |
| 需要呈現精確分位數 | 盒鬚圖 |

---

## 直方圖 規範重點

### 1. Bin 數量（最重要的參數）

Bin 數量直接影響圖表呈現的「故事」：

- **太少（< 10）**：細節遺失，可能掩蓋雙峰、長尾等重要特徵
- **太多（> 50）**：噪音被放大，難以看出整體形狀
- **預設規則**：`bins = ceil(sqrt(n))`，n 為樣本數
  - 例：n = 1200，bins ≈ 35
- **本指引建議**：`bins = 20–30` 為適合大部分疫情資料的範圍

### 2. 填色與邊框

- 填色：主色 `#739A6D`
- **邊框**：白色 1 px——清楚分隔各 bin
- 不使用陰影、漸層或紋路填充

### 3. 統計線疊加

可在直方圖上疊加關鍵統計量：

- 中位數：`Terracotta #B5584A` 虛線
- 平均數：`Slate Blue #587A9D` 虛線
- 圖例註明，並在線旁標數值

### 4. X 軸要有明確區間單位

- 連續變數要顯示完整範圍與單位
- 例：年齡 0–100、住院天數 0–30

### 5. 不使用對數座標（除非極長尾分布）

若資料極度偏態，先嘗試：① 修剪極端值；② 改用密度圖；③ 才考慮對數軸。對數軸會讓非技術讀者困惑。

---

## 盒鬚圖 規範重點

### 1. 元素說明（須在第一次使用時提供圖例）

- **盒**：第 25 ~ 第 75 百分位（四分位距 IQR）
- **盒內中線**：中位數
- **鬚**：通常為 1.5 倍 IQR 範圍內的極值
- **離群點**：超出鬚範圍的個別點

公部門報告對外發布時，**第一次使用須加註說明**。

### 2. 顏色

- 盒填色：主色 alpha 0.7
- 盒邊框：主色加深版 `#5D7F58`
- 中位數線：`#374C34` 加粗 2 px
- 鬚線、上下底線：`#5D7F58` 1.5 px
- 離群點：`Neutral 400` 圓點，半透明（不要太搶眼）

### 3. 盒寬

- 多組比較時所有盒同寬
- 建議 `width = 0.55`（中等寬度）
- 不使用 violin plot 或變寬盒鬚——一般讀者難以解讀

### 4. 順序

- 若類別有自然順序（年齡層、嚴重度）：依自然順序
- 若是等位類別（區域、醫院）：依中位數由大到小排序，便於比較

### 5. 與直條圖混用

**不要在同一張圖混用盒鬚與直條。** 兩種圖式的視覺重量不同，會造成讀者誤解。需要時做兩張圖並排。

---

## 個別重點

### 直方圖凸顯雙峰

確診者年齡分布常呈現雙峰（年輕族群 + 高齡族群）。要呈現此特徵：

- bin 數量足夠（≥ 20）以解析雙峰
- 可疊加 KDE 密度曲線輔助
- 標註兩個峰位置

### 盒鬚圖跨區域比較

最適合的情境：6 個區域的住院天數分布。要點：

- 並列 6 個盒鬚，X 軸為區域名
- 共用 Y 軸（住院天數）
- 中位數高低一目了然
- 鬚的長短反映分布廣度（高變異性）

### 何時用直方圖、何時用盒鬚

| 情境 | 圖式 |
|------|------|
| 1 組資料、需看分布形狀 | 直方圖 |
| 2–3 組比較、需看形狀 | 多個直方圖並列（小倍數） |
| 4+ 組比較、只需關鍵統計量 | 盒鬚圖（並列） |
| 重點是「中位數差異」 | 盒鬚圖 |
| 重點是「分布有無偏態」 | 直方圖 |

---

## 程式碼範例

```python
import numpy as np
import matplotlib.pyplot as plt
from epidemic_palette import (
    PRIMARY, PRIMARY_DARK, PRIMARY_DARKER, NEUTRAL, ACCENT, apply_style
)
apply_style()

# 直方圖
fig, ax = plt.subplots(figsize=(8, 4.5))
ax.hist(ages_data, bins=25, color=PRIMARY,
        edgecolor="white", linewidth=1)
median = np.median(ages_data)
ax.axvline(median, color=ACCENT["terracotta"], linewidth=2,
           linestyle="--", label=f"中位數 = {median:.0f} 歲")
ax.set_xlabel("年齡")
ax.set_ylabel("人數")

# 盒鬚圖
bp = ax.boxplot(data_groups, labels=labels, patch_artist=True,
                widths=0.55,
                medianprops=dict(color=PRIMARY_DARKER, linewidth=2),
                flierprops=dict(marker="o", markersize=4,
                                markerfacecolor=NEUTRAL["400"],
                                markeredgecolor="none", alpha=0.5))
for patch in bp["boxes"]:
    patch.set_facecolor(PRIMARY)
    patch.set_alpha(0.7)
    patch.set_edgecolor(PRIMARY_DARK)
for line in bp["whiskers"] + bp["caps"]:
    line.set_color(PRIMARY_DARK)
```

---

## 範例圖

- `07a-histogram.png` — 確診者年齡分布直方圖（含中位數線）
- `07b-boxplot.png` — 各區域住院天數盒鬚圖

## 常見錯誤

| ✗ 錯誤 | ✓ 正確 |
|--------|--------|
| Bin 數 < 10（細節遺失） | 20–30 |
| Bin 數 > 50（噪音） | 20–30 |
| 直方圖無邊框（融合） | 白色 1 px 邊框 |
| 盒鬚圖未說明元素 | 第一次使用加註說明 |
| 離群點顏色搶眼 | Neutral 400 半透明 |
| 對外報告直接用對數軸 | 修剪極端值或改密度圖 |
| 同圖混用直條與盒鬚 | 分開做兩張並排 |
