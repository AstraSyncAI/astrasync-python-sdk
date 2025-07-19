#!/usr/bin/env python3
"""
Test script for n8n and AgentStack integrations with AstraSync
"""

import sys
import json
import yaml
from astrasync import AstraSync, detect_agent_type
from astrasync.adapters.n8n import register_n8n
from astrasync.adapters.agentstack import register_agentstack

def test_n8n_detection():
    """Test n8n agent detection"""
    print("\n🔍 Testing n8n Detection...")
    
    # Test cases
    test_cases = [
        {
            "name": "n8n AI Agent Node",
            "data": {
                "type": "n8n-nodes-langchain.agent",
                "name": "AI Agent",
                "parameters": {
                    "systemPrompt": "You are helpful",
                    "model": "gpt-4"
                }
            }
        },
        {
            "name": "n8n Workflow",
            "data": {
                "workflow": {
                    "name": "Test Workflow",
                    "nodes": [
                        {
                            "type": "n8n-nodes-langchain.agent",
                            "name": "Agent Node"
                        }
                    ]
                }
            }
        },
        {
            "name": "n8n Nodes List",
            "data": {
                "nodes": [
                    {"type": "webhook", "name": "Start"},
                    {"type": "n8n-nodes-langchain.conversationalAgent", "name": "AI"}
                ]
            }
        }
    ]
    
    for test in test_cases:
        detected = detect_agent_type(test["data"])
        print(f"  ✓ {test['name']}: {detected}")
        assert detected == "n8n", f"Failed to detect {test['name']} as n8n (got {detected})"
    
    print("  ✅ All n8n detection tests passed!")


def test_agentstack_detection():
    """Test AgentStack agent detection"""
    print("\n🔍 Testing AgentStack Detection...")
    
    # Test cases
    test_cases = [
        {
            "name": "AgentStack Single Agent",
            "data": {
                "agent_name": "Test Agent",
                "system_prompt": "You are a test agent",
                "max_loops": 5,
                "autosave": True
            }
        },
        {
            "name": "AgentStack Agents List",
            "data": {
                "agents": [{
                    "agent_name": "Agent1",
                    "system_prompt": "First agent",
                    "max_loops": 3
                }]
            }
        },
        {
            "name": "AgentStack Swarm",
            "data": {
                "swarm_architecture": {
                    "name": "Test Swarm",
                    "swarm_type": "ConcurrentWorkflow"
                }
            }
        }
    ]
    
    for test in test_cases:
        detected = detect_agent_type(test["data"])
        print(f"  ✓ {test['name']}: {detected}")
        assert detected == "agentstack", f"Failed to detect {test['name']} as agentstack (got {detected})"
    
    print("  ✅ All AgentStack detection tests passed!")


def test_n8n_normalization():
    """Test n8n data normalization"""
    print("\n🔄 Testing n8n Normalization...")
    
    from astrasync.adapters.n8n import normalize_agent_data
    
    # Test agent node normalization
    agent_node = {
        "type": "n8n-nodes-langchain.agent",
        "name": "Support Bot",
        "parameters": {
            "systemPrompt": "You are a helpful support assistant that provides accurate information.",
            "model": "gpt-3.5-turbo",
            "tools": ["search", "calculator"],
            "memory": {"type": "windowBuffer", "k": 10},
            "outputParsing": True
        }
    }
    
    normalized = normalize_agent_data(agent_node)
    
    print(f"  ✓ Agent Type: {normalized['agentType']}")
    print(f"  ✓ Name: {normalized['name']}")
    print(f"  ✓ Description: {normalized['description'][:50]}...")
    print(f"  ✓ Capabilities: {normalized['capabilities']}")
    print(f"  ✓ Trust Score: {normalized['trustScore']}")
    
    assert normalized['agentType'] == 'n8n'
    assert normalized['name'] == 'Support Bot'
    assert 'model:gpt-3.5-turbo' in normalized['capabilities']
    assert 'memory:enabled' in normalized['capabilities']
    
    print("  ✅ n8n normalization test passed!")


