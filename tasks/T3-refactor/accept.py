"""T3 受入テスト: Cart の公開 API 互換 + TestCart スイート全パス
usage: python accept.py <workdir>
"""
import json
import subprocess
import sys
import unittest
from pathlib import Path


def check_api(workdir: Path) -> tuple[bool, str]:
    sys.path.insert(0, str(workdir))
    try:
        for m in list(sys.modules):
            if m.startswith("omise"):
                del sys.modules[m]
        from omise.cart import Cart
        from omise.models import Product

        apple, orange = Product("りんご", 100), Product("みかん", 80)
        cart = Cart()
        cart.add(apple, 3)
        cart.add(orange, 2)
        assert cart.count() == 5
        assert cart.count(apple) == 3
        assert cart.quantities() == {"りんご": 3, "みかん": 2}
        assert cart.subtotal() == 460
        cart.remove(apple)
        assert cart.count(apple) == 2
        try:
            cart.add(apple, 0)
            return False, "add(quantity=0) が ValueError を投げない"
        except ValueError:
            pass
        return True, "ok"
    except AssertionError as e:
        return False, f"assertion failed: {e}"
    except Exception as e:  # noqa: BLE001
        return False, f"{type(e).__name__}: {e}"
    finally:
        sys.path.remove(str(workdir))


def run_cart_tests(workdir: Path) -> tuple[bool, str]:
    proc = subprocess.run(
        [sys.executable, "-m", "unittest", "tests.test_omise.TestCart", "-v"],
        cwd=workdir, capture_output=True, text=True, encoding="utf-8", errors="replace",
    )
    return proc.returncode == 0, (proc.stdout or "") + (proc.stderr or "")


def main() -> None:
    workdir = Path(sys.argv[1]).resolve()
    api_ok, api_detail = check_api(workdir)
    suite_ok, suite_log = run_cart_tests(workdir)
    verdict = {
        "pass": api_ok and suite_ok,
        "api_compatible": api_ok,
        "api_detail": api_detail,
        "cart_suite_pass": suite_ok,
    }
    print(json.dumps(verdict, ensure_ascii=False, indent=2))
    sys.exit(0 if verdict["pass"] else 1)


if __name__ == "__main__":
    main()
