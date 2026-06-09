# Draft Examples ── 試行中的範例

本目錄存放 **Pilot 階段** 的範例圖。對應的規範還在試行,**不視為 reference 等級的官方範例**。

## 對應規範

| 範例 PNG | 所屬 RFC | Pilot reference |
|---|---|---|
| `m1-uncertainty-*.png` | [2026-06-01](../../../../docs/rfcs/2026-06-01-uncertainty.md) | [`skill/references/M1-uncertainty-modifier.md`](../../../references/M1-uncertainty-modifier.md) |

## 生成與重生

範例由本目錄內的 `*.py` 腳本生成。色票若變動或規範修訂,重跑對應腳本即同步:

```bash
# 從 repo 根目錄
python3 skill/assets/examples/_drafts/m1_uncertainty_examples.py
```

## 進入 Active 後

當 Pilot reference 升級為 Active 狀態(走完 L1 → L2 → L3),對應 PNG 會 **移至** `skill/assets/examples/`(主目錄),本目錄移除該檔。生成腳本也應隨之搬到 `skill/scripts/generate_examples.py` 內,作為主要範例集的一部分。

## 為何分離

主目錄的 `skill/assets/examples/*.png` 是 **規範權威範例**:SKILL.md decision tree 引用、AI agent 模仿、跨機關採用時的視覺基準。Pilot 階段的範例還可能因 reviewer feedback 而調整實作細節,放主目錄會誤導 AI agent 與後續使用者。