def test_agentstack_normalization():
    """Test AgentStack data normalization"""
    print("\n🔄 Testing AgentStack Normalization...")
    
    from astrasync.adapters.agentstack import normalize_agent_data
    
    # Test YAML agent normalization
    yaml_agent = """
agents:
  - agent_name: "Research-Agent"
    system_prompt: "You are an expert researcher"
    model: "gpt-4"
    max_loops: 5
    autosave: true
    context_length: 100000
    dynamic_temperature_enabled: true
    tools:
      - "web_search"
      - "document_reader"
"""
    
    normalized = normalize_agent_data(yaml_agent)
    
    print(f"  ✓ Agent Type: {normalized['agentType']}")
    print(f"  ✓ Name: {normalized['name']}")
    print(f"  ✓ Capabilities: {normalized['capabilities']}")
    print(f"  ✓ Trust Score: {normalized['trustScore']}")
    print(f"  ✓ Context Length: {normalized['metadata'].get('contextLength', 'N/A')}")
    
    assert normalized['agentType'] == 'agentstack'
    assert normalized['name'] == 'Research-Agent'
    assert 'model:gpt-4' in normalized['capabilities']
    assert normalized['metadata']['contextLength'] == 100000
    
    print("  ✅ AgentStack normalization test passed!")


def test_registration():
    """Test registration for both frameworks"""
    print("\n📝 Testing Registration...")
    
    # Test n8n registration
    n8n_agent = {
        "type": "n8n-nodes-langchain.agent",
        "name": "Test n8n Agent",
        "parameters": {
            "systemPrompt": "Test agent",
            "model": "gpt-4"
        }
    }
    
    try:
        result = register_n8n(
            agent=n8n_agent,
            email="test@example.com",
            owner="Test Org"
        )
        print(f"  ✓ n8n registration successful: {result.get('agentId', 'N/A')}")
    except Exception as e:
        print(f"  ℹ️  n8n registration error (expected in offline testing): {str(e)[:50]}...")
    
    # Test AgentStack registration
    agentstack_agent = {
        "agent_name": "Test AgentStack Agent",
        "system_prompt": "Test agent",
        "max_loops": 3
    }
    
    try:
        result = register_agentstack(
            agent=agentstack_agent,
            email="test@example.com",
            owner="Test Org"
        )
        print(f"  ✓ AgentStack registration successful: {result.get('agentId', 'N/A')}")
    except Exception as e:
        print(f"  ℹ️  AgentStack registration error (expected in offline testing): {str(e)[:50]}...")


def test_auto_detection():
    """Test auto-detection through main AstraSync client"""
    print("\n🤖 Testing Auto-Detection...")
    
    client = AstraSync(email="test@example.com")
    
    # Test n8n auto-detection
    n8n_config = {
        "type": "n8n-nodes-langchain.agent",
        "parameters": {"systemPrompt": "AI assistant"}
    }
    
    detected = detect_agent_type(n8n_config)
    print(f"  ✓ n8n detected as: {detected}")
    assert detected == "n8n"
    
    # Test AgentStack auto-detection
    agentstack_config = {
        "agent_name": "Auto Agent",
        "max_loops": 5,
        "saved_state_path": "agent.json"
    }
    
    detected = detect_agent_type(agentstack_config)
    print(f"  ✓ AgentStack detected as: {detected}")
    assert detected == "agentstack"
    
    print("  ✅ Auto-detection tests passed!")


if __name__ == "__main__":
    print("🚀 AstraSync n8n & AgentStack Integration Test Suite")
    print("=" * 50)
    
    try:
        test_n8n_detection()
        test_agentstack_detection()
        test_n8n_normalization()
        test_agentstack_normalization()
        test_auto_detection()
        test_registration()
        
        print("\n✅ All tests completed successfully!")
        print("\n📚 Both integrations are ready to use!")
        print("   - n8n: ✓ (workflows, AI agent nodes)")
        print("   - AgentStack: ✓ (agents, swarms, YAML configs)")
        
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n⚠️  Unexpected error: {e}")
        sys.exit(1)