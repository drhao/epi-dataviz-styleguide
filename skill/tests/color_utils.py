"""
color_utils.py
測試用色彩工具函式：對比度計算、色覺障礙模擬、HEX 解析
"""
import re


def hex_to_rgb(hex_str):
    """將 #RRGGBB 轉為 (R, G, B) tuple (0-255)"""
    s = hex_str.lstrip("#")
    if len(s) != 6:
        raise ValueError(f"Invalid HEX: {hex_str}")
    return tuple(int(s[i:i+2], 16) for i in (0, 2, 4))


def is_valid_hex(hex_str):
    """檢查是否為合法的 #RRGGBB 格式"""
    return bool(re.fullmatch(r"#[0-9A-Fa-f]{6}", hex_str))


def relative_luminance(rgb):
    """WCAG 2.1 相對亮度計算 (0..1)"""
    def chan(c):
        c = c / 255.0
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = rgb
    return 0.2126 * chan(r) + 0.7152 * chan(g) + 0.0722 * chan(b)


def contrast_ratio(hex1, hex2):
    """兩色之間的 WCAG 對比度，回傳 1..21 之間的數值"""
    l1 = relative_luminance(hex_to_rgb(hex1))
    l2 = relative_luminance(hex_to_rgb(hex2))
    lighter, darker = max(l1, l2), min(l1, l2)
    return (lighter + 0.05) / (darker + 0.05)


def wcag_level(ratio, is_large_text=False):
    """
    回傳對比度等級: 'AAA', 'AA', 'AA Large', 'FAIL'
    - AAA: 文字 >= 7.0,大字 >= 4.5
    - AA:  文字 >= 4.5,大字 >= 3.0
    - 非文字（圖形元素如折線、長條）: 3.0 即達 AA
    """
    if is_large_text:
        if ratio >= 4.5: return "AAA"
        if ratio >= 3.0: return "AA"
        return "FAIL"
    else:
        if ratio >= 7.0: return "AAA"
        if ratio >= 4.5: return "AA"
        if ratio >= 3.0: return "AA Large"
        return "FAIL"


# === 色覺障礙模擬 ===
# 基於 Brettel et al. (1997) 的線性 LMS 模擬，常用簡化矩陣
# 矩陣對 sRGB 操作 (0..1 範圍)

CVD_MATRICES = {
    # 紅色盲 / 紅弱
    "protanopia": [
        [0.567, 0.433, 0.000],
        [0.558, 0.442, 0.000],
        [0.000, 0.242, 0.758],
    ],
    # 綠色盲 / 綠弱（最常見，影響約 6% 男性）
    "deuteranopia": [
        [0.625, 0.375, 0.000],
        [0.700, 0.300, 0.000],
        [0.000, 0.300, 0.700],
    ],
    # 藍色盲（罕見）
    "tritanopia": [
        [0.950, 0.050, 0.000],
        [0.000, 0.433, 0.567],
        [0.000, 0.475, 0.525],
    ],
}


def srgb_to_linear(c):
    c = c / 255.0
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def linear_to_srgb(c):
    c = max(0.0, min(1.0, c))
    v = c * 12.92 if c <= 0.0031308 else 1.055 * (c ** (1/2.4)) - 0.055
    return int(round(max(0.0, min(1.0, v)) * 255))


def simulate_cvd(hex_str, cvd_type):
    """模擬色覺障礙看到的顏色，回傳新的 HEX"""
    if cvd_type not in CVD_MATRICES:
        raise ValueError(f"Unknown CVD type: {cvd_type}")
    m = CVD_MATRICES[cvd_type]
    r, g, b = hex_to_rgb(hex_str)
    rl, gl, bl = srgb_to_linear(r), srgb_to_linear(g), srgb_to_linear(b)
    nr = m[0][0]*rl + m[0][1]*gl + m[0][2]*bl
    ng = m[1][0]*rl + m[1][1]*gl + m[1][2]*bl
    nb = m[2][0]*rl + m[2][1]*gl + m[2][2]*bl
    return "#{:02X}{:02X}{:02X}".format(
        linear_to_srgb(nr), linear_to_srgb(ng), linear_to_srgb(nb))


def color_distance(hex1, hex2):
    """
    計算兩色感知距離（CIE76 簡化，於 sRGB 線性空間計算歐氏距離）
    回傳 0..~441 (越大越能區分)
    """
    r1, g1, b1 = hex_to_rgb(hex1)
    r2, g2, b2 = hex_to_rgb(hex2)
    return ((r1-r2)**2 + (g1-g2)**2 + (b1-b2)**2) ** 0.5
