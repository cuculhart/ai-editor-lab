"""商品モデル"""


class Product:
    def __init__(self, name: str, price: int) -> None:
        self.name = name
        self.price = price

    def __hash__(self) -> int:
        return hash((self.name, self.price))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Product):
            return NotImplemented
        return self.name == other.name and self.price == other.price

    def __repr__(self) -> str:
        return f"Product(name={self.name!r}, price={self.price!r})"
