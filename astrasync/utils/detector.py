from typing import Dict, Any

def detect_agent_type(agent_data: Dict[str, Any]) -> str:
    """Auto-detect agent type based on structure"""
    
    # Google ADK agents - check FIRST before OpenAI
    # Dictionary format with schemas
    if ('input_schema' in agent_data and 'output_schema' in agent_data):
        return 'google-adk'
    
    # Agent type field specific to ADK
    if (agent_data.get('agent_type') in ['llm', 'sequential', 'parallel', 'loop'] and
        ('runner' in agent_data or 'session_service' in agent_data)):
        return 'google-adk'
    
    # Object instances
    if hasattr(agent_data, '__class__'):
        class_name = agent_data.__class__.__name__
        module_name = getattr(agent_data.__class__, '__module__', '')
        
        # Check for ADK agent classes
        if class_name in ['Agent', 'LlmAgent', 'BaseAgent', 'SequentialAgent', 
                         'ParallelAgent', 'LoopAgent']:
            if 'google.adk' in module_name or 'vertexai' in module_name:
                return 'google-adk'
    
    # Serialized format
    if isinstance(agent_data, dict) and 'config' in agent_data:
        config = agent_data.get('config', {})
        if 'agent_class' in config and 'google.adk' in str(config.get('agent_class')):
            return 'google-adk'
    
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
    
    # OpenAI agents - check AFTER Google ADK
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


def normalize_agent_data(agent_data: Dict[str, Any], agent_type: str = None) -> Dict[str, Any]:
    """Normalize agent data to common format"""
    
    if not agent_type:
        agent_type = detect_agent_type(agent_data)
    
    normalized = {
        'agentType': agent_type,
        'version': '1.0.0'  # Default version
    }
    
    # MCP normalization
    if agent_type == 'mcp':
        normalized['name'] = agent_data.get('name', 'MCP Agent')
        normalized['description'] = agent_data.get('description', '')
        normalized['capabilities'] = [skill.get('name', '') for skill in agent_data.get('skills', [])]
    
    # Letta normalization
    elif agent_type == 'letta':
        normalized['name'] = agent_data.get('name', 'Letta Agent')
        normalized['description'] = agent_data.get('description', '')
        normalized['capabilities'] = ['memory_management', 'conversation']
    
    # ACP normalization
    elif agent_type == 'acp':
        normalized['name'] = agent_data.get('name', agent_data.get('agentId', 'ACP Agent'))
        normalized['description'] = agent_data.get('description', '')
        normalized['capabilities'] = list(agent_data.get('capabilities', {}).keys())
    
    # OpenAI normalization
    elif agent_type == 'openai':
        normalized['name'] = agent_data.get('name', 'OpenAI Assistant')
        normalized['description'] = agent_data.get('instructions', '')[:200]
        # Handle tools that might be strings or dicts
        tools = agent_data.get('tools', [])
        normalized['capabilities'] = []
        for tool in tools:
            if isinstance(tool, dict):
                normalized['capabilities'].append(tool.get('type', ''))
            else:
                normalized['capabilities'].append(str(tool))
        normalized['model'] = agent_data.get('model', '')
    
    # AutoGPT normalization
    elif agent_type == 'autogpt':
        normalized['name'] = agent_data.get('ai_name', 'AutoGPT Agent')
        normalized['description'] = agent_data.get('ai_role', '')
        normalized['capabilities'] = agent_data.get('ai_goals', [])
    
    # Google ADK normalization
    elif agent_type == 'google-adk':
        # Handle dictionary configurations FIRST
        if isinstance(agent_data, dict):
            normalized['name'] = (
                agent_data.get('name') or 
                agent_data.get('id') or 
                'Google ADK Agent'
            )
            
            normalized['description'] = (
                agent_data.get('description') or
                agent_data.get('instructions', '')[:200] or
                'Multi-agent orchestration powered by Google ADK'
            )
            
            # Extract capabilities from tools
            tools = agent_data.get('tools', [])
            if tools:
                normalized['capabilities'] = [
                    t.get('name', 'tool') if isinstance(t, dict) else str(t)
                    for t in tools
                ]
            else:
                normalized['capabilities'] = []
            
            # Add orchestration capabilities for workflow agents
            agent_subtype = agent_data.get('agent_type', '').lower()
            if agent_subtype in ['sequential', 'parallel', 'loop']:
                normalized['capabilities'].extend([
                    f"{agent_subtype}_orchestration",
                    "multi_agent_coordination"
                ])
            
            # Include model if specified
            if 'model' in agent_data:
                normalized['model'] = agent_data['model']
        
        # Handle direct agent instances (objects)
        else:
            normalized['name'] = getattr(agent_data, 'name', 
                                       getattr(agent_data, '__name__', 
                                             agent_data.__class__.__name__))
            
            # Get description from docstring or instructions
            normalized['description'] = (
                getattr(agent_data, 'description', '') or
                getattr(agent_data, '__doc__', '') or
                getattr(agent_data, 'instructions', '')[:200] + '...' 
                if hasattr(agent_data, 'instructions') else
                f"Google ADK {agent_data.__class__.__name__} Agent"
            )
            
            # Extract tools/capabilities
            tools = getattr(agent_data, 'tools', [])
            if tools:
                normalized['capabilities'] = [
                    tool.name if hasattr(tool, 'name') else str(tool)
                    for tool in tools
                ]
            else:
                normalized['capabilities'] = [agent_data.__class__.__name__.lower()]
            
            # Get model information if available
            if hasattr(agent_data, 'model'):
                normalized['model'] = str(getattr(agent_data, 'model'))
        
        # ADK-specific metadata (applies to both dicts and objects)
        normalized['framework'] = 'google-adk'
        normalized['orchestration_capable'] = True
        
        # Add compliance-relevant ADK features
        if hasattr(agent_data, 'output_schema') or (isinstance(agent_data, dict) and 'output_schema' in agent_data):
            normalized['structured_output'] = True
            if 'deterministic_output' not in normalized.get('capabilities', []):
                normalized['capabilities'] = normalized.get('capabilities', []) + ['deterministic_output']
    
    # Agentforce normalization
    elif agent_type in ['agentforce', 'agentforce-sdk']:
        normalized['name'] = agent_data.get('label', agent_data.get('name', 'Agentforce Agent'))
        normalized['description'] = agent_data.get('description', 'Salesforce Agentforce agent')
        if 'topics' in agent_data:
            normalized['capabilities'] = [topic.get('label', 'topic') for topic in agent_data.get('topics', [])]
        else:
            normalized['capabilities'] = ['salesforce_integration']
    
    # Generic fallback
    else:
        normalized['name'] = agent_data.get('name', 'Generic Agent')
        normalized['description'] = agent_data.get('description', '')
        normalized['capabilities'] = agent_data.get('capabilities', [])
    
    # Common fields
    normalized['owner'] = agent_data.get('owner', '')
    normalized['version'] = agent_data.get('version', normalized.get('version', '1.0.0'))
    
    return normalized
