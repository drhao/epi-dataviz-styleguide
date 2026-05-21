"""
epidemic_palette.py
疫情資料視覺化指引共用色票模組

匯入方式：
    from epidemic_palette import PRIMARY, CATEGORICAL, apply_style
    apply_style()
"""
import matplotlib.pyplot as plt
from matplotlib import font_manager
import os

# === 主色階 ===
PRIMARY        = "#739A6D"
PRIMARY_LIGHT  = "#B4C9B1"
PRIMARY_DARK   = "#5D7F58"   # 折線主序列
PRIMARY_DARKER = "#374C34"   # 重點均線、深色標題

PRIMARY_SCALE = [
    "#F6F9F6", "#E8EEE7", "#D1DECF", "#B4C9B1", "#91B08C",
    "#739A6D", "#5D7F58", "#496345", "#374C34", "#253423",
]

# === 單色預設組合 ===
# 用於「顏色不傳達類別差異」的情境(序數、時序、層次比較)
# 比類別配色更克制,讀者把注意力放在資料形狀而非色塊區分

MONOCHROME = {
    # 2 序列：本機關 vs 其他/平均（深色 + 淺中性灰）
    # 對比 ≥ 2.0,焦點與對照清楚可分
    "focus_2": ["#496345", "#CACFC9"],

    # 3 序列：低/中/高，或 過去/現在/未來 (淺→深)
    "scale_3": ["#B4C9B1", "#739A6D", "#374C34"],

    # 4 序列：序數類別,如 第1/2/3/4季,輕/中/重/極重症 (淺→深)
    "scale_4": ["#D1DECF", "#91B08C", "#5D7F58", "#374C34"],

    # 5 序列：細緻層次,如 5 個年齡層,5 個區間 (淺→深)
    "scale_5": ["#D1DECF", "#B4C9B1", "#91B08C", "#5D7F58", "#374C34"],

    # 6 序列：完整年齡帶,6 個月份,等等 (淺→深)
    "scale_6": ["#E8EEE7", "#D1DECF", "#B4C9B1", "#91B08C",
                "#5D7F58", "#374C34"],

    # 7 序列：一週、7 個年齡組,需要強化視覺間距 (淺→深)
    "scale_7": ["#E8EEE7", "#D1DECF", "#B4C9B1", "#91B08C",
                "#739A6D", "#5D7F58", "#374C34"],
}

# === 類別配色（依優先順序：綠 → 藍 → 黃 → 鴨綠 → 銅 → 梅）===
CATEGORICAL = [
    "#739A6D",  # 01 Sage（主色）
    "#587A9D",  # 02 Slate Blue
    "#C8A041",  # 03 Mustard
    "#49888D",  # 04 Teal
    "#916E46",  # 05 Bronze
    "#955F71",  # 06 Plum
]

# 折線專用加深版
LINE_COLORS = {
    "primary": "#5D7F58",
    "blue":    "#587A9D",
    "yellow":  "#A8821F",  # Mustard 加深
    "teal":    "#356B70",
}

# === 強調色家族（紅／橙系，僅用於警示）===
ACCENT = {
    "alert":      "#BE373C",
    "terracotta": "#B5584A",
    "clay":       "#B87B61",
    "caution":    "#D2962D",
}

# === 中性色 ===
NEUTRAL = {
    "50":  "#FAFAFA", "100": "#F2F3F1", "200": "#E4E7E4",
    "300": "#CACFC9", "400": "#A2ABA0", "500": "#7A8778",
    "600": "#5D675B", "700": "#444C43", "800": "#2C312B",
    "900": "#181B18",
}

# === 語意色 ===
SEMANTIC = {
    "success": "#54734F",
    "warning": "#D2962D",
    "danger":  "#BE373C",
    "info":    "#477A9E",
}

# === 序列色階（單向）===
SEQUENTIAL = [
    "#F1F5F0", "#D4E0D2", "#AEC5AB", "#8BAC86",
    "#6A9164", "#506D4B", "#354832",
]

# === 發散色階（雙向：負 ← 中 → 正）===
DIVERGING = [
    "#476043", "#71936C", "#B2BFB0",
    "#F2F3F2",
    "#D8C5C0", "#BC8776", "#965440",
]


def _build_font_list(use_chinese):
    """偵測本機可用的 CJK 字型,構建按優先順序排列的字型 list。

    matplotlib 拿到 list 後會依序試;這裡先過濾本機可用字型,
    避免渲染時拋出 "Font family not found" warnings。

    若本機完全沒任何 CJK 字型,中文字會以方塊顯示。建議安裝:
      - macOS:  brew install --cask font-noto-sans-cjk
      - Linux:  sudo apt-get install fonts-noto-cjk
      - Windows: https://fonts.google.com/noto/specimen/Noto+Sans+TC
    """
    if not use_chinese:
        return ["DejaVu Sans"]

    candidates = [
        "Noto Sans TC",        # 開源,跨平台(推薦安裝)
        "Noto Sans CJK TC",
        "Noto Sans CJK JP",
        "Source Han Sans TC",  # Adobe 思源黑體
        "PingFang TC",         # macOS 內建
        "Heiti TC",            # macOS 內建
        "Microsoft JhengHei",  # Windows 繁中內建
        "Microsoft YaHei",     # Windows 簡中內建
        "WenQuanYi Micro Hei", # Linux 開源常見
        "Noto Sans SC",        # 簡中 fallback
        "SimHei",               # Windows 簡中經典
    ]
    available = {f.name for f in font_manager.fontManager.ttflist}
    matched = [c for c in candidates if c in available]
    # 結尾加非 CJK fallback,確保拉丁字符 / 數字 / 標點仍能正常渲染
    return matched + ["DejaVu Sans"]


