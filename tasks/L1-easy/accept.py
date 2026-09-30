"""L1 受入テスト: calc.py / even_numbers の動作確認
usage: python accept.py <workdir>
"""
import importlib.util
import json
import sys
from pathlib import Path


def main() -> None:
    workdir = Path(sys.argv[1]).resolve()
    result = {"exists_calc.py": (workdir / "calc.py").is_file()}
    ok = False
    detail = ""
    if result["exists_calc.py"]:
        try:
            spec = importlib.util.spec_from_file_location("calc", workdir / "calc.py")
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            fn = mod.even_numbers
            cases = [
                ([3, 1, 4, 2], [2, 4]),
                ([], []),
                ([7, 5, 3], []),
                ([8, 2, 6, 4], [2, 4, 6, 8]),
                ([1, 2], [2]),
            ]
            bad = [(a, fn(list(a)), e) for a, e in cases if fn(list(a)) != e]
            ok = not bad
            detail = "ok" if ok else f"failed cases: {bad}"
        except Exception as e:  # noqa: BLE001
            detail = f"exec error: {type(e).__name__}: {e}"
    result["even_numbers"] = detail if detail else ("skipped" if not result["exists_calc.py"] else "ok")
    verdict = {"pass": bool(result["exists_calc.py"] and ok), "checks": result}
    print(json.dumps(verdict, ensure_ascii=False, indent=2))
    sys.exit(0 if verdict["pass"] else 1)


if __name__ == "__main__":
    main()
