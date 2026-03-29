

NDRF_COMPENSATION = {
    "death": "Rs 4,00,000 per family",
    "pucca_full": "Rs 95,100",
    "pucca_partial": "Rs 5,200",
    "kutcha_full": "Rs 50,800",
    "kutcha_partial": "Rs 3,200",
    "crop_unirrigated": "Rs 6,800 per hectare",
    "crop_irrigated": "Rs 13,500 per hectare",
    "boat_non_motorised": "Rs 4,100",
    "boat_motorised": "Rs 57,800",
}


def build_recovery_timeline(
    state: str, district: str, risk_label: str
) -> list:
    """
    Build a 7-day phased recovery timeline with real schemes.
    """
    if risk_label == "CRITICAL":
        schemes_multiplier = 3
    elif risk_label == "HIGH":
        schemes_multiplier = 2
    else:
        schemes_multiplier = 1

    timeline = [
        {
            "day_number": 1,
            "day_range": "Immediate (0-12 hours)",
            "phase_name": "Emergency Response",
            "priority_tasks": [
                "Activate field hospitals in {0}".format(district),
                "Restore water supply to emergency shelters",
                "Deploy emergency generators to health centers",
                "Establish temporary morgue with dignity protocols",
                "Activate communication networks with satellite phones",
            ],
            "collector_action": "Issue immediate relief distribution order for {0}, coordinate with {1}".format(district, "NDRF"),
            "schemes_activated": ["Emergency Relief Fund", "State Disaster Relief Fund"],
        },
        {
            "day_number": 2,
            "day_range": "12-36 hours",
            "phase_name": "Stabilization",
            "priority_tasks": [
                "Restore vehicular access on main arterial roads in {0}".format(district),
                "Clear debris from critical infrastructure",
                "Restore mobile phone connectivity",
                "Assess damage to government schools and Anganwadis",
                "Begin initial damage documentation",
            ],
            "collector_action": "Issue travel pass certifications for essential movements in {0}".format(district),
            "schemes_activated": ["Pradhan Mantri Awas Yojana (temporary shelters)", "MGNREGS activation"],
        },
        {
            "day_number": 3,
            "day_range": "36-60 hours",
            "phase_name": "Power Restoration Phase 1",
            "priority_tasks": [
                "Restore power to district hospital and primary health centers",
                "Restore power to water pumping stations",
                "Establish temporary food kitchens with 3 meals daily",
                "Survey residential collapse in {0}".format(district),
                "Launch cash-for-work programs for debris removal",
            ],
            "collector_action": "Activate inter-ministerial coordination for {0} with state capital".format(district),
            "schemes_activated": ["PM Awas Yojana Gramin", "MGNREGS wage payments"],
        },
        {
            "day_number": 4,
            "day_range": "60-84 hours",
            "phase_name": "Education & Livelihood",
            "priority_tasks": [
                "Initiate structure assessment of all schools in {0}".format(district),
                "Resume school operations from temporary locations",
                "Begin registration for crop loss claims",
                "Restore Anganwadi nutritional programs",
                "Assess fishery infrastructure damage in {0}".format(district),
            ],
            "collector_action": "Distribute claim forms for crop losses and livestock compensation in {0}".format(district),
            "schemes_activated": ["Pradhan Mantri Fasal Bima Yojana", "Matsyakara Bharosa (if {0})".format(state)],
        },
        {
            "day_number": 5,
            "day_range": "84-108 hours",
            "phase_name": "Residential Power & Utilities",
            "priority_tasks": [
                "Restore power to residential areas in {0}".format(district),
                "Verify structural integrity of dwellings",
                "Issue reconstruction permits for partially damaged structures",
                "Restore piped water to households",
                "Begin reconstruction supply distribution (cement, rods, timber)",
            ],
            "collector_action": "Approve reconstruction plans and release material assistance for {0}".format(district),
            "schemes_activated": ["PM Awas Yojana reconstruction", "Jal Jeevan Mission restoration"],
        },
        {
            "day_number": 6,
            "day_range": "108-144 hours",
            "phase_name": "Market & Transport",
            "priority_tasks": [
                "Clear debris from bazaars and markets in {0}".format(district),
                "Allow regulated commerce and business reopening",
                "Restore public transport networks",
                "Reopen financial institutions and banks",
                "Verify supply chain for essential commodities",
            ],
            "collector_action": "Issue commerce restoration guidelines for regulated reopening in {0}".format(district),
            "schemes_activated": ["Trade credit facilitation", "SIDBI emergency loans eligibility"],
        },
        {
            "day_number": 7,
            "day_range": "144-168 hours",
            "phase_name": "Assessment & Planning",
            "priority_tasks": [
                "Complete Preliminary Damage & Needs Assessment (PDNA) for {0}".format(district),
                "Finalize rehabilitation project proposals",
                "Initiate long-term recovery planning meetings",
                "Register all beneficiaries for government support",
                "Begin transition to reconstruction phase management",
            ],
            "collector_action": "Submit consolidated PDNA report to state government for {0}; initiate Multi-Departmental Committee".format(district),
            "schemes_activated": ["Reconstruction financing", "Community-based livelihood programs"],
        },
    ]

    return timeline


def build_closing_statement(district: str, state: str, risk_label: str) -> str:
    """
    Build a one-sentence forward-looking closing statement.
    """
    if risk_label == "CRITICAL":
        return f"Recovery in {district}, {state} will be a coordinated multi-year effort; immediate focus is life-saving and preventing secondary disasters."
    elif risk_label == "HIGH":
        return f"Staged recovery tailored to {district} damage severity; government will lead reconstruction with community participation."
    elif risk_label == "MODERATE":
        return f"Targeted recovery support for {district} will prioritize livelihood restoration alongside infrastructure repair."
    else:
        return f"Support programs for {district} will focus on preventing long-term economic disruption and restoring normalcy."


def recovery_agent(
    hazard_report: dict,
    risk_assessment: dict,
    resource_plan: dict,
    evacuation_plan: dict,
    geo: dict,
    openai_client,
) -> dict:
    """
    Post-Disaster Recovery Coordinator Agent.
    Produces 7-day phased recovery plan with real government schemes.
    """
    state = geo.get("state", "")
    district = geo.get("district", "")
    risk_label = risk_assessment.get("risk_label", "MODERATE")

    timeline = build_recovery_timeline(state, district, risk_label)

    closing = build_closing_statement(district, state, risk_label)

    return {
        "days": timeline,
        "ndrf_compensation": NDRF_COMPENSATION,
        "closing_statement": closing,
    }
