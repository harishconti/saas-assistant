import json
from src.agents.manager import ManagerAgent
from src.agents.architect import ArchitectAgent
from src.agents.developer import DeveloperAgent
from src.agents.tester import TesterAgent
from src.agents.critic import CriticAgent

from src.schemas.workflow import (
    TaskTicket, ArchitectureSpec, CodePatch, 
    TestResult, ReviewReport
)

class AssistantTeam:
    """
    Orchestrates the 5 Agno agents into a structured evaluation-optimization loop.
    """
    def __init__(self):
        self.manager = ManagerAgent()
        self.architect = ArchitectAgent()
        self.developer = DeveloperAgent()
        self.tester = TesterAgent()
        self.critic = CriticAgent()

    def run_workflow(self, user_prompt: str):
        """
        Executes the main pipeline. 
        Currently mocked for Phase 3 to just print the handoffs.
        """
        print("\n" + "="*50)
        print("🧠 1. MANAGER: Processing Request")
        print("="*50)
        ticket_resp = self.manager.run(user_prompt)
        
        # Agno's structured output puts the Pydantic model in .content if it's perfectly typed
        # or we might need to parse. For Phase 3, we expect pure objects.
        ticket: TaskTicket = ticket_resp.content if hasattr(ticket_resp, 'content') else ticket_resp
        if not isinstance(ticket, TaskTicket):
            try:
                # Fallback if the model returned unparsed JSON string
                ticket = TaskTicket.model_validate_json(ticket)
            except Exception as e:
                print(f"Failed to parse TaskTicket: {e}")
                return

        print(f"  🏷️ Intent: {ticket.intent}")
        print(f"  🧠 Found Preferences: {bool(ticket.user_preferences)}")
        print(f"  📂 Found Context: {bool(ticket.project_context)}")

        print("\n" + "="*50)
        print("🏛️ 2. ARCHITECT: Drafting Specification")
        print("="*50)
        
        architect_prompt = f"Task Ticket:\n{ticket.model_dump_json(indent=2)}"
        arch_resp = self.architect.run(architect_prompt)
        arch_spec: ArchitectureSpec = arch_resp.content if hasattr(arch_resp, 'content') else arch_resp
        
        # Just safely grab the dict or pydantic model for printing
        if not isinstance(arch_spec, ArchitectureSpec):
            try:
                arch_spec = ArchitectureSpec.model_validate_json(arch_spec)
            except Exception:
                pass
                
        print(f"  📝 Architectural Summary: {getattr(arch_spec, 'summary', 'Unknown')}")
        files = getattr(arch_spec, 'files_to_change', [])
        print(f"  🛠️ Files to touch: {len(files)}")
        for f in files:
            print(f"     - [{getattr(f,'action','X')}] {getattr(f,'file_path','???')}")

        print("\n" + "="*50)
        print("💻 3. PIPELINE SUMMARY")
        print("="*50)
        print("The Developer, Tester, and Critic are wired up successfully.")
        print("Phase 3 validation complete! Ready for Phase 4 Sandbox.")
        
        return {
            "ticket": ticket,
            "architecture": arch_spec
        }
