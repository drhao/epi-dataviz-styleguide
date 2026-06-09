---
status: active
rfc: 2026-06-02-small-multiples
since: 2026-06-09
promoted: 2026-06-09
---

# M2 · Small Multiples 版面 Modifier

> 對應 RFC:[2026-06-02](../../docs/rfcs/2026-06-02-small-multiples.md)
>
> **本規範為 layout modifier**,套在既有 chart-type(line / bar / area)上,**不創新獨立 pattern**。處理「同一指標 × 多分類維度」的多 panel 並排場景。

## 定位

M2 是 **layout modifier**(版面結構),與 M1(uncertainty modifier)並列,都套在既有 Pattern 與 chart-type 上:

- 與 Pattern A 兼容:焦點 panel 機制(規則 7)
- 與 Pattern E 部分兼容:序數類別當 panel 維度
- 與 Pattern B 通常不一起用(分 panel 後類別配色失意義)
- 與 M1 銜接:多序列 CI 帶疊太亂(> 3 條)→ small multiples 每 panel 一條

## 適用情境

- 多 panels(2-25)同一指標、不同分類維度
- 觀察各別 panel 的形狀(而非「跨類別比例」── 後者用堆疊圖)
- M1 的 multi-series CI fallback

**典型場景**:

1. **22 縣市同指標並排**(地理維度):4×6 grid
2. **各年齡組曲線**(人口分組):8-9 panels
3. **跨年度同期比較**(時間維度,5-6 年以上):每年一 panel ── 少於 4 年仍以 `02-line-chart.md` 同期比較風格(疊一張 + 灰色歷史範圍帶)
4. **變異株各自時序**(疾病維度):每株一 panel

## 不適用情境

- **各 panel 的 X / Y 範圍差異極大且無法標準化** ── 例:絕對人次,人口從 5 萬到 500 萬縣市,改用「每 10 萬人發生率」標準化後才能 small multiples
- **強調「整體 vs 子集」對比** ── 用 Pattern A 焦點圖,不要拆 panel
- **跨類別組成比例**(變異株月份占比)── 用堆疊圖

## 不優先建議(可用但要評估)

- **只有 2-3 個 panel**:通常同圖比較即可,不必拆 panel。**但若一張圖同時呈現多指標 / 多資訊複雜度過高**(例:一張圖含 3 條折線 + 2 個區間帶 + annotation),拆成 2-3 panel 簡化是合理選擇

## 邊界案例

- **Panel > 25**:強制建議重新分組(22 縣市 → 6 區域)或排序篩選前 N
- **Panel 數量為「不規則」**:5 panel 用 2+3 layout;靠右下方空缺處放圖例
- **Panel 帶 CI**(銜接 M1):每 panel 內套用 M1 規則
- **焦點 panel**:該 panel 用 PRIMARY,其餘 NEUTRAL.300(規則 7)
- **各 panel 資料量不均**:仍要呈現,標 `N < threshold` warning,不可移除

---

## 規則細節

**1. 統一 Y 軸 scale**(rule of comparability):所有 panel 同 Y 範圍,讀者掃視時可直接比較波形高度。各 panel magnitude 差太大且不能標準化時,用「相對 scale」(每 10 萬人發生率)轉換後統一

**2. 統一 X 軸範圍與 ticks**:即使某 panel 該段無資料也保留空白

**3. 共用圖例**:放整體**上方或下方**,不在每 panel 重複

**4. 共用 X / Y 軸標題**:放整體**左外(Y)**與**下外(X)**

**5. Panel 標題位置**:**左上**(matplotlib `ax.set_title(..., loc="left")`),字級小於主標題 2 級,顏色 `NEUTRAL.700`(`#444C43`)

**6. Panel 數量建議與 grid 推薦**:

| Panel 數 N | 推薦 grid | 備註 |
|---|---|---|
| 2-3 | 1×2 / 1×3 / 2×2(留空缺) | **不優先建議** ── 通常同圖比較即可,複雜場景才拆 |
| 4-6 | 2×3 或 3×2 | |
| 7-9 | 3×3 | |
| 10-12 | 3×4 或 4×3 | |
| 13-16 | 4×4 | |
| 17-22 | 4×6 或 5×5(留空缺) | 22 縣市典型 |
| > 25 | **強制建議重新分組** | 6 區域、年齡 0-19/20-59/60+ 等 |

**7. 焦點 panel 配色**(Pattern A 兼容):
- **焦點 panel**:用 `PRIMARY` `#739A6D`
- **非焦點 panel**:用 **`NEUTRAL.300` `#CACFC9` 為預設**(視覺對照定稿:讓焦點清楚跳出,非焦點作為位置參考)
- **若各 panel 內波形細節重要**(讀者需從非焦點 panel 讀到資訊):非焦點改用 `NEUTRAL.400` `#A2ABA0`,可讀性高但對比較弱
- **焦點 panel 標題**用主色強調,非焦點標題用 `NEUTRAL.700`

**8. Panel 邊框**:輕邊框 `NEUTRAL.200`(`#E4E7E4`)1px;頂右框沿用既有規範可移除(panel 內仍保留底軸與左軸)

**9. Panel 間距**:matplotlib `plt.tight_layout()` 預設足夠;手動微調 `wspace=0.25, hspace=0.35` 為起點

