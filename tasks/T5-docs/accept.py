"""T5 受入テスト: README に必須節 + コード例 + 十分な分量
usage: python accept.py <workdir>
"""
import json
import sys
from pathlib import Path

REQUIRED_SECTIONS = ["概要", "インストール", "使い方", "テスト", "ライセンス"]
MIN_CHARS = 400


def main() -> None:
    workdir = Path(sys.argv[1]).resolve()
    readme = workdir / "README.md"
    if not readme.exists():
        print(json.dumps({"pass": False, "error": "README.md not found"}, ensure_ascii=False))
        sys.exit(1)
    text = readme.read_text(encoding="utf-8")
    missing = [s for s in REQUIRED_SECTIONS if s not in text]
    verdict = {
        "pass": not missing and len(text) >= MIN_CHARS and "```" in text,
        "missing_sections": missing,
        "char_count": len(text),
        "has_code_block": "```" in text,
    }
    print(json.dumps(verdict, ensure_ascii=False, indent=2))
    sys.exit(0 if verdict["pass"] else 1)


if __name__ == "__main__":
    main()
