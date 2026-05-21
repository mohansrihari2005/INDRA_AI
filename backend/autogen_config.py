# AutoGen Configuration for INDRA AI v2
# This file documents AutoGen integration and configuration options

"""
AutoGen Framework Integration
==============================

INDRA AI v2 now supports Microsoft AutoGen framework for multi-agent orchestration.
This enables sophisticated agent communication and collaborative problem-solving.

ARCHITECTURE CHANGES
====================

1. AGENT DEFINITIONS
   - Each domain specialist now has a factory function: get_<agent>_agent(llm_config)
   - Agents use ConversableAgent from autogen library
   - System prompts define expert roles and responsibilities
   - Agents can be configured with tools via function_map

2. COORDINATOR MODES
   - LEGACY MODE (default): Sequential agent execution
     + Direct data passing between agents
     + Maintains existing output format
     + Best for production (faster, more predictable)
   
   - AUTOGEN MODE: GroupChat orchestration
     + Enables agent-to-agent communication
     + More sophisticated reasoning
     + Better for complex scenarios

3. USAGE

   LEGACY MODE (existing behavior):
   ---
   POST /api/generate/stream
   {
     "place": "Visakhapatnam, AP",
     "use_autogen": false
   }
   
   AUTOGEN MODE:
   ---
   POST /api/generate/stream
   {
     "place": "Visakhapatnam, AP",
     "use_autogen": true
   }

AGENT TEAM
==========

1. HazardOfficer (Hazard Assessment)
   - Role: Analyzes meteorological data
   - Inputs: IMD data, OpenWeather data, location
   - Outputs: Warning color, hazard bulletin
   - System Prompt: IMD-style hazard assessment specialist

2. RiskAssessor (Risk Analysis)
   - Role: Calculates disaster risk levels
   - Inputs: Hazard assessment, geography
   - Outputs: INDRA risk score, risk label
   - System Prompt: Risk calculation specialist

3. ResourcePlanner (Logistics)
   - Role: Plans resource deployment
   - Inputs: Risk assessment, location
   - Outputs: NDRF deployment, resource quantities
   - System Prompt: Disaster logistics expert

4. EvacuationCoordinator (Communications)
   - Role: Generates multilingual alerts
   - Inputs: Hazard, risk, resources, location
   - Outputs: SMS, advisories, role checklists
   - System Prompt: Mass communication officer

5. RecoveryCoordinator (Post-Disaster)
   - Role: Plans recovery phases
   - Inputs: All previous assessments
   - Outputs: 7-day timeline, schemes, compensation
   - System Prompt: Recovery planning specialist

CONFIGURATION OPTIONS
=====================

llm_config = {
    "config_list": [{"model": "gpt-4-turbo", "api_key": os.getenv("OPENAI_API_KEY")}],
    "temperature": 0.3,           # Low for consistency
    "max_tokens": 500,            # Per-agent limit
}

GroupChat Settings:
- max_round: 100 (iterations before termination)
- admin_name: "Coordinator" (human proxy agent)
- speaker_selection_method: "auto" (default)

BACKWARD COMPATIBILITY
======================

✓ Legacy agent functions still work: hazard_agent(), risk_agent(), etc.
✓ All output formats remain unchanged
✓ Frontend code needs no modification
✓ Existing API clients work unmodified
✓ AutoGen is optional; legacy mode is default

PERFORMANCE NOTES
=================

Legacy Mode:
- Average time: ~3-5 seconds per location
- Token usage: ~2000 tokens per request
- Best for: Production, real-time requirements

AutoGen Mode:
- Average time: ~8-15 seconds per location
- Token usage: ~3000-4000 tokens (more interaction)
- Best for: Complex scenarios, agent collaboration

MONITORING & DEBUGGING
======================

Events streamed to frontend:
- "agent_start": Agent begins processing
- "agent_complete": Agent finished, output attached
- "brief_complete": Full analysis ready
- "error": Any failure point
- "warning": AutoGen fallback or degradation

Check logs for AutoGen conversation history when use_autogen=true.

FUTURE ENHANCEMENTS
===================

1. Tool-based agents with function calling
2. Persistent agent state across requests
3. Custom termination strategies
4. Multi-turn refinement of assessments
5. Cross-agent dependencies and triggers

TROUBLESHOOTING
===============

Q: AutoGen mode returns warning about fallback?
A: Check OPENAI_API_KEY is set and AutoGen is installed (pip install pyautogen>=0.2.0)

Q: Getting different results between legacy and AutoGen?
A: Both should produce identical outputs. Differences indicate LLM variance or version changes.

Q: Can I use a different LLM model?
A: Yes - modify llm_config in coordinator_autogen.py to use other models (gpt-4, claude, etc.)

Q: How do I add a new agent?
A: 
1. Create agent-specific functions and tools
2. Add get_<agent>_agent(llm_config) factory function
3. Add to agents list in GroupChat
4. Update coordinator to call new agent

"""

# Python configuration version
AUTOGEN_CONFIG = {
    "legacy_mode": True,  # Set to False to prefer AutoGen
    "llm_model": "gpt-4-turbo",
    "temperature": 0.3,
    "max_tokens": 500,
    "group_chat_max_rounds": 100,
    "timeout": 60,  # seconds
}

# Feature flags
FEATURES = {
    "use_autogen": False,  # Default: use legacy mode
    "enable_agent_logging": True,
    "stream_agent_messages": False,  # Stream full agent chat to frontend
    "enable_tool_calls": False,  # Enable AutoGen tool use
}
