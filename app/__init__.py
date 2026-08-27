from config import USE_OLD

if USE_OLD:
    from .old_fetch_data import fetch_data
else:
    from .fetch_data import fetch_data
from .dependencies import get_scraper, get_sheet_csv_handler, lifespan

__all__ = ['fetch_data', 'get_scraper', 'get_sheet_csv_handler', 'lifespan']
