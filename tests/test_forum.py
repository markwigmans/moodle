import os
import unittest

from forum.Posts import Posts


class TestForum(unittest.TestCase):

    def test_read_posts(self):
        test_dir = os.path.dirname(__file__)
        data_path = os.path.join(test_dir, 'discussion.csv')
        df = Posts(data_path, "test").read()
        self.assertEqual(len(df), 3)


if __name__ == '__main__':
    unittest.main()
