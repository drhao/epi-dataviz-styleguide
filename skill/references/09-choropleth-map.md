# 09. 面量圖／熱力圖（Choropleth / Heatmap）

> 用於**在二維空間（地理或矩陣）上呈現數值差異**。面量圖用於真實地圖；熱力圖用於矩陣狀資料。

## 兩種子類型

### 面量圖（Choropleth）

地理區域填色，例如台灣 22 縣市的發生率地圖。需要 GeoJSON 或 shapefile。

### 熱力圖（Heatmap）

矩陣狀資料填色，例如「縣市 × 月份」的發生率。本指引以此作為主要範例（不需地理檔案）。

---

## 適用情境

| 圖式 | 範例 |
|------|------|
| 面量圖 | 各縣市發生率地圖、各國致死率地圖 |
| 熱力圖（時間 × 地區） | 各縣市每月發生率 |
| 熱力圖（兩變數交叉） | 年齡層 × 嚴重度的人數 |
| 熱力圖（相關係數矩陣） | 多指標的相關性 |

---

## 規範重點

### 1. 配色：序列 vs. 發散

**序列色階（單向，低→高）：**
- 適用於有自然順序、無中點的資料（如發生率、人口密度）
- 使用本指引序列色階（7 色）：`#F1F5F0 → ... → #354832`
- 顏色越深表示數值越大

**發散色階（雙向，負←中→正）：**
- 適用於有自然中點的資料（如預期 vs. 實際的差異、變化率）
- 使用本指引發散色階（7 色）：`#476043 ← ... → #965440`
- 中性過渡色 `#F2F3F2`（非純白！）

**重要**：發散色階的中央**不可使用純白**，否則零值會被誤認為「無資料」。

### 2. 色階離散化（discretize）

連續色階雖然平滑，但讀者難以將顏色對應到具體數值。**建議使用 5–7 個離散色階**：

```python
from matplotlib.colors import BoundaryNorm
levels = [0, 100, 300, 500, 700, 900, 1200]
norm = BoundaryNorm(levels, ncolors=cmap.N)
```

色階斷點應對應**有意義的閾值**（如警戒值、政策標準），不要機械等分。

### 3. 色階條（colorbar）

- 必須有清楚的數值刻度與單位
- 大小：`shrink=0.7–0.85`（不要佔太多空間）
- 位置：圖表右側（直向）或下方（橫向）
- 標籤字級：與軸刻度一致（10–11 px）

### 4. 缺失資料的處理

- **絕對不可填白色**（會被誤認為「最低值」或「零」）
- 使用 `Neutral 300 #CACFC9` 填色
- 在圖例中加註「灰色 = 無資料」

### 5. 標籤策略

- 矩陣每格的數值是否標註？
  - 格子數 ≤ 50：**標註**，提供精確資訊
  - 格子數 51–150：標註重點格（極值）
  - 格子數 > 150：不標註，仰賴顏色

- 標籤對比：當填色深時用白色文字，淺時用深色文字
  - 可用 `Neutral 700 #444C43`（深）與 `#FFFFFF`（淺）自動切換
  - 切換閾值：色階的中段位置

### 6. 排序

- 地理面量圖：依地理位置（不可排序）
- 矩陣熱力圖（無自然順序的類別）：**依平均值排序**，能凸顯模式
- 時間軸：依時序（不可排序）

---

## 個別重點

### 面量圖的標準化

呈現各縣市疫情時，**必須標準化為「每 10 萬人口」**，否則人口大的縣市永遠最深。這是疫情視覺化最常被忽略的錯誤。

### 熱力圖的方向選擇

| 行 × 列 | 適用 |
|---------|------|
| 縣市 × 月份 | 看「哪些縣市在哪些月份較嚴重」 |
| 變數 × 變數 | 相關係數矩陣（對稱） |
| 年齡 × 嚴重度 | 看交叉分布的密度 |

**Y 軸排序原則**：
- 若 Y 軸是地理或自然順序：依地理排（北到南、行政區順序）
- 若是非自然順序的類別：依資料的平均值由大到小排，凸顯模式

### 雙色階的選擇

當需要同時呈現「正向超標」與「負向不足」（如預測 vs. 實際的差異）：

- 使用本指引發散色階
- 中性過渡色 `#F2F3F2`（**非純白**）
- 色階對稱（正負最大值絕對值相同）

例：今年發生率減去去年同期，正值（綠端）表上升，負值（紅端）表下降，零（淺灰）表無變化。

### 矩陣熱力圖的網格

- 各格之間留 1 px 白色間隔
- 不需要外框，色塊本身就是邊界
- 標題、X/Y 軸標籤須有明確的單位

---

## 程式碼範例

```python
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from epidemic_palette import SEQUENTIAL, DIVERGING, NEUTRAL, apply_style
apply_style()

# 建立序列色階
cmap = LinearSegmentedColormap.from_list("epi_seq", SEQUENTIAL, N=256)

# 熱力圖
fig, ax = plt.subplots(figsize=(9.5, 5))
im = ax.imshow(data, cmap=cmap, aspect="auto")
ax.set_xticks(np.arange(len(months)))
ax.set_yticks(np.arange(len(cities)))
ax.set_xticklabels(months)
ax.set_yticklabels(cities)

# 色階條
cbar = fig.colorbar(im, ax=ax, shrink=0.8)
cbar.set_label("發生率（每 10 萬人口）", fontsize=10, color=NEUTRAL["700"])

# 取消網格,色塊本身就是邊界
ax.grid(False)

# 發散色階（雙向）
diverging_cmap = LinearSegmentedColormap.from_list("epi_div", DIVERGING, N=256)
im = ax.imshow(diff_data, cmap=diverging_cmap,
               vmin=-100, vmax=100,  # 強制對稱
               aspect="auto")
```

---

## 範例圖

- `09-choropleth-heatmap.png` — 縣市 × 月份的發生率熱力圖

## 常見錯誤

| ✗ 錯誤 | ✓ 正確 |
|--------|--------|
| 縣市比較用絕對數 | 標準化為每 10 萬人口 |
| 發散色階中心用純白 | 用 `#F2F3F2` 淺灰綠 |
| 連續色階（讀者難對應數值） | 5–7 個離散色階 |
| 缺失資料填白色 | 填 `Neutral 300` + 圖例註明 |
| 色階斷點機械等分 | 對應有意義的閾值 |
| 全部標數值（過於擁擠） | 視格子數量決定 |
| Y 軸隨機排序 | 依平均值或自然順序 |
| 發散色階非對稱 | 強制 `vmin=-max, vmax=+max` |
