from calc import add, discount, mul, sub


def test_add():
    assert add(2, 3) == 5


def test_sub():
    assert sub(10, 4) == 6


def test_mul():
    assert mul(3, 4) == 12


def test_discount():
    # 20% off a price of 100 should leave 80
    assert discount(100, 0.2) == 80
