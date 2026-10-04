"""ショッピングカート"""
from collections import Counter

from .models import Product


class Cart:
    def __init__(self) -> None:
        self._items: dict[tuple[str, int], tuple[Product, int]] = {}

    def add(self, product: Product, quantity: int = 1) -> None:
        if quantity < 1:
            raise ValueError("quantity must be >= 1")
        key = (product.name, product.price)
        if key in self._items:
            _, current_qty = self._items[key]
            self._items[key] = (product, current_qty + quantity)
        else:
            self._items[key] = (product, quantity)

    def remove(self, product: Product) -> None:
        key = (product.name, product.price)
        if key not in self._items:
            raise ValueError(f"{product} not in cart")
        prod, qty = self._items[key]
        if qty > 1:
            self._items[key] = (prod, qty - 1)
        else:
            del self._items[key]

    def count(self, product: Product | None = None) -> int:
        if product is None:
            return sum(qty for _, qty in self._items.values())
        key = (product.name, product.price)
        if key in self._items:
            return self._items[key][1]
        return 0

    def quantities(self) -> dict[str, int]:
        counts: Counter[str] = Counter()
        for prod, qty in self._items.values():
            counts[prod.name] += qty
        return dict(counts)

    def subtotal(self) -> int:
        return sum(prod.price * qty for prod, qty in self._items.values())
