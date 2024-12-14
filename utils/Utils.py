import re
from typing import Optional

import pandas as pd
from xlsxwriter.utility import xl_rowcol_to_cell
from xlsxwriter.worksheet import Worksheet


class Utils:
    """Utility functions for data processing and Excel operations."""

    @staticmethod
    def normalize_key(key: Optional[str]) -> str:
        """Standardize the key by removing all non a-z characters and convert to lowercase."""
        if key is not None:
            return re.sub(r'[^a-zA-Z]', '', key).lower()
        return ""

    @staticmethod
    def set_filter_range(begin_col: int, last_col: int, worksheet: Worksheet, row: int = 0) -> None:
        """Set worksheet auto-filter range"""
        if worksheet.dim_rowmax > 0:
            worksheet.autofilter(row, begin_col, worksheet.dim_rowmax, last_col)

    @staticmethod
    def get_max_column_width(col: str, df: pd.DataFrame) -> int:
        """Get the maximum width of a column based on its values."""
        if col not in df.columns:
            raise KeyError(f"Column '{col}' not found in DataFrame")
        return df[col].astype(str).str.len().max()


    @staticmethod
    def to_cell(col: int, row: int, row_abs=False, col_abs=False) -> str:
        """Transform col,row notation to Excel notation"""
        return xl_rowcol_to_cell(col, row, row_abs, col_abs)
