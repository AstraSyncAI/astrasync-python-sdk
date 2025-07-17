"""
AstraSync adapters for various AI agent frameworks
"""

from .agentforce import (
    register_agentforce,
    register_agentforce_deployment
)

from .langchain import (
    normalize_agent_data as normalize_langchain,
    register_langchain,
    create_registration_decorator as langchain_decorator,
    register_with_astrasync
)

__all__ = [
    'register_agentforce',
    'register_agentforce_deployment',
    'normalize_langchain',
    'register_langchain',
    'langchain_decorator',
    'register_with_astrasync'
]