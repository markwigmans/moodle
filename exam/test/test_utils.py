# test ../main.py

import unittest
from Utils import *

class TestMyModule(unittest.TestCase):
    def test_normalize_key(self):
        self.assertEqual(Utils.normalize_key("Test String"), "teststring")
        self.assertEqual(Utils.normalize_key("Test String", "e"), "tst string")
        self.assertEqual(Utils.normalize_key("Test String", ""), "test string")
        self.assertEqual(Utils.normalize_key("Test String", " "), "teststring")
        self.assertEqual(Utils.normalize_key("Test String", "st "), "tesring")
        self.assertEqual(Utils.normalize_key(None), "")
        self.assertEqual(Utils.normalize_key(""), "")

if __name__ == '__main__':
    unittest.main()