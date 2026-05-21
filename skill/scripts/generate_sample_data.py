"""
generate_sample_data.py
產生對應 9 個圖表類型的範例疫情資料集

執行方式：
    python generate_sample_data.py

輸出至 ../assets/sample-data/
所有資料皆為虛構，僅供圖表規範範例使用。
"""
import os
import json
import csv
from datetime import date, timedelta
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.join(HERE, "..", "assets", "sample-data")
os.makedirs(OUT_DIR, exist_ok=True)


def write_csv(rows, filename, header=None):
    """寫出 CSV，所有檔案使用 UTF-8 (BOM) 確保 Excel 中文不亂碼"""
    path = os.path.join(OUT_DIR, filename)
    with open(path, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f)
        if header:
            writer.writerow(header)
        writer.writerows(rows)
    print(f"  ✓ {filename}  ({len(rows)} 列)")


def write_json(data, filename):
    path = os.path.join(OUT_DIR, filename)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"  ✓ {filename}")


# === 01. 28 天每日新增確診（含週末填報延遲效應） ===
def gen_daily_cases():
    np.random.seed(42)
    end_date = date(2026, 5, 21)
    dates = [end_date - timedelta(days=27-i) for i in range(28)]
    base = 1500 + np.arange(28) * 100  # 線性上升趨勢
    weekend_dip = np.array([0.6 if d.weekday() >= 5 else 1.0 for d in dates])
    daily = (base * weekend_dip + np.random.randint(-200, 200, 28)).astype(int)

    rows = []
    for d, v in zip(dates, daily):
        weekday_zh = "一二三四五六日"[d.weekday()]
        rows.append([d.isoformat(), f"週{weekday_zh}", v])
    write_csv(rows, "01-daily-cases.csv",
              header=["date", "weekday", "new_cases"])


# === 02. 三波疫情的每日數據（用於波次比較） ===
def gen_weekly_waves():
    # 三波各 30 天，按相對日對齊
    wave1 = [120,180,260,380,520,720,980,1240,1580,1820,
             1960,1880,1740,1520,1280,1040,820,640,490,380,
             290,220,170,130,100,80,65,52,42,35]
    wave2 = [180,290,420,640,920,1280,1720,2180,2640,3020,
             3280,3340,3180,2860,2440,1980,1560,1180,890,680,
             510,390,290,220,170,130,100,80,62,48]
    wave3 = [240,380,560,820,1180,1620,2180,2840,3520,4180,
             4720,5040,5180,5040,4640,4080,3420,2780,2210,1740,
             1360,1050,810,620,470,360,275,210,160,120]

    rows = []
    for day in range(30):
        rows.append([day+1, wave1[day], wave2[day], wave3[day]])
    write_csv(rows, "02-weekly-waves.csv",
              header=["relative_day", "wave_2022", "wave_2023", "wave_2024"])


# === 03. 同期比較（今年 vs 去年 + 歷史範圍） ===
def gen_yoy_comparison():
    this_year = [180, 220, 280, 340, 420, 520, 680, 920, 1280,
                 1820, 2640, 3580, 4220, 4180, 3640, 2840, 2120,
                 1580, 1180, 880, 660, 490, 360, 280]
    last_year = [220, 260, 310, 380, 460, 560, 720, 980, 1340,
                 1820, 2480, 3120, 3640, 3580, 3120, 2480, 1880,
                 1380, 1020, 760, 570, 420, 310, 240]
    hist_high = [int(v * 1.35) for v in last_year]
    hist_low  = [int(v * 0.65) for v in last_year]

    rows = []
    for w in range(24):
        rows.append([f"W{w+1}", this_year[w], last_year[w],
                     hist_high[w], hist_low[w]])
    write_csv(rows, "03-yoy-comparison.csv",
              header=["relative_week", "current_year",
                      "last_year", "historical_high", "historical_low"])


# === 04. 22 縣市發生率（用於排名長條與面量圖） ===
def gen_city_rates():
    cities = [
        ("新北市", 920, 401), ("臺北市", 870, 263), ("桃園市", 760, 226),
        ("臺中市", 720, 284), ("高雄市", 680, 276), ("臺南市", 640, 188),
        ("彰化縣", 590, 125), ("屏東縣", 540, 81), ("新竹縣", 510, 57),
        ("雲林縣", 480, 67), ("苗栗縣", 460, 54), ("嘉義縣", 440, 49),
        ("南投縣", 420, 49), ("宜蘭縣", 410, 45), ("基隆市", 400, 36),
        ("新竹市", 390, 45), ("花蓮縣", 360, 33), ("臺東縣", 340, 21),
        ("嘉義市", 330, 27), ("澎湖縣", 290, 11), ("金門縣", 240, 14),
        ("連江縣", 180, 1.3),
    ]
    rows = [[name, rate, pop] for name, rate, pop in cities]
    write_csv(rows, "04-city-rates.csv",
              header=["city", "rate_per_100k", "population_10k"])


