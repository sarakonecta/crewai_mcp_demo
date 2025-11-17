from crewai.tools import BaseTool
import requests
import os
import logging
from typing import Type
from pydantic import BaseModel, Field

# Setup logging
logger = logging.getLogger(__name__)

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
            
            if not url or not key:
                return f"Error: Missing GOOGLE_SEARCH_MCP_URL or GOOGLE_SEARCH_MCP_KEY in environment"
            
            headers = {
                'Authorization': f'Bearer {key}',
                'Content-Type': 'application/json'
            }
            
            payload = {
                'query': query,
                'num_results': 10
            }
            
            endpoints = [
                f"{url}/tools/call",
                f"{url}/call",
                f"{url}/invoke",
                f"{url}/google_search",
                f"{url}/search",
                f"{url}/api/search",
                f"{url}/api/tools/call"
            ]
            
            response = None
            last_error = None
            
            for endpoint in endpoints:
                try:
                    logger.info(f"Trying endpoint: {endpoint}")
                    response = requests.post(endpoint, json=payload, headers=headers, timeout=30)
                    logger.info(f"Response status: {response.status_code}")
                    
                    # Accept 200-299 status codes
                    if 200 <= response.status_code < 300:
                        logger.info(f"Success with endpoint: {endpoint}")
                        break
                    else:
                        logger.warning(f"HTTP {response.status_code} on {endpoint}")
                        last_error = f"HTTP {response.status_code}"
                        response = None
                        
                except Exception as e:
                    logger.warning(f"Failed on {endpoint}: {str(e)}")
                    last_error = e
                    continue
            
            if response is None:
                # Try to get root to see available endpoints
                try:
                    logger.info(f"Trying GET {url}/ to discover endpoints")
                    root_response = requests.get(f"{url}/", headers=headers, timeout=10)
                    logger.info(f"Root response: {root_response.status_code} - {root_response.text[:500]}")
                except:
                    pass
                return f"Search error: Could not reach working endpoint. Last error: {str(last_error)}"
            
            results = response.json()
            logger.info(f"Response JSON: {str(results)[:200]}")
            
            # Format results - handle different response formats
            formatted_results = []
            
            # Try to extract results from different possible response structures
            result_list = None
            if isinstance(results, dict):
                result_list = results.get('results', []) or results.get('data', []) or results.get('content', [])
            elif isinstance(results, list):
                result_list = results
            
            if result_list:
                for idx, result in enumerate(result_list[:5], 1):
                    if isinstance(result, dict):
                        formatted_results.append(
                            f"{idx}. {result.get('title', result.get('name', 'N/A'))}\n"
                            f"   URL: {result.get('url', result.get('link', 'N/A'))}\n"
                            f"   Snippet: {result.get('snippet', result.get('description', 'N/A'))}\n"
                        )
                    else:
                        formatted_results.append(f"{idx}. {str(result)}\n")
            
            return "\n".join(formatted_results) if formatted_results else f"No results formatted. Raw response: {str(results)[:300]}"
            
        except Exception as e:
            logger.error(f"Search error: {str(e)}", exc_info=True)
            return f"Search error: {str(e)}"