markdown# AstraSync Python SDK

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Universal AI agent registration with blockchain compliance tracking. Auto-detects agent formats from OpenAI, Google ADK, MCP, Letta, IBM ACP, AutoGPT, and Salesforce Agentforce.

## 🚀 Quick Start

```bash
# Clone the repository
git clone https://github.com/AstraSyncAI/astrasync-python-sdk.git
cd astrasync-python-sdk

# Install in development mode
pip install -e .

# Or install from GitHub directly
pip install git+https://github.com/AstraSyncAI/astrasync-python-sdk.git
📋 Features

🔍 Universal Auto-Detection: Automatically identifies agent formats from major frameworks
⚡ 30-Second Integration: Simple API for instant agent registration
🎯 Developer Preview: Free registration with temporary IDs during preview
📊 Trust Scores: Automatic calculation based on agent capabilities
🎨 Beautiful CLI: Rich terminal output with progress indicators
🏢 Enterprise Ready: Salesforce Agentforce support for regulated industries

🤖 Supported Agent Formats
✅ Auto-Detected Formats

OpenAI Assistants - model + instructions pattern
Google ADK - Agent Development Kit for multi-agent orchestration
MCP Servers - Model Context Protocol agents
Letta (MemGPT) - Memory-enabled autonomous agents
IBM Agent Control Protocol - Enterprise agent standard
AutoGPT - Autonomous goal-driven agents
Salesforce Agentforce - Enterprise digital labor platform

🔜 Coming Soon

CrewAI multi-agent systems
LangChain agents
Custom formats via plugins

💻 Usage Examples
Basic Registration

**Jarred Sumner**: "Save that, then let's clean up and commit everything:"

```bash
# Clean up backup files
rm astrasync/core.py.backup
rm astrasync/utils/trust_score.py.backup

# Check final status
git status

# Add everything
git add .

# Commit with comprehensive message
git commit -m "feat: Add Google ADK support to Python SDK

- Add Google ADK detection patterns (schemas, agent_type, objects)
- Fix detection order (ADK before OpenAI to prevent false matches)  
- Handle string and dict tool formats in normalization
- Add ADK-specific trust score bonuses (+5% structured output, +3% orchestration, +2% session management)
- Fix owner field defaulting in registration
- Add comprehensive examples in examples/register_google_adk.py
- Add full test coverage in test_all_protocols.py
- Update README to include Google ADK in supported formats

Google ADK agents now fully supported with auto-detection."

# Tag as version 0.2.0
git tag -a v0.2.0 -m "Version 0.2.0 - Google ADK support"

# Push everything
git push origin main --tags
