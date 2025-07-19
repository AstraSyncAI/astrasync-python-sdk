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

from .crewai import (
    normalize_agent_data as normalize_crewai,
    register_crewai,
    create_registration_decorator as crewai_decorator,
    register_with_astrasync as crewai_register_decorator
)

from .n8n import (
    normalize_agent_data as normalize_n8n,
    register_n8n,
    create_registration_decorator as n8n_decorator,
    register_with_astrasync as n8n_register_decorator
)

from .agentstack import (
    normalize_agent_data as normalize_agentstack,
    register_agentstack,
    create_registration_decorator as agentstack_decorator,
    register_with_astrasync as agentstack_register_decorator
)

__all__ = [
    'register_agentforce',
    'register_agentforce_deployment',
    'normalize_langchain',
    'register_langchain',
    'langchain_decorator',
    'register_with_astrasync',
    'normalize_crewai',
    'register_crewai',
    'crewai_decorator',
    'crewai_register_decorator',
    'normalize_n8n',
    'register_n8n',
    'n8n_decorator',
    'n8n_register_decorator',
    'normalize_agentstack',
    'register_agentstack',
    'agentstack_decorator',
    'agentstack_register_decorator'
]