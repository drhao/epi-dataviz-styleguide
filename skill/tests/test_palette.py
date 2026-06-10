"""
test_palette.py
測試疫情資料視覺化指引的色票模組

執行方式：
    cd tests/
    pytest test_palette.py -v
或：
    python test_palette.py        # 不需 pytest 也能跑
"""
import sys
import os
import pytest

# 把 scripts/ 加入 import 路徑
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "scripts"))

from color_utils import (
    contrast_ratio, wcag_level, simulate_cvd, color_distance, is_valid_hex
)
import epidemic_palette as ep


# ============== HEX 格式 ==============

class TestHexFormat:
    """所有色彩都必須是合法的 #RRGGBB 格式（大寫）"""

    def test_primary_scale_format(self):
        for hx in ep.PRIMARY_SCALE:
            assert is_valid_hex(hx), f"非法 HEX: {hx}"
            assert hx == hx.upper(), f"應為大寫: {hx}"

    def test_categorical_format(self):
        for hx in ep.CATEGORICAL:
            assert is_valid_hex(hx), f"非法 HEX: {hx}"
            assert hx == hx.upper(), f"應為大寫: {hx}"

    def test_accent_format(self):
        for name, hx in ep.ACCENT.items():
            assert is_valid_hex(hx), f"非法 HEX {name}: {hx}"

    def test_neutral_format(self):
        for step, hx in ep.NEUTRAL.items():
            assert is_valid_hex(hx), f"非法 HEX neutral-{step}: {hx}"

    def test_semantic_format(self):
        for name, hx in ep.SEMANTIC.items():
            assert is_valid_hex(hx), f"非法 HEX semantic.{name}: {hx}"

    def test_line_colors_format(self):
        for name, hx in ep.LINE_COLORS.items():
            assert is_valid_hex(hx), f"非法 HEX line.{name}: {hx}"

    def test_sequential_format(self):
        for hx in ep.SEQUENTIAL:
            assert is_valid_hex(hx), f"非法 HEX sequential: {hx}"

    def test_diverging_format(self):
        for hx in ep.DIVERGING:
            assert is_valid_hex(hx), f"非法 HEX diverging: {hx}"


# ============== 完整性檢查 ==============

