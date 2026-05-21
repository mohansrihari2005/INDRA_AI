import json
from typing import Optional


# =============================================================================
# UTILITY FUNCTIONS (Non-Agent)
# =============================================================================

def generate_english_sms(district: str, warning_color: str, ndrf_name: str) -> str:
    """
    Generate English SMS alert (max 160 characters).
    """
    color_text = {
        "RED": "ALERT",
        "ORANGE": "WARN",
        "YELLOW": "WATCH",
        "GREEN": "MONITOR",
    }

    color = color_text.get(warning_color, "ALERT")

    sms = (
        f"NDMA {color}: Severe weather approaching {district}. "
        f"Evacuate immediately. Call 1078 (NDMA) or 112. "
        f"Stay safe. {ndrf_name} deployed."
    )

    if len(sms) > 160:
        sms = (
            f"NDMA {color}: {district} at risk. Evacuate now. "
            f"Call 1078 or 112. {ndrf_name} deployed."
        )

    return sms[:160]


def generate_english_advisory(
    district: str, state: str, warning_color: str, wind_speed_kmh: int
) -> str:
    """
    Generate full English advisory (3-5 sentences).
    """
    advisory = f"For {district}, {state}: "

    if warning_color == "RED":
        advisory += (
            f"Severe storm with winds over {wind_speed_kmh} km/h is approaching. "
            f"Immediate evacuation is mandatory. Proceed to designated shelters now. "
            f"Do not wait for further warnings."
        )
    elif warning_color == "ORANGE":
        advisory += (
            f"Strong storm with winds {wind_speed_kmh} km/h expected in 12-24 hours. "
            f"Begin evacuation preparations and move to higher ground if in coastal areas. "
            f"Follow District Administration instructions."
        )
    elif warning_color == "YELLOW":
        advisory += (
            f"Storm with winds {wind_speed_kmh} km/h possible within 24-48 hours. "
            f"Remain alert and ready to evacuate on short notice. "
            f"Monitor official announcements."
        )
    else:
        advisory += (
            f"Weather system being monitored. Winds {wind_speed_kmh} km/h. "
            f"Remain alert. Emergency services on standby. "
            f"Follow official channels for updates."
        )

    return advisory


def generate_telugu_alert(
    district: str, warning_color: str, ndrf_name: str
) -> str:
    """
    Generate Telugu alert in Telugu script.
    """
    color_text = {
        "RED": "జరూరు హెచ్చరిక",
        "ORANGE": "ఓ హెచ్చరిక",
        "YELLOW": "కనిష్ఠ హెచ్చరిక",
        "GREEN": "సాధారణ పర్యవేక్షణ",
    }

    color = color_text.get(warning_color, "సమాచారం")

    alert = (
        f"NDMA {color}: {district} కు తీవ్ర వాతావరణ ప్రవాహం కు చేరుకోయడం. "
        f"వెంటనే సమ్మె జరుపుకోండి. 1078 లేదా 112 కు కాల్ చేయండి. "
        f"{ndrf_name} ప్రయోగించబడింది."
    )

    return alert


def generate_hindi_alert(
    district: str, warning_color: str, ndrf_name: str
) -> str:
    """
    Generate Hindi alert in Devanagari script.
    """
    color_text = {
        "RED": "गंभीर चेतावनी",
        "ORANGE": "उंची चेतावनी",
        "YELLOW": "न्यून चेतावनी",
        "GREEN": "निगरानी",
    }

    color = color_text.get(warning_color, "सूचना")

    alert = (
        f"NDMA {color}: {district} को भीषण तूफान का खतरा। "
        f"तुरंत खालি करें। 1078 या 112 पर कॉल करें। "
        f"सुरक्षित रहें। {ndrf_name} तैनात किया गया है।"
    )

    return alert


def generate_odia_alert(
    district: str, warning_color: str, ndrf_name: str
) -> str:
    """
    Generate Odia alert in Odia script.
    """
    color_text = {
        "RED": "ଗୁରୁତର ସଚେତନତା",
        "ORANGE": "ଉଚ୍ଚ ସଚେତନତା",
        "YELLOW": "ନିମ୍ନ ସଚେତନତା",
        "GREEN": "ତଦାରଖ",
    }

    color = color_text.get(warning_color, "ସୂଚନା")

    alert = (
        f"NDMA {color}: {district} ରେ ଭୟାବହ ତୁଫାନ ଆସୁଛି। "
        f"ତାତକାଳ ଖାଲି କରନ୍ତୁ। 1078 କିମ୍ବା 112 ରେ କଲ କରନ୍ତୁ। "
        f"{ndrf_name} ମୋତାୟନ କରାଯାଇଛି।"
    )

    return alert


