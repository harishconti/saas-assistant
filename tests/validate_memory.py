import os
import sys
import time
from dotenv import load_dotenv

import redis
from mem0 import Memory
from src.memory.mem0_client import Mem0Manager
from src.memory.session import get_redis_storage
from src.memory.airweave_client import AirweaveRetriever

# Load environment variables (API keys)
load_dotenv("/home/harish/git_repos/saas-assistant/.env")

def test_mem0():
    print("--- Testing Mem0 Storage ---")
    if not os.getenv("MEM0_API_KEY"):
        print("❌ MEM0_API_KEY is not set in .env")
        return False
        
    try:
        manager = Mem0Manager()
        test_user = "test_user_memory_agent"
        test_fact = "The user prefers to write configuration files in YAML."
        
        print(f"⏳ Saving preference for {test_user}...")
        t = time.monotonic()
        saved = manager.save_preference(test_user, test_fact)
        if not saved:
            print("❌ Failed to save preference.")
            return False
        print(f"✅ Saved in {time.monotonic()-t:.2f}s")
        
        print(f"⏳ Retrieving preferences for {test_user}...")
        t = time.monotonic()
        prefs = manager.get_preferences(test_user)
        print(f"✅ Retrieved in {time.monotonic()-t:.2f}s:")
        print(f"   \"{prefs.replace(chr(10), ' | ')}\"")
        
        if "YAML" in prefs:
            print("✅ Mem0 test PASSED.")
            return True
        else:
            print("❌ Retrieved preferences did not contain the saved fact.")
            return False
            
    except Exception as e:
        print(f"❌ Mem0 test failed with exception: {str(e)}")
        return False

def test_redis():
    print("\n--- Testing Redis (Conversational Memory) ---")
    try:
        r = redis.from_url(os.getenv("REDIS_URL", "redis://localhost:6379/0"))
        print("⏳ Pinging Redis server...")
        t = time.monotonic()
        if r.ping():
            print(f"✅ Ping successful in {time.monotonic()-t:.2f}s")
            
            # Test Agno compatibility layer via our wrapper
            print("⏳ Testing Agno RedisAgentStorage init...")
            storage = get_redis_storage(session_id="test_session_123")
            if storage:
                print("✅ Agno Redis storage initialized successfully.")
                print("✅ Redis test PASSED.")
                return True
        else:
            print("❌ Redis ping failed.")
            return False
    except redis.exceptions.ConnectionError:
        print("❌ Connection to Redis failed. Is it running? (run 'docker-compose up -d redis')")
        return False
    except Exception as e:
        print(f"❌ Redis test failed with exception: {str(e)}")
        return False

def test_airweave():
    print("\n--- Testing Airweave (Project Context) ---")
    if not os.getenv("AIRWEAVE_API_KEY"):
        print("❌ AIRWEAVE_API_KEY is not set in .env")
        return False
        
    try:
        retriever = AirweaveRetriever()
        print(f"⏳ Searching Airweave collection '{retriever.collection_name}'...")
        t = time.monotonic()
        
        # Search for something very generic that should exist in a code base/docs
        context = retriever.search_context("backend architecture")
        
        print(f"✅ Search completed in {time.monotonic()-t:.2f}s")
        if "Failed" in context or "Airweave Search Error" in context:
            print(f"❌ Airweave test failed: {context}")
            return False
            
        print("   Snippet preview:")
        print("   " + "\n   ".join(context[:300].splitlines()) + "...\n")
        print("✅ Airweave test PASSED.")
        return True
    except Exception as e:
        print(f"❌ Airweave test failed with exception: {str(e)}")
        return False

if __name__ == "__main__":
    print(f"Starting Phase 2 Memory Validation...\n")
    
    mem0_ok = test_mem0()
    redis_ok = test_redis()
    airweave_ok = test_airweave()
    
    print("\n=== Validation Summary ===")
    print(f"Mem0     : {'✅ PASS' if mem0_ok else '❌ FAIL'}")
    print(f"Redis    : {'✅ PASS' if redis_ok else '❌ FAIL'}")
    print(f"Airweave : {'✅ PASS' if airweave_ok else '❌ FAIL'}")
    
    if mem0_ok and redis_ok and airweave_ok:
        print("\nReady to proceed to Phase 3!")
        sys.exit(0)
    else:
        print("\nSome tests failed. Check logs above.")
        sys.exit(1)
    
    mem0_ok = test_mem0()
    redis_ok = test_redis()

