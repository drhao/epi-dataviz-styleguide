"""
generate_examples.py
產生所有圖表類型的範例 PNG（依疫情資料視覺化指引）

執行方式：
    python generate_examples.py

輸出至 ../assets/examples/ 資料夾。每個圖表類型都有 1-2 個範例。
"""
import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import Patch

from epidemic_palette import (
    PRIMARY, PRIMARY_DARK, PRIMARY_DARKER, PRIMARY_LIGHT,
    CATEGORICAL, MONOCHROME, LINE_COLORS, ACCENT, NEUTRAL, SEMANTIC,
    SEQUENTIAL, DIVERGING,
    apply_style, centered_ma, hide_y_axis,
    format_date_axis_daily, format_date_axis_weekly, format_date_axis_monthly,
)

OUT_DIR = os.path.join(os.path.dirname(__file__), "..", "assets", "examples")
os.makedirs(OUT_DIR, exist_ok=True)
apply_style()


def save(fig, name):
    path = os.path.join(OUT_DIR, f"{name}.png")
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  ✓ {name}.png")


# ============== 01. 直條圖 ==============
def bar_chart_examples():
    print("[01] Bar chart...")

    # A. 單組直條（凸顯焦點）
    fig, ax = plt.subplots(figsize=(8, 4.5))
    cats = ["教育", "社福", "經發", "環保", "交通", "文化"]
    vals = [98, 92, 105, 87, 78, 95]
    colors = [NEUTRAL["400"] if i != 2 else PRIMARY for i in range(len(cats))]
    bars = ax.bar(cats, vals, color=colors, width=0.6)
    ax.set_title("各部門年度預算執行率（凸顯焦點：經發）", loc="left")
    ax.set_ylim(0, 120)
    # 直條上方標數值
    for bar, v in zip(bars, vals):
        ax.text(bar.get_x() + bar.get_width()/2, v + 2, f"{v}%",
                ha="center", fontsize=10, color=NEUTRAL["700"])
    # 數值已直接標註,隱藏 Y 軸減少冗餘
    hide_y_axis(ax)
    save(fig, "01a-bar-single-focus")

    # B. 密集每日直條 + 中心對齊移動平均（使用日期物件）
    from datetime import date, timedelta
    fig, ax = plt.subplots(figsize=(9, 4.5))
    # 建立 28 天的日期序列（截至範例日 2026-05-21）
    end_date = date(2026, 5, 21)
    dates = [end_date - timedelta(days=27-i) for i in range(28)]
    np.random.seed(42)
    base = 1500 + np.arange(28) * 100
    weekend_dip = np.array([0.6 if d.weekday() >= 5 else 1.0 for d in dates])
    daily = (base * weekend_dip + np.random.randint(-200, 200, 28)).astype(int)
    ma = centered_ma(list(daily), 7)

    ax.bar(dates, daily, color=PRIMARY, width=0.75, label="每日新增")
    ax.plot(dates, ma, color=PRIMARY_DARKER, linewidth=2.5, label="7 日移動平均")
    ax.set_ylabel("新增確診數")
    ax.set_title("每日新增確診（直條 + 7 日移動平均）", loc="left")
    # 套用日期格式：每 4 天標一個 MM/DD
    format_date_axis_daily(ax, interval=4)
    ax.legend(loc="upper left")
    save(fig, "01b-bar-daily-with-ma")

    # C. 水平排名長條（含強調）
    fig, ax = plt.subplots(figsize=(8, 5))
    cities = ["雲林縣", "新竹縣", "屏東縣", "彰化縣", "臺南市",
              "高雄市", "臺中市", "桃園市", "臺北市", "新北市"]
    rates = [480, 510, 540, 590, 640, 680, 720, 760, 870, 920]
    colors_h = [ACCENT["terracotta"] if r >= 800 else PRIMARY for r in rates]
    ax.barh(cities, rates, color=colors_h, height=0.7)
    ax.set_title("各縣市每 10 萬人口確診率排名（超過 800 標 Terracotta）", loc="left")
    for i, (city, rate) in enumerate(zip(cities, rates)):
        ax.text(rate + 15, i, str(rate), va="center", fontsize=10,
                color=NEUTRAL["700"])
    ax.set_xlim(0, 1050)
    # 數值已標於長條右端,隱藏 X 軸減少冗餘
    ax.tick_params(axis="x", which="both", bottom=False, labelbottom=False)
    ax.set_xlabel("")
    ax.spines["bottom"].set_visible(False)
    ax.grid(False)
    save(fig, "01c-bar-horizontal-ranking")


