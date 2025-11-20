from pydantic import BaseModel, Field
from agents import function_tool
from init_agent import initAgent

INSTRUCTIONS = (
    "You are a senior researcher tasked with writing a cohesive report for a research query. "
    "You will be provided with the original query, and some initial research done by a research assistant.\n"
    "You should first come up with an outline for the report that describes the structure and "
    "flow of the report. Then, generate the report and return that as your final output.\n"
    "The final output should be in markdown format, and it should be lengthy and detailed. Aim "
    "for 5-10 pages of content, at least 1000 words.\n"
    "For each distinct topic in the report, include web search links to Google.com and YouTube.com for further research that open "
    "in a new tab.  Example of a 'Further Research' section in MarkDown format with links to Google and YouTube:\n"
    "Further Research:\n [Google](link) | [YouTube](link)"
)


class ReportData(BaseModel):
    short_summary: str = Field(description="A short 2-3 sentence summary of the findings.")

    markdown_report: str = Field(description="The final report")

    follow_up_questions: list[str] = Field(description="Suggested topics to research further")


@function_tool
def submit_report(short_summary: str, markdown_report: str, follow_up_questions: list[str]) -> dict:
    """Write a report based on the query and search results.
    
    Args:
        short_summary (str): A short 2-3 sentence summary of the findings.
        markdown_report (str): The final report.
        follow_up_questions (list[str]): Suggested topics to research further.

    Returns:
        ReportData: A report data object.
    
    """
    report = ReportData(short_summary=short_summary, markdown_report=markdown_report, follow_up_questions=follow_up_questions)
    return report.model_dump_json()

def getWriterAgent():
    agent = initAgent(
        name="WriterAgent",
        instructions=INSTRUCTIONS,
        tools=[submit_report],
        output_type=None,
    )
    agent.tool_use_behavior = "stop_on_first_tool"
    return agent