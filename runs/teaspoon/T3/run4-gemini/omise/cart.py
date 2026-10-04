"""ショッピングカート"""
from dataclasses import dataclass

from .models import Product


@dataclass
class _CartItem:
    product: Product
    quantity: int


def _item_key(product: Product) -> tuple[str, int, str]:
    return (product.name, product.price, product.category)


class Cart:
    def __init__(self) -> None:
        self._items: dict[tuple[str, int, str], _CartItem] = {}

    def add(self, product: Product, quantity: int = 1) -> None:
        if quantity < 1:
            raise ValueError("quantity must be >= 1")
        key = _item_key(product)
        if key in self._items:
            self._items[key].quantity += quantity
        else:
            self._items[key] = _CartItem(product=product, quantity=quantity)

    def remove(self, product: Product) -> None:
        key = _item_key(product)
        if key not in self._items:
            raise ValueError(f"{product!r} not in cart")
        self._items[key].quantity -= 1
        if self._items[key].quantity == 0:
            del self._items[key]

    def count(self, product: Product | None = None) -> int:
        if product is None:
            return sum(item.quantity for item in self._items.values())
        key = _item_key(product)
        item = self._items.get(key)
        return item.quantity if item is not None else 0

    def quantities(self) -> dict[str, int]:
        result: dict[str, int] = {}
        for item in self._items.values():
            result[item.product.name] = result.get(item.product.name, 0) + item.quantity
        return result

    def subtotal(self) -> int:
        return sum(item.product.price * item.quantity for item in self._items.values())
