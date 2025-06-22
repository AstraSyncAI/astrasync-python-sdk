"""Debug the registration issue"""
from astrasync import AstraSync
from astrasync.utils.detector import detect_agent_type, normalize_agent_data
import json

# Test ADK agent that's failing
adk_agent = {
    "name": "Test ADK Agent",
    "instructions": "This is a test agent for validating Google ADK support in AstraSync",
    "model": "gemini-1.5-pro",
    "tools": ["search", "analyze"],
    "input_schema": {"type": "object"},
    "output_schema": {"type": "object"},
    "agent_type": "llm",
    "session_service": "managed"
}

print("1. Original agent data:")
print(json.dumps(adk_agent, indent=2))

# Test detection
agent_type = detect_agent_type(adk_agent)
print(f"\n2. Detected type: {agent_type}")

# Test normalization
normalized = normalize_agent_data(adk_agent, agent_type)
print("\n3. Normalized data:")
print(json.dumps(normalized, indent=2, default=str))

# Check for problematic fields
print("\n4. Checking for issues:")
print(f"   - 'owner' type: {type(normalized.get('owner'))}")
print(f"   - 'owner' value: {normalized.get('owner')}")
print(f"   - 'metadata' in normalized: {'metadata' in normalized}")
if 'metadata' in normalized:
    print(f"   - 'metadata' type: {type(normalized.get('metadata'))}")
    print(f"   - 'metadata' value: {normalized.get('metadata')}")

# Try to build the payload
try:
    client = AstraSync(email="test@example.com")
    email = "test@example.com"
    
    # Manually build payload to see where it fails
    payload = {
        "email": email,
        "agent": {
            "name": normalized['name'],
            "description": normalized['description'],
            "owner": normalized.get('owner', email),
            "capabilities": normalized.get('capabilities', []),
            "version": normalized.get('version', '1.0.0'),
            "agentType": agent_type,
            "trustScore": 85
        }
    }
    
    # Try adding metadata
    if 'metadata' in normalized:
        payload['agent'].update(normalized['metadata'])
    
    print("\n5. Built payload successfully:")
    print(json.dumps(payload, indent=2))
    
except Exception as e:
    print(f"\n5. Error building payload: {type(e).__name__}: {str(e)}")
    import traceback
    traceback.print_exc()
