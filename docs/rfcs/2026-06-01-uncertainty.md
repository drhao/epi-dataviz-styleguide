# RFC 2026-06-01: 不確定性視覺化

- **作者**: Dr. Hao
- **提案日期**: 2026-06-09
- **狀態**: Draft
- **目標版本**: v1.1(待 Pilot 試行後決定)

## Context · 為什麼需要這個規範

疫情報告幾乎必然涉及不確定性:R/Rt 預測、變異株比例估計、超額死亡推算、抗體血清陽性率等都帶有統計上下界。但本指引目前完全沒規範這類視覺呈現 ── 結果是:

- AI agent 生成預測圖時各自為政:有的用 error bar、有的用 alpha 帶、有的乾脆畫成兩條虛線
- 既有 references 提到「歷史範圍 ±1 SD」(02c-line-year-over-year.png)但只是個案,沒上升為規範
- 讀者看到不同分析師的圖會用不同方式呈現 CI,降低跨報告比較性

### Real use cases

1. **每週 R/Rt 估計**:中央流行疫情指揮中心發布每週 Rt 點估計與 95% CI 帶。讀者最常追蹤「Rt 是否跨過 1.0 警戒線」,因此 CI 是否覆蓋 1.0 是關鍵訊息
2. **變異株消長預測**:模型輸出未來 4 週各變異株占比預測,每個變異株 都有預測區間。當前作法是用實線畫過去 + 虛線畫未來,但未來段沒明確標示不確定性
3. **超額死亡估計**:與歷史 baseline 比較,baseline 本身有歷史變異(過去 5 年同期 ±1 SD)。02c-line-year-over-year.png 已示範這個情境,但只是個案實作

## Proposal · 規範草案

### 適用情境

- **預測模型輸出**(SEIR、ARIMA、ML 預測)的點估計 + 預測區間
- **抽樣資料的估計**(變異株比例、抗體陽性率、超額死亡估計)的點估計 + 信賴區間
- **與歷史 baseline 比較**(同期 ±1 SD、過去 5 年範圍)的對照帶

### 不適用情境

- **已通報的確定值**(每日確診、死亡、住院人數)── 不要硬加 CI 偽裝有不確定性
- **內部行政指標**(預算執行率、各機關 KPI)── 無統計意義
- **「資料有缺漏」的非統計不確定性** ── 屬於另一條規範(缺值標示,未來另開 RFC)
- **boxplot 與 histogram** ── 本身就是 uncertainty 視覺化,不需再加 CI 帶

### 邊界案例

- **既往資料 + 預測連接**:過去段用實線、預測段切換為虛線(dash);CI 帶**只在預測段顯示**,過去段不畫 CI 帶(因為是已知數)
- **多個 CI 級別**(50% + 95%):用兩層漸層帶,內層(50%)深、外層(95%)淺
- **多條時間序列各帶 CI**:每條序列的 CI 帶用該序列主色的淺版,alpha 0.20-0.25。若帶疊太亂(超過 3 條)→ 改用 small multiples(本身亦待 RFC 規範)
- **歷史 baseline 對照帶**:可用中性灰(NEUTRAL["400"] alpha 0.22),非主色淺版 ── 因為 baseline 是「對比基準」非主角,02c-line-year-over-year.png 已示範

### 規則細節

1. **CI 用漸層填充帶**,**不用上下細線**(避免時序資料視覺擁擠)
2. **帶顏色**:該序列主色的淺色版
   - 主色序列(`#5D7F58` 折線)的帶:`#B4C9B1`(p-300),alpha 0.30
   - 藍色序列(`#587A9D` 折線)的帶:`#B0C2D3` 或同色 alpha 0.25
   - 黃色序列(`#A8821F` 折線)的帶:同色 alpha 0.20
   - 歷史 baseline 對照帶:`#A2ABA0`(NEUTRAL.400)alpha 0.22
3. **多個 CI 級別**:兩層帶,內層(50% CI)alpha 0.40,外層(95% CI)alpha 0.20
4. **點估計線**:仍用 LINE_COLORS 加深版(對白底 WCAG AA 對比 ≥ 4.5:1)
5. **預測 vs 觀測分界**:點估計線在預測段改為虛線(`dashes=[6,3]`),且**用垂直 annotation line** 標示「預測起點」
6. **CI 級別必明確標註**:legend 或 caption 寫「95% CI」「±1 SD」「歷史範圍」等,不留歧義
7. **Y 軸仍從零開始**(這條鐵則不變)
8. **CI 帶不傳達「精確值」**:讀者應理解為「真實值有 X% 機率落在帶內」而非「值就在帶上下界」

### 程式碼範例

