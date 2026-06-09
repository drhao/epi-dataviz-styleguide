"""generate_dont_vs_do.py
Do/Don't 對照範例庫(教學用,L2/L3 補充範例)。

每張 PNG 為「左 ✗ DON'T + 右 ✓ DO」並排對照,對應既有規範條目。

執行方式(從 repo 根目錄):
    python3 skill/scripts/generate_dont_vs_do.py

輸出至 skill/assets/examples/dont-vs-do/(獨立於主例集)。
"""
import os
import sys
import numpy as np
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from epidemic_palette import (  # noqa: E402
    PRIMARY, PRIMARY_DARK, PRIMARY_DARKER, PRIMARY_LIGHT,
    CATEGORICAL, MONOCHROME, LINE_COLORS, ACCENT, NEUTRAL,
    apply_style,
)

apply_style()

OUT_DIR = os.path.join(HERE, "..", "assets", "examples", "dont-vs-do")
os.makedirs(OUT_DIR, exist_ok=True)


# ============== 共用 helpers ==============

def title_dont(ax, text):
    ax.set_title(f"✗ DON'T  {text}", loc="left",
                 color=ACCENT["alert"], fontsize=11, fontweight="semibold")


def title_do(ax, text):
    ax.set_title(f"✓ DO  {text}", loc="left",
                 color=PRIMARY_DARK, fontsize=11, fontweight="semibold")


def save_pair(fig, name):
    out = os.path.join(OUT_DIR, name + ".png")
    plt.savefig(out, dpi=150, bbox_inches="tight", facecolor="white")
    plt.close()
    print(f"  ✓ {name}.png")


def chartjunk(ax):
    """在 ax 上加多餘裝飾(框線、格線),供 DON'T 使用 ── 反向覆寫 apply_style()"""
    for s in ["top", "right", "left", "bottom"]:
        ax.spines[s].set_visible(True)
        ax.spines[s].set_linewidth(1.5)
        ax.spines[s].set_edgecolor(NEUTRAL["700"])
    ax.grid(True, which="major", axis="both",
            color=NEUTRAL["400"], linewidth=0.8, linestyle="-")
    ax.set_facecolor("#F0F0F0")


# ============== 01 · Y 軸截斷 ==============
def pair_01_truncated_yaxis():
    cats = ["教育", "社福", "經發", "環保", "交通", "文化"]
    vals = [98, 92, 105, 87, 78, 95]
    fig, (a, b) = plt.subplots(1, 2, figsize=(12, 4.5))

    a.bar(cats, vals, color=PRIMARY, width=0.6)
    a.set_ylim(70, 115)
    title_dont(a, "Y 軸從 70 開始,把差異視覺放大")
    a.set_ylabel("執行率 (%)")

    b.bar(cats, vals, color=PRIMARY, width=0.6)
    b.set_ylim(0, 120)
    title_do(b, "Y 軸從零,真實呈現比例(差異其實不大)")
    b.set_ylabel("執行率 (%)")

    fig.suptitle("01 · 直條圖 Y 軸必須從零", x=0.05, ha="left",
                 fontsize=13, fontweight=700)
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    save_pair(fig, "01-truncated-yaxis")


