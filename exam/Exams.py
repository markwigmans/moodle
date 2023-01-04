import os
import re
import logging
from pathlib import *
from shutil import copyfile
import pandas as pd
from GradeSheet import GradeSheet

class Exams:
    """Process student exams"""	

    def __init__(self, source, target, students):
        self.source = source
        self.target = target
        self.students = students
        self.processed = set()
        self.exams = set()
        self.student_exams = dict()

    def process(self, filename:str) -> None:
        """Process all files in source directory"""	
        for root, dirs,_ in os.walk(self.source):
            for dir in dirs:
                self._process_file(Path(root, dir))        
        self._save_unprocessed(filename)


    def gen_overview(self, filename:str) -> None:
        """Generate overview of all exams"""
        overview = pd.DataFrame.from_dict(self.students, orient='index')
        exam_columns = sorted(self.exams)
        # create columns for exams in the correct order
        for exam in exam_columns:
            overview.insert(len(overview.columns), exam, None, True)

        for student in self.students:
            for exam in exam_columns:
                if exam in self.student_exams.get(student, []):
                    overview.loc[student, exam] = 'X'

        overview.to_excel(filename, 
        columns= [GradeSheet.FIRST_NAME, GradeSheet.SURNAME, GradeSheet.MARKER] + exam_columns, 
        index=False)


    def _process_file(self, path) -> None:
        """Process file if it is a student file"""	
        result = re.match(r"(\w{9}) - (.*)",path.stem)
        if result:
            id = result.group(1)
            if self.students.get(id):
                marker = self.students[id][GradeSheet.MARKER]
                self._move_file(path, marker)
                self._add_exam(id, path)
                self.processed.add(id)
            else:
                logging.warning(f"Student '{id}' not found!")


    def _move_file(self, path, marker) -> None:
        """Move file to target directory"""	
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