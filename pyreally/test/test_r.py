import unittest
from pyreally import R


class TestR(unittest.TestCase):
    def test_properties(self):
        r = R("/users/12aacf8")
        self.assertEqual("/users/12aacf8", str(r))
        self.assertEqual("R(/users/12aacf8)", repr(r))

    def test_equals(self):
        r1 = R("/users/12aacf8")
        r2 = R("/users/12aacf8")
        r3 = R("/people/12aacf8")
        self.assertEqual(r1, r2)
        self.assertEqual(r2, r1)
        self.assertNotEquals(r1, r3)
        self.assertNotEquals(r2, r3)
