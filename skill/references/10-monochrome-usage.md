# 10. 單色使用情境（Monochrome）

> 用**主色階**（同色相、不同明度）取代類別配色，適用於「顏色不傳達類別差異」的情境。

## 為何需要單色情境

類別配色（綠藍黃...）會強烈暗示「這些是不同的東西」。但很多疫情圖表中，序列彼此**有自然順序**而非「不同類別」——此時用不同色相反而是雜訊，會干擾讀者抓到「序列本身的關係」。

| 用類別配色（不同色相） | 用單色色階（同色相不同明度） |
|------|------|
| 暗示「這些是無關的不同類別」 | 暗示「這些彼此有關，只是程度／層次不同」 |
| 適合：縣市、變異株、業務類型 | 適合：嚴重度、年齡、時期、劑次、四分位數 |
| 視覺重點：色塊區分 | 視覺重點：資料形狀 |

---

## 適用情境

### 1. 序數類別（有自然順序）

- **嚴重度**：輕症 → 中症 → 重症 → 極重症
- **年齡層**：0–9, 10–19, ..., 80+（年齡本身就是序數）
- **教育程度**：國小、國中、高中、大學、研究所
- **發病天數**：1–3 天、4–7 天、8–14 天、15+ 天

### 2. 時序比較

- **歷次波次**：第一波、第二波、第三波、當前波
- **季別**：Q1、Q2、Q3、Q4
- **月份序列**：當需要強調「時間越來越近，色越深」

### 3. 同主題的多指標

- **疫苗劑次**：第 1 劑、第 2 劑、第 3 劑、追加劑（都是「累計接種」這個同類概念的不同階段）
- **追蹤天數**：5 日、10 日、20 日、30 日累積數
- **百分位數**：P25、P50、P75、P90

### 4. 焦點 + 對照

- **本機關 vs 其他**：本機關用深色，其他用淺色 / 中性灰
- **本年 vs 歷年**：今年用深主色，歷年用淺主色

### 5. 強度遞進的分組

- **風險等級**：低風險、中風險、高風險、極高風險
- **數量區間**：< 100、100–500、500–1000、1000+

---

## 不適用情境

凡是**真正的「並列類別」**——彼此地位平等、無自然順序，請使用類別配色：

- ✗ 各縣市（彰化和雲林沒有「強度大小」之分） → 用 CATEGORICAL 或 cat-1 主色凸顯焦點
- ✗ 不同變異株（JN.1 vs KP.2 沒有遞進關係） → 用 CATEGORICAL
- ✗ 不同部門（教育部、社福部沒有層級） → 用 CATEGORICAL

**判斷標準**：問自己「這幾個序列**有沒有自然順序？」**
- 有 → 用單色
- 沒有 → 用類別配色

---

## 預設組合（Python 模組）

`epidemic_palette.py` 提供了 6 組常用單色組合：

```python
from epidemic_palette import MONOCHROME

MONOCHROME["focus_2"]    # 2 序列:焦點 + 對照（深綠 + 中性灰）
MONOCHROME["scale_3"]    # 3 序列:淺 → 中 → 深
MONOCHROME["scale_4"]    # 4 序列:細緻 4 階
MONOCHROME["scale_5"]    # 5 序列:5 個年齡層、5 個區間
MONOCHROME["scale_6"]    # 6 序列:完整年齡帶
MONOCHROME["scale_7"]    # 7 序列:一週、7 個年齡組
```

選擇邏輯：**有幾個序列就選對應的 scale_N**。超過 7 個序列時建議改用熱力圖或合併類別。

---

## 規範重點

### 1. 永遠由淺至深對應「弱→強」、「過去→現在」

色階方向必須有意義：
- ✓ 輕症（淺）→ 重症（深）
- ✓ 第一波（淺）→ 當前波（深）
- ✓ 第 1 劑（淺）→ 第 3 劑（深）
- ✗ 反向會造成讀者誤解

### 2. 色階之間必須有清楚對比

如果使用 6 個序列，6 個色階之間視覺上要能清楚區分。`MONOCHROME["scale_6"]` 已經設計過跳階——不是均勻地從 50 到 900，而是**重點在「中段」拉開差距**（避免淺色互相黏在一起）。

不要自己組「均勻分佈」的色階：

```python
# ✗ 6 階均勻（淺色彼此難分）
bad = ["#F6F9F6", "#E8EEE7", "#D1DECF", "#B4C9B1", "#91B08C", "#739A6D"]

# ✓ 本指引建議（中段拉開）
good = MONOCHROME["scale_6"]
```

### 3. 焦點對象使用最深色 + 線寬加粗

