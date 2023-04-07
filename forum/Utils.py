import string
from Utils import *

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
    def set_filter_range(begin_col:int, last_col:int, worksheet) -> None:
        """Set worksheet autofilter range"""
        if worksheet.dim_rowmax > 0:
            worksheet.autofilter(0, begin_col, worksheet.dim_rowmax, last_col)   

    @staticmethod
    def get_size_by_values(col:str, df) -> int :
        """Get size of given column by the maximal value in the given column""" 
        values = df[col].values
        longest_string = max(values, key=len)
        return len(longest_string)  
    
    @staticmethod
    def set_filter_range(begin_col:int, last_col:int, worksheet) -> None:
        """Set worksheet autofilter range"""
        if worksheet.dim_rowmax > 0:
            worksheet.autofilter(0, begin_col, worksheet.dim_rowmax, last_col)