from Utils import *
from Posts import *
import io
import pandas as pd
import seaborn as sns
import xlsxwriter.utility

class Participation:
    """The participation of the forums every student"""

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


    def __init__(self, overview, sheets):
        self.overview = overview
        self.sheets = sheets;

    def calc(self):
        """Calculate overall participation excel file"""
        df = pd.DataFrame()

        # create empty value for every student
        for _, row in self.overview.iterrows():
            df = pd.concat( [df,
                    pd.DataFrame(
                        {
                            self.TOTAL: 0,
                            self.FIRST_NAME: row[ self.FIRST_NAME],
                            self.SURNAME: row[ self.SURNAME],
                            self.MARKER: row[ self.MARKER]
                        },
                        index=[row[ self.KEY]]
                    )])

        for sheet, _, students in self.sheets:
            for _, row in self.overview.iterrows():
                found = '-'
                student = row[ self.KEY]
                try:
                    found = len(students.get_group(student))
                    df.at[student,  self.TOTAL] = df.loc[student][ self.TOTAL] + 1
                except KeyError:
                    pass  # Do Nothing as the given student is not in the given sheet
                df.at[student, sheet] = found
        self.data = df;
    

    def gen_sheet(self, filename):
        """Generate resulting Excel sheet"""
        writer = pd.ExcelWriter(filename, engine="xlsxwriter")

        #
        # Create readme part
        #
        worksheet = writer.book.add_worksheet("Readme")
        worksheet.write_string(0, 0, "Paricipation overview")
        worksheet.write_string(1, 0, "Sheet 'overview' contains per student the number of posts")
        worksheet.write_string(2, 0, "Sheet 'posts' contains all posts of all students")

        for index, (sheet, description, _) in enumerate(self.sheets):
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
        self.data.to_excel(
            writer,
            sheet_name="Overview",
            columns=[self.FIRST_NAME, self.SURNAME, self.MARKER] +  [h for (h,_,_) in self.sheets] + [self.TOTAL],
            index=False)
        worksheet = writer.sheets['Overview']
        worksheet.freeze_panes(1, 0)
        worksheet.set_column('A:A', Utils.get_size_by_values(self.FIRST_NAME, self.data))
        worksheet.set_column('B:B', Utils.get_size_by_values(self.SURNAME, self.data))
        column_letter = xlsxwriter.utility.xl_col_to_name(len(self.sheets) + 2)
        worksheet.set_column(f"D:{column_letter}", None, fmt_number)
        Utils.set_filter_range(2, 2, worksheet)

        #
        # generate sheets with all posts
        #
        posts = pd.DataFrame()
        for _, row in self.overview.iterrows():
            student = row[self.KEY]
            for sheet,_,students in self.sheets:
                try:
                    data = students.get_group(student).copy()
                    data[self.FORUM] = [sheet] * len(data)
                    data[self.FIRST_NAME] = [row[self.FIRST_NAME]] * len(data)
                    data[self.SURNAME] = [row[self.SURNAME]] * len(data)
                    data[self.MARKER] = [row[self.MARKER]] * len(data)
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
            columns=[self.FIRST_NAME, self.SURNAME, self.MARKER, self.FORUM, self.SUBJECT, self.MESSAGE, self.WORD_COUNT, self.LINK],
            index=False)        

        worksheet = writer.sheets['Posts']
        worksheet.freeze_panes(1, 0)
        worksheet.set_column('A:G', None, fmt_text)
        worksheet.set_column('A:A', Utils.get_size_by_values(self.FIRST_NAME, self.data))
        worksheet.set_column('B:B', Utils.get_size_by_values(self.SURNAME, self.data))
        worksheet.set_column('E:E', 40, fmt_message) 
        worksheet.set_column('F:F', 100, fmt_message)
        worksheet.set_column('H:H', 60)
        Utils.set_filter_range(2, 3, worksheet)

        #
        # generate sheets with the data
        #
        for sheet,_,students in self.sheets:
            posts.loc[posts[self.FORUM] == sheet].to_excel(writer, sheet_name=sheet,
                columns=[self.FIRST_NAME, self.SURNAME, self.MARKER, self.SUBJECT, self.MESSAGE, self.WORD_COUNT, self.LINK], 
                index=False)
            worksheet = writer.sheets[sheet]
            worksheet.freeze_panes(1, 0)
            worksheet.set_column('A:G', None, fmt_text) 
            worksheet.set_column('A:A', Utils.get_size_by_values(self.FIRST_NAME, self.data))
            worksheet.set_column('B:B', Utils.get_size_by_values(self.SURNAME, self.data))
            worksheet.set_column('D:D', 40, fmt_message) 
            worksheet.set_column('E:E', 100, fmt_message)
            worksheet.set_column('G:G', 60)
            Utils.set_filter_range(2, 2, worksheet)
            
        worksheet = writer.sheets['Overview']
        worksheet.activate()
        writer.close()    