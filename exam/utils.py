"""Utility functions"""

import string

def normalize_key(key: str, remove_chars: str = string.whitespace) -> str:
    """Remove all specified characters from the input string and return the result in lowercase."""
    if key is not None:
        translation_table = str.maketrans("", "", remove_chars)
        return key.translate(translation_table).lower()
    return ""