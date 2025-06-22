"""
Examples of registering Google ADK agents with AstraSync
"""

from astrasync import AstraSync

def example_simple_adk():
    """Register a basic Google ADK agent configuration"""
    
    # ADK agent configuration
    adk_agent = {
        "name": "Customer Service Agent",
        "instructions": "Help customers with their inquiries politely and efficiently",
        "model": "gemini-1.5-pro",
        "tools": [
            {"name": "search_knowledge_base"},
            {"name": "create_ticket"}
        ],
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {"type": "string"}
            }
        },
        "output_schema": {
            "type": "object",
            "properties": {
                "response": {"type": "string"},
                "ticket_id": {"type": "string", "optional": True}
            }
        }
    }
    
    # Register with AstraSync
    client = AstraSync(email="developer@example.com")
    result = client.register(adk_agent)
    
    print(f"✅ Registered ADK Agent: {result['agentId']}")
    print(f"📊 Trust Score: {result['trustScore']}")
    return result

def example_orchestration_agent():
    """Register an ADK orchestration agent"""
    
    orchestrator = {
        "name": "Multi-Agent Orchestrator",
        "agent_type": "sequential",
        "description": "Coordinates multiple specialized agents for complex tasks",
        "tools": [
            "delegate_to_research",
            "delegate_to_analysis",
            "synthesize_results"
        ],
        "runner": "default",
        "session_service": "managed"
    }
    
    client = AstraSync(email="developer@example.com")
    result = client.register(orchestrator)
    
    print(f"✅ Registered Orchestrator: {result['agentId']}")
    print(f"🔄 Type: Sequential Orchestration")
    return result

def example_vertex_ai_agent():
    """Register an ADK agent with Vertex AI configuration"""
    
    vertex_agent = {
        "name": "Vertex AI Reasoning Engine",
        "model": "gemini-1.5-pro",
        "instructions": "Complex reasoning agent deployed on Vertex AI with advanced capabilities",
        "tools": ["code_execution", "web_search", "data_analysis"],
        "agent_type": "llm",
        "session_service": "managed",
        "config": {
            "agent_class": "google.adk.agents.LlmAgent",
            "deployment": "vertex-ai"
        }
    }
    
    client = AstraSync(email="developer@example.com")
    result = client.register(vertex_agent)
    
    print(f"✅ Registered Vertex AI Agent: {result['agentId']}")
    print(f"☁️  Deployment: Vertex AI")
    return result

def example_adk_object():
    """Example of registering a Google ADK agent object (if available)"""
    
    try:
        # This example shows how it would work with actual ADK objects
        from google.adk.agents import Agent
        
        # Create an ADK agent instance
        agent = Agent(
            name="Python ADK Agent",
            instructions="Demonstrate AstraSync integration with ADK objects",
            tools=["search", "calculate"],
            model="gemini-1.5-flash"
        )
        
        # Register the actual object
        client = AstraSync(email="developer@example.com")
        result = client.register(agent)
        
        print(f"✅ Registered ADK Object: {result['agentId']}")
        print(f"🐍 Direct object registration successful")
        return result
        
    except ImportError:
        print("ℹ️  Google ADK not installed, skipping object example")
        print("   Install with: pip install google-adk")
        return None

def example_parallel_workflow():
    """Register a parallel workflow agent"""
    
    parallel_agent = {
        "name": "Parallel Task Processor",
        "agent_type": "parallel",
        "description": "Executes multiple tasks simultaneously for faster processing",
        "tools": [
            "process_task_1",
            "process_task_2", 
            "process_task_3",
            "merge_results"
        ],
        "output_schema": {
            "type": "object",
            "properties": {
                "results": {"type": "array"},
                "execution_time": {"type": "number"}
            }
        },
        "runner": "parallel_executor"
    }
    
    client = AstraSync(email="developer@example.com")
    result = client.register(parallel_agent)
    
    print(f"✅ Registered Parallel Agent: {result['agentId']}")
    print(f"⚡ Execution: Parallel processing enabled")
    return result

if __name__ == "__main__":
    print("🚀 AstraSync Google ADK Registration Examples\n")
    
    # Run examples
    print("1️⃣ Simple ADK Agent:")
    example_simple_adk()
    print("\n" + "-"*50 + "\n")
    
    print("2️⃣ Orchestration Agent:")
    example_orchestration_agent()
    print("\n" + "-"*50 + "\n")
    
    print("3️⃣ Vertex AI Agent:")
    example_vertex_ai_agent()
    print("\n" + "-"*50 + "\n")
    
    print("4️⃣ ADK Object Registration:")
    example_adk_object()
    print("\n" + "-"*50 + "\n")
    
    print("5️⃣ Parallel Workflow Agent:")
    example_parallel_workflow()
    
    print("\n✅ All examples completed!")
