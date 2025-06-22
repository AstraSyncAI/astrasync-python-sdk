"""
AstraSync validation utilities
"""
import re
from typing import Dict, Any


def validate_email(email: str) -> bool:
    """Validate email format
    
    Args:
        email: Email address to validate
        
    Returns:
        True if valid email format
    """
    if not email or not isinstance(email, str):
        return False
    
    # Basic email regex pattern
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def validate_agent_data(agent_data: Dict[str, Any]) -> bool:
    """Validate agent data structure
    
    Args:
        agent_data: Agent data to validate
        
    Returns:
        True if valid structure
    """
    if not isinstance(agent_data, dict):
        return False
    
    # At minimum, agent should have name
    if 'name' not in agent_data:
        return False
    
    return True


def validate_agent_id(agent_id: str) -> bool:
    """Validate agent ID format
    
    Args:
        agent_id: Agent ID to validate
        
    Returns:
        True if valid format
    """
    if not agent_id or not isinstance(agent_id, str):
        return False
    
    # Check for TEMP- prefix (preview) or ASTRAS- prefix (production)
    if not (agent_id.startswith('TEMP-') or agent_id.startswith('ASTRAS-')):
        return False
    
    return True
