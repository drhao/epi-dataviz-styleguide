# RFC 2026-06-02: Small Multiples 版面 modifier

- **作者**: Dr. Hao
- **提案日期**: 2026-06-09
- **狀態**: Draft v1
- **目標版本**: v1.2(待 review 確認)
- **關聯 RFC**: [2026-06-01 不確定性視覺化](./2026-06-01-uncertainty.md)(M1 留下了 small multiples 接口)

## Context · 為什麼需要這個規範

實務上會碰到「同一指標 × 多分類維度」的場景:22 縣市並排、各年齡組並排、跨年度同期比較等。目前本指引完全沒規範這類**多 panel 版面**,結果是:

- AI agent 生成多 panel 圖時各自為政:Y 軸 scale 不統一、Grid 排版亂、Panel 標題位置不一致、共用圖例擺哪沒共識
- 既有 02c-line-year-over-year.png 用「兩條線疊一張 + 透明範圍帶」處理跨年比較,**但年份多到 5 個以上時就難讀**,目前指引沒給 fallback 路徑
- M1 規則明確留下接口:「多條時間序列(> 3)各帶 CI 的處理:暫議『改用 small multiples』,但 small multiples 規範本身尚未存在」── 本 RFC 補完這個缺口

### Real use cases

1. **22 縣市同指標並排**(地理維度):4×6 或 5×5 grid,每縣市一 panel,看各縣市波形差異
2. **各年齡組曲線**(人口分組維度):8-9 panels(0-9, 10-19, ..., 70+),看年齡層在某波疫情的形態
3. **跨年度同期比較**(時間維度):例 2021-2025 每年一 panel,以週次對齊比較波形 ── 既有 02c 是 2 序列疊一張,本 RFC 處理「3+ 年份」場景
4. **變異株各自時序**(疾病維度):每株一 panel,觀察各株上升與消退節奏
5. **M1 fallback**:多條折線各帶 CI 疊太亂(> 3 條序列),拆 small multiples 每 panel 一條 + 其 CI 帶

## Proposal · 規範草案

### 適用情境

- 多 panels(2-25)同一指標、不同分類維度
- 觀察各別 panel 的形狀(而非「跨類別比例」── 後者用堆疊圖)
- M1 的 multi-series CI fallback(> 3 條 CI 帶)

### 不適用情境

- **只有 2-3 個 panel** ── 直接放同一張圖比較,small multiples 反而浪費版面
- **各 panel 的 X / Y 範圍差異極大且無法標準化** ── 例:絕對人次 vs 千人比率,各縣市相差 10 倍以上,改用「每 10 萬人發生率」標準化後才能 small multiples
- **強調「整體 vs 子集」對比** ── 用 Pattern A 焦點圖,不要拆 panel
- **跨類別組成比例**(各變異株月份占比) ── 用堆疊圖,不要 small multiples

### 邊界案例

- **Panel > 25**:強制建議重新分組(例:22 縣市 → 6 區域)或排序篩選前 N
- **Panel 數量為「不規則」(非完美 grid)**:例 5 panel,layout 用 2+3(2 行,第 1 行 2 個第 2 行 3 個) 或 3+2;靠右下方空缺處放圖例或註解
- **Panel 帶 CI**(銜接 M1):每 panel 內套用 M1 規則(漸層帶或 error bar),不重複規範
- **某個 panel 是焦點**(例:本機關所在地):該 panel 用主色,其餘 panel 用 NEUTRAL.500 ── Pattern A + small multiples 兼容
- **各 panel 資料量不均**(某縣市 N < 30):仍要呈現,在 panel 內標註 `N < 30 樣本不足` warning,不可 cherry-pick 移除

### 規則細節

**1. 統一 Y 軸 scale(rule of comparability)**:所有 panel 同 Y 軸範圍,讀者掃視時直接比較波形高度。例外:**各 panel 的 magnitude 差太大且不能標準化**(例:絕對人次,人口從 5 萬到 500 萬縣市),可用「相對 scale」(每 10 萬人發生率)轉換後統一 ── 仍 enforce 統一,但是統一在標準化後的 scale

**2. 統一 X 軸範圍與 ticks**:所有 panel 同 X 範圍與標籤位置,即使某 panel 該段沒資料也保留空白

**3. 共用圖例**:放整體**上方或下方**,不在每 panel 重複。Grid 不規則時可放空缺處

