import pandas as pd
from Utils import *

class GradeSheet:
    """Process Teams Gradesheet"""

    # used column names as constants
    KEY = "key"
    FIRST_NAME = "First name"
    SURNAME = "Surname"


    def __init__(self, filename:str, sheet_name:str):
        self.filename = filename
        self.sheet_name = sheet_name

    def read(self) -> pd.DataFrame:
        """read participation part of grade spreadsheet"""
        worksheet = pd.read_excel(self.filename, sheet_name=self.sheet_name)
        worksheet = worksheet.dropna(subset=[self.FIRST_NAME, self.SURNAME])
        worksheet[self.KEY] = worksheet.apply(lambda row: Utils.normalize_key(f"{row[self.FIRST_NAME]}{row[self.SURNAME]}"), axis=1)
        worksheet.set_index(self.KEY)
        return worksheet