# === 05. 變異株比例（6 個月） ===
def gen_variant_share():
    months = ["2025-11", "2025-12", "2026-01",
              "2026-02", "2026-03", "2026-04"]
    jn1 =   [62, 48, 32, 18,  8,  3]
    kp2 =   [28, 36, 42, 38, 24, 14]
    kp3 =   [ 6, 12, 18, 28, 42, 48]
    lb1 =   [ 2,  3,  6, 14, 22, 30]
    other = [ 2,  1,  2,  2,  4,  5]

    rows = []
    for i, m in enumerate(months):
        rows.append([m, jn1[i], kp2[i], kp3[i], lb1[i], other[i]])
    write_csv(rows, "05-variant-share.csv",
              header=["month", "JN.1", "KP.2", "KP.3", "LB.1", "other"])


# === 06. 疫苗 1/2/3 劑累計覆蓋率（12 個月） ===
def gen_vaccine_coverage():
    dose1 = [42, 58, 71, 79, 84, 87, 89, 91, 92, 93, 94, 94]
    dose2 = [28, 42, 56, 67, 74, 79, 83, 86, 88, 89, 90, 91]
    dose3 = [ 8, 18, 28, 38, 46, 53, 59, 64, 68, 72, 75, 77]

    rows = []
    for m in range(12):
        month_str = f"2025-{m+1:02d}"
        rows.append([month_str, dose1[m], dose2[m], dose3[m]])
    write_csv(rows, "06-vaccine-coverage.csv",
              header=["month", "dose_1_pct", "dose_2_pct", "dose_3_pct"])


# === 07. 年齡層 × 嚴重度比例（分組長條） ===
def gen_age_severity():
    ages = ["0-9", "10-19", "20-39", "40-59", "60-69", "70-79", "80+"]
    mild = [78, 85, 89, 82, 70, 55, 38]
    mod  = [18, 13,  9, 14, 22, 32, 42]
    sev  = [ 4,  2,  2,  4,  8, 13, 20]

    rows = []
    for i, a in enumerate(ages):
        rows.append([a, mild[i], mod[i], sev[i]])
    write_csv(rows, "07-age-severity.csv",
              header=["age_group", "mild_pct", "moderate_pct", "severe_pct"])


# === 08. 確診者疫苗接種狀態（圓餅 / 水平堆疊；跨年比較） ===
def gen_vax_status():
    years = ["2022", "2023", "2024"]
    full =    [28, 48, 62]
    partial = [24, 22, 18]
    none =    [38, 22, 14]
    unknown = [10,  8,  6]

    rows = []
    for i, y in enumerate(years):
        rows.append([y, full[i], partial[i], none[i], unknown[i]])
    write_csv(rows, "08-vax-status.csv",
              header=["year", "fully_vaccinated_pct",
                      "partially_vaccinated_pct",
                      "unvaccinated_pct", "unknown_pct"])


# === 09. 各縣市疫苗接種率 vs. 重症率（散佈 / 泡泡） ===
def gen_vax_vs_severity():
    # 真實感的負相關：接種率高 → 重症率低
    np.random.seed(7)
    cities = [
        ("新北市", 88, 2.8, 401),
        ("臺北市", 92, 2.1, 263),
        ("桃園市", 85, 3.6, 226),
        ("臺中市", 82, 4.2, 284),
        ("高雄市", 80, 4.5, 276),
        ("臺南市", 78, 5.1, 188),
        ("新竹市", 90, 2.5,  45),
        ("彰化縣", 76, 5.8, 125),
        ("雲林縣", 70, 6.8,  67),
        ("嘉義縣", 73, 6.0,  49),
        ("屏東縣", 74, 5.6,  81),
        ("基隆市", 84, 3.4,  36),
        ("宜蘭縣", 78, 4.8,  45),
        ("花蓮縣", 72, 6.2,  33),
        ("臺東縣", 68, 7.2,  21),
        ("苗栗縣", 75, 5.5,  54),
        ("南投縣", 72, 6.0,  49),
        ("嘉義市", 86, 3.0,  27),
        ("新竹縣", 81, 4.0,  57),
        ("澎湖縣", 79, 4.8,  11),
    ]
    rows = []
    for name, vax, sev, pop in cities:
        rows.append([name, vax, sev, pop])
    write_csv(rows, "09-vax-vs-severity.csv",
              header=["city", "vaccination_pct",
                      "severe_per_1000", "population_10k"])


