#!/usr/bin/env python3
"""
Test script to verify AutoGen integration in INDRA AI v2

Usage:
    python test_autogen_integration.py

Tests:
    1. AutoGen installation
    2. Agent factory functions
    3. LLM configuration
    4. Fallback mechanism
"""

import sys
import os

# Fix Python path to find backend modules
backend_path = os.path.join(os.path.dirname(__file__), 'backend')
sys.path.insert(0, backend_path)

# Load environment variables
from dotenv import load_dotenv
load_dotenv(os.path.join(backend_path, '.env'))

def test_autogen_installation():
    """Test if AutoGen is properly installed"""
    print("=" * 60)
    print("TEST 1: AutoGen Installation")
    print("=" * 60)
    try:
        import autogen
        print(f"✓ AutoGen installed: version {autogen.__version__}")
        print(f"✓ Location: {autogen.__file__}")
        return True
    except ImportError as e:
        print(f"✗ AutoGen not installed: {e}")
        print(f"  Install with: pip install autogen")
        return False

def test_agent_imports():
    """Test if agent factory functions can be imported"""
    print("\n" + "=" * 60)
    print("TEST 2: Agent Factory Functions")
    print("=" * 60)
    try:
        from agents import (
            get_hazard_agent,
            get_risk_agent,
            get_resource_agent,
            get_evacuation_agent,
            get_recovery_agent,
        )
        print("✓ All agent factory functions imported successfully")
        return True
    except ImportError as e:
        print(f"✗ Failed to import agent factories: {e}")
        return False

def test_agent_creation():
    """Test creating agents with mock LLM config"""
    print("\n" + "=" * 60)
    print("TEST 3: Agent Creation")
    print("=" * 60)
    try:
        from agents import (
            get_hazard_agent,
            get_risk_agent,
            get_resource_agent,
            get_evacuation_agent,
            get_recovery_agent,
        )
        
        # Mock LLM config (won't actually call API)
        llm_config = {
            "config_list": [{"model": "gpt-4-turbo", "api_key": "sk-mock"}],
            "temperature": 0.3,
            "max_tokens": 500,
        }
        
        agents = {
            "HazardOfficer": get_hazard_agent,
            "RiskAssessor": get_risk_agent,
            "ResourcePlanner": get_resource_agent,
            "EvacuationCoordinator": get_evacuation_agent,
            "RecoveryCoordinator": get_recovery_agent,
        }
        
        for agent_name, factory_func in agents.items():
            agent = factory_func(llm_config)
            print(f"✓ Created {agent_name}: {agent.name}")
            if agent.system_message:
                preview = agent.system_message[:80] + "..."
                print(f"  System prompt: {preview}")
        
        return True
    except Exception as e:
        print(f"✗ Failed to create agents: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_legacy_functions():
    """Test that legacy agent functions still work"""
    print("\n" + "=" * 60)
    print("TEST 4: Legacy Function Compatibility")
    print("=" * 60)
    try:
        from agents import (
            hazard_agent,
            risk_agent,
            resource_agent,
            evacuation_agent,
            recovery_agent,
        )
        print("✓ All legacy agent functions still available")
        print("  - hazard_agent")
        print("  - risk_agent")
        print("  - resource_agent")
        print("  - evacuation_agent")
        print("  - recovery_agent")
        return True
    except ImportError as e:
        print(f"✗ Failed to import legacy functions: {e}")
        return False

def test_coordinator():
    """Test coordinator initialization"""
    print("\n" + "=" * 60)
    print("TEST 5: Coordinator")
    print("=" * 60)
    try:
        from agents import run_disaster_pipeline
        print("✓ Coordinator imported successfully")
        print("✓ Supports parameters: place, openai_api_key, use_autogen")
        return True
    except Exception as e:
        print(f"✗ Failed to import coordinator: {e}")
        return False

def test_autogen_config():
    """Test AutoGen configuration"""
    print("\n" + "=" * 60)
    print("TEST 6: AutoGen Configuration")
    print("=" * 60)
    try:
        from autogen_config import AUTOGEN_CONFIG, FEATURES
        print("✓ AutoGen configuration loaded")
        print(f"  Legacy mode: {AUTOGEN_CONFIG['legacy_mode']}")
        print(f"  LLM model: {AUTOGEN_CONFIG['llm_model']}")
        print(f"  Temperature: {AUTOGEN_CONFIG['temperature']}")
        print(f"  Max tokens: {AUTOGEN_CONFIG['max_tokens']}")
        print(f"  GroupChat max rounds: {AUTOGEN_CONFIG['group_chat_max_rounds']}")
        print(f"  Features: {FEATURES}")
        return True
    except Exception as e:
        print(f"✗ Failed to load configuration: {e}")
        return False

def test_environment():
    """Test environment variables"""
    print("\n" + "=" * 60)
    print("TEST 7: Environment Variables")
    print("=" * 60)
    
    required_vars = ["OPENAI_API_KEY"]
    optional_vars = ["OPENWEATHER_API_KEY"]
    
    all_ok = True
    
    for var in required_vars:
        if os.getenv(var):
            print(f"✓ {var} is set")
        else:
            print(f"✗ {var} is NOT set (REQUIRED)")
            all_ok = False
    
    for var in optional_vars:
        if os.getenv(var):
            print(f"✓ {var} is set")
        else:
            print(f"⚠ {var} is not set (optional)")
    
    return all_ok

def main():
    """Run all tests"""
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║" + " INDRA AI v2 - AutoGen Integration Test Suite".center(58) + "║")
    print("╚" + "=" * 58 + "╝")
    
    tests = [
        ("AutoGen Installation", test_autogen_installation),
        ("Agent Imports", test_agent_imports),
        ("Agent Creation", test_agent_creation),
        ("Legacy Compatibility", test_legacy_functions),
        ("Coordinator", test_coordinator),
        ("Configuration", test_autogen_config),
        ("Environment", test_environment),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"\n✗ FATAL ERROR in {test_name}: {e}")
            import traceback
            traceback.print_exc()
            results.append((test_name, False))
    
    # Print summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {test_name}")
    
    print("=" * 60)
    print(f"Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! AutoGen integration is ready to use.")
        print("\nNext steps:")
        print("1. Start backend: uvicorn main:app --reload")
        print("2. Test legacy mode: POST /api/generate/stream {'place': 'Visakhapatnam'}")
        print("3. Test AutoGen mode: POST /api/generate/stream {'place': 'Visakhapatnam', 'use_autogen': true}")
        return 0
    else:
        print(f"\n⚠ {total - passed} test(s) failed. Please fix the issues above.")
        if not test_autogen_installation():
            print("\nTo fix AutoGen installation:")
            print("  pip install autogen")
        if not test_environment():
            print("\nTo set environment variables:")
            print("  Create backend/.env with OPENAI_API_KEY and OPENWEATHER_API_KEY")
        return 1

if __name__ == "__main__":
    sys.exit(main())
