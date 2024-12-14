import xlsxwriter.utility

from GradeSheet import GradeSheet
from Posts import *


class Participation:
    """The participation of the forums every student"""

    # used column names as constants
    TOTAL = "Forums"
    FORUM = "Forum"
    SUBJECT = 'Subject'
    MESSAGE = 'Message'
    WORD_COUNT = 'Words'
    LINK = 'Link'

    def __init__(self, gradeSheet, sheets):
        self.gradeSheet = gradeSheet
        self.sheets = sheets

    def gen_sheet(self, filename):
        """Generate resulting Excel sheet"""
        writer = pd.ExcelWriter(filename, engine="xlsxwriter")

        # transform all received data    
        self._create_data()

        # set workbook formats
        fmt_message = writer.book.add_format({'valign': 'top', 'text_wrap': True})
        fmt_text = writer.book.add_format({'valign': 'top'})
        fmt_red_text = writer.book.add_format({'valign': 'top', 'bg_color': '#FF0000'})
        fmt_number = writer.book.add_format({'align': 'center', 'valign': 'top'})
        fmt_perc = writer.book.add_format({'align': 'center', 'valign': 'top', "num_format": "0.0%"})
        fmt_link = writer.book.get_default_url_format()
        fmt_link.set_align('top')
        writer.book.default_url_format = fmt_link

        #
        # Create readme part
        #
        worksheet = writer.book.add_worksheet("Readme")
        worksheet.write_string(0, 0, "Participation Overview")
        worksheet.write_string(2, 0, "Sheet 'overview' contains per student the number of posts")
        worksheet.write_string(3, 0, "Sheet 'posts' contains all posts of all students")

        for index, (sheet, description, _) in enumerate(self.sheets):
            worksheet.write_string(index + 5, 0, f"{sheet} : {description}")

        #
        # Overview part
        #
        offset = 3
        self.data.to_excel(
            writer,
            sheet_name="Overview",
            columns=[GradeSheet.FIRST_NAME, GradeSheet.SURNAME, GradeSheet.ID_NUMBER] + [h for (h, _, _) in
                                                                                         self.sheets] + [self.TOTAL],
            startrow=offset,
            index=False)
        worksheet = writer.sheets['Overview']
        worksheet.freeze_panes(offset + 1, 0)
        worksheet.set_column('A:A', Utils.get_max_column_width(GradeSheet.FIRST_NAME, self.data))
        worksheet.set_column('B:B', Utils.get_max_column_width(GradeSheet.SURNAME, self.data))
        worksheet.set_column('C:C', 15, fmt_number)
        column_letter = xlsxwriter.utility.xl_col_to_name(len(self.sheets) + 3)
        worksheet.set_column(f"D:{column_letter}", None, fmt_number)

        #
        # Generate header 'Overview'
        #
        worksheet.write_string("C1", "Percentage")
        worksheet.write_string("C2", "#Unprocessed")
        for counter, (sheet, _, _) in enumerate(self.sheets):
            col = xlsxwriter.utility.xl_col_to_name(counter + 3)
            sheet_count = len(self.posts[self.posts[self.FORUM] == sheet])
            size = worksheet.dim_rowmax + 1
            worksheet.write_formula(f"{col}1",
                                    f'=COUNTIFS({col}{offset + 2}:{col}{size},">0")/ROWS({col}{offset + 2}:{col}{size})',
                                    fmt_perc)
            worksheet.write_formula(f"{col}2", f'={sheet_count} - SUM({col}{offset + 2}:{col}{size})', fmt_number)
            worksheet.conditional_format(f"{col}2", {'type': 'cell', 'criteria': 'greater than', 'value': 0,
                                                     'format': fmt_red_text})

        #
        # generate sheets with all posts
        #
        self.posts.to_excel(
            writer,
            sheet_name="Posts",
            columns=[GradeSheet.FIRST_NAME, GradeSheet.SURNAME, self.FORUM, self.SUBJECT, self.MESSAGE, self.WORD_COUNT,
                     self.LINK],
            index=False)

        worksheet = writer.sheets['Posts']
        worksheet.freeze_panes(1, 0)
        worksheet.set_column('A:A', Utils.get_max_column_width(GradeSheet.FIRST_NAME, self.data), fmt_text)
        worksheet.set_column('B:B', Utils.get_max_column_width(GradeSheet.SURNAME, self.data), fmt_text)
        worksheet.set_column('C:C', None, fmt_text)
        worksheet.set_column('D:D', 40, fmt_message)
        worksheet.set_column('E:E', 100, fmt_message)
        worksheet.set_column('F:F', None, fmt_text)
        worksheet.set_column('G:G', 60, fmt_text)
        Utils.set_filter_range(0, 2, worksheet)

        worksheet = writer.sheets['Overview']
        worksheet.activate()
        writer.close()

    def _create_data(self):
        """Calculate overall participation excel file"""

        self.posts = self._generate_posts();
        grouped = self.posts.groupby([Posts.KEY, Posts.FORUM]).size();

        # create empty value for every student
        df = pd.DataFrame()
        for _, row in self.gradeSheet.iterrows():
            df = pd.concat([df,
                            pd.DataFrame(
                                {
                                    self.TOTAL: 0,
                                    GradeSheet.FIRST_NAME: row[GradeSheet.FIRST_NAME],
                                    GradeSheet.SURNAME: row[GradeSheet.SURNAME],
                                    GradeSheet.ID_NUMBER: row[GradeSheet.ID_NUMBER]
                                },
                                index=[row[GradeSheet.KEY]]
                            )])

        # fill the data
        for sheet, _, _ in self.sheets:
            for _, row in self.gradeSheet.iterrows():
                found = 0
                student = row[GradeSheet.KEY]
                try:
                    found = grouped.loc[(student, sheet)]
                    df.at[student, self.TOTAL] = df.loc[(student, self.TOTAL)] + 1
                except KeyError:
                    pass  # Do Nothing as the given student is not in the given sheet
                df.at[student, sheet] = found
        self.data = df

    def _generate_posts(self):
        """create 1 DataFrame with the posts in it"""
        posts = pd.DataFrame()
        for _, _, postings in self.sheets:
            result = pd.merge(postings, self.gradeSheet, left_on=Posts.KEY, right_on=GradeSheet.KEY, how='left')
            posts = pd.concat([posts, result])
        return posts
