"""
quickstart_with_sample_data.py
快速上手範例：從 sample-data 讀取資料 + 套用本指引繪圖

執行方式：
    python quickstart_with_sample_data.py

這個腳本示範如何結合：
- assets/sample-data/ 的範例資料集
- epidemic_palette.py 的色票模組
- 9 個 reference markdown 中描述的規範

輸出 4 張示範圖於 ../assets/examples/quickstart/
"""
import os
import csv
from datetime import datetime, date

import numpy as np
import matplotlib.pyplot as plt

from epidemic_palette import (
    PRIMARY, PRIMARY_DARK, PRIMARY_DARKER,
    CATEGORICAL, LINE_COLORS, ACCENT, NEUTRAL,
    apply_style, centered_ma, hide_y_axis,
    format_date_axis_daily, format_date_axis_monthly,
)

HERE = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(HERE, "..", "assets", "sample-data")
OUT_DIR = os.path.join(HERE, "..", "assets", "examples", "quickstart")
os.makedirs(OUT_DIR, exist_ok=True)

apply_style()


def read_csv_dict(filename):
    """讀取 CSV 為 list of dict（不依賴 pandas）"""
    path = os.path.join(DATA_DIR, filename)
    with open(path, encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def save(fig, name):
    path = os.path.join(OUT_DIR, f"{name}.png")
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  ✓ {name}.png")


# ============== 範例 1：每日新增（從 01-daily-cases.csv）==============
def example_daily_cases():
    """示範：從 CSV 讀資料 → 直條 + 7 日移動平均 + 日期軸"""
    print("[1] 每日新增確診（從 01-daily-cases.csv）")
    rows = read_csv_dict("01-daily-cases.csv")
    dates = [date.fromisoformat(r["date"]) for r in rows]
    cases = [int(r["new_cases"]) for r in rows]
    ma = centered_ma(cases, window=7)

    fig, ax = plt.subplots(figsize=(9, 4.5))
    ax.bar(dates, cases, color=PRIMARY, width=0.75, label="每日新增")
    ax.plot(dates, ma, color=PRIMARY_DARKER, linewidth=2.5,
            label="7 日移動平均")
    ax.set_ylabel("新增確診數")
    ax.set_title("每日新增確診（資料來源：sample-data 01）", loc="left")
    format_date_axis_daily(ax, interval=4)
    ax.legend(loc="upper left")
    save(fig, "qs-01-daily-cases")


# ============== 範例 2：縣市排名（從 04-city-rates.csv）==============
def example_city_ranking():
    """示範：CSV 讀取 → 排序 → 取 Top 10 → 水平長條 + 強調 + 隱藏 X 軸"""
    print("[2] 縣市排名（從 04-city-rates.csv）")
    rows = read_csv_dict("04-city-rates.csv")
    # 由大到小排序,取前 10
    rows_sorted = sorted(rows, key=lambda r: float(r["rate_per_100k"]),
                         reverse=True)[:10]
    # 繪圖時由下到上對應由大到小
    rows_sorted.reverse()

    cities = [r["city"] for r in rows_sorted]
    rates = [float(r["rate_per_100k"]) for r in rows_sorted]
    # 超過 800 標 Terracotta
    colors = [ACCENT["terracotta"] if r >= 800 else PRIMARY for r in rates]

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.barh(cities, rates, color=colors, height=0.7)
    ax.set_title("各縣市每 10 萬人口確診率排名 Top 10", loc="left")
    for i, (c, r) in enumerate(zip(cities, rates)):
        ax.text(r + 15, i, str(int(r)), va="center",
                fontsize=10, color=NEUTRAL["700"])
    ax.set_xlim(0, max(rates) * 1.15)
    # 已有資料標籤,隱藏 X 軸
    ax.tick_params(axis="x", which="both", bottom=False, labelbottom=False)
    ax.set_xlabel("")
    ax.spines["bottom"].set_visible(False)
    ax.grid(False)
    save(fig, "qs-02-city-ranking")


# ============== 範例 3：疫苗覆蓋率（從 06-vaccine-coverage.csv）==============
def example_vaccine_coverage():
    """示範：多序列區域圖 + 目標線 + 月份格式"""
    print("[3] 疫苗累計覆蓋率（從 06-vaccine-coverage.csv）")
    rows = read_csv_dict("06-vaccine-coverage.csv")
    months = [date.fromisoformat(r["month"] + "-01") for r in rows]
    d1 = [int(r["dose_1_pct"]) for r in rows]
    d2 = [int(r["dose_2_pct"]) for r in rows]
    d3 = [int(r["dose_3_pct"]) for r in rows]

    fig, ax = plt.subplots(figsize=(8.5, 4.5))
    ax.fill_between(months, 0, d1, color=PRIMARY, alpha=0.22, label="第 1 劑")
    ax.plot(months, d1, color=LINE_COLORS["primary"], linewidth=2.5)
    ax.fill_between(months, 0, d2, color=CATEGORICAL[1], alpha=0.22,
                    label="第 2 劑")
    ax.plot(months, d2, color=LINE_COLORS["blue"], linewidth=2.5)
    ax.fill_between(months, 0, d3, color=CATEGORICAL[2], alpha=0.22,
                    label="第 3 劑")
    ax.plot(months, d3, color=LINE_COLORS["yellow"], linewidth=2.5)
    ax.axhline(90, color=ACCENT["alert"], linewidth=1.5,
               linestyle="--", label="目標 90%")
    ax.set_ylabel("覆蓋率（%）")
    ax.set_ylim(0, 100)
    ax.set_title("疫苗 1/2/3 劑累計覆蓋率（資料來源：sample-data 06）", loc="left")
    format_date_axis_monthly(ax)
    ax.legend(loc="lower right", ncol=4)
    save(fig, "qs-03-vaccine-coverage")


# ============== 範例 4：區域住院天數盒鬚（從 11-region-stay.csv）==============
def example_region_boxplot():
    """示範：長表格 CSV → groupby → boxplot"""
    print("[4] 區域住院天數盒鬚（從 11-region-stay.csv）")
    rows = read_csv_dict("11-region-stay.csv")
    # groupby region（不依賴 pandas）
    groups = {}
    for r in rows:
        groups.setdefault(r["region"], []).append(float(r["hospital_days"]))
    # 依中位數由小到大排序
    sorted_regions = sorted(groups.keys(), key=lambda r: np.median(groups[r]))
    data = [groups[r] for r in sorted_regions]

    fig, ax = plt.subplots(figsize=(8, 4.5))
    bp = ax.boxplot(data, tick_labels=sorted_regions, patch_artist=True,
                    widths=0.55,
                    medianprops=dict(color=PRIMARY_DARKER, linewidth=2),
                    flierprops=dict(marker="o", markersize=4,
                                    markerfacecolor=NEUTRAL["400"],
                                    markeredgecolor="none", alpha=0.5))
    for patch in bp["boxes"]:
        patch.set_facecolor(PRIMARY)
        patch.set_alpha(0.7)
        patch.set_edgecolor(PRIMARY_DARK)
    for line in bp["whiskers"] + bp["caps"]:
        line.set_color(PRIMARY_DARK)
    ax.set_ylabel("住院天數")
    ax.set_title("各區域住院天數分布（依中位數排序）", loc="left")
    save(fig, "qs-04-region-boxplot")


def main():
    print(f"讀取資料: {DATA_DIR}")
    print(f"輸出圖表: {OUT_DIR}\n")
    example_daily_cases()
    example_city_ranking()
    example_vaccine_coverage()
    example_region_boxplot()
    print(f"\n✓ 完成。請查看 {OUT_DIR}")


if __name__ == "__main__":
    main()
