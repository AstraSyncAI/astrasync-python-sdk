#!/usr/bin/env python3
"""
Test script for AutoGen adapter integration
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from astrasync.adapters.autogen import normalize_agent_data, register_autogen

def test_autogen_object():
    """Test AutoGen agent object normalization"""
    print("\n=== Testing AutoGen Agent Object ===")
    
    # Mock AutoGen AssistantAgent
    class MockAssistantAgent:
        def __init__(self):
            self.name = "Research Assistant"
            self.system_message = "You are a helpful research assistant"
            self.llm_config = {
                "model": "gpt-4",
                "temperature": 0.7
            }
            self.code_execution_config = {"work_dir": "coding"}
            
        def __class__(self):
            return type(self)
            
    MockAssistantAgent.__module__ = "autogen"
    MockAssistantAgent.__name__ = "AssistantAgent"
    
    agent = MockAssistantAgent()
    agent.__class__ = MockAssistantAgent
    
    normalized = normalize_agent_data(agent)
    
    print(f"Name: {normalized['name']}")
    print(f"Type: {normalized['agentType']}")
    print(f"Description: {normalized['description']}")
    print(f"Capabilities: {normalized['capabilities']}")
    print(f"Trust Score: {normalized['trustScore']}")
    print(f"Metadata: {normalized['metadata']}")
    
    assert normalized['agentType'] == 'autogen'
    assert normalized['name'] == 'Research Assistant'
    assert 'code_execution:enabled' in normalized['capabilities']
    assert normalized['metadata']['model'] == 'gpt-4'
    assert normalized['trustScore'] > 50

def test_autogen_dict():
    """Test AutoGen configuration dict normalization"""
    print("\n=== Testing AutoGen Configuration Dict ===")
    
    agent_config = {
        "name": "Code Reviewer",
        "description": "AI agent for code review",
        "agent_type": "AssistantAgent",
        "system_message": "Review code for quality and security",
        "llm_config": {
            "model": "gpt-4",
            "temperature": 0.3,
            "functions": ["analyze_code", "suggest_improvements"]
        },
        "code_execution": True,
        "human_input_mode": "NEVER"
    }
    
    normalized = normalize_agent_data(agent_config)
    
    print(f"Name: {normalized['name']}")
    print(f"Type: {normalized['agentType']}")
    print(f"Description: {normalized['description']}")
    print(f"Capabilities: {normalized['capabilities']}")
    print(f"Trust Score: {normalized['trustScore']}")
    print(f"Metadata: {normalized['metadata']}")
    
    assert normalized['agentType'] == 'autogen'
    assert normalized['name'] == 'Code Reviewer'
    assert 'code_execution:enabled' in normalized['capabilities']
    assert 'functions:2' in normalized['capabilities']
    assert normalized['metadata']['humanInputMode'] == 'NEVER'

def test_groupchat_config():
    """Test AutoGen GroupChat configuration"""
    print("\n=== Testing AutoGen GroupChat Configuration ===")
    
    groupchat_config = {
        "name": "Development Team",
        "agents": [
            {"name": "Coder", "agent_type": "AssistantAgent"},
            {"name": "Reviewer", "agent_type": "AssistantAgent"},
            {"name": "Tester", "agent_type": "UserProxyAgent"}
        ],
        "max_round": 10,
        "speaker_selection_method": "round_robin"
    }
    
    normalized = normalize_agent_data(groupchat_config)
    
    print(f"Name: {normalized['name']}")
    print(f"Type: {normalized['agentType']}")
    print(f"Capabilities: {normalized['capabilities']}")
    print(f"Agent Count: {normalized['metadata'].get('agentCount', 0)}")
    print(f"Max Rounds: {normalized['metadata'].get('maxRounds', 0)}")
    
    assert normalized['agentType'] == 'autogen'
    assert 'agents:3' in normalized['capabilities']
    assert 'groupchat:enabled' in normalized['capabilities']
    assert normalized['metadata']['agentCount'] == 3
    assert normalized['metadata']['maxRounds'] == 10

def test_conversable_agent():
    """Test AutoGen ConversableAgent"""
    print("\n=== Testing AutoGen ConversableAgent ===")
    
    agent_config = {
        "name": "Conversable Assistant",
        "conversable": True,
        "function_map": {
            "search": "search_function",
            "calculate": "calc_function"
        },
        "system_message": "You are a conversational assistant",
        "llm_config": {
            "model": "gpt-3.5-turbo"
        }
    }
    
    normalized = normalize_agent_data(agent_config)
    
    print(f"Name: {normalized['name']}")
    print(f"Capabilities: {normalized['capabilities']}")
    print(f"Function Count: {normalized['metadata'].get('functionCount', 0)}")
    
    assert 'functions:2' in normalized['capabilities']
    assert 'conversable:enabled' in normalized['capabilities']

def test_trust_score_calculation():
    """Test trust score calculation for various configurations"""
    print("\n=== Testing Trust Score Calculation ===")
    
    # High trust agent (many features)
    high_trust = {
        "name": "Advanced Agent",
        "description": "Multi-functional AutoGen agent",
        "code_execution": True,
        "human_input_mode": "TERMINATE",
        "llm_config": {
            "model": "gpt-4",
            "functions": ["func1", "func2", "func3", "func4", "func5"]
        },
        "agents": [
            {"name": "Agent1"},
            {"name": "Agent2"},
            {"name": "Agent3"}
        ]
    }
    
    normalized = normalize_agent_data(high_trust)
    print(f"High trust agent score: {normalized['trustScore']}")
    assert normalized['trustScore'] > 70
    
    # Low trust agent (minimal features)
    low_trust = {
        "name": "Simple Agent"
    }
    
    normalized = normalize_agent_data(low_trust)
    print(f"Low trust agent score: {normalized['trustScore']}")
    assert normalized['trustScore'] <= 85  # Base trust score is 85

def main():
    """Run all tests"""
    print("Starting AutoGen adapter tests...")
    
    try:
        test_autogen_object()
        test_autogen_dict()
        test_groupchat_config()
        test_conversable_agent()
        test_trust_score_calculation()
        
        print("\n✅ All AutoGen adapter tests passed!")
        
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()