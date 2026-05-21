import json


# =============================================================================
# UTILITY FUNCTIONS (Non-Agent)
# =============================================================================

def calculate_indra_risk_score(hazard_report: dict) -> tuple:
    """
    Calculate INDRA Risk Score using the exact formula.
    Returns: (score, label, wind_factor, surge_factor, rainfall_factor)
    """
    wind_speed_kmh = hazard_report.get("wind_speed_kmh", 0)
    storm_surge_m = hazard_report.get("storm_surge_m", 0)
    rainfall_24h_mm = hazard_report.get("rainfall_24h_mm", 0)

    wind_factor = min(wind_speed_kmh / 250, 1) * 100
    surge_factor = min(storm_surge_m / 6, 1) * 100
    rainfall_factor = min(rainfall_24h_mm / 300, 1) * 100

    risk_score = (wind_factor * 0.4 + surge_factor * 0.35 + rainfall_factor * 0.25)
    risk_score = round(risk_score)

    if risk_score >= 80:
        label = "CRITICAL"
    elif risk_score >= 60:
        label = "HIGH"
    elif risk_score >= 40:
        label = "MODERATE"
    else:
        label = "LOW"

    return risk_score, label, wind_factor, surge_factor, rainfall_factor


def identify_high_risk_areas(state: str, risk_label: str) -> list:
    """
    Identify high-risk coastal areas based on state.
    """
    coastal_areas = {
        "Andhra Pradesh": [
            {"name": "Visakhapatnam coast", "reason": "Major industrial port"},
            {"name": "Nellore district", "reason": "Low-lying coastal area"},
        ],
        "Odisha": [
            {"name": "Paradip port", "reason": "Significant cyclone exposure"},
            {"name": "Balasore district", "reason": "High-risk coastal zone"},
            {"name": "Puri district", "reason": "Historic cyclone impact area"},
        ],
        "West Bengal": [
            {"name": "Sundarbans delta", "reason": "Mangrove ecosystem at risk"},
            {"name": "Kolkata port area", "reason": "Urban coastal vulnerability"},
        ],
        "Tamil Nadu": [
            {"name": "Chennai coast", "reason": "Major urban-industrial center"},
            {"name": "Pondicherry region", "reason": "Coastal vulnerability"},
        ],
        "Kerala": [
            {"name": "Kochi port", "reason": "Major port infrastructure"},
            {"name": "Northern Kerala coast", "reason": "Cyclone impact zone"},
        ],
    }

    areas = coastal_areas.get(state, [])

    if risk_label in ["CRITICAL", "HIGH"]:
        return areas
    else:
        return areas[:1] if areas else []


def build_risk_narrative(
    risk_score: int,
    label: str,
    wind_factor: float,
    surge_factor: float,
    rainfall_factor: float,
    state: str,
) -> str:
    """
    Build a narrative explanation of the risk assessment.
    """
    narrative = f"INDRA Risk Score: {risk_score}/100 ({label}). "
    narrative += f"Calculation: Wind factor {wind_factor:.1f} (40% weight) + "
    narrative += f"Surge factor {surge_factor:.1f} (35% weight) + "
    narrative += f"Rainfall factor {rainfall_factor:.1f} (25% weight). "

    if label == "CRITICAL":
        narrative += f"Critical risk level demands immediate full mobilization in {state}."
    elif label == "HIGH":
        narrative += f"High risk level requires enhanced preparedness in {state}."
    elif label == "MODERATE":
        narrative += f"Moderate risk level warrants standard response posture in {state}."
    else:
        narrative += f"Low risk level supports monitoring-only posture in {state}."

    return narrative


# =============================================================================
# AUTOGEN TOOLS (exposed for AutoGen agent function_map)
# =============================================================================

def risk_assess_with_hazard_data(hazard_report_json: str, geo_json: str) -> str:
    """
    Tool for AutoGen: Assess risk level based on hazard data.
    Takes JSON strings and returns risk assessment as JSON string.
    """
    try:
        hazard_report = json.loads(hazard_report_json)
        geo = json.loads(geo_json)
        
        risk_score, label, wind_factor, surge_factor, rainfall_factor = (
            calculate_indra_risk_score(hazard_report)
        )
        
        state = geo.get("state", "")
        high_risk_areas = identify_high_risk_areas(state, label)
        narrative = build_risk_narrative(
            risk_score, label, wind_factor, surge_factor, rainfall_factor, state
        )
        
        assessment = {
            "indra_risk_score": risk_score,
            "risk_label": label,
            "wind_factor": round(wind_factor, 2),
            "surge_factor": round(surge_factor, 2),
            "rainfall_factor": round(rainfall_factor, 2),
            "high_risk_areas": high_risk_areas,
            "narrative": narrative,
        }
        return json.dumps(assessment)
    except Exception as e:
        return json.dumps({"error": str(e)})


# =============================================================================
# AGENT FACTORY (for AutoGen integration)
# =============================================================================

def get_risk_agent(llm_config: dict):
    """
    Factory function to create a Risk Assessment AutoGen Agent.
    Returns a ConversableAgent configured as Risk Officer.
    """
    from autogen import ConversableAgent
    
    risk_agent = ConversableAgent(
        name="RiskAssessor",
        system_message="""You are the Risk Assessment Officer for India's National Disaster Management Authority (NDMA).
Your role is to calculate and communicate disaster risk levels based on hazard assessments.

When assessing risk:
1. Use the INDRA Risk Score formula: (Wind × 40% + Storm Surge × 35% + Rainfall × 25%)
2. Normalize components: wind/250×100, surge/6×100, rainfall/300×100
3. Classify risk level: CRITICAL (≥80), HIGH (≥60), MODERATE (≥40), LOW (<40)
4. Identify high-risk areas within the state
5. Build clear narratives explaining the risk assessment

Always provide:
- Numerical risk score (0-100)
- Risk label (CRITICAL/HIGH/MODERATE/LOW)
- Factor breakdowns for transparency
- Geographic risk zones for the state
- Clear, actionable risk narrative

Your assessments guide resource allocation and response coordination.""",
        llm_config=llm_config,
        human_input_mode="NEVER",
    )
    
    return risk_agent


# =============================================================================
# LEGACY FUNCTION (backward compatibility)
# =============================================================================

def risk_agent(
    hazard_report: dict, geo: dict, openai_client
) -> dict:
    """
    Risk Assessment Agent (legacy - for backward compatibility).
    Receives hazard_report and geo, produces risk assessment.
    """
    risk_score, label, wind_factor, surge_factor, rainfall_factor = (
        calculate_indra_risk_score(hazard_report)
    )

    state = geo.get("state", "")
    high_risk_areas = identify_high_risk_areas(state, label)

    narrative = build_risk_narrative(
        risk_score, label, wind_factor, surge_factor, rainfall_factor, state
    )

    return {
        "indra_risk_score": risk_score,
        "risk_label": label,
        "wind_factor": round(wind_factor, 2),
        "surge_factor": round(surge_factor, 2),
        "rainfall_factor": round(rainfall_factor, 2),
        "high_risk_areas": high_risk_areas,
        "narrative": narrative,
    }
