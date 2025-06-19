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
            'capabilities': [skill.get('id', skill.get('name', '')) 
                           for skill in agent_data.get('skills', [])],
            'version': agent_data.get('version', '1.0.0')
        })
    
    elif agent_type == 'openai':
        normalized.update({
            'name': agent_data.get('name', 'Unnamed OpenAI Agent'),
            'description': agent_data.get('instructions', '')[:200],
            'owner': 'OpenAI Platform',
            'capabilities': [tool.get('type', '') 
                           for tool in agent_data.get('tools', [])],
            'metadata': {
                'model': agent_data.get('model', ''),
                'temperature': agent_data.get('temperature', 0.7)
            }
        })
    
    else:
        # Generic handling
        normalized.update({
            'name': (agent_data.get('name') or 
                    agent_data.get('agent_name') or 
                    'Unnamed Agent'),
            'description': (agent_data.get('description') or 
                          agent_data.get('agent_description') or ''),
            'owner': (agent_data.get('owner') or 
                     agent_data.get('agent_owner') or 
                     'Unknown'),
            'capabilities': agent_data.get('capabilities', [])
        })
    
    return normalized
