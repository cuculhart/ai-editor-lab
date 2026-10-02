"""ショッピングカート"""
from .models import Product


class Cart:
    def __init__(self) -> None:
        # Product オブジェクトをキー、数量を値とする辞書で管理
        self._items: dict[Product, int] = {}

    def add(self, product: Product, quantity: int = 1) -> None:
        if quantity < 1:
            raise ValueError("quantity must be >= 1")
        self._items[product] = self._items.get(product, 0) + quantity

    def remove(self, product: Product) -> None:
        if product in self._items:
            del self._items[product]
        else:
            raise KeyError(product)

    def count(self, product: Product | None = None) -> int:
        if product is None:
            return sum(self._items.values())
        return self._items.get(product, 0)

    def quantities(self) -> dict[str, int]:
        return {product.name: qty for product, qty in self._items.items()}

    def subtotal(self) -> int:
        return sum(product.price * qty for product, qty in self._items.items())
