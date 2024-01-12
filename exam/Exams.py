import os
import re
import logging
from pathlib import *
from shutil import copyfile
import pandas as pd
from GradeSheet import GradeSheet
from Utils import Utils

class Exams:
    """Process student exams"""	

    TOTAL = "Total"
    Q1 = "Q1"
    Q2 = "Q2"
    Q3 = "Q3"

    def __init__(self, source, target, students, markers):
        self.source = source
        self.target = target
        self.students = students
        self.markers = markers
        self.processed = set()
        self.exams = set()
        self.student_exams = dict()

    def process(self, filename:str) -> None:
        """Process all files in source directory"""	
        for root, dirs, files in os.walk(self.source):
            for file in files:
                self._process_file(Path(root, file))        
            for dir in dirs:
                self._process_dir(Path(root, dir))        
        self._save_unprocessed(filename)


    def gen_overview(self, filename:str) -> None:
        """Generate overview of all exams"""
        overview = pd.DataFrame.from_dict(self.students, orient='index')
        exam_columns = sorted(self.exams)
        # create columns for exams in the correct order
        for exam in exam_columns:
            overview.insert(len(overview.columns), exam, None, True)

        y_offset = 3
        x_offset = 5

        for student in self.students:
            # I can't add a formula here, pandas changes the content, don't know why
            overview.loc[student, self.TOTAL] = 0
            overview.loc[student, self.Q1] = ''
            overview.loc[student, self.Q2] = ''
            overview.loc[student, self.Q3] = ''
            for exam in exam_columns:
                if exam in self.student_exams.get(student, []):
                    overview.loc[student, exam] = 'X'

        # create file
        with pd.ExcelWriter(filename, engine="xlsxwriter") as writer:
            overview.to_excel(
                writer,
                sheet_name="Overview",
                columns= [GradeSheet.FIRST_NAME, GradeSheet.SURNAME, GradeSheet.ID_NUMBER ,GradeSheet.MARKER, self.TOTAL] + exam_columns + [self.Q1, self.Q2, self.Q3], 
                startrow=y_offset - 1,
                index=False)
            worksheet = writer.sheets['Overview']
            fmt_text = writer.book.add_format({'align' : 'center','valign' : 'top'})

            # write total count headers
            worksheet.freeze_panes(y_offset, 3)
            worksheet.write(f"{Utils.to_cell(0,x_offset-1)}", "Totals")
            worksheet.write_comment(f"{Utils.to_cell(0,x_offset-1)}", "Total number of essays to be marked")
            worksheet.set_column(x_offset, len(exam_columns)+x_offset, None, fmt_text)
            for i in range(x_offset, len(exam_columns)+x_offset):
                start_cell = Utils.to_cell(y_offset, i)
                end_cell =  Utils.to_cell(worksheet.dim_rowmax, i)
                # calculate work to do
                worksheet.write(0,i,f"=SUBTOTAL(103,{start_cell}:{end_cell})-SUBTOTAL(102,{start_cell}:{end_cell})")
            worksheet.write(0, len(exam_columns)+x_offset, f"=SUM({Utils.to_cell(0,x_offset)}:{Utils.to_cell(0,len(exam_columns)+x_offset-1)})")

            # Write formulas
            for i in range (0, len(self.students)):
                row = i + y_offset
                col = len(exam_columns) - 1 + x_offset
                worksheet.write(row, x_offset - 1, f'=SUM({Utils.to_cell(row,col+1)}:{Utils.to_cell(row,col+3)})')
                worksheet.write(row,col+1, f'=IFERROR(SMALL({Utils.to_cell(row,x_offset)}:{Utils.to_cell(row,col)},1),"-")', fmt_text)
                worksheet.write(row,col+2, f'=IFERROR(SMALL({Utils.to_cell(row,x_offset)}:{Utils.to_cell(row,col)},2),"-")', fmt_text)
                worksheet.write(row,col+3, f'=IFERROR(SMALL({Utils.to_cell(row,x_offset)}:{Utils.to_cell(row,col)},3),"-")', fmt_text)

            worksheet.write_comment(y_offset-1,len(exam_columns) + x_offset, 'Calculate the 3 lowest marks')
            Utils.set_filter_range(x_offset-2, x_offset-2, worksheet, y_offset-1)


    def _process_file(self, path) -> None:
        """Process file if it is a question text"""
        if re.match(r"Question text",path.stem):
            for marker in self.markers:
                self._copy_file(path, marker)

    def _process_dir(self, path) -> None:
        """Process dir if it is a student directory"""	
        result = re.match(r"(\w{9}) - (.*)",path.stem)
        if result:
            id = result.group(1)
            if self.students.get(id):
                marker = self.students[id][GradeSheet.MARKER]
                self._copy_dir(path, marker)
                self._add_exam(id, path)
                self.processed.add(id)
            else:
                logging.warning(f"Student '{id}' not found!")


    def _copy_file(self, file, marker) -> None:
        """copy file to target directory"""	
        dir = os.path.dirname(file).split(os.sep)[-1]
        new = Path(self.target, marker, dir)
        new.mkdir(parents=True, exist_ok=True)
        copyfile(file, Path(new, file.name))


    def _copy_dir(self, path, marker) -> None:
        """Copy dir to target directory"""	
        questionDir = os.path.dirname(path).split(os.sep)[-1]
        new = Path(self.target, marker, questionDir, path.name)
        new.mkdir(parents=True, exist_ok=True)
        for file in path.iterdir():
            p = Path(new, file.name)
            copyfile(file,p)


    def _save_unprocessed(self, filename:str) -> None:
        """save all students that were not processed"""
        unprocessed = pd.DataFrame.from_dict(self.students, orient='index')
        result = unprocessed.loc[~unprocessed.index.isin(self.processed )]
        result.to_excel(filename, index=False)

    def _add_exam(self, student, path) -> None:
        """Add exam to student and exam list"""
        examDir = os.path.dirname(path).split(os.sep)[-1]
        exam = examDir.split(' ')[-1]
        self.exams.add(exam)
        if student in self.student_exams:
            self.student_exams[student].add(exam)
        else:
            self.student_exams[student] = {exam}