**4. 共用 X / Y 軸標題**:放整體**左外(Y)**與**下外(X)**,不在每 panel 重複

**5. Panel 標題位置**:**左上**(matplotlib `ax.set_title(..., loc="left")` 慣例),字級小於主標題 2 級,顏色 `NEUTRAL.700`(`#444C43`)

**6. Panel 數量建議**:
| Panel 數 N | 推薦 grid | 備註 |
|---|---|---|
| 2-3 | **不適用** small multiples | 直接同圖比較 |
| 4-6 | 2×3 或 3×2 | |
| 7-9 | 3×3 | |
| 10-12 | 3×4 或 4×3 | |
| 13-16 | 4×4 | |
| 17-22 | 4×6 或 5×5(留空缺) | 22 縣市典型 |
| > 25 | **強制建議重新分組** | 6 區域、年齡 0-19/20-59/60+ 等 |

**7. 焦點 panel 機制**(Pattern A 兼容):某個 panel 是焦點(本機關 / 重點縣市 / 本年度)── 該 panel 用主色 `#739A6D`,其餘 panel 用 `NEUTRAL.500`(`#7A8778`)。焦點 panel 的標題也用主色強調

**8. Panel 邊框**:輕邊框 `NEUTRAL.200`(`#E4E7E4`)1px 區隔每 panel,不用厚框、不用深色;頂右框沿用既有規範可移除(panel 內仍保留底軸與左軸)

**9. Panel 間距**:matplotlib `plt.tight_layout()` 預設足夠;若需手動 `wspace=0.25, hspace=0.35`(數字可調整,共通原則「panel 之間有清楚 gap 但不浪費版面」)

**10. Annotation 與標籤策略**:大量 panel 場景下,每 panel 內標籤過多會雜亂。優先順序:
- 必留:panel 標題(分類維度,如「臺北市」、「2024」)
- 留:Y 軸數值刻度(統一後)
- 視情境保留:X 軸標籤(若 grid 行內 panel 多於 4 個,僅最下方一行標)
- 移除:每 panel 重複圖例、每 panel 重複 X/Y 軸標題

**11. 與 M1 uncertainty 兼容**:每 panel 內可套用 M1 規則 1-13。多 panel 場景下 CI 帶不需在每 panel 都標 legend「95% CI」── 共用圖例已標一次即可

**12. 與 Pattern A/B/C/D/E 兼容**:
- Pattern A + small multiples:**焦點 panel 主色 + 其餘 NEUTRAL.500**(規則 7)
- Pattern B + small multiples:不太合理 ── 既然分 panel 看波形,類別配色用在 panel 內單線(只有一線)沒意義
- Pattern E + small multiples:可能(序數類別當 panel 維度,例:輕/中/重症 panel 並排),用 MONOCHROME.scale_3 為 panel 邊框或標題色

### 程式碼範例

```python
# 範例 A · matplotlib subplots(22 縣市)
from epidemic_palette import apply_style, PRIMARY, NEUTRAL, LINE_COLORS
import matplotlib.pyplot as plt

apply_style()
fig, axes = plt.subplots(4, 6, figsize=(15, 9),
                          sharex=True, sharey=True)  # 統一 X/Y(規則 1+2)

cities = [...]  # 22 縣市資料 dict
focus_city = "臺北市"

for ax, (city, data) in zip(axes.flat, cities):
    is_focus = (city == focus_city)
    color = PRIMARY if is_focus else NEUTRAL["500"]  # 規則 7
    ax.plot(data["week"], data["rate"],
            color=color, linewidth=2.0 if is_focus else 1.5)
    ax.set_title(city, loc="left",                    # 規則 5
                 color=PRIMARY if is_focus else NEUTRAL["700"],
                 fontsize=11)
    for s in ["top", "right"]:                       # 規則 8
        ax.spines[s].set_visible(False)

# 共用標題與軸(規則 3+4)
fig.suptitle("各縣市每週確診率(每 10 萬人)", x=0.1, ha="left")
fig.supxlabel("Week", x=0.5)
fig.supylabel("發生率")
fig.text(0.5, 0.02, "焦點:臺北市", ha="center",
         color=PRIMARY, fontsize=10)  # 焦點說明在外圍

# 隱藏多餘 panel(22 縣市 < 24 = 4×6,後 2 格空缺)
for ax in axes.flat[22:]:
    ax.set_visible(False)

plt.tight_layout()
```

