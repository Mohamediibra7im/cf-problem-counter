API_URL = "https://codeforces.com/api/user.status?handle={handle}"
MIN_RATING = 800
MAX_RATING = 3500
RATING_STEP = 100 

import requests
import requests_cache
import os
from typing import Dict, List, Optional


def fetch_user_submissions(handle: str) -> Optional[List[Dict]]:
    session = requests_cache.CachedSession("codeforces_cache", expire_after=3600)
    try:
        response = session.get(API_URL.format(handle=handle))
        response.raise_for_status()
        data = response.json()

        if data["status"] != "OK":
            print(f"Error: API returned status {data['status']}")
            return None

        return data["result"]

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from Codeforces API: {e}")
        return None


def clear_cache():
    cache_file = "cache.sqlite"
    try:
        if os.path.exists(cache_file):
            os.remove(cache_file)
            print(f"Cache file {cache_file} deleted successfully")
        else:
            print(f"Cache file {cache_file} not found")
    except Exception as e:
        print(f"Error deleting cache file: {e}")
