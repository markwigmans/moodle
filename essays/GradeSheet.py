import pandas as pd
from Utils import *

class GradeSheet:
    """Process Teams Gradesheet"""

    # used column names as constants
    FIRST_NAME = "First name"
    SURNAME = "Surname"
    ID_NUMBER = "ID number"
    MARKER = "Marker"

    FULL_NAME = "Full name"
    INDEX = "ref"

    def __init__(self, filename:str, sheet_name:str, header:int, offset:int):
        self.filename = filename
        self.sheet_name = sheet_name
        self.header = header
        self.offset = offset

    def read(self):
        worksheet = pd.read_excel(self.filename, sheet_name=self.sheet_name, header=self.header)
        # clean data
        worksheet = worksheet.dropna(subset=[self.FIRST_NAME, self.SURNAME])
        worksheet.reset_index(inplace=True, names= self.INDEX)  # add index as column as well
        worksheet[self.INDEX] = worksheet.apply(lambda row: row[self.INDEX] + self.offset, axis=1)
        worksheet[self.FIRST_NAME] = worksheet.apply(lambda row: row[self.FIRST_NAME].title(), axis=1)
        worksheet[self.SURNAME] = worksheet.apply(lambda row: row[self.SURNAME].title(), axis=1)
        worksheet[self.FULL_NAME] = worksheet[self.FIRST_NAME] + " " + worksheet[self.SURNAME]
        worksheet.loc[:, self.ID_NUMBER] = worksheet[self.ID_NUMBER].fillna('')

        students = {Utils.normalize_key(row[self.FULL_NAME]) : row.to_dict() for _, row in worksheet.iterrows()}
        markers  = {row[self.MARKER] : row.to_dict() for _, row in worksheet.iterrows()}
        return students, markers
