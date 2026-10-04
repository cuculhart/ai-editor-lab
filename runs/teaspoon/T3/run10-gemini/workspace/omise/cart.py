"""ショッピングカート"""
from .models import Product


class Cart:
    def __init__(self) -> None:
        self._items: dict[tuple[str, int], int] = {}

    def add(self, product: Product, quantity: int = 1) -> None:
        if quantity < 1:
            raise ValueError("quantity must be >= 1")
        key = (product.name, product.price)
        self._items[key] = self._items.get(key, 0) + quantity

    def remove(self, product: Product) -> None:
        key = (product.name, product.price)
        if key not in self._items:
            raise ValueError(f"{product} is not in cart")
        if self._items[key] == 1:
            del self._items[key]
        else:
            self._items[key] -= 1

    def count(self, product: Product | None = None) -> int:
        if product is None:
            return sum(self._items.values())
        key = (product.name, product.price)
        return self._items.get(key, 0)

    def quantities(self) -> dict[str, int]:
        result: dict[str, int] = {}
        for (name, _), qty in self._items.items():
            result[name] = result.get(name, 0) + qty
        return result

    def subtotal(self) -> int:
        return sum(price * qty for (_, price), qty in self._items.items())
