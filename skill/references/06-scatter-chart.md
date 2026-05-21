# 06. 散佈圖／泡泡圖（Scatter / Bubble）

> 用於**探索兩個（或三個）連續變數之間的關係**。在流行病學中常用於風險因子分析。

## 適用情境

| 情境 | 範例 |
|------|------|
| 相關性探索 | 疫苗接種率 vs. 重症率 |
| 第三維度比較 | 縣市接種率、重症率、人口規模（泡泡） |
| 預測模型驗證 | 預測值 vs. 實際值（含對角線） |
| 群集識別 | 確診時長 vs. 住院天數，找出特殊群 |

## 不適用情境

- X 軸為類別變數 → 改用直條圖
- X 軸為時間 → 改用折線圖
- 資料點 < 10 個 → 改用直接數字或表格

---

## 規範重點

### 1. 資料點外觀

- **大小**：`s=80–100`（標準散佈圖）
- **顏色**：主色 `#739A6D`，alpha `0.65–0.75`
- **邊框**：主色加深版 `#5D7F58`，linewidth 1.2 px
- 半透明 + 邊框的組合能在資料點重疊時仍可辨識

### 2. 趨勢線（regression line）

當資料呈現明顯相關性時，可加上趨勢線：

- 顏色：`Neutral 400 #A2ABA0`（退為背景）
- 線型：**虛線**（避免被誤認為連續觀測值）
- 線寬：1.5 px
- 圖例標註相關係數：`"趨勢線 (r = -0.91)"`

### 3. 軸線必須有明確標籤與單位

散佈圖比其他圖式更依賴讀者自己解讀，**X 與 Y 軸標籤必須清楚標示變數名稱與單位**。例如：

- ✓ "疫苗完整接種率（%）"
- ✗ "接種率"

### 4. 凸顯特殊資料點

若有需要凸顯的異常點（如離群值、政策實施前後的縣市），使用：

- 邊框顏色變為 `Alert Red #BE373C` 或 `Terracotta`
- 旁邊加文字標籤標註該點

### 5. 不使用回歸方程式作為主視覺

回歸方程式（如 `y = -0.10x + 12`）應放於圖表副標題或註腳，**不要疊在資料上方**——會干擾散點本身的視覺。

---

## 個別重點

### 散佈圖 vs. 相關係數

散佈圖最重要的價值在於呈現「相關性的形狀」，而不只是「相關係數」。同樣 r = 0.7 的兩組資料可能形狀完全不同（Anscombe's quartet）。

**永遠先看散佈圖，再看相關係數。** 在圖中標註 r 值是輔助，散點分布本身才是主訊息。

### 泡泡圖（Bubble Chart）

加入第三維度：用點的**面積**表示第三變數。要點：

- **面積（不是直徑）正比於數值**——這是讀者直覺判讀的方式
  - 若用 `s` 參數，matplotlib 的 `s` 表示面積，直接正比即可
- 提供「大小參考」圖例（如「50 萬人、200 萬人、400 萬人」）
- 透明度更低（alpha 0.55）以利重疊辨識
- 大泡泡內標註類別名稱（如縣市名）

當資料點很多（> 30）時，泡泡圖容易混亂。**建議資料點 ≤ 20。**

### 雙變數密度的處理

當資料點極多（數百以上）且大量重疊：

- 改用 hexbin（六邊形分箱）或 2D histogram
- 或對散點增加 jitter（隨機微擾）並降低 alpha 至 0.1–0.2

### 對角線參考（預測 vs. 實際）

呈現模型預測準確性時，加上 y = x 對角線：

- 顏色：`Neutral 400` 虛線
- 標籤："完美預測線"
- 資料點與此線的距離 = 預測誤差

---

## 程式碼範例

```python
import numpy as np
import matplotlib.pyplot as plt
from epidemic_palette import PRIMARY, PRIMARY_DARK, NEUTRAL, apply_style
apply_style()

# 散佈圖 + 趨勢線
fig, ax = plt.subplots(figsize=(7.5, 5))
ax.scatter(x, y, s=90, color=PRIMARY,
           alpha=0.75,
           edgecolors=PRIMARY_DARK, linewidths=1.2)

# 趨勢線
z = np.polyfit(x, y, 1)
p = np.poly1d(z)
x_line = np.linspace(x.min(), x.max(), 50)
r = np.corrcoef(x, y)[0, 1]
ax.plot(x_line, p(x_line), color=NEUTRAL["400"],
        linewidth=1.5, linestyle="--",
        label=f"趨勢線 (r = {r:.2f})")

ax.set_xlabel("疫苗完整接種率（%）")
ax.set_ylabel("重症發生率（每千例）")

# 泡泡圖（s 為面積）
sizes = [pop * 4 for pop in populations]  # 縮放
ax.scatter(x, y, s=sizes, color=PRIMARY,
           alpha=0.55, edgecolors=PRIMARY_DARK)
for i, name in enumerate(city_names):
    ax.annotate(name, (x[i], y[i]),
                fontsize=9, ha="center", va="center",
                fontweight="bold")

# 大小參考圖例
for ref_size, label in [(50, "50 萬"), (200, "200 萬"), (400, "400 萬")]:
    ax.scatter([], [], s=ref_size*4, color=PRIMARY, alpha=0.55,
               edgecolors=PRIMARY_DARK, label=label)
ax.legend(title="人口規模", labelspacing=1.5, borderpad=1)
```

---

## 範例圖

- `06a-scatter-correlation.png` — 接種率 vs. 重症率（含趨勢線）
- `06b-bubble-3rd-dimension.png` — 各縣市三維泡泡圖

## 常見錯誤

| ✗ 錯誤 | ✓ 正確 |
|--------|--------|
| 不透明圓點互相遮蓋 | alpha 0.65–0.75 |
| 趨勢線用實線 | 虛線（避免誤認為觀測） |
| 趨勢線使用主色 | 用中性灰退為背景 |
| 泡泡大小用直徑正比 | 用面積正比（matplotlib `s` 預設正確） |
| 泡泡圖 30+ 個點（擁擠） | ≤ 20 個，或改 hexbin |
| 軸標籤無單位 | 必標單位（%, 例/千、年） |
| 只看 r 值不看散點形狀 | 散點形狀是主訊息 |
