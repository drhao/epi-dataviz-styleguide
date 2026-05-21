"""
build_pdf.py — 從 docs/guideline.html 重新生成 docs/guideline.pdf

兩步驟：
  1. 把 Chart.js (chart.umd.js) 內嵌進 HTML,避免 PDF 渲染時受 CDN 影響
  2. 用 Playwright 套用列印 CSS 並輸出 PDF

執行方式（從 repo 根目錄）：
    python dev-tools/build_pdf.py

或從 dev-tools/ 目錄：
    cd dev-tools && python build_pdf.py

首次使用需安裝相依：
    pip install playwright
    playwright install chromium
"""
from pathlib import Path
import sys
import time

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    print("✗ 缺少 playwright。安裝方式:")
    print("    pip install playwright")
    print("    playwright install chromium")
    sys.exit(1)


# ============== 路徑（相對於本檔案）==============
HERE = Path(__file__).resolve().parent
REPO_ROOT = HERE.parent
SRC_HTML = REPO_ROOT / "docs" / "guideline.html"
CHARTJS = HERE / "chart.umd.js"
EMBEDDED_HTML = HERE / "_embedded-guideline.html"  # 暫存檔
OUT_PDF = REPO_ROOT / "docs" / "guideline.pdf"


# ============== 列印專用 CSS ==============
PRINT_CSS = """
@page {
  size: A4;
  margin: 18mm 16mm 20mm 16mm;
  @bottom-center {
    content: "疫情資料視覺化指引  ／  Page " counter(page) " of " counter(pages);
    font-family: 'Noto Sans TC', sans-serif;
    font-size: 9pt;
    color: #7A8778;
  }
}

/* 隱藏側邊目錄欄 */
nav.toc { display: none !important; }
.shell {
  grid-template-columns: 1fr !important;
  gap: 0 !important;
  padding: 0 !important;
  max-width: 100% !important;
}

/* 縮小頁首區塊 */
.masthead { padding: 8px 0 !important; border-bottom-width: 2px !important; }
.masthead-inner { padding: 8px 16px !important; }
.hero { padding: 32px 0 24px !important; }
.hero::before { display: none !important; }
.hero-inner { padding: 0 16px !important; }
h1.hero-title { font-size: 32pt !important; }
.hero-lead { font-size: 12pt !important; }
.hero-stats {
  grid-template-columns: repeat(4, 1fr) !important;
  gap: 0 !important;
}
.hero-stat .num { font-size: 18pt !important; }

/* 主內容 */
main { padding: 16px 16px 24px !important; }
section.chapter { margin-bottom: 32px !important; }
.chapter-head { margin-bottom: 16px !important; padding-bottom: 10px !important; }
.chapter-head h2 { font-size: 22pt !important; }
.lead-para { font-size: 11pt !important; margin-bottom: 14px !important; }
p { font-size: 10.5pt !important; line-height: 1.55 !important; margin-bottom: 8px !important; }
h3 { font-size: 14pt !important; margin: 18px 0 8px !important; }
h4 { font-size: 11pt !important; margin: 12px 0 6px !important; }

/* 章節必定從新頁開始 */
section.chapter { page-break-before: always; }
section#ch1 { page-break-before: avoid; }  /* 第一章接續 hero */

/* 圖表卡片避免被切斷 */
.chart-card { page-break-inside: avoid; break-inside: avoid; }
.dd-card { page-break-inside: avoid; break-inside: avoid; }
.principle { page-break-inside: avoid; break-inside: avoid; }
.combo-card { page-break-inside: avoid; break-inside: avoid; }
table { page-break-inside: avoid; break-inside: avoid; }
pre.code { page-break-inside: avoid; break-inside: avoid; font-size: 8pt !important; }

/* 圖表 grid 縮小 gap */
.chart-grid { gap: 12px !important; }
.chart-card { padding: 14px !important; }
.chart-wrap { min-height: 200px !important; }
.chart-wrap.tall { min-height: 240px !important; }

/* 色卡縮小 */
.scale-grid { margin-bottom: 18px !important; }
.swatch { aspect-ratio: 1 / 1.5 !important; padding: 6px 4px !important; }
.swatch .step { font-size: 8pt !important; }
.swatch .hex { font-size: 7pt !important; }
.cat-chip .color { height: 50px !important; }
.cat-chip .meta { padding: 6px 8px 8px !important; }
.cat-chip .name { font-size: 10pt !important; }
.cat-chip .hex { font-size: 8pt !important; }

/* 表格字級 */
.matrix, .contrast-table { font-size: 9.5pt !important; }
.matrix th, .matrix td, .contrast-table th, .contrast-table td {
  padding: 8px 10px !important;
}
.matrix td:first-child { font-size: 10pt !important; }

/* Footer 列印時精簡（保留聯絡資訊,隱藏其他欄位） */
footer { 
  background: transparent !important;
  color: var(--n-700) !important;
  padding: 12px 16px 0 !important;
  border-top: 1px solid var(--n-300) !important;
  margin-top: 18px !important;
  page-break-before: avoid !important;
  page-break-inside: avoid !important;
}
footer * { color: var(--n-700) !important; }
footer a { color: var(--p-700) !important; text-decoration: underline !important; }
.foot-inner {
  display: block !important;
  grid-template-columns: none !important;
}
.foot-inner > div { display: none !important; }
.foot-inner > div:first-child { display: block !important; }  /* 只保留第一欄 */
footer h5 { font-size: 10pt !important; margin-bottom: 4px !important; }
footer p { font-size: 9pt !important; line-height: 1.5 !important; margin-bottom: 4px !important; }
"""


