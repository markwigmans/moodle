import string
import sys
import pandas as pd
import xlsxwriter.utility

# used column names as constants
KEY = "key"
FIRST_NAME = "First name"
SURNAME = "Surname"
MARKER = "Marker"
TOTAL = "Forums"
FORUM = "Forum"
MESSAGE = 'message'


def normalize_key(key: str, remove_chars: str = string.whitespace) -> str:
    """Remove all specified characters from the input string and return the result in lowercase."""
    if key is not None:
        translation_table = str.maketrans("", "", remove_chars)
        return key.translate(translation_table).lower()
    return ""


def read_grade_sheet(filename:str) -> pd.DataFrame:
    """read participation part of grade spreadsheet"""
    worksheet = pd.read_excel(filename, sheet_name="Quizes - Participation")
    worksheet = worksheet.dropna(subset=[FIRST_NAME, SURNAME])
    worksheet[KEY] = worksheet.apply(lambda row: normalize_key(f"{row['First name']}{row['Surname']}"), axis=1)
    worksheet.set_index(KEY)
    return worksheet


def get_students(filename:str) -> pd.core.groupby.generic.DataFrameGroupBy:
    """get students from forum CSV file"""
    df = pd.read_csv(filename)
    # groupBy() can't handle empty DataFrames it seems, so we have to create a trick
    if len(df) > 0:
        df[KEY] = df.apply(lambda row: normalize_key(row["userfullname"]), axis=1)
        df[MESSAGE] = df[MESSAGE].apply(lambda x: x.strip())
    else:
        df = pd.DataFrame({KEY: []})
    return df.groupby(KEY)


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


def filter_range(prefix:str, worksheet) -> str:
    """Create the range the given worksheet will have a autofilter range"""
    if worksheet.dim_rowmax > 0:
        return prefix + str(worksheet.dim_rowmax)
    else:
        return prefix + '1'    


def gen_sheet(filename, participation, overview, sheets):
    """Generate resulting Excel sheet"""
    writer = pd.ExcelWriter(filename, engine="xlsxwriter")

    #
    # Create readme part
    #
    worksheet = writer.book.add_worksheet("Readme")
    worksheet.write_string(0, 0, "Paricipation overview")
    worksheet.write_string(1, 0, "Sheet 'overview' contains per student the number of posts")
    worksheet.write_string(2, 0, "Sheet 'posts' contains all posts of all students")

    for index, (sheet, description, _) in enumerate(sheets):
        worksheet.write_string(index + 4, 0, f"{sheet} : {description}")

    fmt_message = writer.book.add_format({'valign': 'top','text_wrap': True})
    fmt_text = writer.book.add_format({'valign': 'top'})
    fmt_number = writer.book.add_format({'align': 'center','valign': 'top'})

    #
    # Overview part
    #
    participation.to_excel(
        writer,
        sheet_name="Overview",
        columns=[FIRST_NAME, SURNAME, MARKER] +  [h for (h,_,_) in sheets] + [TOTAL],
        index=False)
    worksheet = writer.sheets['Overview']
    worksheet.freeze_panes(1, 0)
    column_letter = xlsxwriter.utility.xl_col_to_name(len(sheets) + 2)
    worksheet.set_column(f"D:{column_letter}", None, fmt_number) 
    worksheet.autofilter(filter_range('C1:C', worksheet))

    #
    # generate sheets with all posts
    #
    posts = pd.DataFrame()
    for _, row in overview.iterrows():
        student = row[KEY]
        for sheet,_,students in sheets:
            try:
                data = students.get_group(student).copy()
                data[FORUM] = [sheet] * len(data)
                data[FIRST_NAME] = [row[FIRST_NAME]] * len(data)
                data[SURNAME] = [row[SURNAME]] * len(data)
                data[MARKER] = [row[MARKER]] * len(data)
                posts = pd.concat([posts, data])
            except KeyError:
                pass  # Do Nothing as the given student is not in the given sheet

    posts.to_excel(
        writer,
        sheet_name="Posts",
        columns=[FIRST_NAME, SURNAME, MARKER, FORUM, 'subject', 'message', 'wordcount'],
        index=False)        

    worksheet = writer.sheets['Posts']
    worksheet.freeze_panes(1, 0)
    worksheet.set_column('A:G', None, fmt_text) 
    worksheet.set_column('E:E', 40) 
    worksheet.set_column('F:F', 100, fmt_message)
    worksheet.autofilter(filter_range('C1:D', worksheet))

    #
    # generate sheets with the data
    #
    for sheet,_,students in sheets:
        posts.loc[posts[FORUM] == sheet].to_excel(writer, sheet_name=sheet,
            columns=[FIRST_NAME, SURNAME, MARKER, 'subject', 'message', 'wordcount'], 
            index=False)
        worksheet = writer.sheets[sheet]
        worksheet.freeze_panes(1, 0)
        worksheet.set_column('A:F', None, fmt_text) 
        worksheet.set_column('D:D', 40) 
        worksheet.set_column('E:E', 100, fmt_message)
        worksheet.autofilter(filter_range('C1:C', worksheet))
         
    worksheet = writer.sheets['Overview']
    worksheet.activate()
    writer.close()


def main(args) -> None:
    """Main application"""
    overview = read_grade_sheet("bloc-516 - Fall 2022 - Exam Marks.xlsx")
    sheets_list = [
        ("P-1", "Session 4  - Creating Money", get_students("discussion-1.csv")),
        ("P-2", "Session 6  - Securitization", get_students("discussion-2.csv")),
        ("P-3", "Session 8  - Central bank digital currencies", get_students("discussion-3.csv")),
        ("P-4", "Session 10 - Valuation of Financial Instruments",get_students("discussion-4.csv")),
        ("P-5", "Session 12 - Evaluating Cryptocurrencies", get_students("discussion-5.csv")),
    ]
    participation = calc_participation(overview, sheets_list)
    gen_sheet("participation.xlsx", participation, overview, sheets_list)


if __name__ == "__main__":
    main(sys.argv)
