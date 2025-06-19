from typing import Dict, Any

def detect_agent_type(agent_data: Dict[str, Any]) -> str:
    """Auto-detect agent type based on structure"""
    # MCP agents
    if (agent_data.get('protocol') == 'ai-agent' and
        'skills' in agent_data and
        isinstance(agent_data['skills'], list)):
        return 'mcp'
    
    # Letta agents
    if (agent_data.get('type') == 'agent' and
        'memory' in agent_data and
        isinstance(agent_data['memory'], dict)):
        return 'letta'
    
    # ACP agents (IBM)
    if ('agentId' in agent_data and
        'authentication' in agent_data and
        isinstance(agent_data['authentication'], dict)):
        return 'acp'
    
    # OpenAI agents
    if ('model' in agent_data and
        'instructions' in agent_data and
        isinstance(agent_data.get('tools'), list)):
        return 'openai'
    
    # AutoGPT agents
    if ('ai_name' in agent_data and
        'ai_role' in agent_data and
        'ai_goals' in agent_data):
        return 'autogpt'
    
    # Salesforce Agentforce patterns
    if agent_data.get('agent_type') in ['External', 'Internal'] and \
       agent_data.get('agent_template_type') == 'EinsteinServiceAgent':
        return 'agentforce'
    
    # Agentforce with topics/actions structure
    if 'topics' in agent_data and isinstance(agent_data.get('system_messages'), list):
        return 'agentforce'
    
    # Agentforce SDK object detection
    if hasattr(agent_data, '__class__') and \
       'agentforce' in str(agent_data.__class__.__module__).lower():
        return 'agentforce-sdk'
    
    return 'generic'

def normalize_agent_data(agent_data: Dict[str, Any], agent_type: str) -> Dict[str, Any]:
    """Normalize agent data to standard format"""
    normalized = {
        'type': agent_type,
        'metadata': {}
    }
    
    if agent_type == 'mcp':
        normalized.update({
            'name': agent_data.get('name', 'Unnamed MCP Agent'),
            'description': agent_data.get('description', ''),
            'owner': agent_data.get('owner', 'Unknown'),
            'capabilities': [
                skill.get('id', skill.get('name', '')) if isinstance(skill, dict) else skill
                for skill in agent_data.get('skills', [])
            ],
            'version': agent_data.get('version', '1.0.0')
        })
    
    elif agent_type == 'openai':
        normalized.update({
            'name': agent_data.get('name', 'Unnamed OpenAI Agent'),
            'description': agent_data.get('instructions', '')[:200],
            'owner': agent_data.get('owner', 'Unknown'),
            'capabilities': [skill.get('id', skill.get('name', ''))
                           for skill in agent_data.get('skills', [])],
            'version': agent_data.get('version', '1.0.0')
        })
    
    elif agent_type == 'letta':
        normalized.update({
            'name': agent_data.get('name', 'Unnamed Letta Agent'),
            'description': agent_data.get('description', ''),
            'owner': agent_data.get('owner', 'Unknown'),
            'capabilities': agent_data.get('tools', []),
            'version': agent_data.get('version', '1.0.0'),
            'metadata': {
                'memory_type': agent_data.get('memory', {}).get('type', 'unknown')
            }
        })
    
    elif agent_type == 'acp':
        normalized.update({
            'name': agent_data.get('name', 'Unnamed ACP Agent'),
            'description': agent_data.get('description', ''),
            'owner': agent_data.get('owner', 'Unknown'),
            'capabilities': agent_data.get('capabilities', []),
            'version': agent_data.get('version', '1.0.0'),
            'metadata': {
                'agentId': agent_data.get('agentId', '')
            }
        })
    
    elif agent_type == 'autogpt':
        normalized.update({
            'name': agent_data.get('ai_name', 'Unnamed AutoGPT'),
            'description': agent_data.get('ai_role', ''),
            'owner': agent_data.get('owner', 'Unknown'),
            'capabilities': agent_data.get('ai_goals', []),
            'version': agent_data.get('version', '1.0.0')
        })
    
    else:
        # Generic/unknown agent type
        normalized.update({
            'name': agent_data.get('name', 'Unnamed Agent'),
            'description': agent_data.get('description', ''),
            'owner': agent_data.get('owner', 'Unknown'),
            'capabilities': agent_data.get('capabilities', []),
            'version': agent_data.get('version', '1.0.0')
        })
    
    return normalized
