from GradeSheet import *
from Exams import *
import sys

def main(args):
    grades = GradeSheet('grades.xlsx', 'Final Exam')
    students, markers =  grades.read()
    exams = Exams('data', 'markers', students, markers)
    exams.process('not_processed.xlsx')
    exams.gen_overview('overview.xlsx')

if __name__ == '__main__':
    main(sys.argv)