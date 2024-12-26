"""main file of forum application"""

import configparser
import logging

from GradeSheet import GradeSheet
from Participation import Participation
from Posts import Posts


def main():
    """Main application"""
    logging.basicConfig(level=logging.INFO)

    config = configparser.ConfigParser()
    config.read(['default.ini', 'config.ini'])
    students_cfg = config['students']
    grade_sheet = GradeSheet(students_cfg['file'], students_cfg['worksheet']).read()

    sheets_list = []
    for section in config.sections():
        if section.startswith('forum.'):
            title = config.get(section, 'title')
            sheets_list.append((title,
                                config.get(section, 'description'),
                                Posts(config.get(section, 'file'), title).read()))

    participation = Participation(grade_sheet, sheets_list)
    participation.gen_sheet(config.get('output', 'file'))


if __name__ == '__main__':
    main()