def generate_tamil_alert(
    district: str, warning_color: str, ndrf_name: str
) -> str:
    """
    Generate Tamil alert in Tamil script.
    """
    color_text = {
        "RED": "கடுமையான எச்சரிக்கை",
        "ORANGE": "உயர் எச்சரிக்கை",
        "YELLOW": "குறைந்த எச்சரிக்கை",
        "GREEN": "கண்காணிப்பு",
    }

    color = color_text.get(warning_color, "தகவல்")

    alert = (
        f"NDMA {color}: {district} க்கு கடுமையான புயல் வருகிறது। "
        f"உடனே வெளியேறவும். 1078 அல்லது 112 ஐ அழையுங்கள். "
        f"பாதுகாப்பாக இருங்கள். {ndrf_name} பகுதிக்கு அனுப்பப்பட்டது."
    )

    return alert


def generate_role_checklists(
    district: str, risk_label: str, ndrf_name: str, state: str
) -> dict:
    """
    Generate role-specific checklists (6 departments, 5 items each).
    """
    return {
        "police": [
            f"Enforce immediate evacuation of {district} coastal area",
            f"Set up 5 emergency checkpoints on evacuation routes",
            f"Coordinate with {ndrf_name} for mass transportation",
            "Activate emergency communication network with WhatsApp/Radio groups",
            "Deploy riot control equipment to prevent panicked looting",
        ],
        "revenue": [
            f"Issue official evacuation order for {district}",
            f"Activate all relief camps with capacity for {risk_label} risk population",
            "Coordinate land documents recovery from revenue offices",
            f"Arrange for livestock movement from {district} to inland areas",
            "Prepare ex-gratia payout lists based on real assessment data",
        ],
        "health": [
            f"Pre-position medical teams at {district} evacuation centers",
            "Stock 500+ first-aid kits and critical medicines",
            "Set up floating mobile clinics for post-disaster medical aid",
            "Brief all ASHA/ANM workers on emergency health protocols",
            "Identify water-borne disease hotspots for early intervention",
        ],
        "panchayat": [
            f"Conduct village-by-village evacuation drills in {district}",
            "Register vulnerable populations (elderly, disabled, pregnant women)",
            f"Identify and mark {ndrf_name} assembly points for easier coordination",
            "Organize volunteer training for community-based disaster response",
            "Prepare ward-level action registers with real contact numbers",
        ],
        "ngos": [
            f"Coordinate community kitchens at {district} relief camps",
            "Run psychosocial support programs for evacuees and families",
            f"Establish coordination with {ndrf_name} for last-mile logistics",
            "Deploy health workers to camps for medical surveillance",
            "Document testimonies and losses for rapid damage assessment",
        ],
        "fishermen": [
            f"Secure all fishing boats and equipment away from {district} coast",
            "Relocate family members to designated shelters immediately",
            "Register with local fisheries office for relief eligibility",
            "Avoid sea entry — even for small fishing in next 72 hours",
            "Keep boat registration papers and motor certificates safe",
        ],
    }


def generate_do_not_list(district: str, warning_color: str, state: str) -> list:
    """
    Generate critical DO NOT list based on risk level.
    """
    do_not_items = [
        f"Do NOT delay evacuation for any personal items",
        f"Do NOT travel by road in {district} without authorization",
        f"Do NOT venture near sea or riverbanks during the storm",
        f"Do NOT attempt sea rescue unless officially authorized",
        f"Do NOT spread rumors — use only official government channels",
    ]

    if warning_color in ["RED", "ORANGE"]:
        do_not_items.extend([
            f"Do NOT remain in non-concrete structures in {district}",
            f"Do NOT let children or elderly stay behind during evacuation",
        ])

    return do_not_items


# =============================================================================
# AUTOGEN TOOLS (exposed for AutoGen agent function_map)
# =============================================================================

