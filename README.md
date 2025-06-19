# AstraSync Python SDK

Universal AI agent registration for blockchain compliance. Auto-detects agent formats from all major frameworks.

> 🚀 **Developer Preview**: Currently issuing temporary IDs. [Sign up for early access](https://astrasync.ai/auth) to get permanent blockchain verification when we launch.

## Installation

```bash
# Coming soon to PyPI
# For now, install from GitHub:
git clone https://github.com/AstraSyncAI/astrasync-python-sdk.git
cd astrasync-python-sdk
pip install -e .
```

## Quick Start

```python
from astrasync import register

@register(email="your-email@example.com")
def my_agent(prompt):
    """An AI agent that processes prompts"""
    return f"Processed: {prompt}"

# Your agent is now registered with a temporary ID
print(f"Agent ID: {my_agent._astrasync_id}")
```

## CLI Usage

```bash
# Check API health
astrasync health

# Register an agent from file
astrasync register agent.json --email dev@example.com
```

## Auto-Detection Magic

The SDK automatically detects and registers agents from:
- ✅ OpenAI Agents SDK
- ✅ MCP (Model Context Protocol)
- ✅ Letta (formerly MemGPT)
- ✅ IBM ACP
- ✅ AutoGPT
- 🔜 CrewAI (coming this week)
- 🔜 LangChain (coming this week)

## Why AstraSync?

As AI agents become more powerful, they need verifiable identity and compliance tracking. AstraSync provides the infrastructure for the emerging agent economy.

## Developer Preview Notes

- Currently issuing TEMP- prefixed IDs
- These automatically convert to permanent IDs when you create an account
- Trust scores are simulated (70-95% range)
- Full blockchain integration coming in production release

## Examples

### Register an OpenAI Agent

```python
from astrasync import AstraSync

client = AstraSync(email="developer@example.com")

# OpenAI agent format
openai_agent = {
    "name": "Customer Support Bot",
    "model": "gpt-4",
    "instructions": "You are a helpful customer support agent",
    "tools": [{"type": "retrieval"}, {"type": "code_interpreter"}]
}

result = client.register(openai_agent)
print(f"Registered with ID: {result['agentId']}")
```

### Register from File

```python
from astrasync import AstraSync

client = AstraSync(email="developer@example.com")
result = client.register("path/to/agent.json")
print(f"Registered with ID: {result['agentId']}")
```

### Using the Decorator Pattern

```python
from astrasync import register

@register(
    email="developer@example.com",
    name="Analytics Agent",
    description="Processes data and generates insights"
)
class AnalyticsAgent:
    def analyze(self, data):
        # Your agent logic here
        return {"insights": "..."}

# Access registration info
print(f"Agent ID: {AnalyticsAgent._astrasync_id}")
```

## Supported Agent Formats

### OpenAI Format
```json
{
  "name": "Agent Name",
  "model": "gpt-4",
  "instructions": "Agent instructions",
  "tools": [{"type": "retrieval"}]
}
```

### MCP Format
```json
{
  "protocol": "ai-agent",
  "name": "MCP Agent",
  "skills": [
    {"id": "skill1", "description": "..."}
  ]
}
```

### Letta Format
```json
{
  "type": "agent",
  "memory": {
    "human": "User information",
    "persona": "Agent persona"
  }
}
```

## API Reference

### AstraSync Class

```python
from astrasync import AstraSync

# Initialize client
client = AstraSync(
    email="developer@example.com",  # Optional: can use env var ASTRASYNC_EMAIL
    api_url="https://..."          # Optional: defaults to production
)

# Register an agent
result = client.register(agent_data)  # Dict, JSON string, or file path

# Verify an agent
verification = client.verify(agent_id)
```

### Environment Variables

- `ASTRASYNC_EMAIL` - Default email for registrations
- `ASTRASYNC_API_URL` - API endpoint (defaults to production)

## Contributing

We're in active development! Feel free to open issues or submit PRs.

## Links

- [JavaScript SDK](https://github.com/AstraSyncAI/astrasync-node-sdk)
- [Documentation](https://docs.astrasync.ai) (coming soon)
- [Sign up for Developer Preview](https://astrasync.ai/auth)
- [API Status](https://astrasync-api-production.up.railway.app)

## License

MIT License - see LICENSE file for details

## Support

- 📧 Email: developers@astrasync.ai
- 💬 Discord: [Join our community](https://discord.gg/astrasync) (coming soon)
- 🐛 Issues: [GitHub Issues](https://github.com/AstraSyncAI/astrasync-python-sdk/issues)