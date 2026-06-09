"""
check_drift.py — 跨檔案一致性檢查工具

掃描 repo 內各層級文件,檢查關鍵概念是否在應出現的所有地方都出現了。
這是 CONTRIBUTING.md 「Level 3 變動」階段四「跨文件 grep」的自動化版本。

執行方式（從 repo 根目錄）：
    python dev-tools/check_drift.py

或從 dev-tools/ 目錄：
    cd dev-tools && python check_drift.py

回傳 exit code:
    0 = 全部檢查通過
    1 = 有檢查項目失敗（顯示哪些檔案缺漏）
"""
from __future__ import annotations

import re
import sys
from dataclasses import dataclass, field
from pathlib import Path


# ============== 路徑設定 ==============
HERE = Path(__file__).resolve().parent
REPO_ROOT = HERE.parent


# ============== 三層文件定義 ==============
# 修改任何規範時,變動應該在這三層中對應的檔案都出現

L1_AUTHORITY = [   # AI agent 規範權威源
    "skill/SKILL.md",
    # references/ 為按需查閱,某些概念可能只出現在特定圖表規範中
]

L1_REFERENCES = [  # 圖表類型詳細規範（可選擇性檢查）
    "skill/references/01-bar-chart.md",
    "skill/references/02-line-chart.md",
    "skill/references/03-area-chart.md",
    "skill/references/04-stacked-chart.md",
    "skill/references/05-pie-chart.md",
    "skill/references/06-scatter-chart.md",
    "skill/references/07-histogram-boxplot.md",
    "skill/references/08-pyramid-chart.md",
    "skill/references/09-choropleth-map.md",
    "skill/references/10-monochrome-usage.md",
]

L2_HUMAN_DOCS = [  # 人類閱讀層
    "docs/guideline.md",
    "docs/guideline.html",
    # guideline.pdf 是從 HTML 生成,不單獨檢查
]

L3_PUBLIC = [      # 對外展示層
    "docs/index.html",
]


@dataclass
class Check:
    """單一檢查項目"""
    name: str                          # 檢查名稱
    keywords: list[str]                # 要找的關鍵字
    expected_in: list[str]             # 預期出現的檔案路徑列表
    description: str = ""              # 為什麼檢查這個
    optional_in: list[str] = field(default_factory=list)  # 出現也好,沒出現也 OK
    match_all: bool = False            # True = 每個關鍵字都要出現（值級一致性）；False = 任一出現即可


# ============== 檢查項目定義 ==============
# 新增規範時,在這裡加入對應的 Check,確保未來變動不會漏改

