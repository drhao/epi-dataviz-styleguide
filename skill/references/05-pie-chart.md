# 05. 圓餅圖／甜甜圈圖（Pie / Donut）

> **條件使用圖表。** 本指引將其列為「需謹慎使用」類別，多數情況下優先使用[水平堆疊條](04-stacked-chart.md)。

## 為何謹慎使用

人眼對「扇形角度」的判讀遠不如「長度」精確。多項實驗顯示讀者經常誤判 5–10% 的差異。圓餅圖視覺直觀但**不利於精確比較**，且**幾乎不可能在多個圓餅之間做比較**。

---

## 適用情境（所有條件須同時成立）

- ✓ 類別數 **2–4 個**
- ✓ 總和為 **100%**
- ✓ **單一時點**，無需跨期比較
- ✓ 切片差異 **≥ 5%**（小於此值人眼難以區分）
- ✓ 視覺直覺優先於精確讀取

## 不適用情境（任一成立則改用其他圖式）

- ✗ 類別 > 4 個 → 改用水平堆疊條
- ✗ 切片差異 < 5% → 改用水平長條（精確比較）
- ✗ 需要跨時點比較 → 改用 100% 堆疊長條
- ✗ 需要精確讀取百分比 → 改用水平長條 + 直接標籤
- ✗ 多個圓餅並列 → 一律改用堆疊長條

---

## 規範重點

### 1. 直接標籤（必要）

**百分比與類別名稱必須標於切片旁，不依賴圖例。** 圓餅圖讀者已經要費力判讀扇形大小，再去比對圖例會大幅降低可讀性。

### 2. 不使用 3D 效果

3D 圓餅會嚴重扭曲比例感受（前景的切片看起來比後景的大）。**絕對禁止使用**。

### 3. 切片排序

- **由大到小排序**
- 從 12 點鐘方向**順時針**開始
- matplotlib 預設是逆時針，需設定 `counterclock=False`
- `startangle=90` 讓最大切片從 12 點開始

### 4. 顏色策略

依本指引類別配色順序使用：cat-1（最大切片）→ cat-2 → ... → cat-N。
**「其他」永遠用 `Neutral 300 #CACFC9`。**

不為追求視覺效果而採用高飽和或彩虹色。

### 5. 切片之間的白邊

加 1.5–2 px 白色邊框分隔切片，避免相鄰類似色融在一起。

### 6. 百分比標籤對比

- 切片內標籤：白色粗體，搭配深色填色（主色 500 以下都夠深）
- 切片外標籤：使用 `Neutral 800 #2C312B` 內文色

---

## 圓餅 vs. 甜甜圈

**甜甜圈圖（Donut）的優勢：**
- 中心可放置關鍵數字（如主要切片的百分比），加強訊息聚焦
- 視覺較圓餅輕盈

**甜甜圈圖的限制：**
- 中心挖空進一步降低判讀精度（厚度比扇形更難辨識）
- **若不放中心數字，就不要用甜甜圈，回到圓餅**

甜甜圈的環厚度：佔半徑的 35–45%（`width=0.4`）。

---

## 個別重點

### 「其他」類別的處理

當你想用圓餅但發現有 6+ 類，**先合併小於 5% 的類別為「其他」**。

合併後若仍超過 4 類，改用水平堆疊條。

### 與水平堆疊條的比較

同樣呈現「確診者疫苗接種狀態」的範例：

| 圖式 | 優點 | 缺點 |
|------|------|------|
| 圓餅 | 一眼看出「主要 vs. 其他」 | 無法精確比較第 2、3 切片 |
| 水平堆疊條 | 可精確比較，可跨時期比較 | 第一眼較不「直覺」 |

**判斷標準**：若你的圖表會被報告作者反覆閱讀或用於精確決策 → 水平堆疊條；若只是儀表板首頁的「一眼瀏覽」項目 → 可考慮圓餅或甜甜圈。

---

## 程式碼範例

```python
import matplotlib.pyplot as plt
from epidemic_palette import PRIMARY, CATEGORICAL, NEUTRAL, apply_style
apply_style()

labels = ["已完整接種", "部分接種", "未接種", "不詳"]
sizes  = [62, 18, 14, 6]
colors = [PRIMARY, CATEGORICAL[1], CATEGORICAL[2], NEUTRAL["300"]]

fig, ax = plt.subplots(figsize=(7, 5))
wedges, texts, autotexts = ax.pie(
    sizes, labels=labels, colors=colors,
    autopct=lambda p: f"{p:.0f}%",
    startangle=90,
    counterclock=False,        # 順時針
    wedgeprops=dict(edgecolor="white", linewidth=2),
    pctdistance=0.78,
)
# 白色粗體百分比
for at in autotexts:
    at.set_color("white")
    at.set_fontweight("bold")

# 甜甜圈圖（中心放關鍵數字）
ax.pie(sizes, ...,
       wedgeprops=dict(width=0.4, edgecolor="white", linewidth=2))
ax.text(0, 0.1, "62%", ha="center", va="center",
        fontsize=32, fontweight="bold", color=PRIMARY_DARKER)
ax.text(0, -0.18, "完整接種率", ha="center", va="center",
        fontsize=11, color=NEUTRAL["600"])
```

---

## 範例圖

- `05a-pie-standard.png` — 標準圓餅（4 類）
- `05b-donut-with-center.png` — 甜甜圈圖（中心強調主要數字）

## 常見錯誤

| ✗ 錯誤 | ✓ 正確 |
|--------|--------|
| 6+ 類別的圓餅 | 合併為「其他」或改水平堆疊條 |
| 3D 效果 | 平面 |
| 切片未排序 | 由大至小，12 點順時針開始 |
| 切片差異 < 5% | 改用水平長條（人眼難辨） |
| 純依賴圖例 | 直接標籤（類別 + 百分比） |
| 兩個圓餅並列比較 | 改用 100% 堆疊長條 |

**視覺對照圖**(`skill/assets/examples/dont-vs-do/`):

- `04-decorated-pie.png` ── 3D / 陰影 / explode / 鮮豔色 vs 平面 2D + Pattern B + 直接標籤
- `05-too-many-pie-slices.png` ── 圓餅 9 切片 vs 排序橫條由大到小
| 切片用彩虹色 | 依本指引類別配色順序 |
| 甜甜圈無中心數字 | 改用圓餅，或加上中心數字 |
