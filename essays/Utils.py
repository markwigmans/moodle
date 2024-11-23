import re

class Utils:
    """Utility functions"""

    @staticmethod
    def normalize_key(key: str) -> str:
        """Standardize the key by removing all non a-z characters and convert to lowercase."""
        if key is not None:
             return re.sub(r'[^a-zA-Z]', '', key).lower()
        return ""

    @staticmethod
    def set_filter_range(begin_col:int, last_col:int, worksheet) -> None:
        """Set worksheet autofilter range"""
        if worksheet.dim_rowmax > 0:
            worksheet.autofilter(0, begin_col, worksheet.dim_rowmax, last_col)   