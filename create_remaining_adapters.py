#!/usr/bin/env python3
"""
Script to create the remaining adapter files for AstraSync
"""

import os

adapters = [
    {
        "filename": "babyagi.py",
        "agent_type": "babyagi",
        "display_name": "BabyAGI",
        "description": "Autonomous task management AI system",
        "module_patterns": ["babyagi", "baby_agi"],
        "class_patterns": ["BabyAGI", "TaskAgent"],
        "dict_fields": ["objective", "task_list", "task", "tasks"],
        "capabilities": ["task_management", "autonomous_execution", "memory"],
        "special_features": {
            "task_creation": "Task creation and prioritization",
            "vectorstore": "Vector database for memory",
            "execution_chain": "Task execution chain"
        }
    },
    {
        "filename": "superagi.py",
        "agent_type": "superagi",
        "display_name": "SuperAGI",
        "description": "Enterprise autonomous agent framework",
        "module_patterns": ["superagi", "super_agi"],
        "class_patterns": ["SuperAGI", "Agent", "Workflow"],
        "dict_fields": ["agent_config", "tools", "goals", "instructions", "workflows"],
        "capabilities": ["workflows", "toolkits", "memory", "telemetry"],
        "special_features": {
            "agent_workflows": "Predefined workflow execution",
            "performance_telemetry": "Performance monitoring",
            "token_optimization": "Cost management"
        }
    },
    {
        "filename": "mistral_agents.py",
        "agent_type": "mistral_agents",
        "display_name": "Mistral Agents",
        "description": "Mistral AI agent framework (Le Chat)",
        "module_patterns": ["mistral", "lechat"],
        "class_patterns": ["MistralAgent", "LeChat"],
        "dict_fields": ["model", "functions", "tools", "system_prompt"],
        "capabilities": ["function_calling", "streaming", "json_mode"],
        "special_features": {
            "function_calling": "Native function calling",
            "json_mode": "Structured JSON outputs",
            "safe_mode": "Safety filtering"
        }
    },
    {
        "filename": "vertex_ai.py",
        "agent_type": "vertex_ai",
        "display_name": "Vertex AI Agent Builder",
        "description": "Google Cloud Vertex AI agents",
        "module_patterns": ["vertexai", "vertex_ai", "google.cloud"],
        "class_patterns": ["VertexAgent", "Agent", "AgentBuilder"],
        "dict_fields": ["agent_name", "display_name", "goal", "tools", "datastores"],
        "capabilities": ["grounding", "datastores", "extensions", "playbooks"],
        "special_features": {
            "grounding": "Fact grounding with search",
            "datastores": "Custom data integration",
            "playbooks": "Conversation flows"
        }
    },
    {
        "filename": "bedrock_agents.py",
        "agent_type": "bedrock_agents",
        "display_name": "Amazon Bedrock Agents",
        "description": "AWS Bedrock managed AI agents",
        "module_patterns": ["bedrock", "boto3", "aws"],
        "class_patterns": ["BedrockAgent", "Agent"],
        "dict_fields": ["agent_name", "instruction", "foundation_model", "action_groups"],
        "capabilities": ["action_groups", "knowledge_bases", "guardrails"],
        "special_features": {
            "action_groups": "API integrations",
            "knowledge_bases": "RAG capabilities",
            "guardrails": "Content filtering"
        }
    },
    {
        "filename": "dify.py",
        "agent_type": "dify",
        "display_name": "Dify",
        "description": "Visual AI workflow builder",
        "module_patterns": ["dify"],
        "class_patterns": ["DifyAgent", "Workflow", "App"],
        "dict_fields": ["app_config", "workflow", "nodes", "tools", "model_config"],
        "capabilities": ["visual_workflow", "no_code", "plugins", "datasets"],
        "special_features": {
            "visual_builder": "Drag-and-drop workflow creation",
            "app_templates": "Pre-built templates",
            "dataset_management": "Built-in data handling"
        }
    }
]

