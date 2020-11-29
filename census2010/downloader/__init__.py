"""
Census 2010
===========

Downloader
----------

Downloader subpackage provides tools to:
1. Go to Russian Statistics web-site
2. Follow down the link path to a specific indicator in specific oblast
3. Fill out data request form
4. Extract the HTML data
5. Save HTML to disk
"""

from .downloader import download, download_single
from .downloader import download_region, download_range, download_all
from .downloader import download_indicator
from .post_process import format_folder, extract_metadata, html_to_csv
