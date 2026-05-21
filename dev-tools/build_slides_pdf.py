"""
build_slides_pdf.py — 投影片版指引產製

工作流程:
  1. 讀 docs/guideline-slides-summary.html(14 張,handwritten source)
  2. 讀 docs/_slides-extra.html(10 張補充 sections,handwritten source)
  3. 按 MANIFEST 合併 → 產生 docs/guideline-slides-full.html(22 張)
  4. 為兩個 HTML 內嵌 Chart.js(避免 PDF 渲染受 CDN 阻擋)
  5. 用 Playwright 以 1280×720 landscape 渲染:
        docs/guideline-slides-summary.pdf
        docs/guideline-slides-full.pdf

執行方式(從 repo 根目錄):
    python dev-tools/build_slides_pdf.py

只生成 HTML(不渲染 PDF,適合 chromium 裝不下的環境):
    python dev-tools/build_slides_pdf.py --html-only

首次使用需安裝相依:
    pip install playwright
    playwright install chromium

設計決策:
  - 摘要版 HTML 是手寫的 standalone artifact,maintainer 可直接編輯
  - 完整版 HTML 是 generated artifact,**不要手動編輯**
    (修改摘要 slide 內容 → 改 summary HTML;
     修改補充 slide 內容 → 改 _slides-extra.html)
  - 完整版的頁碼由 build script 自動填入,所以兩個 source 內
    可用 placeholder `__P__ / __T__` 或寫死的「NN / 14」
    都會被 build script 統一覆寫
"""
from __future__ import annotations

import argparse
import re
import sys
import time
from pathlib import Path

# ============== 路徑 ==============
HERE = Path(__file__).resolve().parent
REPO_ROOT = HERE.parent
DOCS = REPO_ROOT / "docs"

SUMMARY_HTML = DOCS / "guideline-slides-summary.html"
EXTRA_HTML = DOCS / "_slides-extra.html"
FULL_HTML = DOCS / "guideline-slides-full.html"

SUMMARY_PDF = DOCS / "guideline-slides-summary.pdf"
FULL_PDF = DOCS / "guideline-slides-full.pdf"

CHARTJS = HERE / "chart.umd.js"

CHARTJS_CDN_PATTERN = (
    '<script src="https://cdn.jsdelivr.net/npm/'
    'chart.js@4.4.0/dist/chart.umd.min.js"></script>'
)

# ============== 完整版合併 manifest ==============
# 22 張 = 完整版封面(extra 0)
#       + 摘要 1-12(原則 → 無障礙)
#       + 補充 1-8(序列色階 → AI agent)
#       + 完整版收尾(extra 9)
FULL_MANIFEST = {
    "summary_slice_a": (1, 13),   # 摘要 idx 1..12 (Python slice 1:13)
    "extra_cover": 0,             # 完整封面
    "extra_supplements": (1, 9),  # extra idx 1..8
    "extra_closing": 9,           # 完整收尾
}


# ============== 工具函式 ==============

SECTION_RE = re.compile(
    r'<section class="slide[^"]*"[^>]*>.*?</section>',
    re.DOTALL,
)


def extract_sections(html: str) -> list[str]:
    """從 HTML 抽取所有 <section class="slide ..."> ... </section>"""
    return SECTION_RE.findall(html)


def renumber_section(section_html: str, page_num: int, total: int) -> str:
    """覆寫 section 的 .num 與 footer 內的頁碼,統一為 NN / TT 格式"""
    nn = f"{page_num:02d}"
    tt = f"{total:02d}"

    # 1. 覆寫標題列的 .num span (允許 0+ 個空白或原內容)
    section_html = re.sub(
        r'(<span class="num">)[^<]*(</span>)',
        rf'\g<1>{nn} / {tt}\g<2>',
        section_html,
    )
    # 2. 覆寫 footer 的 "Page NN / NN"
    section_html = re.sub(
        r'(<span>)(?:Page\s*)?(?:__P__|\d+)\s*/\s*(?:__T__|\d+)(</span>)',
        rf'\g<1>Page {nn} / {tt}\g<2>',
        section_html,
    )
    return section_html


