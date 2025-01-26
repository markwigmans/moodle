"""main file of exam application"""

import configparser
import logging
from configparser import SectionProxy
from typing import Final

from Exams import Exams
from GradeSheet import GradeSheet

# Constants for configuration keys
GRADES_SECTION: Final[str] = 'grades'
FILES_SECTION: Final[str] = 'files'
FILE_KEY: Final[str] = 'file'
WORKSHEET_KEY: Final[str] = 'worksheet'
HEADER_KEY: Final[str] = 'header'
DATA_KEY: Final[str] = 'data'
OUTPUT_KEY: Final[str] = 'output'
NOT_PROCESSED_KEY: Final[str] = 'not_processed'
MIN_LENGTH_KEY: Final[str] = 'min_length'
OVERVIEW_KEY: Final[str] = 'overview'


def load_config() -> configparser.ConfigParser:
    config = configparser.ConfigParser()
    try:
        config.read(['default.ini', 'config.ini'])
    except configparser.Error as e:
        logging.error(f"Error reading configuration: {e}")
        raise
    return config


def setup_logging() -> None:
    logging.basicConfig(level='INFO',
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


def main() -> None:
    setup_logging()

    try:
        config = load_config()

        grades_cfg: SectionProxy = config[GRADES_SECTION]
        grades = GradeSheet(grades_cfg[FILE_KEY],
                            grades_cfg[WORKSHEET_KEY],
                            int(grades_cfg[HEADER_KEY]))
        students, markers = grades.read()

        files_cfg: SectionProxy = config[FILES_SECTION]
        exams = Exams(files_cfg[DATA_KEY],
                      files_cfg[OUTPUT_KEY],
                      students, markers)
        exams.process(files_cfg[NOT_PROCESSED_KEY],
                      int(files_cfg[MIN_LENGTH_KEY]))
        exams.gen_overview(files_cfg[OVERVIEW_KEY])

    except Exception as e:
        logging.exception(f"An error occurred: {e}")
        raise


if __name__ == '__main__':
    main()