CHARTJS_CDN_PATTERN = (
    '<script src="https://cdn.jsdelivr.net/npm/'
    'chart.js@4.4.0/dist/chart.umd.min.js"></script>'
)


def step1_embed_chartjs() -> Path:
    """把 chart.umd.js 內嵌進 HTML,避免 PDF 渲染時受 CDN 影響"""
    print(f"[1/2] 嵌入 Chart.js 至 HTML")

    if not SRC_HTML.exists():
        raise FileNotFoundError(f"原始 HTML 不存在: {SRC_HTML}")
    if not CHARTJS.exists():
        raise FileNotFoundError(
            f"Chart.js 不存在: {CHARTJS}\n"
            f"  本檔案應與 build_pdf.py 同層,從 https://www.jsdelivr.com/"
            f"package/npm/chart.js 下載 4.4.0 版本"
        )

    html = SRC_HTML.read_text(encoding="utf-8")
    chartjs = CHARTJS.read_text(encoding="utf-8")

    if CHARTJS_CDN_PATTERN not in html:
        raise ValueError(
            f"在 HTML 中找不到 Chart.js CDN tag。預期格式:\n  {CHARTJS_CDN_PATTERN}\n"
            f"若 HTML 中的 Chart.js 載入方式有變,請更新本腳本的 CHARTJS_CDN_PATTERN。"
        )

    new_html = html.replace(
        CHARTJS_CDN_PATTERN,
        f"<script>/* Chart.js 4.4.0 embedded */\n{chartjs}\n</script>",
    )

    EMBEDDED_HTML.write_text(new_html, encoding="utf-8")
    print(f"      ✓ 嵌入版: {EMBEDDED_HTML.name} ({len(new_html):,} bytes)")
    return EMBEDDED_HTML


def step2_render_pdf(embedded_html: Path) -> Path:
    """用 Playwright 渲染為 PDF"""
    print(f"[2/2] 用 Playwright 渲染為 PDF")

    with sync_playwright() as p:
        browser = p.chromium.launch()
        ctx = browser.new_context(
            viewport={"width": 1280, "height": 1800},
            device_scale_factor=2,
        )
        page = ctx.new_page()

        page.goto(f"file://{embedded_html.absolute()}", wait_until="networkidle")
        page.add_style_tag(content=PRINT_CSS)

        # 等所有 Chart.js 完成繪製
        page.wait_for_function("""() => {
            if (typeof Chart === 'undefined') return false;
            const canvases = document.querySelectorAll('canvas');
            if (canvases.length === 0) return false;
            for (const c of canvases) {
                const inst = Chart.getChart(c);
                if (!inst) return false;
            }
            return true;
        }""", timeout=15000)
        time.sleep(3)  # 給動畫完成的緩衝

        page.emulate_media(media="print")
        page.pdf(
            path=str(OUT_PDF),
            format="A4",
            print_background=True,
            margin={"top": "0", "right": "0", "bottom": "0", "left": "0"},
            prefer_css_page_size=True,
        )
        browser.close()

    size_kb = OUT_PDF.stat().st_size / 1024
    print(f"      ✓ PDF 輸出: {OUT_PDF.relative_to(REPO_ROOT)} ({size_kb:.1f} KB)")
    return OUT_PDF


def cleanup():
    """清掉暫存檔"""
    if EMBEDDED_HTML.exists():
        EMBEDDED_HTML.unlink()
        print(f"      ✓ 清除暫存: {EMBEDDED_HTML.name}")


def main():
    print(f"build_pdf.py — 從 HTML 生成 PDF")
    print(f"  來源: {SRC_HTML.relative_to(REPO_ROOT)}")
    print(f"  輸出: {OUT_PDF.relative_to(REPO_ROOT)}")
    print()

    try:
        embedded = step1_embed_chartjs()
        step2_render_pdf(embedded)
        cleanup()
        print("\n完成。")
    except Exception as e:
        print(f"\n✗ 失敗: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