def evacuation_generate_alerts(hazard_json: str, risk_json: str, resource_json: str, geo_json: str) -> str:
    """
    Tool for AutoGen: Generate multilingual evacuation alerts and checklists.
    Takes JSON strings and returns evacuation plan as JSON string.
    """
    try:
        hazard_report = json.loads(hazard_json)
        risk_assessment = json.loads(risk_json)
        resource_plan = json.loads(resource_json)
        geo = json.loads(geo_json)
        
        district = geo.get("district", "N/A")
        state = geo.get("state", "N/A")
        warning_color = hazard_report.get("warning_color", "YELLOW")
        wind_speed = hazard_report.get("wind_speed_kmh", 0)
        risk_label = risk_assessment.get("risk_label", "MODERATE")
        ndrf_name = resource_plan.get("nearest_ndrf", {}).get("name", "NDRF Unit")
        
        english_sms = generate_english_sms(district, warning_color, ndrf_name)
        english_full = generate_english_advisory(district, state, warning_color, wind_speed)
        telugu = generate_telugu_alert(district, warning_color, ndrf_name)
        hindi = generate_hindi_alert(district, warning_color, ndrf_name)
        
        odia = None
        if state == "Odisha":
            odia = generate_odia_alert(district, warning_color, ndrf_name)
        
        tamil = None
        if state in ["Tamil Nadu", "Puducherry"]:
            tamil = generate_tamil_alert(district, warning_color, ndrf_name)
        
        role_plans = generate_role_checklists(district, risk_label, ndrf_name, state)
        do_not_list = generate_do_not_list(district, warning_color, state)
        
        plan = {
            "english_sms": english_sms,
            "english_full": english_full,
            "telugu": telugu,
            "hindi": hindi,
            "odia": odia,
            "tamil": tamil,
            "role_plans": role_plans,
            "do_not_list": do_not_list,
        }
        return json.dumps(plan)
    except Exception as e:
        return json.dumps({"error": str(e)})


# =============================================================================
# AGENT FACTORY (for AutoGen integration)
# =============================================================================

def get_evacuation_agent(llm_config: dict):
    """
    Factory function to create an Evacuation Communication AutoGen Agent.
    Returns a ConversableAgent configured as Mass Communication Officer.
    """
    from autogen import ConversableAgent
    
    evacuation_agent = ConversableAgent(
        name="EvacuationCoordinator",
        system_message="""You are the Mass Communication Officer for India's National Disaster Management Authority (NDMA).
Your role is to generate multilingual evacuation alerts and coordinate departmental response checklists.

When communicating evacuation plans:
1. Generate concise SMS alerts (max 160 characters) in English and multiple Indian languages
2. Create detailed advisories with clear action items for each risk level
3. Generate role-specific checklists for Police, Revenue, Health, Panchayat, NGOs, and Fishermen
4. Provide critical DO NOT lists for public safety
5. Localize all communications to specific districts and states

Always provide:
- English SMS (160 chars max) for rapid mass communication
- Full English advisory with detailed guidance
- Multilingual alerts in Telugu, Hindi, Odia (for Odisha), and Tamil (for TN)
- Department-specific action checklists (5 items per dept)
- Critical safety warnings in priority order

Your communications save lives by ensuring clarity, reducing confusion, and enabling coordinated action.""",
        llm_config=llm_config,
        human_input_mode="NEVER",
    )
    
    return evacuation_agent


# =============================================================================
# LEGACY FUNCTION (backward compatibility)
# =============================================================================

def evacuation_agent(
    hazard_report: dict,
    risk_assessment: dict,
    resource_plan: dict,
    geo: dict,
    openai_client,
) -> dict:
    """
    Mass Communication Agent for evacuation alerts and checklists (legacy - for backward compatibility).
    """
    district = geo.get("district", "N/A")
    state = geo.get("state", "N/A")
    warning_color = hazard_report.get("warning_color", "YELLOW")
    wind_speed = hazard_report.get("wind_speed_kmh", 0)
    risk_label = risk_assessment.get("risk_label", "MODERATE")
    ndrf_name = resource_plan.get("nearest_ndrf", {}).get("name", "NDRF Unit")

    english_sms = generate_english_sms(district, warning_color, ndrf_name)
    english_full = generate_english_advisory(
        district, state, warning_color, wind_speed
    )
    telugu = generate_telugu_alert(district, warning_color, ndrf_name)
    hindi = generate_hindi_alert(district, warning_color, ndrf_name)

    odia = None
    if state == "Odisha":
        odia = generate_odia_alert(district, warning_color, ndrf_name)

    tamil = None
    if state in ["Tamil Nadu", "Puducherry"]:
        tamil = generate_tamil_alert(district, warning_color, ndrf_name)

    role_plans = generate_role_checklists(district, risk_label, ndrf_name, state)
    do_not_list = generate_do_not_list(district, warning_color, state)

    return {
        "english_sms": english_sms,
        "english_full": english_full,
        "telugu": telugu,
        "hindi": hindi,
        "odia": odia,
        "tamil": tamil,
        "role_plans": role_plans,
        "do_not_list": do_not_list,
    }
