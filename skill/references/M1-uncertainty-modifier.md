---
status: active
rfc: 2026-06-01-uncertainty
since: 2026-06-09
promoted: 2026-06-09
---

# M1 · 不確定性視覺化 Modifier

> 對應 RFC:[2026-06-01](../../docs/rfcs/2026-06-01-uncertainty.md)
>
> **本規範為 modifier(修飾性規範)**,套在既有 Pattern A/B/D 上。AI agent 在偵測到資料含「估計值 + 區間」「預測區間」「抽樣 CI」時,應依本規範實作。

## 定位

本規範是 **modifier**(修飾性規範),套在既有 Pattern A/B/D 上,**不創新獨立 pattern**:

- Pattern A + uncertainty:主色焦點線 + 同色淺版漸層帶
- Pattern B + uncertainty:多色折線各帶各色淺版漸層帶(≤ 3 條,否則改 small multiples)
- Pattern D + uncertainty:加深主線 + 該色淺版漸層帶
- Pattern C / E **不直接適用**:C 是強度比較,E 是序數類別,uncertainty 通常不適合疊在這兩種

## 適用情境

- **預測模型輸出**(SEIR / ARIMA / ML 短中期預測)的點估計 + 預測區間
- **抽樣資料的估計**(類流感就診率、抗體陽性率)的點估計 + 信賴區間
- **與歷史 baseline 比較**(同期 ±1 SD、過去 5 年範圍)的對照帶
- **少量類別的點估計比較**(各年齡組重症率、各疫苗保護力)── 用 error bar

## 不適用情境

- **已通報的確定值**(每日確診、死亡、住院人數)── 不可硬加 CI 偽裝有不確定性
- **內部行政指標**(預算執行率、各機關 KPI)── 無統計意義
- **「資料有缺漏」的非統計不確定性** ── 屬於另一條規範(缺值標示,待另開 RFC)
- **boxplot 與 histogram** ── 本身就是 uncertainty 視覺化,不需再加 CI 帶

## 邊界案例

- **既往資料 + 預測連接**:過去段用實線、預測段切換為虛線(`dashes=[6,3]`);CI 帶**只在預測段顯示**,過去段不畫 CI 帶(因為是已知數)
- **多個 CI 級別**(50% + 95%):用兩層漸層帶,內層(50%)alpha 0.40、外層(95%)alpha 0.20
- **多條時間序列各帶 CI**:每條序列的 CI 帶用該序列主色的淺版,alpha 0.20-0.25。若帶疊太亂(> 3 條)→ 改用 small multiples,**詳見 `M2-small-multiples.md` 規則 11(M1 / M2 兼容)** ── 每 panel 一條 + 該條的 CI 帶,共用圖例只標一次「95% CI」
- **歷史 baseline 對照帶**:可用 `NEUTRAL["400"]` alpha 0.22,非主色淺版 ── 因為 baseline 是「對比基準」非主角

---

## 規則 ── 漸層填充帶(時序、預測主場)

**1. CI 用漸層填充帶,不用上下細線**(避免時序資料視覺擁擠)

**2. 帶顏色:該序列主色的淺色版**
- 主色序列(`#5D7F58` 折線)的帶:`#B4C9B1`(p-300),alpha 0.30
- 藍色序列(`#587A9D` 折線)的帶:同色 alpha 0.25
- 黃色序列(`#A8821F` 折線)的帶:同色 alpha 0.20
- 歷史 baseline 對照帶:`#A2ABA0`(NEUTRAL.400)alpha 0.22

**3. 多個 CI 級別**:兩層帶,內層(50% CI)alpha 0.40,外層(95% CI)alpha 0.20

**4. 點估計線**:仍用 LINE_COLORS 加深版(對白底 WCAG AA 對比 ≥ 4.5:1)

**5. 預測 vs 觀測分界**:點估計線在預測段改為虛線(`dashes=[6,3]`),並用垂直 annotation line 標示「預測起點」

**6. CI 級別必明確標註**:legend 或 caption 寫「95% CI」「±1 SD」「歷史範圍」等,不留歧義

**7. Y 軸**:遵循 SKILL.md §4.4 既有規範
- 直條圖:Y 軸必從零(這條鐵則不變)
- 折線 / 區域:zero baseline preferred but optional。**Rt、再生數、相對風險等「值在特定區間變動」的估計,從零反而難看清變化,可從合理 lower bound 起算(但 caption 須註明)**

**8. CI 帶不傳達「精確值」**:讀者應理解為「真實值有 X% 機率落在帶內」,而非「值就在帶上下界」

## 規則 ── Error bar(少量類別 + 點估計)

**9. 適用 error bar 的情境**:類別 < 6 個、各類別有點估計 + 區間(例:各年齡組重症率 7 組以下、各疫苗保護力 3-5 種)

**10. 不適用 error bar 的情境**:時序資料(28+ 點)── 視覺過擁擠,改用規則 1-6 的漸層帶