```python
# 範例 B · 焦點 panel + uncertainty(Pattern A + M1 兼容)
# 跨年度同期比較,2024 為焦點 + 預測區間
fig, axes = plt.subplots(2, 3, figsize=(13, 6),
                          sharex=True, sharey=True)

years_data = {
    "2021": {...}, "2022": {...}, "2023": {...},
    "2024": {...}, "2025": {...},  # 2025 是預測,有 CI
}

for ax, (year, data) in zip(axes.flat, years_data.items()):
    is_current = (year == "2025")
    color = PRIMARY_DARKER if is_current else NEUTRAL["500"]
    if is_current and "ci_low" in data:  # M1 規則:預測段 CI 帶
        ax.fill_between(data["week"], data["ci_low"], data["ci_high"],
                        color=PRIMARY_LIGHT, alpha=0.30)
    ax.plot(data["week"], data["rate"], color=color,
            linewidth=2.5 if is_current else 1.5,
            linestyle="--" if is_current else "-")  # M1 規則:預測虛線
    ax.set_title(year, loc="left",
                 color=PRIMARY if is_current else NEUTRAL["700"])
```

### 與 既有 references 的關係

| Reference | 受影響? | 需要更新? |
|---|---|---|
| `02-line-chart.md` | M2 的主要 host | 「相關規範」段加 cross-link(多 panel 場景套 M2) |
| `03-area-chart.md` | 同上 | 同上 |
| `01-bar-chart.md` | 多縣市排名場景可能用 | 「相關規範」段加 cross-link |
| `M1-uncertainty-modifier.md` | M2 是 M1 的 fallback 路徑 | M1 規則 1 邊界案例段補一句「> 3 序列改 small multiples → 參 M2」 |

## Affected existing rules · 對既有規範的影響盤點

### Patterns(A/B/C/D/E)

- [x] **不創新獨立 pattern**;small multiples 是 **layout modifier**(類似 M1 是 uncertainty modifier)
- [x] Pattern A 與 M2 兼容(規則 7 焦點 panel 機制)
- [x] Pattern E 與 M2 部分兼容(序數類別當 panel 維度)
- [x] Pattern B 與 M2 通常不一起用(分 panel 後類別配色失意義)

### 9 種圖表 references + M1

| Reference | 受影響? | 需要更新? |
|---|---|---|
| 01-bar-chart.md | 排名 small multiples | 「相關規範」加 cross-link |
| **02-line-chart.md** | **M2 主場** | 補 cross-link 段 |
| **03-area-chart.md** | **M2 主場**(累計圖跨地區並排) | 補 cross-link 段 |
| 04-stacked-chart.md | 不太用 | ── |
| 05-pie-chart.md | 不適用 | ── |
| 06-scatter-chart.md | 少數情境 | 補 cross-link 段(可選) |
| 07-histogram-boxplot.md | 跨組分布並排 | 補 cross-link 段(可選) |
| 08-pyramid-chart.md | 跨年度金字塔並排 | 補 cross-link 段(可選) |
| 09-choropleth-map.md | 不適用(本身就是地理 grid) | ── |
| 10-monochrome-usage.md | 不直接影響 | ── |
| **M1-uncertainty-modifier.md** | **M1 主動引用 M2** | M1 規則 1 邊界案例段補一句「> 3 序列改 small multiples → M2」 |

### SKILL.md decision tree

- [x] **新增 step 6**:「需要多 panels 並排比較不同分類維度?」→ 套 M2
- [x] §4.7 新章節介紹 M2(類似 §4.6 介紹 M1)
- [x] Reference Files 表新增 M2 條目

### 新檔案

- 新增 `skill/references/M2-small-multiples.md`(status: draft 期間)
- 新增 `skill/scripts/generate_examples.py` 內 `small_multiples_examples()` 函式(進 Active 才整合)
- Pilot 階段範例放 `skill/assets/examples/_drafts/`(改成 `m2*-small-multiples-*.py` 命名)

## Regression check · 對既有範例的回歸驗證

跑既有 21 張範例 PNG(原 19 + M1 新增 2)+ 投影片 + Office 樣板:

