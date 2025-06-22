"""
Comprehensive test suite for AstraSync Python SDK v0.2.1
Tests all supported agent protocols with API trust scores
"""
from astrasync import AstraSync, detect_agent_type, normalize_agent_data
import json
import time

print("🧪 AstraSync v0.2.1 - Comprehensive Protocol Test")
print("=" * 50)

# Test agents for all supported protocols
test_agents = {
    "MCP": {
        "protocol": "ai-agent",
        "skills": [{"name": "search"}, {"name": "calculate"}],
        "name": "MCP Assistant",
        "description": "MCP protocol agent"
    },
    "Letta": {
        "type": "agent",
        "memory": {"core": "data", "recall": "events"},
        "name": "Letta Memory Agent",
        "description": "Memory-enabled agent"
    },
    "ACP": {
        "agentId": "acp-123",
        "authentication": {"method": "oauth", "scope": "full"},
        "name": "IBM ACP Agent",
        "capabilities": {"search": True, "analyze": True}
    },
    "OpenAI": {
        "model": "gpt-4",
        "instructions": "You are a helpful assistant",
        "tools": [{"type": "code_interpreter"}, {"type": "retrieval"}],
        "name": "OpenAI Assistant"
    },
    "AutoGPT": {
        "ai_name": "AutoBot",
        "ai_role": "General Assistant", 
        "ai_goals": ["Help users", "Learn continuously", "Be efficient"]
    },
    "Google ADK (Schema)": {
        "name": "ADK Schema Agent",
        "input_schema": {"type": "object", "properties": {"query": {"type": "string"}}},
        "output_schema": {"type": "object", "properties": {"response": {"type": "string"}}},
        "tools": ["search", "analyze", "report"],
        "model": "gemini-1.5-pro"
    },
    "Google ADK (Workflow)": {
        "name": "ADK Orchestrator",
        "agent_type": "sequential",
        "runner": "default",
        "session_service": "managed",
        "tools": ["delegate_task1", "delegate_task2", "synthesize"]
    },
    "Agentforce": {
        "agent_type": "External",
        "agent_template_type": "EinsteinServiceAgent",
        "label": "Salesforce Service Agent",
        "topics": [{"label": "Support"}, {"label": "Sales"}]
    }
}

# Test 1: Detection
print("\n📊 Test 1: Agent Detection")
print("-" * 40)
detection_results = []
for expected_type, agent_data in test_agents.items():
    detected = detect_agent_type(agent_data)
    
    # Map expected to actual
    expected_map = {
        "MCP": "mcp",
        "Letta": "letta",
        "ACP": "acp",
        "OpenAI": "openai",
        "AutoGPT": "autogpt",
        "Google ADK (Schema)": "google-adk",
        "Google ADK (Workflow)": "google-adk",
        "Agentforce": "agentforce"
    }
    
    expected = expected_map.get(expected_type, expected_type.lower())
    passed = detected == expected
    
    status = "✅ PASS" if passed else "❌ FAIL"
    print(f"{expected_type:20} -> {detected:15} {status}")
    detection_results.append(passed)

# Test 2: Normalization (v0.2.1 - single argument)
print("\n🔄 Test 2: Agent Normalization")
print("-" * 40)
normalization_results = []
for name, agent_data in test_agents.items():
    try:
        # v0.2.1: normalize_agent_data takes only one argument
        normalized = normalize_agent_data(agent_data)
        
        # Check for required fields
        required = all([
            'name' in normalized,
            'agentType' in normalized,
            'capabilities' in normalized,
            'owner' in normalized and normalized['owner'] != ''
        ])
        
        status = "✅ PASS" if required else "❌ FAIL"
        print(f"{name:20} {status} (owner: {normalized.get('owner', 'MISSING')})")
        normalization_results.append(required)
    except Exception as e:
        print(f"{name:20} ❌ Error: {str(e)}")
        normalization_results.append(False)

# Test 3: API Trust Scores (v0.2.1 - from API only)
print("\n📈 Test 3: API Trust Scores")
print("-" * 40)
client = AstraSync(email="test@example.com")
trust_results = []

for name, agent_data in test_agents.items():
    try:
        # Register and get API trust score
        result = client.register(agent_data)
        trust_score = result.get('trustScore', 'ERROR')
        
        # v0.2.1: All trust scores should be TEMP-95% from API
        passed = trust_score == 'TEMP-95%'
        status = "✅ PASS" if passed else "❌ FAIL"
        
        print(f"{name:20} Score: {trust_score} {status}")
        trust_results.append(passed)
        
        # Rate limit protection
        time.sleep(0.5)
    except Exception as e:
        print(f"{name:20} ❌ Error: {str(e)}")
        trust_results.append(False)

# Test 4: Verify Registration
print("\n🔍 Test 4: Registration Verification")
print("-" * 40)
try:
    # Register a test agent
    test_agent = {
        "name": "Verification Test Agent",
        "description": "Testing verification endpoint",
        "input_schema": {"type": "object"},
        "output_schema": {"type": "object"}
    }
    
    result = client.register(test_agent)
    agent_id = result['agentId']
    
    # Verify it exists
    verification = client.verify(agent_id)
    
    print(f"Agent ID: {agent_id}")
    print(f"Exists: {verification.get('exists', False)}")
    print(f"Status: {'✅ PASS' if verification.get('exists') else '❌ FAIL'}")
    verify_passed = verification.get('exists', False)
except Exception as e:
    print(f"❌ Verification failed: {str(e)}")
    verify_passed = False

# Summary
print("\n" + "=" * 50)
print("📊 TEST SUMMARY")
print("=" * 50)

tests = {
    "Detection": (sum(detection_results), len(detection_results)),
    "Normalization": (sum(normalization_results), len(normalization_results)),
    "API Trust Scores": (sum(trust_results), len(trust_results)),
    "Verification": (1 if verify_passed else 0, 1)
}

all_passed = True
for test_name, (passed, total) in tests.items():
    status = "✅" if passed == total else "❌"
    print(f"{test_name:15} {status} {passed}/{total} passed")
    if passed != total:
        all_passed = False

print("\n" + ("✅ ALL TESTS PASSED!" if all_passed else "⚠️ Some tests failed"))
print(f"\nSDK Version: {__import__('astrasync').__version__}")
