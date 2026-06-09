# epidemic_palette.R
# 疫情資料視覺化指引共用色票模組（R / ggplot2 版）
#
# 對應 Python 版 scripts/epidemic_palette.py，色票值完全一致。
# 兩者皆以 #739A6D（Sage Green）為主色，類別配色順序綠 → 藍 → 黃 → 鴨綠 → 銅 → 梅。
#
# 載入方式：
#   source("epidemic_palette.R")
#   library(ggplot2)
#   ggplot(df, aes(x, y, fill = grp)) +
#     geom_col(width = 0.6) +
#     scale_fill_epi() +
#     theme_epi()
#
# 相依：ggplot2（>= 3.4，scale 函式使用 linewidth）。字型建議安裝 Noto Sans TC /
#   Noto Serif TC；若用 showtext 載入 Google Fonts：
#     sysfonts::font_add_google("Noto Sans TC", "Noto Sans TC")
#     sysfonts::font_add_google("Noto Serif TC", "Noto Serif TC")
#     showtext::showtext_auto()

# === 主色階 ===
EPI_PRIMARY        <- "#739A6D"
EPI_PRIMARY_LIGHT  <- "#B4C9B1"
EPI_PRIMARY_DARK   <- "#5D7F58"   # 折線主序列
EPI_PRIMARY_DARKER <- "#374C34"   # 重點均線、深色標題

EPI_PRIMARY_SCALE <- c(
  "#F6F9F6", "#E8EEE7", "#D1DECF", "#B4C9B1", "#91B08C",
  "#739A6D", "#5D7F58", "#496345", "#374C34", "#253423"
)

# === 類別配色（依優先順序：綠 → 藍 → 黃 → 鴨綠 → 銅 → 梅）===
# 取用時依序取所需數量（2 類別取前 2，不可跳號）。最多 6 類別，
# 超過請合併為「其他」（中性灰 #CACFC9）。
EPI_CATEGORICAL <- c(
  "#739A6D",  # 01 Sage（主色）
  "#587A9D",  # 02 Slate Blue
  "#C8A041",  # 03 Mustard
  "#49888D",  # 04 Teal
  "#916E46",  # 05 Bronze
  "#955F71"   # 06 Plum
)

# === 折線專用加深版（細線比色塊顯淺，需加深以維持對比）===
EPI_LINE_COLORS <- list(
  primary = "#5D7F58",
  blue    = "#587A9D",
  yellow  = "#A8821F",  # Mustard 加深
  teal    = "#356B70"
)

# === 單色預設組合（Pattern E：顏色不傳達類別差異時）===
# 用於序數、時序、層次比較。淺 → 深須對應 弱 → 強 / 過去 → 現在。
EPI_MONOCHROME <- list(
  focus_2 = c("#496345", "#CACFC9"),
  scale_3 = c("#B4C9B1", "#739A6D", "#374C34"),
  scale_4 = c("#D1DECF", "#91B08C", "#5D7F58", "#374C34"),
  scale_5 = c("#D1DECF", "#B4C9B1", "#91B08C", "#5D7F58", "#374C34"),
  scale_6 = c("#E8EEE7", "#D1DECF", "#B4C9B1", "#91B08C", "#5D7F58", "#374C34"),
  scale_7 = c("#E8EEE7", "#D1DECF", "#B4C9B1", "#91B08C",
              "#739A6D", "#5D7F58", "#374C34")
)

# === 強調色家族（紅／橙系，僅用於警示，不可作一般類別色）===
EPI_ACCENT <- list(
  alert      = "#BE373C",
  terracotta = "#B5584A",
  clay       = "#B87B61",
  caution    = "#D2962D"
)

# === 中性色 ===
EPI_NEUTRAL <- list(
  "50"  = "#FAFAFA", "100" = "#F2F3F1", "200" = "#E4E7E4",
  "300" = "#CACFC9", "400" = "#A2ABA0", "500" = "#7A8778",
  "600" = "#5D675B", "700" = "#444C43", "800" = "#2C312B",
  "900" = "#181B18"
)

# === 語意色（KPI / 狀態）===
EPI_SEMANTIC <- list(
  success = "#54734F",
  warning = "#D2962D",
  danger  = "#BE373C",
  info    = "#477A9E"
)

# === 序列色階（單向：低 → 高）===
EPI_SEQUENTIAL <- c(
  "#F1F5F0", "#D4E0D2", "#AEC5AB", "#8BAC86",
  "#6A9164", "#506D4B", "#354832"
)

# === 發散色階（雙向：負 ← 中 → 正）。中點 #F2F3F2 非純白，避免零值看似缺資料 ===
EPI_DIVERGING <- c(
  "#476043", "#71936C", "#B2BFB0",
  "#F2F3F2",
  "#D8C5C0", "#BC8776", "#965440"
)


# === 取色輔助 ===

