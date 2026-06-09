"""m1_uncertainty_examples.py
RFC 2026-06-01 / M1 不確定性視覺化 modifier 的 Pilot 階段範例。

執行方式(從 repo 根目錄):
    python3 skill/assets/examples/_drafts/m1_uncertainty_examples.py

輸出:
    m1-uncertainty-A-trailing-band.png        時序預測 + 漸層帶
    m1-uncertainty-B-errorbar-asymmetric.png  少量類別 + 不對稱 error bar

對應規範:skill/references/M1-uncertainty-modifier.md(status: draft)
"""
import os
import sys

import numpy as np
import matplotlib.pyplot as plt

# 加入 skill/scripts 路徑以 import epidemic_palette
HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPTS = os.path.abspath(os.path.join(HERE, "..", "..", "..", "scripts"))
sys.path.insert(0, SCRIPTS)

from epidemic_palette import (  # noqa: E402
    PRIMARY, PRIMARY_LIGHT, PRIMARY_DARKER,
    LINE_COLORS, NEUTRAL,
    apply_style,
)

apply_style()
OUT_DIR = HERE


# ============== Example A: 時序預測 漸層帶 ==============
def example_a_trailing_band():
    """類流感就診人次預測 ── 過去觀測 + 4 週預測區間"""
    # 過去 12 週觀測(類流感週期性 + 雜訊)
    weeks_past = np.arange(1, 13)
    np.random.seed(7)
    seasonal = 320 + 180 * np.sin((weeks_past - 1) * np.pi / 7.5)
    obs = (seasonal + np.random.randn(12) * 25).clip(min=0).astype(int)

    # 未來 4 週預測 + 區間(銜接 W12)
    weeks_future_x = np.array([12, 13, 14, 15, 16])
    point_est = np.array([obs[-1], 520, 580, 640, 690])
    se_50 = np.array([0, 35, 55, 75, 95])
    se_95 = np.array([0, 85, 130, 175, 220])
    lower_95 = point_est - se_95
    upper_95 = point_est + se_95
    lower_50 = point_est - se_50
    upper_50 = point_est + se_50

    fig, ax = plt.subplots(figsize=(9, 4.8))

    # 觀測段:實線
    ax.plot(weeks_past, obs, color=LINE_COLORS["primary"],
            linewidth=2.5, label="觀測值",
            marker="o", markersize=5)

    # 預測段:95% CI 外層
    ax.fill_between(weeks_future_x, lower_95, upper_95,
                    color=PRIMARY_LIGHT, alpha=0.20, label="95% CI")
    # 50% CI 內層
    ax.fill_between(weeks_future_x, lower_50, upper_50,
                    color=PRIMARY_LIGHT, alpha=0.40, label="50% CI")

    # 預測點估計:虛線
    ax.plot(weeks_future_x, point_est,
            color=LINE_COLORS["primary"], linewidth=2.5,
            linestyle=(0, (6, 3)), label="預測點估計",
            marker="o", markersize=5)

    # 預測起點 annotation
    ax.axvline(x=12, color=NEUTRAL["400"], linestyle="--", linewidth=1)
    ax.text(12.15, ax.get_ylim()[1] * 0.95, " 預測起點",
            color=NEUTRAL["600"], fontsize=9, va="top")

    ax.set_xlabel("週次")
    ax.set_ylabel("類流感就診人次")
    ax.set_title("時序預測 · 漸層帶 + 預測虛線",
                 loc="left")
    ax.legend(loc="upper left", fontsize=9, ncol=4)
    ax.set_ylim(bottom=0)

    out = os.path.join(OUT_DIR, "m1-uncertainty-A-trailing-band.png")
    plt.savefig(out, dpi=150, bbox_inches="tight", facecolor="white")
    plt.close()
    print(f"  ✓ {out}")


# ============== Example B: error bar 不對稱 CI ==============
def example_b_errorbar_asymmetric():
    """各年齡組重症率 · 不對稱 95% CI(規則 11 + 13 主場)"""
    ages = ["0-9", "10-39", "40-64", "65-74", "75+"]
    rates = [0.5, 1.2, 3.8, 8.4, 15.2]
    ci_low = [0.3, 0.9, 3.2, 7.2, 13.4]
    ci_high = [0.8, 1.6, 4.5, 9.7, 17.3]

    # 規則 13:不對稱 CI 上下臂分別計算
    errors = [
        [r - l for r, l in zip(rates, ci_low)],
        [h - r for h, r in zip(ci_high, rates)],
    ]

    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.bar(ages, rates, color=PRIMARY, width=0.6)

    # 規則 11:error bar 用 PRIMARY_DARKER
    # 規則 12:capsize=4(matplotlib 建議值)
    ax.errorbar(ages, rates, yerr=errors,
                fmt="none",
                ecolor=PRIMARY_DARKER,
                elinewidth=1.5, capsize=4, capthick=1)

    ax.set_xlabel("年齡組")
    ax.set_ylabel("重症率(%, 95% CI)")
    ax.set_title("少量類別 · error bar(主色更深版,不對稱)",
                 loc="left")
    ax.set_ylim(bottom=0)

    out = os.path.join(OUT_DIR, "m1-uncertainty-B-errorbar-asymmetric.png")
    plt.savefig(out, dpi=150, bbox_inches="tight", facecolor="white")
    plt.close()
    print(f"  ✓ {out}")


if __name__ == "__main__":
    print("生成 M1 不確定性視覺化 Pilot 範例...")
    example_a_trailing_band()
    example_b_errorbar_asymmetric()
    print("\n完成。RFC: docs/rfcs/2026-06-01-uncertainty.md")
