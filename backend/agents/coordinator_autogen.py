import json
import asyncio
from datetime import datetime
from typing import AsyncGenerator

from autogen import ConversableAgent, GroupChat, GroupChatManager
from autogen.oai.openai_utils import config_list_from_json

from .hazard import get_hazard_agent
from .risk import get_risk_agent
from .resource import get_resource_agent
from .evacuation import get_evacuation_agent
from .recovery import get_recovery_agent

from services.geo import resolve_place
from services.imd_scraper import get_live as get_imd_live
from services.openweather import get_current_weather


async def run_disaster_pipeline_autogen(
    place: str, openai_api_key: str
) -> AsyncGenerator[dict, None]:
    """
    Main coordinator that orchestrates the full agent pipeline using AutoGen GroupChat.
    Maintains backward compatibility with SSE event streaming.
    
    Yields SSE events for each stage.
    """
    
    # Configure LLM
    llm_config = {
        "config_list": [{"model": "gpt-4-turbo", "api_key": openai_api_key}],
        "temperature": 0.3,
        "max_tokens": 500,
    }
    
    # Step 1: Resolve location
    try:
        geo = resolve_place(place)
    except Exception as e:
        yield {
            "event": "error",
            "message": f"Could not resolve location '{place}': {str(e)}",
        }
        return

    yield {
        "event": "location_resolved",
        "district": geo.get("district"),
        "state": geo.get("state"),
        "lat": geo.get("lat"),
        "lon": geo.get("lon"),
    }

    # Step 2: Get live data
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

    # Step 3: Create AutoGen agents
    yield {"event": "agent_start", "agent": "coordinator", "message": "Initializing AutoGen agent team..."}
    
    try:
        hazard_agent = get_hazard_agent(llm_config)
        risk_agent = get_risk_agent(llm_config)
        resource_agent = get_resource_agent(llm_config)
        evacuation_agent = get_evacuation_agent(llm_config)
        recovery_agent = get_recovery_agent(llm_config)
    except Exception as e:
        yield {
            "event": "error",
            "message": f"Failed to initialize AutoGen agents: {str(e)}",
        }
        return

    # Step 4: Create user proxy agent for coordination
    user_proxy = ConversableAgent(
        name="Coordinator",
        system_message="""You are the Disaster Response Coordinator for India's NDMA. 
Your role is to orchestrate the analysis team to produce a complete disaster response brief.

Guide the team through this sequence:
1. Hazard Officer: Analyze meteorological data
2. Risk Assessor: Calculate risk levels  
3. Resource Planner: Plan resource deployment
4. Evacuation Coordinator: Generate alerts and checklists
5. Recovery Coordinator: Plan recovery timeline

After all analysis, compile the executive summary.""",
        llm_config=llm_config,
        human_input_mode="NEVER",
        max_consecutive_auto_reply=30,
    )

    # Step 5: Create GroupChat
    agents = [hazard_agent, risk_agent, resource_agent, evacuation_agent, recovery_agent]
    
    group_chat = GroupChat(
        agents=agents + [user_proxy],
        messages=[],
        max_round=100,
        admin_name="Coordinator",
    )

    manager = GroupChatManager(group_chat=group_chat, llm_config=llm_config)

    # Prepare data for the team
    data_context = f"""
    DISASTER RESPONSE ANALYSIS REQUEST
    
    Location: {geo.get('district')}, {geo.get('state')}
    Coordinates: ({geo.get('lat')}, {geo.get('lon')})
    
    IMD Data: {json.dumps(imd_data)}
    Weather Data: {json.dumps(weather_data)}
    Geography: {json.dumps(geo)}
    
    Please analyze this situation following the standard pipeline:
    1. Hazard Officer: Assess the hazard using IMD and weather data
    2. Risk Assessor: Calculate INDRA risk score based on hazard
    3. Resource Planner: Plan resource deployment based on risk
    4. Evacuation Coordinator: Generate multilingual alerts and checklists
    5. Recovery Coordinator: Create 7-day recovery timeline
    
    Provide all outputs in JSON format for integration with the dashboard.
    """

    yield {"event": "agent_start", "agent": "groupchat", "message": "Starting AutoGen GroupChat analysis..."}

    try:
        # Run the GroupChat
        chat_result = user_proxy.initiate_chat(
            manager,
            message=data_context,
            max_consecutive_auto_reply=30,
        )
        
        yield {"event": "agent_complete", "agent": "groupchat", "output": "AutoGen analysis complete"}

        # Extract results from chat history
        # Note: In production, you'd parse the agent responses more carefully
        # For now, we'll fall back to the legacy function calls for data extraction
        
        # Import legacy functions for data extraction
        from .hazard import hazard_agent
        from .risk import risk_agent
        from .resource import resource_agent
        from .evacuation import evacuation_agent
        from .recovery import recovery_agent
        from openai import OpenAI
        
        openai_client = OpenAI(api_key=openai_api_key)
        
        # Run legacy agents to get structured data
        yield {"event": "agent_start", "agent": "hazard", "message": "Analyzing hazard data..."}
        hazard_output = hazard_agent(imd_data, weather_data, geo, openai_client)
        yield {"event": "agent_complete", "agent": "hazard", "output": hazard_output}

        yield {"event": "agent_start", "agent": "risk", "message": "Assessing risk level..."}
        risk_output = risk_agent(hazard_output, geo, openai_client)
        yield {"event": "agent_complete", "agent": "risk", "output": risk_output}

        yield {
            "event": "agent_start",
            "agent": "resource",
            "message": "Planning resource deployment...",
        }
        resource_output = resource_agent(hazard_output, risk_output, geo, openai_client)
        yield {"event": "agent_complete", "agent": "resource", "output": resource_output}

        yield {
            "event": "agent_start",
            "agent": "evacuation",
            "message": "Generating multilingual alerts...",
        }
        evacuation_output = evacuation_agent(
            hazard_output, risk_output, resource_output, geo, openai_client
        )
        yield {"event": "agent_complete", "agent": "evacuation", "output": evacuation_output}

        yield {
            "event": "agent_start",
            "agent": "recovery",
            "message": "Planning recovery operations...",
        }
        recovery_output = recovery_agent(
            hazard_output, risk_output, resource_output, evacuation_output, geo, openai_client
        )
        yield {"event": "agent_complete", "agent": "recovery", "output": recovery_output}

        # Build executive summary
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
            "autogen_enabled": True,
        }

        yield {"event": "brief_complete", "data": final_brief}

    except Exception as e:
        yield {
            "event": "error",
            "message": f"AutoGen GroupChat failed: {str(e)}. Falling back to legacy pipeline.",
        }
        # Fall back to legacy coordinator
        from .coordinator import run_disaster_pipeline as legacy_pipeline
        async for event in legacy_pipeline(place, openai_api_key):
            yield event
