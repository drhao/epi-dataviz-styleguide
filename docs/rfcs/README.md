# RFCs ── 規範新增提案

本目錄存放本指引的規範新增提案(Request For Comments)。

## 為什麼需要 RFC

`CONTRIBUTING.md` 的 L1/L2/L3 流程處理「**已決定**的變動如何同步到各層」。
但「**該不該加這個新規範**」、「會不會破壞既有圖表」這類前置討論需要書面留存與系統性盤點 ── 這就是 RFC 的位置。

關鍵動機:**避免規範擴張讓既有運作良好的圖表被誤傷**。RFC 強迫提案者在動手前盤點影響範圍。

## 何時需要寫 RFC

| 變動類型 | 需要 RFC? | 走哪個流程 |
|---|---|---|
| 修錯字、格式調整 | ✗ | CONTRIBUTING L1 |
| 補充說明、新增範例 | ✗ | CONTRIBUTING L2 |
| 既有規則調整 | △ | 視變更影響範圍 ── BREAKING 必寫 |
| **新規範類別**(新圖表類型、新 pattern、新規則大類) | ✓ | RFC → CONTRIBUTING L3 |
| **新工具支援 / 新依賴** | ✗ | CONTRIBUTING(已有先例:office-templates、slides) |

## 流程概覽

```
Stage 0 ── 對話討論(GitHub Issue / 維護者對話)
   │
   ├─ 確定方向後 →
   │
Stage 1 ── 寫 RFC(本目錄)
   │
   ├─ 必填:Affected existing rules + Regression check
   ├─ 對既有 19 張範例做 keep/adjust/waive/break 標記
   │
Stage 2 ── Pilot(試行,status: draft)
   │
   ├─ references/NN-xxx.md 寫好但 frontmatter status: draft
   ├─ 範例放 skill/assets/examples/_drafts/
   ├─ SKILL.md decision tree 暫不更新(AI agent 不主動套用)
   ├─ check_drift.py 對 draft 規範用 optional_in
   │
Stage 3 ── Promote 至 Active
   │
   ├─ 走完整 L1 → L2 → L3
   ├─ status 改 active,SKILL.md decision tree 更新
   ├─ CHANGELOG 加採納紀錄
   │
Stage 4 ── 後續迭代
   │
   ├─ 規範錯了 → status: deprecated + 寫替代
```

## 命名規則

`YYYY-MM-NN-short-name.md`

- **YYYY-MM**:提案月份
- **NN**:該月內第幾個 RFC,從 `01` 起跳
- **short-name**:kebab-case,3-5 字描述

例:`2026-06-01-uncertainty.md`、`2026-06-02-small-multiples.md`

## 寫作

複製 `0000-template.md` 開始寫。

## 索引

| 編號 | 標題 | 狀態 | 採納日期 |
|---|---|---|---|
| (尚無 RFC) | | | |

採納後請更新本表。
