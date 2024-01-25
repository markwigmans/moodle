import pandas as pd

class GradeSheet:
    """
    A class to process a gradesheet for teams.

    Attributes:
        filename (str): The name of the file containing the gradesheet.
        sheet_name (str): The name of the sheet within the Excel file.
        header (int): The row number of the header.
    """

    # used column names as constants
    FIRST_NAME = "First name"
    SURNAME = "Surname"
    ID_NUMBER = "ID number"
    MARKER = "Marker"
    DEFAULT_MARKER = "-"

    def __init__(self, filename:str, sheet_name:str, header:int):
        self.filename = filename
        self.sheet_name = sheet_name
        self.header = header

    def read(self):
        """
        Reads and processes the gradesheet.

        Returns:
            tuple: A tuple containing dictionaries of students and markers.
        """
        worksheet = pd.read_excel(self.filename, sheet_name=self.sheet_name, header=self.header)
        worksheet = worksheet.dropna(subset=[self.FIRST_NAME, self.SURNAME])

        # Clean and standardize data
        worksheet[self.FIRST_NAME] = worksheet[self.FIRST_NAME].str.title()
        worksheet[self.SURNAME] = worksheet[self.SURNAME].str.title()
        worksheet[self.ID_NUMBER] = worksheet[self.ID_NUMBER].fillna('')
        worksheet[self.MARKER] = worksheet[self.MARKER].fillna(self.DEFAULT_MARKER)

        # Create dictionaries for students and markers
        students = {row[self.ID_NUMBER] : row.to_dict() for _, row in worksheet.iterrows()}
        markers  = {row[self.MARKER] : row.to_dict() for _, row in worksheet.iterrows()}
        return students, markers
