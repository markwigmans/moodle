from GradeSheet import *
from Exams import *
import sys

def main(args):
    grades = GradeSheet('grades.xlsx', 'Students')
    exams = Exams('data', 'markers', grades.read_students())
    exams.process()
    exams.print_unprocessed()

if __name__ == '__main__':
    main(sys.argv)