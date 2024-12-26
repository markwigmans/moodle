from typing import Final

import pandas as pd

from utils.Utils import Utils


class Posts:
    """Process Moodle Posts"""

    # used column names as constants
    KEY: Final[str] = "key"
    FIRST_NAME: Final[str] = "First name"
    SURNAME: Final[str] = "Surname"
    MARKER: Final[str] = "Marker"
    TOTAL: Final[str] = "Forums"
    FORUM: Final[str] = "Forum"
    SUBJECT: Final[str] = 'Subject'
    MESSAGE: Final[str] = 'Message'
    WORD_COUNT: Final[str] = 'Words'
    LINK: Final[str] = 'Link'
    PREFIX_LINK: Final[str] = "https://courses.unic.ac.cy/mod/forum/discuss.php?d="

    def __init__(self, filename: str, forum: str):
        self.filename = filename
        self.forum = forum

    def read(self) -> pd.DataFrame:
        """Read and process posts from forum CSV file."""
        df = pd.read_csv(self.filename)
        df = df.rename(columns={'wordcount': self.WORD_COUNT, 'message': self.MESSAGE, 'subject': self.SUBJECT})
        df[self.KEY] = df['userfullname'].apply(Utils.normalize_key)
        df[self.LINK] = self.PREFIX_LINK + df['discussion'].astype(str)
        df[self.SUBJECT] = df[self.SUBJECT].str.strip()
        df[self.MESSAGE] = df[self.MESSAGE].str.strip()
        df[self.FORUM] = self.forum
        return df
