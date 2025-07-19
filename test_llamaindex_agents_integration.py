#!/usr/bin/env python3
"""
Test script for LlamaIndex agents adapter integration
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from astrasync.adapters.llamaindex_agents import normalize_agent_data, register_llamaindex_agents

def test_agent_service():
    """Test LlamaIndex AgentService normalization"""
    print("\n=== Testing LlamaIndex AgentService ===")
    
    # Mock AgentService
    class MockAgentService:
        def __init__(self):
            self.name = "Query Processing Service"
            self.service_name = "query_processor"
            self.host = "localhost"
            self.port = 8080
            self.description = "Service for processing complex queries"
            
        def __class__(self):
            return type(self)
            
    MockAgentService.__module__ = "llama_index.agents"
    MockAgentService.__name__ = "AgentService"
    
    service = MockAgentService()
    service.__class__ = MockAgentService
    
    normalized = normalize_agent_data(service)
    
    print(f"Name: {normalized['name']}")
    print(f"Type: {normalized['agentType']}")
    print(f"Description: {normalized['description']}")
    print(f"Capabilities: {normalized['capabilities']}")
    print(f"Trust Score: {normalized['trustScore']}")
    print(f"Metadata: {normalized['metadata']}")
    
    assert normalized['agentType'] == 'llamaindex_agents'
    assert normalized['name'] == 'Query Processing Service'
    assert 'microservice:enabled' in normalized['capabilities']
    assert normalized['metadata']['serviceName'] == 'query_processor'
    assert normalized['metadata']['host'] == 'localhost'
    assert normalized['metadata']['port'] == 8080

def test_agent_worker():
    """Test LlamaIndex Agent/Worker normalization"""
    print("\n=== Testing LlamaIndex Agent Worker ===")
    
    # Mock Agent with tools
    class MockAgent:
        def __init__(self):
            self.name = "Research Agent"
            self.description = "Agent for research tasks"
            self.tools = ["search_tool", "summarize_tool", "extract_tool"]
            
        def __class__(self):
            return type(self)
            
    MockAgent.__module__ = "llamaindex"
    MockAgent.__name__ = "Agent"
    
    agent = MockAgent()
    agent.__class__ = MockAgent
    
    normalized = normalize_agent_data(agent)
    
    print(f"Name: {normalized['name']}")
    print(f"Capabilities: {normalized['capabilities']}")
    print(f"Tool Count: {normalized['metadata'].get('toolCount', 0)}")
    
    assert 'agent:enabled' in normalized['capabilities']
    assert 'tools:3' in normalized['capabilities']
    assert normalized['metadata']['toolCount'] == 3

def test_orchestrator():
    """Test LlamaIndex Orchestrator configuration"""
    print("\n=== Testing LlamaIndex Orchestrator ===")
    
    orchestrator_config = {
        "name": "Multi-Agent Orchestrator",
        "orchestrator": {
            "agents": [
                {"name": "Agent1", "type": "research"},
                {"name": "Agent2", "type": "analysis"},
                {"name": "Agent3", "type": "synthesis"}
            ]
        },
        "message_queue": {
            "type": "rabbitmq",
            "host": "localhost"
        },
        "control_plane": True
    }
    
    normalized = normalize_agent_data(orchestrator_config)
    
    print(f"Name: {normalized['name']}")
    print(f"Capabilities: {normalized['capabilities']}")
    print(f"Agent Count: {normalized['metadata'].get('agentCount', 0)}")
    print(f"Message Queue Type: {normalized['metadata'].get('messageQueueType', 'None')}")
    
    assert 'orchestrator:enabled' in normalized['capabilities']
    assert 'agents:3' in normalized['capabilities']
    assert 'message_queue:enabled' in normalized['capabilities']
    assert 'control_plane:enabled' in normalized['capabilities']
    assert normalized['metadata']['agentCount'] == 3
    assert normalized['metadata']['messageQueueType'] == 'rabbitmq'

def test_microservice_config():
    """Test microservice configuration"""
    print("\n=== Testing Microservice Configuration ===")
    
    service_config = {
        "name": "Document Processing Service",
        "agent_service": {
            "service_name": "doc_processor",
            "description": "Process and index documents",
            "host": "0.0.0.0",
            "port": 5000
        },
        "agent": {
            "system_prompt": "You are a document processing expert",
            "tools": ["pdf_reader", "text_extractor", "embedder"]
        },
        "human_in_loop": True
    }
    
    normalized = normalize_agent_data(service_config)
    
    print(f"Name: {normalized['name']}")
    print(f"Description: {normalized['description']}")
    print(f"Capabilities: {normalized['capabilities']}")
    print(f"Service Name: {normalized['metadata'].get('serviceName', 'None')}")
    
    assert normalized['name'] == 'Document Processing Service'
    assert normalized['description'] == 'Process and index documents'
    assert 'microservice:enabled' in normalized['capabilities']
    assert 'human_in_loop:enabled' in normalized['capabilities']
    assert normalized['metadata']['serviceName'] == 'doc_processor'

def test_tool_extraction():
    """Test tool extraction from various formats"""
    print("\n=== Testing Tool Extraction ===")
    
    tool_config = {
        "name": "Tool User Agent",
        "tools": [
            "search",
            {"name": "calculator", "description": "Math calculations"},
            {"tool_name": "translator", "languages": ["en", "es", "fr"]}
        ]
    }
    
    normalized = normalize_agent_data(tool_config)
    
    print(f"Name: {normalized['name']}")
    print(f"Capabilities: {normalized['capabilities']}")
    print(f"Tools: {normalized['metadata'].get('tools', [])}")
    
    assert 'tools:3' in normalized['capabilities']
    assert 'tool:search' in normalized['capabilities']
    assert 'tool:calculator' in normalized['capabilities']
    assert 'tool:translator' in normalized['capabilities']
    assert len(normalized['metadata']['tools']) == 3

def test_trust_score_calculation():
    """Test trust score calculation for various configurations"""
    print("\n=== Testing Trust Score Calculation ===")
    
    # High trust agent (many features)
    high_trust = {
        "name": "Advanced LlamaIndex System",
        "orchestrator": {
            "agents": ["agent1", "agent2", "agent3", "agent4"]
        },
        "message_queue": {"type": "kafka"},
        "control_plane": True,
        "agent_service": {
            "service_name": "main_service"
        }
    }
    
    normalized = normalize_agent_data(high_trust)
    print(f"High trust agent score: {normalized['trustScore']}")
    assert normalized['trustScore'] > 70
    
    # Low trust agent (minimal features)
    low_trust = {
        "name": "Simple LlamaIndex Agent"
    }
    
    normalized = normalize_agent_data(low_trust)
    print(f"Low trust agent score: {normalized['trustScore']}")
    assert normalized['trustScore'] <= 85

def main():
    """Run all tests"""
    print("Starting LlamaIndex agents adapter tests...")
    
    try:
        test_agent_service()
        test_agent_worker()
        test_orchestrator()
        test_microservice_config()
        test_tool_extraction()
        test_trust_score_calculation()
        
        print("\n✅ All LlamaIndex agents adapter tests passed!")
        
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