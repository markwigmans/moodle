# test ../main.py

import unittest
import os
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

    def test_get_posts(self):
        test_dir = os.path.dirname(__file__)
        data_path = os.path.join(test_dir, 'discussion.csv')
        df = get_posts(data_path)
        self.assertEqual(len(df), 2)
        self.assertEqual(len(df.get_group("janjansen")), 2)
        self.assertEqual(len(df.get_group("pietpietersen")), 1)


if __name__ == '__main__':
    unittest.main()