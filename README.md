# 🚀 SaaS Assistant: Software-Team-in-a-Box

A powerful, multi-agent AI workforce designed to handle the entire software development lifecycle—from requirements gathering to remote execution and testing. Powered by **Agno**, **LiteLLM**, and **Railway**.

## 🧠 The Workforce
- **Manager**: Gathers context from Airweave and Mem0 to define the mission.
- **Architect**: Designs the technical specification and file structure.
- **Developer**: Implements the code changes using specialized FileTools.
- **Tester**: Executes tests in a remote **Railway Sandbox** (Compute Layer).
- **Critic**: Performs security and maintainability reviews.

## 🛠️ Tech Stack
- **Orchestration**: Agno (Multi-Agent framework)
- **Model Gateway**: LiteLLM Proxy (Unified routing to Gemini, OpenRouter, etc.)
- **Persistence**: PostgreSQL (State) & Redis (Flash memory)
- **External Context**: Airweave (Project context) & Mem0 (User preferences)
- **Execution**: Railway Sandbox (Isolated remote environments)
- **Observability**: Langfuse (Full-trace completion monitoring)

## ⚡ Quick Start (Docker)

The easiest way to run the entire stack is via Docker Compose:

1. **Configure Environment**:
   Duplicate `.env.example` to `.env` and fill in your API keys (LiteLLM, Langfuse, Railway, etc.).

2. **Launch the Box**:
   ```bash
   docker-compose up --build
   ```

3. **Interact via API**:
   The Assistant API will be available at `http://localhost:8000`.
   - **Health Check**: `GET /health`
   - **Trigger Team**: `POST /ask`
     ```json
     {
       "prompt": "Add a new endpoint to handle user profile uploads."
     }
     ```

## 🧪 Development & Testing

### Local Setup
```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

### Running Tests
- **API Tests**: `pytest tests/test_api.py`
- **Sandbox Validation**: `python tests/test_sandbox.py`

## 📊 Observability
All agent interactions are automatically tracked and grouped by `session_id` in your **Langfuse** dashboard. This includes:
- Token usage and costs per agent.
- Detailed step-by-step trace of the Manager -> Critic pipeline.
- Execution logs from the remote Sandbox.

## 📄 License
MIT
