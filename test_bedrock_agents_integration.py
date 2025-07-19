#!/usr/bin/env python3
"""
Test script for Bedrock Agents adapter integration
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from astrasync.adapters.bedrock_agents import normalize_agent_data, register_bedrock_agents

def test_bedrock_object():
    """Test Bedrock agent object normalization"""
    print("\n=== Testing Bedrock Agent Object ===")
    
    # Mock Bedrock Agent
    class MockBedrockAgent:
        def __init__(self):
            self.agent_name = "Customer Support Agent"
            self.agent_id = "AGENT123456"
            self.agent_arn = "arn:aws:bedrock:us-east-1:123456789:agent/AGENT123456"
            self.agent_version = "1"
            self.description = "AI agent for customer support"
            self.instruction = "You are a helpful customer support agent. Help customers with their queries professionally."
            self.foundation_model = "anthropic.claude-v2"
            self.action_groups = [
                {
                    "action_group_name": "OrderManagement",
                    "api_schema": {"source": "s3://bucket/openapi.json"},
                    "action_group_executor": {"lambda": "arn:aws:lambda:us-east-1:123456789:function:OrderHandler"}
                },
                {
                    "action_group_name": "CustomerData",
                    "api_schema": {"inline": "..."}
                }
            ]
            self.knowledge_bases = [
                {"knowledge_base_id": "KB001", "description": "Product documentation"}
            ]
            self.guardrails = {"guardrail_id": "GR001", "version": "1"}
            
        def __class__(self):
            return type(self)
            
    MockBedrockAgent.__module__ = "bedrock"
    MockBedrockAgent.__name__ = "BedrockAgent"
    
    agent = MockBedrockAgent()
    agent.__class__ = MockBedrockAgent
    
    normalized = normalize_agent_data(agent)
    
    print(f"Name: {normalized['name']}")
    print(f"Type: {normalized['agentType']}")
    print(f"Description: {normalized['description']}")
    print(f"Capabilities: {normalized['capabilities']}")
    print(f"Trust Score: {normalized['trustScore']}")
    print(f"Metadata: {normalized['metadata']}")
    
    assert normalized['agentType'] == 'bedrock_agents'
    assert normalized['name'] == 'Customer Support Agent'
    assert 'action_groups:enabled' in normalized['capabilities']
    assert 'knowledge_bases:enabled' in normalized['capabilities']
    assert 'guardrails:enabled' in normalized['capabilities']
    assert 'lambda:enabled' in normalized['capabilities']
    assert normalized['metadata']['actionGroupCount'] == 2
    assert normalized['trustScore'] > 70

def test_bedrock_dict():
    """Test Bedrock configuration dict normalization"""
    print("\n=== Testing Bedrock Configuration Dict ===")
    
    agent_config = {
        "agent_name": "Sales Assistant",
        "instruction": "Help customers find products and complete purchases. Be friendly and knowledgeable.",
        "foundation_model": "anthropic.claude-instant-v1",
        "agent_resource_role_arn": "arn:aws:iam::123456789:role/BedrockAgentRole",
        "action_groups": [
            {
                "name": "ProductSearch",
                "api_schema": {"source": "s3://api-schemas/product-search.yaml"},
                "action_group_executor": {"lambda": "arn:aws:lambda:us-east-1:123456789:function:ProductSearch"}
            },
            {
                "name": "InventoryCheck",
                "api_schema": {"source": "s3://api-schemas/inventory.yaml"}
            },
            {
                "name": "OrderProcessing",
                "api_schema": {"inline": "openapi: 3.0.0..."}
            }
        ],
        "knowledge_bases": [
            {"id": "KB-PRODUCTS", "description": "Product catalog and specifications"},
            {"id": "KB-POLICIES", "description": "Company policies and procedures"}
        ],
        "guardrails": {
            "guardrail_id": "sales-guardrail",
            "version": "2"
        },
        "idle_session_ttl": 3600,
        "tags": {
            "Environment": "Production",
            "Team": "Sales"
        }
    }
    
    normalized = normalize_agent_data(agent_config)
    
    print(f"Name: {normalized['name']}")
    print(f"Type: {normalized['agentType']}")
    print(f"Description: {normalized['description']}")
    print(f"Capabilities: {normalized['capabilities']}")
    print(f"Trust Score: {normalized['trustScore']}")
    print(f"Action Groups: {normalized['metadata'].get('actionGroups', [])}")
    print(f"Knowledge Bases: {normalized['metadata'].get('knowledgeBases', [])}")
    
    assert normalized['agentType'] == 'bedrock_agents'
    assert normalized['name'] == 'Sales Assistant'
    assert 'iam:configured' in normalized['capabilities']
    assert 'action_groups:enabled' in normalized['capabilities']
    assert 'knowledge_bases:enabled' in normalized['capabilities']
    assert 'rag:enabled' in normalized['capabilities']
    assert normalized['metadata']['actionGroupCount'] == 3
    assert normalized['metadata']['knowledgeBaseCount'] == 2

def test_minimal_config():
    """Test minimal Bedrock configuration"""
    print("\n=== Testing Minimal Configuration ===")
    
    minimal_config = {
        "agent_name": "Simple Agent",
        "instruction": "Answer questions helpfully",
        "foundation_model": "amazon.titan-text-express-v1"
    }
    
    normalized = normalize_agent_data(minimal_config)
    
    print(f"Name: {normalized['name']}")
    print(f"Capabilities: {normalized['capabilities']}")
    print(f"Model: {normalized['metadata'].get('foundationModel', 'None')}")
    
    assert normalized['name'] == 'Simple Agent'
    assert 'model:amazon.titan-text-express-v1' in normalized['capabilities']
    assert normalized['metadata']['foundationModel'] == 'amazon.titan-text-express-v1'

def test_advanced_features():
    """Test advanced Bedrock features"""
    print("\n=== Testing Advanced Features ===")
    
    advanced_config = {
        "name": "Advanced Bedrock Agent",
        "foundation_model": "meta.llama2-70b-chat-v1",
        "prompt_override_configuration": {
            "prompt_configurations": [
                {"promptType": "PRE_PROCESSING", "basePromptTemplate": "..."}
            ]
        },
        "customer_encryption_key_arn": "arn:aws:kms:us-east-1:123456789:key/12345678-1234-1234-1234-123456789012",
        "action_groups": ["APIGroup1", "APIGroup2"],
        "knowledge_bases": ["KB1", "KB2", "KB3"]
    }
    
    normalized = normalize_agent_data(advanced_config)
    
    print(f"Name: {normalized['name']}")
    print(f"Capabilities: {normalized['capabilities']}")
    print(f"Has Prompt Override: {'prompt_override:enabled' in normalized['capabilities']}")
    print(f"Has Custom Encryption: {'encryption:custom' in normalized['capabilities']}")
    
    assert 'prompt_override:enabled' in normalized['capabilities']
    assert 'encryption:custom' in normalized['capabilities']
    assert normalized['metadata']['actionGroupCount'] == 2
    assert normalized['metadata']['knowledgeBaseCount'] == 3

def test_trust_score_calculation():
    """Test trust score calculation for various configurations"""
    print("\n=== Testing Trust Score Calculation ===")
    
    # High trust agent (many features)
    high_trust = {
        "agent_name": "Enterprise Bedrock Agent",
        "description": "Advanced enterprise AI agent",
        "foundation_model": "anthropic.claude-v2",
        "agent_resource_role_arn": "arn:aws:iam::123456789:role/BedrockAgentRole",
        "action_groups": [
            {"name": "API1", "api_schema": {"source": "s3://schema1.json"}},
            {"name": "API2", "api_schema": {"source": "s3://schema2.json"}},
            {"name": "API3", "api_schema": {"source": "s3://schema3.json"}}
        ],
        "knowledge_bases": [
            {"id": "KB1"},
            {"id": "KB2"}
        ],
        "guardrails": {"guardrail_id": "GR001"},
        "customer_encryption_key_arn": "arn:aws:kms:us-east-1:123456789:key/custom-key"
    }
    
    normalized = normalize_agent_data(high_trust)
    print(f"High trust agent score: {normalized['trustScore']}")
    assert normalized['trustScore'] > 70
    
    # Low trust agent (minimal features)
    low_trust = {
        "name": "Simple Bedrock Agent"
    }
    
    normalized = normalize_agent_data(low_trust)
    print(f"Low trust agent score: {normalized['trustScore']}")
    assert normalized['trustScore'] <= 85

def main():
    """Run all tests"""
    print("Starting Bedrock Agents adapter tests...")
    
    try:
        test_bedrock_object()
        test_bedrock_dict()
        test_minimal_config()
        test_advanced_features()
        test_trust_score_calculation()
        
        print("\n✅ All Bedrock Agents adapter tests passed!")
        
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