當有「需強調的對象」時（如當前波、本機關）：
- 色：使用色階中**最深**那一格
- 線寬：比其他粗 0.5–1px
- 標記點：只在焦點線上加 marker

```python
mono4 = MONOCHROME["scale_4"]
for vals, color, is_focus in zip(series_list, mono4, focus_flags):
    ax.plot(x, vals, color=color,
            linewidth=3 if is_focus else 1.8,
            marker="o" if is_focus else None)
```

### 4. 加白色邊線增強堆疊區分

單色堆疊長條／區域圖中，相鄰色階若太接近，加 1 px 白色邊線就能清楚分隔：

```python
ax.bar(x, mild, color=mono3[0], edgecolor="white", linewidth=0.5)
ax.bar(x, mod, bottom=mild, color=mono3[1], edgecolor="white", linewidth=0.5)
```

### 5. 跨圖一致

同一份報告中，若某個指標用了單色（如嚴重度色階），所有相關圖表都該用同一組色階。讀者習慣「深色 = 重症」後，跨圖能直覺對應。

---

## 何時選單色 vs 何時選類別配色

| 情境 | 序列數 | 推薦 |
|------|-------|------|
| 嚴重度（輕／中／重） | 3 | `MONOCHROME["scale_3"]` |
| 年齡 × 性別人口金字塔 | 2 組 | 類別配色（性別非序數）+ 軸對稱 |
| 22 縣市排名 | 22 | 單色主色 + Terracotta 標警示 |
| 6 種變異株 | 6 | 類別配色（變異株並列無序） |
| 疫苗 1/2/3 劑覆蓋率 | 3 | **`MONOCHROME["scale_3"]`** |
| 三家醫院床位使用率 | 3 | 類別配色（醫院並列） |
| 歷次 4 波疫情比較 | 4 | **`MONOCHROME["scale_4"]`**，當前波最深 |
| 縣市發生率熱力圖 | 連續 | 序列色階 SEQUENTIAL |

---

## 程式碼範例

```python
import matplotlib.pyplot as plt
from epidemic_palette import (
    MONOCHROME, PRIMARY_DARKER, ACCENT, NEUTRAL, apply_style
)
apply_style()

# 範例 A: 單色堆疊長條（嚴重度為序數）
ages = ["0-9", "10-19", "20-39", "40-59", "60-69", "70-79", "80+"]
mild, mod, sev = [...], [...], [...]  # 各序列資料

colors_3 = MONOCHROME["scale_3"]
fig, ax = plt.subplots(figsize=(9, 4.5))
ax.bar(ages, mild, color=colors_3[0], width=0.6,
       edgecolor="white", linewidth=0.5, label="輕症")
ax.bar(ages, mod, bottom=mild, color=colors_3[1], width=0.6,
       edgecolor="white", linewidth=0.5, label="中症")
ax.bar(ages, sev, bottom=[a+b for a,b in zip(mild,mod)],
       color=colors_3[2], width=0.6,
       edgecolor="white", linewidth=0.5, label="重症")

# 範例 B: 單色多折線（波次比較,當前波最深最粗）
mono4 = MONOCHROME["scale_4"]
for (label, vals), c in zip(waves.items(), mono4):
    is_current = "本波" in label
    ax.plot(days, vals, color=c,
            linewidth=3 if is_current else 1.8,
            label=label)

# 範例 C: 焦點 + 對照(2 序列)
mono2 = MONOCHROME["focus_2"]
ax.plot(years, ours, color=mono2[0], linewidth=2.5,
        marker="o", label="本機關")
ax.plot(years, avg, color=mono2[1], linewidth=1.5,
        linestyle="--", label="同類機關平均")
```

---

## 範例圖

- `10a-mono-stacked-severity.png` — 年齡層 × 嚴重度（單色堆疊,色階反映嚴重度）
- `10b-mono-line-waves.png` — 歷次波次比較（單色折線,當前波最深最粗）
- `10c-mono-area-doses.png` — 疫苗 1/2/3 劑覆蓋率（單色堆疊區域）

## 常見錯誤

| ✗ 錯誤 | ✓ 正確 |
|--------|--------|
| 用 cat-1/cat-2/cat-3 畫嚴重度（綠藍黃） | 用 `MONOCHROME["scale_3"]`（淺→中→深） |
| 色階方向倒過來（重症淺、輕症深） | 強度對應明度,深色=重 |
| 6 階均勻分布（淺色互相難分） | 用本指引預設的 `scale_6`（中段拉開）|
| 單色堆疊無邊線（色塊融合） | 加 1 px 白色 edgecolor |
| 報告中時而單色時而類別色（同指標） | 同指標跨圖一致用單色 |
| 為了「視覺豐富」把單色情境改用類別色 | 顏色服務於訊息,不為豐富而豐富 |
