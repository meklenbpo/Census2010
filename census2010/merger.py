"""
Census 2010
===========

Merger
------

Merger sub-package provides tools to:
1. scan through a list of indicator dataframes
2. merge them into one country-wide dataset with all possible indicators
included
3. save the merged dataframe to disk
"""

def merge(src_directory: str, dest_filename: str):
    """
    Scan `src_directory` folder for parsed dataframes, merge them into
    one well-formed dataset and save as a pandas-compatible file.
    """
