# Deployment Guide

This guide covers deploying the SaaS Assistant to various environments.

---

## Local Development (Docker Compose)

The simplest way to run the full stack locally:

```bash
# 1. Configure environment
cp .env.example .env
# Edit .env with your API keys

# 2. Start all services
docker-compose up --build

# 3. Verify
curl http://localhost:8000/health
```

### Services Started

| Service       | Port   | Description                             |
|---------------|--------|-----------------------------------------|
| `app`         | `8000` | FastAPI server (SaaS Assistant API)     |
| `litellm`     | `4000` | LiteLLM Proxy (model gateway)          |
| `postgres`    | `5432` | PostgreSQL (task state, metadata)       |
| `redis`       | `6379` | Redis (session cache)                   |

### Starting Only Infrastructure

If you want to run the Python app locally (for faster iteration) but use Docker for the backing services:

```bash
# Start only infrastructure
docker-compose up litellm postgres redis -d

# Run the app locally
python main.py
```

---

## Railway Deployment

### Prerequisites
- Railway account and CLI installed: `npm i -g @railway/cli`
- Railway project created with Postgres and Redis add-ons.

### Steps

1. **Link the project**:
   ```bash
   railway login
   railway link
   ```

2. **Set environment variables** in the Railway dashboard:
   - All keys from `.env.example`
   - Set `LITELLM_PROXY_URL` to the internal URL of your LiteLLM service.

3. **Deploy**:
   ```bash
   railway up
   ```

4. **Verify**:
   ```bash
   curl https://<your-app>.up.railway.app/health
   ```

### Service Architecture on Railway

```
┌──────────────────────────────────────────────┐
│                Railway Project                │
│                                              │
│  ┌──────────┐  ┌──────────┐  ┌───────────┐  │
│  │ FastAPI   │  │ LiteLLM  │  │ Sandbox   │  │
│  │ (app)     │──│ (proxy)  │  │ (executor)│  │
│  └──────────┘  └──────────┘  └───────────┘  │
│       │              │                       │
│  ┌──────────┐  ┌──────────┐                  │
│  │ Postgres  │  │  Redis   │                  │
│  │ (managed) │  │ (managed)│                  │
│  └──────────┘  └──────────┘                  │
└──────────────────────────────────────────────┘
```

---

## Environment Variables

All environment variables are documented in [`.env.example`](../.env.example). The critical ones are:

| Variable               | Required | Purpose                                |
|------------------------|----------|----------------------------------------|
| `OPENROUTER_API_KEY`   | ✅       | Primary LLM provider                   |
| `ZAI_API_KEY`          | ✅       | Z.ai GLM-4.7 coding model              |
| `LITELLM_MASTER_KEY`   | ✅       | LiteLLM proxy auth                     |
| `LANGFUSE_PUBLIC_KEY`  | ✅       | Observability tracing                   |
| `LANGFUSE_SECRET_KEY`  | ✅       | Observability tracing                   |
| `POSTGRES_PASSWORD`    | ✅       | Database authentication                 |
| `AIRWEAVE_API_KEY`     | ✅       | Project context retrieval               |
| `MEM0_API_KEY`         | ✅       | User preference memory                  |
| `GITHUB_PAT`           | ✅       | Repository access                       |
| `SANDBOX_ENDPOINT_URL` | ❌       | Railway Sandbox URL (mock if unset)     |
| `SANDBOX_API_KEY`      | ❌       | Railway Sandbox auth (mock if unset)    |

---

## Health Checks

All services include health checks:

| Service  | Endpoint                          | Method |
|----------|-----------------------------------|--------|
| App      | `http://localhost:8000/health`    | GET    |
| LiteLLM  | `http://localhost:4000/health`    | GET    |
| Postgres | `pg_isready` (Docker healthcheck) | CLI    |
| Redis    | `redis-cli ping` (Docker healthcheck) | CLI |

---

## Scaling

- **Horizontal**: Run multiple `app` instances behind a load balancer. Each request creates its own `AssistantTeam` with a unique `session_id`.
- **Vertical**: Increase Railway instance resources for LiteLLM proxy if throughput is a concern.
- **Model Routing**: Adjust `gateway/litellm_config.yaml` to add/remove model fallbacks based on cost and performance needs.
