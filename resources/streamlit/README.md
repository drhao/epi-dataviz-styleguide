# Streamlit 支援

在 [Streamlit](https://streamlit.io) 儀表板中套用疫情資料視覺化指引。

## 1. App 外觀（chrome）

把 [`config.toml`](./config.toml) 複製到你的專案：

```
my-dashboard/
├── .streamlit/
│   └── config.toml     ← 從這裡複製過去
└── app.py
```

`[theme]` 會把主色設為 Sage `#739A6D`，套用到互動元件、滑桿、選取狀態與連結。注意這只影響 app 外觀，**不影響圖表配色**——圖表需另外指定色彩（見下）。

## 2. 圖表配色

Streamlit 的原生 `st.bar_chart` / `st.line_chart` 使用自家配色，無法直接套用指引。請改用下列任一方式取得一致色彩。

### 做法 A：matplotlib（最完整，含 trailing MA、日期軸等輔助）

```python
import sys; sys.path.append("path/to/skill/scripts")
from epidemic_palette import apply_style, PRIMARY, PRIMARY_DARKER, trailing_ma
import matplotlib.pyplot as plt
import streamlit as st

apply_style()                       # 一次套用全部指引樣式
fig, ax = plt.subplots(figsize=(9, 4.5))
ax.bar(dates, cases, color=PRIMARY, width=0.75)
ax.plot(dates, trailing_ma(cases), color=PRIMARY_DARKER, linewidth=2.5)
st.pyplot(fig)
```

### 做法 B：Plotly

```python
import plotly.express as px
import streamlit as st
from epidemic_palette import CATEGORICAL

fig = px.bar(df, x="date", y="cases", color="region",
             color_discrete_sequence=CATEGORICAL)
st.plotly_chart(fig, use_container_width=True)
```

### 做法 C：Altair

```python
import altair as alt
import streamlit as st
from epidemic_palette import CATEGORICAL

chart = (
    alt.Chart(df)
    .mark_bar()
    .encode(x="date:T", y="cases:Q",
            color=alt.Color("region:N",
                            scale=alt.Scale(range=CATEGORICAL)))
)
st.altair_chart(chart, use_container_width=True)
```

## 重點

- 主色填色用 `PRIMARY` `#739A6D`；折線改用加深版 `LINE_COLORS["primary"]` `#5D7F58`。
- 紅色（`ACCENT["alert"]`）僅用於警示，不作一般類別色。
- 序數資料（嚴重度／劑次／波次）改用 `MONOCHROME` 單色色階。
- 完整色票與輔助函式見 [`skill/scripts/epidemic_palette.py`](../../skill/scripts/epidemic_palette.py)。
