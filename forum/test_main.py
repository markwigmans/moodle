# test main.py

import unittest
from main import *

class TestMyModule(unittest.TestCase):
    def test_normalize_key(self):
        self.assertEqual(normalize_key("Test String"), "teststring")
        self.assertEqual(normalize_key("Test String", "e"), "tst string")
        self.assertEqual(normalize_key("Test String", ""), "test string")
        self.assertEqual(normalize_key("Test String", " "), "teststring")
        self.assertEqual(normalize_key("Test String", "st "), "tesring")
        self.assertEqual(normalize_key(None), "")
        self.assertEqual(normalize_key(""), "")

if __name__ == '__main__':
    unittest.main()