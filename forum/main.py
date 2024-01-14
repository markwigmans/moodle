"""main file of forum application"""

from GradeSheet import *
from Posts import *
from Participation import *
import configparser

def main():
    """Main application"""
    config = configparser.ConfigParser()
    config.read(['default.ini','config.ini'])
    students_cfg = config['students']
    gradeSheet = GradeSheet(students_cfg['file'], students_cfg['worksheet']).read()

    sheets_list = []
    for section in config.sections():
        if (section.startswith('forum.')):
            title = config.get(section, 'title')
            sheets_list.append((title,
                               config.get(section, 'description'),
                               Posts(config.get(section, 'file'), title).read()))

    participation = Participation(gradeSheet, sheets_list)
    participation.gen_sheet(config.get('output','file'))

if __name__ == '__main__':
    main()