# ============== 02 · 折線都用紅色 ==============
def pair_02_red_as_categorical():
    weeks = np.arange(1, 21)
    np.random.seed(2)
    series_a = 200 + np.cumsum(np.random.randn(20) * 15) + 80
    series_b = 180 + np.cumsum(np.random.randn(20) * 12) + 60
    series_c = 220 + np.cumsum(np.random.randn(20) * 18) + 100

    fig, (a, b) = plt.subplots(1, 2, figsize=(12, 4.5))

    # DON'T:三條都用紅色家族
    a.plot(weeks, series_a, color=ACCENT["alert"], linewidth=2.5, label="A 區")
    a.plot(weeks, series_b, color=ACCENT["terracotta"], linewidth=2.5, label="B 區")
    a.plot(weeks, series_c, color=ACCENT["clay"], linewidth=2.5, label="C 區")
    a.set_ylabel("確診率 (每 10 萬)")
    a.legend(loc="upper left", fontsize=9)
    title_dont(a, "三條折線都用紅色家族(全部都像警示)")

    # DO:Pattern B 類別配色(綠藍黃加深版)
    b.plot(weeks, series_a, color=LINE_COLORS["primary"], linewidth=2.5, label="A 區")
    b.plot(weeks, series_b, color=LINE_COLORS["blue"], linewidth=2.5, label="B 區")
    b.plot(weeks, series_c, color=LINE_COLORS["yellow"], linewidth=2.5, label="C 區")
    b.set_ylabel("確診率 (每 10 萬)")
    b.legend(loc="upper left", fontsize=9)
    title_do(b, "Pattern B 類別配色(綠/藍/黃 加深版)")

    fig.suptitle("02 · 紅色僅用於警示,不可作為一般類別色",
                 x=0.05, ha="left", fontsize=13, fontweight=700)
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    save_pair(fig, "02-red-as-categorical")


# ============== 03 · 每根長條不同色 ==============
def pair_03_rainbow_bars():
    cats = ["教育", "社福", "經發", "環保", "交通", "文化"]
    vals = [98, 92, 105, 87, 78, 95]
    focus_idx = 4  # 交通是焦點(最低)
    fig, (a, b) = plt.subplots(1, 2, figsize=(12, 4.5))

    # DON'T:每根不同色
    rainbow = ["#E74C3C", "#F39C12", "#F1C40F", "#2ECC71", "#3498DB",
               "#9B59B6"]
    a.bar(cats, vals, color=rainbow, width=0.6)
    title_dont(a, "每根長條用不同顏色(顏色無資訊意義)")
    a.set_ylabel("執行率 (%)")
    a.set_ylim(0, 120)

    # DO:Pattern A 凸顯焦點
    colors_b = [NEUTRAL["400"] if i != focus_idx else ACCENT["alert"]
                for i in range(len(cats))]
    b.bar(cats, vals, color=colors_b, width=0.6)
    title_do(b, "Pattern A 中性 + 焦點凸顯(交通最低,紅色警示)")
    b.set_ylabel("執行率 (%)")
    b.set_ylim(0, 120)

    fig.suptitle("03 · 顏色應傳達資訊;Pattern A 用中性背景 + 主色/警示色凸顯焦點",
                 x=0.05, ha="left", fontsize=13, fontweight=700)
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    save_pair(fig, "03-rainbow-bars")


# ============== 04 · 過度裝飾圓餅 ==============
def pair_04_decorated_pie():
    labels = ["A", "B", "C", "D"]
    sizes = [38, 28, 22, 12]
    fig, (a, b) = plt.subplots(1, 2, figsize=(12, 5))

    # DON'T:shadow + explode + 不必要邊框
    a.pie(sizes, labels=labels, autopct="%1.0f%%",
          colors=["#E74C3C", "#F39C12", "#3498DB", "#9B59B6"],
          shadow=True, explode=(0.08, 0.05, 0.05, 0.05), startangle=45,
          wedgeprops={"edgecolor": "white", "linewidth": 2})
    title_dont(a, "陰影 + explode + 鮮豔色 + 起始角隨意")

    # DO:平面 2D + Pattern B + 直接標籤
    wedges, texts, autotexts = b.pie(
        sizes, labels=labels, autopct="%1.0f%%",
        colors=CATEGORICAL[:4],
        startangle=90, counterclock=False,
        wedgeprops={"edgecolor": "white", "linewidth": 1.5},
    )
    for at in autotexts:
        at.set_color("white")
        at.set_fontweight("semibold")
    title_do(b, "平面 2D · Pattern B · 從 12 點順時針 · 直接標籤")

    fig.suptitle("04 · 圓餅圖不用 3D/陰影/explode;類別 ≤ 5 + 直接標籤",
                 x=0.05, ha="left", fontsize=13, fontweight=700)
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    save_pair(fig, "04-decorated-pie")


