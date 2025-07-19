#!/usr/bin/env python3
"""
Test script for Llama Stack adapter integration
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from astrasync.adapters.llamastack import normalize_agent_data, register_llamastack

def test_llamastack_object():
    """Test Llama Stack agent object normalization"""
    print("\n=== Testing Llama Stack Agent Object ===")
    
    # Mock Llama Stack Agent
    class MockLlamaStackAgent:
        def __init__(self):
            self.name = "Research Assistant"
            self.config = {
                "model": "llama-3.1-70b",
                "tools": [
                    {"name": "web_search", "type": "web_search"},
                    {"name": "code_interpreter", "type": "code_interpreter"}
                ]
            }
            self.memory = {"type": "conversational"}
            
        def __class__(self):
            return type(self)
            
    MockLlamaStackAgent.__module__ = "llamastack"
    MockLlamaStackAgent.__name__ = "Agent"
    
    agent = MockLlamaStackAgent()
    agent.__class__ = MockLlamaStackAgent
    
    normalized = normalize_agent_data(agent)
    
    print(f"Name: {normalized['name']}")
    print(f"Type: {normalized['agentType']}")
    print(f"Description: {normalized['description']}")
    print(f"Capabilities: {normalized['capabilities']}")
    print(f"Trust Score: {normalized['trustScore']}")
    print(f"Metadata: {normalized['metadata']}")
    
    assert normalized['agentType'] == 'llamastack'
    assert normalized['name'] == 'Research Assistant'
    assert 'memory:enabled' in normalized['capabilities']
    assert 'model:llama-3.1-70b' in normalized['capabilities']
    assert normalized['trustScore'] > 50

def test_llamastack_dict():
    """Test Llama Stack configuration dict normalization"""
    print("\n=== Testing Llama Stack Configuration Dict ===")
    
    agent_config = {
        "name": "Code Assistant",
        "agent_config": {
            "system_prompt": "You are an expert programmer. Help users write clean, efficient code.",
            "model": "llama-3.1-8b",
            "temperature": 0.3
        },
        "tools": [
            {"name": "code_interpreter", "type": "code_interpreter"},
            {"name": "file_reader", "type": "tool", "description": "Read files"}
        ],
        "memory": {
            "type": "semantic",
            "store": "chroma"
        },
        "safety": {
            "shields": ["prompt_guard", "llama_guard"]
        },
        "multi_turn": {
            "max_turns": 10
        },
        "code_execution": True
    }
    
    normalized = normalize_agent_data(agent_config)
    
    print(f"Name: {normalized['name']}")
    print(f"Type: {normalized['agentType']}")
    print(f"Description: {normalized['description']}")
    print(f"Capabilities: {normalized['capabilities']}")
    print(f"Trust Score: {normalized['trustScore']}")
    print(f"Metadata: {normalized['metadata']}")
    
    assert normalized['agentType'] == 'llamastack'
    assert normalized['name'] == 'Code Assistant'
    assert 'memory:enabled' in normalized['capabilities']
    assert 'code_execution:enabled' in normalized['capabilities']
    assert 'safety:enabled' in normalized['capabilities']
    assert 'shields:2' in normalized['capabilities']
    assert 'multi_turn:enabled' in normalized['capabilities']
    assert normalized['metadata']['maxTurns'] == 10

def test_tools_extraction():
    """Test tool extraction from Llama Stack config"""
    print("\n=== Testing Tool Extraction ===")
    
    tool_config = {
        "name": "Tool User",
        "tools": [
            "web_search",
            {"name": "calculator", "type": "math"},
            {"name": "code_runner", "type": "code_interpreter"}
        ]
    }
    
    normalized = normalize_agent_data(tool_config)
    
    print(f"Name: {normalized['name']}")
    print(f"Capabilities: {normalized['capabilities']}")
    print(f"Tool Count: {normalized['metadata'].get('toolCount', 0)}")
    print(f"Tools: {normalized['metadata'].get('tools', [])}")
    
    assert 'tools:3' in normalized['capabilities']
    assert 'tool:web_search' in normalized['capabilities']
    assert 'tool:calculator' in normalized['capabilities']
    assert 'code_execution:enabled' in normalized['capabilities']  # from code_interpreter
    assert 'web_search:enabled' in normalized['capabilities']

def test_memory_types():
    """Test different memory configurations"""
    print("\n=== Testing Memory Types ===")
    
    memory_configs = [
        {"name": "Agent1", "memory": {"type": "conversational"}},
        {"name": "Agent2", "memory": {"type": "semantic", "store": "pinecone"}},
        {"name": "Agent3", "memory": True}
    ]
    
    for config in memory_configs:
        normalized = normalize_agent_data(config)
        print(f"{config['name']}: {normalized['capabilities']}")
        assert 'memory:enabled' in normalized['capabilities']

def test_trust_score_calculation():
    """Test trust score calculation for various configurations"""
    print("\n=== Testing Trust Score Calculation ===")
    
    # High trust agent (many features)
    high_trust = {
        "name": "Advanced Llama Agent",
        "description": "Multi-functional Llama Stack agent",
        "agent_config": {
            "model": "llama-3.1-405b",
            "system_prompt": "Advanced AI assistant"
        },
        "tools": ["tool1", "tool2", "tool3", "tool4", "tool5"],
        "memory": {"type": "semantic"},
        "safety": {"shields": ["shield1", "shield2"]},
        "code_execution": True,
        "multi_turn": {"max_turns": 20}
    }
    
    normalized = normalize_agent_data(high_trust)
    print(f"High trust agent score: {normalized['trustScore']}")
    assert normalized['trustScore'] > 70
    
    # Low trust agent (minimal features)
    low_trust = {
        "name": "Simple Llama Agent"
    }
    
    normalized = normalize_agent_data(low_trust)
    print(f"Low trust agent score: {normalized['trustScore']}")
    assert normalized['trustScore'] <= 85

def main():
    """Run all tests"""
    print("Starting Llama Stack adapter tests...")
    
    try:
        test_llamastack_object()
        test_llamastack_dict()
        test_tools_extraction()
        test_memory_types()
        test_trust_score_calculation()
        
        print("\n✅ All Llama Stack adapter tests passed!")
        
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