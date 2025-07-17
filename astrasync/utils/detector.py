"""
Agent type detection and normalization utilities
"""
from typing import Dict, Any, Union


def detect_agent_type(agent_data: Union[Dict[str, Any], object]) -> str:
    """Detect the type of agent from its configuration
    
    Args:
        agent_data: Agent configuration (dict or object)
        
    Returns:
        Agent type string
    """
    # Handle object instances
    if not isinstance(agent_data, dict):
        # Check for direct ADK agent instances
        if hasattr(agent_data, '__class__'):
            class_name = agent_data.__class__.__name__
            module_name = getattr(agent_data.__class__, '__module__', '')
            
            if 'google.adk' in module_name or class_name in ['Agent', 'ADKAgent']:
                return 'google-adk'
            
            # Check for LangChain objects
            if 'langchain' in module_name.lower():
                return 'langchain'
            
            # Common LangChain class patterns
            if any(pattern in class_name for pattern in ['Agent', 'Chain', 'Executor']):
                if 'langchain' in str(type(agent_data)):
                    return 'langchain'
        
        # Convert to dict for further checks
        if hasattr(agent_data, '__dict__'):
            agent_data = agent_data.__dict__
        else:
            return 'unknown'
    
    # Check Google ADK patterns FIRST (before OpenAI)
    if ('input_schema' in agent_data and 'output_schema' in agent_data):
        return 'google-adk'
    
    if 'agent_type' in agent_data and agent_data['agent_type'] in ['llm', 'sequential', 'parallel', 'loop']:
        return 'google-adk'
    
    # Check for serialized ADK agents
    if 'config' in agent_data and isinstance(agent_data['config'], dict):
        config = agent_data['config']
        if any(key in config for key in ['google.adk', 'ADKAgent', 'agent_type']):
            return 'google-adk'
    
    # MCP (Model Context Protocol)
    if 'protocol' in agent_data and agent_data['protocol'] == 'ai-agent':
        return 'mcp'
    
    if 'skills' in agent_data and isinstance(agent_data.get('skills'), list):
        if all(isinstance(skill, dict) and 'name' in skill for skill in agent_data['skills']):
            return 'mcp'
    
    # Check for LangChain before Letta (both can have memory)
    # LangChain typically has llm + tools/memory combination
    if 'llm' in agent_data and ('tools' in agent_data or 'memory' in agent_data):
        # Additional check to ensure it's not another type
        if 'agent_type' in agent_data and agent_data.get('agent_type') not in ['External', 'llm', 'sequential', 'parallel', 'loop']:
            return 'langchain'
        elif 'agent_type' not in agent_data:
            return 'langchain'
    
    # Letta (MemGPT) - more specific check
    if 'memory' in agent_data and isinstance(agent_data.get('memory'), dict):
        # Letta-specific memory structure check
        if 'type' not in agent_data.get('memory', {}) or agent_data.get('type') == 'agent':
            return 'letta'
    
    if 'type' in agent_data and agent_data['type'] == 'agent' and 'memory' in agent_data:
        return 'letta'
    
    # IBM ACP (Agent Communication Protocol)
    if 'agentId' in agent_data and 'authentication' in agent_data:
        return 'acp'
    
    # OpenAI Assistants
    if ('model' in agent_data and 'instructions' in agent_data and 
        isinstance(agent_data.get('tools'), list)):
        return 'openai'
    
    # AutoGPT
    if all(key in agent_data for key in ['ai_name', 'ai_role', 'ai_goals']):
        return 'autogpt'
    
    # Agentforce
    if ('agent_type' in agent_data and agent_data['agent_type'] == 'External' and
        'agent_template_type' in agent_data):
        return 'agentforce'
    
    return 'unknown'


