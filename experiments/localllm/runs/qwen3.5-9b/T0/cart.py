"""Shopping cart built on the calc helpers."""

from calc import discount, mul


class Cart:
    def __init__(self):
        self.items = []  # list of (name, price, qty)

    def add_item(self, name, price, qty=1):
        self.items.append((name, price, qty))

    def subtotal(self):
        """Sum of price*qty over all items."""
        return sum(mul(price, qty) for _, price, qty in self.items)

    def total(self, member_discount=0.0):
        """Total after applying the member discount rate."""
        return discount(self.subtotal(), member_discount)