template = '''"""
{display_name} adapter for AstraSync agent registration.
Supports {display_name} agents and configurations.
"""

import logging
from typing import Dict, Any, List, Optional, Union
from ..utils.trust_score import calculate_trust_score
from ..core import AstraSync

logger = logging.getLogger(__name__)


def normalize_agent_data(agent_data: Any) -> Dict[str, Any]:
    """
    Normalize {display_name} agent data to AstraSync standard format.
    
    Supports:
    - {display_name} agents and configurations
    - {special_feature_list}
    """
    # Start with empty normalized structure
    normalized = {{
        'agentType': '{agent_type}',
        'version': '1.0',
        'capabilities': [],
        'metadata': {{}}
    }}
    
    # Handle {display_name} agent objects
    if hasattr(agent_data, '__class__'):
        class_name = agent_data.__class__.__name__
        module_name = getattr(agent_data.__class__, '__module__', '')
        
        if {module_check}:
            normalized['name'] = getattr(agent_data, 'name', f'{{class_name}} Instance')
            normalized['metadata']['agentClass'] = class_name
            
            # Check for specific class types
            if {class_check}:
                normalized['description'] = getattr(agent_data, 'description', '{description}')
                normalized['capabilities'].append('{primary_capability}:enabled')
                
            # Extract configuration
            if hasattr(agent_data, 'config'):
                config = agent_data.config
                if isinstance(config, dict):
                    normalized['metadata']['config'] = config
                    
    # Handle dictionary-based definitions
    elif isinstance(agent_data, dict):
        # Direct field mappings
        for field in ['name', 'description', 'owner', 'version']:
            if field in agent_data:
                normalized[field] = agent_data[field]
                
        # {display_name}-specific fields
{dict_field_checks}
        
    # Ensure capabilities are unique
    normalized['capabilities'] = list(set(normalized['capabilities']))
    
    # Set defaults for missing required fields
    if 'name' not in normalized:
        normalized['name'] = 'Unnamed {display_name} Agent'
    if 'description' not in normalized:
        normalized['description'] = '{description}'
    if 'owner' not in normalized:
        normalized['owner'] = 'Unknown'
    if 'version' not in normalized:
        normalized['version'] = '1.0'
    
    # Calculate trust score with {display_name}-specific bonuses
    trust_score = calculate_trust_score(normalized)
    
    # {display_name}-specific trust score bonuses
    if normalized['capabilities']:
        trust_score += min(5, len(normalized['capabilities']))
{trust_score_bonuses}
        
    normalized['trustScore'] = min(trust_score, 95)  # Cap at 95 for preview
    
    return normalized


def register_{agent_type}(agent: Any, email: str, owner: Optional[str] = None) -> Dict[str, Any]:
    """
    Register a {display_name} agent with AstraSync.
    
    Args:
        agent: {display_name} agent object or configuration
        email: Developer email for registration
        owner: Optional owner name (defaults to email domain)
        
    Returns:
        Registration response with agent ID and trust score
    """
    try:
        client = AstraSync(email=email)
        normalized_data = normalize_agent_data(agent)
        
        if owner:
            normalized_data['owner'] = owner
            
        return client.register(normalized_data, owner=owner)
    except Exception as e:
        logger.error(f"Failed to register {display_name} agent: {{e}}")
        raise


def create_registration_decorator(email: str, owner: Optional[str] = None):
    """
    Create a decorator for automatic {display_name} agent registration.
    
    Usage:
        @register_with_astrasync(email="dev@example.com")
        class My{display_name}Agent:
            ...
    """
    def decorator(cls):
        original_init = cls.__init__
        
        def new_init(self, *args, **kwargs):
            original_init(self, *args, **kwargs)
            try:
                result = register_{agent_type}(self, email=email, owner=owner)
                self.astrasync_id = result.get('agentId')
                self.astrasync_trust_score = result.get('trustScore')
                logger.info(f"Auto-registered {display_name} agent: {{self.astrasync_id}}")
            except Exception as e:
                logger.warning(f"Failed to auto-register agent: {{e}}")
                self.astrasync_id = None
                self.astrasync_trust_score = None
                
        cls.__init__ = new_init
        return cls
        
    return decorator


# Convenience function alias
register_with_astrasync = create_registration_decorator'''

def generate_adapter(adapter_info):
    # Generate module check
    module_checks = []
    for pattern in adapter_info["module_patterns"]:
        module_checks.append(f"'{pattern}' in module_name.lower()")
    module_check = " or ".join(module_checks)
    
    # Generate class check
    class_checks = []
    for pattern in adapter_info["class_patterns"]:
        class_checks.append(f"'{pattern}' in class_name")
    class_check = " or ".join(class_checks)
    
    # Generate dict field checks
    dict_checks = []
    for field in adapter_info["dict_fields"]:
        check = f"""        if '{field}' in agent_data:
            {field}_config = agent_data['{field}']
            if isinstance({field}_config, dict):
                normalized['metadata']['{field}'] = {field}_config
            elif isinstance({field}_config, list):
                normalized['metadata']['{field}Count'] = len({field}_config)
                normalized['capabilities'].append(f'{field}:{{len({field}_config)}}')
            else:
                normalized['metadata']['{field}'] = {field}_config"""
        dict_checks.append(check)
    dict_field_checks = "\n".join(dict_checks)
    
    # Generate special feature list
    feature_list = []
    for key, desc in adapter_info["special_features"].items():
        feature_list.append(f"{desc}")
    special_feature_list = "\n    - ".join(feature_list)
    
    # Generate trust score bonuses
    bonuses = []
    for capability in adapter_info["capabilities"]:
        bonuses.append(f"""    if '{capability}:enabled' in normalized['capabilities']:
        trust_score += 5""")
    trust_score_bonuses = "\n".join(bonuses)
    
    # Fill in the template
    content = template.format(
        display_name=adapter_info["display_name"],
        agent_type=adapter_info["agent_type"],
        description=adapter_info["description"],
        module_check=module_check,
        class_check=class_check,
        primary_capability=adapter_info["capabilities"][0],
        dict_field_checks=dict_field_checks,
        special_feature_list=special_feature_list,
        trust_score_bonuses=trust_score_bonuses
    )
    
    return content

# Generate all adapter files
adapters_dir = "astrasync/adapters"
for adapter in adapters:
    filepath = os.path.join(adapters_dir, adapter["filename"])
    content = generate_adapter(adapter)
    with open(filepath, 'w') as f:
        f.write(content)
    print(f"Created {filepath}")

print("\nAll adapter files created successfully!")