# ============== 02. 折線圖 ==============
def line_chart_examples():
    print("[02] Line chart...")

    # A. Pattern A 焦點對照（本機關 vs. 平均）
    fig, ax = plt.subplots(figsize=(8, 4.5))
    years = list(range(2020, 2026))
    ours = [12.4, 13.2, 13.8, 15.1, 16.2, 17.5]
    avg  = [12.1, 12.7, 13.1, 13.8, 14.4, 14.9]
    ax.plot(years, ours, color=PRIMARY_DARK, linewidth=2.5,
            marker="o", markersize=5, label="本機關")
    ax.plot(years, avg, color=NEUTRAL["400"], linewidth=1.5,
            linestyle="--", marker="s", markersize=4, label="同類機關平均")
    ax.set_ylabel("服務人次（千）")
    ax.set_title("近 6 年服務人次趨勢（焦點：本機關）", loc="left")
    ax.legend(loc="upper left")
    # 直接標籤線條末端
    ax.annotate(f"{ours[-1]}", xy=(years[-1], ours[-1]),
                xytext=(8, 0), textcoords="offset points",
                fontsize=10, color=PRIMARY_DARK, fontweight="bold")
    save(fig, "02a-line-focus-vs-average")

    # B. 多指標折線（用形狀區分輔助色覺友善）
    fig, ax = plt.subplots(figsize=(9, 4.5))
    weeks = [f"W{i}" for i in range(1, 13)]
    cases = [42, 58, 78, 92, 100, 96, 84, 68, 52, 38, 28, 22]
    hosp  = [28, 38, 52, 70, 88, 100, 94, 78, 62, 48, 36, 28]
    sev   = [18, 24, 32, 48, 68, 88, 100, 92, 76, 60, 48, 38]

    ax.plot(weeks, cases, color=LINE_COLORS["primary"], linewidth=2.5,
            marker="o", markersize=6, label="確診（標準化）")
    ax.plot(weeks, hosp, color=LINE_COLORS["blue"], linewidth=2,
            marker="s", markersize=5, label="住院")
    ax.plot(weeks, sev, color=LINE_COLORS["yellow"], linewidth=2,
            marker="^", markersize=6, label="重症")
    ax.set_ylabel("標準化值（最大 = 100）")
    ax.set_title("多指標監測：確診→住院→重症的時滯（色 + 形狀雙重編碼）", loc="left")
    ax.legend(loc="upper right")
    save(fig, "02b-line-multi-metric")

    # C. 同期比較含歷史範圍
    fig, ax = plt.subplots(figsize=(9, 4.5))
    weeks = np.arange(1, 25)
    this_year  = np.array([180, 220, 280, 340, 420, 520, 680, 920, 1280,
                           1820, 2640, 3580, 4220, 4180, 3640, 2840, 2120,
                           1580, 1180, 880, 660, 490, 360, 280])
    last_year  = np.array([220, 260, 310, 380, 460, 560, 720, 980, 1340,
                           1820, 2480, 3120, 3640, 3580, 3120, 2480, 1880,
                           1380, 1020, 760, 570, 420, 310, 240])
    hist_high  = (last_year * 1.35).astype(int)
    hist_low   = (last_year * 0.65).astype(int)

    ax.fill_between(weeks, hist_low, hist_high,
                    color=NEUTRAL["400"], alpha=0.22, label="歷史範圍（±1 SD）")
    ax.plot(weeks, last_year, color=NEUTRAL["400"], linewidth=1.5,
            linestyle="--", label="去年同期")
    ax.plot(weeks, this_year, color=PRIMARY_DARK, linewidth=3,
            label="今年")
    ax.set_xlabel("相對週數（W1 = 流行季開始）")
    ax.set_ylabel("每週新增確診數")
    ax.set_title("同期比較：今年 vs. 去年 + 歷史範圍", loc="left")
    ax.legend(loc="upper right")
    save(fig, "02c-line-year-over-year")


