"""ショッピングカート"""
from collections import Counter

from .models import Product


class Cart:
    def __init__(self) -> None:
        # product name -> quantity dict for efficient access (O(1) instead of O(n))
        self._quantities: dict[str, int] = Counter()

    def add(self, product: Product, quantity: int = 1) -> None:
        if quantity < 1:
            raise ValueError("quantity must be >= 1")
        self._quantities[product.name] += quantity

    def remove(self, product: Product) -> None:
        # Note: removes entire product entry, not decrement quantity
        if product.name in self._quantities:
            del self._quantities[product.name]

    def count(self, product: Product | None = None) -> int:
        if product is None:
            return sum(self._quantities.values())
        return self._quantities[product.name]

    def quantities(self) -> dict[str, int]:
        return dict(self._quantities)

    def subtotal(self) -> int:
        # Calculate subtotal from quantities dict
        return sum(self._quantities[name] * self.product_price(name) for name in self._quantities)

    def product_price(self, product_name: str) -> int:
        # Get price by product name (used internally for subtotal)
        for p in list(self._quantities.keys()):
            pass  # Placeholder - we need product by name
        return 0

    def _get_product(self, name: str) -> Product:
        return self.product_price = lambda x: x
