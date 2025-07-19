#!/usr/bin/env python3
"""
Test script for Semantic Kernel adapter integration
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from astrasync.adapters.semantic_kernel import normalize_agent_data, register_semantic_kernel

def test_semantic_kernel_object():
    """Test Semantic Kernel agent object normalization"""
    print("\n=== Testing Semantic Kernel Agent Object ===")
    
    # Mock Semantic Kernel Agent
    class MockSKAgent:
        def __init__(self):
            self.name = "Knowledge Assistant"
            self.description = "An AI assistant powered by Semantic Kernel"
            self.kernel = MockKernel()
            
        def __class__(self):
            return type(self)
            
    class MockKernel:
        def __init__(self):
            self.plugins = ["WebSearch", "Calculator", "TextGeneration"]
            self.memory = {"type": "semantic"}
            
    MockSKAgent.__module__ = "semantic_kernel"
    MockSKAgent.__name__ = "Agent"
    
    agent = MockSKAgent()
    agent.__class__ = MockSKAgent
    
    normalized = normalize_agent_data(agent)
    
    print(f"Name: {normalized['name']}")
    print(f"Type: {normalized['agentType']}")
    print(f"Description: {normalized['description']}")
    print(f"Capabilities: {normalized['capabilities']}")
    print(f"Trust Score: {normalized['trustScore']}")
    print(f"Metadata: {normalized['metadata']}")
    
    assert normalized['agentType'] == 'semantic_kernel'
    assert normalized['name'] == 'Knowledge Assistant'
    assert 'plugins:3' in normalized['capabilities']
    assert 'memory:enabled' in normalized['capabilities']
    assert normalized['trustScore'] > 50

def test_semantic_kernel_dict():
    """Test Semantic Kernel configuration dict normalization"""
    print("\n=== Testing Semantic Kernel Configuration Dict ===")
    
    agent_config = {
        "name": "Enterprise Assistant",
        "description": "Enterprise-grade AI assistant",
        "kernel": {
            "model": "gpt-4",
            "temperature": 0.7
        },
        "plugins": [
            {"name": "EmailPlugin", "functions": ["send", "read", "search"]},
            {"name": "CalendarPlugin", "functions": ["schedule", "list"]}
        ],
        "memory": {
            "type": "semantic",
            "store": "qdrant"
        },
        "planner": {
            "type": "sequential"
        }
    }
    
    normalized = normalize_agent_data(agent_config)
    
    print(f"Name: {normalized['name']}")
    print(f"Type: {normalized['agentType']}")
    print(f"Description: {normalized['description']}")
    print(f"Capabilities: {normalized['capabilities']}")
    print(f"Trust Score: {normalized['trustScore']}")
    print(f"Metadata: {normalized['metadata']}")
    
    assert normalized['agentType'] == 'semantic_kernel'
    assert normalized['name'] == 'Enterprise Assistant'
    assert 'plugins:2' in normalized['capabilities']
    assert 'memory:enabled' in normalized['capabilities']
    assert 'planner:sequential' in normalized['capabilities']
    assert normalized['metadata']['memoryType'] == 'semantic'

def test_sk_plugins():
    """Test Semantic Kernel plugin configuration"""
    print("\n=== Testing SK Plugin Configuration ===")
    
    plugin_config = {
        "name": "Plugin Manager",
        "plugins": {
            "WebSearchPlugin": {
                "functions": ["search", "scrape", "summarize"]
            },
            "MathPlugin": {
                "functions": ["calculate", "solve"]
            },
            "TextPlugin": {
                "functions": ["translate", "summarize", "analyze"]
            }
        },
        "orchestration": True
    }
    
    normalized = normalize_agent_data(plugin_config)
    
    print(f"Name: {normalized['name']}")
    print(f"Capabilities: {normalized['capabilities']}")
    print(f"Plugin Count: {normalized['metadata'].get('pluginCount', 0)}")
    
    assert 'plugins:3' in normalized['capabilities']
    assert 'orchestration:enabled' in normalized['capabilities']
    assert normalized['metadata']['pluginCount'] == 3

def test_sk_agent_with_skills():
    """Test Semantic Kernel with skills (legacy name for plugins)"""
    print("\n=== Testing SK Agent with Skills ===")
    
    agent_config = {
        "name": "Skill-based Assistant",
        "skills": [
            "WriterSkill",
            "PlannerSkill",
            "WebSkill"
        ],
        "kernel": {
            "model": "gpt-3.5-turbo"
        }
    }
    
    normalized = normalize_agent_data(agent_config)
    
    print(f"Name: {normalized['name']}")
    print(f"Capabilities: {normalized['capabilities']}")
    print(f"Skill Count: {normalized['metadata'].get('skillCount', 0)}")
    
    assert 'skills:3' in normalized['capabilities']
    assert normalized['metadata']['skillCount'] == 3

def test_trust_score_calculation():
    """Test trust score calculation for various configurations"""
    print("\n=== Testing Trust Score Calculation ===")
    
    # High trust agent (many features)
    high_trust = {
        "name": "Advanced SK Agent",
        "description": "Multi-functional Semantic Kernel agent",
        "plugins": ["Plugin1", "Plugin2", "Plugin3", "Plugin4", "Plugin5"],
        "memory": {"type": "semantic"},
        "planner": {"type": "stepwise"},
        "orchestration": True,
        "kernel": {
            "model": "gpt-4",
            "functions": ["func1", "func2", "func3"]
        }
    }
    
    normalized = normalize_agent_data(high_trust)
    print(f"High trust agent score: {normalized['trustScore']}")
    assert normalized['trustScore'] > 70
    
    # Low trust agent (minimal features)
    low_trust = {
        "name": "Simple SK Agent"
    }
    
    normalized = normalize_agent_data(low_trust)
    print(f"Low trust agent score: {normalized['trustScore']}")
    assert normalized['trustScore'] <= 85

def main():
    """Run all tests"""
    print("Starting Semantic Kernel adapter tests...")
    
    try:
        test_semantic_kernel_object()
        test_semantic_kernel_dict()
        test_sk_plugins()
        test_sk_agent_with_skills()
        test_trust_score_calculation()
        
        print("\n✅ All Semantic Kernel adapter tests passed!")
        
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()