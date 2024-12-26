from typing import Final

import pandas as pd

from utils.Utils import Utils


class GradeSheet:
    """Process Teams GradeSheet"""

    # used column names as constants
    FIRST_NAME: Final[str] = "First name"
    SURNAME: Final[str] = "Surname"
    ID_NUMBER: Final[str] = "ID number"
    MARKER: Final[str] = "Marker"
    DEFAULT_MARKER: Final[str] = "-"
    FULL_NAME: Final[str] = "Full name"
    INDEX: Final[str] = "ref"

    def __init__(self, filename: str, sheet_name: str, header: int, offset: int):
        self.filename = filename
        self.sheet_name = sheet_name
        self.header = header
        self.offset = offset

    def read(self):
        worksheet = (pd
                     .read_excel(self.filename, sheet_name=self.sheet_name, header=self.header)
                     .dropna(subset=[self.FIRST_NAME, self.SURNAME])
                     .reset_index(names=self.INDEX))
        # clean data
        worksheet[self.INDEX] = worksheet.apply(lambda row: row[self.INDEX] + self.offset, axis=1)
        worksheet[self.FIRST_NAME] = worksheet[self.FIRST_NAME].str.title()
        worksheet[self.SURNAME] = worksheet[self.SURNAME].str.title()
        worksheet[self.FULL_NAME] = worksheet[self.FIRST_NAME] + " " + worksheet[self.SURNAME]
        worksheet[self.ID_NUMBER] = worksheet[self.ID_NUMBER].fillna('')
        worksheet[self.MARKER] = worksheet[self.MARKER].fillna(self.DEFAULT_MARKER)

        students = {Utils.normalize_key(row[self.FULL_NAME]): row.to_dict() for _, row in worksheet.iterrows()}
        markers = {row[self.MARKER]: row.to_dict() for _, row in worksheet.iterrows()}
        return students, markers