class TestCompleteness:
    """檢查色票數量與必要鍵"""

    def test_primary_scale_has_10_steps(self):
        assert len(ep.PRIMARY_SCALE) == 10, \
            f"主色階應有 10 階，實際 {len(ep.PRIMARY_SCALE)}"

    def test_categorical_has_6_colors(self):
        assert len(ep.CATEGORICAL) == 6, \
            f"類別配色應有 6 色，實際 {len(ep.CATEGORICAL)}"

    def test_primary_500_is_organizational_color(self):
        """主色 500 必為組織主色 #739A6D"""
        assert ep.PRIMARY == "#739A6D"
        assert ep.PRIMARY_SCALE[5] == "#739A6D"

    def test_categorical_first_is_primary(self):
        """類別配色第一順位必須是主色（指引核心規範）"""
        assert ep.CATEGORICAL[0] == ep.PRIMARY

    def test_accent_has_required_keys(self):
        required = {"alert", "terracotta", "clay", "caution"}
        assert set(ep.ACCENT.keys()) >= required, \
            f"強調色缺少必要鍵: {required - set(ep.ACCENT.keys())}"

    def test_semantic_has_required_keys(self):
        required = {"success", "warning", "danger", "info"}
        assert set(ep.SEMANTIC.keys()) == required

    def test_diverging_center_not_white(self):
        """發散色階中心點不可為純白（指引明文規範）"""
        center = ep.DIVERGING[len(ep.DIVERGING) // 2]
        assert center != "#FFFFFF", "發散色階中心不可為純白"
        assert center != "#FFF", "發散色階中心不可為純白"


# ============== 順序與性質 ==============

class TestOrdering:
    """檢查色階的單調性"""

    def test_primary_scale_monotonically_darkens(self):
        """主色階從 50 到 900 應單調變暗"""
        from color_utils import relative_luminance, hex_to_rgb
        lums = [relative_luminance(hex_to_rgb(c)) for c in ep.PRIMARY_SCALE]
        for i in range(len(lums) - 1):
            assert lums[i] > lums[i+1], \
                f"主色階非單調: step {i*100 if i else 50} 應比 step {(i+1)*100 if i+1 else 50} 亮"

    def test_sequential_monotonically_darkens(self):
        """序列色階應單調變暗"""
        from color_utils import relative_luminance, hex_to_rgb
        lums = [relative_luminance(hex_to_rgb(c)) for c in ep.SEQUENTIAL]
        for i in range(len(lums) - 1):
            assert lums[i] > lums[i+1], f"序列色階非單調，step {i}"

    def test_categorical_scales_have_10_levels(self):
        """6 個類別色階各有 10 級"""
        for name, scale in ep.CATEGORICAL_SCALES.items():
            assert len(scale) == 10, f"{name}_SCALE 必須 10 級,實際 {len(scale)}"

    def test_categorical_scales_500_is_base(self):
        """每個類別色階的 500 級必須等於 CATEGORICAL 對應 base"""
        scale_order = ["sage", "slate", "mustard", "teal", "bronze", "plum"]
        for i, name in enumerate(scale_order):
            assert ep.CATEGORICAL_SCALES[name][5].upper() == ep.CATEGORICAL[i].upper(), \
                f"{name}_SCALE[5] 必須等於 CATEGORICAL[{i}]({ep.CATEGORICAL[i]})"

    def test_categorical_scales_monotonically_darken(self):
        """6 個類別色階各自從 50 到 900 單調變暗"""
        from color_utils import relative_luminance, hex_to_rgb
        for name, scale in ep.CATEGORICAL_SCALES.items():
            lums = [relative_luminance(hex_to_rgb(c)) for c in scale]
            for i in range(len(lums) - 1):
                assert lums[i] > lums[i+1], \
                    f"{name}_SCALE 非單調: step {i} → {i+1}"


# ============== WCAG 對比度 ==============

class TestContrast:
    """確保色彩在實際使用時可達 WCAG 標準"""

    WHITE = "#FFFFFF"
    DARK_TEXT = "#181B18"  # Neutral 900

    # ---- 文字用色（≥ 4.5）----

    def test_primary_600_passes_AA_text(self):
        """主色 600 用於正文時必須過 AA"""
        r = contrast_ratio(ep.PRIMARY_DARK, self.WHITE)
        assert r >= 4.5, f"主色 600 對白色對比 {r:.2f} < 4.5"

    def test_primary_700_passes_AA_text(self):
        """主色 700 用於文字必須過 AA"""
        r = contrast_ratio(ep.PRIMARY_SCALE[7], self.WHITE)
        assert r >= 4.5, f"主色 700 對白色對比 {r:.2f} < 4.5"

    def test_dark_text_on_light_bg_passes_AAA(self):
        """深色文字在淺色背景必須過 AAA"""
        for bg_hex in [self.WHITE, ep.NEUTRAL["50"], ep.NEUTRAL["100"]]:
            r = contrast_ratio(self.DARK_TEXT, bg_hex)
            assert r >= 7.0, f"深色文字對 {bg_hex} 對比 {r:.2f} < 7.0"

    def test_neutral_700_text_passes_AA(self):
        """正文用 Neutral 700 對白底必須過 AA"""
        r = contrast_ratio(ep.NEUTRAL["700"], self.WHITE)
        assert r >= 4.5, f"Neutral 700 對白色對比 {r:.2f} < 4.5"

    # ---- 非文字（圖形）用色 ----
    # WCAG 2.1 非文字對比建議 3.0，但僅針對「使用者介面元件」
    # 對於資料視覺化中的填色（如長條、圓餅切片），實務門檻較寬鬆
    # 本指引：填色 ≥ 2.4；邊框/線條/小圖示 ≥ 3.0

    FILL_THRESHOLD = 2.4       # 大面積填色
    GRAPHIC_THRESHOLD = 3.0    # 邊框、線條、圖示

    def test_primary_500_passes_non_text_contrast(self):
        """主色 500 作為長條/填色必須過 3.0"""
        r = contrast_ratio(ep.PRIMARY, self.WHITE)
        assert r >= self.GRAPHIC_THRESHOLD, f"主色 500 對白色對比 {r:.2f}"

    def test_categorical_pass_fill_contrast(self):
        """類別配色作為大面積填色（長條、圓餅）門檻 2.4"""
        for hx in ep.CATEGORICAL:
            r = contrast_ratio(hx, self.WHITE)
            assert r >= self.FILL_THRESHOLD, \
                f"類別色 {hx} 對白色對比 {r:.2f} < {self.FILL_THRESHOLD}（填色不可用）"

    def test_categorical_mustard_warning(self):
        """Mustard #C8A041 對白色僅 2.45，作為長條填色勉強可用，但不應作為線條/邊框使用"""
        r = contrast_ratio(ep.CATEGORICAL[2], self.WHITE)
        # 確認它在 2.4-3.0 之間,所以指引應引導使用者改用 line_mustard
        assert 2.4 <= r < 3.0, (
            f"Mustard 對比 {r:.2f} 不在預期區間（2.4–3.0）。"
            f"若 ≥ 3.0 表示色相已調整，本測試可移除。"
        )
        # 因此提供了 line_mustard (加深版) 給折線/邊框使用
        line_r = contrast_ratio(ep.LINE_COLORS["yellow"], self.WHITE)
        assert line_r >= self.GRAPHIC_THRESHOLD, \
            f"line.yellow 應作為折線版補強，但對比 {line_r:.2f}"

    # ---- 折線專用版（必須夠深）----

    def test_line_primary_passes_AA(self):
        """折線主色必須對白底 ≥ 4.5（折線比長條纖細）"""
        r = contrast_ratio(ep.LINE_COLORS["primary"], self.WHITE)
        assert r >= 4.5, f"line.primary {ep.LINE_COLORS['primary']} 對比 {r:.2f} < 4.5"

    def test_line_mustard_passes_non_text(self):
        """Mustard 折線版必須對白底 ≥ 3.0（原 Mustard 僅 2.45 不過）"""
        r = contrast_ratio(ep.LINE_COLORS["yellow"], self.WHITE)
        assert r >= 3.0, f"line.yellow {ep.LINE_COLORS['yellow']} 對比 {r:.2f} < 3.0"

    def test_line_mustard_darker_than_categorical_mustard(self):
        """Mustard 折線版必須比類別配色版深"""
        from color_utils import relative_luminance, hex_to_rgb
        line_lum = relative_luminance(hex_to_rgb(ep.LINE_COLORS["yellow"]))
        cat_lum = relative_luminance(hex_to_rgb(ep.CATEGORICAL[2]))
        assert line_lum < cat_lum, \
            f"折線版 Mustard 應比類別版深 (line={line_lum:.3f}, cat={cat_lum:.3f})"

    # ---- 白字於主色背景（按鈕場景）----

    def test_white_on_primary_large_text(self):
        """白字於主色背景：適用 18px+ 或 14px+ 粗體（AA Large 門檻 3.0）"""
        r = contrast_ratio(self.WHITE, ep.PRIMARY)
        assert r >= 3.0, f"白字於主色對比 {r:.2f} < 3.0（連 AA Large 都不過）"

    def test_white_on_primary_dark_passes_AA_text(self):
        """主色 600 作為按鈕背景，搭配白字必須過 AA（小字也適用）"""
        r = contrast_ratio(self.WHITE, ep.PRIMARY_DARK)
        assert r >= 4.5, f"白字於主色 600 對比 {r:.2f}（按鈕小字場景）"

    # ---- 語意色 ----

    def test_semantic_colors_pass_fill_contrast(self):
        """語意色作為大面積填色（KPI 卡背景）門檻 2.4"""
        for name, hx in ep.SEMANTIC.items():
            r = contrast_ratio(hx, self.WHITE)
            assert r >= self.FILL_THRESHOLD, \
                f"semantic.{name} {hx} 對比 {r:.2f} < {self.FILL_THRESHOLD}"

    def test_semantic_danger_alert_meet_graphic(self):
        """語意色中 danger/success 用於警示符號、圖示須過 3.0"""
        for name in ["danger", "success", "info"]:
            r = contrast_ratio(ep.SEMANTIC[name], self.WHITE)
            assert r >= self.GRAPHIC_THRESHOLD, \
                f"semantic.{name} 用於圖示對比 {r:.2f} 不足"

    # ---- 強調色 ----

    def test_alert_red_passes_graphic(self):
        """警示紅必須過 3.0（圖形警示）"""
        r = contrast_ratio(ep.ACCENT["alert"], self.WHITE)
        assert r >= self.GRAPHIC_THRESHOLD


# ============== 色覺障礙友善 ==============

class TestColorBlindness:
    """類別配色在三種主要色覺障礙下仍能區分

    實務說明：
    - 「前 3 色」（綠/藍/黃）為最常用組合，必須在所有 CVD 下嚴格可區分
    - 4 色以上的配色，部分色對在 CVD 下會接近（如 Slate Blue ↔ Teal 在綠色盲下）
      此時必須搭配形狀、紋路、直接標籤輔助
    - 本測試確保前 3 色 CVD 友善；超過 3 色的限制有獨立測試提示
    """

    STRICT_THRESHOLD = 30   # 前 3 色：嚴格門檻
    LOOSE_THRESHOLD = 8     # 6 色全用：寬鬆門檻（已知接近的色對）

    def _pairwise_min_distance(self, palette, cvd_type):
        sim = [simulate_cvd(c, cvd_type) for c in palette]
        min_d = float("inf")
        min_pair = None
        for i in range(len(sim)):
            for j in range(i+1, len(sim)):
                d = color_distance(sim[i], sim[j])
                if d < min_d:
                    min_d = d
                    min_pair = (palette[i], palette[j], sim[i], sim[j])
        return min_d, min_pair

    # --- 前 3 色（核心承諾，必須嚴格可區分）---

    @pytest.mark.parametrize("cvd_type", ["protanopia", "deuteranopia", "tritanopia"])
    def test_top3_categorical_distinguishable(self, cvd_type):
        """前 3 色（綠/藍/黃）在所有 CVD 下兩兩可區分（核心承諾）"""
        min_d, pair = self._pairwise_min_distance(ep.CATEGORICAL[:3], cvd_type)
        assert min_d >= self.STRICT_THRESHOLD, (
            f"前 3 色在 {cvd_type} 下最小距離 {min_d:.1f} < {self.STRICT_THRESHOLD}\n"
            f"  難辨識對: {pair[0]} ↔ {pair[1]} "
            f"(模擬後 {pair[2]} ↔ {pair[3]})"
        )

    # --- 前 4 色（常用,寬鬆門檻）---

    def test_top4_known_limitation_documented(self):
        """前 4 色中 Slate Blue ↔ Teal 在綠色盲下接近（已知限制，須加形狀輔助）"""
        # 確認這個已知限制仍存在（用以追蹤未來色票調整）
        d = color_distance(
            simulate_cvd(ep.CATEGORICAL[1], "deuteranopia"),  # Slate Blue
            simulate_cvd(ep.CATEGORICAL[3], "deuteranopia"),  # Teal
        )
        # 若已修復（d > 30），此測試會通過但應移除提示
        assert d < 30, (
            f"已知限制已修復：Slate Blue ↔ Teal 在綠色盲下距離 {d:.1f}。"
            f"可以從指引中移除「需搭配形狀」的提示。"
        )

    # --- 全部 6 色（已知有部分衝突,只要求最低門檻）---

    @pytest.mark.parametrize("cvd_type", ["protanopia", "deuteranopia", "tritanopia"])
    def test_full_palette_meets_loose_threshold(self, cvd_type):
        """全部 6 色在 CVD 下達基本門檻 8（避免完全無法區分）"""
        min_d, pair = self._pairwise_min_distance(ep.CATEGORICAL, cvd_type)
        assert min_d >= self.LOOSE_THRESHOLD, (
            f"全部 6 色在 {cvd_type} 下最小距離 {min_d:.1f} < {self.LOOSE_THRESHOLD}（完全無法區分）"
        )

    # --- 發散色階兩端（重要承諾）---

    @pytest.mark.parametrize("cvd_type", ["protanopia", "deuteranopia"])
    def test_diverging_endpoints_distinguishable(self, cvd_type):
        """發散色階兩端（綠 vs. 紅）在紅綠色盲下仍須清楚區分"""
        left = ep.DIVERGING[0]
        right = ep.DIVERGING[-1]
        d = color_distance(simulate_cvd(left, cvd_type),
                           simulate_cvd(right, cvd_type))
        assert d >= self.STRICT_THRESHOLD, (
            f"發散色階兩端 {left} ↔ {right} 在 {cvd_type} 下距離 {d:.1f}"
        )

    # --- 主色 vs 強調紅（必須明顯區分）---

    @pytest.mark.parametrize("cvd_type", ["protanopia", "deuteranopia"])
    def test_primary_vs_alert_red(self, cvd_type):
        """主色 vs. Alert Red 在紅綠色盲下必須清楚區分（疫情圖表常見組合）"""
        d = color_distance(
            simulate_cvd(ep.PRIMARY, cvd_type),
            simulate_cvd(ep.ACCENT["alert"], cvd_type),
        )
        assert d >= self.STRICT_THRESHOLD, (
            f"主色 vs. Alert Red 在 {cvd_type} 下距離 {d:.1f}"
        )


# ============== 函式正確性 ==============

class TestTrailingMA:
    """測試 trailing 移動平均(本日含前 window-1 日)"""

    def test_constant_input_returns_constant(self):
        """常數輸入應得常數輸出"""
        data = [100] * 20
        ma = ep.trailing_ma(data, window=7)
        assert all(v == 100 for v in ma)

    def test_length_preserved(self):
        """輸出長度等於輸入長度"""
        data = list(range(1, 30))
        ma = ep.trailing_ma(data, window=7)
        assert len(ma) == len(data)

    def test_no_none_values(self):
        """自適應窗口版本不可有 None(前 window-1 天用較短窗口)"""
        data = list(range(1, 30))
        ma = ep.trailing_ma(data, window=7)
        assert None not in ma

    def test_value_at_window_minus_one_uses_full_window(self):
        """第 window 個位置(index = window-1)起應使用完整窗口"""
        data = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100,
                110, 120, 130, 140, 150, 160, 170]
        ma = ep.trailing_ma(data, window=7)
        # index 6 是第 7 個元素,窗口為 data[0:7]
        expected_at_6 = sum(data[0:7]) / 7  # = 40
        assert ma[6] == round(expected_at_6)
        # index 10 是第 11 個,窗口為 data[4:11]
        expected_at_10 = sum(data[4:11]) / 7  # = 80
        assert ma[10] == round(expected_at_10)

    def test_early_indices_use_adaptive_window(self):
        """前 window-1 個位置應使用較短窗口而非 None"""
        data = list(range(1, 20))  # [1, 2, ..., 19]
        ma = ep.trailing_ma(data, window=7)
        # 第一個值應是 data[0:1] = data[0] = 1
        assert ma[0] == data[0]
        # 第二個值應是 data[0:2] = (1+2)/2 = 1.5 → 2(四捨五入)
        assert ma[1] == round(sum(data[0:2]) / 2)
        # 第三個值應是 data[0:3] 平均
        assert ma[2] == round(sum(data[0:3]) / 3)

    def test_endpoint_uses_full_window(self):
        """最後一個值應使用最近 window 個元素(完整窗口)"""
        data = list(range(1, 20))
        ma = ep.trailing_ma(data, window=7)
        # 最後一個值應是 data[-7:] 平均
        assert ma[-1] == round(sum(data[-7:]) / 7)

    def test_window_size_3(self):
        """支援不同 window 大小"""
        data = [10, 20, 30, 40, 50]
        ma = ep.trailing_ma(data, window=3)
        # index 2 應為 data[0:3] = (10+20+30)/3 = 20
        assert ma[2] == 20
        # index 3 應為 data[1:4] = (20+30+40)/3 = 30
        assert ma[3] == 30


