"""ショッピングカート"""
from .models import Product


class Cart:
    def __init__(self) -> None:
        self._items: list[tuple[Product, int]] = []

    def add(self, product: Product, quantity: int = 1) -> None:
        if quantity < 1:
            raise ValueError("quantity must be >= 1")
        for i, (p, q) in enumerate(self._items):
            if p == product:
                self._items[i] = (p, q + quantity)
                return
        self._items.append((product, quantity))

    def remove(self, product: Product) -> None:
        for i, (p, q) in enumerate(self._items):
            if p == product:
                if q > 1:
                    self._items[i] = (p, q - 1)
                else:
                    self._items.pop(i)
                return
        self._items.remove(product)  # 元のリストと同様に ValueError を発生させるため

    def count(self, product: Product | None = None) -> int:
        if product is None:
            return sum(q for _, q in self._items)
        return sum(q for p, q in self._items if p == product)

    def quantities(self) -> dict[str, int]:
        result: dict[str, int] = {}
        for p, q in self._items:
            result[p.name] = result.get(p.name, 0) + q
        return result

    def subtotal(self) -> int:
        return sum(p.price * q for p, q in self._items)
