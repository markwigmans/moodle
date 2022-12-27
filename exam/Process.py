from GradeSheet import *
from Exams import *
import sys

def main(args):
    grades = GradeSheet('BLOC512 - Fall 2022 - Grades - local.xlsx')
    exams = Exams('data', 'markers', grades.read_students())
    exams.files()

if __name__ == '__main__':
    main(sys.argv)