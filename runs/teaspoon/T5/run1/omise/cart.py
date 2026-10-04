"""ショッピングカート"""
from collections import Counter

from .models import Product


class Cart:
    def __init__(self) -> None:
        self._items: list[Product] = []

    def add(self, product: Product, quantity: int = 1) -> None:
        if quantity < 1:
            raise ValueError("quantity must be >= 1")
        self._items.extend([product] * quantity)

    def remove(self, product: Product) -> None:
        self._items.remove(product)

    def count(self, product: Product | None = None) -> int:
        if product is None:
            return len(self._items)
        return self._items.count(product)

    def quantities(self) -> dict[str, int]:
        return dict(Counter(p.name for p in self._items))

    def subtotal(self) -> int:
        return sum(p.price for p in self._items)