# === 10. 年齡 × 性別（人口金字塔） ===
def gen_age_gender():
    ages = ["0-9", "10-19", "20-29", "30-39", "40-49",
            "50-59", "60-69", "70-79", "80+"]
    male   = [12, 18, 22, 24, 28, 30, 26, 18, 10]
    female = [11, 17, 24, 26, 29, 31, 28, 22, 14]

    rows = []
    for i, a in enumerate(ages):
        rows.append([a, male[i], female[i]])
    write_csv(rows, "10-age-gender.csv",
              header=["age_group", "male_thousand", "female_thousand"])


# === 11. 各區域住院天數樣本（用於盒鬚圖） ===
def gen_region_stay():
    """長表格格式：每列一筆住院記錄,適合 boxplot 直接讀"""
    np.random.seed(101)
    regions_params = {
        "北區":    (2.5, 2.5),
        "桃竹苗":  (3.0, 2.2),
        "中區":    (2.8, 2.8),
        "雲嘉南":  (3.5, 2.4),
        "高屏":    (3.2, 3.0),
        "東區":    (4.0, 2.6),
    }
    rows = []
    for region, (shape, scale) in regions_params.items():
        # 每區 200 筆樣本
        samples = np.random.gamma(shape, scale, 200)
        for s in samples:
            rows.append([region, round(float(s), 1)])
    write_csv(rows, "11-region-stay.csv",
              header=["region", "hospital_days"])


# === 12. 縣市 × 月份發生率矩陣（熱力圖） ===
def gen_monthly_incidence():
    np.random.seed(55)
    cities = ["新北", "臺北", "桃園", "臺中", "臺南", "高雄",
              "新竹", "基隆", "彰化", "屏東"]
    months_str = [f"2025-{m:02d}" for m in range(1, 13)]
    data = np.random.randint(50, 900, size=(10, 12)).astype(float)
    data[:, 6:9] *= 1.5  # 夏季高峰
    data[:, 11] *= 1.3   # 年底反彈
    data = data.astype(int)

    rows = []
    for i, city in enumerate(cities):
        rows.append([city] + list(data[i]))
    write_csv(rows, "12-monthly-incidence.csv",
              header=["city"] + months_str)


# === 同時產生一份 JSON 主資料集（給 API 開發者使用）===
def gen_master_json():
    """整合所有資料集為單一 JSON,方便程式化讀取"""
    master = {
        "version": "1.0",
        "generated": "2026-05-21",
        "note": "All data is fictional, for visualization guideline examples only.",
        "datasets": {
            "daily_cases": {
                "description": "28 days of daily new cases with weekend reporting effect",
                "source_file": "01-daily-cases.csv",
            },
            "weekly_waves": {
                "description": "Three pandemic waves aligned by relative day from start",
                "source_file": "02-weekly-waves.csv",
            },
            "yoy_comparison": {
                "description": "Year-over-year weekly comparison with historical range",
                "source_file": "03-yoy-comparison.csv",
            },
            "city_rates": {
                "description": "Per-100k incidence rates for 22 cities, with population",
                "source_file": "04-city-rates.csv",
            },
            "variant_share": {
                "description": "Monthly share of major variants",
                "source_file": "05-variant-share.csv",
            },
            "vaccine_coverage": {
                "description": "Cumulative vaccination coverage for dose 1/2/3 by month",
                "source_file": "06-vaccine-coverage.csv",
            },
            "age_severity": {
                "description": "Severity (mild/moderate/severe) by age group",
                "source_file": "07-age-severity.csv",
            },
            "vax_status": {
                "description": "Vaccination status among confirmed cases, by year",
                "source_file": "08-vax-status.csv",
            },
            "vax_vs_severity": {
                "description": "City-level correlation: vaccination rate vs. severe rate",
                "source_file": "09-vax-vs-severity.csv",
            },
            "age_gender": {
                "description": "Confirmed cases by age group and gender (for pyramid)",
                "source_file": "10-age-gender.csv",
            },
            "region_stay": {
                "description": "Long-format sample of hospital stay days by region (1,200 records)",
                "source_file": "11-region-stay.csv",
            },
            "monthly_incidence": {
                "description": "Matrix of monthly incidence by city (for heatmap)",
                "source_file": "12-monthly-incidence.csv",
            },
        }
    }
    write_json(master, "_manifest.json")


def main():
    print(f"輸出目錄: {OUT_DIR}\n")
    gen_daily_cases()
    gen_weekly_waves()
    gen_yoy_comparison()
    gen_city_rates()
    gen_variant_share()
    gen_vaccine_coverage()
    gen_age_severity()
    gen_vax_status()
    gen_vax_vs_severity()
    gen_age_gender()
    gen_region_stay()
    gen_monthly_incidence()
    gen_master_json()
    print(f"\n✓ 全部完成。共 13 個檔案。")


if __name__ == "__main__":
    main()
