from ddgs import DDGS

class WebSearchTool:
    """
    A tool to perform web searches using the DuckDuckGo Search API via the `ddgs` library.
    It's designed to be simple, dependency-free (no API key needed), and robust.
    """

    def search(self, query: str, max_results: int = 3) -> str:
        """
        Performs a web search for the given query and returns a concatenated
        string of the top search result snippets.

        Args:
            query: The search query string.
            max_results: The maximum number of search results to retrieve.

        Returns:
            A single string containing the bodies (snippets) of the search results,
            separated by a clear delimiter. This format is ideal for an LLM to read
            and summarize. Returns a specific "No information found." message if
            the search yields no results or fails.
        """
        print(f"--- TOOL: Performing web search for query: '{query}' ---")
        try:
            with DDGS() as ddgs:

                # The 'backend="lite"' can sometimes be faster and more reliable for simple text searches.
                results = [r['body'] for r in ddgs.text(query, max_results=max_results, backend="lite")]
            
            # Check if the search actually returned anything.
            if not results:
                print("--- TOOL: Web search returned no results. ---")
                return "No information found for the specified query."

            # Join the results with a clear separator for the LLM to easily parse.
            return "\n\n---\n\n".join(results)
            
        except Exception as e:
            # Catch any potential exceptions from the ddgs library (e.g., network issues).
            print(f"ERROR in WebSearchTool during search for '{query}': {e}")
            return "An error occurred during the web search."