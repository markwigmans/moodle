"""main file of exam application"""
import configparser
import logging

from Essays import Essays
from GradeSheet import GradeSheet


def main():
    logging.basicConfig(level=logging.INFO)
    config = configparser.ConfigParser()
    config.read(['default.ini', 'config.ini'])
    grades_cfg = config['grades']
    grades = GradeSheet(grades_cfg['file'], grades_cfg['worksheet'], int(grades_cfg['header']),
                        int(grades_cfg['id_offset']))
    students, markers = grades.read()

    files_cfg = config['files']
    essays = Essays(files_cfg['data'], files_cfg['output'], int(files_cfg['refnr_length']), students, markers)
    essays.process(files_cfg['not_processed'])
    essays.gen_overview(files_cfg['overview'])


if __name__ == '__main__':
    main()