def apply_style(use_chinese=True):
    """套用本指引的 matplotlib 全域樣式"""
    plt.rcParams.update({
        # 顏色
        "axes.prop_cycle": plt.cycler(color=CATEGORICAL),

        # 邊框：移除頂部右側
        "axes.spines.top":   False,
        "axes.spines.right": False,
        "axes.edgecolor":    NEUTRAL["300"],
        "axes.linewidth":    0.8,

        # 網格：預設僅水平線（直條/折線最常見的判讀方向）
        # 需要垂直格線時（如散佈圖、水平長條圖），個別圖表手動開啟
        "axes.grid":      True,
        "axes.grid.axis": "y",
        "axes.axisbelow": True,
        "grid.color":     NEUTRAL["200"],
        "grid.linewidth": 0.6,
        "grid.linestyle": "-",

        # 字體:CJK 自動 fallback。macOS/Windows/Linux 都能用,
        # 不需要強制使用者安裝特定字型(雖然推薦 Noto Sans TC)
        "font.family":      "sans-serif",
        "font.sans-serif":  _build_font_list(use_chinese),
        "font.size":        11,
        "axes.titlesize":   14,
        "axes.titleweight": "semibold",
        "axes.titlepad":  14,
        "axes.labelsize": 11,
        "axes.labelcolor": NEUTRAL["700"],
        "xtick.labelsize": 10,
        "ytick.labelsize": 10,
        "xtick.color":    NEUTRAL["600"],
        "ytick.color":    NEUTRAL["600"],
        "xtick.major.size": 0,
        "ytick.major.size": 0,
        "xtick.major.pad":  6,
        "ytick.major.pad":  6,

        # 圖例
        "legend.frameon":     False,
        "legend.fontsize":    10,
        "legend.title_fontsize": 11,

        # 輸出
        "figure.dpi":       100,
        "savefig.dpi":      150,
        "savefig.bbox":     "tight",
        "savefig.facecolor": "white",
        "figure.facecolor": "white",
    })


def trailing_ma(data, window=7):
    """Trailing 移動平均（本日含前 window-1 日,即 i-6 到 i)

    前 window-1 天因為窗口不足,使用自適應窗口(從第 1 天累積到當天)避免斷線。
    採用 trailing 而非 centered 因為:
      1. 通用慣例(WHO/CDC/JHU 等公開儀表板皆採 trailing)
      2. 即時 dashboard 場景無未來資料可用
      3. 不需要在不同情境切換不同 MA 演算法
    """
    n = len(data)
    return [
        round(sum(data[max(0, i - window + 1):i + 1]) /
              min(window, i + 1))
        for i in range(n)
    ]


def hide_y_axis(ax):
    """當長條上已標註數值時，可隱藏 Y 軸減少視覺冗餘

    隱藏項目：Y 軸標籤文字、刻度、刻度線、Y 軸標題、水平格線
    （X 軸軸線保留，仍需區分長條與背景）

    Args:
        ax: matplotlib Axes 物件
    """
    ax.tick_params(axis="y", which="both", left=False, labelleft=False)
    ax.set_ylabel("")
    ax.spines["left"].set_visible(False)
    ax.grid(False)


# === 日期軸格式化輔助 ===
# 疫情資料的時間軸常見三種情境：短期（天/週）、中期（月）、跨年
# 以下函式封裝 matplotlib.dates 常用設定，避免每張圖重複配置

def format_date_axis_daily(ax, interval=4):
    """短期每日資料（≤ 5 週）：每 N 天標一個日期，格式 MM/DD

    Args:
        ax: matplotlib Axes
        interval: 標籤間隔天數（預設 4，避免擁擠）
    """
    import matplotlib.dates as mdates
    ax.xaxis.set_major_locator(mdates.DayLocator(interval=interval))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%m/%d"))


def format_date_axis_weekly(ax):
    """中期每週資料（1-6 個月）：每週一標示，格式 MM/DD"""
    import matplotlib.dates as mdates
    ax.xaxis.set_major_locator(mdates.WeekdayLocator(byweekday=mdates.MO))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%m/%d"))


def format_date_axis_monthly(ax, show_year_on_jan=True):
    """跨月／跨年資料：每月 1 日標示，1 月顯示年份

    Args:
        ax: matplotlib Axes
        show_year_on_jan: 是否在每年 1 月顯示完整年份（如「2025\\n1月」）
                         False 則只顯示「1月」
    """
    import matplotlib.dates as mdates
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    if show_year_on_jan:
        # 1 月顯示「YYYY\n1月」，其他月份只顯示「N月」
        def _fmt(x, pos=None):
            d = mdates.num2date(x)
            if d.month == 1:
                return f"{d.year}\n1月"
            return f"{d.month}月"
        from matplotlib.ticker import FuncFormatter
        ax.xaxis.set_major_formatter(FuncFormatter(_fmt))
    else:
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%m月"))
