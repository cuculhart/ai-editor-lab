import unittest

from omise.cart import Cart
from omise.models import Product


class TestCartAdditional(unittest.TestCase):
    def test_remove_product(self):
        cart = Cart()
        apple = Product("りんご", 100)
        cart.add(apple, 2)
        cart.remove(apple)
        self.assertEqual(cart.count(apple), 1)
        self.assertEqual(cart.count(), 1)

    def test_quantities_mixed_products(self):
        cart = Cart()
        apple = Product("りんご", 100)
        banana = Product("バナナ", 150)
        cart.add(apple, 2)
        cart.add(banana, 3)
        qtys = cart.quantities()
        self.assertEqual(qtys, {"りんご": 2, "バナナ": 3})

    def test_mixed_products_subtotal_and_count(self):
        cart = Cart()
        apple = Product("りんご", 100)
        banana = Product("バナナ", 150)
        orange = Product("オレンジ", 120)
        cart.add(apple, 1)
        cart.add(banana, 2)
        cart.add(orange, 1)
        self.assertEqual(cart.count(), 4)
        self.assertEqual(cart.subtotal(), 100 + 150 * 2 + 120)


if __name__ == "__main__":
    unittest.main()
