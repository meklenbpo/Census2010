"""
Census 2010
===========

Geocoder
--------

Geocoder sub-package provides tools to:
1. add a unique Geocode (OKTMO) to every line of dataset based on two
values - municipality name, oblast code
"""

import pandas as pd


def geocode(df: pd.DataFrame, obl_code_column: str,
                              muni_name_column: str) -> pd.DataFrame:
    """
    Take a pandas DataFrame with specified name and oblast code columns,
    assign geocodes to each lines and return a new DataFrame with
    additional geocode column.
    """
    return pd.DataFrame()