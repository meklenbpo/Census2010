"""
Census 2010
===========

Formatter
---------

Formatter sub-package provides tools to:
1. Read merged geocoded dataset from disk
2. Add header/footer text, column names etc.
3. Format colors/fonts/widths etc.
4. Save as an Excel spreadsheet file.
"""

import pandas as pd


def format_to_excel(src_df: pd.DataFrame, excel_fn: str):
    """
    Take a merged and geocoded DataFrame, format and save it to Excel
    format spreadsheet file.
    """
    raise FileNotFoundError(f'{excel_fn} not found.')
