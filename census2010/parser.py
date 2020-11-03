"""
Census 2010
===========

Parser
------

Parser sub-package provides tools to:
- read an HTML table downloaded from Russian Statistics website as a
pandas dataframe
- identify metadata for an HTML file (indicator-oblast pair)
- filter out irrelevant data
- save the filtered dataset as a pandas-compatible CSV/feather file
"""

import pandas as pd


def parse(html: str) -> pd.DataFrame:
    """
    Take a raw HTML string, process it and return a filtered version,
    converted to a pandas Dataframe.
    """
    return pd.DataFrame()

def parse_all(src_directory: str, dest_directory: str):
    """
    Scan `src_directory` for unparsed raw HTML files, parse each of them
    and save parsed versions into `dest_directory`.
    """
