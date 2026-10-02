import unittest

from omise.cart import Cart
from omise.checkout import total_with_tax
from omise.discount import apply_bulk_discount, bulk_discount_rate
from omise.models import Product
from omise.points import earn_points


class TestCart(unittest.TestCase):
    def test_add_and_count(self):
        cart = Cart()
        apple = Product("りんご", 100)
        cart.add(apple, 3)
        self.assertEqual(cart.count(), 3)
        self.assertEqual(cart.count(apple), 3)

    def test_subtotal(self):
        cart = Cart()
        cart.add(Product("りんご", 100), 2)
        cart.add(Product("みかん", 80), 1)
        self.assertEqual(cart.subtotal(), 280)

    def test_add_invalid_quantity(self):
        cart = Cart()
        with self.assertRaises(ValueError):
            cart.add(Product("りんご", 100), 0)


class TestDiscount(unittest.TestCase):
    def test_bulk_discount_boundary(self):
        """3個ちょうどでも10%引きになること（境界値）"""
        self.assertEqual(bulk_discount_rate(3), 0.10)

    def test_bulk_discount_none(self):
        self.assertEqual(bulk_discount_rate(2), 0.0)

    def test_apply_bulk_discount(self):
        self.assertEqual(apply_bulk_discount(100, 4), 360)


class TestCheckout(unittest.TestCase):
    def test_total_with_tax(self):
        self.assertEqual(total_with_tax(1000), 1100)


class TestPoints(unittest.TestCase):
    def test_earn_points(self):
        self.assertEqual(earn_points(1000), 10)
        self.assertEqual(earn_points(150), 1)
        self.assertEqual(earn_points(99), 0)
        self.assertEqual(earn_points(0), 0)


if __name__ == "__main__":
    unittest.main()
