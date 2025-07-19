"""
Example: Registering AgentStack agents with AstraSync

This example demonstrates how to register AgentStack agents and swarms
with the AstraSync blockchain registry.
"""

from astrasync import AstraSync
from astrasync.adapters.agentstack import register_agentstack, register_with_astrasync

# Example 1: Register a single AgentStack agent from YAML
def example_yaml_agent_registration():
    """Register an AgentStack agent using YAML configuration"""
    
    # AgentStack YAML agent configuration
    yaml_agent = """
agents:
  - agent_name: "Financial-Analysis-Agent"
    system_prompt: |
      You are a financial analyst specializing in market research and investment strategies.
      Your role is to analyze financial data, identify trends, and provide actionable insights.
      Always cite your sources and provide data-driven recommendations.
    model: "gpt-4"
    max_loops: 3
    autosave: true
    dashboard: false
    verbose: true
    dynamic_temperature_enabled: true
    saved_state_path: "finance_agent.json"
    user_name: "analyst_corp"
    retry_attempts: 2
    context_length: 100000
    return_step_meta: true
    output_type: "str"
    tools:
      - "stock_analyzer"
      - "market_researcher"
      - "report_generator"
"""
    
    # Register with AstraSync
    result = register_agentstack(
        agent=yaml_agent,
        email="developer@example.com",
        owner="Finance Team"
    )
    
    print(f"YAML agent registered with ID: {result['agentId']}")
    print(f"Trust Score: {result['trustScore']}")
    return result


# Example 2: Register an AgentStack agent dictionary
def example_dict_agent_registration():
    """Register an AgentStack agent using dictionary configuration"""
    
    # AgentStack agent configuration
    agentstack_agent = {
        "agent_name": "Customer-Success-Agent",
        "system_prompt": """You are a customer success specialist focused on ensuring 
        customer satisfaction and retention. Help users get the most value from our products
        and resolve any issues they encounter.""",
        "model": "gpt-3.5-turbo",
        "max_loops": 5,
        "autosave": True,
        "verbose": False,
        "dynamic_temperature_enabled": True,
        "context_length": 50000,
        "retry_attempts": 3,
        "tools": ["ticket_system", "knowledge_base", "email_sender"],
        "saved_state_path": "customer_success_state.json",
        "output_type": "json"
    }
    
    # Register with AstraSync
    result = register_agentstack(
        agent=agentstack_agent,
        email="developer@example.com",
        owner="Support Department"
    )
    
    print(f"\nDict agent registered with ID: {result['agentId']}")
    print(f"Trust Score: {result['trustScore']}")
    return result


# Example 3: Register an AgentStack swarm
def example_swarm_registration():
    """Register an AgentStack multi-agent swarm"""
    
    # AgentStack swarm configuration
    swarm_config = {
        "swarm_architecture": {
            "name": "Research-Analysis-Swarm",
            "description": "A swarm for comprehensive research and analysis tasks",
            "swarm_type": "ConcurrentWorkflow",
            "task": "Conduct market research and competitive analysis",
            "max_loops": 3
        },
        "agents": [
            {
                "agent_name": "Research-Lead",
                "system_prompt": "You coordinate research efforts and ensure quality",
                "model": "gpt-4",
                "max_loops": 2,
                "autosave": True
            },
            {
                "agent_name": "Data-Collector",
                "system_prompt": "You gather data from various sources",
                "model": "gpt-3.5-turbo",
                "max_loops": 5,
                "tools": ["web_scraper", "api_connector"]
            },
            {
                "agent_name": "Data-Analyst",
                "system_prompt": "You analyze collected data and identify insights",
                "model": "gpt-4",
                "max_loops": 3,
                "tools": ["data_processor", "statistics_calculator"]
            },
            {
                "agent_name": "Report-Writer",
                "system_prompt": "You create comprehensive reports from analysis",
                "model": "gpt-3.5-turbo",
                "max_loops": 2,
                "tools": ["document_generator", "chart_creator"]
            }
        ]
    }
    
    # Register with AstraSync
    client = AstraSync(email="developer@example.com")
    result = client.register(swarm_config, owner="Research Institute")
    
    print(f"\nSwarm registered with ID: {result['agentId']}")
    print(f"Trust Score: {result['trustScore']}")
    return result


