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
    def __init__(self, session_id: str = "default-session"):
        self.manager = ManagerAgent(session_id=session_id)
        self.architect = ArchitectAgent(session_id=session_id)
        self.developer = DeveloperAgent(session_id=session_id)
        self.tester = TesterAgent(session_id=session_id)
        self.critic = CriticAgent(session_id=session_id)

    def run_workflow(self, user_prompt: str, user_id: str = "default_user"):
        """
        Executes the main pipeline: 
        Manager -> Architect -> Developer -> Tester (Loop) -> Critic
        """
        print("\n" + "="*50)
        print(f"🧠 1. MANAGER: Processing Request (User: {user_id})")
        print("="*50)
        # Pass user_id to the manager run to fetch correct memories
        manager_resp = self.manager.run(user_prompt, user_id=user_id)
        ticket: TaskTicket = manager_resp.content if hasattr(manager_resp, 'content') else manager_resp
        
        # Ensure we have a valid pydantic object
        if not isinstance(ticket, TaskTicket):
            ticket = TaskTicket.model_validate(ticket)

        print(f"  🏷️ Intent: {ticket.intent}")

        print("\n" + "="*50)
        print("🏛️ 2. ARCHITECT: Drafting Specification")
        print("="*50)
        arch_resp = self.architect.run(ticket.model_dump_json())
        spec: ArchitectureSpec = arch_resp.content if hasattr(arch_resp, 'content') else arch_resp
        if not isinstance(spec, ArchitectureSpec):
            spec = ArchitectureSpec.model_validate(spec)
        
        print(f"  📝 Architectural Summary: {spec.summary}")

        # Developer-Tester Loop (Evaluation-Optimization)
        max_retries = 3
        current_patch = None
        test_result = None

        for i in range(max_retries):
            print("\n" + "="*50)
            print(f"💻 3.{i+1} DEVELOPER: Implementing Changes (Attempt {i+1})")
            print("="*50)
            
            dev_prompt = f"Architecture Spec:\n{spec.model_dump_json()}"
            if test_result and not test_result.passed:
                dev_prompt += f"\n\nPrevious implementation failed tests. Errors:\n{test_result.error_summary}"

            dev_resp = self.developer.run(dev_prompt)
            current_patch = dev_resp.content if hasattr(dev_resp, 'content') else dev_resp
            if not isinstance(current_patch, CodePatch):
                current_patch = CodePatch.model_validate(current_patch)

            print(f"  ✅ Developer provided patch for {len(current_patch.files_added) + len(current_patch.files_modified)} files.")

            print("\n" + "="*50)
            print(f"🧪 4.{i+1} TESTER: Validating in Sandbox")
            print("="*50)
            
            # Tester needs both the spec (to know what to test) and the patch (to know what changed)
            tester_prompt = f"Spec:\n{spec.model_dump_json()}\n\nPatch:\n{current_patch.model_dump_json()}"
            tester_resp = self.tester.run(tester_prompt)
            test_result = tester_resp.content if hasattr(tester_resp, 'content') else tester_resp
            if not isinstance(test_result, TestResult):
                test_result = TestResult.model_validate(test_result)

            if test_result.passed:
                print("  🎉 Tests PASSED!")
                break
            else:
                print(f"  ❌ Tests FAILED: {test_result.error_summary}")
        
        print("\n" + "="*50)
        print("⚖️ 5. CRITIC: Final Review")
        print("="*50)
        critic_prompt = f"Final Patch:\n{current_patch.model_dump_json()}\nTest Results:\n{test_result.model_dump_json() if test_result else 'N/A'}"
        critic_resp = self.critic.run(critic_prompt)
        review: ReviewReport = critic_resp.content if hasattr(critic_resp, 'content') else critic_resp
        if not isinstance(review, ReviewReport):
            review = ReviewReport.model_validate(review)
            
        print(f"  🛡️ Security Score: {review.security_score}/10")
        print(f"  📈 Maintainability: {review.maintainability_rating}")

        return {
            "ticket": ticket,
            "architecture": spec,
            "final_patch": current_patch,
            "test_result": test_result,
            "review": review
        }
