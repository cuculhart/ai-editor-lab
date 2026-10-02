"""T3 受入テスト: Cart の公開 API 互換 + TestCart スイート全パス + 実質的なリファクタ
usage: python accept.py <workdir>
"""
import json
import subprocess
import sys
import unittest
from pathlib import Path

FIXTURE_CART = Path(__file__).resolve().parents[2] / "fixture" / "omise" / "cart.py"


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


def check_real_refactor(workdir: Path) -> tuple[bool, str]:
    """no-op 合格を防ぐ: ベースラインと同一ファイル、または内部が依然として
    「1個につき1要素」のリストなら不合格とする。"""
    cart_py = workdir / "omise" / "cart.py"
    if not cart_py.is_file():
        return False, "omise/cart.py が見つからない"
    if FIXTURE_CART.is_file() and cart_py.read_bytes() == FIXTURE_CART.read_bytes():
        return False, "cart.py がベースラインと同一(no-op)"

    sys.path.insert(0, str(workdir))
    try:
        for m in list(sys.modules):
            if m.startswith("omise"):
                del sys.modules[m]
        from omise.cart import Cart
        from omise.models import Product

        cart = Cart()
        cart.add(Product("りんご", 100), 5)
        try:
            internals = vars(cart)
        except TypeError:
            internals = {}
        for name, v in internals.items():
            if isinstance(v, list) and len(v) == 5:
                return False, f"内部属性 '{name}' が1個につき1要素のリストのまま(数量管理されていない)"
        return True, "ok"
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
    refactor_ok, refactor_detail = check_real_refactor(workdir)
    verdict = {
        "pass": api_ok and suite_ok and refactor_ok,
        "api_compatible": api_ok,
        "api_detail": api_detail,
        "cart_suite_pass": suite_ok,
        "real_refactor": refactor_ok,
        "refactor_detail": refactor_detail,
    }
    print(json.dumps(verdict, ensure_ascii=False, indent=2))
    sys.exit(0 if verdict["pass"] else 1)


if __name__ == "__main__":
    main()