CHECKS = [
    Check(
        name="Pattern E / 模式 E（單色色階）",
        # SKILL.md 用英文 "Pattern E",中文文件用「模式 E」,部分用「單色色階」
        keywords=[
            "Pattern E", "模式 E", "PATTERN E",
            "monochrome", "Monochrome", "MONOCHROME", "單色色階", "單色 ",
        ],
        expected_in=[
            "skill/SKILL.md",
            "skill/references/10-monochrome-usage.md",
            "docs/guideline.md",
            "docs/guideline.html",
            "docs/index.html",
        ],
        description="單色色階配色模式必須在三層文件都有對應描述",
    ),
    Check(
        name="MONOCHROME 字典",
        keywords=["MONOCHROME", "MONO.scale", "MONO.focus"],
        expected_in=[
            "skill/scripts/epidemic_palette.py",
            "skill/SKILL.md",
            "skill/references/10-monochrome-usage.md",
            "skill/scripts/generate_examples.py",
        ],
        description="MONOCHROME 字典應在 Python 模組定義,並在 SKILL/references 文件化",
        optional_in=["docs/guideline.html"],  # HTML 中用 MONO 簡寫
    ),
    Check(
        name="主色 #739A6D",
        keywords=["#739A6D", "#739a6d"],
        expected_in=[
            "skill/scripts/epidemic_palette.py",
            "skill/scripts/epidemic_palette.R",
            "skill/SKILL.md",
            "docs/guideline.md",
            "docs/guideline.html",
            "docs/index.html",
            "resources/palette.csv",
            "resources/quarto/_brand.yml",
            "resources/quarto/epidemic.scss",
            "resources/streamlit/config.toml",
        ],
        description="主色 HEX 必須在所有色彩定義檔中一致出現（含 R / Quarto / Streamlit 交付檔）",
    ),
    Check(
        name="R / ggplot2 色票模組（epidemic_palette.R）",
        # R 支援的權威是實際模組檔，文件層以 theme_epi / scale_fill_epi 指稱
        keywords=["epidemic_palette.R", "theme_epi", "scale_fill_epi"],
        expected_in=[
            "skill/scripts/epidemic_palette.R",
            "skill/SKILL.md",
            "skill/SKILL-README.md",
            "docs/guideline.md",
            "docs/guideline.html",
            "README.md",
            "CHANGELOG.md",
        ],
        description="R / ggplot2 色票模組應在權威源、人類文件與對外文件一致出現",
    ),
    Check(
        name="Quarto 支援（_brand.yml / SCSS）",
        keywords=["Quarto", "_brand.yml", "epidemic.scss"],
        expected_in=[
            "resources/quarto/_brand.yml",
            "resources/quarto/epidemic.scss",
            "resources/quarto/README.md",
            "skill/SKILL.md",
            "docs/guideline.md",
            "docs/guideline.html",
            "README.md",
            "CHANGELOG.md",
        ],
        description="Quarto 工具支援必須在交付檔與各層文件一致出現",
    ),
    Check(
        name="Streamlit 支援（config.toml）",
        keywords=["Streamlit", "streamlit"],
        expected_in=[
            "resources/streamlit/config.toml",
            "resources/streamlit/README.md",
            "skill/SKILL.md",
            "docs/guideline.md",
            "docs/guideline.html",
            "README.md",
            "CHANGELOG.md",
        ],
        description="Streamlit 工具支援必須在交付檔與各層文件一致出現",
    ),
    Check(
        name="類別配色完整一致（R / Quarto 交付檔，值級）",
        # 全部 6 個類別 HEX 都必須出現，避免非主色（藍/黃/鴨綠/銅/梅）悄悄漂移。
        # config.toml 僅宣告主色，故不納入此檢查。
        keywords=[
            "#739A6D", "#587A9D", "#C8A041",
            "#49888D", "#916E46", "#955F71",
        ],
        match_all=True,
        expected_in=[
            "skill/scripts/epidemic_palette.R",
            "resources/quarto/_brand.yml",
            "resources/quarto/epidemic.scss",
        ],
        description=(
            "6 個類別配色 HEX 必須完整出現在 R / Quarto 交付檔。"
            "check_drift 對其他交付檔僅驗主色出現,此項補上值級一致性,"
            "與 test_palette.py 對 PowerBI 的逐色比對等強度。"
        ),
    ),
    Check(
        name="紅色僅警示（不可作類別色）",
        # SKILL.md 用 "Alert Red" / "warning only",中文用「紅色」「警示」
        keywords=[
            "紅色", "Alert Red", "alert_red", "ALERT_RED",
            "warning only", "for alerts", "exclusively for alerts",
        ],
        expected_in=[
            "skill/SKILL.md",
            "docs/guideline.md",
            "docs/guideline.html",
            "docs/index.html",
        ],
        description="紅色警示用途規範必須在三層文件都明示",
    ),
    Check(
        name="Trailing 7 日移動平均",
        # 移動平均主要規範在 01-bar-chart.md(每日新增直條加 MA 線)
        keywords=[
            "trailing_ma", "trailing 7",
            "i-6 到 i", "i-6 to i", "本日含前 6",
        ],
        expected_in=[
            "skill/SKILL.md",
            "skill/references/01-bar-chart.md",
            "skill/scripts/epidemic_palette.py",
            "docs/guideline.md",
            "docs/guideline.html",
        ],
        description="移動平均採 trailing 7 日(本日含前 6 日)的規範必須在多處提及",
    ),
    Check(
        name="Y 軸誠實呈現(直條必從零,折線視情境)",
        # SKILL.md §4.4 區分:Bar MUST start at zero; Line preferred but optional
        keywords=[
            "Y 軸", "Y-axis", "從零開始", "beginAtZero",
            "start at zero", "從 0 開始", "zero baseline",
            "直條圖 Y 軸",  # 精細化後的常見寫法
        ],
        expected_in=[
            "skill/SKILL.md",
            "docs/guideline.md",
            "docs/guideline.html",
            "docs/index.html",
        ],
        description=(
            "直條必從零(鐵則),折線/區域 zero baseline preferred but optional。"
            "若變化才是訊息(Rt、相對風險等),折線可從合理 lower bound 起算但須註明。"
        ),
    ),
    Check(
        name="WCAG AA 對比",
        keywords=["WCAG", "對比", "4.5:1", "3:1", "contrast"],
        expected_in=[
            "skill/SKILL.md",
            "docs/guideline.md",
            "docs/guideline.html",
            "docs/index.html",
            "skill/tests/test_palette.py",
        ],
        description="WCAG 無障礙標準必須在規範與測試中都覆蓋",
    ),
    Check(
        name="Office 樣板(內部,暫不對外發布)",
        keywords=["office-templates", "office_templates", "build_office_templates"],
        expected_in=[
            "skill/SKILL.md",
            "dev-tools/README.md",
            "CHANGELOG.md",
        ],
        description=(
            "Office 樣板目前僅供內部迭代,對外文件(README、docs/*)不應宣傳。"
            "若決定對外發布,把 README.md / docs/guideline.html / docs/index.html "
            "等加進 expected_in 並同步更新文件。"
        ),
    ),
    Check(
        name="投影片版指引",
        keywords=[
            "guideline-slides", "build_slides_pdf",
            "投影片版", "投影片摘要", "投影片完整",
            "slide-format", "slides-summary", "slides-full",
        ],
        expected_in=[
            "README.md",
            "skill/SKILL.md",
            "docs/index.html",
            "dev-tools/README.md",
            "CHANGELOG.md",
        ],
        description=(
            "投影片版 PDF(摘要 14 張 + 完整 22 張)為對外發布交付物,"
            "使用者面向文件(README、docs/index.html)與內部維護文件"
            "(SKILL.md、dev-tools/README.md、CHANGELOG.md)都應提及。"
        ),
    ),
    Check(
        name="聯絡資訊（Dr. Hao）",
        keywords=["Dr. Hao", "dr.hao.tw@gmail.com"],
        expected_in=[
            "README.md",
            "CONTRIBUTING.md",
            "docs/guideline.md",
            "docs/guideline.html",
            "docs/index.html",
        ],
        description="維護者聯絡資訊應在所有面向使用者的文件出現",
    ),
    Check(
        name="不確定性視覺化 modifier(M1)",
        keywords=[
            "M1-uncertainty-modifier",
            "uncertainty modifier",
            "不確定性視覺化",
            "預測區間",
            "PRIMARY_LIGHT, alpha",  # 漸層帶實作 signature
        ],
        expected_in=[
            "skill/SKILL.md",
            "skill/references/M1-uncertainty-modifier.md",
            "skill/references/02-line-chart.md",
            "skill/references/03-area-chart.md",
            "skill/references/01-bar-chart.md",
            "skill/references/06-scatter-chart.md",
            "skill/scripts/generate_examples.py",
            "CHANGELOG.md",
        ],
        description=(
            "M1 不確定性視覺化 modifier(RFC 2026-06-01,2026-06-09 採納為 Active)"
            "規範本身在 M1-uncertainty-modifier.md,SKILL.md decision tree 有對應分支,"
            "01/02/03/06 references 應有 cross-link 段。"
        ),
    ),
    Check(
        name="Small multiples layout modifier(M2)",
        keywords=[
            "M2-small-multiples",
            "small multiples",
            "Small multiples",
            "並排比較",
            "sharex=True, sharey=True",  # 規則 1+2 實作 signature
        ],
        expected_in=[
            "skill/SKILL.md",
            "skill/references/M2-small-multiples.md",
            "skill/references/02-line-chart.md",
            "skill/references/03-area-chart.md",
            "skill/references/01-bar-chart.md",
            "skill/references/M1-uncertainty-modifier.md",
            "skill/scripts/generate_examples.py",
            "CHANGELOG.md",
        ],
        description=(
            "M2 small multiples 版面 modifier(RFC 2026-06-02,2026-06-09 採納為 Active)"
            "規範本身在 M2-small-multiples.md,SKILL.md decision tree 有對應分支,"
            "02/03/01/M1 references 應有 cross-link 段。"
        ),
    ),
    Check(
        name="5 分鐘入門 by role(quickstart)",
        keywords=[
            "quickstart-by-role",
            "5 分鐘入門",
            "⚡ 5 分鐘",
        ],
        expected_in=[
            "docs/quickstart-by-role.md",
            "docs/index.html",
            "README.md",
            "CHANGELOG.md",
        ],
        description=(
            "依角色分流的 5 分鐘入門文件(設計師 / 工程師 / PM / 長官)。"
            "docs/index.html SECTION 02 與 audience cards、README.md 使用情境表"
            "應有 cross-link 指向 quickstart-by-role.md。"
        ),
    ),
    Check(
        name="Do/Don't 對照範例庫",
        keywords=[
            "dont-vs-do",
            "generate_dont_vs_do",
            "視覺對照圖",  # 各 reference cross-link 用語
        ],
        expected_in=[
            "skill/SKILL.md",
            "skill/scripts/generate_dont_vs_do.py",
            "skill/assets/examples/dont-vs-do/README.md",
            "skill/references/01-bar-chart.md",
            "skill/references/02-line-chart.md",
            "skill/references/05-pie-chart.md",
            "skill/references/M2-small-multiples.md",
            "docs/dont-vs-do.html",  # 線上展示頁
            "docs/guideline.html",   # Ch.9 callout 連結到展示頁
            "docs/index.html",       # 設計師卡片入口
            "CHANGELOG.md",
        ],
        description=(
            "Do/Don't 對照範例庫(L2 教學補充)。8 對 ✗/✓ 並排 PNG,"
            "對應既有規則。SKILL.md 提及目錄、各 reference 的「常見錯誤」"
            "段補 cross-link、生成腳本 + README + CHANGELOG 紀錄。"
        ),
    ),
    Check(
        name="重症在底（單色堆疊原則）",
        # SKILL.md 用英文 "darkest color at the base"
        keywords=[
            "重症在底", "最深色放底", "darkest at base",
            "darkest color at the base", "深色放在底", "stack base",
        ],
        expected_in=[
            "skill/SKILL.md",
            "skill/references/10-monochrome-usage.md",
            "docs/guideline.html",  # chart11 chart-meta 中提及
        ],
        description="單色堆疊「最深色放底部」規範應在規範與範例中提及",
    ),
]


