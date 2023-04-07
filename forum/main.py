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
    overview = GradeSheet(students_cfg['file'], students_cfg['worksheet']).read()

    sheets_list = []
    for section in config.sections():
        if (section.startswith('forum.')):
            sheets_list.append((config.get(section, 'title'),
                               config.get(section, 'description'),
                               Posts(config.get(section, 'file')).read()));

    participation = Participation(overview, sheets_list)
    participation.calc()
    participation.gen_sheet(config.get('output','file'))

if __name__ == '__main__':
    main()
