"""T2 受入テスト: points.py の earn_points が仕様通り + リグレッションなし
usage: python accept.py <workdir>
"""
import importlib
import json
import subprocess
import sys
import unittest
from pathlib import Path


def check_points(workdir: Path) -> tuple[bool, str]:
    sys.path.insert(0, str(workdir))
    try:
        for m in list(sys.modules):
            if m.startswith("omise"):
                del sys.modules[m]
        points = importlib.import_module("omise.points")
        cases = {1000: 10, 150: 1, 99: 0, 0: 0}
        for amount, expected in cases.items():
            got = points.earn_points(amount)
            if got != expected:
                return False, f"earn_points({amount}) -> {got} (expected {expected})"
        return True, "ok"
    except Exception as e:  # noqa: BLE001
        return False, f"{type(e).__name__}: {e}"
    finally:
        sys.path.remove(str(workdir))


def run_unittest(workdir: Path) -> tuple[bool, str]:
    proc = subprocess.run(
        [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-t", "."],
        cwd=workdir, capture_output=True, text=True, encoding="utf-8", errors="replace",
    )
    out = (proc.stdout or "") + (proc.stderr or "")
    # T1 の埋め込みバグ由来の失敗は除外（直しているなら尚良し）
    failures = [l for l in out.splitlines() if l.startswith(("FAIL:", "ERROR:"))]
    real_failures = [l for l in failures if "test_bulk_discount" not in l]
    return not real_failures, out


def main() -> None:
    workdir = Path(sys.argv[1]).resolve()
    points_ok, points_detail = check_points(workdir)
    tests_ok, _ = run_unittest(workdir)
    verdict = {
        "pass": points_ok and tests_ok,
        "points_api": points_ok,
        "points_detail": points_detail,
        "no_regression": tests_ok,
    }
    print(json.dumps(verdict, ensure_ascii=False, indent=2))
    sys.exit(0 if verdict["pass"] else 1)


if __name__ == "__main__":
    main()
