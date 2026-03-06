# Changelog

All notable changes to the SaaS Assistant project are documented here.

## [0.1.0] — 2026-03-06

### Added
- **Phase 1 — LiteLLM Gateway**: Configured LiteLLM proxy with virtual model routing (`intent-model`, `worker-model`, `developer-model`, `architect-model`, `critic-model`), fallback chains via OpenRouter/Z.ai/Ollama, and Langfuse observability callbacks.
- **Phase 2 — Retrieval & Memory**: Integrated Airweave for project context retrieval and Mem0 for long-term user preference memory. Created Redis session manager and PostgreSQL infrastructure via Docker Compose.
- **Phase 3 — Agent Roles & Team**: Implemented 5 Agno agents (Manager, Architect, Developer, Tester, Critic) with Pydantic schemas (`TaskTicket`, `ArchitectureSpec`, `CodePatch`, `TestResult`, `ReviewReport`) for strict inter-agent data contracts. Built the `AssistantTeam` orchestrator.
- **Phase 4 — Sandbox Integration**: Created `SandboxManager` for Railway ComputeSDK remote execution. Integrated into `TesterAgent` with mock fallback mode. Implemented the Developer ↔ Tester retry loop (up to 3 attempts).
- **Phase 5 — API & Observability**: Wrapped the orchestration in a FastAPI server (`POST /ask`, `GET /health`). Added per-request `session_id` for unified Langfuse tracing across all 5 agents. Updated `main.py` to serve via Uvicorn.
- **Containerization**: Added `Dockerfile` and integrated the `app` service into `docker-compose.yml` with health-check dependencies.
- **Documentation**: Created comprehensive `README.md`, `CONTRIBUTING.md`, `CHANGELOG.md`, `docs/API.md`, and `docs/DEPLOYMENT.md`. Aligned architecture document with actual provider usage (OpenRouter, Z.ai, Ollama).
