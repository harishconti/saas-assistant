import sys
import os
import asyncio
from dotenv import load_dotenv

# Ensure we can load local modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

load_dotenv()

from src.execution.sandbox import SandboxManager

async def validate_sandbox():
    """
    Tests the SandboxManager by executing a simple 'echo' command.
    Checks if it falls back to mock or hits a real endpoint.
    """
    print("Starting Sandbox Validation...")
    
    # Check if env vars are present
    endpoint = os.getenv("SANDBOX_ENDPOINT_URL")
    if not endpoint:
        print("ℹ️ SANDBOX_ENDPOINT_URL not set. Running in MOCK mode.")
    else:
        print(f"🚀 Targeting remote sandbox: {endpoint}")

    manager = SandboxManager()
    
    test_command = "echo 'Hello from SaaS Assistant Sandbox'"
    print(f"Executing command: {test_command}")
    
    result = await manager.execute_command(test_command)
    
    print("\n--- Execution Result ---")
    print(f"Exit Code: {result.get('exit_code')}")
    print(f"STDOUT: {result.get('stdout')}")
    print(f"STDERR: {result.get('stderr')}")
    print("------------------------")
    
    if result.get("exit_code") == 0 and "Hello" in result.get("stdout", ""):
        print("\n✅ Sandbox validation PASSED!")
        return True
    else:
        print("\n❌ Sandbox validation FAILED!")
        return False

if __name__ == "__main__":
    success = asyncio.run(validate_sandbox())
    sys.exit(0 if success else 1)
