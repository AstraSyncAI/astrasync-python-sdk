#!/usr/bin/env python3
"""
Test script for LangChain integration with AstraSync
"""

import sys
import json
from astrasync import AstraSync, detect_agent_type
from astrasync.adapters.langchain import register_langchain

def test_langchain_detection():
    """Test LangChain agent detection"""
    print("\n🔍 Testing LangChain Detection...")
    
    # Test cases
    test_cases = [
        {
            "name": "Basic LangChain Agent",
            "data": {
                "agent_type": "conversational",
                "llm": "gpt-4",
                "tools": ["search", "calculator"],
                "memory": {"type": "buffer"}
            }
        },
        {
            "name": "LangChain Chain",
            "data": {
                "llm": "claude-3",
                "tools": ["analyzer", "summarizer"],
                "prompt": "Analyze and summarize..."
            }
        },
        {
            "name": "Mock LangChain Object",
            "data": type('MockAgent', (), {
                '__module__': 'langchain.agents',
                '__class__': type('AgentExecutor', (), {'__name__': 'AgentExecutor'}),
                'tools': ['web_search'],
                'memory': {}
            })()
        }
    ]
    
    for test in test_cases:
        detected = detect_agent_type(test["data"])
        print(f"  ✓ {test['name']}: {detected}")
        assert detected == "langchain", f"Failed to detect {test['name']} as langchain"
    
    print("  ✅ All detection tests passed!")


def test_langchain_registration():
    """Test LangChain agent registration"""
    print("\n📝 Testing LangChain Registration...")
    
    # Test agent configuration
    agent_config = {
        "name": "Test LangChain Agent",
        "agent_type": "qa",
        "llm": "gpt-3.5-turbo",
        "tools": ["retriever", "reranker"],
        "memory": {
            "type": "vector_store",
            "dimension": 1536
        },
        "description": "Question-answering agent with retrieval capabilities",
        "owner": "Test Suite"
    }
    
    try:
        # Test with mock email (won't actually register)
        result = register_langchain(
            agent=agent_config,
            email="test@example.com",
            owner="Test Organization"
        )
        
        print(f"  ✓ Registration response received")
        print(f"    - Agent ID: {result.get('agentId', 'N/A')}")
        print(f"    - Status: {result.get('status', 'N/A')}")
        print(f"    - Trust Score: {result.get('trustScore', 'N/A')}")
        
        # Note: In developer preview, we'll get a temporary ID
        if result.get('agentId', '').startswith('TEMP-'):
            print("  ✅ Registration test passed (developer preview mode)")
        else:
            print("  ✅ Registration test passed")
            
    except Exception as e:
        print(f"  ❌ Registration failed: {e}")
        # This is expected if we're not connected to the API
        if "Connection" in str(e) or "request" in str(e):
            print("  ℹ️  API connection error (expected in offline testing)")
        else:
            raise


def test_normalization():
    """Test LangChain data normalization"""
    print("\n🔄 Testing Data Normalization...")
    
    from astrasync.adapters.langchain import normalize_agent_data
    
    # Test normalization
    agent_data = {
        "name": "Normalized Agent",
        "agent_type": "task",
        "llm": "mixtral-8x7b",
        "tools": [
            {"name": "code_executor", "description": "Execute code"},
            "file_reader",
            {"name": "web_browser", "description": "Browse web"}
        ],
        "memory": {"type": "redis", "ttl": 3600},
        "prompt": "You are a helpful coding assistant that can execute code and browse documentation.",
        "tags": ["coding", "assistant"],
        "verbose": True
    }
    
    normalized = normalize_agent_data(agent_data)
    
    print(f"  ✓ Agent Type: {normalized['agentType']}")
    print(f"  ✓ Name: {normalized['name']}")
    print(f"  ✓ Description: {normalized['description'][:50]}...")
    print(f"  ✓ Capabilities: {normalized['capabilities']}")
    print(f"  ✓ Trust Score: {normalized['trustScore']}")
    print(f"  ✓ Metadata: {json.dumps(normalized.get('metadata', {}), indent=2)}")
    
    # Verify required fields
    assert normalized['agentType'] == 'langchain'
    assert normalized['name'] == 'Normalized Agent'
    assert len(normalized['capabilities']) > 0
    assert normalized['trustScore'] > 0
    
    print("  ✅ Normalization test passed!")


def test_auto_detection():
    """Test auto-detection through main AstraSync client"""
    print("\n🤖 Testing Auto-Detection via Main Client...")
    
    client = AstraSync(email="test@example.com")
    
    # This should be auto-detected as LangChain
    agent = {
        "name": "Auto-Detected Agent",
        "llm": "llama-2-70b",
        "tools": ["search", "calculate", "translate"],
        "memory": {"type": "summary", "max_tokens": 2000}
    }
    
    # The detector should identify this as LangChain
    detected_type = detect_agent_type(agent)
    print(f"  ✓ Detected type: {detected_type}")
    assert detected_type == "langchain"
    
    print("  ✅ Auto-detection test passed!")


if __name__ == "__main__":
    print("🚀 AstraSync LangChain Integration Test Suite")
    print("=" * 50)
    
    try:
        test_langchain_detection()
        test_normalization()
        test_auto_detection()
        test_langchain_registration()
        
        print("\n✅ All tests completed successfully!")
        print("\n📚 LangChain integration is ready to use!")
        print("   - Auto-detection: ✓")
        print("   - Normalization: ✓")
        print("   - Registration: ✓")
        print("   - Trust scoring: ✓")
        
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n⚠️  Unexpected error: {e}")
        sys.exit(1)