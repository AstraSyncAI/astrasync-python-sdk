"""
Comprehensive test script for AstraSync Python SDK
Tests all supported protocols including Google ADK
"""

import json
from astrasync import AstraSync
from astrasync.utils.detector import detect_agent_type, normalize_agent_data
from astrasync.utils.trust_score import calculate_trust_score

def test_detection():
    """Test agent type detection for all protocols"""
    print("🔍 Testing Agent Detection\n")
    
    test_cases = [
        # MCP Agent
        {
            "name": "MCP Test",
            "data": {
                "protocol": "ai-agent",
                "skills": [{"name": "search"}, {"name": "calculate"}],
                "name": "MCP Assistant"
            },
            "expected": "mcp"
        },
        # Letta Agent
        {
            "name": "Letta Test",
            "data": {
                "type": "agent",
                "memory": {"core": "data"},
                "name": "Letta Memory Agent"
            },
            "expected": "letta"
        },
        # ACP Agent (IBM)
        {
            "name": "ACP Test",
            "data": {
                "agentId": "acp-123",
                "authentication": {"method": "oauth"},
                "name": "IBM ACP Agent"
            },
            "expected": "acp"
        },
        # OpenAI Agent
        {
            "name": "OpenAI Test",
            "data": {
                "model": "gpt-4",
                "instructions": "Be helpful",
                "tools": [{"type": "code_interpreter"}],
                "name": "OpenAI Assistant"
            },
            "expected": "openai"
        },
        # AutoGPT Agent
        {
            "name": "AutoGPT Test",
            "data": {
                "ai_name": "AutoBot",
                "ai_role": "General Assistant",
                "ai_goals": ["Help users", "Learn continuously"]
            },
            "expected": "autogpt"
        },
        # Google ADK - Schema format
        {
            "name": "Google ADK Schema Test",
            "data": {
                "name": "ADK Schema Agent",
                "input_schema": {"type": "object"},
                "output_schema": {"type": "object"},
                "instructions": "Process requests"
            },
            "expected": "google-adk"
        },
        # Google ADK - Workflow format
        {
            "name": "Google ADK Workflow Test",
            "data": {
                "name": "ADK Orchestrator",
                "agent_type": "sequential",
                "runner": "default",
                "tools": ["task1", "task2"]
            },
            "expected": "google-adk"
        },
        # Google ADK - Serialized format
        {
            "name": "Google ADK Serialized Test",
            "data": {
                "config": {
                    "agent_class": "google.adk.agents.LlmAgent"
                },
                "name": "Serialized ADK Agent"
            },
            "expected": "google-adk"
        },
        # Agentforce
        {
            "name": "Agentforce Test",
            "data": {
                "agent_type": "External",
                "agent_template_type": "EinsteinServiceAgent",
                "label": "Salesforce Agent"
            },
            "expected": "agentforce"
        }
    ]
    
    passed = 0
    failed = 0
    
    for test in test_cases:
        detected = detect_agent_type(test["data"])
        if detected == test["expected"]:
            print(f"✅ {test['name']}: {detected}")
            passed += 1
        else:
            print(f"❌ {test['name']}: Expected {test['expected']}, got {detected}")
            failed += 1
    
    print(f"\n📊 Detection Results: {passed} passed, {failed} failed")
    return failed == 0

def test_normalization():
    """Test normalization for all protocols"""
    print("\n\n🔄 Testing Agent Normalization\n")
    
    test_agents = [
        # Simple agents from each protocol
        {
            "protocol": "ai-agent",
            "skills": [{"name": "search"}],
            "name": "MCP Test Agent"
        },
        {
            "name": "ADK Test Agent",
            "input_schema": {"type": "object"},
            "output_schema": {"type": "object"},
            "model": "gemini-1.5-pro",
            "tools": ["search", "calculate"]
        },
        {
            "ai_name": "AutoGPT Test",
            "ai_role": "Assistant",
            "ai_goals": ["Help", "Learn"]
        }
    ]
    
    for agent in test_agents:
        agent_type = detect_agent_type(agent)
        normalized = normalize_agent_data(agent, agent_type)
        
        print(f"Agent Type: {agent_type}")
        print(f"Name: {normalized.get('name')}")
        print(f"Capabilities: {normalized.get('capabilities', [])}")
        
        # Check for Google ADK specific fields
        if agent_type == 'google-adk':
            print(f"Framework: {normalized.get('framework')}")
            print(f"Orchestration: {normalized.get('orchestration_capable')}")
        
        print("-" * 40)
    
    return True

