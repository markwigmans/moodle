import pandas as pd

from utils.Utils import Utils


class Posts:
    """Process Moodle Posts"""

    # used column names as constants
    KEY = "key"
    FIRST_NAME = "First name"
    SURNAME = "Surname"
    MARKER = "Marker"
    TOTAL = "Forums"
    FORUM = "Forum"
    SUBJECT = 'Subject'
    MESSAGE = 'Message'
    WORD_COUNT = 'Words'
    LINK = 'Link'
    PREFIX_LINK = "https://courses.unic.ac.cy/mod/forum/discuss.php?d="

    def __init__(self, filename: str, forum: str):
        self.filename = filename
        self.forum = forum

    def read(self):
        """get posts from forum CSV file"""
        df = pd.read_csv(self.filename)
        df = df.rename(columns={'wordcount': self.WORD_COUNT, 'message': self.MESSAGE, 'subject': self.SUBJECT})
        df[self.KEY] = df['userfullname'].apply(lambda row: Utils.normalize_key(row))
        df[self.LINK] = df['discussion'].apply(lambda row: f"{self.PREFIX_LINK}{row}")
        df[self.SUBJECT] = df[self.SUBJECT].str.strip()
        df[self.MESSAGE] = df[self.MESSAGE].str.strip()
        df[self.FORUM] = self.forum
        return df
