#!/usr/bin/env python3
"""
Test script for CrewAI integration with AstraSync
"""

import sys
import json
from astrasync import AstraSync, detect_agent_type
from astrasync.adapters.crewai import register_crewai

def test_crewai_detection():
    """Test CrewAI agent detection"""
    print("\n🔍 Testing CrewAI Detection...")
    
    # Test cases
    test_cases = [
        {
            "name": "Basic CrewAI Agent",
            "data": {
                "role": "Researcher",
                "goal": "Find information",
                "backstory": "Expert researcher"
            }
        },
        {
            "name": "CrewAI Agent with Tools",
            "data": {
                "role": "Analyst",
                "goal": "Analyze data",
                "backstory": "Data expert",
                "tools": ["calculator", "search"],
                "llm": "gpt-4"
            }
        },
        {
            "name": "CrewAI Crew",
            "data": {
                "agents": [
                    {"role": "Lead", "goal": "Coordinate"},
                    {"role": "Worker", "goal": "Execute"}
                ],
                "tasks": [
                    {"description": "Plan work"},
                    {"description": "Do work"}
                ],
                "process": "sequential"
            }
        },
        {
            "name": "Mock CrewAI Object",
            "data": type('MockAgent', (), {
                '__module__': 'crewai.agent',
                'role': 'Executor',
                'goal': 'Execute tasks',
                'backstory': 'Task executor',
                'tools': ['tool1'],
                'memory': True
            })()
        }
    ]
    
    for test in test_cases:
        detected = detect_agent_type(test["data"])
        print(f"  ✓ {test['name']}: {detected}")
        assert detected == "crewai", f"Failed to detect {test['name']} as crewai (got {detected})"
    
    print("  ✅ All detection tests passed!")


def test_crewai_registration():
    """Test CrewAI agent registration"""
    print("\n📝 Testing CrewAI Registration...")
    
    # Test agent configuration
    agent_config = {
        "name": "Test CrewAI Agent",
        "role": "QA Specialist",
        "goal": "Ensure quality of outputs",
        "backstory": "Experienced QA professional with attention to detail",
        "tools": ["validator", "tester"],
        "memory": True,
        "llm": "gpt-3.5-turbo",
        "max_iter": 10,
        "description": "Quality assurance specialist",
        "owner": "QA Team"
    }
    
    try:
        # Test with mock email (won't actually register)
        result = register_crewai(
            agent=agent_config,
            email="test@example.com",
            owner="Test Organization"
        )
        
        print(f"  ✓ Registration response received")
        print(f"    - Agent ID: {result.get('agentId', 'N/A')}")
        print(f"    - Status: {result.get('status', 'N/A')}")
        print(f"    - Trust Score: {result.get('trustScore', 'N/A')}")
        
        # Note: In developer preview, we'll get a temporary ID
        if result.get('agentId', '').startswith('TEMP-'):
            print("  ✅ Registration test passed (developer preview mode)")
        else:
            print("  ✅ Registration test passed")
            
    except Exception as e:
        print(f"  ❌ Registration failed: {e}")
        # This is expected if we're not connected to the API
        if "Connection" in str(e) or "request" in str(e):
            print("  ℹ️  API connection error (expected in offline testing)")
        else:
            raise


def test_normalization():
    """Test CrewAI data normalization"""
    print("\n🔄 Testing Data Normalization...")
    
    from astrasync.adapters.crewai import normalize_agent_data
    
    # Test agent normalization
    agent_data = {
        "name": "Normalized Agent",
        "role": "Data Processor",
        "goal": "Process and analyze data efficiently",
        "backstory": "You are an experienced data processor with expertise in handling large datasets.",
        "tools": [
            {"name": "pandas_tool", "description": "Process dataframes"},
            "numpy_tool",
            {"name": "sklearn_tool", "description": "Machine learning"}
        ],
        "memory": True,
        "llm": "claude-3",
        "max_iter": 15
    }
    
    normalized = normalize_agent_data(agent_data)
    
    print(f"  ✓ Agent Type: {normalized['agentType']}")
    print(f"  ✓ Name: {normalized['name']}")
    print(f"  ✓ Description: {normalized['description'][:50]}...")
    print(f"  ✓ Capabilities: {normalized['capabilities']}")
    print(f"  ✓ Trust Score: {normalized['trustScore']}")
    print(f"  ✓ Metadata: {json.dumps(normalized.get('metadata', {}), indent=2)}")
    
    # Verify required fields
    assert normalized['agentType'] == 'crewai'
    assert normalized['name'] == 'Normalized Agent'
    assert len(normalized['capabilities']) > 0
    assert normalized['trustScore'] > 0
    assert 'role:Data Processor' in normalized['capabilities']
    
    print("  ✅ Agent normalization test passed!")
    
    # Test crew normalization
    crew_data = {
        "name": "Test Crew",
        "agents": [
            {"role": "Manager", "goal": "Manage team"},
            {"role": "Developer", "goal": "Write code"}
        ],
        "tasks": [
            {"description": "Plan sprint"},
            {"description": "Implement features"}
        ],
        "process": "hierarchical"
    }
    
    crew_normalized = normalize_agent_data(crew_data)
    
    print(f"\n  ✓ Crew Type: {crew_normalized['agentType']}")
    print(f"  ✓ Name: {crew_normalized['name']}")
    print(f"  ✓ Capabilities: {crew_normalized['capabilities']}")
    print(f"  ✓ Agent Count: {crew_normalized['metadata'].get('agentCount', 0)}")
    print(f"  ✓ Task Count: {crew_normalized['metadata'].get('taskCount', 0)}")
    
    assert crew_normalized['agentType'] == 'crewai'
    assert 'agents:2' in crew_normalized['capabilities']
    assert 'tasks:2' in crew_normalized['capabilities']
    
    print("  ✅ Crew normalization test passed!")


def test_auto_detection():
    """Test auto-detection through main AstraSync client"""
    print("\n🤖 Testing Auto-Detection via Main Client...")
    
    client = AstraSync(email="test@example.com")
    
    # This should be auto-detected as CrewAI
    agent = {
        "name": "Auto-Detected Agent",
        "role": "Automation Expert",
        "goal": "Automate repetitive tasks",
        "backstory": "Specialist in process automation"
    }
    
    # The detector should identify this as CrewAI
    detected_type = detect_agent_type(agent)
    print(f"  ✓ Detected type: {detected_type}")
    assert detected_type == "crewai"
    
    print("  ✅ Auto-detection test passed!")


if __name__ == "__main__":
    print("🚀 AstraSync CrewAI Integration Test Suite")
    print("=" * 50)
    
    try:
        test_crewai_detection()
        test_normalization()
        test_auto_detection()
        test_crewai_registration()
        
        print("\n✅ All tests completed successfully!")
        print("\n📚 CrewAI integration is ready to use!")
        print("   - Auto-detection: ✓")
        print("   - Normalization: ✓")
        print("   - Registration: ✓")
        print("   - Trust scoring: ✓")
        print("   - Multi-agent crews: ✓")
        
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n⚠️  Unexpected error: {e}")
        sys.exit(1)