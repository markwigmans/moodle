import pandas as pd
from Utils import *
from GradeSheet import *

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
        # groupBy() can't handle empty DataFrames it seems, so we have to create a trick
        if len(df) > 0:
            df = df.rename(columns={'wordcount': self.WORD_COUNT, 'message' : self.MESSAGE, 'subject' : self.SUBJECT})
            df[self.KEY] = df.apply(lambda row: Utils.normalize_key(row["userfullname"]), axis=1)
            df[self.LINK] = df.apply(lambda row: f"{self.PREFIX_LINK}{row['discussion']}", axis=1)
            df[self.SUBJECT] = df[self.SUBJECT].apply(lambda x: x.strip())
            df[self.MESSAGE] = df[self.MESSAGE].apply(lambda x: x.strip())
        else:
            df = pd.DataFrame({self.KEY: []})
        return df.groupby(self.KEY)