#!/usr/bin/env python3
"""
Test script for BabyAGI adapter integration
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from astrasync.adapters.babyagi import normalize_agent_data, register_babyagi

def test_babyagi_object():
    """Test BabyAGI agent object normalization"""
    print("\n=== Testing BabyAGI Agent Object ===")
    
    # Mock BabyAGI instance
    class MockBabyAGI:
        def __init__(self):
            self.name = "Research BabyAGI"
            self.objective = "Research and summarize the latest AI developments"
            self.task_list = [
                {"task_id": 1, "task_name": "Search for AI papers"},
                {"task_id": 2, "task_name": "Read and analyze papers"},
                {"task_id": 3, "task_name": "Write summary report"}
            ]
            self.vectorstore = {"type": "pinecone", "index": "research"}
            self.execution_chain = {"type": "langchain"}
            self.llm = "gpt-4"
            
        def __class__(self):
            return type(self)
            
    MockBabyAGI.__module__ = "babyagi"
    MockBabyAGI.__name__ = "BabyAGI"
    
    agent = MockBabyAGI()
    agent.__class__ = MockBabyAGI
    
    normalized = normalize_agent_data(agent)
    
    print(f"Name: {normalized['name']}")
    print(f"Type: {normalized['agentType']}")
    print(f"Description: {normalized['description']}")
    print(f"Capabilities: {normalized['capabilities']}")
    print(f"Trust Score: {normalized['trustScore']}")
    print(f"Metadata: {normalized['metadata']}")
    
    assert normalized['agentType'] == 'babyagi'
    assert normalized['name'] == 'Research BabyAGI'
    assert 'tasks:3' in normalized['capabilities']
    assert 'memory:enabled' in normalized['capabilities']
    assert 'vectorstore:enabled' in normalized['capabilities']
    assert 'execution_chain:enabled' in normalized['capabilities']
    assert normalized['metadata']['objective'] == "Research and summarize the latest AI developments"

def test_babyagi_dict():
    """Test BabyAGI configuration dict normalization"""
    print("\n=== Testing BabyAGI Configuration Dict ===")
    
    agent_config = {
        "name": "Content Creator AGI",
        "objective": "Create engaging blog posts about technology",
        "initial_task": "Research trending tech topics",
        "task_list": [
            "Research topics",
            "Generate outlines", 
            "Write drafts",
            "Edit and polish"
        ],
        "vectorstore": {
            "type": "chroma",
            "collection": "content"
        },
        "llm": "gpt-3.5-turbo",
        "max_iterations": 10,
        "task_creation_chain": True,
        "task_prioritization_chain": True
    }
    
    normalized = normalize_agent_data(agent_config)
    
    print(f"Name: {normalized['name']}")
    print(f"Type: {normalized['agentType']}")
    print(f"Description: {normalized['description']}")
    print(f"Capabilities: {normalized['capabilities']}")
    print(f"Trust Score: {normalized['trustScore']}")
    print(f"Metadata: {normalized['metadata']}")
    
    assert normalized['agentType'] == 'babyagi'
    assert normalized['name'] == 'Content Creator AGI'
    assert 'autonomous:enabled' in normalized['capabilities']
    assert 'tasks:4' in normalized['capabilities']
    assert 'task_creation:enabled' in normalized['capabilities']
    assert 'task_prioritization:enabled' in normalized['capabilities']
    assert normalized['metadata']['maxIterations'] == 10

def test_complex_task_structure():
    """Test complex task structure handling"""
    print("\n=== Testing Complex Task Structure ===")
    
    complex_config = {
        "name": "Project Manager AGI",
        "objective": "Manage software development project",
        "tasks": [
            {"id": 1, "name": "Define requirements", "priority": "high", "status": "pending"},
            {"id": 2, "name": "Create architecture", "priority": "high", "status": "pending"},
            {"id": 3, "name": "Implement features", "priority": "medium", "status": "pending"},
            {"id": 4, "name": "Write tests", "priority": "medium", "status": "pending"},
            {"id": 5, "name": "Deploy", "priority": "low", "status": "pending"}
        ],
        "memory_backend": {
            "type": "redis",
            "host": "localhost"
        },
        "execution_chain": {
            "type": "custom",
            "modules": ["planner", "executor", "validator"]
        }
    }
    
    normalized = normalize_agent_data(complex_config)
    
    print(f"Name: {normalized['name']}")
    print(f"Task Count: {normalized['metadata'].get('taskCount', 0)}")
    print(f"Capabilities: {normalized['capabilities']}")
    
    assert 'tasks:5' in normalized['capabilities']
    assert 'task_prioritization:enabled' in normalized['capabilities']
    assert normalized['metadata']['taskStructure'] == 'complex'
    assert normalized['metadata']['executionChainType'] == 'custom'

def test_autonomous_features():
    """Test autonomous operation features"""
    print("\n=== Testing Autonomous Features ===")
    
    autonomous_config = {
        "objective": "Solve complex research problems autonomously",
        "task_creation_chain": {"model": "gpt-4"},
        "task_prioritization_chain": {"algorithm": "weighted"},
        "execution_chain": {"parallel": True},
        "vectorstore": {"type": "faiss"},
        "model": "gpt-4"
    }
    
    normalized = normalize_agent_data(autonomous_config)
    
    print(f"Name: {normalized['name']}")
    print(f"Description: {normalized['description']}")
    print(f"Capabilities: {normalized['capabilities']}")
    
    assert 'autonomous:enabled' in normalized['capabilities']
    assert 'task_creation:enabled' in normalized['capabilities']
    assert 'task_prioritization:enabled' in normalized['capabilities']
    assert 'memory:enabled' in normalized['capabilities']
    assert 'vectorstore:enabled' in normalized['capabilities']

def test_trust_score_calculation():
    """Test trust score calculation for various configurations"""
    print("\n=== Testing Trust Score Calculation ===")
    
    # High trust agent (many features)
    high_trust = {
        "name": "Advanced BabyAGI System",
        "objective": "Complex autonomous problem solving",
        "task_list": ["task1", "task2", "task3", "task4", "task5", "task6"],
        "vectorstore": {"type": "pinecone"},
        "task_creation_chain": True,
        "task_prioritization_chain": True,
        "execution_chain": {"type": "advanced"},
        "llm": "gpt-4"
    }
    
    normalized = normalize_agent_data(high_trust)
    print(f"High trust agent score: {normalized['trustScore']}")
    assert normalized['trustScore'] > 70
    
    # Low trust agent (minimal features)
    low_trust = {
        "name": "Simple BabyAGI",
        "objective": "Basic task"
    }
    
    normalized = normalize_agent_data(low_trust)
    print(f"Low trust agent score: {normalized['trustScore']}")
    assert normalized['trustScore'] <= 92  # Base score plus objective bonus

def main():
    """Run all tests"""
    print("Starting BabyAGI adapter tests...")
    
    try:
        test_babyagi_object()
        test_babyagi_dict()
        test_complex_task_structure()
        test_autonomous_features()
        test_trust_score_calculation()
        
        print("\n✅ All BabyAGI adapter tests passed!")
        
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