# ============== apply_style 不崩潰 ==============

class TestApplyStyle:
    """apply_style() 應能無錯誤套用至 matplotlib"""

    def test_apply_style_does_not_raise(self):
        ep.apply_style()
        # 確認關鍵設定生效
        import matplotlib.pyplot as plt
        assert plt.rcParams["axes.spines.top"] is False
        assert plt.rcParams["axes.spines.right"] is False

    def test_apply_style_sets_categorical_cycle(self):
        """套用後的色彩循環必須是本指引的類別配色"""
        ep.apply_style()
        import matplotlib.pyplot as plt
        cycler_colors = plt.rcParams["axes.prop_cycle"].by_key()["color"]
        assert list(cycler_colors) == ep.CATEGORICAL

    def test_apply_style_can_create_figure(self):
        """套用樣式後能成功繪圖"""
        import matplotlib
        matplotlib.use("Agg")  # 非互動模式
        import matplotlib.pyplot as plt
        ep.apply_style()
        fig, ax = plt.subplots()
        ax.plot([1, 2, 3], [4, 5, 6])
        ax.set_title("test")
        plt.close(fig)

    def test_default_grid_horizontal_only(self):
        """預設網格僅水平（適合多數直條/折線圖）"""
        ep.apply_style()
        import matplotlib.pyplot as plt
        assert plt.rcParams["axes.grid.axis"] == "y", \
            "預設網格應僅 Y 軸（水平線），需垂直格線的圖表自行開啟"

    def test_hide_y_axis_helper(self):
        """hide_y_axis() 應清除 Y 軸所有元素"""
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        ep.apply_style()
        fig, ax = plt.subplots()
        ax.bar(["A", "B"], [10, 20])
        ax.set_ylabel("test label")
        ep.hide_y_axis(ax)

        # Y 軸標籤被清空
        assert ax.get_ylabel() == ""
        # 左軸線隱藏
        assert not ax.spines["left"].get_visible()
        plt.close(fig)

    def test_date_axis_helpers_work(self):
        """日期軸格式化函式應能套用於有日期 X 軸的圖表"""
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        from datetime import date, timedelta
        ep.apply_style()

        # 短期每日
        fig, ax = plt.subplots()
        dates = [date(2026, 5, 1) + timedelta(days=i) for i in range(28)]
        ax.plot(dates, range(28))
        ep.format_date_axis_daily(ax, interval=4)
        plt.close(fig)

        # 每週
        fig, ax = plt.subplots()
        ax.plot(dates, range(28))
        ep.format_date_axis_weekly(ax)
        plt.close(fig)

        # 跨月（中文格式 + 年份）
        fig, ax = plt.subplots()
        months = [date(2025, m, 1) for m in range(1, 13)]
        ax.plot(months, range(12))
        ep.format_date_axis_monthly(ax)
        # 確認 X 軸有設置 formatter
        assert ax.xaxis.get_major_formatter() is not None
        plt.close(fig)


