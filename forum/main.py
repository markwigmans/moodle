"""main file of forum application"""

from GradeSheet import *
from Posts import *
import configparser

def main():
    """Main application"""
    config = configparser.ConfigParser()
    config.read('config.ini')
    grades_cfg = config['grades']
    overview = GradeSheet(grades_cfg['file'], grades_cfg['worksheet']).read()
    sheets_list = [
        ("P-1", "Session 4  - Creating Money", Posts("discussion-1.csv").read()),
        ("P-2", "Session 6  - Securitization", Posts("discussion-2.csv").read()),
        ("P-3", "Session 8  - Central bank digital currencies", Posts("discussion-3.csv").read()),
        ("P-4", "Session 10 - Valuation of Financial Instruments",Posts("discussion-4.csv").read()),
        ("P-5", "Session 12 - Evaluating Cryptocurrencies", Posts("discussion-5.csv").read()),
    ]
    participation = calc_participation(overview, sheets_list)
    gen_sheet("participation.xlsx", participation, overview, sheets_list)

if __name__ == '__main__':
    main()
