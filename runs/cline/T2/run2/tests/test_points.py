import unittest

from omise.points import earn_points


class TestPoints(unittest.TestCase):
    def test_earn_points_standard(self):
        self.assertEqual(earn_points(1000), 10)

    def test_earn_points_fraction(self):
        self.assertEqual(earn_points(150), 1)

    def test_earn_points_small(self):
        self.assertEqual(earn_points(99), 0)

    def test_earn_points_zero(self):
        self.assertEqual(earn_points(0), 0)
