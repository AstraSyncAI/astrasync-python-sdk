"""
Example: Registering LangChain agents with AstraSync

This example demonstrates how to register various LangChain components
with the AstraSync blockchain registry.
"""

from astrasync import AstraSync
from astrasync.adapters.langchain import register_langchain, register_with_astrasync

# Example 1: Register a dictionary-based LangChain agent configuration
def example_dict_registration():
    """Register a LangChain agent using dictionary configuration"""
    
    # Define your LangChain agent configuration
    langchain_agent = {
        "name": "Customer Support Agent",
        "agent_type": "conversational",
        "llm": "gpt-4",
        "tools": ["search", "calculator", "weather"],
        "memory": {
            "type": "conversation_buffer",
            "k": 10
        },
        "prompt": "You are a helpful customer support agent...",
        "description": "AI agent for handling customer inquiries",
        "owner": "Support Team"
    }
    
    # Register with AstraSync
    result = register_langchain(
        agent=langchain_agent,
        email="developer@example.com",
        owner="ACME Corp"
    )
    
    print(f"Agent registered with ID: {result['agentId']}")
    print(f"Trust Score: {result['trustScore']}")
    return result


# Example 2: Register a LangChain agent object (mock example)
def example_object_registration():
    """Register a LangChain agent object"""
    
    # This is a mock example - in real usage, you would have actual LangChain objects
    class MockLangChainAgent:
        """Mock LangChain agent for demonstration"""
        def __init__(self):
            self.__class__.__module__ = 'langchain.agents'
            self.__class__.__name__ = 'AgentExecutor'
            self.tools = ['search_tool', 'math_tool']
            self.memory = {"type": "buffer"}
            self.verbose = True
            self.tags = ['customer-support', 'v1']
    
    # Create agent instance
    agent = MockLangChainAgent()
    
    # Register with AstraSync
    result = register_langchain(
        agent=agent,
        email="developer@example.com",
        owner="Dev Team"
    )
    
    print(f"\nObject Agent registered with ID: {result['agentId']}")
    print(f"Trust Score: {result['trustScore']}")
    return result


# Example 3: Using the decorator for automatic registration
@register_with_astrasync(email="developer@example.com", owner="AI Team")
class MyLangChainAgent:
    """Example agent class with auto-registration"""
    
    def __init__(self, name="Auto-Registered Agent"):
        self.__class__.__module__ = 'langchain.agents'
        self.name = name
        self.tools = ['web_search', 'code_interpreter']
        self.llm = 'claude-3'
        self.memory = {"type": "conversation_summary"}
    
    def run(self, query):
        # Your agent logic here
        return f"Processing query: {query}"


# Example 4: Direct registration using AstraSync client
def example_direct_registration():
    """Register using the main AstraSync client with auto-detection"""
    
    client = AstraSync(email="developer@example.com")
    
    # LangChain configuration
    agent_config = {
        "name": "Research Assistant",
        "llm": "gpt-4-turbo",
        "tools": [
            {"name": "arxiv_search", "description": "Search academic papers"},
            {"name": "wikipedia", "description": "Search Wikipedia"},
            {"name": "calculator", "description": "Perform calculations"}
        ],
        "memory": {"type": "entity", "k": 20},
        "agent_type": "research",
        "description": "Advanced research assistant with access to academic sources"
    }
    
    # The SDK will auto-detect this as a LangChain agent
    result = client.register(agent_config, owner="Research Lab")
    
    print(f"\nAuto-detected Agent registered with ID: {result['agentId']}")
    print(f"Trust Score: {result['trustScore']}")
    print(f"Detected Type: langchain")  # Auto-detected
    return result


# Example 5: Chain registration
def example_chain_registration():
    """Register a LangChain chain configuration"""
    
    chain_config = {
        "name": "Analysis Chain",
        "agent_type": "sequential_chain",
        "llm": "claude-3-sonnet",
        "tools": ["data_analyzer", "report_generator"],
        "prompt": "Analyze the following data and generate insights...",
        "description": "Multi-step analysis chain for data processing",
        "capabilities": ["data-analysis", "report-generation", "visualization"]
    }
    
    result = register_langchain(
        agent=chain_config,
        email="analytics@example.com",
        owner="Analytics Team"
    )
    
    print(f"\nChain registered with ID: {result['agentId']}")
    print(f"Trust Score: {result['trustScore']}")
    return result


if __name__ == "__main__":
    print("AstraSync LangChain Integration Examples")
    print("=" * 50)
    
    # Run examples
    example_dict_registration()
    example_object_registration()
    
    # Create decorated agent (auto-registers on instantiation)
    print("\nCreating auto-registered agent...")
    agent = MyLangChainAgent("Smart Assistant")
    if hasattr(agent, 'astrasync_id'):
        print(f"Auto-registered with ID: {agent.astrasync_id}")
        print(f"Trust Score: {agent.astrasync_trust_score}")
    
    example_direct_registration()
    example_chain_registration()
    
    print("\n✅ All LangChain agents registered successfully!")