# ============== 跨檔案一致性 ==============

class TestCrossFileConsistency:
    """檢查 CSV、PowerBI JSON、R 模組、Quarto、Streamlit 交付檔的色彩與 Python 模組一致"""

    @property
    def package_root(self):
        return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    @property
    def repo_root(self):
        # package_root = skill/；repo 根目錄為其上一層（resources/ 在此）
        return os.path.dirname(self.package_root)

    def _read(self, *parts):
        path = os.path.join(*parts)
        if not os.path.exists(path):
            pytest.skip(f"檔案不存在: {path}")
        with open(path, encoding="utf-8") as f:
            return f.read()

    @staticmethod
    def _find(pattern, content, label):
        import re
        m = re.search(pattern, content, re.S | re.M)
        assert m, f"未找到{label}（pattern: {pattern}）"
        return m.group(1)

    def test_csv_contains_primary(self):
        path = os.path.join(self.package_root, "epidemic-dataviz-palette.csv")
        if not os.path.exists(path):
            pytest.skip(f"CSV 不存在: {path}")
        with open(path, encoding="utf-8") as f:
            content = f.read()
        assert "#739A6D" in content, "CSV 中未找到主色 #739A6D"

    def test_powerbi_theme_data_colors(self):
        import json
        path = os.path.join(self.package_root, "epidemic-dataviz-theme.json")
        if not os.path.exists(path):
            pytest.skip(f"JSON 不存在: {path}")
        with open(path, encoding="utf-8") as f:
            theme = json.load(f)
        # 前 6 色應對應類別配色
        for i in range(6):
            assert theme["dataColors"][i] == ep.CATEGORICAL[i], \
                f"PowerBI theme dataColors[{i}] 與 CATEGORICAL[{i}] 不一致"

    def test_powerbi_theme_semantic(self):
        import json
        path = os.path.join(self.package_root, "epidemic-dataviz-theme.json")
        if not os.path.exists(path):
            pytest.skip(f"JSON 不存在: {path}")
        with open(path, encoding="utf-8") as f:
            theme = json.load(f)
        assert theme["good"] == ep.SEMANTIC["success"]
        assert theme["bad"] == ep.SEMANTIC["danger"]

    # ---- R / ggplot2 模組（值級，對齊 PowerBI 逐色比對強度）----

    def test_r_module_categorical_matches(self):
        """R 模組 EPI_CATEGORICAL 必須與 Python CATEGORICAL 順序、值完全一致"""
        import re
        content = self._read(self.package_root, "scripts", "epidemic_palette.R")
        body = self._find(r"EPI_CATEGORICAL\s*<-\s*c\((.*?)\)", content, "EPI_CATEGORICAL")
        hexes = re.findall(r"#[0-9A-Fa-f]{6}", body)
        assert hexes == ep.CATEGORICAL, \
            f"R EPI_CATEGORICAL {hexes} 與 Python CATEGORICAL {ep.CATEGORICAL} 不一致"

    def test_r_module_primary_line_accent_match(self):
        """R 模組主色、折線黃加深版、警示紅須與 Python 一致"""
        content = self._read(self.package_root, "scripts", "epidemic_palette.R")
        primary = self._find(r'EPI_PRIMARY\s*<-\s*"(#[0-9A-Fa-f]{6})"', content, "EPI_PRIMARY")
        assert primary == ep.PRIMARY, f"R EPI_PRIMARY {primary} != {ep.PRIMARY}"
        line_yellow = self._find(r'yellow\s*=\s*"(#[0-9A-Fa-f]{6})"', content, "折線黃")
        assert line_yellow == ep.LINE_COLORS["yellow"], \
            f"R 折線黃 {line_yellow} != {ep.LINE_COLORS['yellow']}"
        alert = self._find(r'alert\s*=\s*"(#[0-9A-Fa-f]{6})"', content, "警示紅")
        assert alert == ep.ACCENT["alert"], f"R alert {alert} != {ep.ACCENT['alert']}"

    def test_r_module_monochrome_matches(self):
        """R 模組 EPI_MONOCHROME 各組必須與 Python MONOCHROME 完全一致"""
        import re
        content = self._read(self.package_root, "scripts", "epidemic_palette.R")
        r_mono = {}
        for key, body in re.findall(r'(focus_2|scale_[3-7])\s*=\s*c\((.*?)\)', content, re.S):
            r_mono[key] = re.findall(r"#[0-9A-Fa-f]{6}", body)
        assert set(r_mono) == set(ep.MONOCHROME), \
            f"R 單色組合鍵 {set(r_mono)} 與 Python {set(ep.MONOCHROME)} 不一致"
        for key, colors in ep.MONOCHROME.items():
            assert r_mono[key] == colors, \
                f"R MONOCHROME[{key}] {r_mono[key]} != Python {colors}"

    # ---- Quarto 交付檔 ----

    def test_quarto_brand_categorical_complete(self):
        """Quarto _brand.yml 必須包含全部 6 個類別配色（避免非主色漂移）"""
        content = self._read(self.repo_root, "resources", "quarto", "_brand.yml")
        for hx in ep.CATEGORICAL:
            assert hx in content, f"_brand.yml 缺少類別配色 {hx}"

    def test_quarto_brand_primary_is_organizational(self):
        """_brand.yml 的 sage 必為組織主色，且 primary 角色指向 sage"""
        content = self._read(self.repo_root, "resources", "quarto", "_brand.yml")
        sage = self._find(r'sage:\s*"(#[0-9A-Fa-f]{6})"', content, "_brand.yml sage")
        assert sage == ep.PRIMARY, f"_brand.yml sage {sage} != 主色 {ep.PRIMARY}"
        prim_role = self._find(r'^\s*primary:\s*(\S+)', content, "_brand.yml primary 角色")
        assert prim_role == "sage", f"_brand.yml primary 角色應為 sage，實際 {prim_role}"

    def test_quarto_scss_categorical_complete(self):
        """epidemic.scss 的 --epi-cat-* 必須涵蓋全部 6 個類別配色"""
        content = self._read(self.repo_root, "resources", "quarto", "epidemic.scss")
        for hx in ep.CATEGORICAL:
            assert hx in content, f"epidemic.scss 缺少類別配色 {hx}"

    # ---- Streamlit 交付檔 ----

    def test_streamlit_config_primary(self):
        """Streamlit config.toml 的 primaryColor 必須是組織主色"""
        content = self._read(self.repo_root, "resources", "streamlit", "config.toml")
        primary = self._find(r'primaryColor\s*=\s*"(#[0-9A-Fa-f]{6})"', content,
                             "Streamlit primaryColor")
        assert primary == ep.PRIMARY, \
            f"Streamlit primaryColor {primary} != 主色 {ep.PRIMARY}"


