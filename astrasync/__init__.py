"""
AstraSync AI - Universal AI Agent Registration
"""
from .core import AstraSync
from .exceptions import AstraSyncError, RegistrationError, ValidationError
from .decorators import register

__version__ = "0.2.0"
__all__ = ["AstraSync", "register", "AstraSyncError", "RegistrationError", "ValidationError"]

# Convenience instance
_default_client = None

def register_agent(agent_data, email=None):
    """Convenience function for quick registration"""
    global _default_client
    if _default_client is None:
        _default_client = AstraSync(email=email)
    return _default_client.register(agent_data)

# Agentforce integration
try:
    from .adapters.agentforce import (
        register_agentforce,
        register_agentforce_deployment,
        AgentforceAdapter
    )
except ImportError:
    # Agentforce adapter not available
    pass
