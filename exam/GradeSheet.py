import pandas as pd

class GradeSheet:
    """Process Teams Gradesheet"""

    # used column names as constants
    FIRST_NAME = "First name"
    SURNAME = "Surname"
    ID_NUMBER = "ID number"
    MARKER = "Marker"

    def __init__(self, filename:str, sheet_name:str, header:int):
        self.filename = filename
        self.sheet_name = sheet_name
        self.header = header

    def read(self):
        worksheet = pd.read_excel(self.filename, sheet_name=self.sheet_name, header=self.header)
        worksheet = worksheet.dropna(subset=[self.FIRST_NAME])
        worksheet[self.FIRST_NAME] = worksheet.apply(lambda row: row[self.FIRST_NAME].title(), axis=1)
        worksheet[self.SURNAME] = worksheet.apply(lambda row: row[self.SURNAME].title(), axis=1)
        worksheet.loc[:, self.ID_NUMBER] = worksheet[self.ID_NUMBER].fillna('')
        students = {row[self.ID_NUMBER] : row.to_dict() for _, row in worksheet.iterrows()}
        markers  = {row[self.MARKER] : row.to_dict() for _, row in worksheet.iterrows()}
        return students, markers