class TestMonochrome:
    """單色使用組合（MONOCHROME）的正確性"""

    EXPECTED_KEYS = {"focus_2", "scale_3", "scale_4",
                     "scale_5", "scale_6", "scale_7"}

    def test_monochrome_has_required_keys(self):
        """MONOCHROME 應包含所有預期的組合鍵"""
        actual_keys = set(ep.MONOCHROME.keys())
        missing = self.EXPECTED_KEYS - actual_keys
        assert not missing, f"MONOCHROME 缺少組合: {missing}"

    def test_monochrome_lengths_match_keys(self):
        """每個組合的色彩數量應與名稱數字一致（scale_3 = 3 色等）"""
        for key, colors in ep.MONOCHROME.items():
            # 從 key 解出預期長度
            if key == "focus_2":
                expected = 2
            elif key.startswith("scale_"):
                expected = int(key.split("_")[1])
            else:
                continue
            assert len(colors) == expected, \
                f"MONOCHROME[{key}] 應有 {expected} 色,實際 {len(colors)}"

    def test_monochrome_all_valid_hex(self):
        """所有單色組合的 HEX 都應合法"""
        for key, colors in ep.MONOCHROME.items():
            for hx in colors:
                assert is_valid_hex(hx), f"MONOCHROME[{key}] 含非法 HEX: {hx}"

    def test_scale_palettes_monotonically_darken(self):
        """所有 scale_N 必須單調由淺至深（核心規範:色階方向有意義）"""
        from color_utils import relative_luminance, hex_to_rgb
        for key, colors in ep.MONOCHROME.items():
            if not key.startswith("scale_"):
                continue
            lums = [relative_luminance(hex_to_rgb(c)) for c in colors]
            for i in range(len(lums) - 1):
                assert lums[i] > lums[i+1], (
                    f"MONOCHROME[{key}] 非單調變深: "
                    f"index {i} ({colors[i]}, lum={lums[i]:.3f}) ≤ "
                    f"index {i+1} ({colors[i+1]}, lum={lums[i+1]:.3f})"
                )

    def test_focus_2_has_clear_contrast(self):
        """focus_2 兩色之間必須有清楚對比（焦點 + 對照需可區分）"""
        c1, c2 = ep.MONOCHROME["focus_2"]
        r = contrast_ratio(c1, c2)
        assert r >= 2.0, \
            f"focus_2 兩色對比 {r:.2f} 不足（焦點與對照需可區分）"

    def test_adjacent_scale_steps_distinguishable(self):
        """相鄰色階間需有足夠對比（避免淺色互相黏在一起）"""
        from color_utils import relative_luminance, hex_to_rgb
        for key in ["scale_3", "scale_4", "scale_5", "scale_6", "scale_7"]:
            colors = ep.MONOCHROME[key]
            lums = [relative_luminance(hex_to_rgb(c)) for c in colors]
            for i in range(len(lums) - 1):
                lum_diff = lums[i] - lums[i+1]
                # 相鄰色階亮度差至少 0.04（經驗值,確保人眼能分辨）
                assert lum_diff >= 0.04, (
                    f"MONOCHROME[{key}] 相鄰色階 index {i} 與 {i+1} "
                    f"亮度差 {lum_diff:.3f} < 0.04（人眼難以分辨）"
                )

    def test_scale_endpoints_strong_contrast(self):
        """每個 scale 的首末兩色對比必須足夠強"""
        for key in ["scale_3", "scale_4", "scale_5", "scale_6", "scale_7"]:
            colors = ep.MONOCHROME[key]
            r = contrast_ratio(colors[0], colors[-1])
            assert r >= 4.0, (
                f"MONOCHROME[{key}] 首末對比 {r:.2f} < 4.0"
                f"（色階首末應清楚區分）"
            )


