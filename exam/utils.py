import string
import xlsxwriter

class Utils:
    """Utility functions"""

    @staticmethod
    def normalize_key(key: str, remove_chars: str = string.whitespace) -> str:
        """Remove all specified characters from the input string and return the result in lowercase."""
        if key is not None:
            translation_table = str.maketrans("", "", remove_chars)
            return key.translate(translation_table).lower()
        return ""

    @staticmethod
    def set_filter_range(begin_col:int, last_col:int, worksheet, row:int = 0) -> None:
        """Set worksheet autofilter range"""
        if worksheet.dim_rowmax > 0:
            worksheet.autofilter(row, begin_col, worksheet.dim_rowmax, last_col)   

    @staticmethod
    def to_cell(col:int, row:int) -> str:
        """Transform col,row notation to Excel notation"""
        return xlsxwriter.utility.xl_rowcol_to_cell(col, row)