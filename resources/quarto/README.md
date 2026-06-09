# Quarto 支援

在 [Quarto](https://quarto.org) 報告／網站／簡報中套用疫情資料視覺化指引。本資料夾提供兩種互補做法：

| 檔案 | 適用 | 套用範圍 |
|------|------|---------|
| [`_brand.yml`](./_brand.yml) | Quarto **≥ 1.6** | 文件主題 **＋ 圖表**（ggplot2 / matplotlib）統一品牌 |
| [`epidemic.scss`](./epidemic.scss) | **所有版本** | HTML 文件主題（Bootstrap 變數、字型、callout） |

色票值與 [`skill/scripts/epidemic_palette.py`](../../skill/scripts/epidemic_palette.py) 及 [`epidemic_palette.R`](../../skill/scripts/epidemic_palette.R) 完全一致。

## 做法 A：`_brand.yml`（推薦，Quarto 1.6+）

把 `_brand.yml` 複製到 Quarto 專案根目錄。Quarto 會自動套用——文件主題、連結、callout 以及由 ggplot2 / matplotlib 繪製的圖表都會採用本指引的色彩與字型。

```
my-report/
├── _brand.yml          ← 從這裡複製過去
├── _quarto.yml
└── report.qmd
```

R / ggplot2 圖表（搭配 `library(thematic)` 時 Quarto 會自動掛上品牌）：

````markdown
```{r}
library(ggplot2)
ggplot(cases, aes(date, n, fill = region)) +
  geom_col(width = 0.6)
# _brand.yml 的 palette 會經 thematic 套用
```
````

若需要**精準的類別順序**（綠 → 藍 → 黃…）或單色色階（Pattern E），請另外 source 色票模組搭配使用：

````markdown
```{r}
source("path/to/epidemic_palette.R")
ggplot(cases, aes(date, n, fill = region)) +
  geom_col(width = 0.6) +
  scale_fill_epi() +     # 強制依指引順序取色
  theme_epi()
```
````

Python / matplotlib 圖表：

````markdown
```{python}
import sys; sys.path.append("path/to/skill/scripts")
from epidemic_palette import apply_style, CATEGORICAL
apply_style()
```
````

## 做法 B：`epidemic.scss`（任何 Quarto 版本）

在文件或 `_quarto.yml` 的 YAML 指定主題：

```yaml
format:
  html:
    theme: [cosmo, epidemic.scss]
    mainfont: "Noto Sans TC"
```

`epidemic.scss` 會覆寫 Bootstrap 的 `$primary`、字型、連結色與標題色，並提供 `--epi-cat-1` ~ `--epi-cat-6` CSS 變數供自訂圖表 / Observable cell 使用。

> 圖表配色：SCSS 只負責 HTML 文件外觀，圖表仍由繪圖引擎決定。請搭配 `epidemic_palette.R`（ggplot2）或 `epidemic_palette.py`（matplotlib）取得一致的圖表色彩。

## 字型

`_brand.yml` 與 `epidemic.scss` 皆預設 **Noto Sans TC**（內文）與 **Noto Serif TC**（標題）。HTML 輸出會自動從 Google Fonts 載入；PDF / Typst 輸出請確認本機已安裝對應字型。
