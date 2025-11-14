from crewai.tools import BaseTool
import requests
import os
from typing import Type
from pydantic import BaseModel, Field

class GoogleSearchInput(BaseModel):
    """Input schema for Google Search."""
    query: str = Field(..., description="Search query")

class MCPGoogleSearchTool(BaseTool):
    name: str = "Google Search"
    description: str = "Search for information on Google. Useful for finding documentation, articles, use cases and general information about technologies."
    args_schema: Type[BaseModel] = GoogleSearchInput
    
    def _run(self, query: str) -> str:
        """Execute Google search via MCP."""
        try:
            url = os.getenv('GOOGLE_SEARCH_MCP_URL')
            key = os.getenv('GOOGLE_SEARCH_MCP_KEY')
            
            headers = {
                'Authorization': f'Bearer {key}',
                'Content-Type': 'application/json'
            }
            
            payload = {
                'query': query,
                'num_results': 10
            }
            
            response = requests.post(f"{url}/search", json=payload, headers=headers, timeout=30)
            response.raise_for_status()
            
            results = response.json()
            
            # Format results
            formatted_results = []
            for idx, result in enumerate(results.get('results', [])[:5], 1):
                formatted_results.append(
                    f"{idx}. {result.get('title', 'N/A')}\n"
                    f"   URL: {result.get('url', 'N/A')}\n"
                    f"   Snippet: {result.get('snippet', 'N/A')}\n"
                )
            
            return "\n".join(formatted_results)
            
        except Exception as e:
            return f"Search error: {str(e)}"