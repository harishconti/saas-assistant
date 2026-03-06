import os
from airweave import AirweaveSDK, SearchRequest

class AirweaveRetriever:
    """
    Manages semantic search against the project's codebase and documentation
    using Airweave. Used by the Manager and Architect agents for context.
    """
    def __init__(self, collection_name: str = None):
        self.api_key = os.getenv("AIRWEAVE_API_KEY")
        self.base_url = os.getenv("AIRWEAVE_BASE_URL", "https://api.airweave.ai")
        # Ensure we have the user's provided collection ID
        self.collection_name = collection_name or "basecollection-bl0ujv"
        
        # Initialize the Airweave client
        self.client = AirweaveSDK(
            api_key=self.api_key,
            base_url=self.base_url
        )

    def search_context(self, query: str, limit: int = 5) -> str:
        """
        Searches the Airweave collection for snippets matching the query.
        Returns a formatted Markdown string.
        """
        if not self.collection_name:
            return "Airweave context disabled (no collection ID provided)."
            
        try:
            # Execute the semantic search
            results = self.client.collections.search(
                readable_id=self.collection_name,
                request=SearchRequest(query=query),
            )
            
            # The exact response structure depends on the SDK version, we'll access safely
            search_results = getattr(results, 'results', getattr(results, 'data', []))
            
            if not search_results:
                return "No contextual results found in Airweave."
                
            # Format the output for the LLM context window
            formatted_chunks = []
            for item in search_results[:limit]:
                source = getattr(item, 'source', 'Unknown Source')
                metadata = getattr(item, 'metadata', {})
                url = metadata.get('url', source) if isinstance(metadata, dict) else source
                content = getattr(item, 'text', '')
                
                chunk_str = f"### Source: {url}\n```\n{content}\n```\n"
                formatted_chunks.append(chunk_str)
                
            return "## Project Context (from Airweave)\n\n" + "\n".join(formatted_chunks)
            
        except Exception as e:
            err_msg = str(e)
            if "Collection has no sources" in err_msg:
                return "Airweave collection has no data sources attached yet. Returning empty context."
            print(f"Airweave Search Error: {err_msg}")
            return f"Failed to retrieve context from Airweave: {err_msg}"
