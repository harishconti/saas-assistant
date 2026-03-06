from src.agents.base import BaseAgent
from src.schemas.workflow import ArchitectureSpec

class ArchitectAgent(BaseAgent):
    """
    Requirements Engineer / Planner.
    Takes the TaskTicket from the Manager and turns it into a detailed technical
    specification (`ArchitectureSpec`) guiding the Developer exactly what files to modify.
    """
    def __init__(self, **kwargs):
        super().__init__(
            role_name="Architect",
            # We use an alias 'architect-model' defined in Litellm aiming at Claude/Kimi
            model_id="architect-model", 
            description="You are a Staff Software Engineer. You translate high-level TaskTickets into concrete execution blueprints.",
            instructions=[
                "1. Read the provided TaskTicket containing the user's goal, their preferences, and project context.",
                "2. Determine precisely which files need to be created, modified, or deleted.",
                "3. Outline the internal logic for those files.",
                "4. Define exactly what the Tester agent needs to assert to prove this feature works.",
                "5. Ensure the design satisfies any stylistic preferences defined in the ticket."
            ],
            output_schema=ArchitectureSpec,
            **kwargs
        )
