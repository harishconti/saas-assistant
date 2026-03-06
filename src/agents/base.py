import os
from typing import Optional
from agno.agent import Agent
from agno.models.openai import OpenAIChat

class BaseAgent(Agent):
    """
    A foundational Agno Agent pre-configured to point to our local LiteLLM proxy
    so that all agent requests flow through a unified logging/cost-tracking gateway.
    """
    def __init__(self, role_name: str, model_id: str, session_id: Optional[str] = None, **kwargs):
        # We assume LiteLLM proxy is running on localhost:4000 (as per docker-compose)
        # By using the OpenAI client, we can transparently route through LiteLLM.
        proxy_url = os.getenv("LITELLM_PROXY_URL", "http://localhost:4000")
        
        super().__init__(
            name=role_name,
            session_id=session_id,
            model=OpenAIChat(
                id=model_id,
                base_url=proxy_url,
                api_key="sk-1234" # Dummy key for local litellm proxy
            ),
            # Add base parameters like markdown tracking
            markdown=True,
            **kwargs
        )