| 既有項目 | 狀態 |
|---|---|
| 01a-bar-single-focus.png | keep |
| 01b-bar-daily-with-ma.png | keep |
| 01c-bar-horizontal-ranking.png | keep |
| 02a-line-focus-vs-average.png | keep |
| 02b-line-multi-metric.png | keep |
| **02c-line-year-over-year.png** | **keep**(2 條疊一張,「跨年度同期比較」場景 < 4 序列適用直接疊,non-conflicting) |
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
| m1a-uncertainty-trailing-band.png | keep |
| m1b-uncertainty-errorbar-asymmetric.png | keep |
| 投影片 Slide 10-12 | keep |
| Office 樣板 6 個檔 | keep |

**統計**:
- `keep`: 33(全部)
- `adjust`: 0
- `waive`: 0
- `break`: 0

✓ 0 break、0 adjust ── 新規範完全不誤傷既有。M2 是補完現有未覆蓋領域,既有單 panel 圖型不受影響。

## Trade-offs · 取捨

- **好處**:
  - 補完疫情報告核心 layout 缺口(22 縣市並排、跨年度比較等實務場景)
  - 與 M1 自然銜接(M1 留下接口,M2 補完)
  - AI agent 在多 panel 場景有規範可循,跨報告一致
  - 與既有 patterns 互補不衝突
- **犧牲**:
  - references 多一個檔
  - SKILL.md 多一個 decision tree 分支與 §4.7 章節
- **為何選 layout modifier(M2)而非新 chart-type**:
  - small multiples 不是 chart type(它的內容仍是 line/bar/area 等),是「版面結構」
  - modifier 命名(M-prefix)清楚與 chart-type(01-10)區分
  - 與 M1 命名一致

## Alternatives considered · 評估過的其他方向

1. **Alt A:不規範,讓使用者自由發揮**
   - 否決:多 panel 場景無規範會產出 Y 軸不統一、grid 隨意排、標題位置不一致等問題
2. **Alt B:新建 chart-type reference `11-small-multiples.md`**
   - 否決:small multiples 不是 chart type;內容仍是 line/bar/area
3. **Alt C:把 small multiples 視為「圖表選用」的一個分支**
   - 否決:SKILL.md §3 圖表選用是「資料形態 → 圖表型」,small multiples 是「資料維度多 → 版面拆分」,屬不同 axis 的決策
4. **Alt D:強制每 panel 都顯示 X 軸標籤**
   - 否決:大量 panel 場景下會視覺擁擠,規則 10 給彈性(僅最下方一行標)
5. **Alt E:強制 Y 軸 scale 統一(無例外)**
   - 否決:magnitude 差太大的場景(縣市人口差 10 倍)會壓平小縣市的 panel,規則 1 給「標準化後統一」例外

## Open questions · 未解的問題

1. **規則 9 panel 間距**(`wspace=0.25, hspace=0.35`)── 數字可調整,但本指引要不要訂死預設值?
2. **規則 10 X 軸標籤**:「grid 行內 panel > 4 個時僅最下方一行標」── 4 是 arbitrary 邊界,要不要改為 ≥ 3 / ≥ 5 / 視情境?
3. **跨年度同期比較場景**(use case 4):**單一張多線 vs small multiples 拆 panel** 的決策門檻 ── 我寫「年份 > 3-4」改 small multiples,這個門檻 OK 嗎?還是用「序列數 > 4」這種更通用的判準?
4. **與既有 02c-line-year-over-year.png 的關係**:該 PNG 用「2 序列疊一張 + 灰色歷史範圍帶」,如果未來要新增「5 年並排」案例,要不要替換 02c?還是兩個範例並存(2 序列用 02c、5+ 年用 M2)?── 我傾向兩個並存

## Decision · 決策狀態

- [x] **Draft v1**   ── 待 reviewer review
- [ ] **Pilot**   ── reference + draft 範例 + SKILL.md 不更新
- [ ] **Active**  ── L1 → L2 → L3 同步,SKILL.md decision tree 更新
- [ ] **Withdrawn**

---

## Reviewer notes(v1 待確認)

1. **規則 6 panel 數量 grid 推薦表**:寫得太硬性嗎?或可接受?(我傾向 OK,實作上需明確指引)
2. **規則 7 焦點 panel 用主色 vs 主色更深版**:目前寫主色 `#739A6D`,但 M1 規則 11 學到「主色與 NEUTRAL 區分不夠」── 是否該改主色更深 `PRIMARY_DARK` `#5D7F58`?(需視覺對照)
3. **Open question #3 跨年度同期門檻**:「年份 > 3-4 改 small multiples」── 你的實務感覺是?
4. **Open question #4 02c 是否替換**:兩個並存,還是統一改 M2 風格?
