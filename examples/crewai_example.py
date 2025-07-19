"""
Example: Registering CrewAI agents with AstraSync

This example demonstrates how to register CrewAI agents, crews, and tasks
with the AstraSync blockchain registry.
"""

from astrasync import AstraSync
from astrasync.adapters.crewai import register_crewai, register_with_astrasync

# Example 1: Register a dictionary-based CrewAI agent configuration
def example_agent_registration():
    """Register a CrewAI agent using dictionary configuration"""
    
    # Define your CrewAI agent configuration
    crewai_agent = {
        "name": "Research Analyst",
        "role": "Senior Research Analyst",
        "goal": "Uncover cutting-edge developments in AI and data science",
        "backstory": """You work at a leading tech think tank.
        Your expertise lies in identifying emerging trends.
        You have a knack for dissecting complex data and presenting
        actionable insights.""",
        "tools": ["search_tool", "scraper_tool"],
        "llm": "gpt-4",
        "memory": True,
        "max_iter": 5,
        "description": "Expert researcher focused on AI trends",
        "owner": "Research Team"
    }
    
    # Register with AstraSync
    result = register_crewai(
        agent=crewai_agent,
        email="developer@example.com",
        owner="ACME Research"
    )
    
    print(f"Agent registered with ID: {result['agentId']}")
    print(f"Trust Score: {result['trustScore']}")
    return result


# Example 2: Register a CrewAI crew configuration
def example_crew_registration():
    """Register a CrewAI crew with multiple agents"""
    
    # Define a crew configuration
    crew_config = {
        "name": "AI Research Crew",
        "description": "Multi-agent crew for comprehensive AI research",
        "agents": [
            {
                "role": "Researcher",
                "goal": "Find and analyze AI papers",
                "backstory": "Expert in academic research"
            },
            {
                "role": "Writer",
                "goal": "Create comprehensive reports",
                "backstory": "Technical writing specialist"
            }
        ],
        "tasks": [
            {
                "description": "Research latest AI developments",
                "expected_output": "List of key findings"
            },
            {
                "description": "Write summary report",
                "expected_output": "Comprehensive report document"
            }
        ],
        "process": "sequential",
        "owner": "Research Department"
    }
    
    # Register with AstraSync
    client = AstraSync(email="developer@example.com")
    result = client.register(crew_config, owner="AI Lab")
    
    print(f"\nCrew registered with ID: {result['agentId']}")
    print(f"Trust Score: {result['trustScore']}")
    return result


# Example 3: Register a CrewAI agent object (mock example)
def example_object_registration():
    """Register a CrewAI agent object"""
    
    # This is a mock example - in real usage, you would have actual CrewAI objects
    class MockCrewAIAgent:
        """Mock CrewAI agent for demonstration"""
        def __init__(self):
            self.__class__.__module__ = 'crewai.agent'
            self.__class__.__name__ = 'Agent'
            self.role = "Data Analyst"
            self.goal = "Analyze and interpret complex datasets"
            self.backstory = "You are a data expert with 10 years of experience"
            self.tools = ['pandas_tool', 'visualization_tool']
            self.memory = True
            self.llm = 'gpt-3.5-turbo'
            self.max_iter = 10
    
    # Create agent instance
    agent = MockCrewAIAgent()
    
    # Register with AstraSync
    result = register_crewai(
        agent=agent,
        email="developer@example.com",
        owner="Analytics Team"
    )
    
    print(f"\nObject Agent registered with ID: {result['agentId']}")
    print(f"Trust Score: {result['trustScore']}")
    return result


# Example 4: Using the decorator for automatic registration
@register_with_astrasync(email="developer@example.com", owner="AI Team")
class MyCrewAIAgent:
    """Example agent class with auto-registration"""
    
    def __init__(self, role="Task Executor"):
        self.__class__.__module__ = 'crewai.agent'
        self.role = role
        self.goal = "Execute assigned tasks efficiently"
        self.backstory = "Specialized agent for task automation"
        self.tools = ['executor', 'validator']
        self.llm = 'claude-2'
        self.memory = True
    
    def execute(self, task):
        # Your agent logic here
        return f"Executing task: {task}"


# Example 5: Direct registration using AstraSync client
def example_direct_registration():
    """Register using the main AstraSync client with auto-detection"""
    
    client = AstraSync(email="developer@example.com")
    
    # CrewAI configuration - will be auto-detected
    agent_config = {
        "name": "Content Creator",
        "role": "Content Creation Specialist",
        "goal": "Create engaging and informative content about AI",
        "backstory": """You are a creative content specialist.
        You excel at transforming complex technical concepts
        into accessible, engaging content.""",
        "tools": ["web_search", "content_generator", "editor"],
        "memory": True,
        "description": "AI content creation specialist"
    }
    
    # The SDK will auto-detect this as a CrewAI agent
    result = client.register(agent_config, owner="Content Team")
    
    print(f"\nAuto-detected Agent registered with ID: {result['agentId']}")
    print(f"Trust Score: {result['trustScore']}")
    print(f"Detected Type: crewai")  # Auto-detected
    return result


# Example 6: Complex crew with multiple agents and tasks
def example_complex_crew():
    """Register a complex CrewAI crew"""
    
    complex_crew = {
        "name": "Full Research Pipeline",
        "description": "End-to-end research and reporting crew",
        "agents": [
            {
                "role": "Research Lead",
                "goal": "Coordinate research efforts",
                "backstory": "Senior researcher with management experience"
            },
            {
                "role": "Data Collector",
                "goal": "Gather relevant data from multiple sources",
                "backstory": "Expert in data mining and collection"
            },
            {
                "role": "Analyst",
                "goal": "Analyze collected data for insights",
                "backstory": "Statistical analysis expert"
            },
            {
                "role": "Report Writer",
                "goal": "Create comprehensive reports",
                "backstory": "Technical documentation specialist"
            }
        ],
        "tasks": [
            {
                "description": "Define research parameters",
                "expected_output": "Research scope document"
            },
            {
                "description": "Collect data from sources",
                "expected_output": "Raw data collection"
            },
            {
                "description": "Analyze and interpret data",
                "expected_output": "Analysis results"
            },
            {
                "description": "Write final report",
                "expected_output": "Final research report"
            }
        ],
        "process": "hierarchical",
        "capabilities": ["research", "analysis", "reporting", "coordination"]
    }
    
    result = register_crewai(
        agent=complex_crew,
        email="research@example.com",
        owner="Research Institute"
    )
    
    print(f"\nComplex Crew registered with ID: {result['agentId']}")
    print(f"Trust Score: {result['trustScore']}")
    return result


if __name__ == "__main__":
    print("AstraSync CrewAI Integration Examples")
    print("=" * 50)
    
    # Run examples
    example_agent_registration()
    example_crew_registration()
    example_object_registration()
    
    # Create decorated agent (auto-registers on instantiation)
    print("\nCreating auto-registered agent...")
    agent = MyCrewAIAgent("Automation Specialist")
    if hasattr(agent, 'astrasync_id'):
        print(f"Auto-registered with ID: {agent.astrasync_id}")
        print(f"Trust Score: {agent.astrasync_trust_score}")
    
    example_direct_registration()
    example_complex_crew()
    
    print("\n✅ All CrewAI agents registered successfully!")