# AstraSync Python SDK

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Universal AI agent registration with blockchain compliance tracking. Auto-detects agent formats from OpenAI, MCP, Letta, IBM ACP, AutoGPT, and Salesforce Agentforce.

## 🚀 Quick Start

```bash
# Clone the repository
git clone https://github.com/AstraSyncAI/astrasync-python-sdk.git
cd astrasync-python-sdk

# Install in development mode
pip install -e .

# Or install from GitHub directly
pip install git+https://github.com/AstraSyncAI/astrasync-python-sdk.git
```

## 📋 Features

- 🔍 **Universal Auto-Detection**: Automatically identifies agent formats from major frameworks
- ⚡ **30-Second Integration**: Simple API for instant agent registration
- 🎯 **Developer Preview**: Free registration with temporary IDs during preview
- 📊 **Trust Scores**: Automatic calculation based on agent capabilities
- 🎨 **Beautiful CLI**: Rich terminal output with progress indicators
- 🏢 **Enterprise Ready**: Salesforce Agentforce support for regulated industries

## 🤖 Supported Agent Formats

### ✅ Auto-Detected Formats

- **OpenAI Assistants** - `model` + `instructions` pattern
- **MCP Servers** - Model Context Protocol agents
- **Letta (MemGPT)** - Memory-enabled autonomous agents  
- **IBM Agent Control Protocol** - Enterprise agent standard
- **AutoGPT** - Autonomous goal-driven agents
- **Salesforce Agentforce** - Enterprise digital labor platform

### 🔜 Coming Soon

- CrewAI multi-agent systems
- LangChain agents
- Custom formats via plugins

## 💻 Usage Examples

### Basic Registration

```python
from astrasync import AstraSync

# Initialize client
client = AstraSync(email="developer@example.com")

# Register any supported agent format
result = client.register({
    "name": "Customer Support Bot",
    "model": "gpt-4",
    "instructions": "Help customers with their queries"
})

print(f"Agent registered with ID: {result['agentId']}")
# Output: Agent registered with ID: TEMP-1734567890123-ABC123
```

### Auto-Detection Magic

```python
# OpenAI format - automatically detected
openai_agent = {
    "name": "Sales Assistant",
    "model": "gpt-4", 
    "instructions": "Help with sales inquiries",
    "tools": [{"type": "retrieval"}]
}

# MCP format - automatically detected
mcp_agent = {
    "protocol": "ai-agent",
    "skills": ["query", "update"],
    "capabilities": {"streaming": True}
}

# Letta format - automatically detected
letta_agent = {
    "type": "agent",
    "memory": {"type": "core_memory"},
    "model": "gpt-4"
}

# Register any format - auto-detection handles it!
for agent in [openai_agent, mcp_agent, letta_agent]:
    result = client.register(agent)
    print(f"Registered {agent.get('name', 'agent')} as type: {result.get('agentType')}")
```

### 🆕 Salesforce Agentforce Support (NEW!)

Perfect for enterprises requiring blockchain-based compliance tracking.

```python
from astrasync.adapters.agentforce import register_agentforce

# Register your Agentforce agent
agent_config = {
    "name": "Customer Service Agent",
    "agent_type": "External",
    "agent_template_type": "EinsteinServiceAgent",
    "company_name": "YourCompany",
    "topics": ["support", "orders"]
}

result = register_agentforce(agent_config, email="you@company.com")
print(f"AstraSync ID: {result['agentId']}")
```

**Ideal for:**
- 🏦 Financial services (every decision traceable)
- 🏥 Healthcare (HIPAA compliance built-in)
- 🏢 Enterprise deployments (SOX compliance)
- 🛍️ AgentExchange marketplace (verified trust scores)

[See full Agentforce example →](examples/agentforce_example.py)

### Decorator Pattern

```python
from astrasync import register

@register(email="developer@example.com")
def my_agent(prompt):
    return f"Response to: {prompt}"

# The agent is automatically registered when defined!
# Access the ID via my_agent.astrasync_id
```

### Using the CLI

```bash
# Check API health
astrasync health

# Register from command line
astrasync register --name "My Agent" --email "dev@example.com"

# Beautiful output with rich formatting!
```

## 🎯 Developer Preview

During our developer preview, all agents receive **temporary IDs** (TEMP-xxxx format) that will automatically convert to permanent blockchain-registered IDs when you create your AstraSync account.

### Why Developer Preview?

- ✅ **Instant Testing**: Start integrating immediately
- ✅ **No Blockchain Setup**: Skip the complexity during development
- ✅ **Free Registration**: No costs during preview
- ✅ **Automatic Migration**: Your TEMP IDs convert to permanent IDs

### What Happens Next?

1. Use the same email when creating your AstraSync account
2. All your preview agents automatically migrate
3. Receive permanent blockchain IDs
4. Full audit trail and compliance features activate

## 📁 Examples

Check out the `examples/` directory for complete code:

- `quickstart.py` - Basic usage patterns
- `auto_detection.py` - See auto-detection in action
- `agentforce_example.py` - Salesforce Agentforce integration
- `decorator_example.py` - Using the @register decorator

## 🛠️ API Reference

### AstraSync Class

```python
client = AstraSync(email="your@email.com", api_url=None)
```

- `email` (required): Your developer email
- `api_url` (optional): Custom API endpoint (defaults to production)

### Methods

#### `register(agent_data) -> dict`

Registers an agent with auto-detection.

**Parameters:**
- `agent_data`: Dict, JSON string, or file path containing agent configuration

**Returns:**
```python
{
    "agentId": "TEMP-1234567890-XXXXX",
    "status": "registered",
    "trustScore": "TEMP-85%",
    "agentType": "detected-type"
}
```

### Supported Input Formats

The SDK accepts agents in multiple formats:

- Python dictionaries
- JSON strings
- File paths (`.json` files)
- Agent objects (with appropriate adapters)

## 🌟 Trust Score Calculation

Trust scores (0-95% during preview) are calculated based on:

- ✓ Agent name quality
- ✓ Description completeness  
- ✓ Number of capabilities
- ✓ Version information
- ✓ Platform-specific features

## 🔧 Development

```bash
# Clone the repo
git clone https://github.com/AstraSyncAI/astrasync-python-sdk.git
cd astrasync-python-sdk

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e .

# Run tests
python examples/quickstart.py
```

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Development Roadmap

- [x] Core SDK functionality
- [x] Auto-detection for 5+ formats
- [x] Beautiful CLI interface
- [x] Salesforce Agentforce support
- [ ] CrewAI integration (this week)
- [ ] LangChain integration (this week)
- [ ] PyPI publication
- [ ] Async support
- [ ] Batch registration

## 📄 License

MIT License - see [LICENSE](LICENSE) for details.

## 🔗 Links

- [AstraSync Website](https://astrasync.ai)
- [Documentation](https://docs.astrasync.ai)
- [API Reference](https://api.astrasync.ai/docs)
- [GitHub Repository](https://github.com/AstraSyncAI/astrasync-python-sdk)

## 💬 Support

- 📧 Email: support@astrasync.ai
- 💬 Discord: [Join our community](https://discord.gg/astrasync)
- 🐛 Issues: [GitHub Issues](https://github.com/AstraSyncAI/astrasync-python-sdk/issues)

---

Built with ❤️ by the AstraSync team. Making AI agents accountable, one blockchain registration at a time.
