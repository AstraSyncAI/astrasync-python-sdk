from typing import Dict, Any

def calculate_trust_score(agent_data: Dict[str, Any]) -> int:
    """Calculate trust score based on agent metadata completeness"""
    score = 70  # Base score
    
    # Name quality
    if agent_data.get('name') and agent_data['name'] != 'Unnamed Agent':
        score += 5
    
    # Description quality
    desc = agent_data.get('description', '')
    if len(desc) > 50:
        score += 5
    if len(desc) > 100:
        score += 5
    
    # Capabilities
    capabilities = agent_data.get('capabilities', [])
    if len(capabilities) > 0:
        score += 5
    if len(capabilities) > 3:
        score += 5
    
    # Version info
    if agent_data.get('version'):
        score += 5
    
    return min(score, 95)  # Cap at 95 for preview
