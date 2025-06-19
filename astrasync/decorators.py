import functools
import inspect
from typing import Optional

from .core import AstraSync

def register(
    email: Optional[str] = None,
    name: Optional[str] = None,
    description: Optional[str] = None,
    auto_register: bool = True
):
    """
    Decorator to automatically register functions or classes as AI agents
    """
    def decorator(func_or_class):
        agent_name = name or func_or_class.__name__
        agent_description = description or (
            inspect.getdoc(func_or_class) or 
            f"Auto-registered {func_or_class.__name__}"
        )
        
        agent_data = {
            'name': agent_name,
            'description': agent_description,
            'owner': email or 'decorator',
            'agentType': 'python-decorated',
            'capabilities': ['function-based'],
            'metadata': {
                'module': func_or_class.__module__,
                'qualname': func_or_class.__qualname__,
            }
        }
        
        if auto_register:
            try:
                client = AstraSync(email=email)
                result = client.register(agent_data)
                
                func_or_class._astrasync_id = result['agentId']
                func_or_class._astrasync_registered = True
                
                print(f"✅ Registered {agent_name} with AstraSync: {result['agentId']}")
            except Exception as e:
                print(f"⚠️  Failed to register {agent_name}: {e}")
                func_or_class._astrasync_registered = False
        
        return func_or_class
    
    return decorator
