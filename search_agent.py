import os
from agents import ModelSettings, function_tool
from init_agent import initAgent
from serpapi import GoogleSearch

INSTRUCTIONS = (
    "You are a research assistant. Given a search term, use your google_search tool to search the web for that term and "
    "produce a concise summary of the results. The summary must be 2-3 paragraphs and less than 300 "
    "words. Capture the main points. Write succintly, no need to have complete sentences or good "
    "grammar. This will be consumed by someone synthesizing a report, so its vital you capture the "
    "essence and ignore any fluff. Do not include any additional commentary other than the summary itself."
)

@function_tool
def google_search(q:str):
    """A tool that lets the LLM search the web.
    
    Args:
        q (str): The query to search for

    Returns:
        str: A summary of the search results
    """

    params = {
        "engine": "google",
        "q": q,
        "api_key": os.environ.get("SERPAPI_API_KEY")
    }

    search = GoogleSearch(params)
    results = search.get_dict()
    organic_results = results["organic_results"]
    return organic_results

def getSearchAgent():

    return initAgent(
        name="Search agent",
        instructions=INSTRUCTIONS,
        tools=[google_search],
        model_settings=ModelSettings(tool_choice="required")
    )
