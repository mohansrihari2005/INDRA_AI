import json
from datetime import datetime
from typing import AsyncGenerator
from openai import OpenAI

from .hazard import hazard_agent
from .risk import risk_agent
from .resource import resource_agent
from .evacuation import evacuation_agent
from .recovery import recovery_agent
from services.geo import resolve_place
from services.imd_scraper import get_live as get_imd_live
from services.openweather import get_current_weather


async def run_disaster_pipeline(
    place: str, openai_api_key: str
) -> AsyncGenerator[dict, None]:
    """
    Main coordinator that orchestrates the full agent pipeline.
    Yields SSE events for each stage.
    """

    openai_client = OpenAI(api_key=openai_api_key)

    try:
        geo = resolve_place(place)
    except Exception as e:
        yield {
            "event": "error",
            "message": f"Could not resolve location '{place}': {str(e)}",
        }
        return

    try:
        imd_data = get_imd_live()
    except Exception as e:
        yield {
            "event": "error",
            "message": f"Could not fetch IMD data: {str(e)}",
        }
        imd_data = {"status": "ERROR", "error": str(e)}

    try:
        weather_data = get_current_weather(geo["display_name"])
    except Exception as e:
        yield {
            "event": "error",
            "message": f"Could not fetch weather data: {str(e)}",
        }
        weather_data = {"error": str(e)}

    yield {
        "event": "location_resolved",
        "district": geo.get("district"),
        "state": geo.get("state"),
        "lat": geo.get("lat"),
        "lon": geo.get("lon"),
    }

    hazard_output = None
    risk_output = None
    resource_output = None
    evacuation_output = None
    recovery_output = None

    yield {"event": "agent_start", "agent": "hazard", "message": "Analyzing hazard data..."}
    try:
        hazard_output = hazard_agent(imd_data, weather_data, geo, openai_client)
        yield {"event": "agent_complete", "agent": "hazard", "output": hazard_output}
    except Exception as e:
        yield {
            "event": "agent_error",
            "agent": "hazard",
            "error": str(e),
        }
        return

    yield {"event": "agent_start", "agent": "risk", "message": "Assessing risk level..."}
    try:
        risk_output = risk_agent(hazard_output, geo, openai_client)
        yield {"event": "agent_complete", "agent": "risk", "output": risk_output}
    except Exception as e:
        yield {
            "event": "agent_error",
            "agent": "risk",
            "error": str(e),
        }
        return

    yield {
        "event": "agent_start",
        "agent": "resource",
        "message": "Planning resource deployment...",
    }
    try:
        resource_output = resource_agent(
            hazard_output, risk_output, geo, openai_client
        )
        yield {"event": "agent_complete", "agent": "resource", "output": resource_output}
    except Exception as e:
        yield {
            "event": "agent_error",
            "agent": "resource",
            "error": str(e),
        }
        return

    yield {
        "event": "agent_start",
        "agent": "evacuation",
        "message": "Generating multilingual alerts...",
    }
    try:
        evacuation_output = evacuation_agent(
            hazard_output, risk_output, resource_output, geo, openai_client
        )
        yield {"event": "agent_complete", "agent": "evacuation", "output": evacuation_output}
    except Exception as e:
        yield {
            "event": "agent_error",
            "agent": "evacuation",
            "error": str(e),
        }
        return

    yield {
        "event": "agent_start",
        "agent": "recovery",
        "message": "Planning recovery operations...",
    }
    try:
        recovery_output = recovery_agent(
            hazard_output, risk_output, resource_output, evacuation_output, geo, openai_client
        )
        yield {"event": "agent_complete", "agent": "recovery", "output": recovery_output}
    except Exception as e:
        yield {
            "event": "agent_error",
            "agent": "recovery",
            "error": str(e),
        }
        return

    coordinator_notes = []
    if resource_output and evacuation_output:
        shortages = resource_output.get("critical_shortages", [])
        if shortages and evacuation_output.get("english_sms"):
            if "shortage" not in evacuation_output["english_sms"].lower():
                coordinator_notes.append(
                    "Resource shortages detected but not mentioned in evacuation alerts. "
                    "Recommend emphasizing supply constraints in public communications."
                )

    executive_summary = ""
    if hazard_output and risk_output:
        risk_label = risk_output.get("risk_label", "MODERATE")
        district = geo.get("district", "N/A")

        if risk_label == "CRITICAL":
            nearest_ndrf = resource_output.get("nearest_ndrf", {})
            ndrf_name = nearest_ndrf.get("name", "NDRF")
            executive_summary = (
                f"Critical risk level in {district}. "
                f"Immediate full evacuation required. "
                f"{ndrf_name} mobilizing now. Follow District Administration instructions on 1078."
            )
        elif risk_label == "HIGH":
            nearest_ndrf = resource_output.get("nearest_ndrf", {})
            ndrf_name = nearest_ndrf.get("name", "NDRF")
            executive_summary = (
                f"High risk level in {district}. "
                f"Begin evacuation from coastal areas. "
                f"{ndrf_name} on active deployment. Stay alert."
            )
        elif risk_label == "MODERATE":
            executive_summary = (
                f"Moderate risk in {district}. "
                f"Standard emergency preparedness active. "
                f"Monitor official updates."
            )
        else:
            executive_summary = f"Low risk in {district}. Monitoring continuing."

    final_brief = {
        "district": geo.get("district", ""),
        "state": geo.get("state", ""),
        "lat": geo.get("lat", 0),
        "lon": geo.get("lon", 0),
        "hazard": hazard_output,
        "risk": risk_output,
        "resource": resource_output,
        "evacuation": evacuation_output,
        "recovery": recovery_output,
        "executive_summary": executive_summary,
        "coordinator_notes": coordinator_notes,
        "generated_at": datetime.utcnow().isoformat(),
    }

    yield {"event": "brief_complete", "data": final_brief}