#' 依優先順序取前 n 個類別色
#' @param n 類別數量（最多 6）
epi_pal <- function(n = 6) {
  if (n > length(EPI_CATEGORICAL)) {
    warning("類別超過 6 色，建議合併為「其他」（中性灰 #CACFC9）")
  }
  EPI_CATEGORICAL[seq_len(min(n, length(EPI_CATEGORICAL)))]
}


# === ggplot2 scale 輔助 ===
# 採用 scale_*_manual 以相容各版本 ggplot2；類別依資料因子順序對應色票順序，
# 故第一個類別即主色 #739A6D（對齊指引「主物件用主色」規範）。

#' 類別配色 fill scale
scale_fill_epi <- function(...) {
  ggplot2::scale_fill_manual(values = EPI_CATEGORICAL, ...)
}

#' 類別配色 colour scale（美式 color 拼法別名見下）
scale_colour_epi <- function(...) {
  ggplot2::scale_colour_manual(values = EPI_CATEGORICAL, ...)
}
scale_color_epi <- scale_colour_epi

#' 單色色階 fill scale（Pattern E）
#' @param key EPI_MONOCHROME 的鍵："focus_2"、"scale_3" ~ "scale_7"
scale_fill_epi_mono <- function(key = "scale_3", ...) {
  ggplot2::scale_fill_manual(values = EPI_MONOCHROME[[key]], ...)
}

#' 單色色階 colour scale（Pattern E）
scale_colour_epi_mono <- function(key = "scale_3", ...) {
  ggplot2::scale_colour_manual(values = EPI_MONOCHROME[[key]], ...)
}
scale_color_epi_mono <- scale_colour_epi_mono

#' 序列色階（連續，低 → 高）
scale_fill_epi_sequential <- function(...) {
  ggplot2::scale_fill_gradientn(colours = EPI_SEQUENTIAL, ...)
}
scale_colour_epi_sequential <- function(...) {
  ggplot2::scale_colour_gradientn(colours = EPI_SEQUENTIAL, ...)
}

#' 發散色階（連續，負 ← 中 → 正）。中點非純白。
scale_fill_epi_diverging <- function(...) {
  ggplot2::scale_fill_gradientn(colours = EPI_DIVERGING, ...)
}
scale_colour_epi_diverging <- function(...) {
  ggplot2::scale_colour_gradientn(colours = EPI_DIVERGING, ...)
}


# === 主題 ===

#' 本指引 ggplot2 主題
#'
#' 移除頂部／右側框線、預設僅水平格線（直條／折線判讀方向）、
#' 標題置左、中文字型。
#'
#' @param base_size   基礎字級（預設 11）
#' @param base_family 內文字型（預設 Noto Sans TC）
#' @param title_family 標題字型（預設 Noto Serif TC）
theme_epi <- function(base_size = 11,
                      base_family = "Noto Sans TC",
                      title_family = "Noto Serif TC") {
  ggplot2::theme_minimal(base_family = base_family, base_size = base_size) +
    ggplot2::theme(
      panel.grid.major.y  = ggplot2::element_line(color = "#E4E7E4", linewidth = 0.4),
      panel.grid.major.x  = ggplot2::element_blank(),
      panel.grid.minor    = ggplot2::element_blank(),
      axis.line.x         = ggplot2::element_line(color = "#CACFC9", linewidth = 0.4),
      axis.ticks          = ggplot2::element_blank(),
      axis.title          = ggplot2::element_text(color = "#444C43", size = base_size),
      axis.text           = ggplot2::element_text(color = "#5D675B", size = base_size - 1),
      plot.title          = ggplot2::element_text(family = title_family, face = "bold",
                                                  size = base_size + 5, color = "#374C34"),
      plot.title.position = "plot",
      plot.subtitle       = ggplot2::element_text(color = "#5D675B", size = base_size),
      plot.caption        = ggplot2::element_text(color = "#7A8778", size = base_size - 2,
                                                  hjust = 0),
      plot.caption.position = "plot",
      legend.position     = "top",
      legend.justification = "left",
      legend.title        = ggplot2::element_text(size = base_size),
      legend.key.size     = ggplot2::unit(10, "pt")
    )
}


# === Trailing 移動平均 ===

#' Trailing 移動平均（本日含前 window-1 日，即 i-6 到 i）
#'
#' 對齊 Python 版 trailing_ma 與 WHO/CDC/JHU 通用慣例。前 window-1 天
#' 採自適應較短窗口（從第 1 天累積），不產生 NA、避免折線斷裂。
#'
#' @param data   數值向量
#' @param window 窗口大小（預設 7）
trailing_ma <- function(data, window = 7) {
  n <- length(data)
  vapply(seq_len(n), function(i) {
    lo <- max(1L, i - window + 1L)
    round(mean(data[lo:i]))
  }, numeric(1))
}
