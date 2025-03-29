import os
import unittest
import pandas as pd
from forum.Posts import Posts


class TestPosts(unittest.TestCase):

    def setUp(self):
        # Create a sample CSV file for testing
        self.test_dir = os.path.dirname(__file__)
        self.data_path = os.path.join(self.test_dir, 'test_discussion.csv')
        self.sample_data = {
            'userfullname': ['John Doe', 'Jane Smith', 'Alice Johnson'],
            'discussion': [1, 2, 3],
            'id': [101, 102, 103],
            'wordcount': [100, 150, 200],
            'message': ['Message 1', 'Message 2', 'Message 3'],
            'subject': ['Subject 1', 'Subject 2', 'Subject 3']
        }
        df = pd.DataFrame(self.sample_data)
        df.to_csv(self.data_path, index=False)

    def tearDown(self):
        # Remove the sample CSV file after testing
        os.remove(self.data_path)

    def test_read_posts(self):
        posts = Posts(self.data_path, "test_forum")
        df = posts.read()

        # Check if the dataframe has the correct number of rows
        self.assertEqual(len(df), 3)

        # Check if the dataframe has the correct columns
        expected_columns = [
            'userfullname', 'discussion', 'id', 'Words', 'Message', 'Subject',
            'key', 'Link', 'Forum'
        ]
        self.assertTrue(all(column in df.columns for column in expected_columns))

        # Check if the 'Forum' column is correctly set
        self.assertTrue((df['Forum'] == "test_forum").all())


if __name__ == '__main__':
    unittest.main()