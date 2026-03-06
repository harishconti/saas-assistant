# Contributing to SaaS Assistant

Thank you for your interest in contributing! This guide will help you get started.

## Development Setup

```bash
# Clone the repo
git clone https://github.com/<your-org>/saas-assistant.git
cd saas-assistant

# Create virtual environment
python -m venv .venv
source .venv/bin/activate

# Install dependencies (editable mode)
pip install -e .

# Copy environment config
cp .env.example .env
# Fill in your API keys in .env
```

## Project Structure

- `src/agents/` — Agno agent implementations (Manager, Architect, Developer, Tester, Critic).
- `src/schemas/` — Pydantic models for inter-agent communication.
- `src/execution/` — SandboxManager for Railway remote execution.
- `src/memory/` — Airweave, Mem0, and Redis integration.
- `src/api/` — FastAPI application.
- `gateway/` — LiteLLM proxy configuration.
- `tests/` — Test suite.

## Adding a New Agent

1. Create `src/agents/your_agent.py` extending `BaseAgent`.
2. Define an output schema in `src/schemas/workflow.py`.
3. Register the agent in `src/agents/team.py`.
4. Add a corresponding model alias to `gateway/litellm_config.yaml`.

## Adding a New LLM Provider

1. Add the model deployment to `gateway/litellm_config.yaml` under the relevant model group.
2. Add the required API key to `.env.example`.
3. Test the routing via: `curl http://localhost:4000/chat/completions -d '{"model": "your-model-id", ...}'`

## Running Tests

```bash
# API tests
PYTHONPATH=. pytest tests/test_api.py -v

# Sandbox validation
PYTHONPATH=. python tests/test_sandbox.py
```

## Code Style

- Use type hints everywhere.
- All inter-agent data must use Pydantic models (no raw dicts).
- Follow the existing pattern in `src/agents/base.py` for new agents.

## Pull Request Process

1. Fork the repository and create a feature branch.
2. Make your changes with clear, descriptive commits.
3. Ensure all tests pass.
4. Submit a PR with a description of what changed and why.
