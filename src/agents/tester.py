from src.agents.base import BaseAgent
from src.schemas.workflow import TestResult

class TesterAgent(BaseAgent):
    """
    Evaluator.
    Takes the ArchitectureSpec constraints and the CodePatch from the Developer.
    Runs the sandbox environment to ensure the code works as expected.
    """
    def __init__(self, **kwargs):
        super().__init__(
            role_name="Tester",
            model_id="worker-model", # Routes to Ministral 8b (fast, good log parsing)
            description="You are a rigorous QA Engineer. You don't write the code; you run it, try to break it, and parse the logs.",
            instructions=[
                "1. Review the CodePatch provided by the Developer.",
                "2. Note the 'test_requirements' outlined in the ArchitectureSpec.",
                "3. Call your Sandbox tool (e.g., `execute_tests`) to run the checks.",
                "4. Parse the output logs.",
                "5. Return a strict TestResult containing 'passed=True' if everything is green, or a helpful 'error_summary' if it failed so the Developer can retry."
            ],
            tools=[self.execute_tests],
            output_schema=TestResult,
            **kwargs
        )

    def execute_tests(self, command: str) -> str:
        """
        Placeholder tool for Railway Sandbox execution.
        Currently returns a mocked success to allow the workflow to be tested.
        Phase 4 will replace this with actual ComputeSDK remote execution.
        """
        print(f"    [Tester executing sandbox command: {command}]")
        return "STDOUT: pytest execution complete. 1 passed, 0 failed.\nExit code: 0"
