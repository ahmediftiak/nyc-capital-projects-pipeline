import os
import requests
import pandas as pd

BASE_URL = "https://data.cityofnewyork.us/resource/fb86-vt7u.json"
PAGE_SIZE = 10000


def fetch_all(base_url, page_size=PAGE_SIZE):
    """Pull every row from a NYC Open Data endpoint, one page at a time."""
    frames = []
    offset = 0
    while True:
        params = {"$limit": page_size, "$offset": offset, "$order": ":id"}
        resp = requests.get(base_url, params=params, timeout=120)
        resp.raise_for_status()
        rows = resp.json()
        if not rows:
            break
        frames.append(pd.DataFrame(rows))
        offset += page_size
        print(f"Fetched {offset} rows so far...")
    return pd.concat(frames, ignore_index=True)


if __name__ == "__main__":
    os.makedirs("data", exist_ok=True)
    df = fetch_all(BASE_URL)
    print(df.shape)
    print(df.head())
    df.to_csv("data/capital_projects_budget_raw.csv", index=False)