```python
# Python · matplotlib
from epidemic_palette import apply_style, LINE_COLORS, PRIMARY_LIGHT, NEUTRAL
import matplotlib.pyplot as plt

apply_style()
fig, ax = plt.subplots(figsize=(9, 4.5))

# 95% CI 漸層帶(主色淺版)
ax.fill_between(weeks, lower_95, upper_95,
                color=PRIMARY_LIGHT, alpha=0.30,
                label="95% CI")

# 50% CI 內層帶(同色更深 alpha)
ax.fill_between(weeks, lower_50, upper_50,
                color=PRIMARY_LIGHT, alpha=0.40,
                label="50% CI")

# 點估計線(加深版主色)
ax.plot(weeks, point_estimate,
        color=LINE_COLORS["primary"], linewidth=2.5,
        label="Rt 估計值")

# 預測起點 annotation
ax.axvline(x=forecast_start, color=NEUTRAL["400"],
           linestyle="--", linewidth=1)
ax.text(forecast_start, ax.get_ylim()[1] * 0.95,
        " 預測起點", color=NEUTRAL["600"], fontsize=9)
```

```javascript
// Chart.js · 填充帶用兩個 datasets(上界 + 下界 + fill)
datasets: [
  { label: '_upper95', data: upper_95, borderColor: 'transparent',
    backgroundColor: 'rgba(180, 201, 177, 0.30)',  // PRIMARY_LIGHT alpha
    fill: '+1', pointRadius: 0 },
  { label: '_lower95', data: lower_95, borderColor: 'transparent',
    backgroundColor: 'transparent', pointRadius: 0 },
  { label: 'Rt 估計', data: pointEst, borderColor: '#5D7F58',
    borderWidth: 2.5, pointRadius: 0, tension: 0.25 }
]
```

## Affected existing rules · 對既有規範的影響盤點

### Patterns(A/B/C/D/E)

- [x] **不創新 Pattern F**;不確定性是 **modifier**,套在既有 Pattern A/B/D 上
  - Pattern A + uncertainty:主色焦點線 + 同色淺版帶
  - Pattern B + uncertainty:多色折線各帶各色淺版帶(限 ≤ 3 條,否則用 small multiples)
  - Pattern D + uncertainty:加深主線 + 該色淺版帶
- [x] Pattern C / E **不直接適用**:C 是強度比較,E 是序數類別,uncertainty 通常不適合疊在這兩種

### 9 種圖表 references

| Reference | 受影響? | 需要更新? |
|---|---|---|
| 01-bar-chart.md | 輕微 | 補一小段:類別比較若需 CI,可用 error bar(垂直細線 + cap),但不主推 |
| **02-line-chart.md** | **主場** | 新增「不確定性帶」段落,參照本 RFC |
| **03-area-chart.md** | **主場** | 區分「資料 area」vs「uncertainty area」,後者用 alpha + 顏色淺版 |
| 04-stacked-chart.md | 不受影響 | ── |
| 05-pie-chart.md | 不適用 | ── |
| 06-scatter-chart.md | 輕微 | 補 error bar 用法 |
| 07-histogram-boxplot.md | 不受影響(boxplot 本身就是 uncertainty 視覺化) | ── |
| 08-pyramid-chart.md | 不受影響 | ── |
| 09-choropleth-map.md | 進階 | 留待後續:用透明度表示估計可信度(本 RFC 暫不涵蓋) |
| 10-monochrome-usage.md | 不直接影響(uncertainty 是 modifier,與配色 pattern 正交) | ── |

### SKILL.md decision tree

- [x] **新增 modifier 分支**:在 chart selection decision tree 結尾加一段
  ```
  資料是否含「估計值 + 區間」?
    └─ 是 → 套用 RFC 2026-06-01 不確定性視覺化規範
            (在既有 Pattern A/B/D 上添加 uncertainty layer)
  ```
- [x] **不修改既有分支**:既有 patterns 的 decision tree 不變

### 新檔案

- 新增 `skill/references/11-uncertainty.md`(status: draft 期間)
- 新增 `skill/assets/examples/_drafts/`:至少 2 張範例 PNG(Rt 預測、超額死亡 baseline 比較)

## Regression check · 對既有範例的回歸驗證

跑既有 19 張範例 PNG + 投影片內 4 張 Chart.js 範例:

