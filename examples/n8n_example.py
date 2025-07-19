"""
Example: Registering n8n workflows and AI agents with AstraSync

This example demonstrates how to register n8n AI agent nodes and workflows
with the AstraSync blockchain registry.
"""

from astrasync import AstraSync
from astrasync.adapters.n8n import register_n8n, register_with_astrasync

# Example 1: Register a single n8n AI Agent node
def example_agent_node_registration():
    """Register a single n8n AI Agent node configuration"""
    
    # n8n AI Agent node configuration
    n8n_agent_node = {
        "type": "n8n-nodes-langchain.agent",
        "name": "Customer Support AI",
        "parameters": {
            "systemPrompt": """You are a helpful customer support assistant. 
            You help users with their questions and provide accurate information 
            about our products and services.""",
            "model": "gpt-4",
            "tools": ["search", "calculator", "product_database"],
            "memory": {
                "type": "windowBuffer",
                "k": 10
            },
            "agentType": "Tools Agent",
            "outputParsing": True
        },
        "position": [250, 300]
    }
    
    # Register with AstraSync
    result = register_n8n(
        agent=n8n_agent_node,
        email="developer@example.com",
        owner="Support Team"
    )
    
    print(f"Agent node registered with ID: {result['agentId']}")
    print(f"Trust Score: {result['trustScore']}")
    return result


# Example 2: Register a complete n8n workflow with AI agents
def example_workflow_registration():
    """Register a complete n8n workflow containing AI agents"""
    
    # n8n workflow with multiple nodes including AI agents
    n8n_workflow = {
        "workflow": {
            "name": "AI Customer Support Workflow",
            "description": "Automated customer support with AI agents and integrations",
            "nodes": [
                {
                    "type": "n8n-nodes-base.webhook",
                    "name": "Webhook Trigger",
                    "parameters": {
                        "path": "customer-support",
                        "method": "POST"
                    },
                    "position": [50, 300]
                },
                {
                    "type": "n8n-nodes-langchain.agent",
                    "name": "AI Support Agent",
                    "parameters": {
                        "systemPrompt": "You are a customer support specialist...",
                        "model": "gpt-3.5-turbo",
                        "tools": ["knowledge_base", "ticket_system"],
                        "memory": {"type": "windowBuffer", "k": 5}
                    },
                    "position": [250, 300]
                },
                {
                    "type": "n8n-nodes-base.http",
                    "name": "Update CRM",
                    "parameters": {
                        "url": "https://api.crm.com/update",
                        "method": "POST"
                    },
                    "position": [450, 300]
                }
            ],
            "connections": {
                "Webhook Trigger": {
                    "main": [["AI Support Agent"]]
                },
                "AI Support Agent": {
                    "main": [["Update CRM"]]
                }
            },
            "settings": {
                "executionOrder": "v1"
            }
        }
    }
    
    # Register with AstraSync
    client = AstraSync(email="developer@example.com")
    result = client.register(n8n_workflow, owner="Automation Team")
    
    print(f"\nWorkflow registered with ID: {result['agentId']}")
    print(f"Trust Score: {result['trustScore']}")
    return result


# Example 3: Direct registration using AstraSync client
def example_direct_registration():
    """Register using the main AstraSync client with auto-detection"""
    
    client = AstraSync(email="developer@example.com")
    
    # n8n configuration - will be auto-detected
    agent_config = {
        "type": "n8n-nodes-langchain.conversationalAgent",
        "name": "Research Assistant",
        "parameters": {
            "systemPrompt": """You are an expert research assistant.
            Help users find accurate information and provide detailed analysis.""",
            "model": "claude-3-sonnet",
            "tools": ["web_search", "document_analyzer", "citation_generator"],
            "memory": {
                "type": "vectorStore",
                "dimension": 1536
            },
            "outputParsing": True,
            "agentType": "Tools Agent"
        },
        "description": "AI-powered research assistant"
    }
    
    # The SDK will auto-detect this as an n8n agent
    result = client.register(agent_config, owner="Research Lab")
    
    print(f"\nAuto-detected Agent registered with ID: {result['agentId']}")
    print(f"Trust Score: {result['trustScore']}")
    print(f"Detected Type: n8n")  # Auto-detected
    return result


# Example 4: Complex multi-agent workflow
def example_multi_agent_workflow():
    """Register a complex n8n workflow with multiple AI agents"""
    
    complex_workflow = {
        "name": "Multi-Agent Analysis Pipeline",
        "description": "Complex workflow with multiple specialized AI agents",
        "nodes": [
            {
                "type": "n8n-nodes-base.trigger",
                "name": "Start",
                "position": [50, 200]
            },
            {
                "type": "n8n-nodes-langchain.agent",
                "name": "Data Collector Agent",
                "parameters": {
                    "systemPrompt": "Collect and organize data from various sources",
                    "model": "gpt-4",
                    "tools": ["web_scraper", "api_connector", "file_reader"]
                },
                "position": [250, 100]
            },
            {
                "type": "n8n-nodes-langchain.agent", 
                "name": "Analysis Agent",
                "parameters": {
                    "systemPrompt": "Analyze collected data and identify patterns",
                    "model": "gpt-4",
                    "tools": ["data_analyzer", "statistics", "visualization"]
                },
                "position": [250, 300]
            },
            {
                "type": "n8n-nodes-langchain.agent",
                "name": "Report Generator Agent",
                "parameters": {
                    "systemPrompt": "Generate comprehensive reports from analysis",
                    "model": "gpt-3.5-turbo",
                    "tools": ["document_generator", "chart_creator"]
                },
                "position": [450, 200]
            }
        ],
        "connections": {
            "Start": {
                "main": [["Data Collector Agent", "Analysis Agent"]]
            },
            "Data Collector Agent": {
                "main": [["Report Generator Agent"]]
            },
            "Analysis Agent": {
                "main": [["Report Generator Agent"]]
            }
        }
    }
    
    result = register_n8n(
        agent=complex_workflow,
        email="analytics@example.com",
        owner="Analytics Department"
    )
    
    print(f"\nMulti-agent workflow registered with ID: {result['agentId']}")
    print(f"Trust Score: {result['trustScore']}")
    return result


# Example 5: Using the decorator for automatic registration
@register_with_astrasync(email="developer@example.com", owner="AI Team")
class MyN8nWorkflow:
    """Example workflow class with auto-registration"""
    
    def __init__(self, name="Auto-Registered Workflow"):
        self.workflow = {
            "name": name,
            "nodes": [
                {
                    "type": "n8n-nodes-langchain.agent",
                    "name": "Main Agent",
                    "parameters": {
                        "systemPrompt": "General purpose AI assistant",
                        "model": "gpt-4"
                    }
                }
            ]
        }
    
    def execute(self):
        # Your workflow execution logic here
        return f"Executing workflow: {self.workflow['name']}"


if __name__ == "__main__":
    print("AstraSync n8n Integration Examples")
    print("=" * 50)
    
    # Run examples
    example_agent_node_registration()
    example_workflow_registration()
    example_direct_registration()
    example_multi_agent_workflow()
    
    # Create decorated workflow (auto-registers on instantiation)
    print("\nCreating auto-registered workflow...")
    workflow = MyN8nWorkflow("Smart Automation")
    if hasattr(workflow, 'astrasync_id'):
        print(f"Auto-registered with ID: {workflow.astrasync_id}")
        print(f"Trust Score: {workflow.astrasync_trust_score}")
    
    print("\n✅ All n8n agents and workflows registered successfully!")