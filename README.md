# 🚀 SaaS Assistant: Software-Team-in-a-Box

A multi-agent AI workforce that handles the entire software development lifecycle — from requirements gathering to remote test execution and code review. Powered by **Agno**, **LiteLLM**, **Airweave**, and **Railway**.

---

## 🧠 The Workforce

| Agent       | Role                  | Primary Model                       | What It Does                                                     |
|-------------|-----------------------|-------------------------------------|------------------------------------------------------------------|
| **Manager** | Intent Router         | Gemini 2.5 Flash (via OpenRouter)   | Gathers context from Airweave & Mem0, produces a `TaskTicket`.   |
| **Architect** | Technical Planner   | Kimi K2 (via OpenRouter)            | Designs the `ArchitectureSpec` with file changes and test plans. |
| **Developer** | Code Executor       | GLM-4.7 (via Z.ai)                 | Implements changes using `FileTools`, outputs a `CodePatch`.     |
| **Tester**  | QA Engineer           | Ministral 8B (via OpenRouter)       | Runs code in Railway Sandbox, returns `TestResult`.              |
| **Critic**  | Security Reviewer     | Gemini 2.5 Flash (via OpenRouter)   | Scores security & maintainability, outputs a `ReviewReport`.     |

All agents communicate via strict **Pydantic schemas** — no free-form text handoffs.

---

## 🛠️ Tech Stack

| Layer            | Technology                                    |
|------------------|-----------------------------------------------|
| Orchestration    | **Agno** (Multi-Agent framework)              |
| Model Gateway    | **LiteLLM** Proxy (OpenRouter, Z.ai, Ollama)  |
| Persistence      | **PostgreSQL** (state) & **Redis** (cache)    |
| External Context | **Airweave** (code/docs) & **Mem0** (prefs)   |
| Code Execution   | **Railway Sandbox** (ComputeSDK)              |
| Observability    | **Langfuse** (trace monitoring)               |
| API Framework    | **FastAPI** + **Uvicorn**                     |

---

## 📁 Project Structure

```
saas-assistant/
├── main.py                     # Uvicorn entry point
├── Dockerfile                  # Container image
├── docker-compose.yml          # Full stack orchestration
├── pyproject.toml              # Python dependencies
├── gateway/
│   └── litellm_config.yaml     # Model routing & fallback chains
├── src/
│   ├── api/
│   │   └── main.py             # FastAPI app (/health, /ask)
│   ├── agents/
│   │   ├── base.py             # BaseAgent → LiteLLM proxy
│   │   ├── manager.py          # Intent Router
│   │   ├── architect.py        # Technical Planner
│   │   ├── developer.py        # Code Executor
│   │   ├── tester.py           # QA Engineer + Sandbox
│   │   ├── critic.py           # Security Reviewer
│   │   └── team.py             # AssistantTeam orchestrator
│   ├── schemas/
│   │   └── workflow.py         # Pydantic models (TaskTicket, etc.)
│   ├── execution/
│   │   └── sandbox.py          # SandboxManager (Railway bridge)
│   └── memory/
│       ├── airweave_client.py   # Airweave retrieval
│       ├── mem0_client.py       # Mem0 preference memory
│       └── session.py           # Redis session manager
├── tests/
│   ├── test_api.py             # FastAPI health check tests
│   └── test_sandbox.py         # Sandbox validation
└── docs/
    ├── Architecture and Setup Plan.md
    ├── API.md                  # API reference
    └── DEPLOYMENT.md           # Deployment guide
```

---

## ⚡ Quick Start

### Docker (Recommended)

```bash
# 1. Configure environment
cp .env.example .env
# Edit .env with your API keys

# 2. Launch everything
docker-compose up --build

# 3. Test
curl http://localhost:8000/health
```

### Local Development

```bash
# 1. Create virtual environment
python -m venv .venv && source .venv/bin/activate
pip install -e .

# 2. Start infrastructure
docker-compose up litellm postgres redis -d

# 3. Run the API
python main.py

# 4. Run tests
PYTHONPATH=. pytest tests/
```

---

## 🔌 API Usage

### Health Check
```bash
curl http://localhost:8000/health
# → {"status": "ok", "version": "0.1.0"}
```

### Trigger the Team
```bash
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Add a /users endpoint with CRUD operations", "user_id": "harish"}'
```

See [docs/API.md](docs/API.md) for the full API reference.

---

## 📊 Observability

All agent interactions are automatically traced and grouped by `session_id` in **Langfuse**:
- Token usage and costs per agent per request.
- Full trace of the Manager → Architect → Developer → Tester → Critic pipeline.
- Sandbox execution logs and exit codes.

---

## 🔑 Required API Keys

| Key                    | Provider    | Purpose                                |
|------------------------|-------------|----------------------------------------|
| `OPENROUTER_API_KEY`   | OpenRouter  | Primary LLM provider                   |
| `ZAI_API_KEY`          | Z.ai        | GLM-4.7 coding model                   |
| `LANGFUSE_PUBLIC_KEY`  | Langfuse    | Observability tracing                   |
| `LANGFUSE_SECRET_KEY`  | Langfuse    | Observability tracing                   |
| `AIRWEAVE_API_KEY`     | Airweave    | Project context retrieval               |
| `MEM0_API_KEY`         | Mem0        | User preference memory                  |
| `GITHUB_PAT`           | GitHub      | Repository access (Developer agent)     |

See [`.env.example`](.env.example) for the full template.

---

## 📚 Documentation

- [Architecture & Setup Plan](docs/Architecture%20and%20Setup%20Plan.md) — Full system design, model matrix, and phased build plan.
- [API Reference](docs/API.md) — Endpoints, request/response schemas, and examples.
- [Deployment Guide](docs/DEPLOYMENT.md) — Docker, Railway, and production deployment instructions.
- [Contributing](CONTRIBUTING.md) — How to contribute to the project.
- [Changelog](CHANGELOG.md) — Release history and version notes.

---

## 📄 License

MIT
