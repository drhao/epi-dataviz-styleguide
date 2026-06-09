# RFC 2026-06-01: 不確定性視覺化

- **作者**: Dr. Hao
- **提案日期**: 2026-06-09
- **狀態**: **Active**(2026-06-09 採納)
- **目標版本**: v1.1(待 Pilot 試行後決定)

## Context · 為什麼需要這個規範

疫情報告幾乎必然涉及不確定性:類流感就診人次預測、重症病例數預測、Rt 估計、抗體陽性率調查等都帶有統計上下界。但本指引目前完全沒規範這類視覺呈現 ── 結果是:

- AI agent 生成預測圖時各自為政:有的用 error bar、有的用 alpha 帶、有的乾脆畫成兩條虛線
- 既有 references 已隱含 uncertainty 概念(`02c-line-year-over-year.png` 用「歷史範圍 ±1 SD」對照帶)但只是個案,沒上升為規範
- 不同分析師會用不同方式呈現 CI,降低跨報告比較性

### Real use cases

1. **每週 Rt 估計**:中央流行疫情指揮中心發布每週 Rt 點估計與 95% CI 帶。讀者最常追蹤「Rt 是否跨過 1.0 警戒線」,因此 CI 是否覆蓋 1.0 是關鍵訊息。**Rt 值通常落在 0.5-2 區間,Y 軸從零開始反而無法看清變化**
2. **類流感就診人次預測**:NHIS 監測資料 + 短中期預測,每週發布過去觀測 + 未來 4 週預測區間。讀者需要區分「已通報的確定值」與「預測的估計值」
3. **重症病例數預測**:預測中重度與死亡的醫療資源負荷,通常 SEIR / ARIMA 等模型輸出點估計 + 預測區間。CI 在政策決策上是關鍵(例如「ICU 床數是否會超過容量上限」)

## Proposal · 規範草案

### 適用情境

- **預測模型輸出**(SEIR、ARIMA、ML 短中期預測)的點估計 + 預測區間
- **抽樣資料的估計**(類流感就診率、抗體陽性率)的點估計 + 信賴區間
- **與歷史 baseline 比較**(同期 ±1 SD、過去 5 年範圍)的對照帶
- **少量類別的點估計比較**(例如各年齡組重症率,各自有 95% CI)── 使用 error bar(規則 8)

### 不適用情境

- **已通報的確定值**(每日確診、死亡、住院人數)── 不要硬加 CI 偽裝有不確定性
- **內部行政指標**(預算執行率、各機關 KPI)── 無統計意義
- **「資料有缺漏」的非統計不確定性** ── 屬於另一條規範(缺值標示,未來另開 RFC)
- **boxplot 與 histogram** ── 本身就是 uncertainty 視覺化,不需再加 CI 帶

### 邊界案例

- **既往資料 + 預測連接**:過去段用實線、預測段切換為虛線(dash);CI 帶**只在預測段顯示**,過去段不畫 CI 帶(因為是已知數)
- **多個 CI 級別**(50% + 95%):用兩層漸層帶,內層(50%)深、外層(95%)淺
- **多條時間序列各帶 CI**:每條序列的 CI 帶用該序列主色的淺版,alpha 0.20-0.25。若帶疊太亂(超過 3 條)→ 改用 small multiples(尚待 RFC 規範)
- **歷史 baseline 對照帶**:可用中性灰(NEUTRAL["400"] alpha 0.22),非主色淺版 ── 因為 baseline 是「對比基準」非主角,02c-line-year-over-year.png 已示範

### 規則細節 ── 漸層填充帶(時序、預測主場)

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
7. **Y 軸**:**遵循既有規範**(SKILL.md §4.4)
   - 直條圖:Y 軸必從零(這條鐵則不變)
   - 折線 / 區域:zero baseline preferred but optional 若變化才是訊息(annotate the choice)。**Rt、再生數、相對風險等「值在特定區間變動」的估計**,從零反而難看清變化,可從合理 lower bound 起算(但 caption 須註明)
8. **CI 帶不傳達「精確值」**:讀者應理解為「真實值有 X% 機率落在帶內」而非「值就在帶上下界」

### 規則細節 ── Error bar(少量類別 + 點估計)