# ============== 05 · 圓餅 9 切片 vs 排序橫條 ==============
def pair_05_too_many_pie_slices():
    variants = ["JN.1", "KP.2", "KP.3", "LB.1", "JN.4", "KP.1",
                "JN.5", "KP.4", "其他"]
    counts = [28, 22, 14, 11, 9, 7, 4, 3, 2]
    fig, (a, b) = plt.subplots(1, 2, figsize=(13, 5))

    # DON'T:9 切片圓餅(切片太多看不清)
    a.pie(counts, labels=variants, autopct="%1.0f%%",
          colors=CATEGORICAL + [NEUTRAL["400"]] * 3,
          startangle=90, counterclock=False,
          textprops={"fontsize": 9},
          wedgeprops={"edgecolor": "white", "linewidth": 1})
    title_dont(a, "圓餅 9 切片(類別 > 5,切片太碎讀不出比例)")

    # DO:橫條排序由大到小
    order = np.argsort(counts)[::-1]
    sorted_v = [variants[i] for i in order]
    sorted_c = [counts[i] for i in order]
    bar_colors = [PRIMARY if i < 2 else NEUTRAL["400"] for i in range(len(sorted_v))]
    b.barh(sorted_v[::-1], sorted_c[::-1], color=bar_colors[::-1], height=0.6)
    title_do(b, "橫條排序由大到小,主流(前 2 名)用主色凸顯")
    b.set_xlabel("占比 (%)")

    fig.suptitle("05 · 類別 > 5 時改用排序橫條圖,讀者用「長度」比較比「角度」準確",
                 x=0.02, ha="left", fontsize=13, fontweight=700)
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    save_pair(fig, "05-too-many-pie-slices")


# ============== 06 · 22 縣市疊一張 ==============
def pair_06_spaghetti_vs_small_multiples():
    np.random.seed(42)
    cities = [
        "臺北", "新北", "桃園", "臺中", "臺南", "高雄", "基隆", "新竹市",
        "嘉義市", "新竹縣", "苗栗", "彰化", "南投", "雲林", "嘉義縣",
        "屏東", "宜蘭", "花蓮", "臺東", "澎湖", "金門", "連江",
    ]
    weeks = np.arange(1, 25)
    curves = []
    for i in range(22):
        base = 100 * np.sin((weeks + i % 6) * np.pi / 12) + 150
        curves.append(
            (base * (0.6 + 0.5 * np.random.rand())
             + np.random.randn(len(weeks)) * 12).clip(min=0)
        )

    fig = plt.figure(figsize=(15, 6.5))

    # DON'T:22 條折線疊一張(spaghetti)
    ax_a = plt.subplot(1, 2, 1)
    rainbow22 = plt.cm.tab20(np.linspace(0, 1, 22))
    for c, color in zip(curves, rainbow22):
        ax_a.plot(weeks, c, color=color, linewidth=1.2, alpha=0.8)
    ax_a.set_xlabel("Week")
    ax_a.set_ylabel("Rate")
    title_dont(ax_a, "22 條折線疊一張(讀者完全分不出哪條是哪縣市)")

    # DO:M2 small multiples(4×6 mini grid in right half)
    gs = fig.add_gridspec(4, 12, left=0.55, right=0.99,
                           top=0.86, bottom=0.10,
                           wspace=0.15, hspace=0.4)
    focus_idx = 0
    for i in range(22):
        row = i // 6
        col = i % 6
        ax = fig.add_subplot(gs[row, col])
        is_focus = (i == focus_idx)
        color = PRIMARY if is_focus else NEUTRAL["300"]
        ax.plot(weeks, curves[i], color=color,
                linewidth=1.5 if is_focus else 1.0)
        ax.set_title(cities[i] + ("★" if is_focus else ""),
                     loc="left",
                     color=PRIMARY if is_focus else NEUTRAL["700"],
                     fontsize=7)
        ax.set_xticks([])
        ax.set_yticks([])
        for s in ["top", "right"]:
            ax.spines[s].set_visible(False)

    # title overlay for DO half
    fig.text(0.55, 0.92,
             "✓ DO  M2 small multiples(臺北為焦點 PRIMARY,其餘 N300)",
             color=PRIMARY_DARK, fontsize=11, fontweight="semibold")

    fig.suptitle("06 · 多 panels(>= 4)同指標跨類別比較,改用 M2 small multiples",
                 x=0.02, ha="left", fontsize=13, fontweight=700)
    save_pair(fig, "06-spaghetti-vs-small-multiples")


