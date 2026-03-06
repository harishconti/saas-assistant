import os
from mem0 import Memory

class Mem0Manager:
    """
    Manages long-term user preferences and profile facts using Mem0.
    Used by the Manager (Intent Router) to pass stylistic and structural 
    preferences to the Architect and Developer agents.
    """
    def __init__(self):
        # Configure Mem0 to use LiteLLM (Gemini) instead of default OpenAI
        config = {
            "llm": {
                "provider": "litellm",
                "config": {
                    "model": "gemini/gemini-2.5-flash",
                }
            },
            "embedder": {
                "provider": "ollama",
                "config": {
                    "model": "nomic-embed-text:latest",
                }
            },
            "vector_store": {
                "provider": "qdrant",
                "config": {
                    "collection_name": "saas_assistant_mem0",
                    "embedding_model_dims": 768,
                }
            }
        }
        self.memory = Memory.from_config(config)
    def get_preferences(self, user_id: str) -> str:
        """
        Retrieves all stored preferences for a given user and formats them
        as a prompt-friendly string.
        """
        try:
            memories = self.memory.get_all(user_id=user_id)
            
            # Handle both list and dict returns (Mem0 versions differ)
            if isinstance(memories, dict) and "results" in memories:
                memories = memories["results"]
                
            if not memories:
                return "No specific user preferences found."
            
            prefs = [f"- {m['memory']}" for m in memories]
            return "User Preferences:\n" + "\n".join(prefs)
        except Exception as e:
            print(f"Mem0 Search Error: {e}")
            return "Failed to retrieve user preferences."

    def save_preference(self, user_id: str, text: str) -> bool:
        """
        Saves a new fact or preference about the user.
        """
        try:
            self.memory.add(text, user_id=user_id)
            return True
        except Exception as e:
            print(f"Mem0 Add Error: {e}")
            return False