# ============== 03. 區域圖 ==============
def area_chart_examples():
    print("[03] Area chart...")

    # A. 單序列累計 + 目標線（使用日期物件）
    from datetime import date
    fig, ax = plt.subplots(figsize=(8, 4.5))
    months_date = [date(2025, m, 1) for m in range(1, 13)]
    cov = [42, 58, 71, 79, 84, 87, 89, 91, 92, 93, 94, 94]

    ax.fill_between(months_date, 0, cov, color=PRIMARY, alpha=0.25)
    ax.plot(months_date, cov, color=PRIMARY_DARK, linewidth=2.5,
            marker="o", markersize=4)
    ax.axhline(y=90, color=ACCENT["alert"], linewidth=1.5,
               linestyle="--", label="目標 90%")
    ax.set_ylabel("覆蓋率（%）")
    ax.set_ylim(0, 100)
    ax.set_title("疫苗第 1 劑累計覆蓋率（含目標線）", loc="left")
    # 套用月份格式（每月一標,1月顯示年份）
    format_date_axis_monthly(ax)
    ax.legend(loc="lower right")
    save(fig, "03a-area-cumulative")

    # B. 多序列疊加（半透明）— 同樣使用日期物件
    fig, ax = plt.subplots(figsize=(8.5, 4.5))
    dose1 = [42, 58, 71, 79, 84, 87, 89, 91, 92, 93, 94, 94]
    dose2 = [28, 42, 56, 67, 74, 79, 83, 86, 88, 89, 90, 91]
    dose3 = [8, 18, 28, 38, 46, 53, 59, 64, 68, 72, 75, 77]

    ax.fill_between(months_date, 0, dose1, color=PRIMARY,
                    alpha=0.22, label="第 1 劑")
    ax.plot(months_date, dose1, color=LINE_COLORS["primary"], linewidth=2.5)
    ax.fill_between(months_date, 0, dose2, color=CATEGORICAL[1],
                    alpha=0.22, label="第 2 劑")
    ax.plot(months_date, dose2, color=LINE_COLORS["blue"], linewidth=2.5)
    ax.fill_between(months_date, 0, dose3, color=CATEGORICAL[2],
                    alpha=0.22, label="第 3 劑")
    ax.plot(months_date, dose3, color=LINE_COLORS["yellow"], linewidth=2.5)
    ax.set_ylabel("覆蓋率（%）")
    ax.set_ylim(0, 100)
    ax.set_title("疫苗 1/2/3 劑累計覆蓋率", loc="left")
    format_date_axis_monthly(ax)
    ax.legend(loc="lower right", ncol=3)
    save(fig, "03b-area-multi-series")


