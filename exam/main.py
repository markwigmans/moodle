"""main file of exam application"""

import configparser
import logging

from Exams import Exams
from GradeSheet import GradeSheet


def main():
    logging.basicConfig(level='INFO')
    config = configparser.ConfigParser()
    config.read(['default.ini', 'config.ini'])
    grades_cfg = config['grades']
    grades = GradeSheet(grades_cfg['file'], grades_cfg['worksheet'], int(grades_cfg['header']))
    students, markers = grades.read()

    files_cfg = config['files']
    exams = Exams(files_cfg['data'], files_cfg['output'], students, markers)
    exams.process(files_cfg['not_processed'], int(files_cfg['min_length']))
    exams.gen_overview(files_cfg['overview'])


if __name__ == '__main__':
    main()
