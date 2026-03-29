import requests
from bs4 import BeautifulSoup
from functools import lru_cache
import time
from datetime import datetime
import os

IMD_CYCLONE_URL = "https://mausam.imd.gov.in/responsive/cyclonewarning.php"
IMD_REPORT_URL = "https://rsmcnewdelhi.imd.gov.in/report.php"

CACHE_TTL = int(os.getenv("IMD_CACHE_TTL", "600"))
last_cache_time = {"cyclone": 0, "report": 0}
cached_data = {"cyclone": None, "report": None}


def _get_cache(key: str):
    """Get cached data if still valid."""
    if time.time() - last_cache_time[key] < CACHE_TTL:
        return cached_data[key]
    return None


def _set_cache(key: str, data):
    """Set cache with current timestamp."""
    cached_data[key] = data
    last_cache_time[key] = time.time()


def get_live():
    """
    Fetch live IMD cyclone data. If no active system, return status.
    Returns: dict with system data or { "status": "NO_ACTIVE_SYSTEM", "checked_at": timestamp }
    """
    cached = _get_cache("cyclone")
    if cached:
        return cached

    try:
        cyclone_data = _scrape_cyclone_page()

        if cyclone_data:
            result = {
                "status": "ACTIVE",
                "system_name": cyclone_data.get("system_name"),
                "category": cyclone_data.get("category"),
                "lat": cyclone_data.get("lat"),
                "lon": cyclone_data.get("lon"),
                "wind_speed_kmh": cyclone_data.get("wind_speed_kmh"),
                "pressure_hpa": cyclone_data.get("pressure_hpa"),
                "movement_direction": cyclone_data.get("movement_direction"),
                "movement_speed_kmh": cyclone_data.get("movement_speed_kmh"),
                "storm_surge_m": cyclone_data.get("storm_surge_m"),
                "landfall_district": cyclone_data.get("landfall_district"),
                "landfall_eta_hours": cyclone_data.get("landfall_eta_hours"),
                "rainfall_24h_mm": cyclone_data.get("rainfall_24h_mm"),
                "rainfall_48h_mm": cyclone_data.get("rainfall_48h_mm"),
                "rainfall_72h_mm": cyclone_data.get("rainfall_72h_mm"),
                "checked_at": datetime.utcnow().isoformat(),
            }
        else:
            result = {
                "status": "NO_ACTIVE_SYSTEM",
                "checked_at": datetime.utcnow().isoformat(),
            }

        _set_cache("cyclone", result)
        return result

    except Exception as e:
        return {
            "status": "ERROR",
            "error": str(e),
            "checked_at": datetime.utcnow().isoformat(),
        }


def _scrape_cyclone_page():
    """
    Scrape IMD cyclone warning page and extract structured data.
    Returns: dict with extracted fields or None if no system found.
    """
    try:
        response = requests.get(IMD_CYCLONE_URL, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "lxml")

        system_data = {}

        table = soup.find("table")
        if not table:
            return None

        rows = table.find_all("tr")
        for row in rows:
            cells = row.find_all("td")
            if len(cells) >= 2:
                label = cells[0].get_text(strip=True).lower()
                value = cells[1].get_text(strip=True)

                if "system name" in label or "system" in label:
                    system_data["system_name"] = value
                elif "category" in label:
                    system_data["category"] = value
                elif "latitude" in label:
                    try:
                        system_data["lat"] = float(value)
                    except ValueError:
                        pass
                elif "longitude" in label:
                    try:
                        system_data["lon"] = float(value)
                    except ValueError:
                        pass
                elif "wind" in label and "speed" in label:
                    try:
                        system_data["wind_speed_kmh"] = int(
                            float(value.split()[0])
                        )
                    except (ValueError, IndexError):
                        pass
                elif "pressure" in label:
                    try:
                        system_data["pressure_hpa"] = int(float(value.split()[0]))
                    except (ValueError, IndexError):
                        pass
                elif "movement" in label and "direction" in label:
                    system_data["movement_direction"] = value
                elif "movement" in label and "speed" in label:
                    try:
                        system_data["movement_speed_kmh"] = int(
                            float(value.split()[0])
                        )
                    except (ValueError, IndexError):
                        pass
                elif "surge" in label or "storm surge" in label:
                    try:
                        system_data["storm_surge_m"] = float(value.split()[0])
                    except (ValueError, IndexError):
                        pass
                elif "landfall" in label and "district" in label:
                    system_data["landfall_district"] = value
                elif "landfall" in label and "eta" in label:
                    try:
                        system_data["landfall_eta_hours"] = int(float(value.split()[0]))
                    except (ValueError, IndexError):
                        pass

        if "rainfall_24h_mm" not in system_data:
            system_data["rainfall_24h_mm"] = 0
        if "rainfall_48h_mm" not in system_data:
            system_data["rainfall_48h_mm"] = 0
        if "rainfall_72h_mm" not in system_data:
            system_data["rainfall_72h_mm"] = 0

        if system_data.get("system_name"):
            return system_data

        return None

    except Exception as e:
        print(f"Error scraping IMD cyclone page: {e}")
        return None
