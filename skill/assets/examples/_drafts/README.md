# Draft Examples ── 試行中的範例

本目錄存放 **Pilot 階段** 的範例圖。對應的規範還在試行,**不視為 reference 等級的官方範例**。

## 目前狀態

**目前沒有 Pilot 試行中的規範。**

過往採納紀錄:

| 範例 | 對應 RFC | 採納日期 | 移至 |
|---|---|---|---|
| `m1*-uncertainty-*.png` | [2026-06-01](../../../../docs/rfcs/2026-06-01-uncertainty.md) | 2026-06-09 | `skill/assets/examples/` 主目錄 |

## 規則(下次 Pilot 啟動時參考)

進入 Pilot 階段時:
- 對應 reference 加 frontmatter `status: draft` + `rfc: YYYY-MM-NN-name`
- 範例 PNG 命名 `<rfc-id>-<letter>-<name>.png` 或類似 modifier 編號(`m1a`、`m1b`)
- 生成腳本可暫放本目錄,但採納為 Active 後**移至** `skill/scripts/generate_examples.py` 整合進主例集
- 主目錄範例與 SKILL.md decision tree 在 **Active 後** 才更新,Pilot 期間刻意不動,避免 AI agent 把 draft 規範當成 active

完整流程見 `CONTRIBUTING.md` 的「規範新增的 RFC-lite 流程」段。