# ============== 04. 堆疊圖 ==============
def stacked_chart_examples():
    print("[04] Stacked chart...")

    # A. 100% 百分比堆疊（變異株）
    fig, ax = plt.subplots(figsize=(8, 4.5))
    months_v = ["11月", "12月", "1月", "2月", "3月", "4月"]
    jn1 = [62, 48, 32, 18, 8, 3]
    kp2 = [28, 36, 42, 38, 24, 14]
    kp3 = [6, 12, 18, 28, 42, 48]
    lb1 = [2, 3, 6, 14, 22, 30]
    other = [2, 1, 2, 2, 4, 5]

    ax.bar(months_v, jn1, color=CATEGORICAL[0], width=0.6, label="JN.1")
    ax.bar(months_v, kp2, bottom=jn1, color=CATEGORICAL[1], width=0.6, label="KP.2")
    bot3 = [a+b for a, b in zip(jn1, kp2)]
    ax.bar(months_v, kp3, bottom=bot3, color=CATEGORICAL[2], width=0.6, label="KP.3")
    bot4 = [a+b+c for a, b, c in zip(jn1, kp2, kp3)]
    ax.bar(months_v, lb1, bottom=bot4, color=CATEGORICAL[3], width=0.6, label="LB.1")
    bot5 = [a+b+c+d for a, b, c, d in zip(jn1, kp2, kp3, lb1)]
    ax.bar(months_v, other, bottom=bot5, color=NEUTRAL["300"], width=0.6, label="其他")
    ax.set_ylabel("組成比例（%）")
    ax.set_ylim(0, 100)
    ax.set_title("變異株消長：100% 堆疊長條", loc="left")
    ax.legend(loc="upper left", bbox_to_anchor=(1.01, 1), ncol=1)
    save(fig, "04a-stacked-100-percent")

    # B. 水平堆疊條（圓餅的推薦替代）
    fig, ax = plt.subplots(figsize=(8.5, 3.5))
    rows = ["2024 年", "2023 年", "2022 年"]
    full = [62, 48, 28]
    partial = [18, 22, 24]
    none = [14, 22, 38]
    unknown = [6, 8, 10]

    ax.barh(rows, full, color=CATEGORICAL[0], height=0.6, label="已完整接種")
    ax.barh(rows, partial, left=full, color=CATEGORICAL[1], height=0.6, label="部分接種")
    left3 = [a+b for a, b in zip(full, partial)]
    ax.barh(rows, none, left=left3, color=CATEGORICAL[2], height=0.6, label="未接種")
    left4 = [a+b+c for a, b, c in zip(full, partial, none)]
    ax.barh(rows, unknown, left=left4, color=NEUTRAL["300"], height=0.6, label="不詳")
    ax.set_xlim(0, 100)
    ax.set_xlabel("比例（%）")
    ax.set_title("確診者疫苗接種狀態：跨年度組成比較（水平堆疊條）", loc="left")
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.2), ncol=4)
    save(fig, "04b-stacked-horizontal")

    # C. 分組長條
    # 設計原則：組內條間留 1-2px 細縫（區分各條），組間留更大空白（區分主分類）
    fig, ax = plt.subplots(figsize=(9, 4.5))
    ages = ["0-9", "10-19", "20-39", "40-59", "60-69", "70-79", "80+"]
    mild = [78, 85, 89, 82, 70, 55, 38]
    mod  = [18, 13,  9, 14, 22, 32, 42]
    sev  = [ 4,  2,  2,  4,  8, 13, 20]

    x = np.arange(len(ages))
    bar_w = 0.23     # 條寬（較細，讓組內有細縫）
    offset = 0.25    # 中心偏移略大於條寬，產生細縫
    ax.bar(x - offset, mild, bar_w, color=CATEGORICAL[0], label="輕症")
    ax.bar(x,          mod,  bar_w, color=CATEGORICAL[1], label="中症")
    ax.bar(x + offset, sev,  bar_w, color=CATEGORICAL[2], label="重症")
    ax.set_xticks(x)
    ax.set_xticklabels(ages)
    ax.set_ylabel("比例（%）")
    ax.set_xlabel("年齡層")
    ax.set_title("年齡層 × 嚴重度（分組長條圖）", loc="left")
    ax.legend(loc="upper right")
    save(fig, "04c-grouped-bar")


