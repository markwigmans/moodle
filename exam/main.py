"""main file of exam application"""

from GradeSheet import *
from Exams import *
import configparser

def main():
    config = configparser.ConfigParser()
    config.read(['default.ini','config.ini'])
    grades_cfg = config['grades']
    grades = GradeSheet(grades_cfg['file'], grades_cfg['worksheet'], int(grades_cfg['header']))
    students, markers = grades.read()

    files_cfg = config['files']
    exams = Exams(files_cfg['data'], files_cfg['output'], students, markers)
    exams.process(files_cfg['not_processed'])
    exams.gen_overview(files_cfg['overview'])

if __name__ == '__main__':
    main()