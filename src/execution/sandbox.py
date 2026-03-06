import os
import httpx
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv

load_dotenv()

class SandboxManager:
    """
    Manages isolated code execution using Railway's ComputeSDK / Sandbox environment.
    This allows the TesterAgent to run generated code safely in a remote container.
    """
    def __init__(self):
        # The user has the ComputeSDK endpoint running in Railway.
        # We assume it follows the standard sandbox API or the specific one 
        # deployed by the user.
        self.base_url = os.getenv("SANDBOX_ENDPOINT_URL")
        self.api_key = os.getenv("SANDBOX_API_KEY")
        
        if not self.base_url:
            print("WARNING: SANDBOX_ENDPOINT_URL not set. Sandbox execution will be mocked.")

    async def execute_command(self, command: str, files: Optional[List[Dict[str, str]]] = None) -> Dict[str, Any]:
        """
        Sends a command to the remote sandbox for execution.
        :param command: The shell command to run (e.g., 'pytest tests/test_feature.py')
        :param files: Periodic list of file updates to sync to the sandbox before running.
        :return: Dict containing stdout, stderr, and exit_code.
        """
        if not self.base_url:
            # Mock behavior if no remote endpoint is configured yet
            print(f"  [Sandbox Mock] Executing: {command}")
            return {
                "stdout": f"Mock output for: {command}\nSTDOUT: Success",
                "stderr": "",
                "exit_code": 0
            }

        payload = {
            "command": command,
            "files": files or []
        }
        
        headers = {
            "Authorization": f"Bearer {self.api_key}" if self.api_key else ""
        }

        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(
                    f"{self.base_url}/execute",
                    json=payload,
                    headers=headers
                )
                response.raise_for_status()
                return response.json()
        except Exception as e:
            return {
                "stdout": "",
                "stderr": f"Sandbox execution failed: {str(e)}",
                "exit_code": 1
            }

    def run_command_sync(self, command: str) -> str:
        """
        Synchronous wrapper for Agno tools.
        """
        import asyncio
        result = asyncio.run(self.execute_command(command))
        output = result.get("stdout", "")
        if result.get("stderr"):
            output += f"\nSTDERR: {result['stderr']}"
        return output