# ============== 05. 圓餅／甜甜圈 ==============
def pie_chart_examples():
    print("[05] Pie chart...")

    # A. 標準圓餅（僅 4 類，直接標籤）
    fig, ax = plt.subplots(figsize=(7, 5))
    labels = ["已完整接種", "部分接種", "未接種", "不詳"]
    sizes = [62, 18, 14, 6]
    colors_p = [PRIMARY, CATEGORICAL[1], CATEGORICAL[2], NEUTRAL["300"]]

    wedges, texts, autotexts = ax.pie(
        sizes, labels=labels, colors=colors_p,
        autopct=lambda p: f"{p:.0f}%", startangle=90,
        counterclock=False,  # 順時針
        wedgeprops=dict(edgecolor="white", linewidth=2),
        textprops=dict(fontsize=11, color=NEUTRAL["800"]),
        pctdistance=0.78,
    )
    for at in autotexts:
        at.set_color("white")
        at.set_fontweight("bold")
        at.set_fontsize(11)
    ax.set_title("確診者疫苗接種狀態（圓餅，僅 4 類）", loc="left")
    save(fig, "05a-pie-standard")

    # B. 甜甜圈圖（中心放關鍵數字）
    fig, ax = plt.subplots(figsize=(7, 5))
    ax.pie(sizes, labels=labels, colors=colors_p,
           autopct=lambda p: f"{p:.0f}%", startangle=90,
           counterclock=False,
           wedgeprops=dict(width=0.4, edgecolor="white", linewidth=2),
           textprops=dict(fontsize=11, color=NEUTRAL["800"]),
           pctdistance=0.83)
    ax.text(0, 0.1, "62%", ha="center", va="center",
            fontsize=32, fontweight="bold", color=PRIMARY_DARKER)
    ax.text(0, -0.18, "完整接種率", ha="center", va="center",
            fontsize=11, color=NEUTRAL["600"])
    ax.set_title("確診者疫苗接種狀態（甜甜圈圖：中心強調主要數字）", loc="left")
    save(fig, "05b-donut-with-center")


# ============== 06. 散佈／泡泡圖 ==============
def scatter_chart_examples():
    print("[06] Scatter chart...")

    # A. 散佈圖：疫苗接種率 vs. 重症率
    np.random.seed(7)
    vax_rate = np.array([45, 52, 58, 62, 65, 68, 72, 75, 78, 82,
                         85, 87, 89, 91, 93, 95, 88, 70, 60, 50])
    sev_rate = 12 - vax_rate * 0.10 + np.random.randn(20) * 0.6

    fig, ax = plt.subplots(figsize=(7.5, 5))
    ax.grid(True, axis="both")  # 散佈圖兩軸皆連續,需雙向格線
    ax.scatter(vax_rate, sev_rate, s=90, color=PRIMARY,
               alpha=0.75, edgecolors=PRIMARY_DARK, linewidths=1.2)
    # 趨勢線
    z = np.polyfit(vax_rate, sev_rate, 1)
    p = np.poly1d(z)
    x_line = np.linspace(vax_rate.min(), vax_rate.max(), 50)
    ax.plot(x_line, p(x_line), color=NEUTRAL["400"], linewidth=1.5,
            linestyle="--", label=f"趨勢線 (r = -0.91)")
    ax.set_xlabel("疫苗完整接種率（%）")
    ax.set_ylabel("重症發生率（每千例）")
    ax.set_title("接種率與重症率的相關性（各縣市散佈圖）", loc="left")
    ax.legend(loc="upper right")
    save(fig, "06a-scatter-correlation")

    # B. 泡泡圖（第三維度：人口規模）
    np.random.seed(11)
    cities_n = ["新北", "臺北", "桃園", "臺中", "臺南", "高雄",
                "新竹", "彰化", "雲林", "嘉義"]
    vax_b = [88, 92, 85, 82, 78, 80, 90, 76, 70, 73]
    sev_b = [2.8, 2.1, 3.6, 4.2, 5.1, 4.5, 2.5, 5.8, 6.8, 6.0]
    pop_b = [400, 270, 230, 280, 188, 275, 45, 125, 67, 50]  # 萬人

    fig, ax = plt.subplots(figsize=(8.5, 5))
    ax.grid(True, axis="both")  # 兩軸皆連續
    sizes_b = [p * 4 for p in pop_b]
    sc = ax.scatter(vax_b, sev_b, s=sizes_b, color=PRIMARY,
                    alpha=0.55, edgecolors=PRIMARY_DARK, linewidths=1.2)
    for i, c in enumerate(cities_n):
        ax.annotate(c, (vax_b[i], sev_b[i]),
                    fontsize=9, color=NEUTRAL["800"],
                    ha="center", va="center", fontweight="bold")
    ax.set_xlabel("疫苗完整接種率（%）")
    ax.set_ylabel("重症發生率（每千例）")
    ax.set_title("各縣市接種率、重症率、人口規模（泡泡大小 = 人口）", loc="left")
    # 圖例：泡泡大小說明
    for ref_size, label in [(50, "50 萬人"), (200, "200 萬人"), (400, "400 萬人")]:
        ax.scatter([], [], s=ref_size*4, color=PRIMARY, alpha=0.55,
                   edgecolors=PRIMARY_DARK, label=label)
    ax.legend(loc="upper right", title="人口規模", labelspacing=1.5, borderpad=1)
    save(fig, "06b-bubble-3rd-dimension")


