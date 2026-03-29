import requests
from functools import lru_cache
import time

NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"
RATE_LIMIT_DELAY = 1.0
last_request_time = 0


def _rate_limit():
    global last_request_time
    elapsed = time.time() - last_request_time
    if elapsed < RATE_LIMIT_DELAY:
        time.sleep(RATE_LIMIT_DELAY - elapsed)
    last_request_time = time.time()


@lru_cache(maxsize=128)
def resolve_place(place: str):
    """
    Resolve a place name to coordinates and district/state using Nominatim.
    Uses User-Agent to comply with Nominatim policy.
    Returns: { display_name, lat, lon, district, state }
    Raises ValueError if place not found in India.
    """
    _rate_limit()

    headers = {"User-Agent": "INDRA-AI-Disaster-System/2.0"}
    params = {
        "q": place,
        "format": "json",
        "countrycodes": "in",
        "limit": 1,
    }

    response = requests.get(NOMINATIM_URL, params=params, headers=headers, timeout=10)
    response.raise_for_status()

    results = response.json()
    if not results:
        raise ValueError(f"Place '{place}' not found in India")

    result = results[0]
    display_name = result.get("display_name", "")
    lat = float(result.get("lat"))
    lon = float(result.get("lon"))

    district, state = _parse_district_state(display_name)

    return {
        "display_name": display_name,
        "lat": lat,
        "lon": lon,
        "district": district,
        "state": state,
    }


def _parse_district_state(display_name: str):
    """
    Parse district and state from Nominatim display_name.
    Format typically: "..., district, state, India"
    Returns: (district, state)
    """
    parts = [p.strip() for p in display_name.split(",")]

    if len(parts) >= 2:
        state = parts[-2]
        district = parts[-3] if len(parts) >= 3 else parts[-1]
        return district, state

    return "", ""
