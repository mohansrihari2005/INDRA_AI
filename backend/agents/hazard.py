import json
from typing import Optional
from datetime import datetime


def determine_warning_color(
    imd_data: dict, wind_speed_kmh: int, landfall_eta_hours: Optional[int]
) -> str:
    """
    Determine warning color based on IMD-style criteria.
    RED = landfall ETA < 12h OR wind > 160 km/h
    ORANGE = ETA 12-24h OR wind 120-160 km/h
    YELLOW = ETA 24-48h OR wind 80-120 km/h
    GREEN = ETA > 48h OR wind < 80 km/h
    """
    if landfall_eta_hours is not None:
        if landfall_eta_hours < 12:
            return "RED"
        elif landfall_eta_hours < 24:
            return "ORANGE"
        elif landfall_eta_hours < 48:
            return "YELLOW"

    if wind_speed_kmh > 160:
        return "RED"
    elif wind_speed_kmh >= 120:
        return "ORANGE"
    elif wind_speed_kmh >= 80:
        return "YELLOW"

    return "GREEN"


def build_hazard_assessment(
    imd_data: dict, weather_data: dict, geo: dict, openai_client
) -> dict:
    """
    Use LLM to build hazard assessment from raw data.
    """
    system_name = imd_data.get("system_name", "")
    category = imd_data.get("category", "")
    wind_speed_kmh = imd_data.get("wind_speed_kmh", 0)
    pressure_hpa = imd_data.get("pressure_hpa", 0)
    storm_surge_m = imd_data.get("storm_surge_m", 0)
    landfall_eta_hours = imd_data.get("landfall_eta_hours")
    rainfall_24h = imd_data.get("rainfall_24h_mm", 0)
    rainfall_48h = imd_data.get("rainfall_48h_mm", 0)
    rainfall_72h = imd_data.get("rainfall_72h_mm", 0)

    data_source = imd_data.get("status", "")
    if data_source == "NO_ACTIVE_SYSTEM":
        data_source = "NO_ACTIVE_SYSTEM"
        wind_speed_kmh = max(
            wind_speed_kmh, weather_data.get("wind_speed_kmh", 0)
        )
    elif data_source == "ACTIVE":
        data_source = "IMD_LIVE"
    else:
        data_source = "OPENWEATHER_ONLY"

    warning_color = determine_warning_color(
        imd_data, wind_speed_kmh, landfall_eta_hours
    )

    context = f"""
    Raw Meteorological Data:
    System Name: {system_name or 'None detected'}
    Category: {category or 'N/A'}
    Wind Speed: {wind_speed_kmh} km/h
    Pressure: {pressure_hpa} hPa
    Storm Surge: {storm_surge_m} m
    Landfall ETA: {landfall_eta_hours} hours
    Rainfall 24h: {rainfall_24h} mm
    Rainfall 48h: {rainfall_48h} mm
    Rainfall 72h: {rainfall_72h} mm
    Data Source: {data_source}
    Location: {geo.get('district', 'N/A')}, {geo.get('state', 'N/A')}

    Based on this data, produce a formal IMD-style hazard assessment.
    Include all the numeric values from the data.
    """

    try:
        response = openai_client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are the Hazard Intelligence Officer for India's NDMA. Produce official IMD-style assessments using ONLY the data provided. If no active cyclone exists, clearly state so and assess the existing weather risk from OpenWeather data.",
                },
                {"role": "user", "content": context},
            ],
            max_tokens=500,
            temperature=0.3,
        )
        bulletin_text = response.choices[0].message.content
    except Exception as e:
        bulletin_text = f"Hazard assessment error: {str(e)}"

    return {
        "system_name": system_name or "Monitoring",
        "category": category or "Unclassified",
        "warning_color": warning_color,
        "wind_speed_kmh": wind_speed_kmh,
        "pressure_hpa": pressure_hpa,
        "storm_surge_m": storm_surge_m,
        "landfall_eta_hours": landfall_eta_hours,
        "rainfall_24h_mm": rainfall_24h,
        "rainfall_48h_mm": rainfall_48h,
        "rainfall_72h_mm": rainfall_72h,
        "bulletin_text": bulletin_text,
        "data_source": data_source,
    }


def hazard_agent(imd_data: dict, weather_data: dict, geo: dict, openai_client) -> dict:
    """
    Hazard Intelligence Agent.
    Receives raw IMD and OpenWeather data, produces hazard assessment.
    """
    return build_hazard_assessment(imd_data, weather_data, geo, openai_client)
