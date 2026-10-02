"""ショッピングカート"""
from dataclasses import dataclass

from .models import Product


@dataclass
class _CartEntry:
    product: Product
    quantity: int


class Cart:
    def __init__(self) -> None:
        self._items: dict[tuple[str, int], _CartEntry] = {}

    def add(self, product: Product, quantity: int = 1) -> None:
        if quantity < 1:
            raise ValueError("quantity must be >= 1")
        key = (product.name, product.price)
        if key in self._items:
            self._items[key].quantity += quantity
        else:
            self._items[key] = _CartEntry(product, quantity)

    def remove(self, product: Product) -> None:
        key = (product.name, product.price)
        if key not in self._items:
            raise ValueError(f"{product!r} not in cart")
        if self._items[key].quantity > 1:
            self._items[key].quantity -= 1
        else:
            del self._items[key]

    def count(self, product: Product | None = None) -> int:
        if product is None:
            return sum(entry.quantity for entry in self._items.values())
        key = (product.name, product.price)
        entry = self._items.get(key)
        return entry.quantity if entry is not None else 0

    def quantities(self) -> dict[str, int]:
        result: dict[str, int] = {}
        for entry in self._items.values():
            result[entry.product.name] = result.get(entry.product.name, 0) + entry.quantity
        return result

    def subtotal(self) -> int:
        return sum(entry.product.price * entry.quantity for entry in self._items.values())
