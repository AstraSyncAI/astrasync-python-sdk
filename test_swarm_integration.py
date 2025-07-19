#!/usr/bin/env python3
"""
Test script for OpenAI Swarm adapter integration
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from astrasync.adapters.swarm import normalize_agent_data, register_swarm

def test_swarm_object():
    """Test Swarm agent object normalization"""
    print("\n=== Testing Swarm Agent Object ===")
    
    # Mock Swarm Agent
    class MockSwarmAgent:
        def __init__(self):
            self.name = "Customer Support Agent"
            self.instructions = "You are a helpful customer support agent. Be polite and professional."
            self.functions = [self.check_order, self.process_refund, self.escalate_issue]
            self.model = "gpt-4"
            
        def check_order(self):
            pass
            
        def process_refund(self):
            pass
            
        def escalate_issue(self):
            pass
            
        def __class__(self):
            return type(self)
            
    MockSwarmAgent.__module__ = "swarm"
    MockSwarmAgent.__name__ = "Agent"
    
    agent = MockSwarmAgent()
    agent.__class__ = MockSwarmAgent
    
    normalized = normalize_agent_data(agent)
    
    print(f"Name: {normalized['name']}")
    print(f"Type: {normalized['agentType']}")
    print(f"Description: {normalized['description']}")
    print(f"Capabilities: {normalized['capabilities']}")
    print(f"Trust Score: {normalized['trustScore']}")
    print(f"Metadata: {normalized['metadata']}")
    
    assert normalized['agentType'] == 'swarm'
    assert normalized['name'] == 'Customer Support Agent'
    assert 'functions:3' in normalized['capabilities']
    assert 'model:gpt-4' in normalized['capabilities']
    assert normalized['trustScore'] > 50

def test_swarm_dict():
    """Test Swarm configuration dict normalization"""
    print("\n=== Testing Swarm Configuration Dict ===")
    
    agent_config = {
        "name": "Sales Assistant",
        "instructions": "Help customers find the right products and complete purchases",
        "model": "gpt-3.5-turbo",
        "functions": ["search_products", "check_inventory", "create_order"],
        "handoffs": ["technical_support", "billing_department"]
    }
    
    normalized = normalize_agent_data(agent_config)
    
    print(f"Name: {normalized['name']}")
    print(f"Type: {normalized['agentType']}")
    print(f"Description: {normalized['description']}")
    print(f"Capabilities: {normalized['capabilities']}")
    print(f"Trust Score: {normalized['trustScore']}")
    print(f"Metadata: {normalized['metadata']}")
    
    assert normalized['agentType'] == 'swarm'
    assert normalized['name'] == 'Sales Assistant'
    assert 'functions:3' in normalized['capabilities']
    assert 'handoffs:enabled' in normalized['capabilities']
    assert normalized['metadata']['handoffTargets'] == ["technical_support", "billing_department"]

def test_multi_agent_swarm():
    """Test multi-agent Swarm configuration"""
    print("\n=== Testing Multi-Agent Swarm ===")
    
    swarm_config = {
        "name": "Support Swarm",
        "agents": [
            {"name": "Triage Agent", "instructions": "Route requests to appropriate agents"},
            {"name": "Technical Agent", "instructions": "Handle technical issues"},
            {"name": "Billing Agent", "instructions": "Handle billing inquiries"}
        ],
        "routines": [
            {"name": "escalation", "steps": ["evaluate", "transfer", "notify"]}
        ]
    }
    
    normalized = normalize_agent_data(swarm_config)
    
    print(f"Name: {normalized['name']}")
    print(f"Capabilities: {normalized['capabilities']}")
    print(f"Agent Count: {normalized['metadata'].get('agentCount', 0)}")
    print(f"Routine Count: {normalized['metadata'].get('routineCount', 0)}")
    
    assert 'agents:3' in normalized['capabilities']
    assert 'routines:enabled' in normalized['capabilities']
    assert normalized['metadata']['agentCount'] == 3
    assert normalized['metadata']['routineCount'] == 1

def test_dynamic_instructions():
    """Test Swarm with dynamic instructions"""
    print("\n=== Testing Dynamic Instructions ===")
    
    # Mock agent with callable instructions
    class MockDynamicAgent:
        def __init__(self):
            self.name = "Context-Aware Agent"
            self.instructions = lambda context: f"Current context: {context}"
            self.model = "gpt-4"
            
        def __class__(self):
            return type(self)
            
    MockDynamicAgent.__module__ = "swarm"
    MockDynamicAgent.__name__ = "Agent"
    
    agent = MockDynamicAgent()
    agent.__class__ = MockDynamicAgent
    
    normalized = normalize_agent_data(agent)
    
    print(f"Name: {normalized['name']}")
    print(f"Description: {normalized['description']}")
    print(f"Capabilities: {normalized['capabilities']}")
    
    assert normalized['description'] == 'Swarm agent with dynamic instructions'
    assert 'dynamic_instructions:enabled' in normalized['capabilities']

def test_trust_score_calculation():
    """Test trust score calculation for various configurations"""
    print("\n=== Testing Trust Score Calculation ===")
    
    # High trust agent (many features)
    high_trust = {
        "name": "Advanced Swarm Agent",
        "description": "Multi-functional Swarm agent",
        "model": "gpt-4",
        "functions": ["func1", "func2", "func3", "func4", "func5"],
        "handoffs": ["agent1", "agent2", "agent3"],
        "agents": [
            {"name": "Agent1"},
            {"name": "Agent2"}
        ]
    }
    
    normalized = normalize_agent_data(high_trust)
    print(f"High trust agent score: {normalized['trustScore']}")
    assert normalized['trustScore'] > 70
    
    # Low trust agent (minimal features)
    low_trust = {
        "name": "Simple Swarm Agent"
    }
    
    normalized = normalize_agent_data(low_trust)
    print(f"Low trust agent score: {normalized['trustScore']}")
    assert normalized['trustScore'] <= 85

def main():
    """Run all tests"""
    print("Starting Swarm adapter tests...")
    
    try:
        test_swarm_object()
        test_swarm_dict()
        test_multi_agent_swarm()
        test_dynamic_instructions()
        test_trust_score_calculation()
        
        print("\n✅ All Swarm adapter tests passed!")
        
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