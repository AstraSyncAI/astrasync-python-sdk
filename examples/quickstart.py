from astrasync import register

# This is all it takes to register an AI agent
@register(email="developer@example.com")
def customer_support_agent(query):
    """An AI agent that handles customer support inquiries."""
    return f"I'll help you with: {query}"

# Your agent is queued for a blockchain-verified identity! All you need to do is register for a free developer account at https://astrasync.ai/auth
print(f"Agent ID: {customer_support_agent._astrasync_id}")
