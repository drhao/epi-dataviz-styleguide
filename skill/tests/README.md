# 測試 ／ Tests

本目錄包含色票模組的自動化測試。每次修改 `scripts/epidemic_palette.py` 或相關色票檔（CSV、JSON）後，請執行測試以確保未破壞指引核心承諾。

## 測試涵蓋範圍

80 個測試案例，分為 10 個測試類別：

| 類別 | 測試項目 | 數量 |
|------|---------|------|
| `TestHexFormat` | 所有色票格式合法（#RRGGBB 大寫） | 8 |
| `TestCompleteness` | 必要色彩存在、數量正確、主色為 #739A6D | 7 |
| `TestOrdering` | 主色階、序列色階單調變暗 | 2 |
| `TestContrast` | WCAG 對比度（文字 4.5、圖形 3.0、填色 2.4） | 15 |
| `TestColorBlindness` | 三種色覺障礙下的可區分性 | 11 |
| `TestTrailingMA` | Trailing 移動平均函式正確性 | 7 |
| `TestApplyStyle` | matplotlib 樣式套用不崩潰 | 6 |
| `TestCrossFileConsistency` | CSV / PowerBI JSON / R 模組 / Quarto / Streamlit 與 Python 模組值級一致 | 10 |
| `TestMonochrome` | 單色組合（MONOCHROME）正確性與單調性 | 7 |
| `TestSampleData` | 範例 CSV 完整性、編碼、加總、單調性 | 7 |

## 執行方式

### 方式 A：使用 pytest（推薦）

```bash
cd tests/
pytest test_palette.py -v
```

需要先安裝 pytest：`pip install pytest`

### 方式 B：純 Python 執行（無需 pytest）

```bash
cd tests/
python test_palette.py
```

會看到類似輸出：

```
── TestHexFormat ──
  ✓ test_primary_scale_format
  ✓ test_categorical_format
  ...

══════════════════════════════════════════════════
  共 80 個測試  ✓ 80  ✗ 0  ⊘ 0
══════════════════════════════════════════════════
```

## 關鍵測試說明

### WCAG 對比度分級

本指引採用三層門檻：

| 用途 | 門檻 | 理由 |
|------|------|------|
| 文字（一般） | ≥ 4.5 | WCAG AA 標準 |
| 圖形元素（邊框、線條、小圖示） | ≥ 3.0 | WCAG 非文字 AA |
| 大面積填色（長條、圓餅切片） | ≥ 2.4 | 實務門檻（資料視覺化慣例） |

**為何填色標準較寬鬆？** 大面積填色在白底上即使對比較低仍可辨識；嚴格 3.0 標準主要針對線條/圖示等纖細元素。例如 Mustard `#C8A041` 對白底對比 2.45，作為大面積長條可用，但作為折線就需改用加深版 `#A8821F`。

### 色覺障礙測試的分層門檻

| 配色情境 | 門檻 | 說明 |
|---------|------|------|
| 前 3 色（綠/藍/黃，最常用） | 嚴格 30 | 核心承諾，必須完全可區分 |
| 全部 6 色 | 寬鬆 8 | 已知 Slate Blue ↔ Teal 在綠色盲下接近 |
| 發散色階兩端 | 嚴格 30 | 紅綠對立必須區分 |
| 主色 vs 警示紅 | 嚴格 30 | 疫情圖表常見組合 |

**已知限制**：當需要使用 4 色以上時，必須搭配形狀、紋路、直接標籤輔助，避免單靠顏色傳達訊息。`test_top4_known_limitation_documented` 持續追蹤這個限制，若未來色票調整使限制消失，此測試會自動失敗以提醒更新指引。

## 修改色票時的工作流程

1. 編輯 `scripts/epidemic_palette.py`
2. 執行測試：`python tests/test_palette.py`
3. 若有失敗，依失敗訊息修正色票或修正測試門檻
4. 同步更新 `epidemic-dataviz-palette.csv` 與 `epidemic-dataviz-theme.json`
5. 重新執行測試以確認跨檔案一致
6. 重新生成範例 PNG：`python scripts/generate_examples.py`

## CI 整合

若要在 CI 中執行（例如 GitHub Actions）：

```yaml
- name: Run palette tests
  run: |
    pip install pytest matplotlib
    python -m pytest tests/test_palette.py -v
```

退出碼：0 = 全部通過，1 = 有失敗（CI 應視為失敗）。

## 擴充測試

要加入新測試：

1. 在 `test_palette.py` 中的對應 `TestXxx` 類別內加方法
2. 方法名稱以 `test_` 開頭
3. 使用 `assert` 與清楚的錯誤訊息
4. 涉及多參數的測試用 `@pytest.mark.parametrize`（standalone 模式也支援）
5. 跨檔案的測試請放 `TestCrossFileConsistency`
