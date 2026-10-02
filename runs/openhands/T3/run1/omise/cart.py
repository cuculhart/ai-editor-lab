"""ショッピングカート"""
from .models import Product


class Cart:
    def __init__(self) -> None:
        self._items: dict[tuple[str, int], tuple[Product, int]] = {}

    def add(self, product: Product, quantity: int = 1) -> None:
        if quantity < 1:
            raise ValueError("quantity must be >= 1")
        key = (product.name, product.price)
        if key in self._items:
            _, qty = self._items[key]
            self._items[key] = (product, qty + quantity)
        else:
            self._items[key] = (product, quantity)

    def remove(self, product: Product) -> None:
        key = (product.name, product.price)
        if key not in self._items:
            raise ValueError("list.remove(x): x not in list")
        _, qty = self._items[key]
        if qty <= 1:
            del self._items[key]
        else:
            self._items[key] = (product, qty - 1)

    def count(self, product: Product | None = None) -> int:
        if product is None:
            return sum(qty for _, qty in self._items.values())
        key = (product.name, product.price)
        item = self._items.get(key)
        return item[1] if item else 0

    def quantities(self) -> dict[str, int]:
        res: dict[str, int] = {}
        for (name, _), (_, qty) in self._items.items():
            res[name] = res.get(name, 0) + qty
        return res

    def subtotal(self) -> int:
        return sum(product.price * qty for product, qty in self._items.values())
