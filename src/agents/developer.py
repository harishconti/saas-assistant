from src.agents.base import BaseAgent
from src.schemas.workflow import CodePatch
from pathlib import Path
from agno.tools.file import FileTools

class DeveloperAgent(BaseAgent):
    """
    The Executor.
    Takes the precise ArchitectureSpec and actually writes/modifies the code.
    Reads current file states, applies changes, and outputs a CodePatch indicating
    it is ready for testing.
    """
    def __init__(self, **kwargs):
        # Tools: ability to read/write files (Agno built-in tools)
        # Note: Since this proxy sits locally for now, FileTools operates on the local disk.
        # Inside the Railway Sandbox, we will use a different environment for the Tester.
        file_tools = FileTools(base_dir=Path("."))
        
        super().__init__(
            role_name="Developer",
            model_id="developer-model", # Routes to GLM-4.7 / Qwen2.5-Coder via LiteLLM
            description="You are a 10x Staff Engineer. Your job is to execute ArchitectureSpecs rapidly and accurately without breaking existing invariants.",
            instructions=[
                "1. Read the provided ArchitectureSpec carefully.",
                "2. Use `read_file` to see the current state of any files you need to modify.",
                "3. Use `write_file` or `append_to_file` to implement the requested changes.",
                "4. When all files are updated according to the spec, output a structured CodePatch indicating readiness for the Tester."
            ],
            tools=[file_tools],
            output_schema=CodePatch,
            **kwargs
        )