**10. Annotation 與標籤策略**:大量 panel 場景優先順序:
- 必留:panel 標題、Y 軸數值刻度
- 視情境:X 軸標籤(若 grid 行內 panel > 4 個,僅最下方一行標)
- 移除:每 panel 重複圖例、每 panel 重複 X/Y 軸標題

**11. 與 M1 uncertainty 兼容**:每 panel 內可套用 M1 規則 1-13。多 panel 場景下 CI 帶不需在每 panel 標 legend ── 共用圖例已標一次即可

**12. 與 Pattern A/B/C/D/E 兼容**:
- **Pattern A + M2**:焦點 panel 主色 + 其餘 N.300(規則 7)── 最常用組合
- **Pattern B + M2**:**通常不一起用** ── 既然分 panel 看波形,類別配色在 panel 內單線(只有一線)沒意義
- **Pattern E + M2**:可能(序數類別當 panel 維度,例:輕/中/重症 panel 並排),用 MONOCHROME.scale_3 為 panel 標題色

---

## 程式碼範例

### 範例 A · 22 縣市並排(use case 1)

```python
from epidemic_palette import apply_style, PRIMARY, NEUTRAL
import matplotlib.pyplot as plt

apply_style()
fig, axes = plt.subplots(4, 6, figsize=(15, 9),
                          sharex=True, sharey=True)  # 規則 1+2

focus_city = "臺北市"

for ax, (city, data) in zip(axes.flat, cities_data):
    is_focus = (city == focus_city)
    # 規則 7:焦點 PRIMARY,非焦點 NEUTRAL.300(可讀性需求改 .400)
    color = PRIMARY if is_focus else NEUTRAL["300"]
    ax.plot(data["week"], data["rate"],
            color=color, linewidth=2.0 if is_focus else 1.5)
    ax.set_title(city, loc="left",
                 color=PRIMARY if is_focus else NEUTRAL["700"],
                 fontsize=11)
    for s in ["top", "right"]:
        ax.spines[s].set_visible(False)

# 規則 3+4:共用標題與軸
fig.suptitle("各縣市每週確診率(每 10 萬人)", x=0.1, ha="left")
fig.supxlabel("Week")
fig.supylabel("發生率")

# 隱藏空缺 panel
for ax in axes.flat[22:]:
    ax.set_visible(False)

plt.tight_layout()
```

### 範例 B · 跨年度同期 + M1 uncertainty(use case 3 + 5,M2 與 M1 銜接)

```python
# 5 年同期比較,2025 是當年(焦點 + 預測 CI)
fig, axes = plt.subplots(2, 3, figsize=(13, 6),
                          sharex=True, sharey=True)

for ax, (year, data) in zip(axes.flat, years_data.items()):
    is_current = (year == "2025")
    color = PRIMARY if is_current else NEUTRAL["300"]  # 規則 7
    if is_current and "ci_low" in data:  # M1 規則 1:預測段 CI 帶
        ax.fill_between(data["week"], data["ci_low"], data["ci_high"],
                        color=PRIMARY_LIGHT, alpha=0.30)
    ax.plot(data["week"], data["rate"], color=color,
            linewidth=2.5 if is_current else 1.5,
            linestyle="--" if is_current else "-")  # M1 規則 5:預測虛線
    ax.set_title(year, loc="left",
                 color=PRIMARY if is_current else NEUTRAL["700"])
```

---

## 常見錯誤

| ✗ 錯誤 | ✓ 正確 |
|---|---|
| 各 panel Y 軸獨立 auto scale | `sharey=True` 統一 scale,跨 panel 直接比較 |
| 每 panel 重複完整圖例 | 共用圖例放整體外圍(規則 3) |
| Panel 標題置中或下方 | 左上 `loc="left"`(規則 5) |
| 焦點 panel 用 PRIMARY_DARKER(過深) | PRIMARY `#739A6D`(規則 7 定稿) |
| 非焦點用 NEUTRAL.500(對比不夠) | NEUTRAL.300 預設(規則 7),可讀性需求改 N400 |
| 22 panel 用 6×6 grid(留 14 空缺) | 4×6(只留 2 空缺,看起來緊湊) |
| 3 panel 預設拆 small multiples | 通常同圖比較;**只有複雜度高才拆 2-3 panel** |
| 跨年度 3 年用 small multiples | < 4 年用 `02c-line-year-over-year` 風格(疊一張) |

---

## 範例圖

預生成範例位於 `skill/assets/examples/`:

- `m2a-small-multiples-cities.png` — 22 縣市每週發生率並排(use case 1,焦點 + 5 個淺色非焦點)
- `m2b-small-multiples-yearly-with-uncertainty.png` — 跨年度同期 + 2025 預測 CI(use case 3 + M1 銜接示範)

生成函式:`skill/scripts/generate_examples.py` 內的 `small_multiples_examples()`

## 與其他規範的關係

- **`02-line-chart.md` 「同期比較」段**:處理 2-3 年同期比較(疊一張 + 灰色歷史範圍帶),與本 M2 並存。年份 ≥ 5-6 用 M2,< 4 年用 02-line 的 02c 風格
- **`M1-uncertainty-modifier.md` 規則 1 邊界**:多條 CI 帶疊太亂(> 3 條序列)時 fallback 至 M2,每 panel 一條 + 該條 CI 帶
- **Pattern A 焦點**:M2 規則 7 焦點機制本身就是 Pattern A 在多 panel 場景的延伸
