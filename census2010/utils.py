"""
Census 2010
===========

Utilities
---------

Utilities sub-package provides tools to:
- validate folder names
- create folder if it doesn't exist
"""

import os


def _validate_folder(folder: str) -> str:
    """Check if dir. name ends in '/' suffix and add it if necesary."""
    return folder if folder.endswith('/') else folder + '/'

def create_folder(folder: str):
    """Create a directory if it doesn't exist."""
    if not os.path.isdir(_validate_folder(folder)):
        os.makedirs(folder)