# Example 4: Direct registration with auto-detection
def example_direct_registration():
    """Register using the main AstraSync client with auto-detection"""
    
    client = AstraSync(email="developer@example.com")
    
    # AgentStack configuration - will be auto-detected
    agent_config = {
        "agent_name": "DevOps-Automation-Agent",
        "system_prompt": """You are a DevOps automation specialist.
        You help with CI/CD pipelines, infrastructure management, and deployment automation.
        Always follow best practices and security guidelines.""",
        "model": "claude-3-sonnet",
        "max_loops": 10,
        "autosave": True,
        "dynamic_temperature_enabled": True,
        "saved_state_path": "devops_agent_state.json",
        "context_length": 150000,
        "tools": ["kubernetes_manager", "terraform_executor", "pipeline_builder"],
        "verbose": True,
        "return_step_meta": True
    }
    
    # The SDK will auto-detect this as an AgentStack agent
    result = client.register(agent_config, owner="DevOps Team")
    
    print(f"\nAuto-detected Agent registered with ID: {result['agentId']}")
    print(f"Trust Score: {result['trustScore']}")
    print(f"Detected Type: agentstack")  # Auto-detected
    return result


# Example 5: Using the decorator for automatic registration
@register_with_astrasync(email="developer@example.com", owner="AI Team")
class MyAgentStackAgent:
    """Example agent class with auto-registration"""
    
    def __init__(self, name="Auto-Registered Agent"):
        self.agent_name = name
        self.system_prompt = "I am an AI assistant ready to help with various tasks"
        self.model = "gpt-4"
        self.max_loops = 5
        self.autosave = True
        self.context_length = 100000
        self.dynamic_temperature_enabled = True
        self.saved_state_path = f"{name.lower().replace(' ', '_')}_state.json"
    
    def run(self, task):
        # Your agent logic here
        return f"Processing task: {task}"


# Example 6: Complex AgentStack configuration with AgentOps monitoring
def example_agentops_integrated():
    """Register an AgentStack agent with AgentOps monitoring configuration"""
    
    agentops_config = {
        "agents": [{
            "agent_name": "Monitored-Production-Agent",
            "system_prompt": """Production-grade agent with full monitoring and observability.
            Handles critical business processes with reliability and transparency.""",
            "model": "gpt-4",
            "max_loops": 20,
            "autosave": True,
            "dashboard": True,  # Enable AgentOps dashboard
            "verbose": True,
            "dynamic_temperature_enabled": True,
            "saved_state_path": "production_agent.json",
            "user_name": "production_system",
            "retry_attempts": 5,
            "context_length": 200000,
            "return_step_meta": True,
            "output_type": "json",
            "tools": [
                "database_connector",
                "api_gateway",
                "monitoring_service",
                "alert_system"
            ],
            # AgentOps specific configurations
            "agentops_config": {
                "session_tracking": True,
                "event_logging": True,
                "llm_monitoring": True,
                "cost_tracking": True
            }
        }]
    }
    
    result = register_agentstack(
        agent=agentops_config,
        email="production@example.com",
        owner="Production Team"
    )
    
    print(f"\nProduction agent with monitoring registered with ID: {result['agentId']}")
    print(f"Trust Score: {result['trustScore']}")
    return result


if __name__ == "__main__":
    print("AstraSync AgentStack Integration Examples")
    print("=" * 50)
    
    # Run examples
    example_yaml_agent_registration()
    example_dict_agent_registration()
    example_swarm_registration()
    example_direct_registration()
    
    # Create decorated agent (auto-registers on instantiation)
    print("\nCreating auto-registered agent...")
    agent = MyAgentStackAgent("Smart Assistant")
    if hasattr(agent, 'astrasync_id'):
        print(f"Auto-registered with ID: {agent.astrasync_id}")
        print(f"Trust Score: {agent.astrasync_trust_score}")
    
    example_agentops_integrated()
    
    print("\n✅ All AgentStack agents registered successfully!")