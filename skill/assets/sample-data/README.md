# 範例資料集 ／ Sample Data Dictionary

> ⚠️ **所有資料皆為虛構，僅供圖表規範範例使用，不代表真實疫情狀況。**

本目錄包含 12 個範例資料集，對應指引中 9 個圖表類型的所有範例圖。所有檔案：

- **CSV 格式**：UTF-8 with BOM（Excel 直接開啟中文不亂碼）
- **欄位命名**：英文 snake_case，單位後綴清楚（`_pct`, `_per_100k`, `_thousand`）
- **日期格式**：ISO 8601（`YYYY-MM-DD` 或 `YYYY-MM`）
- **可重現**：所有隨機資料皆使用固定種子，重跑 `generate_sample_data.py` 結果一致

## 檔案總覽

| 編號 | 檔案 | 列數 | 對應圖表 |
|------|------|------|---------|
| 01 | `01-daily-cases.csv` | 28 | 每日新增直條 + 移動平均 |
| 02 | `02-weekly-waves.csv` | 30 | 波次比較折線 |
| 03 | `03-yoy-comparison.csv` | 24 | 同期比較含歷史範圍 |
| 04 | `04-city-rates.csv` | 22 | 縣市排名長條、面量圖 |
| 05 | `05-variant-share.csv` | 6 | 變異株 100% 堆疊 |
| 06 | `06-vaccine-coverage.csv` | 12 | 疫苗覆蓋率區域圖 |
| 07 | `07-age-severity.csv` | 7 | 年齡 × 嚴重度分組長條 |
| 08 | `08-vax-status.csv` | 3 | 接種狀態圓餅／水平堆疊 |
| 09 | `09-vax-vs-severity.csv` | 20 | 散佈圖、泡泡圖 |
| 10 | `10-age-gender.csv` | 9 | 人口金字塔 |
| 11 | `11-region-stay.csv` | 1200 | 區域住院天數盒鬚圖 |
| 12 | `12-monthly-incidence.csv` | 10 | 縣市 × 月份熱力圖 |
| – | `_manifest.json` | – | 整合 metadata（API 用） |

---

## 詳細欄位說明

### 01-daily-cases.csv

每日新增確診數，含明顯的「週末填報延遲」效應，適合示範 7 日移動平均的價值。

| 欄位 | 型別 | 說明 |
|------|------|------|
| `date` | Date (ISO 8601) | 報告日（2026-04-24 ~ 2026-05-21） |
| `weekday` | String | 星期（週一 ~ 週日，方便目視確認週末效應） |
| `new_cases` | Integer | 該日新增確診數 |

### 02-weekly-waves.csv

三波疫情各 30 天的每日新增，已**按波峰相對日對齊**（不是真實日期）。適合波次比較折線圖。

| 欄位 | 型別 | 說明 |
|------|------|------|
| `relative_day` | Integer | 相對日（1–30，1 = 該波起點） |
| `wave_2022` | Integer | 第一波每日新增 |
| `wave_2023` | Integer | 第二波每日新增 |
| `wave_2024` | Integer | 第三波每日新增（最新） |

### 03-yoy-comparison.csv

今年 vs. 去年同期的每週比較，含「歷史 ±1 SD 範圍」可繪製陰影區帶。

| 欄位 | 型別 | 說明 |
|------|------|------|
| `relative_week` | String | 相對週（W1, W2, ..., W24） |
| `current_year` | Integer | 今年該週新增 |
| `last_year` | Integer | 去年同期該週新增 |
| `historical_high` | Integer | 歷史 +1 SD（虛擬，模擬 3 年資料的離散） |
| `historical_low` | Integer | 歷史 -1 SD |

### 04-city-rates.csv

22 縣市的疫情指標。發生率已標準化（每 10 萬人口），可直接用於排名長條與面量圖。

| 欄位 | 型別 | 說明 |
|------|------|------|
| `city` | String | 縣市名稱 |
| `rate_per_100k` | Number | 發生率（每 10 萬人口） |
| `population_10k` | Number | 縣市人口（萬人）—— 適合作泡泡圖第三維度 |

### 05-variant-share.csv

6 個月變異株比例。橫向加總應為 100%（在 100% 堆疊圖中即為各層厚度）。

| 欄位 | 型別 | 說明 |
|------|------|------|
| `month` | String | 月份（YYYY-MM） |
| `JN.1` | Integer | JN.1 變異株比例（%） |
| `KP.2` | Integer | KP.2 變異株比例（%） |
| `KP.3` | Integer | KP.3 變異株比例（%） |
| `LB.1` | Integer | LB.1 變異株比例（%） |
| `other` | Integer | 其他變異株合計（%） |

### 06-vaccine-coverage.csv

12 個月疫苗 1/2/3 劑累計覆蓋率（單調遞增）。

