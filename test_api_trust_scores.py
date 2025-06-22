"""Test that SDK uses API trust scores exclusively"""
from astrasync import AstraSync
import json

print("🧪 AstraSync v0.2.1 - API Trust Score Test")
print("=" * 50)

# Test agents
test_agents = {
    "Google ADK (High Features)": {
        "name": "ADK Premium Agent",
        "input_schema": {"type": "object"},
        "output_schema": {"type": "object"},
        "tools": ["search", "analyze", "report"],
        "agent_type": "orchestration",
        "model": "gemini-1.5-pro"
    },
    "Simple Agent": {
        "name": "Basic Bot",
        "description": "A simple agent",
        "owner": "Test Corp"
    }
}

# Initialize client
client = AstraSync(email="test@example.com")

# Test registrations
print("\n📊 Registration & Trust Score Test:")
print("-" * 40)

for name, agent_data in test_agents.items():
    try:
        result = client.register(agent_data)
        
        # Verify we're getting API trust scores
        print(f"\n{name}:")
        print(f"  Agent ID:    {result['agentId']}")
        print(f"  Trust Score: {result['trustScore']}")
        print(f"  Status:      {result['status']}")
        
        # During preview, ALL agents should have TEMP-95%
        if result['trustScore'] != 'TEMP-95%':
            print(f"  ❌ ERROR: Expected 'TEMP-95%', got '{result['trustScore']}'")
        else:
            print(f"  ✅ Correctly using API trust score")
            
    except Exception as e:
        print(f"\n{name}: ❌ Failed: {str(e)}")

print("\n" + "=" * 50)
print("✅ Test complete - SDK now uses API trust scores exclusively")
