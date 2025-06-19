import os
import json
from typing import Dict, Any, Optional, Union
from pathlib import Path

from .utils.api import APIClient
from .utils.detector import detect_agent_type, normalize_agent_data
from .utils.trust_score import calculate_trust_score
from .exceptions import ValidationError

class AstraSync:
    """AstraSync AI Agent Registration Client"""
    
    def __init__(self, email: Optional[str] = None, api_url: Optional[str] = None):
        self.email = email or os.getenv('ASTRASYNC_EMAIL')
        self.api_url = api_url or os.getenv(
            'ASTRASYNC_API_URL', 
            'https://astrasync-api-production.up.railway.app'
        )
        self.api_client = APIClient(self.api_url)
        
    def register(self, agent: Union[Dict[str, Any], str, Path]) -> Dict[str, Any]:
        """Register an AI agent with auto-detection"""
        agent_data = self._parse_agent_input(agent)
        agent_type = detect_agent_type(agent_data)
        normalized = normalize_agent_data(agent_data, agent_type)
        
        email = normalized.get('owner_email') or self.email
        if not email:
            raise ValidationError(
                "Email required. Set via constructor, ASTRASYNC_EMAIL env var, "
                "or include in agent data"
            )
            
        trust_score = calculate_trust_score(normalized)
        
        payload = {
            "email": email,
            "agent": {
                "name": normalized['name'],
                "description": normalized['description'],
                "owner": normalized['owner'],
                "capabilities": normalized.get('capabilities', []),
                "version": normalized.get('version', '1.0.0'),
                "agentType": agent_type,
                "trustScore": trust_score,
                **normalized.get('metadata', {})
            }
        }
        
        return self.api_client.register(payload)
    
    def verify(self, agent_id: str) -> Dict[str, Any]:
        """Verify if an agent is registered"""
        return self.api_client.verify(agent_id)
    
    def _parse_agent_input(self, agent: Union[Dict, str, Path]) -> Dict:
        """Parse various input formats"""
        if isinstance(agent, dict):
            return agent
        elif isinstance(agent, (str, Path)):
            path = Path(agent)
            if path.exists():
                with open(path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                try:
                    return json.loads(agent)
                except json.JSONDecodeError:
                    raise ValidationError(f"Invalid input: {agent}")
        else:
            raise ValidationError(f"Unsupported agent input type: {type(agent)}")
