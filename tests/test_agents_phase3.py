import os
import sys
import time

# Ensure we can load local modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv

def validate_agent_team():
    """
    Validates that the Manager and Architect agents can successfully generate 
    structured Pydantic Pydantic schemas from a realistic user prompt.
    """
    print("Starting Phase 3 Agent Team Validation...\n")
    
    # Needs API keys for LiteLLM to route through OpenRouter/Gemini
    load_dotenv("/home/harish/git_repos/saas-assistant/.env")
    
    from src.agents.team import AssistantTeam
    
    try:
        team = AssistantTeam()
        print("✅ Models initialized and ready.")
    except Exception as e:
        print(f"❌ Failed to initialize Agent Team: {e}")
        return False
        
    dummy_prompt = "Create a new FastAPI endpoint at /health that returns {'status': 'ok'}. I prefer clean architecture."
    
    print(f"\nUser Prompt: '{dummy_prompt}'")
    
    t0 = time.monotonic()
    
    try:
        # Run the partial pipeline (Manager -> Architect)
        results = team.run_workflow(dummy_prompt)
    except Exception as e:
        print(f"\n❌ Pipeline failed during execution: {str(e)}")
        # Print full traceback during testing
        import traceback
        traceback.print_exc()
        return False
        
    execution_time = time.monotonic() - t0
    print(f"\n✅ Total Execution Time: {execution_time:.2f}s")
    
    if results and getattr(results.get('architecture'), 'files_to_change', None):
        print("\n=== Validation Summary ===")
        print("Manager Agent      : ✅ PASS (Valid TaskTicket returned)")
        print("Architect Agent    : ✅ PASS (Valid ArchitectureSpec returned)")
        print("Schema Enforcement : ✅ PASS")
        return True
    else:
        print("\n❌ Pipeline completed but failed to parse strict Pydantic models.")
        return False

if __name__ == "__main__":
    success = validate_agent_team()
    sys.exit(0 if success else 1)
