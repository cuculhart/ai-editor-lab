"""T1 受入テスト: テスト未改変 + 全テストパス
usage: python accept.py <workdir>
"""
import json
import subprocess
import sys
from pathlib import Path

FIXTURE = Path(__file__).resolve().parents[2] / "fixture"


def run_unittest(workdir: Path) -> tuple[bool, str]:
    proc = subprocess.run(
        [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-t", "."],
        cwd=workdir, capture_output=True, text=True, encoding="utf-8", errors="replace",
    )
    return proc.returncode == 0, (proc.stdout or "") + (proc.stderr or "")


def check_tests_unmodified(workdir: Path) -> list[str]:
    modified = []
    for orig in (FIXTURE / "tests").rglob("*.py"):
        rel = orig.relative_to(FIXTURE)
        mine = workdir / rel
        if not mine.exists() or mine.read_bytes() != orig.read_bytes():
            modified.append(str(rel))
    return modified


def main() -> None:
    workdir = Path(sys.argv[1]).resolve()
    modified = check_tests_unmodified(workdir)
    ok, log = run_unittest(workdir)
    verdict = {
        "pass": ok and not modified,
        "tests_unmodified": not modified,
        "modified_files": modified,
        "all_tests_pass": ok,
    }
    print(json.dumps(verdict, ensure_ascii=False, indent=2))
    sys.exit(0 if verdict["pass"] else 1)


if __name__ == "__main__":
    main()
