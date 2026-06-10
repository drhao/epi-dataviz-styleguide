"""生成 6 主色的完整 10 級色階 + 色卡對照 PNG。

策略:
- 50-400(淺階):用 PRIMARY_SCALE 各級的 absolute lightness
  (確保跨類別 300/400 視覺明度一致)
- 500:用該類別 base hex
- 600-900(深階):用「PRIMARY 該級 lightness / PRIMARY 500」比例,
  套到該類別 base lightness(避免 Bronze/Teal 500-600 重疊)
- saturation:用 PRIMARY 該級相對 500 的比例,套到該類別 base saturation
"""
import colorsys
import os
import sys

import matplotlib.pyplot as plt
import matplotlib.patches as patches

sys.path.insert(0, os.path.join(HERE, "..", "skill", "scripts"))
from epidemic_palette import PRIMARY_SCALE


def hex_to_hls(s):
    s = s.lstrip("#")
    r, g, b = (int(s[i:i+2], 16) / 255 for i in (0, 2, 4))
    return colorsys.rgb_to_hls(r, g, b)


def hls_to_hex(h, l, s):
    r, g, b = colorsys.hls_to_rgb(h, l, s)
    return "#{:02X}{:02X}{:02X}".format(
        max(0, min(255, round(r * 255))),
        max(0, min(255, round(g * 255))),
        max(0, min(255, round(b * 255))),
    )


LEVELS = ["50", "100", "200", "300", "400", "500", "600", "700", "800", "900"]
primary_pattern = [hex_to_hls(c) for c in PRIMARY_SCALE]
primary_500_l = primary_pattern[5][1]
primary_500_s = primary_pattern[5][2]

HUES = {
    "sage":    "#739A6D",
    "slate":   "#587A9D",
    "mustard": "#C8A041",
    "teal":    "#49888D",
    "bronze":  "#916E46",
    "plum":    "#955F71",
}

# 淺階 hue shift(度):拉開「米色家族」相近 hue 在淺階的視覺差異
# Mustard 42° + 5 = 47°(更純黃),Bronze 32° - 7 = 25°(更橘棕)
# 兩者淺階 hue diff 從 10° 拉到 ~22°,跟 Tailwind amber vs orange 同等級
LIGHT_HUE_SHIFT = {
    "mustard": +5 / 360,   # 42° → 47°(更純黃)
    "bronze":  -7 / 360,   # 32° → 25°(更橘棕)
    "plum":    -20 / 360,  # 343° → 323°(更紫紅,跟 Bronze 25° 拉開 58° hue diff)
}


# 非 Sage 類別色,50/100 級 lightness 比 PRIMARY 50/100 略低,
# 讓 hue 有表現空間;Sage(PRIMARY_SCALE)維持設計師原值不動
NON_SAGE_LIGHT_OVERRIDE = {
    0: (0.93, 0.50),  # 50:lightness 0.93,sat = base × 0.50
    1: (0.88, 0.62),  # 100:lightness 0.88,sat = base × 0.62
}


def generate_scale(base_hex, name=None):
    h_base, l_base, s_base = hex_to_hls(base_hex)
    light_shift = LIGHT_HUE_SHIFT.get(name, 0)
    scale = []
    for idx, (_, l_p, s_p) in enumerate(primary_pattern):
        if idx == 5:
            scale.append(base_hex.upper())
            continue
        if idx < 5:
            h = (h_base + light_shift) % 1.0
            if idx in NON_SAGE_LIGHT_OVERRIDE:
                # 50/100 級:用 override 拉低 lightness,saturation 直接從 base 算
                l, sat_factor = NON_SAGE_LIGHT_OVERRIDE[idx]
                s = min(1.0, s_base * sat_factor)
            else:
                # 200-400:用 PRIMARY 該級 absolute lightness
                l = l_p
                sat_ratio = s_p / primary_500_s if primary_500_s > 0 else 1
                s = min(1.0, s_base * sat_ratio)
        else:
            # 深階:用相對 ratio,套到 base lightness
            ratio = l_p / primary_500_l if primary_500_l > 0 else 1
            l = l_base * ratio
            h = h_base
            sat_ratio = s_p / primary_500_s if primary_500_s > 0 else 1
            s = min(1.0, s_base * sat_ratio)
        scale.append(hls_to_hex(h, l, s))
    return scale


scales = {
    name: (PRIMARY_SCALE if name == "sage" else generate_scale(hex_val, name))
    for name, hex_val in HUES.items()
}


print("=== 生成的色階 ===\n")
for name in ["slate", "mustard", "teal", "bronze", "plum"]:
    scale = scales[name]
    print(f"{name.upper()}_SCALE = [")
    for i, hex_v in enumerate(scale):
        marker = " ← base" if i == 5 else ""
        print(f'    "{hex_v}",  # {LEVELS[i]}{marker}')
    print("]\n")


# === 色卡對照 PNG ===
fig, axes = plt.subplots(6, 1, figsize=(13, 5.5))
order = ["sage", "slate", "mustard", "teal", "bronze", "plum"]
labels = {
    "sage": "Sage (PRIMARY)",
    "slate": "Slate Blue",
    "mustard": "Mustard",
    "teal": "Teal",
    "bronze": "Bronze",
    "plum": "Plum",
}

for ax, name in zip(axes, order):
    scale = scales[name]
    for i, hex_v in enumerate(scale):
        ax.add_patch(patches.Rectangle((i, 0), 1, 1, facecolor=hex_v,
                                        edgecolor="white", linewidth=1))
        _, l, _ = hex_to_hls(hex_v)
        text_color = "#FFFFFF" if l < 0.55 else "#181B18"
        ax.text(i + 0.5, 0.6, LEVELS[i],
                ha="center", va="center",
                color=text_color, fontsize=10, fontweight="bold")
        ax.text(i + 0.5, 0.3, hex_v,
                ha="center", va="center",
                color=text_color, fontsize=7.5,
                family="monospace")
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 1)
    ax.set_yticks([])
    ax.set_xticks([])
    ax.set_ylabel(labels[name], fontsize=11, fontweight="semibold",
                  rotation=0, ha="right", va="center", labelpad=14)
    for s in ["top", "right", "left", "bottom"]:
        ax.spines[s].set_visible(False)

fig.suptitle("Categorical Scales  6 hues x 10 levels",
             fontsize=14, fontweight="bold", y=0.99, x=0.4)
plt.tight_layout(rect=[0.05, 0, 1, 0.95])
out = os.path.join(HERE, "..", "docs", "examples", "categorical-scales.png")
plt.savefig(out, dpi=140, bbox_inches="tight", facecolor="white")
plt.close()
print(f"\n色卡 PNG: {out}")
