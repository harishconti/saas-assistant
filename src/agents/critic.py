from src.agents.base import BaseAgent
from src.schemas.workflow import ReviewReport

class CriticAgent(BaseAgent):
    """
    Code Reviewer / Optimizer.
    Even if tests pass, the Critic performs a static analysis of the Developer's 
    work against the project's stylistic constraints and security standards.
    """
    def __init__(self, **kwargs):
        super().__init__(
            role_name="Critic",
            model_id="critic-model", # Routes to Gemini 2.5 Flash / strong reasoning
            description="You are an uncompromising Lead Security & Architecture Reviewer. Your job is to catch things that unit tests miss.",
            instructions=[
                "1. Review the original ArchitectureSpec and the final CodePatch.",
                "2. Look for hardcoded credentials, SQL injection risks, and performance bottlenecks.",
                "3. Enforce the user's coding style preferences strictly.",
                "4. Output a ReviewReport. If 'approved=False', provide actionable feedback."
            ],
            output_schema=ReviewReport,
            **kwargs
        )
