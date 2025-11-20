from datetime import date
from pydantic import BaseModel, Field
from agents import ModelSettings, function_tool
from init_agent import initAgent

HOW_MANY_SEARCHES = 5

INSTRUCTIONS = f"You are a helpful research assistant. The current date in the format YYYY-MM-DD \
is {date.today().strftime('%Y-%m-%d')}. Given a query, come up with a set of web searches \
to perform to best answer the query. Devise exactly {HOW_MANY_SEARCHES} search terms, then call the \
`submit_search_plan` tool once with your finalized plan."

class WebSearchItem(BaseModel):
    reason: str = Field(description="Your reasoning for why this search is important to the query.")
    query: str = Field(description="The search term to use for the web search.")


class WebSearchPlan(BaseModel):
    searches: list[WebSearchItem] = Field(description="A list of web searches to perform to best answer the query.")


@function_tool
def submit_search_plan(searches: list[WebSearchItem]) -> dict:
    """Finalize and submit the web search plan.
    
    Args:
        searches (list[WebSearchItem]): A list of web searches to perform to best answer the query.

    Returns:
        WebSearchPlan: A web search plan.
    """

    plan = WebSearchPlan(searches=searches)

    print(f"plan: {plan}")
    return plan.model_dump_json()

def getPlannerAgent():
    agent = initAgent(
        name="PlannerAgent",
        instructions=INSTRUCTIONS,
        tools=[submit_search_plan],
        model_settings=ModelSettings(tool_choice="required"),
        output_type=None,
    )
    agent.tool_use_behavior = "stop_on_first_tool"
    return agent
