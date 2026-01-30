import re
from pathlib import Path
import requests

NOWCAST_URL = "https://www.glerl.noaa.gov/emf/waves/GLERL-Experimental-WW3-Data/ncast/"
OUT_DIR = Path("data/ncast")


def get_two_most_recent_files():
    r = requests.get(NOWCAST_URL, timeout=30)
    r.raise_for_status()
    files = sorted(set(re.findall(r"\b\d{6}_ww3\.nc\b", r.text)))
    return files[-2:]


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    files = get_two_most_recent_files()

    if not files:
        raise RuntimeError("No nowcast files found")

    for fname in files:
        out = OUT_DIR / fname
        if out.exists():
            continue
        with requests.get(NOWCAST_URL + fname, stream=True) as r:
            r.raise_for_status()
            out.write_bytes(r.content)


if __name__ == "__main__":
    main()