# ============== 07. 直方圖／盒鬚圖 ==============
def histogram_boxplot_examples():
    print("[07] Histogram / Boxplot...")

    np.random.seed(33)

    # A. 直方圖：年齡分布
    fig, ax = plt.subplots(figsize=(8, 4.5))
    ages_data = np.concatenate([
        np.random.normal(35, 12, 800),
        np.random.normal(65, 8, 400)
    ])
    ages_data = ages_data[(ages_data >= 0) & (ages_data <= 100)]
    ax.hist(ages_data, bins=25, color=PRIMARY,
            edgecolor="white", linewidth=1)
    median = np.median(ages_data)
    ax.axvline(median, color=ACCENT["terracotta"], linewidth=2,
               linestyle="--", label=f"中位數 = {median:.0f} 歲")
    ax.set_xlabel("年齡")
    ax.set_ylabel("人數")
    ax.set_title("確診者年齡分布（直方圖）", loc="left")
    ax.legend(loc="upper right")
    save(fig, "07a-histogram")

    # B. 盒鬚圖：跨縣市住院天數分布
    fig, ax = plt.subplots(figsize=(8, 4.5))
    np.random.seed(101)
    data_box = [
        np.random.gamma(2.5, 2.5, 200),
        np.random.gamma(3.0, 2.2, 200),
        np.random.gamma(2.8, 2.8, 200),
        np.random.gamma(3.5, 2.4, 200),
        np.random.gamma(3.2, 3.0, 200),
        np.random.gamma(4.0, 2.6, 200),
    ]
    labels_box = ["北區", "桃竹苗", "中區", "雲嘉南", "高屏", "東區"]
    bp = ax.boxplot(data_box, labels=labels_box, patch_artist=True,
                    widths=0.55,
                    medianprops=dict(color=PRIMARY_DARKER, linewidth=2),
                    flierprops=dict(marker="o", markersize=4,
                                    markerfacecolor=NEUTRAL["400"],
                                    markeredgecolor="none", alpha=0.5))
    for patch in bp["boxes"]:
        patch.set_facecolor(PRIMARY)
        patch.set_alpha(0.7)
        patch.set_edgecolor(PRIMARY_DARK)
    for whisker in bp["whiskers"]:
        whisker.set_color(PRIMARY_DARK)
    for cap in bp["caps"]:
        cap.set_color(PRIMARY_DARK)
    ax.set_ylabel("住院天數")
    ax.set_title("各區域確診者住院天數分布（盒鬚圖）", loc="left")
    save(fig, "07b-boxplot")


# ============== 08. 人口金字塔 ==============
def pyramid_chart_examples():
    print("[08] Population pyramid...")
    fig, ax = plt.subplots(figsize=(8, 5.5))
    ages_p = ["0-9", "10-19", "20-29", "30-39", "40-49",
              "50-59", "60-69", "70-79", "80+"]
    male   = [12, 18, 22, 24, 28, 30, 26, 18, 10]
    female = [11, 17, 24, 26, 29, 31, 28, 22, 14]

    y = np.arange(len(ages_p))
    ax.barh(y, [-v for v in male], color=PRIMARY, height=0.75,
            label="男性", edgecolor="white", linewidth=0.5)
    ax.barh(y, female, color=CATEGORICAL[1], height=0.75,
            label="女性", edgecolor="white", linewidth=0.5)
    ax.set_yticks(y)
    ax.set_yticklabels(ages_p)
    # X 軸顯示絕對值,刻度為 0, 10, 20, 30
    ax.set_xticks([-30, -20, -10, 0, 10, 20, 30])
    ax.set_xticklabels(["30", "20", "10", "0", "10", "20", "30"])
    ax.set_xlim(-35, 35)
    ax.set_xlabel("確診人數（千人）")
    ax.set_title("確診者年齡 × 性別分布（人口金字塔）", loc="left")
    ax.axvline(0, color=NEUTRAL["400"], linewidth=1)
    ax.legend(loc="upper right")
    # 在 X 軸下方標註左右兩側
    ax.text(-17, -1.3, "← 男性", ha="center", fontsize=10,
            color=PRIMARY_DARK, fontweight="bold")
    ax.text(17, -1.3, "女性 →", ha="center", fontsize=10,
            color=CATEGORICAL[1], fontweight="bold")
    save(fig, "08-pyramid")