9. **適用 error bar 的情境**:類別 < 6 個、各類別有點估計 + 區間。例如各年齡組的重症率(7 組以下)、各疫苗的保護力(3-5 種)
10. **不適用 error bar 的情境**:時序資料(28+ 點)── 視覺過擁擠,改用規則 1-6 的漸層帶
11. **Error bar 顏色**:cap 與垂直線用 **`PRIMARY_DARKER`**(`#374C34`)── 或多色情境下用該系列主色的更深版。**不用中性灰**:中性灰雖然安靜不搶主色,但與 bar 主色區分不夠明顯,反而視覺干擾(v3 視覺對照後決定)
12. **Error bar 尺寸**:視覺上明確標示區間端點即可,**不過分搶眼,但不訂死絕對數字**
    - 垂直線寬:1.5 px(matplotlib `elinewidth=1.5`)
    - cap:matplotlib 建議 `capsize=4`;Chart.js / D3 / R 等視 chart 整體尺寸與 DPI 調整
    - 共通原則:cap 視覺上**不超過 bar width 50%、不小於 20%**(避免太搶眼或幾乎看不到)
13. **Error bar 對稱性 ── 規範強制(Pilot 階段即 enforce)**:對數空間估計(RR、OR、HR 等)的 CI 本來就不對稱,**不可硬畫成對稱**
    - 強制對稱會嚴重誤導:例 RR=2.5, 95% CI [1.4, 4.5] ── 真實下限 1.4 不跨過 1(顯著);若強制對稱,下限會被計算成 0.95 跨過 1(看起來非顯著),**結論完全相反**
    - matplotlib `errorbar(yerr=[lower_dist, upper_dist])` 分別傳上下臂
    - 任何時候只要 lower CI ≠ upper CI,都不可用單值 yerr 強制對稱

### 程式碼範例

```python
# 範例 A · 時序預測:漸層帶
from epidemic_palette import apply_style, LINE_COLORS, PRIMARY_LIGHT, NEUTRAL
import matplotlib.pyplot as plt

apply_style()
fig, ax = plt.subplots(figsize=(9, 4.5))

# 觀測段:實線(無 CI)
ax.plot(weeks_past, obs, color=LINE_COLORS["primary"], linewidth=2.5)

# 預測段:CI 帶 + 虛線
ax.fill_between(weeks_future, lower_95, upper_95,
                color=PRIMARY_LIGHT, alpha=0.30, label="95% CI")
ax.fill_between(weeks_future, lower_50, upper_50,
                color=PRIMARY_LIGHT, alpha=0.40, label="50% CI")
ax.plot(weeks_future, point_est,
        color=LINE_COLORS["primary"], linewidth=2.5,
        linestyle=(0, (6, 3)), label="點估計(預測)")

# 預測起點 annotation
ax.axvline(x=forecast_start, color=NEUTRAL["400"],
           linestyle="--", linewidth=1)
ax.text(forecast_start, ax.get_ylim()[1] * 0.95,
        " 預測起點", color=NEUTRAL["600"], fontsize=9)
```

```python
# 範例 B · 少量類別:error bar
from epidemic_palette import apply_style, PRIMARY, PRIMARY_DARKER

apply_style()
fig, ax = plt.subplots(figsize=(7, 4))

ages = ["0-9", "10-39", "40-64", "65-74", "75+"]
rates = [0.5, 1.2, 3.8, 8.4, 15.2]      # 重症率 %
ci_low = [0.3, 0.9, 3.2, 7.2, 13.4]
ci_high = [0.8, 1.6, 4.5, 9.7, 17.3]

# 規則 13:CI 不對稱 ── 上下臂分別計算,不可強制對稱
errors = [
    [r - l for r, l in zip(rates, ci_low)],   # lower 距離
    [h - r for h, r in zip(ci_high, rates)],  # upper 距離
]

ax.bar(ages, rates, color=PRIMARY, width=0.6)
ax.errorbar(ages, rates, yerr=errors,
            fmt="none", ecolor=PRIMARY_DARKER,   # 規則 11:主色更深版
            elinewidth=1.5, capsize=4, capthick=1)
ax.set_ylabel("重症率(%, 95% CI)")
```

