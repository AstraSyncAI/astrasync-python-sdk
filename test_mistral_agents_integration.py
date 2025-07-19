#!/usr/bin/env python3
"""
Test script for Mistral Agents adapter integration
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from astrasync.adapters.mistral_agents import normalize_agent_data, register_mistral_agents

def test_mistral_object():
    """Test Mistral agent object normalization"""
    print("\n=== Testing Mistral Agent Object ===")
    
    # Mock Mistral Agent
    class MockMistralAgent:
        def __init__(self):
            self.name = "Customer Service Bot"
            self.description = "Helpful customer service assistant"
            self.system_prompt = "You are a helpful customer service agent. Be polite and professional."
            self.model = "mistral-large"
            self.functions = [
                {"name": "check_order", "description": "Check order status"},
                {"name": "process_return", "description": "Process return request"},
                {"name": "escalate_issue", "description": "Escalate to human agent"}
            ]
            self.json_mode = True
            self.safe_mode = True
            
        def __class__(self):
            return type(self)
            
    MockMistralAgent.__module__ = "mistral"
    MockMistralAgent.__name__ = "MistralAgent"
    
    agent = MockMistralAgent()
    agent.__class__ = MockMistralAgent
    
    normalized = normalize_agent_data(agent)
    
    print(f"Name: {normalized['name']}")
    print(f"Type: {normalized['agentType']}")
    print(f"Description: {normalized['description']}")
    print(f"Capabilities: {normalized['capabilities']}")
    print(f"Trust Score: {normalized['trustScore']}")
    print(f"Metadata: {normalized['metadata']}")
    
    assert normalized['agentType'] == 'mistral_agents'
    assert normalized['name'] == 'Customer Service Bot'
    assert 'function_calling:enabled' in normalized['capabilities']
    assert 'json_mode:enabled' in normalized['capabilities']
    assert 'safe_mode:enabled' in normalized['capabilities']
    assert 'functions:3' in normalized['capabilities']
    assert normalized['trustScore'] > 70

def test_mistral_dict():
    """Test Mistral configuration dict normalization"""
    print("\n=== Testing Mistral Configuration Dict ===")
    
    agent_config = {
        "name": "Code Assistant",
        "system_prompt": "You are an expert programmer. Help users write clean, efficient code.",
        "model": "mistral-medium",
        "functions": [
            "analyze_code",
            "suggest_improvements",
            "fix_bugs",
            "write_tests"
        ],
        "json_mode": True,
        "temperature": 0.3,
        "max_tokens": 2000,
        "stream": True,
        "safety_settings": {
            "enabled": True,
            "level": "strict"
        }
    }
    
    normalized = normalize_agent_data(agent_config)
    
    print(f"Name: {normalized['name']}")
    print(f"Type: {normalized['agentType']}")
    print(f"Description: {normalized['description']}")
    print(f"Capabilities: {normalized['capabilities']}")
    print(f"Trust Score: {normalized['trustScore']}")
    print(f"Metadata: {normalized['metadata']}")
    
    assert normalized['agentType'] == 'mistral_agents'
    assert normalized['name'] == 'Code Assistant'
    assert 'function_calling:enabled' in normalized['capabilities']
    assert 'functions:4' in normalized['capabilities']
    assert 'json_mode:enabled' in normalized['capabilities']
    assert 'streaming:enabled' in normalized['capabilities']
    assert 'safe_mode:enabled' in normalized['capabilities']
    assert normalized['metadata']['temperature'] == 0.3

def test_lechat_features():
    """Test Le Chat specific features"""
    print("\n=== Testing Le Chat Features ===")
    
    lechat_config = {
        "name": "Le Chat Assistant",
        "model": "mistral-large",
        "lechat_config": {
            "web_search": True,
            "code_interpreter": True
        },
        "response_format": {
            "type": "json_object",
            "schema": {"type": "object"}
        }
    }
    
    normalized = normalize_agent_data(lechat_config)
    
    print(f"Name: {normalized['name']}")
    print(f"Capabilities: {normalized['capabilities']}")
    print(f"Response Format: {normalized['metadata'].get('responseFormat', {})}")
    
    assert 'web_search:enabled' in normalized['capabilities']
    assert 'code_interpreter:enabled' in normalized['capabilities']
    assert 'json_mode:enabled' in normalized['capabilities']
    assert normalized['metadata']['responseFormat']['type'] == 'json_object'

def test_function_types():
    """Test different function/tool configurations"""
    print("\n=== Testing Function Types ===")
    
    function_config = {
        "name": "Multi-Tool Agent",
        "tools": [
            {"name": "search", "type": "web_search"},
            {"name": "code_runner", "type": "code_interpreter"},
            {"name": "calculator", "description": "Perform calculations"}
        ]
    }
    
    normalized = normalize_agent_data(function_config)
    
    print(f"Name: {normalized['name']}")
    print(f"Capabilities: {normalized['capabilities']}")
    print(f"Functions: {normalized['metadata'].get('functions', [])}")
    
    assert 'web_search:enabled' in normalized['capabilities']
    assert 'code_interpreter:enabled' in normalized['capabilities']
    assert 'function:search' in normalized['capabilities']
    assert 'function:code_runner' in normalized['capabilities']
    assert 'function:calculator' in normalized['capabilities']

def test_trust_score_calculation():
    """Test trust score calculation for various configurations"""
    print("\n=== Testing Trust Score Calculation ===")
    
    # High trust agent (many features)
    high_trust = {
        "name": "Advanced Mistral Agent",
        "description": "Multi-functional Mistral AI agent",
        "model": "mistral-large",
        "functions": ["func1", "func2", "func3", "func4", "func5"],
        "json_mode": True,
        "safe_mode": True,
        "stream": True,
        "lechat_config": {
            "web_search": True,
            "code_interpreter": True
        }
    }
    
    normalized = normalize_agent_data(high_trust)
    print(f"High trust agent score: {normalized['trustScore']}")
    assert normalized['trustScore'] > 70
    
    # Low trust agent (minimal features)
    low_trust = {
        "name": "Simple Mistral Agent"
    }
    
    normalized = normalize_agent_data(low_trust)
    print(f"Low trust agent score: {normalized['trustScore']}")
    assert normalized['trustScore'] <= 85

def main():
    """Run all tests"""
    print("Starting Mistral Agents adapter tests...")
    
    try:
        test_mistral_object()
        test_mistral_dict()
        test_lechat_features()
        test_function_types()
        test_trust_score_calculation()
        
        print("\n✅ All Mistral Agents adapter tests passed!")
        
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()