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

import pandas as pd


def merge(list_of_dfs: list) -> pd.DataFrame:
    """
    Take a list of parsed datasets and merge it into one well-formed
    dataset.
    """
    return pd.DataFrame()
