"""Small arithmetic helpers shared by the cart module."""


def add(a, b):
    return a + b


def sub(a, b):
    return a - b


def mul(a, b):
    return a * b


def discount(price, rate):
    """Return the discounted price for a rate in [0, 1]."""
    return price * rate