def html_shell(title: str, body: str) -> str:
    """產生完整版 HTML shell(與 summary HTML 結構相同)"""
    return f"""<!DOCTYPE html>
<html lang="zh-Hant">
<head>
<meta charset="UTF-8">
<title>{title}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Noto+Serif+TC:wght@400;600;700&family=Noto+Sans+TC:wght@300;400;500;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="_slides.css">
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
<!--
  自動生成的檔案 —— 請勿手動編輯。
  source: docs/guideline-slides-summary.html + docs/_slides-extra.html
  builder: dev-tools/build_slides_pdf.py
-->
</head>
<body>

{body}

</body>
</html>
"""


def extract_summary_scripts(html: str) -> str:
    """從摘要 HTML 提取 <script> 區塊(Chart.js 設定),保留給完整版用"""
    # 找最後一個 </section> 之後到 </body> 之間的內容
    match = re.search(
        r'</section>\s*(<!--.*?-->\s*)*(<script>.*?</script>)\s*</body>',
        html,
        re.DOTALL,
    )
    if match:
        return match.group(2)
    return ""


# ============== 步驟 1:合併產生完整版 HTML ==============

def build_full_html() -> None:
    print("[1/3] 合併產生完整版 HTML")

    summary_html = SUMMARY_HTML.read_text(encoding="utf-8")
    extra_html = EXTRA_HTML.read_text(encoding="utf-8")

    summary_sections = extract_sections(summary_html)
    extra_sections = extract_sections(extra_html)

    if len(summary_sections) != 14:
        print(f"  ⚠ 警告:摘要 HTML 預期 14 張,實際 {len(summary_sections)} 張")
    if len(extra_sections) != 10:
        print(f"  ⚠ 警告:extra HTML 預期 10 張,實際 {len(extra_sections)} 張")

    # 按 manifest 組合
    full_sections = (
        [extra_sections[FULL_MANIFEST["extra_cover"]]]
        + summary_sections[slice(*FULL_MANIFEST["summary_slice_a"])]
        + extra_sections[slice(*FULL_MANIFEST["extra_supplements"])]
        + [extra_sections[FULL_MANIFEST["extra_closing"]]]
    )
    total = len(full_sections)
    print(f"      合併後 {total} 張 slide")

    # 重新編號
    renumbered = [
        renumber_section(s, idx, total)
        for idx, s in enumerate(full_sections, start=1)
    ]

    # 取得 Chart.js 設定
    scripts = extract_summary_scripts(summary_html)

    body = "\n\n".join(renumbered)
    if scripts:
        body += "\n\n" + scripts

    html = html_shell("疫情資料視覺化指引 — 完整版投影片", body)
    FULL_HTML.write_text(html, encoding="utf-8")
    print(f"      ✓ 輸出: {FULL_HTML.relative_to(REPO_ROOT)}")

    # 同時也對 summary HTML 做頁碼正規化(統一格式),寫回原檔
    summary_resections = extract_sections(summary_html)
    summary_total = len(summary_resections)
    renum_summary = [
        renumber_section(s, idx, summary_total)
        for idx, s in enumerate(summary_resections, start=1)
    ]
    # 替換 summary HTML 中的 sections
    new_summary = summary_html
    for old, new in zip(summary_resections, renum_summary):
        new_summary = new_summary.replace(old, new, 1)
    SUMMARY_HTML.write_text(new_summary, encoding="utf-8")
    print(f"      ✓ 正規化頁碼: {SUMMARY_HTML.relative_to(REPO_ROOT)}")


# ============== 步驟 2:Chart.js 內嵌 ==============

