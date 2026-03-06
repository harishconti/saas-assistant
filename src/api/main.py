import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, Any

from src.agents.team import AssistantTeam

app = FastAPI(
    title="SaaS Assistant API",
    description="REST API for the Agno-based Multi-Agent Software Team",
    version="0.1.0"
)

# Initialize the team
# Note: In a production environment, we might want to handle this as a dependency
# or within a lifespan event to manage resources.
team = AssistantTeam()

class AssistantRequest(BaseModel):
    prompt: str
    user_id: Optional[str] = "default_user"

class AssistantResponse(BaseModel):
    status: str
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None

@app.get("/health")
def health_check():
    return {"status": "ok", "version": "0.1.0"}

@app.post("/ask", response_model=AssistantResponse)
async def ask_assistant(request: AssistantRequest):
    """
    Main endpoint to interact with the SaaS Assistant Team.
    Triggers the Manager -> Architect -> Developer -> Tester -> Critic pipeline.
    """
    import uuid
    session_id = f"sess-{uuid.uuid4()}"
    
    try:
        # Initialize a fresh team with a unique session ID for this request
        # to ensure unified tracing in Langfuse.
        req_team = AssistantTeam(session_id=session_id)
        
        # Pass the prompt and user_id for context-aware execution
        result = req_team.run_workflow(request.prompt, user_id=request.user_id)
        
        # We need to ensure the result is JSON serializable
        # Pydantic models in the result dict need to be dumped to dicts
        serializable_result = {}
        for key, value in result.items():
            if hasattr(value, "model_dump"):
                serializable_result[key] = value.model_dump()
            else:
                serializable_result[key] = value

        return AssistantResponse(status="success", result=serializable_result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
