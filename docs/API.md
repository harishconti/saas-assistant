# API Reference

The SaaS Assistant exposes a REST API via FastAPI on port `8000`.

---

## Endpoints

### `GET /health`

Health check endpoint.

**Response** `200 OK`:
```json
{
  "status": "ok",
  "version": "0.1.0"
}
```

---

### `POST /ask`

Triggers the full multi-agent workflow: Manager → Architect → Developer → Tester (loop) → Critic.

**Request Body**:
```json
{
  "prompt": "Add a /users endpoint with CRUD operations",
  "user_id": "harish"
}
```

| Field     | Type   | Required | Default          | Description                              |
|-----------|--------|----------|------------------|------------------------------------------|
| `prompt`  | string | ✅       | —                | The task description for the agent team. |
| `user_id` | string | ❌       | `"default_user"` | User ID for Mem0 preference retrieval.   |

**Response** `200 OK`:
```json
{
  "status": "success",
  "result": {
    "ticket": {
      "intent": "feature_request",
      "user_preferences": "Prefers FastAPI, clean architecture",
      "project_context": "Existing app uses SQLAlchemy..."
    },
    "architecture": {
      "summary": "Add REST CRUD endpoints...",
      "files_to_change": [
        {"file_path": "src/api/users.py", "action": "create", "description": "New user endpoints"}
      ],
      "test_requirements": ["Unit tests for each CRUD operation"]
    },
    "final_patch": {
      "files_added": ["src/api/users.py"],
      "files_modified": ["src/api/main.py"],
      "summary": "Added /users endpoint with full CRUD..."
    },
    "test_result": {
      "passed": true,
      "error_summary": ""
    },
    "review": {
      "security_score": 8,
      "maintainability_rating": "A",
      "suggestions": ["Consider adding rate limiting"]
    }
  }
}
```

**Error Response** `500`:
```json
{
  "detail": "Connection error."
}
```

---

## Pydantic Schemas

All inter-agent data is enforced via strict Pydantic models defined in `src/schemas/workflow.py`:

| Schema             | Produced By | Consumed By       | Key Fields                                          |
|--------------------|-------------|--------------------|-----------------------------------------------------|
| `TaskTicket`       | Manager     | Architect          | `intent`, `user_preferences`, `project_context`     |
| `ArchitectureSpec` | Architect   | Developer, Tester  | `summary`, `files_to_change`, `test_requirements`   |
| `CodePatch`        | Developer   | Tester, Critic     | `files_added`, `files_modified`, `summary`          |
| `TestResult`       | Tester      | Developer (retry)  | `passed`, `error_summary`                           |
| `ReviewReport`     | Critic      | (Final output)     | `security_score`, `maintainability_rating`           |

---

## Authentication

The current API does **not** require authentication. For production, add an API key middleware or OAuth2 integration.

---

## Running the Server

```bash
# Local
python main.py

# Docker
docker-compose up app

# The API is available at http://localhost:8000
```