**11. Error bar 顏色:用 `PRIMARY_DARKER`(`#374C34`)**,多色情境用該系列主色的更深版。
> ⚠️ **不要用中性灰** ── 視覺對照確認(RFC v3 #R5):中性灰與 bar 主色區分不夠明顯,反而造成視覺干擾。深綠版視覺辨識度高且仍隸屬主色系統

**12. Error bar 尺寸:視覺明確標示區間端點即可,不過分搶眼,不訂死絕對數字**
- 垂直線寬:1.5 px(matplotlib `elinewidth=1.5`)
- cap:matplotlib 建議 `capsize=4`;Chart.js / D3 / R 等視 chart 整體尺寸調整
- 共通原則:cap 視覺上 **不超過 bar width 50%、不小於 20%**

**13. Error bar 對稱性 ── 規範強制**:對數空間估計(RR、OR、HR 等)的 CI 本來就不對稱,**不可硬畫成對稱**
- 強制對稱會嚴重誤導:例 RR=2.5, 95% CI [1.4, 4.5] ── 真實下限 1.4 不跨過 1(顯著);若強制對稱,下限會被計算成 0.95 跨過 1(看起來非顯著),結論完全相反
- matplotlib `errorbar(yerr=[lower_dist, upper_dist])` 分別傳上下臂
- 任何時候只要 lower CI ≠ upper CI,都不可用單值 yerr 強制對稱

---

## 程式碼範例

### 範例 A · 時序預測(漸層帶)

```python
from epidemic_palette import (
    apply_style, LINE_COLORS, PRIMARY_LIGHT, NEUTRAL,
)
import matplotlib.pyplot as plt
import numpy as np

apply_style()
fig, ax = plt.subplots(figsize=(9, 4.5))

# 觀測段:實線(無 CI)
ax.plot(weeks_past, obs, color=LINE_COLORS["primary"],
        linewidth=2.5, label="觀測值")

# 預測段:95% CI 外層 + 50% CI 內層
ax.fill_between(weeks_future, lower_95, upper_95,
                color=PRIMARY_LIGHT, alpha=0.20, label="95% CI")
ax.fill_between(weeks_future, lower_50, upper_50,
                color=PRIMARY_LIGHT, alpha=0.40, label="50% CI")

# 預測點估計:虛線
ax.plot(weeks_future, point_est,
        color=LINE_COLORS["primary"], linewidth=2.5,
        linestyle=(0, (6, 3)), label="預測點估計")

# 預測起點 annotation
ax.axvline(x=forecast_start, color=NEUTRAL["400"],
           linestyle="--", linewidth=1)
ax.text(forecast_start, ax.get_ylim()[1] * 0.95, " 預測起點",
        color=NEUTRAL["600"], fontsize=9)
```

### 範例 B · 少量類別(error bar,不對稱 CI)

```python
from epidemic_palette import apply_style, PRIMARY, PRIMARY_DARKER

apply_style()
fig, ax = plt.subplots(figsize=(7, 4))

ages = ["0-9", "10-39", "40-64", "65-74", "75+"]
rates = [0.5, 1.2, 3.8, 8.4, 15.2]
ci_low = [0.3, 0.9, 3.2, 7.2, 13.4]
ci_high = [0.8, 1.6, 4.5, 9.7, 17.3]

# 規則 13:不對稱 CI ── 上下臂分別計算,不可強制對稱
errors = [
    [r - l for r, l in zip(rates, ci_low)],   # lower 距離
    [h - r for h, r in zip(ci_high, rates)],  # upper 距離
]

ax.bar(ages, rates, color=PRIMARY, width=0.6)
ax.errorbar(ages, rates, yerr=errors, fmt="none",
            ecolor=PRIMARY_DARKER,  # 規則 11
            elinewidth=1.5, capsize=4, capthick=1)
ax.set_ylabel("重症率(%, 95% CI)")
```

### 範例 C · Chart.js(漸層帶)

```javascript
// 漸層帶用兩個 datasets(上界 + 下界 + fill: '+1')
datasets: [
  { label: '_upper95', data: upper_95,
    borderColor: 'transparent',
    backgroundColor: 'rgba(180, 201, 177, 0.30)',  // PRIMARY_LIGHT alpha
    fill: '+1', pointRadius: 0 },
  { label: '_lower95', data: lower_95,
    borderColor: 'transparent',
    backgroundColor: 'transparent', pointRadius: 0 },
  { label: '點估計', data: pointEst,
    borderColor: '#5D7F58', borderWidth: 2.5,
    pointRadius: 0, tension: 0.25,
    borderDash: [6, 3]  // 預測段虛線
  }
]
```

---

## 常見錯誤

| ✗ 錯誤 | ✓ 正確 |
|---|---|
| 用單一值 yerr 強制對稱 CI | 上下臂分別計算 `yerr=[lower_dist, upper_dist]` |
| Error bar 用中性灰看不清 | 用 `PRIMARY_DARKER` 視覺辨識度高 |
| 時序資料疊 error bar | 改用漸層填充帶 |
| 觀測段加 CI 帶 | CI 帶只在預測段顯示 |
| 預測與觀測同樣實線 | 預測段改虛線 `dashes=[6,3]` |
| Y 軸從零(Rt 從 0 到 2.5) | Rt 等估計值可從合理 lower bound 起算,但 caption 註明 |
| 漸層帶用主色填,看起來像「資料 area」 | 用該主色的淺版(`PRIMARY_LIGHT`)+ alpha,清楚區分「資料」vs「不確定性」 |

---

## 範例圖

預生成範例圖位於 `skill/assets/examples/`:

- `m1a-uncertainty-trailing-band.png` — 時序預測(類流感就診人次 + 4 週預測區間,50% / 95% 兩層帶)
- `m1b-uncertainty-errorbar-asymmetric.png` — 各年齡組重症率(error bar + 不對稱 95% CI)

生成函式:`skill/scripts/generate_examples.py` 內的 `uncertainty_modifier_examples()`
