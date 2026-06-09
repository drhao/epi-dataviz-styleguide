# 5 分鐘入門 — 依角色分流

不同身份的人需要的東西不一樣。本頁針對 4 個典型角色,各給 **5 個步驟**讓你最快上手。

| 你是 | 入門目標 | 跳到 |
|---|---|---|
| 🎨 設計師 / 分析師 | 用 Excel / Power BI / Tableau 套用本指引色票畫圖 | [→](#-設計師--分析師) |
| 💻 工程師 | 用 Python / R / JS 程式產生符合規範的圖表 | [→](#-工程師) |
| 📋 PM / 培訓 / 簡報製作 | 把本指引濃縮為長官 brief / 教材 | [→](#-pm--培訓--簡報製作) |
| 🎯 長官 / 決策者 | 5 分鐘理解本指引精神 + 之後審圖能挑問題 | [→](#-長官--決策者) |

---

## 🎨 設計師 / 分析師

**入門目標**:把本指引色票套進你日常的 Excel / Power BI / Tableau。

| Step | 動作 | 時間 |
|---|---|---|
| **1** | 下載 [`resources/palette.csv`](https://github.com/drhao/epi-dataviz-styleguide/blob/main/resources/palette.csv) ── 6 個類別色 + 強調色 + 中性色的完整 HEX/RGB | 1 分 |
| **2** | **Excel 使用者**:`頁面配置` → `色彩` → `自訂色彩`,依 CSV 填入 Accent 1-6。**Power BI 使用者**:下載 [`powerbi-theme.json`](https://github.com/drhao/epi-dataviz-styleguide/blob/main/resources/powerbi-theme.json) → `檢視` → `佈景主題` → 匯入 | 2 分 |
| **3** | **5 個鐵則** ── 看 [Do/Don't 對照範例庫](dont-vs-do.html)(8 對視覺對照,5 分鐘內可逛完)。常踩雷:**Y 軸截斷、用紅色當類別色、彩虹條、圓餅切片太多、字典序排名** | 5 分 |
| **4** | 你的圖表類型怎麼選?看 [互動式圖表選用矩陣(guideline.html 圖表選用章)](guideline.html#ch8) ── 9 種圖式對應的情境一覽 | 3 分 |
| **5** | 卡關時:**[guideline.html](guideline.html)** 內含 13 張即時繪製範例,可直接 copy 配色/比例參數 | 隨時 |

**進階方向**(各 5 分鐘):
- 不確定性視覺化(R/Rt 預測、CI 帶):看 [M1 modifier 規範](https://github.com/drhao/epi-dataviz-styleguide/blob/main/skill/references/M1-uncertainty-modifier.md)
- 22 縣市 / 各年齡組並排:看 [M2 small multiples 規範](https://github.com/drhao/epi-dataviz-styleguide/blob/main/skill/references/M2-small-multiples.md)
- 預生成樣板(內部 office templates):聯絡 Dr. Hao(dr.hao.tw@gmail.com)

---

## 💻 工程師

**入門目標**:用 Python / R / JS 程式產生符合本指引的圖表,並讓 AI agent(Claude Code、Codex)自動遵守。

| Step | 動作 | 時間 |
|---|---|---|
| **1** | `git clone` repo,看 [`skill/scripts/epidemic_palette.py`](https://github.com/drhao/epi-dataviz-styleguide/blob/main/skill/scripts/epidemic_palette.py) ── 主要 color constants 與 helper 函式都在這 | 5 分 |
| **2** | 一行套樣式: ` from epidemic_palette import apply_style; apply_style()` ── 自動套主色、移除頂右框、CJK 字型 fallback、`trailing_ma` 等工具函式 | 1 分 |
| **3** | **R 開發者**:用 [`epidemic_palette.R`](https://github.com/drhao/epi-dataviz-styleguide/blob/main/skill/scripts/epidemic_palette.R) ── `theme_epi()` + `scale_fill_epi()` 等同等對等 ggplot2 函式 | 5 分 |
| **4** | **AI agent 整合**:把整個 `skill/` 資料夾放進 Claude Code / Codex / Antigravity 的 skill 目錄,問「畫每日確診直條圖」時 AI 會自動讀 SKILL.md 套規範。詳 [`skill/SKILL-README.md`](https://github.com/drhao/epi-dataviz-styleguide/blob/main/skill/SKILL-README.md) | 3 分 |
| **5** | 寫 PR 前跑兩條:`python3 skill/tests/test_palette.py`(80 測試)+ `python3 dev-tools/check_drift.py`(跨檔案一致性)。CI 也會跑這兩條當 gate | 1 分 |

**進階方向**:
- 寫新規範:走 [RFC-lite 流程](https://github.com/drhao/epi-dataviz-styleguide/blob/main/CONTRIBUTING.md#%E8%A6%8F%E7%AF%84%E6%96%B0%E5%A2%9E%E7%9A%84-rfc-lite-%E6%B5%81%E7%A8%8B)(`docs/rfcs/`)
- Quarto template:`resources/quarto/_brand.yml`
- Streamlit:`resources/streamlit/config.toml`
- Chart.js / D3:看 [`docs/guideline.html`](guideline.html) 第 12 章「技術實作參考」

---

## 📋 PM / 培訓 / 簡報製作

**入門目標**:把本指引濃縮成長官 brief 或內部培訓教材。

| Step | 動作 | 時間 |
|---|---|---|
| **1** | 下載 [**摘要版投影片 PDF**](guideline-slides-summary.pdf)(14 張,5 分鐘可講完)── 4 核心原則、主色、6 類別色、6 條鐵則、圖表選用矩陣 | 5 分 |
| **2** | 需要內部訓練?下載 [**完整版投影片 PDF**](guideline-slides-full.pdf)(22 張,30 分鐘培訓版,含 M1 不確定性、M2 small multiples、工具支援、AI agent 整合等補充章節) | 30 分(用作教材) |
| **3** | 培訓對照教材:[Do/Don't 對照範例庫](dont-vs-do.html)(8 對 ✗/✓ PNG)── 培訓時最有說服力的視覺證據 | 隨用隨拿 |
| **4** | 引用本指引:你的簡報可直接 link 到 GitHub Pages 站台 `https://drhao.github.io/epi-dataviz-styleguide/` ── 給聽眾「想深入再來看」 | 1 行 |
| **5** | 不確定哪段需要強調?**4 項核心原則**(清晰優先、誠實呈現、一致性、負責任溝通)是最該記住的;鐵則中**「紅色僅警示」**最常被讀者誤用,最值得在培訓中重複 | 1 分 |

**進階方向**:
- 自製簡報需要範例圖?[`skill/assets/examples/`](https://github.com/drhao/epi-dataviz-styleguide/tree/main/skill/assets/examples) 內 23 張 PNG 可直接拉進去
- 跨機關推廣?引用 Pages URL 或下載 [完整 PDF](guideline.pdf)(22 頁列印版)

---

## 🎯 長官 / 決策者

**入門目標**:5 分鐘理解本指引精神,之後審圖能挑問題、能要求屬下「依本指引修改」。

| Step | 動作 | 時間 |
|---|---|---|
| **1** | 看 [**摘要版投影片首 8 張**](guideline-slides-summary.pdf)(封面 + 4 原則 + 主色 + 類別配色 + 強調色 + 鐵則)── 後半 6 張是範例,可略過 | 3 分 |
| **2** | **4 項核心原則**:清晰優先 / 誠實呈現 / 一致性 / 負責任溝通 ── 記住這 4 個詞 | 30 秒 |
| **3** | **3 條「審圖時最常用」鐵則**: ① 直條圖 Y 軸從零(截軸 = 誤導);② 紅色只用於警示;③ 排名圖按數值大小排,不按字典序 | 1 分 |
| **4** | 看 [Do/Don't 對照範例庫](dont-vs-do.html) 第 1、2、4、8 張 ── 看完你能立即指出「這張圖哪裡不對」 | 5 分 |
| **5** | 屬下交圖時,只要問三個問題:**「Y 軸從零嗎?」「為什麼這裡用紅色?」「排名為什麼這樣排?」**── 涵蓋 80% 常見問題 | 隨時 |

**進階方向**:
- 對外發布前:檢查是否含「暫定數字」並明確標示
- 涉及預測 / 估計值:CI 帶有沒有畫出來?(R/Rt 等)── 看 [M1 不確定性](https://github.com/drhao/epi-dataviz-styleguide/blob/main/skill/references/M1-uncertainty-modifier.md) 精簡版

---

## 共通資源

- 🌐 [線上指引(GitHub Pages)](index.html)
- 📖 [完整指引 PDF](guideline.pdf)(22 頁列印版)
- 📊 [Do/Don't 對照範例庫](dont-vs-do.html)
- 💾 [GitHub repo](https://github.com/drhao/epi-dataviz-styleguide)
- 📧 聯絡:Dr. Hao(dr.hao.tw@gmail.com)
