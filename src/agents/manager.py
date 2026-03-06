from src.agents.base import BaseAgent
from src.schemas.workflow import TaskTicket
from src.memory.mem0_client import Mem0Manager
from src.memory.airweave_client import AirweaveRetriever
from typing import Dict, Any

class ManagerAgent(BaseAgent):
    """
    The Intent Router.
    It takes the raw user prompt, fetches relevant memories (preferences & context),
    and normalizes everything into a strict TaskTicket for downstream agents.
    """
    def __init__(self, **kwargs):
        # Tools: Mem0 and Airweave access
        self.mem0 = Mem0Manager()
        self.airweave = AirweaveRetriever()
        
        super().__init__(
            role_name="Manager (Intent Router)",
            model_id="intent-model",  # Routes to Gemini 2.5 Flash / Llama 3.2 3B
            description="You are an expert technical manager. You understand what the user wants, retrieve their coding preferences, fetch relevant snippets from the codebase, and compile a clear TaskTicket.",
            instructions=[
                "1. Analyze the user's prompt.",
                "2. Call `get_user_preferences` to see how the user likes their code (e.g., specific frameworks, style).",
                "3. Call `search_codebase` using keywords from the prompt to find relevant files.",
                "4. Synthesize all this into a structured TaskTicket.",
            ],
            tools=[self.get_user_preferences, self.search_codebase],
            output_schema=TaskTicket,
            **kwargs
        )

    def get_user_preferences(self, user_name: str = "default_user") -> str:
        """Fetch coding style and architectural preferences for the user."""
        return self.mem0.get_preferences(user_name)

    def search_codebase(self, query: str) -> str:
        """Search the Airweave indexed codebase for context relating to the user's request."""
        return self.airweave.search_context(query)
