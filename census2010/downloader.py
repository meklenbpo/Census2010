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

def download(indicator_code: str, oblast_code: str) -> str:
    """
    Download an HTML table of a specified indicator for a specified
    oblast and return it as string.
    """
    return ''

def download_all(save_directory: str):
    """
    Consequently download every indicator for every oblast and save
    obtained tables as separate files to a specified folder.
    """
