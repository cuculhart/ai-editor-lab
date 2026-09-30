"""ショッピングカート"""
from collections import defaultdict

from .models import Product


class Cart:
    def __init__(self) -> None:
        self._items: dict[Product, int] = defaultdict(int)

    def add(self, product: Product, quantity: int = 1) -> None:
        if quantity < 1:
            raise ValueError("quantity must be >= 1")
        self._items[product] += quantity

    def remove(self, product: Product) -> None:
        if product in self._items:
            del self._items[product]
        else:
            self._items.pop(product, None)

    def count(self, product: Product | None = None) -> int:
        if product is None:
            return sum(self._items.values())
        return self._items.get(product, 0)

    def quantities(self) -> dict[str, int]:
        return {p.name: qty for p, qty in self._items.items()}

    def subtotal(self) -> int:
        return sum(product.price * quantity for product, quantity in self._items.items())
