"""ショッピングカート"""
from .models import Product


class Cart:
    def __init__(self) -> None:
        self._items: list[tuple[Product, int]] = []

    def add(self, product: Product, quantity: int = 1) -> None:
        if quantity < 1:
            raise ValueError("quantity must be >= 1")
        for i, (item, qty) in enumerate(self._items):
            if item == product:
                self._items[i] = (item, qty + quantity)
                return
        self._items.append((product, quantity))

    def remove(self, product: Product) -> None:
        for i, (item, qty) in enumerate(self._items):
            if item == product:
                if qty > 1:
                    self._items[i] = (item, qty - 1)
                else:
                    self._items.pop(i)
                return
        raise ValueError(f"{product} not in cart")

    def count(self, product: Product | None = None) -> int:
        if product is None:
            return sum(qty for _, qty in self._items)
        for item, qty in self._items:
            if item == product:
                return qty
        return 0

    def quantities(self) -> dict[str, int]:
        result: dict[str, int] = {}
        for item, qty in self._items:
            result[item.name] = result.get(item.name, 0) + qty
        return result

    def subtotal(self) -> int:
        return sum(item.price * qty for item, qty in self._items)
