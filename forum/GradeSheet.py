from typing import Final

import pandas as pd

from utils.Utils import Utils


class GradeSheet:
    """Process Teams Grade sheet"""

    # used column names as constants
    KEY: Final[str] = "key"
    FIRST_NAME: Final[str] = "First name"
    SURNAME: Final[str] = "Surname"
    ID_NUMBER: Final[str] = "ID number"

    def __init__(self, filename: str, sheet_name: str, header: int = 0):
        self.filename = filename
        self.sheet_name = sheet_name
        self.header = header

    def read(self) -> pd.DataFrame:
        """read participation part of grade spreadsheet"""
        worksheet = (pd
                     .read_excel(self.filename, sheet_name=self.sheet_name, header=self.header)
                     .dropna(subset=[self.FIRST_NAME, self.SURNAME]))
        # clean data
        worksheet[self.ID_NUMBER] = worksheet[self.ID_NUMBER].fillna('')
        worksheet[self.KEY] = worksheet.apply(
            lambda row: Utils.normalize_key(f"{row[self.FIRST_NAME]}{row[self.SURNAME]}"), axis=1)

        worksheet.set_index(self.KEY)
        return worksheet
