"""
Census 2010
===========

is a package that provides tools to download, process and generate a
dataset that describes the most important indicators of Russian
Federation Census 2010 as agreed upon with the customer.

It includes the following sub-packages:
1. *Downloader* - downloads a single indicator table from rosstat.gov.ru
website and saves it as raw HTML

2. *Parser* - extracts relevant and strips unrelevant information from
the downloaded HTML files and saves it as pandas dataframe.

3. *Merger* - merges all relevant information into a single dataset.

4. *Geocoder* - assigns unique geocodes (OKTMO) to every line of the
merged dataframe.

5. *Formatter* - formats the geocoded dataset into a well-presented
Excel table.
"""

from .downloader import download, download_all
from .parser import parse, parse_all
from .merger import merge
from .geocoder import geocode
from .formatter import format_to_excel
