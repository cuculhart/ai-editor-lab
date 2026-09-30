import unittest

from omise.cart import Cart
from omise.models import Product


class TestCartExtended(unittest.TestCase):
    def test_remove_product(self):
        cart = Cart()
        apple = Product("りんご", 100)
        banana = Product("バナナ", 150)
        cart.add(apple, 2)
        cart.add(banana, 1)

        cart.remove(apple)
        self.assertEqual(cart.count(apple), 1)
        self.assertEqual(cart.count(), 2)
        self.assertEqual(cart.quantities(), {"りんご": 1, "バナナ": 1})
        self.assertEqual(cart.subtotal(), 250)

    def test_quantities_multiple_types(self):
        cart = Cart()
        apple = Product("りんご", 100)
        banana = Product("バナナ", 150)
        orange = Product("オレンジ", 120)

        cart.add(apple, 3)
        cart.add(banana, 2)
        cart.add(orange, 1)

        expected_quantities = {
            "りんご": 3,
            "バナナ": 2,
            "オレンジ": 1,
        }
        self.assertEqual(cart.quantities(), expected_quantities)

    def test_mixed_products_operations(self):
        cart = Cart()
        apple = Product("りんご", 100)
        banana = Product("バナナ", 150)

        cart.add(apple, 5)
        cart.add(banana, 3)
        self.assertEqual(cart.count(), 8)
        self.assertEqual(cart.subtotal(), 950)

        cart.remove(banana)
        self.assertEqual(cart.quantities(), {"りんご": 5, "バナナ": 2})
        self.assertEqual(cart.subtotal(), 800)

    def test_remove_nonexistent_product(self):
        cart = Cart()
        apple = Product("りんご", 100)
        with self.assertRaises(ValueError):
            cart.remove(apple)


if __name__ == "__main__":
    unittest.main()
