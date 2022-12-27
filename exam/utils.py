"""Unit functions"""

def normalize_key(string):
    '''remove all whitespace characters'''
    return ''.join(string.split()).lower()