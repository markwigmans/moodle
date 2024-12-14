import re

from pandas import DataFrame
from xlsxwriter import utility


class Utils:
    """Utility functions"""

    @staticmethod
    def normalize_key(key: str) -> str:
        """Standardize the key by removing all non a-z characters and convert to lowercase."""
        if key is not None:
            return re.sub(r'[^a-zA-Z]', '', key).lower()
        return ""

    @staticmethod
    def set_filter_range(begin_col: int, last_col: int, worksheet, row: int = 0) -> None:
        """Set worksheet auto-filter range"""
        if worksheet.dim_rowmax > 0:
            worksheet.autofilter(row, begin_col, worksheet.dim_rowmax, last_col)

    @staticmethod
    def get_size_by_values(col: str, df: DataFrame) -> int:
        """Get size of given column by the maximal value in the given column"""
        values = df[col].values
        longest_string = max(values, key=len)
        return len(longest_string)

    @staticmethod
    def to_cell(col: int, row: int, row_abs=False, col_abs=False) -> str:
        """Transform col,row notation to Excel notation"""
        return utility.xl_rowcol_to_cell(col, row, row_abs, col_abs)
