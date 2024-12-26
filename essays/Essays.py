import logging
import os
import re
from pathlib import Path
from shutil import copyfile

import pandas as pd

from GradeSheet import GradeSheet
from utils.Utils import Utils


class Essays:
    """Process student exams"""

    def __init__(self, source, target, length: int, students, markers):
        self.source = source
        self.target = target
        self.length = length
        self.students = students
        self.markers = markers
        self.processed = set()
        self.exams = set()
        self.student_exams = dict()

    def process(self, filename: str) -> None:
        """Process all files in source directory"""
        for root, dirs, files in os.walk(self.source):
            for file in files:
                self._process_file(Path(root, file))
            for dir in dirs:
                self._process_dir(Path(root, dir))
        self._save_unprocessed(filename)

    def gen_overview(self, filename: str) -> None:
        """Generate overview of all exams"""
        overview = pd.DataFrame.from_dict(self.students, orient='index')
        exam_columns = sorted(self.exams)
        # create columns for exams in the correct order
        for exam in exam_columns:
            overview.insert(len(overview.columns), exam, '', True)

        for student in self.students:
            for exam in exam_columns:
                if exam in self.student_exams.get(student, []):
                    overview.loc[student, exam] = 'X'

        # create file
        with pd.ExcelWriter(filename, engine="xlsxwriter") as writer:
            overview.to_excel(
                writer,
                sheet_name="Overview",
                columns=[GradeSheet.FIRST_NAME, GradeSheet.SURNAME, GradeSheet.ID_NUMBER, GradeSheet.INDEX,
                         GradeSheet.MARKER] + exam_columns,
                index=False)
            worksheet = writer.sheets['Overview']
            Utils.set_filter_range(4, 5, worksheet)

    def _process_file(self, path) -> None:
        """Do nothing"""

    def _process_dir(self, path) -> None:
        """Process dir if it is a student directory"""
        result = re.match(r"(.*)_([0-9]+)_assignsubmission_file(.*)", path.stem)
        if result:
            student_id = Utils.normalize_key(result.group(1))
            if self.students.get(student_id):
                index = self.students[student_id][GradeSheet.INDEX]
                marker = self.students[student_id][GradeSheet.MARKER]
                self._copy_dir(path, marker, index)
                self._add_exam(student_id, path)
                self.processed.add(student_id)
            else:
                logging.warning(f"Student '{student_id}' not found!")

    def _copy_file(self, file, marker) -> None:
        """copy file to target directory"""
        directory = os.path.dirname(file).split(os.sep)[-1]
        new = Path(self.target, marker, directory)
        new.mkdir(parents=True, exist_ok=True)
        copyfile(file, Path(new, file.name))

    def _copy_dir(self, path, marker, index) -> None:
        """Copy dir to target directory"""
        new = Path(self.target, marker)
        new.mkdir(parents=True, exist_ok=True)
        for file in path.iterdir():
            # copy file with index prefix
            copyfile(file, Path(new, str(index).zfill(self.length) + '_' + file.name))

    def _save_unprocessed(self, filename: str) -> None:
        """save all students that were not processed"""
        unprocessed = pd.DataFrame.from_dict(self.students, orient='index')
        result = unprocessed.loc[~unprocessed.index.isin(self.processed)]
        result.to_excel(filename, index=False)

    def _add_exam(self, student, path) -> None:
        """Add exam to student and exam list"""
        exam_dir = os.path.dirname(path).split(os.sep)[-1]
        exam = exam_dir.split(' ')[-1]
        self.exams.add(exam)
        if student in self.student_exams:
            self.student_exams[student].add(exam)
        else:
            self.student_exams[student] = {exam}
