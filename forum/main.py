"""main file of forum application"""

from GradeSheet import *
from Posts import *
from Participation import *
import configparser

def main():
    """Main application"""
    config = configparser.ConfigParser()
    config.read('default.ini')
    config.read('config.ini')
    students_cfg = config['students']
    overview = GradeSheet(students_cfg['file'], students_cfg['worksheet']).read()
    sheets_list = [
        ("P-1", "Session 4  - Creating Money", Posts("discussion-1.csv").read()),
        ("P-2", "Session 6  - Securitization", Posts("discussion-2.csv").read()),
        ("P-3", "Session 8  - Central bank digital currencies", Posts("discussion-3.csv").read()),
        ("P-4", "Session 10 - Valuation of Financial Instruments",Posts("discussion-4.csv").read()),
        ("P-5", "Session 12 - Evaluating Cryptocurrencies", Posts("discussion-5.csv").read()),
    ]
    participation = Participation(overview, sheets_list)
    participation.calc()
    participation.gen_sheet("participation.xlsx")

if __name__ == '__main__':
    main()
