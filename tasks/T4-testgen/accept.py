"""T4 受入テスト: 新規テストファイル + 3メソッド以上 + 全パス
usage: python accept.py <workdir>
"""
import importlib.util
import json
import sys
import unittest
from pathlib import Path

ORIGINAL_TESTS = {"test_omise.py", "__init__.py"}


def collect_new_tests(workdir: Path) -> tuple[list[str], unittest.TestSuite]:
    suite = unittest.TestSuite()
    loader = unittest.TestLoader()
    found = []
    for path in sorted((workdir / "tests").glob("test_*.py")):
        if path.name in ORIGINAL_TESTS:
            continue
        found.append(path.name)
        spec = importlib.util.spec_from_file_location(path.stem, path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        suite.addTests(loader.loadTestsFromModule(mod))
    return found, suite


def main() -> None:
    workdir = Path(sys.argv[1]).resolve()
    sys.path.insert(0, str(workdir))
    new_files, suite = collect_new_tests(workdir)
    count = suite.countTestCases()
    runner = unittest.TextTestRunner(stream=open("NUL", "w", encoding="utf-8") if sys.platform == "win32" else open("/dev/null", "w"))
    result = runner.run(suite)
    all_pass = result.wasSuccessful()
    verdict = {
        "pass": bool(new_files) and count >= 3 and all_pass,
        "new_test_files": new_files,
        "new_test_count": count,
        "new_tests_pass": all_pass,
    }
    print(json.dumps(verdict, ensure_ascii=False, indent=2))
    sys.exit(0 if verdict["pass"] else 1)


if __name__ == "__main__":
    main()
