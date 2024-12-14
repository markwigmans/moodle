import unittest

from utils.Utils import Utils


class TestMyModule(unittest.TestCase):

    def test_normalize_key(self):
        self.assertEqual(Utils.normalize_key("Test String"), "teststring")
        self.assertEqual(Utils.normalize_key(""), "")

    def test_to_cell(self):
        self.assertEqual(Utils.to_cell(0,0), "A1")
        self.assertEqual(Utils.to_cell(6,2), "C7")
        self.assertEqual(Utils.to_cell(6, 2, True, False), "C$7")
        self.assertEqual(Utils.to_cell(6, 2, False, True), "$C7")
        self.assertEqual(Utils.to_cell(6, 2, True, True), "$C$7")

if __name__ == '__main__':
    unittest.main()
