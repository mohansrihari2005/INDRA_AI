from geopy.distance import geodesic


NDRF_UNITS = [
    {"name": "11 NDRF Battalion", "location": "Varanasi", "lat": 25.3676, "lon": 82.9960, "coverage": ["UP", "Bihar"]},
    {"name": "12 NDRF Battalion", "location": "Guwahati", "lat": 26.1445, "lon": 91.7362, "coverage": ["NE India"]},
    {"name": "01 NDRF Battalion", "location": "Ghaziabad", "lat": 28.6692, "lon": 77.4538, "coverage": ["Delhi", "NCR"]},
    {"name": "04 NDRF Battalion", "location": "Arakkonam, TN", "lat": 12.9816, "lon": 79.8864, "coverage": ["Tamil Nadu", "Kerala"]},
    {"name": "05 NDRF Battalion", "location": "Pune", "lat": 18.5204, "lon": 73.8567, "coverage": ["Maharashtra", "Goa"]},
    {"name": "08 NDRF Battalion", "location": "Guwahati", "lat": 26.1445, "lon": 91.7362, "coverage": ["Assam", "NE"]},
    {"name": "09 NDRF Battalion", "location": "Patna", "lat": 25.5941, "lon": 85.1376, "coverage": ["Bihar"]},
    {"name": "10 NDRF Battalion", "location": "Vijayawada", "lat": 16.5062, "lon": 80.6480, "coverage": ["Andhra Pradesh", "Telangana"]},
]


def calculate_haversine_eta(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calculate ETA in hours using straight-line distance and 60 km/h speed assumption.
    """
    try:
        point1 = (lat1, lon1)
        point2 = (lat2, lon2)
        distance_km = geodesic(point1, point2).kilometers
        eta_hours = distance_km / 60
        return eta_hours
    except Exception:
        return 0


def find_nearest_ndrf(geo: dict) -> tuple:
    """
    Find the nearest NDRF battalion to the target location.
    Returns: (nearest_unit, all_units_with_eta)
    """
    target_lat = geo.get("lat", 0)
    target_lon = geo.get("lon", 0)

    units_with_eta = []
    min_eta = float("inf")
    nearest_unit = None

    for unit in NDRF_UNITS:
        eta = calculate_haversine_eta(
            unit["lat"], unit["lon"], target_lat, target_lon
        )
        unit_data = {
            "name": unit["name"],
            "location": unit["location"],
            "eta_hours": round(eta, 2),
        }
        units_with_eta.append(unit_data)

        if eta < min_eta:
            min_eta = eta
            nearest_unit = unit_data

    return nearest_unit, units_with_eta


def calculate_resources(risk_score: int) -> tuple:
    """
    Calculate resource quantities using NDMA standards.
    """
    food_packets = round((risk_score * 1000) / 1000) * 1000
    water_litres = food_packets * 3
    medicine_kits = round(food_packets / 100)

    return food_packets, water_litres, medicine_kits


def identify_critical_shortages(risk_label: str) -> list:
    """
    Identify resource gaps for HIGH and CRITICAL risk levels.
    """
    if risk_label in ["CRITICAL", "HIGH"]:
        return [
            "Emergency medical supplies critically low",
            "Shelter capacity insufficient for mass evacuation",
        ]
    return []


def build_deployment_narrative(
    nearest_ndrf: dict, risk_label: str, food_packets: int, state: str
) -> str:
    """
    Build deployment narrative.
    """
    if risk_label == "LOW":
        return f"Monitoring posture recommended. {nearest_ndrf.get('name')} on alert status. Mobilization standby in {state}."
    elif risk_label in ["MODERATE"]:
        return f"Standard response posture. {nearest_ndrf.get('name')} to mobilize within 24h. {food_packets} food packets pre-positioned in {state}."
    else:
        return f"Enhanced/Full mobilization. {nearest_ndrf.get('name')} deploying immediately. {food_packets} emergency packets required in {state}."


def resource_agent(
    hazard_report: dict, risk_assessment: dict, geo: dict, openai_client
) -> dict:
    """
    Resource Logistics Agent.
    Receives hazard, risk, and geo; produces resource deployment plan.
    """
    nearest_ndrf, all_ndrf = find_nearest_ndrf(geo)

    risk_score = risk_assessment.get("indra_risk_score", 0)
    risk_label = risk_assessment.get("risk_label", "LOW")

    food_packets, water_litres, medicine_kits = calculate_resources(risk_score)

    critical_shortages = identify_critical_shortages(risk_label)

    deployment_notes = build_deployment_narrative(
        nearest_ndrf, risk_label, food_packets, geo.get("state", "")
    )

    return {
        "nearest_ndrf": nearest_ndrf,
        "all_ndrf_units": all_ndrf,
        "food_packets_required": food_packets,
        "water_litres_required": water_litres,
        "medicine_kits_required": medicine_kits,
        "critical_shortages": critical_shortages,
        "deployment_notes": deployment_notes,
    }
