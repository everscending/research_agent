from pydantic import BaseModel, Field
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


writer_agent = initAgent(
    name="WriterAgent",
    instructions=INSTRUCTIONS,
    output_type=ReportData
)