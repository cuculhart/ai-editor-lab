import unittest

from omise.cart import Cart
from omise.models import Product


class TestCartAdditional(unittest.TestCase):
    def test_remove_product(self):
        cart = Cart()
        apple = Product("りんご", 100)
        banana = Product("バナナ", 80)
        cart.add(apple, 2)
        cart.add(banana, 1)
        
        cart.remove(apple)
        self.assertEqual(cart.count(apple), 1)
        self.assertEqual(cart.count(banana), 1)
        self.assertEqual(cart.subtotal(), 180)

    def test_quantities_mixed_products(self):
        cart = Cart()
        apple = Product("りんご", 100)
        banana = Product("バナナ", 80)
        orange = Product("みかん", 120)
        
        cart.add(apple, 3)
        cart.add(banana, 2)
        cart.add(orange, 1)
        
        expected_quantities = {
            "りんご": 3,
            "バナナ": 2,
            "みかん": 1,
        }
        self.assertEqual(cart.quantities(), expected_quantities)

    def test_mixed_products_subtotal_and_count(self):
        cart = Cart()
        apple = Product("りんご", 100)
        banana = Product("バナナ", 80)
        
        cart.add(apple, 2)
        cart.add(banana, 3)
        
        self.assertEqual(cart.count(), 5)
        self.assertEqual(cart.count(apple), 2)
        self.assertEqual(cart.count(banana), 3)
        self.assertEqual(cart.subtotal(), (100 * 2) + (80 * 3))


if __name__ == "__main__":
    unittest.main()