# ============== 過時用詞檢查（黑名單）==============
# 當規範演進時,某些用詞被取代,確保舊用詞已全部移除

DEPRECATED_TERMS = [
    {
        "term": "centered_ma",
        "reason": "移動平均規範改為 trailing 7 日(本日含前 6 日),函式重命名為 trailing_ma()",
        "scope": ["**/*.md", "**/*.html", "**/*.py"],
    },
    {
        "term": "i-3 到 i+3",
        "reason": "centered MA 已改為 trailing(i-6 到 i)",
        "scope": ["**/*.md", "**/*.html", "**/*.py"],
    },
    {
        "term": "公部門",
        "reason": "所有說明文字不特別點明使用者身份;改用「正式報告/對外溝通/組織」等中性詞",
        "scope": ["**/*.md", "**/*.html", "**/*.py"],
    },
    {
        "term": "font-style: italic",
        "reason": "本指引網頁不使用斜體;HTML 與 CSS 一律避免",
        "scope": ["**/*.html", "**/*.css"],
    },
    {
        "term": "font-style:italic",
        "reason": "本指引網頁不使用斜體;HTML 與 CSS 一律避免",
        "scope": ["**/*.html", "**/*.css"],
    },
    {
        "term": "資料治理小組",
        "reason": "已取代為 Dr. Hao 聯絡資訊（2026.05 更新）",
        "scope": ["**/*.md", "**/*.html"],
    },
    {
        "term": "YOUR_ORG",
        "reason": "佔位符,應替換為實際 organization（drhao）",
        "scope": ["**/*.md", "**/*.html"],
    },
    {
        "term": "YOUR_USERNAME",
        "reason": "佔位符,應替換為實際 username",
        "scope": ["**/*.md", "**/*.html"],
    },
]


