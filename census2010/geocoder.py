"""
Census 2010
===========

Geocoder
--------

Geocoder sub-package provides tools to:
1. add a unique Geocode (OKTMO) to every line of dataset based on two
values - municipality name, oblast code
"""


def geocode(src_fn: str, dest_fn: str):
    """
    Load a pandas-compatible DataFrame of municipality data, assign
    geocodes to each line and save a new DataFrame with an additional
    geocode column.
    """