```javascript
// Chart.js · 漸層帶用兩個 datasets(上界 + 下界 + fill)
datasets: [
  { label: '_upper95', data: upper_95, borderColor: 'transparent',
    backgroundColor: 'rgba(180, 201, 177, 0.30)',  // PRIMARY_LIGHT alpha
    fill: '+1', pointRadius: 0 },
  { label: '_lower95', data: lower_95, borderColor: 'transparent',
    backgroundColor: 'transparent', pointRadius: 0 },
  { label: '點估計', data: pointEst, borderColor: '#5D7F58',
    borderWidth: 2.5, pointRadius: 0, tension: 0.25,
    borderDash: [6, 3]  // 預測段虛線
  }
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
| 01-bar-chart.md | error bar 主場 | **不需修改** ── error bar 用法整合進本 RFC 規則 9-13(避免規範散落多處) |
| **02-line-chart.md** | 漸層帶主場 | 在「相關資源」段加 cross-link 指向 M1-uncertainty-modifier.md |
| **03-area-chart.md** | 漸層帶主場 | 同上 cross-link;補一句說明「資料 area」vs「uncertainty area」的視覺區分 |
| 04-stacked-chart.md | 不受影響 | ── |
| 05-pie-chart.md | 不適用 | ── |
| 06-scatter-chart.md | error bar 適用 | **不需修改** ── 同 01,cross-link 指向本 RFC 規則 9-13 |
| 07-histogram-boxplot.md | 不受影響(boxplot 本身就是 uncertainty 視覺化) | ── |
| 08-pyramid-chart.md | 不受影響 | ── |
| 09-choropleth-map.md | 進階 | 留待後續:用透明度表示估計可信度(本 RFC 暫不涵蓋) |
| 10-monochrome-usage.md | 不直接影響(uncertainty 是 modifier,與配色 pattern 正交) | ── |

### SKILL.md decision tree

- [x] **新增 modifier 分支**:在 chart selection decision tree 結尾加一段
  ```
  資料是否含「估計值 + 區間 / 預測區間」?
    └─ 是 → 套用 RFC 2026-06-01(M1-uncertainty-modifier)
            在既有 Pattern A/B/D 上添加 uncertainty layer
  ```
- [x] **不修改既有分支**:既有 patterns 的 decision tree 不變

### 新檔案

- 新增 `skill/references/M1-uncertainty-modifier.md`(status: draft 期間)
  - 命名 `M1-` 表示 modifier,與既有 chart-type references(`01-` 到 `10-`)區分
- 新增 `skill/assets/examples/_drafts/`:至少 2 張範例 PNG(Rt 預測、各年齡組重症率 error bar)

## Regression check · 對既有範例的回歸驗證

跑既有 19 張範例 PNG + 投影片內 4 張 Chart.js 範例 + 樣板:

| 既有項目 | 狀態 |
|---|---|
| 01a-bar-single-focus.png | keep |
| 01b-bar-daily-with-ma.png | keep |
| 01c-bar-horizontal-ranking.png | keep |
| 02a-line-focus-vs-average.png | keep |
| 02b-line-multi-metric.png | keep |
| **02c-line-year-over-year.png** | **keep**(已示範:歷史範圍 ±1 SD 用 NEUTRAL.400 alpha 0.22,與新規範「baseline 可用中性灰帶」一致) |
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
| Office 樣板 6 個檔 | keep |

**統計:**
- `keep`: 31(全部)
- `adjust`: 0
- `waive`: 0
- `break`: 0

✓ **0 break、0 adjust** ── 新規範完全不誤傷既有,只擴充未曾涵蓋的領域。Regression check 漂亮通過。

## Trade-offs · 取捨

- **好處**:
  - 補上疫情報告核心缺口(Rt、類流感預測、重症預測都需要)
  - AI agent 在生成預測圖時有規範可循,跨報告一致
  - 與既有 patterns 互補不衝突
  - error bar 與漸層帶兩種情境一份文件涵蓋,讀者不用跨檔
  - 02c-line-year-over-year.png 已隱含此規範精神,正式化此既有作法
- **犧牲**:
  - references 多一個檔(維護成本 +1,但有限,因為是 modifier 規範,內容不會像 chart-type reference 那麼大)
  - AI agent 的觸發判斷需更精準(需偵測資料是否含 CI / 預測區間)
- **為何選漸層填充帶(時序)+ error bar(少量類別)的混合策略**:
  - 時序 28+ 點:error bar 視覺過擁擠 → 帶
  - 少量類別 < 6:帶反而抽象(沒「時間軸」概念),error bar 更直觀傳達區間
  - 兩種情境互補,讀者依資料形態自然選

## Alternatives considered · 評估過的其他方向

1. **Alt A:全用錯誤條(error bars)**
   - 否決:在密集時序資料下視覺過擁擠;不適合疫情主場(時序預測)
2. **Alt B:全用漸層帶,不規範 error bar**
   - 否決:少量類別場景(各年齡組重症率)的 error bar 是業界主流,本指引應涵蓋
3. **Alt C:不規範,讓使用者自由發揮**
   - 否決:AI agent 無規範會產出 trailing/error bar/不一致色 mix。本指引精神是「規範化讓品質可控」
4. **Alt D:新建獨立 Pattern F(uncertainty)**
   - 否決:不確定性是 **modifier**(套在既有 Pattern A/B/D 上)而非獨立配色 pattern;新建 Pattern F 會讓 decision tree 多一個沒必要的分支
5. **Alt E:用 violin plot / ridge plot 等進階形式**
   - 否決:這些圖表型本身需要另一份 reference,本 RFC 聚焦時序 + 少量類別的標準場景
6. **Alt F:分兩個 RFC(漸層帶 + error bar 各一)**
   - 否決:讀者需跨檔讀才掌握「不確定性如何呈現」完整 picture。整合進本 RFC 較好

## Open questions · 未解的問題

1. **多條時間序列(> 3)各帶 CI 的處理**:暫議「改用 small multiples」,但 small multiples 規範本身尚未存在(下一支 RFC 候選)。在 small multiples RFC 完成前,本規範如何處置這個邊界?
2. **「機率分布」視覺化**(例:預測有 30% 機率超過閾值):暫不在本 RFC 範圍,留待後續
3. **進階情境**:choropleth 用透明度表示「估計值的可信度」── 本 RFC 暫不涵蓋,留註記

## Decision · 決策狀態

- [x] **Draft**   ── 草案 v3 完成(v1 + v2 + v3 reviewer feedback 皆已 incorporate)
- [x] **Pilot**   ── 2026-06-09 進入試行(同日完成 Promote,因為 framework 試走順利、無實作疑慮)
- [x] **Active**  ── **2026-06-09 採納**
  - `skill/references/M1-uncertainty-modifier.md` frontmatter `status: active`,移除 Pilot 警示框
  - `skill/SKILL.md`:Quick Decision Tree step 5 新增 uncertainty modifier;§4.6 新增完整章節;Reference Files 表新增 M1 條目
  - 既有 references cross-link:`02-line-chart.md` / `03-area-chart.md`(漸層帶主場)+ `01-bar-chart.md` / `06-scatter-chart.md`(error bar)各加「相關規範」段
  - `skill/scripts/generate_examples.py` 新增 `uncertainty_modifier_examples()`,輸出 `m1a-uncertainty-trailing-band.png`、`m1b-uncertainty-errorbar-asymmetric.png` 至主目錄
  - `skill/assets/examples/_drafts/` 清空 m1 腳本,README 改為「目前無 Pilot」狀態
  - `dev-tools/check_drift.py`:新增「不確定性視覺化 modifier(M1)」CHECK
  - `docs/guideline.{md,html}` 各加章節介紹(指向 reference)
  - `CHANGELOG.md` 新增採納紀錄
- [ ] **Active**  ── Pilot 跑一段時間無問題後升級,走完整 L1→L2→L3
- [ ] **Withdrawn**

---

## Pilot feedback

Pilot 期間(2026-06-09 同日)無實作疑慮、無 framework 反饋。三個 reviewer 視覺對照已在 Draft v3 階段定稿(規則 11/12/13),無新疑慮浮現,直接走 Promote。

未來若有實際使用回饋,在此段累加紀錄。

## Reviewer notes ── 所有問題已 resolved

### v1 resolved
- ✓ **#R1 適用 / 不適用 / 邊界範圍**:涵蓋 OK,僅 use cases 修正(類流感、重症病例數預測)
- ✓ **#R2 規則具體度**:認可,僅規則 7(Y 軸)需與既有「直條必從零、其他視情境」對齊
- ✓ **#R3 error bar 整合**:整合進本 RFC 規則 9-13(避免規範散落)
- ✓ **#R4 命名**:`M1-uncertainty-modifier.md`(M = modifier,與 chart-type 01-10 區分)

### v3 resolved(視覺對照後決定)

對應的視覺對照圖已在 review 過程中生成、決策定稿:

- ✓ **#R5 規則 11 顏色**:選 **PRIMARY_DARKER (`#374C34`)**。中性灰雖較安靜,但與 bar 主色區分不夠明顯反而視覺干擾。深綠版讓 error bar 視覺辨識度高且仍隸屬主色系統
- ✓ **#R6 規則 12 尺寸**:**不訂死絕對數字**。matplotlib 建議 `capsize=4` + 共通原則「cap 視覺上不超過 bar width 50%、不小於 20%」。理由:不同工具(Chart.js / D3 / R)的 cap 單位不一,寫死數字會不通用
- ✓ **#R7 規則 13 不對稱 CI**:**Pilot 階段即 enforce**(非 best practice 軟性建議)。視覺對照顯示強制對稱會讓 RR=2.5 的下限從 1.4 變 0.95,結論從顯著反轉為非顯著 ── 嚴重誤導

---

## 關聯議題:既有「Y 軸從零」描述精細化(不在本 RFC 範圍,獨立處理)

撰寫本 RFC 時發現既有規範文件對「Y 軸從零」描述不一致:

- `SKILL.md §4.4` 與 `references/01-bar-chart.md` 寫對(區分 bar vs line)
- 但 `AGENTS.md`、`README.md`、`docs/guideline-slides-summary.html`、`docs/prompt-examples.md`、`docs/guideline.md` 等多處寫得過度絕對(「Y 軸必從零」沒區分圖型)

此精細化屬於「既有規範文字修訂」,走 CONTRIBUTING L2/L3 跨層同步,**不需 RFC**。本 RFC 採納後另開 commit 處理。