# ============== Reference frontmatter / RFC 試行狀態 ==============

def parse_frontmatter(path: Path) -> dict:
    """簡單 YAML frontmatter 解析(只支援 key: value 單行欄位)。"""
    try:
        text = path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, IsADirectoryError, FileNotFoundError):
        return {}
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---", 4)
    if end < 0:
        return {}
    body = text[4:end]
    result = {}
    for line in body.splitlines():
        if ":" in line:
            k, _, v = line.partition(":")
            result[k.strip()] = v.strip()
    return result


def report_draft_references() -> list[tuple[str, str]]:
    """列出 skill/references/ 內 status: draft 的規範。

    沒有 frontmatter 的 reference 視為 active(向後相容 pre-RFC 既有規範)。
    """
    refs_dir = REPO_ROOT / "skill" / "references"
    drafts = []
    if not refs_dir.exists():
        return drafts
    for md in sorted(refs_dir.glob("*.md")):
        fm = parse_frontmatter(md)
        if fm.get("status", "active").lower() == "draft":
            drafts.append((
                str(md.relative_to(REPO_ROOT)),
                fm.get("rfc", "?"),
            ))
    return drafts


# ============== 檢查邏輯 ==============

def file_contains_any(path: Path, keywords: list[str]) -> bool:
    """檔案是否包含任一關鍵字"""
    if not path.exists():
        return False
    try:
        content = path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, IsADirectoryError):
        return False
    return any(kw in content for kw in keywords)