def embed_chartjs(src_path: Path) -> Path:
    """把 chart.umd.js 內嵌進 HTML,輸出暫存檔"""
    if not CHARTJS.exists():
        raise FileNotFoundError(
            f"Chart.js 不存在: {CHARTJS}\n"
            f"  應與 build_pdf.py 共用同一個 chart.umd.js"
        )
    html = src_path.read_text(encoding="utf-8")
    if CHARTJS_CDN_PATTERN not in html:
        # 不含 Chart.js 引用,直接返回原檔
        return src_path
    chartjs = CHARTJS.read_text(encoding="utf-8")
    new_html = html.replace(
        CHARTJS_CDN_PATTERN,
        f"<script>/* Chart.js 4.4.0 embedded */\n{chartjs}\n</script>",
    )
    embedded = src_path.with_suffix(".embedded.html")
    embedded.write_text(new_html, encoding="utf-8")
    return embedded


# ============== 步驟 3:Playwright 渲染 PDF ==============

def render_pdf(src_html: Path, out_pdf: Path) -> None:
    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        browser = p.chromium.launch()
        ctx = browser.new_context(
            viewport={"width": 1280, "height": 720},
            device_scale_factor=2,
        )
        page = ctx.new_page()
        page.goto(f"file://{src_html.absolute()}", wait_until="networkidle")

        # 等所有 Chart.js 完成繪製(若 HTML 含 canvas)
        has_canvas = page.evaluate(
            "document.querySelectorAll('canvas').length > 0"
        )
        if has_canvas:
            page.wait_for_function("""() => {
                if (typeof Chart === 'undefined') return false;
                const canvases = document.querySelectorAll('canvas');
                if (canvases.length === 0) return false;
                for (const c of canvases) {
                    const inst = Chart.getChart(c);
                    if (!inst) return false;
                }
                return true;
            }""", timeout=20000)
            time.sleep(2)  # 動畫緩衝

        page.emulate_media(media="print")
        page.pdf(
            path=str(out_pdf),
            width="1280px",
            height="720px",
            print_background=True,
            margin={"top": "0", "right": "0", "bottom": "0", "left": "0"},
            prefer_css_page_size=False,
        )
        browser.close()

    size_kb = out_pdf.stat().st_size / 1024
    print(f"      ✓ {out_pdf.relative_to(REPO_ROOT)} ({size_kb:.1f} KB)")


def render_pdfs() -> None:
    print("[2/3] 內嵌 Chart.js 並渲染 PDF")
    try:
        from playwright.sync_api import sync_playwright  # noqa: F401
    except ImportError:
        print("  ✗ 缺少 playwright。安裝方式:")
        print("      pip install playwright")
        print("      playwright install chromium")
        raise SystemExit(1)

    tmp_files: list[Path] = []
    for src, out in [(SUMMARY_HTML, SUMMARY_PDF), (FULL_HTML, FULL_PDF)]:
        embedded = embed_chartjs(src)
        if embedded != src:
            tmp_files.append(embedded)
        render_pdf(embedded, out)

    print("[3/3] 清理暫存檔")
    for t in tmp_files:
        if t.exists():
            t.unlink()
            print(f"      ✓ 移除: {t.name}")


# ============== 主流程 ==============

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--html-only", action="store_true",
        help="只產生完整版 HTML 與正規化頁碼,不渲染 PDF",
    )
    args = parser.parse_args()

    print(f"build_slides_pdf.py")
    print(f"  摘要源: {SUMMARY_HTML.relative_to(REPO_ROOT)}")
    print(f"  補充源: {EXTRA_HTML.relative_to(REPO_ROOT)}")
    print(f"  輸出 HTML: {FULL_HTML.relative_to(REPO_ROOT)}")
    if not args.html_only:
        print(f"  輸出 PDF:  {SUMMARY_PDF.relative_to(REPO_ROOT)}")
        print(f"            {FULL_PDF.relative_to(REPO_ROOT)}")
    print()

    build_full_html()

    if not args.html_only:
        render_pdfs()

    print("\n完成。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
