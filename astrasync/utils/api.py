import requests
import json
from typing import Dict, Any, Optional
from ..exceptions import APIError, RegistrationError

class APIClient:
    """
    Client for AstraSync API
    Matches the exact requirements from the deployed API
    """
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'User-Agent': 'AstraSync-Python-SDK/0.2.1',
            'x-source': 'python-sdk'  # Track SDK usage
        })
    
    def register(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Register an agent with AstraSync API
        
        CRITICAL: Returns 201 for success, not 200!
        """
        try:
            response = self.session.post(
                f"{self.base_url}/v1/register",
                json=payload,
                timeout=30
            )
            
            # Your API returns 201 for success
            if response.status_code == 201:
                return response.json()
            else:
                raise APIError(
                    f"Registration failed: {response.text}",
                    status_code=response.status_code,
                    response_body=response.text
                )
                
        except requests.exceptions.RequestException as e:
            raise RegistrationError(f"Network error: {str(e)}")
    
    def verify(self, agent_id: str) -> Dict[str, Any]:
        """Verify if an agent exists"""
        try:
            response = self.session.get(
                f"{self.base_url}/v1/verify/{agent_id}",
                timeout=10
            )
            
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 404:
                return {"exists": False, "agentId": agent_id}
            else:
                raise APIError(
                    f"Verification failed: {response.text}",
                    status_code=response.status_code
                )
                
        except requests.exceptions.RequestException as e:
            raise APIError(f"Network error: {str(e)}")
    
    def health_check(self) -> Dict[str, Any]:
        """Check API health"""
        response = self.session.get(f"{self.base_url}/", timeout=5)
        response.raise_for_status()
        return {"status": "healthy", "endpoint": self.base_url}
