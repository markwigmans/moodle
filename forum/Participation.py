import pandas as pd
from Utils import *
from Posts import *

class Participation:
    """The participation of the forums every student"""

    def calc_participation(overview, sheets):
    """Calculate overall participation excel file"""
    df = pd.DataFrame()

    # create empty value for every student
    for _, row in overview.iterrows():
        df = pd.concat( [df,
                pd.DataFrame(
                    {
                        TOTAL: 0,
                        FIRST_NAME: row[FIRST_NAME],
                        SURNAME: row[SURNAME],
                        MARKER: row[MARKER]
                    },
                    index=[row[KEY]]
                )])

    for sheet, _, students in sheets:
        for _, row in overview.iterrows():
            found = '-'
            student = row[KEY]
            try:
                found = len(students.get_group(student))
                df.at[student, TOTAL] = df.loc[student][TOTAL] + 1
            except KeyError:
                pass  # Do Nothing as the given student is not in the given sheet
            df.at[student, sheet] = found
    return df