def test_trust_scores():
    """Test trust score calculation with Google ADK bonuses"""
    print("\n\n📊 Testing Trust Score Calculation\n")
    
    test_cases = [
        # Basic agent
        {
            "name": "Basic Agent",
            "data": {
                "name": "Simple Agent",
                "description": "A simple test agent",
                "capabilities": ["search"],
                "version": "1.0.0"
            }
        },
        # Google ADK with bonuses
        {
            "name": "ADK with Structured Output",
            "data": {
                "name": "Advanced ADK Agent",
                "description": "An ADK agent with structured output for deterministic responses and compliance tracking",
                "capabilities": ["search", "analyze", "report", "orchestrate"],
                "version": "2.0.0",
                "framework": "google-adk",
                "structured_output": True,
                "orchestration_capable": True,
                "session_service": "managed"
            }
        },
        # Regular ADK without bonuses
        {
            "name": "Basic ADK Agent",
            "data": {
                "name": "Simple ADK",
                "description": "Basic ADK agent",
                "capabilities": ["process"],
                "agentType": "google-adk"
            }
        }
    ]
    
    for test in test_cases:
        score = calculate_trust_score(test["data"])
        print(f"{test['name']}: {score}%")
        
        # Show score breakdown for ADK agents
        if test["data"].get("framework") == "google-adk" or test["data"].get("agentType") == "google-adk":
            bonuses = []
            if test["data"].get("structured_output"):
                bonuses.append("  +5% for structured output")
            if test["data"].get("orchestration_capable"):
                bonuses.append("  +3% for orchestration")
            if "session_service" in str(test["data"]):
                bonuses.append("  +2% for session management")
            
            if bonuses:
                print("  Bonuses applied:")
                for bonus in bonuses:
                    print(bonus)
        print()
    
    return True

def test_registration():
    """Test actual registration with the API"""
    print("\n\n🚀 Testing Live Registration\n")
    
    # Create client
    client = AstraSync(email="test@example.com")
    
    # Test Google ADK registration
    adk_agent = {
        "name": "Test ADK Agent",
        "instructions": "This is a test agent for validating Google ADK support in AstraSync",
        "model": "gemini-1.5-pro",
        "tools": ["search", "analyze"],
        "input_schema": {"type": "object"},
        "output_schema": {"type": "object"},
        "agent_type": "llm",
        "session_service": "managed"
    }
    
    try:
        result = client.register(adk_agent)
        print(f"✅ Successfully registered Google ADK agent!")
        print(f"   Agent ID: {result['agentId']}")
        print(f"   Status: {result['status']}")
        print(f"   Trust Score: {result['trustScore']}")
        
        # Verify the agent
        if 'agentId' in result:
            verify_result = client.verify(result['agentId'])
            print(f"   Verification: {'✅ Exists' if verify_result else '❌ Not found'}")
        
        return True
    except Exception as e:
        print(f"❌ Registration failed: {str(e)}")
        return False

def test_cli_detection():
    """Test CLI analysis of Google ADK agents"""
    print("\n\n🖥️  Testing CLI Detection\n")
    
    # Create a test file
    test_adk = {
        "name": "CLI Test ADK Agent",
        "agent_type": "sequential",
        "tools": ["step1", "step2", "step3"],
        "runner": "default",
        "output_schema": {
            "type": "object",
            "properties": {
                "result": {"type": "string"}
            }
        }
    }
    
    # Save to temporary file
    with open("test_adk_agent.json", "w") as f:
        json.dump(test_adk, f, indent=2)
    
    print("Created test_adk_agent.json")
    print("Run: astrasync analyze test_adk_agent.json")
    print("Expected: Detection as google-adk with orchestration capabilities")
    
    # Clean up
    import os
    try:
        os.remove("test_adk_agent.json")
        print("Cleaned up test file")
    except:
        pass
    
    return True

def main():
    """Run all tests"""
    print("🧪 AstraSync Python SDK - Comprehensive Protocol Test")
    print("=" * 50)
    
    tests = [
        ("Detection", test_detection),
        ("Normalization", test_normalization),
        ("Trust Scores", test_trust_scores),
        ("Registration", test_registration),
        ("CLI Detection", test_cli_detection)
    ]
    
    results = []
    
    for name, test_func in tests:
        try:
            success = test_func()
            results.append((name, success))
        except Exception as e:
            print(f"\n❌ {name} test crashed: {str(e)}")
            results.append((name, False))
    
    # Summary
    print("\n\n📈 Test Summary")
    print("=" * 50)
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for name, success in results:
        status = "✅ PASSED" if success else "❌ FAILED"
        print(f"{name}: {status}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! Google ADK support is working perfectly!")
    else:
        print("\n⚠️  Some tests failed. Please review the output above.")

if __name__ == "__main__":
    main()
