""""
Salesforce Agentforce adapter for AstraSync
Enables automatic registration of Agentforce agents with blockchain identity
"""

from typing import Dict, Any, Optional, List
import json
from ..core import AstraSync
from ..utils.trust_score import calculate_trust_score

class AgentforceAdapter:
    """Adapter for Salesforce Agentforce agents"""
    
    @staticmethod
    def normalize_agent_data(agentforce_data: Any) -> Dict[str, Any]:
        """Convert Agentforce agent format to AstraSync format"""
        
        # Handle different input types
        if hasattr(agentforce_data, 'to_dict'):
            data = agentforce_data.to_dict()
        elif hasattr(agentforce_data, 'to_json'):
            data = json.loads(agentforce_data.to_json())
        elif isinstance(agentforce_data, dict):
            data = agentforce_data
        else:
            data = {'raw': str(agentforce_data)}
        
        # Extract core fields
        normalized = {
            'name': data.get('name', 'Unnamed Agentforce Agent'),
            'description': data.get('description', ''),
            'owner': data.get('company_name', 'Unknown'),
            'version': '1.0',  # Agentforce doesn't version agents
            'agentType': 'agentforce',
            'capabilities': [],
            'metadata': {
                'platform': 'salesforce',
                'agent_type': data.get('agent_type', 'External'),
                'template_type': data.get('agent_template_type', 'EinsteinServiceAgent'),
                'domain': data.get('domain', 'General'),
                'sample_utterances': data.get('sample_utterances', []),
                'variables': data.get('variables', []),
                'system_messages': data.get('system_messages', []),
                'topics': data.get('topics', [])
            }
        }
        
        # Build capabilities from various sources
        capabilities = []
        
        # Add topics as capabilities
        if data.get('topics'):
            capabilities.extend([f"topic:{topic}" for topic in data.get('topics', [])])
        
        # Add actions if present
        if data.get('actions'):
            for action in data.get('actions', []):
                if isinstance(action, dict):
                    capabilities.append(f"action:{action.get('name', 'unknown')}")
                else:
                    capabilities.append(f"action:{action}")
        
        # Add domain as capability
        if data.get('domain'):
            capabilities.append(f"domain:{data['domain']}")
        
        # Add template type as capability
        if data.get('agent_template_type'):
            capabilities.append(f"template:{data['agent_template_type']}")
        
        normalized['capabilities'] = capabilities
        
        # Calculate trust score with Agentforce-specific factors
        base_score = calculate_trust_score(normalized)
        
        # Boost for enterprise features
        if data.get('company_name') and data['company_name'] != 'Unknown':
            base_score += 5  # Verified company
        
        if data.get('agent_type') == 'Internal':
            base_score += 3  # Internal agents are more controlled
        
        if len(data.get('system_messages', [])) > 0:
            base_score += 2  # Has system instructions
        
        if len(data.get('variables', [])) > 0:
            base_score += 2  # Has defined variables
        
        normalized['trustScore'] = min(base_score, 95)
        
        return normalized

    @staticmethod
    def extract_from_sdk_agent(agent_obj) -> Dict[str, Any]:
        """Extract data from Agentforce SDK agent object"""
        # This handles the programmatic agent creation pattern
        data = {
            'name': getattr(agent_obj, 'name', 'SDK Agent'),
            'description': getattr(agent_obj, 'description', ''),
            'agent_type': getattr(agent_obj, 'agent_type', 'External'),
            'agent_template_type': getattr(agent_obj, 'agent_template_type', 'EinsteinServiceAgent'),
            'company_name': getattr(agent_obj, 'company_name', 'Unknown'),
            'domain': getattr(agent_obj, 'domain', 'General')
        }
        
        # Extract collections
        for attr in ['topics', 'actions', 'variables', 'system_messages', 'sample_utterances']:
            if hasattr(agent_obj, attr):
                value = getattr(agent_obj, attr)
                if hasattr(value, '__iter__'):
                    data[attr] = list(value)
                else:
                    data[attr] = value
        
        return data
    
    @classmethod
    def create_registration_decorator(cls, email: str):
        """Decorator for Agentforce SDK agents"""
        def decorator(agent_class):
            # Store original init
            original_init = getattr(agent_class, '__init__', None)
            
            def new_init(self, *args, **kwargs):
                # Try to call original init
                if original_init:
                    try:
                        original_init(self, *args, **kwargs)
                    except Exception as e:
                        # If Agentforce SDK requires specific init params, skip registration
                        print(f"Note: Agentforce SDK initialization requires specific parameters")
                        print(f"      Auto-registration skipped. Use register_agentforce() directly.")
                        return
                
                # Only register if we have required attributes
                if not hasattr(self, 'name'):
                    print("Warning: Agent missing 'name' attribute, skipping registration")
                    return
                
                try:
                    # Extract data from the agent
                    if hasattr(self, 'to_dict'):
                        agent_data = self.to_dict()
                    else:
                        agent_data = cls.extract_from_sdk_agent(self)
                    
                    # Register with AstraSync
                    client = AstraSync(email=email)
                    normalized = cls.normalize_agent_data(agent_data)
                    result = client.register(normalized)
                    
                    # Attach the ID to the agent
                    self.astrasync_id = result['agentId']
                    self.astrasync_trust_score = result['trustScore']
                    
                    print(f"✅ Registered {self.name} with AstraSync: {self.astrasync_id}")
                    print(f"   Trust Score: {self.astrasync_trust_score}")
                    
                except Exception as e:
                    print(f"Warning: Could not auto-register agent: {str(e)}")
                    print(f"         Use register_agentforce() directly for manual registration")
            
            agent_class.__init__ = new_init
            return agent_class
        
        return decorator


# Convenience functions
def register_agentforce(agent_data: Any, email: str) -> Dict[str, Any]:
    """Register an Agentforce agent with AstraSync"""
    adapter = AgentforceAdapter()
    
    # Handle SDK objects
    if hasattr(agent_data, '__class__') and 'agent' in str(agent_data.__class__.__name__).lower():
        agent_data = adapter.extract_from_sdk_agent(agent_data)
    
    normalized = adapter.normalize_agent_data(agent_data)
    
    client = AstraSync(email=email)
    return client.register(normalized)


def register_agentforce_deployment(deployment_result: Dict[str, Any], email: str) -> Dict[str, Any]:
    """Register an Agentforce agent after deployment"""
    # Extract agent data from deployment result
    agent_data = deployment_result.get('agent', deployment_result)
    
    result = register_agentforce(agent_data, email)
    
    # Add deployment info to result
    result['deployment_id'] = deployment_result.get('id', 'N/A')
    result['deployment_status'] = deployment_result.get('deployResult', {}).get('status', 'Unknown')
    
    return result
