"""T6 受入テスト: 3ファイル構成の静的検証 + playwright があれば動的検証
usage: python accept.py <workdir>
"""
import json
import re
import sys
from pathlib import Path

REQUIRED_FILES = ["index.html", "style.css", "script.js"]
REQUIRED_IDS = ["start-button", "score", "timer"]
CDN_PATTERNS = [r"src=\"https?://", r"src='https?://", r"href=\"https?://", r"href='https?://",
                r"@import", r"import\s+.*from\s+['\"]https?://"]


def static_checks(workdir: Path) -> dict:
    result = {}
    for f in REQUIRED_FILES:
        result[f"exists_{f}"] = (workdir / f).is_file()
    if not all(result.values()):
        result["fatal"] = "required files missing"
        return result

    html = (workdir / "index.html").read_text(encoding="utf-8", errors="replace")
    css = (workdir / "style.css").read_text(encoding="utf-8", errors="replace")
    js = (workdir / "script.js").read_text(encoding="utf-8", errors="replace")

    result["links_css"] = "style.css" in html
    result["links_js"] = "script.js" in html
    for rid in REQUIRED_IDS:
        result[f"id_{rid}"] = rid in html
    result["has_cells"] = "cell" in html or "cell" in js
    result["has_mole"] = "mole" in html or "mole" in js
    result["has_handler"] = bool(re.search(r"addEventListener|onclick", js))
    result["no_external"] = not any(
        re.search(p, html) for p in CDN_PATTERNS
    )
    result["js_nonempty"] = len(js.strip()) > 100
    result["css_nonempty"] = len(css.strip()) > 0
    return result


def dynamic_checks(workdir: Path) -> dict:
    """playwright があれば実際に操作して検証。なければ skipped を返す"""
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        return {"skipped": "playwright not installed"}

    checks = {"mole_appears": False, "score_increments": False}
    # 透明(opacity:0)・visibility:hidden・display:none をすべて除外して
    # 「ユーザーから本当に見えているモグラ」の DOM index を返す
    find_visible_js = """() => {
        const moles = [...document.querySelectorAll('.mole')];
        return moles.findIndex(m => {
            const s = getComputedStyle(m);
            if (s.display === 'none' || s.visibility === 'hidden' || parseFloat(s.opacity) < 0.5) return false;
            const r = m.getBoundingClientRect();
            return r.width > 0 && r.height > 0;
        });
    }"""
    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch()
            page = browser.new_page()
            page.goto((workdir / "index.html").resolve().as_uri())
            page.click("#start-button")
            def stable_visible_idx() -> int:
                """連続2回ポーリングで見え続けているモグラのみ（フェード中を除外）"""
                a = page.evaluate(find_visible_js)
                if a < 0:
                    return -1
                page.wait_for_timeout(120)
                b = page.evaluate(find_visible_js)
                return a if a == b else -1

            # モグラ出現を待つ
            for _ in range(30):
                if stable_visible_idx() >= 0:
                    checks["mole_appears"] = True
                    break
                page.wait_for_timeout(400)
            # モグラが消えるタイミングとの競合を避けるため複数回試行する
            for _ in range(15):
                idx = stable_visible_idx()
                if idx >= 0:
                    checks["mole_appears"] = True
                    try:
                        page.locator(".mole").nth(idx).click(timeout=1500)
                    except Exception:
                        pass
                text = page.inner_text("#score") or "0"
                digits = re.sub(r"\D", "", text)
                if digits and int(digits) >= 1:
                    checks["score_increments"] = True
                    break
                page.wait_for_timeout(300)
            browser.close()
    except Exception as e:  # noqa: BLE001
        checks["error"] = f"{type(e).__name__}: {e}"
    return checks


def main() -> None:
    workdir = Path(sys.argv[1]).resolve()
    static = static_checks(workdir)
    static_pass = all(v is True for k, v in static.items() if not k.startswith("fatal"))
    dynamic = dynamic_checks(workdir) if static_pass else {"skipped": "static failed"}
    dynamic_pass = dynamic.get("skipped") is not None or (
        dynamic.get("mole_appears") and dynamic.get("score_increments")
    )
    verdict = {
        "pass": bool(static_pass and dynamic_pass),
        "static": static,
        "dynamic": dynamic,
    }
    print(json.dumps(verdict, ensure_ascii=False, indent=2))
    sys.exit(0 if verdict["pass"] else 1)


if __name__ == "__main__":
    main()