# ============== 09. 面量圖（熱力圖代替）==============
def choropleth_examples():
    print("[09] Choropleth (heatmap proxy)...")

    # 由於沒有 GeoJSON,用熱力圖示意「縣市 × 月份」的二維面量
    from matplotlib.colors import LinearSegmentedColormap

    cmap = LinearSegmentedColormap.from_list("epi_seq", SEQUENTIAL, N=256)

    np.random.seed(55)
    cities_c = ["新北", "臺北", "桃園", "臺中", "臺南", "高雄",
                "新竹", "基隆", "彰化", "屏東"]
    months_c = ["1月", "2月", "3月", "4月", "5月",
                "6月", "7月", "8月", "9月", "10月", "11月", "12月"]
    data_c = np.random.randint(50, 900, size=(10, 12)).astype(float)
    data_c[:, 6:9] *= 1.5  # 夏季高峰
    data_c[:, 11] *= 1.3   # 年底反彈

    fig, ax = plt.subplots(figsize=(9.5, 5))
    im = ax.imshow(data_c, cmap=cmap, aspect="auto")
    ax.set_xticks(np.arange(len(months_c)))
    ax.set_yticks(np.arange(len(cities_c)))
    ax.set_xticklabels(months_c)
    ax.set_yticklabels(cities_c)
    ax.set_title("各縣市每月每 10 萬人口發生率（面量熱力圖）", loc="left")
    cbar = fig.colorbar(im, ax=ax, shrink=0.8)
    cbar.set_label("發生率", fontsize=10, color=NEUTRAL["700"])
    cbar.ax.tick_params(labelsize=9)

    # 軸線與網格清理
    ax.grid(False)
    ax.set_xticks(np.arange(len(months_c)+1) - 0.5, minor=True)
    ax.set_yticks(np.arange(len(cities_c)+1) - 0.5, minor=True)
    ax.tick_params(which="minor", size=0)
    save(fig, "09-choropleth-heatmap")


