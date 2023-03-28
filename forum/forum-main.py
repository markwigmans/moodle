import string
import sys
import io
import pandas as pd
import seaborn as sns
import xlsxwriter.utility

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


def set_filter_range(begin_col:int, last_col:int, worksheet) -> None:
    """Set worksheet autofilter range"""
    if worksheet.dim_rowmax > 0:
        worksheet.autofilter(0, begin_col, worksheet.dim_rowmax, last_col)
  

def get_size_by_values(col:str, df) -> int :
    values = df[col].values
    longest_string = max(values, key=len)
    return len(longest_string)


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

    # set workbook formats
    fmt_message = writer.book.add_format({'valign' : 'top','text_wrap' : True})
    fmt_text = writer.book.add_format({'valign' : 'top'})
    fmt_number = writer.book.add_format({'align' : 'center','valign' : 'top'})
    fmt_link = writer.book.get_default_url_format()
    fmt_link.set_align('top')
    writer.book.default_url_format = fmt_link

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
    worksheet.set_column('A:A', get_size_by_values(FIRST_NAME, participation))
    worksheet.set_column('B:B', get_size_by_values(SURNAME, participation))
    column_letter = xlsxwriter.utility.xl_col_to_name(len(sheets) + 2)
    worksheet.set_column(f"D:{column_letter}", None, fmt_number)
    set_filter_range(2, 2, worksheet)

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

    # create plot image
    buf = io.BytesIO()
    plot = sns.countplot(x='Forum', data=posts)
    plot.set(ylabel = "Posts")
    plot.get_figure().savefig(buf, format='png')
    worksheet.insert_image('L2', 'Posts', {'image_data': buf})

    posts.to_excel(
        writer,
        sheet_name="Posts",
        columns=[FIRST_NAME, SURNAME, MARKER, FORUM, SUBJECT, MESSAGE, WORD_COUNT, LINK],
        index=False)        

    worksheet = writer.sheets['Posts']
    worksheet.freeze_panes(1, 0)
    worksheet.set_column('A:G', None, fmt_text)
    worksheet.set_column('A:A', get_size_by_values(FIRST_NAME, participation))
    worksheet.set_column('B:B', get_size_by_values(SURNAME, participation))
    worksheet.set_column('E:E', 40, fmt_message) 
    worksheet.set_column('F:F', 100, fmt_message)
    worksheet.set_column('H:H', 60)
    set_filter_range(2, 3, worksheet)

    #
    # generate sheets with the data
    #
    for sheet,_,students in sheets:
        posts.loc[posts[FORUM] == sheet].to_excel(writer, sheet_name=sheet,
            columns=[FIRST_NAME, SURNAME, MARKER, SUBJECT, MESSAGE, WORD_COUNT, LINK], 
            index=False)
        worksheet = writer.sheets[sheet]
        worksheet.freeze_panes(1, 0)
        worksheet.set_column('A:G', None, fmt_text) 
        worksheet.set_column('A:A', get_size_by_values(FIRST_NAME, participation))
        worksheet.set_column('B:B', get_size_by_values(SURNAME, participation))
        worksheet.set_column('D:D', 40, fmt_message) 
        worksheet.set_column('E:E', 100, fmt_message)
        worksheet.set_column('G:G', 60)
        set_filter_range(2, 2, worksheet)
         
    worksheet = writer.sheets['Overview']
    worksheet.activate()
    writer.close()


def main(args) -> None:
    """Main application"""
    overview = read_grade_sheet("students.xlsx")
    sheets_list = [
        ("P-1", "Session 4  - Creating Money", get_posts("discussion-1.csv")),
        ("P-2", "Session 6  - Securitization", get_posts("discussion-2.csv")),
        ("P-3", "Session 8  - Central bank digital currencies", get_posts("discussion-3.csv")),
        ("P-4", "Session 10 - Valuation of Financial Instruments",get_posts("discussion-4.csv")),
        ("P-5", "Session 12 - Evaluating Cryptocurrencies", get_posts("discussion-5.csv")),
    ]
    participation = calc_participation(overview, sheets_list)
    gen_sheet("participation.xlsx", participation, overview, sheets_list)


if __name__ == "__main__":
    main(sys.argv)
