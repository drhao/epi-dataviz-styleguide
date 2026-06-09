# Do / Don't 對照範例庫

本目錄存放「✗ DON'T 違反規範 / ✓ DO 正確做法」並排對照的 PNG,作為**既有規範條目的視覺教學補充**。

主目錄 `skill/assets/examples/*.png` 是「規範示範範例」── 給 AI agent 與設計師模仿;本目錄是「教學對照範例」── 給 review 或培訓時指出「為什麼不能 X」的視覺證據。

## 線上瀏覽

GitHub Pages 訪客可直接看完整 8 對對照頁:

**🌐 [docs/dont-vs-do.html](https://drhao.github.io/epi-dataviz-styleguide/dont-vs-do.html)**

(該頁 PNG 引用 `docs/examples/dont-vs-do/` 副本,因 GitHub Pages 僅 serve `docs/` 路徑。更新源 PNG 後須一併 `cp` 到 docs 副本目錄。)

## 與 docs/guideline.html Ch.9 的定位差異

兩者並存互補:

| | docs/guideline.html **Ch.9** | 本範例庫 / **dont-vs-do.html** |
|---|---|---|
| 對數 | 3 對 | 8 對 |
| 主題 | 4 項**核心原則**的應用 | **具體規則**的典型誤用 |
| 呈現 | Chart.js 動態繪製(嵌主指引) | 靜態 PNG(獨立檔案 + 獨立網頁) |
| 讀者 | docs 訪客(原則沉浸式 onboarding) | AI agent / 培訓 / review 引用 |

Ch.9 教「**為什麼**」遵守原則(原則導向),本範例庫教「**哪些具體錯**」(規則導向)。同一概念兩種呈現,非冗餘。

## 索引

| 檔案 | 對應規則 | 重點 |
|------|---------|------|
| `01-truncated-yaxis.png` | SKILL.md §4.4 / 01-bar-chart 規則 1 | Y 軸從零 vs 從 70 截斷誇大差異 |
| `02-red-as-categorical.png` | SKILL.md §1.3 紅色僅警示 | 多條折線都用紅色家族 vs Pattern B 類別配色 |
| `03-rainbow-bars.png` | 01-bar-chart §3 顏色策略 | 每根長條不同色 vs Pattern A 焦點凸顯 |
| `04-decorated-pie.png` | 05-pie-chart 規範 | 3D / 陰影 / explode vs 平面 2D + 直接標籤 |
| `05-too-many-pie-slices.png` | 05-pie-chart 條件使用 | 圓餅 9 切片 vs 排序橫條由大到小 |
| `06-spaghetti-vs-small-multiples.png` | M2-small-multiples | 22 縣市疊一張 spaghetti vs 4×6 small multiples |
| `07-chartjunk-vs-minimal.png` | SKILL.md §4.1.5 / §4.1.6 | 全邊框 + 雙向格線 + 灰底 vs 移除頂右邊框 + 僅水平格線 |
| `08-sort-by-name-vs-value.png` | 01-bar-chart 規則 4 | 排名直條圖按行政區編號排 vs 按數值大小排 |

## 使用情境

- **AI agent**:讀完 reference 後遇到模糊情境,可參照對照圖確認哪邊算 DON'T
- **設計師 / 分析師 review**:指出產出違反規範時,引用具體 ✗ 範例最有說服力
- **內部培訓**:當作「常見錯誤盤點」教材
- **跨機關採用**:推廣本指引時,並排對照比純文字解說有效

## 生成與重生

範例由 `skill/scripts/generate_dont_vs_do.py` 從 `epidemic_palette.py` 色票常數自動生成。色票若變動或新增 do/don't 條目,重跑即同步:

```bash
# 從 repo 根目錄
python3 skill/scripts/generate_dont_vs_do.py
```

## 為何分離於主例集

主例集(`skill/assets/examples/*.png`)是規範權威範例,SKILL.md decision tree 引用、AI agent 模仿、跨機關採用基準。本目錄是「教學對照」── 故意呈現錯誤示範,放主目錄會誤導 AI agent。獨立目錄 + 獨立生成腳本,語意清楚。

## 擴充

需要新增 do/don't 對照時:
1. 在 `generate_dont_vs_do.py` 加 `pair_NN_xxx()` 函式
2. main() 內加呼叫
3. 在本 README 索引補一行
4. 對應 reference 的「常見錯誤」段加 cross-link 指向 `dont-vs-do/NN-xxx.png`