def file_contains_all(path: Path, keywords: list[str]) -> bool:
    """檔案是否包含全部關鍵字（值級一致性檢查用）"""
    if not path.exists():
        return False
    try:
        content = path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, IsADirectoryError):
        return False
    return all(kw in content for kw in keywords)


def check_concept_coverage(check: Check) -> tuple[bool, list[str], list[str]]:
    """檢查單一概念在預期檔案中的覆蓋情況。回傳 (是否全部通過, 缺漏的檔案, 在 optional 中發現的檔案)"""
    missing = []
    optional_found = []
    contains = file_contains_all if check.match_all else file_contains_any

    for relpath in check.expected_in:
        path = REPO_ROOT / relpath
        if not contains(path, check.keywords):
            missing.append(relpath)

    for relpath in check.optional_in:
        path = REPO_ROOT / relpath
        if file_contains_any(path, check.keywords):
            optional_found.append(relpath)

    return len(missing) == 0, missing, optional_found


def check_deprecated_terms() -> list[tuple[str, str, list[str]]]:
    """掃描整個 repo 找過時用詞。回傳 [(term, reason, found_in_files)]"""
    findings = []
    for entry in DEPRECATED_TERMS:
        term = entry["term"]
        found_in = []
        # 掃描所有 md / html / py / css 檔案(排除 .git、本檔案、CHANGELOG)
        # CHANGELOG.md 內保留歷史條目作為演進記錄,故排除
        for ext in ("md", "html", "py", "css"):
            for path in REPO_ROOT.rglob(f"*.{ext}"):
                if ".git" in path.parts:
                    continue
                if path.name == "check_drift.py":
                    continue
                if path.name == "CHANGELOG.md":
                    continue
                try:
                    if term in path.read_text(encoding="utf-8"):
                        found_in.append(str(path.relative_to(REPO_ROOT)))
                except (UnicodeDecodeError, IsADirectoryError):
                    continue
        if found_in:
            findings.append((term, entry["reason"], found_in))
    return findings


# ============== 主流程 ==============

def main():
    print("=" * 60)
    print("檢查跨檔案規範一致性")
    print("=" * 60)
    print()

    total_checks = len(CHECKS)
    passed_checks = 0
    failed_details = []

    # === 概念覆蓋檢查 ===
    print(f"【概念覆蓋檢查】共 {total_checks} 項")
    print()
    for check in CHECKS:
        ok, missing, optional_found = check_concept_coverage(check)
        status = "✓" if ok else "✗"
        print(f"  {status} {check.name}")
        if not ok:
            print(f"      預期出現但缺漏：")
            for m in missing:
                print(f"        - {m}")
            failed_details.append(check)
        else:
            passed_checks += 1
        if optional_found:
            print(f"      （選擇性出現於：{', '.join(optional_found)}）")

    print()
    print(f"  通過 {passed_checks}/{total_checks}")
    print()

    # === Pilot 規範清單(RFC 試行階段) ===
    drafts = report_draft_references()
    if drafts:
        print("【Pilot 試行中的規範】")
        print()
        print(f"  以下 {len(drafts)} 個 reference 為 status: draft,SKILL.md decision tree 未更新")
        print("  AI agent 不主動套用。詳見 docs/rfcs/")
        print()
        for path, rfc in drafts:
            print(f"  ● {path}")
            print(f"      RFC: {rfc}")
        print()

    # === 過時用詞檢查 ===
    print("【過時用詞檢查】")
    print()
    deprecated_findings = check_deprecated_terms()
    if not deprecated_findings:
        print("  ✓ 沒有過時用詞殘留")
        print()
    else:
        print(f"  ✗ 發現 {len(deprecated_findings)} 個過時用詞殘留：")
        print()
        for term, reason, files in deprecated_findings:
            print(f"  • 「{term}」")
            print(f"      原因：{reason}")
            for f in files:
                print(f"      殘留於：{f}")
            print()

    # === 總結 ===
    print("=" * 60)
    all_passed = (passed_checks == total_checks) and (not deprecated_findings)
    if all_passed:
        print("✓ 所有檢查通過")
        print("=" * 60)
        return 0
    else:
        print("✗ 有檢查項目失敗,請依上方提示更新對應檔案")
        print()
        print("提示：")
        print("  - 若新增規範:在 CHECKS 列表中加入對應的 Check 項目")
        print("  - 若取代用詞:在 DEPRECATED_TERMS 中加入舊用詞")
        print("  - 修改完檔案後,重跑本腳本確認")
        print("=" * 60)
        return 1


if __name__ == "__main__":
    sys.exit(main())