# ============== 10. 單色使用 ==============
def monochrome_examples():
    print("[10] Monochrome usage...")

    # A. 單色堆疊長條：年齡 × 嚴重度（嚴重度有自然順序,用色階）
    fig, ax = plt.subplots(figsize=(9, 4.5))
    ages = ["0-9", "10-19", "20-39", "40-59", "60-69", "70-79", "80+"]
    mild = [78, 85, 89, 82, 70, 55, 38]
    mod  = [18, 13,  9, 14, 22, 32, 42]
    sev  = [ 4,  2,  2,  4,  8, 13, 20]

    colors_3 = MONOCHROME["scale_3"]
    ax.bar(ages, mild, color=colors_3[0], width=0.6, label="輕症",
           edgecolor="white", linewidth=0.5)
    ax.bar(ages, mod, bottom=mild, color=colors_3[1], width=0.6, label="中症",
           edgecolor="white", linewidth=0.5)
    bot3 = [a+b for a, b in zip(mild, mod)]
    ax.bar(ages, sev, bottom=bot3, color=colors_3[2], width=0.6, label="重症",
           edgecolor="white", linewidth=0.5)
    ax.set_xlabel("年齡層")
    ax.set_ylabel("比例（%）")
    ax.set_ylim(0, 100)
    ax.set_title("年齡層 × 嚴重度（單色堆疊;嚴重度為序數,色階反映程度）",
                 loc="left")
    ax.legend(loc="upper left", ncol=3)
    save(fig, "10a-mono-stacked-severity")

    # B. 單色多折線：歷次波次比較（焦點為當前波,最深色）
    fig, ax = plt.subplots(figsize=(9, 4.5))
    days = np.arange(1, 31)
    np.random.seed(0)
    waves = {
        "2021 (第一波)": [120,180,260,380,520,720,980,1240,1580,1820,
                       1960,1880,1740,1520,1280,1040,820,640,490,380,
                       290,220,170,130,100,80,65,52,42,35],
        "2022 (第二波)": [180,290,420,640,920,1280,1720,2180,2640,3020,
                       3280,3340,3180,2860,2440,1980,1560,1180,890,680,
                       510,390,290,220,170,130,100,80,62,48],
        "2023 (第三波)": [200,310,460,700,1020,1420,1900,2400,2920,3340,
                       3640,3700,3520,3160,2680,2180,1720,1300,980,750,
                       560,430,320,240,180,140,108,82,62,48],
        "2024 (本波)":   [240,380,560,820,1180,1620,2180,2840,3520,4180,
                       4720,5040,5180,5040,4640,4080,3420,2780,2210,1740,
                       1360,1050,810,620,470,360,275,210,160,120],
    }
    # 4 序列遞進色階,最後一條(當前)最深
    mono4 = MONOCHROME["scale_4"]
    for (label, vals), c in zip(waves.items(), mono4):
        is_current = "本波" in label
        ax.plot(days, vals, color=c,
                linewidth=3 if is_current else 1.8,
                label=label,
                marker="o" if is_current else None,
                markersize=4 if is_current else 0,
                markevery=5)
    ax.set_xlabel("該波相對日")
    ax.set_ylabel("每日新增")
    ax.set_title("歷次波次比較（單色折線;當前波最深最粗）", loc="left")
    ax.legend(loc="upper right")
    save(fig, "10b-mono-line-waves")

    # C. 單色堆疊區域：疫苗 1/2/3 劑（同主題,劑次有自然順序）
    from datetime import date
    fig, ax = plt.subplots(figsize=(8.5, 4.5))
    months_date = [date(2025, m, 1) for m in range(1, 13)]
    dose1 = [42, 58, 71, 79, 84, 87, 89, 91, 92, 93, 94, 94]
    dose2 = [28, 42, 56, 67, 74, 79, 83, 86, 88, 89, 90, 91]
    dose3 = [ 8, 18, 28, 38, 46, 53, 59, 64, 68, 72, 75, 77]

    mono3 = MONOCHROME["scale_3"]
    # 由淺到深疊（最大量在下、最少量在上）
    ax.fill_between(months_date, 0, dose3, color=mono3[2], alpha=0.85,
                    label="第 3 劑")
    ax.fill_between(months_date, dose3, dose2, color=mono3[1], alpha=0.85,
                    label="第 2 劑 (僅算到此)")
    ax.fill_between(months_date, dose2, dose1, color=mono3[0], alpha=0.85,
                    label="第 1 劑 (僅算到此)")
    ax.plot(months_date, dose1, color=PRIMARY_DARKER, linewidth=1.5)
    ax.axhline(90, color=ACCENT["alert"], linewidth=1.5,
               linestyle="--", label="目標 90%")
    ax.set_ylabel("覆蓋率（%）")
    ax.set_ylim(0, 100)
    ax.set_title("疫苗 1/2/3 劑覆蓋率（單色堆疊區域;劑次為序數）", loc="left")
    format_date_axis_monthly(ax)
    ax.legend(loc="lower right", ncol=2)
    save(fig, "10c-mono-area-doses")


# ============== 主執行 ==============
def main():
    print(f"輸出目錄: {OUT_DIR}\n")
    bar_chart_examples()
    line_chart_examples()
    area_chart_examples()
    stacked_chart_examples()
    pie_chart_examples()
    scatter_chart_examples()
    histogram_boxplot_examples()
    pyramid_chart_examples()
    choropleth_examples()
    monochrome_examples()
    print(f"\n✓ 全部完成。輸出於：{OUT_DIR}")


if __name__ == "__main__":
    main()