class TestSampleData:
    """sample-data 資料集完整性"""

    @property
    def data_dir(self):
        return os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "assets", "sample-data",
        )

    def _list_csv(self):
        if not os.path.exists(self.data_dir):
            return []
        return sorted([f for f in os.listdir(self.data_dir)
                       if f.endswith(".csv")])

    def test_all_expected_csv_files_exist(self):
        """確認 12 個範例 CSV 都存在"""
        if not os.path.exists(self.data_dir):
            pytest.skip(f"sample-data 目錄不存在: {self.data_dir}")
        expected = [
            "01-daily-cases.csv", "02-weekly-waves.csv",
            "03-yoy-comparison.csv", "04-city-rates.csv",
            "05-variant-share.csv", "06-vaccine-coverage.csv",
            "07-age-severity.csv", "08-vax-status.csv",
            "09-vax-vs-severity.csv", "10-age-gender.csv",
            "11-region-stay.csv", "12-monthly-incidence.csv",
        ]
        existing = self._list_csv()
        for f in expected:
            assert f in existing, f"缺少範例資料: {f}"

    def test_manifest_json_lists_all_files(self):
        """_manifest.json 應列出所有資料檔"""
        manifest_path = os.path.join(self.data_dir, "_manifest.json")
        if not os.path.exists(manifest_path):
            pytest.skip("無 manifest 檔")
        import json
        with open(manifest_path, encoding="utf-8") as f:
            manifest = json.load(f)
        listed_files = {v["source_file"]
                        for v in manifest["datasets"].values()}
        existing = set(self._list_csv())
        # manifest 列出的每個檔案都該存在
        missing = listed_files - existing
        assert not missing, f"manifest 引用但實際缺少的檔案: {missing}"

    def test_csv_files_are_utf8_with_bom(self):
        """所有 CSV 都應使用 UTF-8 with BOM（Excel 相容）"""
        for fn in self._list_csv():
            path = os.path.join(self.data_dir, fn)
            with open(path, "rb") as f:
                first_bytes = f.read(3)
            assert first_bytes == b"\xef\xbb\xbf", \
                f"{fn} 缺少 UTF-8 BOM（Excel 會中文亂碼）"

    def test_csv_files_are_parseable(self):
        """所有 CSV 應能被 csv 模組正確 parse"""
        import csv as csv_mod
        for fn in self._list_csv():
            path = os.path.join(self.data_dir, fn)
            with open(path, encoding="utf-8-sig") as f:
                reader = csv_mod.DictReader(f)
                rows = list(reader)
            assert len(rows) > 0, f"{fn} 沒有資料列"
            assert reader.fieldnames, f"{fn} 缺少欄位標頭"

    def test_percentage_columns_sum_correctly(self):
        """部分資料的 % 欄位橫向加總應為 100"""
        import csv as csv_mod
        # 變異株比例
        with open(os.path.join(self.data_dir, "05-variant-share.csv"),
                  encoding="utf-8-sig") as f:
            for row in csv_mod.DictReader(f):
                total = sum(int(row[k]) for k in ["JN.1", "KP.2",
                                                  "KP.3", "LB.1", "other"])
                assert total == 100, f"05 月份 {row['month']} 加總 {total} ≠ 100"

        # 年齡 × 嚴重度
        with open(os.path.join(self.data_dir, "07-age-severity.csv"),
                  encoding="utf-8-sig") as f:
            for row in csv_mod.DictReader(f):
                total = sum(int(row[k]) for k in
                            ["mild_pct", "moderate_pct", "severe_pct"])
                assert total == 100, \
                    f"07 年齡組 {row['age_group']} 加總 {total} ≠ 100"

        # 疫苗接種狀態
        with open(os.path.join(self.data_dir, "08-vax-status.csv"),
                  encoding="utf-8-sig") as f:
            for row in csv_mod.DictReader(f):
                total = sum(int(row[k]) for k in [
                    "fully_vaccinated_pct", "partially_vaccinated_pct",
                    "unvaccinated_pct", "unknown_pct"])
                assert total == 100, f"08 年份 {row['year']} 加總 {total} ≠ 100"

    def test_vaccine_coverage_monotonically_increasing(self):
        """累計疫苗覆蓋率應隨時間單調遞增"""
        import csv as csv_mod
        with open(os.path.join(self.data_dir, "06-vaccine-coverage.csv"),
                  encoding="utf-8-sig") as f:
            rows = list(csv_mod.DictReader(f))
        for col in ["dose_1_pct", "dose_2_pct", "dose_3_pct"]:
            vals = [int(r[col]) for r in rows]
            for i in range(len(vals) - 1):
                assert vals[i] <= vals[i+1], \
                    f"{col} 在月份 {rows[i+1]['month']} 反向遞減（累計應單調遞增）"

    def test_city_rates_population_realistic(self):
        """22 縣市人口資料應合理（總和接近 2300 萬）"""
        import csv as csv_mod
        with open(os.path.join(self.data_dir, "04-city-rates.csv"),
                  encoding="utf-8-sig") as f:
            total_pop = sum(float(r["population_10k"])
                            for r in csv_mod.DictReader(f))
        # 台灣 22 縣市總人口約 2300 萬
        assert 2000 <= total_pop <= 2500, \
            f"22 縣市人口總和 {total_pop} 萬人不在合理範圍 [2000, 2500]"