# ============== 07 · 多餘框線/格線 vs 極簡 ==============
def pair_07_chartjunk_vs_minimal():
    cats = ["1月", "2月", "3月", "4月", "5月", "6月"]
    vals = [120, 145, 180, 165, 200, 220]
    fig, (a, b) = plt.subplots(1, 2, figsize=(12, 4.5))

    # DON'T:全邊框 + 雙向格線 + 灰底
    a.bar(cats, vals, color=PRIMARY, width=0.6,
          edgecolor=NEUTRAL["800"], linewidth=1.5)
    chartjunk(a)
    a.set_ylabel("確診人次", color=NEUTRAL["800"])
    title_dont(a, "四面邊框 + 雙向格線 + 灰底(chartjunk)")

    # DO:apply_style() 預設 ── 無頂右框 + 僅水平格線
    b.bar(cats, vals, color=PRIMARY, width=0.6)
    b.set_ylabel("確診人次")
    title_do(b, "移除頂右邊框 + 僅顯示水平格線(讀數方向)")

    fig.suptitle("07 · 移除不傳達資訊的裝飾(SKILL.md §4.1.5 grid / §4.1.6 spines)",
                 x=0.05, ha="left", fontsize=13, fontweight=700)
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    save_pair(fig, "07-chartjunk-vs-minimal")


# ============== 08 · 字典序 vs 數值排序 ==============
def pair_08_sort_by_name_vs_value():
    # 各縣市發生率(虛構)
    data = {
        "臺北": 235, "新北": 312, "桃園": 287, "臺中": 198,
        "臺南": 145, "高雄": 178, "基隆": 95, "新竹": 168,
        "嘉義": 88, "苗栗": 76, "宜蘭": 112,
    }

    fig, (a, b) = plt.subplots(1, 2, figsize=(13, 5))

    # DON'T:按字典序(即建檔順序,讀者無法看 ranking)
    names = list(data.keys())
    vals = [data[n] for n in names]
    a.barh(names[::-1], vals[::-1], color=PRIMARY, height=0.65)
    a.set_xlabel("發生率 (每 10 萬)")
    title_dont(a, "按行政區編號排序(無 ranking 訊息,讀者要自己比)")

    # DO:按發生率排序由大到小
    sorted_items = sorted(data.items(), key=lambda x: x[1], reverse=True)
    s_names = [n for n, _ in sorted_items]
    s_vals = [v for _, v in sorted_items]
    # 前 3 名用主色強調
    colors = [PRIMARY if i < 3 else NEUTRAL["400"] for i in range(len(s_names))]
    b.barh(s_names[::-1], s_vals[::-1], color=colors[::-1], height=0.65)
    b.set_xlabel("發生率 (每 10 萬)")
    title_do(b, "按發生率排序由大到小,前 3 名主色凸顯")

    fig.suptitle("08 · 排名類直條圖必須按數值排序(01-bar-chart 規則 4)",
                 x=0.02, ha="left", fontsize=13, fontweight=700)
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    save_pair(fig, "08-sort-by-name-vs-value")


# ============== 主執行 ==============

def main():
    print(f"輸出目錄: {OUT_DIR}\n")
    pair_01_truncated_yaxis()
    pair_02_red_as_categorical()
    pair_03_rainbow_bars()
    pair_04_decorated_pie()
    pair_05_too_many_pie_slices()
    pair_06_spaghetti_vs_small_multiples()
    pair_07_chartjunk_vs_minimal()
    pair_08_sort_by_name_vs_value()
    print(f"\n✓ 全部完成(8 對),輸出於:{OUT_DIR}")


if __name__ == "__main__":
    main()