| 欄位 | 型別 | 說明 |
|------|------|------|
| `month` | String | 月份（YYYY-MM） |
| `dose_1_pct` | Integer | 第 1 劑累計覆蓋率（%） |
| `dose_2_pct` | Integer | 第 2 劑累計覆蓋率（%） |
| `dose_3_pct` | Integer | 第 3 劑累計覆蓋率（%） |

### 07-age-severity.csv

各年齡層的嚴重度比例。橫向加總應為 100%（每年齡層內部）。

| 欄位 | 型別 | 說明 |
|------|------|------|
| `age_group` | String | 年齡組（0-9, 10-19, ..., 80+） |
| `mild_pct` | Integer | 輕症比例（%） |
| `moderate_pct` | Integer | 中症比例（%） |
| `severe_pct` | Integer | 重症比例（%） |

### 08-vax-status.csv

跨年度確診者疫苗接種狀態組成。橫向加總應為 100%。可同時用於圓餅圖（單年）與水平堆疊條（跨年比較）。

| 欄位 | 型別 | 說明 |
|------|------|------|
| `year` | String | 年份（2022, 2023, 2024） |
| `fully_vaccinated_pct` | Integer | 已完整接種比例（%） |
| `partially_vaccinated_pct` | Integer | 部分接種比例（%） |
| `unvaccinated_pct` | Integer | 未接種比例（%） |
| `unknown_pct` | Integer | 不詳比例（%） |

### 09-vax-vs-severity.csv

20 個縣市的接種率與重症率（呈負相關），含人口可作泡泡圖第三維度。

| 欄位 | 型別 | 說明 |
|------|------|------|
| `city` | String | 縣市名稱 |
| `vaccination_pct` | Integer | 完整接種率（%） |
| `severe_per_1000` | Number | 重症率（每 1000 確診例） |
| `population_10k` | Number | 人口（萬人） |

### 10-age-gender.csv

確診者年齡 × 性別，男女分欄。

| 欄位 | 型別 | 說明 |
|------|------|------|
| `age_group` | String | 年齡組（0-9, 10-19, ..., 80+） |
| `male_thousand` | Integer | 男性確診數（千人） |
| `female_thousand` | Integer | 女性確診數（千人） |

### 11-region-stay.csv

**長表格格式**：每列一筆住院記錄。1200 筆樣本（6 區 × 200 筆），適合直接餵給 boxplot。

| 欄位 | 型別 | 說明 |
|------|------|------|
| `region` | String | 地理區域（北區、桃竹苗、中區、雲嘉南、高屏、東區） |
| `hospital_days` | Number | 住院天數（從 Gamma 分布抽樣，符合住院天數的右偏特性） |

### 12-monthly-incidence.csv

**寬表格／矩陣格式**：10 縣市 × 12 月份的發生率，適合直接傳入 `imshow()` 或 heatmap。

| 欄位 | 型別 | 說明 |
|------|------|------|
| `city` | String | 縣市名稱 |
| `2025-01` ~ `2025-12` | Integer | 該月發生率（每 10 萬人口） |

---

## 使用範例

### Python (pandas)

```python
import pandas as pd

# 一般 CSV
df = pd.read_csv("01-daily-cases.csv",
                 encoding="utf-8-sig",
                 parse_dates=["date"])

# 月份字串轉日期
df = pd.read_csv("05-variant-share.csv", encoding="utf-8-sig")
df["month"] = pd.to_datetime(df["month"] + "-01")

# 矩陣格式（熱力圖）
df = pd.read_csv("12-monthly-incidence.csv",
                 encoding="utf-8-sig", index_col="city")
heatmap_data = df.values  # numpy array
```

### R

```r
library(readr)
daily <- read_csv("01-daily-cases.csv")
df <- read_csv("11-region-stay.csv")
boxplot(hospital_days ~ region, data = df)
```

### Excel

直接雙擊開啟，BOM 確保中文不亂碼。所有 CSV 都可在 Excel 中直接製作圖表。

---

## 重新生成資料

```bash
cd scripts/
python generate_sample_data.py
```

所有資料使用固定亂數種子，重跑結果完全一致（除了 11-region-stay.csv 用 seed=101、其他用 seed=42/55/7 等）。

## 資料合理性說明

雖然是虛構資料，但設計時遵循疫情資料的真實樣貌：

- **每日新增**：含週末填報延遲（週末約為週間的 60%）
- **波次曲線**：呈現典型的「指數上升 → 高峰 → 衰減」鐘形
- **變異株消長**：新株逐月取代舊株，符合實際傳播動力學
- **疫苗覆蓋率**：累計值單調遞增，符合接種統計邏輯
- **年齡 × 嚴重度**：高齡組重症比例明顯較高
- **住院天數**：使用 Gamma 分布模擬右偏的住院天數分布
- **散佈圖**：接種率與重症率呈明顯負相關（r ≈ -0.9）
- **發生率排名**：六都人口大、發生率較高，但已標準化避免絕對數偏誤
