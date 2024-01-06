import pandas as pd
from Utils import Utils

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


    def __init__(self, filename:str):
        self.filename = filename

    def read(self) -> pd.core.groupby.generic.DataFrameGroupBy:
        """get students from forum CSV file"""
        df = pd.read_csv(self.filename)
        # groupBy() can't handle empty DataFrames it seems, so we have to check
        if len(df) > 0:
            df = df.rename(columns={'wordcount': self.WORD_COUNT, 'message' : self.MESSAGE, 'subject' : self.SUBJECT})
            df[self.KEY] = df['userfullname'].apply(lambda row: Utils.normalize_key(row))
            df[self.LINK] = df['discussion'].apply(lambda row: f"{self.PREFIX_LINK}{row}")
            df[self.SUBJECT] = df[self.SUBJECT].str.strip()
            df[self.MESSAGE] = df[self.MESSAGE].str.strip()
        else:
            df = pd.DataFrame({self.KEY: []})
        return df.groupby(self.KEY)