def normalize_agent_data(agent_data: Union[Dict[str, Any], object]) -> Dict[str, Any]:
    """Normalize agent data to a common format
    
    Args:
        agent_data: Agent configuration (dict or object)
        
    Returns:
        Normalized agent data dict
    """
    agent_type = detect_agent_type(agent_data)
    
    # Convert object to dict if needed
    if not isinstance(agent_data, dict):
        if hasattr(agent_data, '__dict__'):
            agent_data = agent_data.__dict__
        else:
            agent_data = {}
    
    # Base normalized structure
    normalized = {
        'agentType': agent_type,
        'version': agent_data.get('version', '1.0.0'),
        'name': '',
        'description': '',
        'capabilities': [],
        'owner': ''  # Will be set properly below
    }
    
    # Type-specific normalization
    if agent_type == 'mcp':
        normalized['name'] = agent_data.get('name', 'Unnamed MCP Agent')
        normalized['description'] = agent_data.get('description', 'MCP protocol agent')
        normalized['capabilities'] = [skill.get('name', '') for skill in agent_data.get('skills', [])]
        normalized['owner'] = agent_data.get('owner', agent_data.get('developer', ''))
    
    elif agent_type == 'letta':
        normalized['name'] = agent_data.get('name', 'Unnamed Letta Agent')
        normalized['description'] = agent_data.get('description', 'Memory-augmented agent')
        normalized['capabilities'] = ['memory', 'recall', 'persistent_context']
        normalized['owner'] = agent_data.get('owner', agent_data.get('creator', ''))
    
    elif agent_type == 'acp':
        normalized['name'] = agent_data.get('name', f"ACP Agent {agent_data.get('agentId', 'Unknown')}")
        normalized['description'] = agent_data.get('description', 'IBM Agent Communication Protocol agent')
        normalized['capabilities'] = list(agent_data.get('capabilities', {}).keys())
        normalized['owner'] = agent_data.get('owner', agent_data.get('organization', ''))
    
    elif agent_type == 'openai':
        normalized['name'] = agent_data.get('name', 'Unnamed OpenAI Assistant')
        normalized['description'] = agent_data.get('description', agent_data.get('instructions', 'OpenAI Assistant'))[:200]
        tools = agent_data.get('tools', [])
        normalized['capabilities'] = []
        for tool in tools:
            if isinstance(tool, dict):
                normalized['capabilities'].append(tool.get('type', ''))
            else:
                normalized['capabilities'].append(str(tool))
        normalized['owner'] = agent_data.get('owner', agent_data.get('created_by', ''))
    
    elif agent_type == 'autogpt':
        normalized['name'] = agent_data.get('ai_name', 'Unnamed AutoGPT Agent')
        normalized['description'] = agent_data.get('ai_role', 'AutoGPT autonomous agent')
        normalized['capabilities'] = agent_data.get('ai_goals', [])[:5]  # Limit to 5 goals
        normalized['owner'] = agent_data.get('owner', agent_data.get('user', ''))
    
    elif agent_type == 'google-adk':
        normalized['name'] = agent_data.get('name', 'Unnamed ADK Agent')
        normalized['description'] = agent_data.get('description', 'Multi-agent orchestration powered by Google ADK')
        
        # Extract capabilities from tools or features
        tools = agent_data.get('tools', [])
        normalized['capabilities'] = []
        for tool in tools:
            if isinstance(tool, dict):
                normalized['capabilities'].append(tool.get('type', tool.get('name', '')))
            else:
                normalized['capabilities'].append(str(tool))
        
        # Add ADK-specific capabilities
        if agent_data.get('output_schema') or agent_data.get('structured_output'):
            normalized['capabilities'].append('deterministic_output')
        
        # Add framework info
        normalized['framework'] = 'google-adk'
        normalized['orchestration_capable'] = agent_data.get('agent_type') in ['sequential', 'parallel', 'loop']
        normalized['structured_output'] = bool(agent_data.get('output_schema'))
        
        # FIX: Ensure owner is never empty for ADK agents
        normalized['owner'] = agent_data.get('owner', agent_data.get('developer', 'ADK Developer'))
    
    elif agent_type == 'agentforce':
        normalized['name'] = agent_data.get('label', 'Unnamed Agentforce Agent')
        normalized['description'] = agent_data.get('description', f"{agent_data.get('agent_template_type', 'Salesforce')} agent")
        topics = agent_data.get('topics', [])
        normalized['capabilities'] = [topic.get('label', '') for topic in topics if isinstance(topic, dict)]
        normalized['owner'] = agent_data.get('owner', agent_data.get('organization', 'Salesforce Org'))
    
    elif agent_type == 'langchain':
        # Import here to avoid circular dependency
        from ..adapters.langchain import normalize_agent_data as langchain_normalize
        return langchain_normalize(agent_data)
    
    else:
        # Unknown type - use generic extraction
        normalized['name'] = agent_data.get('name', agent_data.get('agent_name', 'Unnamed Agent'))
        normalized['description'] = agent_data.get('description', 'Unknown agent type')
        normalized['capabilities'] = agent_data.get('capabilities', agent_data.get('features', []))
        normalized['owner'] = agent_data.get('owner', agent_data.get('creator', ''))
    
    # Final validation - ensure no empty critical fields
    if not normalized['name']:
        normalized['name'] = f"Unnamed {agent_type} Agent"
    
    if not normalized['description']:
        normalized['description'] = f"A {agent_type} agent"
    
    # CRITICAL FIX: Never leave owner empty
    if not normalized['owner']:
        normalized['owner'] = 'Unknown'
    
    return normalized