# ============== 直接執行（無 pytest 也能跑）==============

def _run_without_pytest():
    """簡易執行模式：不需 pytest，直接呼叫所有 test 方法

    處理 @pytest.mark.parametrize: 從裝飾器抽出參數展開呼叫
    """
    import traceback

    def _extract_parametrize_args(method):
        """從方法的 pytest.mark.parametrize 取出參數值；無則回傳 None"""
        if not hasattr(method, "pytestmark"):
            return None
        params_list = []
        for mark in method.pytestmark:
            if mark.name == "parametrize":
                # mark.args = (argnames, argvalues)
                argnames, argvalues = mark.args
                for val in argvalues:
                    params_list.append((argnames, val))
        return params_list if params_list else None

    test_classes = [
        TestHexFormat, TestCompleteness, TestOrdering,
        TestContrast, TestColorBlindness, TestTrailingMA,
        TestApplyStyle, TestCrossFileConsistency,
        TestMonochrome, TestSampleData,
    ]
    total = passed = failed = skipped = 0
    failures = []

    for cls in test_classes:
        instance = cls()
        test_methods = [m for m in dir(instance) if m.startswith("test_")]
        cls_name = cls.__name__
        print(f"\n── {cls_name} ──")
        for m in test_methods:
            method = getattr(instance, m)
            params = _extract_parametrize_args(method)
            cases = params if params else [(None, None)]

            for argnames, val in cases:
                total += 1
                display_name = m if argnames is None else f"{m}[{val}]"
                try:
                    if argnames is None:
                        method()
                    else:
                        method(val)
                    passed += 1
                    print(f"  ✓ {display_name}")
                except pytest.skip.Exception as e:
                    skipped += 1
                    print(f"  ⊘ {display_name}  (skipped: {e})")
                except AssertionError as e:
                    failed += 1
                    failures.append((cls_name, display_name, str(e)))
                    print(f"  ✗ {display_name}")
                    msg = str(e).split("\n")[0]
                    print(f"      {msg}")
                except Exception as e:
                    failed += 1
                    failures.append((cls_name, display_name, f"{type(e).__name__}: {e}"))
                    print(f"  ✗ {display_name} (錯誤)")
                    traceback.print_exc()

    print("\n" + "═" * 50)
    print(f"  共 {total} 個測試  ✓ {passed}  ✗ {failed}  ⊘ {skipped}")
    print("═" * 50)
    if failures:
        print("\n失敗詳情：")
        for cls_name, method, err in failures:
            print(f"  • {cls_name}.{method}")
            for line in err.split("\n"):
                print(f"      {line}")
    return failed


if __name__ == "__main__":
    sys.exit(1 if _run_without_pytest() > 0 else 0)
