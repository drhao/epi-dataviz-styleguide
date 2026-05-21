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
    keywords: list[str]                # 要找的關鍵字（任一出現即視為「有提及」）
    expected_in: list[str]             # 預期出現的檔案路徑列表
    description: str = ""              # 為什麼檢查這個
    optional_in: list[str] = field(default_factory=list)  # 出現也好,沒出現也 OK


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
            "skill/SKILL.md",
            "docs/guideline.md",
            "docs/guideline.html",
            "docs/index.html",
            "resources/palette.csv",
        ],
        description="主色 HEX 必須在所有色彩定義檔中一致出現",
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
        name="中心對齊移動平均",
        # 移動平均主要規範在 01-bar-chart.md(每日新增直條加 MA 線)
        keywords=[
            "中心對齊", "centered_ma", "centered moving",
            "i-3 到 i+3", "centered (i-3 to i+3)",
        ],
        expected_in=[
            "skill/SKILL.md",
            "skill/references/01-bar-chart.md",
            "skill/scripts/epidemic_palette.py",
            "docs/guideline.md",
            "docs/guideline.html",
        ],
        description="移動平均的中心對齊規範必須在多處提及",
    ),
    Check(
        name="Y 軸從零開始",
        # SKILL.md 用英文 "Y-axis MUST start at zero"
        keywords=[
            "Y 軸", "Y-axis", "從零開始", "beginAtZero",
            "start at zero", "從 0 開始", "zero baseline",
        ],
        expected_in=[
            "skill/SKILL.md",
            "docs/guideline.md",
            "docs/guideline.html",
            "docs/index.html",
        ],
        description="Y 軸誠實呈現原則必須在多處強調",
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
        name="Office 樣板(office-templates)",
        keywords=["office-templates", "office_templates", "build_office_templates"],
        expected_in=[
            "README.md",
            "skill/SKILL.md",
            "docs/guideline.html",
            "docs/index.html",
            "dev-tools/README.md",
            "CHANGELOG.md",
        ],
        description="Excel/PPT 預生成樣板的入口提及必須在使用者面向文件都有,維護者面向(dev-tools/README)也要有",
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


def check_concept_coverage(check: Check) -> tuple[bool, list[str], list[str]]:
    """檢查單一概念在預期檔案中的覆蓋情況。回傳 (是否全部通過, 缺漏的檔案, 在 optional 中發現的檔案)"""
    missing = []
    optional_found = []

    for relpath in check.expected_in:
        path = REPO_ROOT / relpath
        if not file_contains_any(path, check.keywords):
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
        # 掃描所有 md / html 檔案（排除 .git 與本檔案）
        for ext in ("md", "html"):
            for path in REPO_ROOT.rglob(f"*.{ext}"):
                if ".git" in path.parts:
                    continue
                if path.name == "check_drift.py":
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
