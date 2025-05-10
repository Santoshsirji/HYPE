"""
This module serves as a compatibility layer for the refactored page structure.
It imports all individual page modules to ensure routes are registered correctly
when this file is imported by legacy code or tests.

Individual page implementations have been moved to:
- home_page.py
- songs_page.py 
- favourites_page.py
"""

import pages.home_page as home_page
import songs_page 
import pages.favourites_page as favourites_page

# These imports ensure all pages are registered when ui_pages is imported 