| 既有項目 | 狀態 |
|---|---|
| 01a-bar-single-focus.png | keep |
| 01b-bar-daily-with-ma.png | keep |
| 01c-bar-horizontal-ranking.png | keep |
| 02a-line-focus-vs-average.png | keep |
| 02b-line-multi-metric.png | keep |
| **02c-line-year-over-year.png** | **keep**(已示範 uncertainty 概念:歷史範圍 ±1 SD 用 NEUTRAL.400 alpha 0.22,與新規範「baseline 可用中性灰帶」一致) |
| 03a-area-cumulative.png | keep |
| 03b-area-multi-series.png | keep |
| 04a-stacked-100-percent.png | keep |
| 04b-stacked-horizontal.png | keep |
| 04c-grouped-bar.png | keep |
| 05a-pie-standard.png | keep |
| 05b-donut-with-center.png | keep |
| 06a-scatter-correlation.png | keep |
| 06b-bubble-3rd-dimension.png | keep |
| 07a-histogram.png | keep |
| 07b-boxplot.png | keep |
| 08-pyramid.png | keep |
| 09-choropleth-heatmap.png | keep |
| 10a-mono-stacked-severity.png | keep |
| 10b-mono-line-waves.png | keep |
| 10c-mono-area-doses.png | keep |
| 投影片 Slide 10 (直條 + MA) | keep |
| 投影片 Slide 11 (三波折線) | keep |
| 投影片 Slide 12 (堆疊雙模式) | keep |

**統計:**
- `keep`: 25(全部)
- `adjust`: 0
- `waive`: 0
- `break`: 0

✓ **0 break、0 adjust** ── 新規範完全不誤傷既有,只擴充未曾涵蓋的領域。Regression check 漂亮通過。

## Trade-offs · 取捨

- **好處**:
  - 補上疫情報告核心缺口(R/Rt、預測、估計都需要)
  - AI agent 在生成預測圖時有規範可循,跨報告一致
  - 與既有 patterns 互補不衝突
  - 02c-line-year-over-year.png 已隱含此規範精神,正式化此既有作法
- **犧牲**:
  - references 多一個檔(維護成本 +1,但有限,因為是 modifier 規範,內容不會像 chart-type reference 那麼大)
  - AI agent 的觸發判斷需更精準(需偵測資料是否含 CI / 預測區間)
- **為何選漸層填充帶,而非錯誤條(error bars)**:
  - 時序資料 28+ 個點時,error bar 視覺過擁擠
  - 漸層帶是統計學界與資料新聞主流(NYT、FiveThirtyEight、R/ggplot2 慣例)
  - 與本指引「移除不傳達資訊的裝飾」精神一致(帶比一堆細線更乾淨)

## Alternatives considered · 評估過的其他方向

1. **Alt A:錯誤條(error bars 含 cap)**
   - 否決:在密集時序資料下視覺過擁擠;適合「少量類別比較」場景(此用法暫納入 01-bar-chart 補一小段),但不是疫情主場
2. **Alt B:不規範,讓使用者自由發揮**
   - 否決:AI agent 無規範會產出 trailing/error bar/不一致色 mix。本指引精神是「規範化讓品質可控」
3. **Alt C:新建獨立 Pattern F(uncertainty)**
   - 否決:不確定性是 **modifier**(套在既有 Pattern A/B/D 上)而非獨立配色 pattern;新建 Pattern F 會讓 decision tree 多一個沒必要的分支
4. **Alt D:用 violin plot / ridge plot 等進階形式**
   - 否決:這些圖表型本身需要另一份 reference,本 RFC 聚焦時序 + 散佈的標準場景

## Open questions · 未解的問題

1. **多條時間序列(> 3)各帶 CI 的處理**:暫議「改用 small multiples」,但 small multiples 規範本身尚未存在(下一支 RFC 候選)。在 small multiples RFC 完成前,本規範如何處置這個邊界?
2. **「機率分布」視覺化**(例:預測有 30% 機率超過閾值):暫不在本 RFC 範圍,留待後續
3. **error bar 在 01-bar-chart 內的具體規範**(cap style、寬度、顏色):本 RFC 在 01-bar-chart 只補一小段「可用 error bar」,但不訂死細節 ── 是否需要在本 RFC 內把這個也寫死?
4. **進階情境**:choropleth 用透明度表示「估計值的可信度」── 本 RFC 暫不涵蓋,留註記

## Decision · 決策狀態

- [x] **Draft**   ── 已完成草案,進入維護者 review
- [ ] **Pilot**   ── 待 review 確認後進入試行:寫 `skill/references/11-uncertainty.md`(`status: draft`),`SKILL.md` decision tree 暫不更新,範例放 `_drafts/`
- [ ] **Active**  ── Pilot 跑一段時間無問題後升級,走完整 L1→L2→L3
- [ ] **Withdrawn**

---

**Reviewer notes** ── 進 Pilot 前請維護者確認:

1. 「適用 / 不適用 / 邊界」三段範圍 OK 嗎?有沒有 missing 的常見情境?
2. 規則 1-8 中是否有過度具體(導致實作彈性太低)或過度模糊(實作會各自詮釋)的條目?
3. Open question #3(error bar 在 bar chart 內的規範)要在本 RFC 內定,還是另開 RFC?
4. 命名 `11-uncertainty.md`(接 10-monochrome 之後)或改為 `M1-uncertainty-modifier.md`(M = modifier,與 chart-type 區分)?
