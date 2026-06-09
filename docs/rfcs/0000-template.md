# RFC YYYY-MM-NN: 提案標題

- **作者**: 你的名字
- **提案日期**: YYYY-MM-DD
- **狀態**: Draft  <!-- Draft | Pilot | Active | Withdrawn -->
- **目標版本**: (採納時填,例 v1.1)

## Context · 為什麼需要這個規範

(背景說明:目前的痛點、發現的缺口、引發提案的具體事件)

### Real use cases

至少 3 個實際使用情境,證明這個規範有需求:

1. **Use case A**: (描述真實場景與目前該怎麼做)
2. **Use case B**:
3. **Use case C**:

## Proposal · 規範草案

### 適用情境

(明確列出何時套用此規範)

### 不適用情境

(同樣重要 ── 明確列出此規範不該管的場景,避免擴張)

### 邊界案例

(灰色地帶的處理:例 X 應該套用嗎?例 Y 呢?)

### 規則細節

(具體規範條文)

### 程式碼範例

```python
# 範例
```

## Affected existing rules · 對既有規範的影響盤點

**這是 RFC 最關鍵的一段,必須誠實填寫。**

### Patterns(A/B/C/D/E)

- [ ] 不影響任何既有 pattern
- [ ] 影響 Pattern X:[如何影響、是擴充還是衝突]

### 9 種圖表 references

| Reference | 受影響? | 需要更新? |
|---|---|---|
| 01-bar-chart.md | | |
| 02-line-chart.md | | |
| 03-area-chart.md | | |
| 04-stacked-chart.md | | |
| 05-pie-chart.md | | |
| 06-scatter-chart.md | | |
| 07-histogram-boxplot.md | | |
| 08-pyramid-chart.md | | |
| 09-choropleth-map.md | | |
| 10-monochrome-usage.md | | |

### SKILL.md decision tree

- [ ] 不變
- [ ] 新增分支:[在哪、how]
- [ ] 修改既有分支:[在哪、how]

## Regression check · 對既有範例的回歸驗證

對 `skill/assets/examples/` 既有 19 張範例 PNG(以及投影片版內 Chart.js 範例)的標記:

| 既有項目 | 在新規範下的狀態 |
|---|---|
| 01a-bar-single-focus.png | [keep / adjust / waive / break] |
| 01b-bar-daily-with-ma.png | |
| 01c-bar-horizontal-ranking.png | |
| 02a-line-focus-vs-average.png | |
| 02b-line-multi-metric.png | |
| 02c-line-year-over-year.png | |
| 03a-area-cumulative.png | |
| 03b-area-multi-series.png | |
| 04a-stacked-100-percent.png | |
| 04b-stacked-horizontal.png | |
| 04c-grouped-bar.png | |
| 05a-pie-standard.png | |
| 05b-donut-with-center.png | |
| 06a-scatter-correlation.png | |
| 06b-bubble-3rd-dimension.png | |
| 07a-histogram.png | |
| 07b-boxplot.png | |
| 08-pyramid.png | |
| 09-choropleth-heatmap.png | |
| 10a-mono-stacked-severity.png | |
| 10b-mono-line-waves.png | |
| 10c-mono-area-doses.png | |

**標記定義:**
- `keep` ── 現有作法在新規範下仍合規,不需動
- `adjust` ── 需小幅修改才合規(列出具體調整)
- `waive` ── 既有圖跨期保留(legacy),但新圖必須遵守新規範
- `break` ── 既有圖在新規範下違規且無法調整 → **警訊,重新檢視 proposal**

若 `break` 數量 > 1,強烈建議回到 Stage 0 重新討論方向。

## Trade-offs · 取捨

- **好處**:
- **犧牲**:
- **為何選這個方向(而非 alternatives)**:

## Alternatives considered · 評估過的其他方向

列出評估過但否決的方案,簡述否決理由:

1. **Alt A**: (否決理由)
2. **Alt B**: (否決理由)

## Open questions · 未解的問題

採納前需釐清的事項:

1.
2.

## Decision · 決策狀態

- [ ] **Draft**   ── 對話討論中
- [ ] **Pilot**   ── 試行:references 寫好但 `status: draft`,SKILL.md decision tree 不更新
- [ ] **Active**  ── 正式採納:走完 L1→L2→L3,SKILL.md 更新,寫進 CHANGELOG
- [ ] **Withdrawn** ── 撤回(原因記錄在下方)

採納後請:
1. 更新 `docs/rfcs/README.md` 的索引表
2. CHANGELOG.md 加採納紀錄
3. references/NN-xxx.md 的 frontmatter 改 `status: active`
