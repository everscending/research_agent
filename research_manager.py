import time
from agents import Runner, trace, gen_trace_id
from search_agent import getSearchAgent
from planner_agent import getPlannerAgent, WebSearchItem, WebSearchPlan
from writer_agent import getWriterAgent, ReportData
from email_agent import getEmailAgent
import asyncio

class ResearchManager:

    async def run(self, query: str):
        """ Run the deep research process, yielding the status updates and the final report"""
        trace_id = gen_trace_id()
        with trace("Research trace", trace_id=trace_id):
            start_time = time.perf_counter()

            print(f"View trace: https://platform.openai.com/traces/trace?trace_id={trace_id}")
            yield f"View trace: https://platform.openai.com/traces/trace?trace_id={trace_id}"
            print("Starting research...")
            search_plan = await self.plan_searches(query)
            yield "Searches planned, starting to search..."     
            search_results = await self.perform_searches_parallel(search_plan)
            
            print(f"search_results: {search_results}")

            yield "Searches complete, writing report..."
            report = await self.write_report(query, search_results)

            yield "Report written, sending email..."
            await self.send_email(report)
            yield "Email sent, research complete"
            yield report.markdown_report

            end_time = time.perf_counter()
            elapsed_time = end_time - start_time
            print(f"Total execution time: {elapsed_time:.4f} seconds")

        

    async def plan_searches(self, query: str) -> WebSearchPlan:
        """ Plan the searches to perform for the query """
        start_time = time.perf_counter()

        print("Planning searches...")
        result = await Runner.run(
            getPlannerAgent(),
            f"Query: {query}",
        )
        
        plan = WebSearchPlan.model_validate_json(result.final_output)
        print(f"Will perform {len(plan.searches)} searches")
        end_time = time.perf_counter()
        elapsed_time = end_time - start_time
        print(f"Execution time: {elapsed_time:.4f} seconds")
        return plan

    async def perform_searches_parallel(self, search_plan: WebSearchPlan) -> list[str]:
        """ Perform the searches to perform for the query """
        print("Searching...")

        tasks = [asyncio.create_task(self.search(item)) for item in search_plan.searches]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        successful_results = [result for result in results if result is not None]
        print(f"Finished searching. {len(successful_results)}/{len(results)} searches successful")
        return successful_results

    async def search(self, item: WebSearchItem) -> str | None:
        """ Perform a search for the query """
        input = f"Search term: {item.query}\nReason for searching: {item.reason}"
        try:
            start_time = time.perf_counter()

            result = await Runner.run(
                getSearchAgent(),
                input,
            )
            end_time = time.perf_counter()
            elapsed_time = end_time - start_time
            print(f"Search term: {item.query}, Execution time: {elapsed_time:.4f} seconds")

            return str(result.final_output)
        except Exception:
            return None

    async def write_report(self, query: str, search_results: list[str]) -> ReportData:
        """ Write the report for the query """
        
        input = f"Original query: {query}\nSummarized search results: {search_results}"
        print(f"Thinking about report...\n\n{input}")
        start_time = time.perf_counter()
        result = await Runner.run(
            getWriterAgent(),
            input,
        )

        report = ReportData.model_validate_json(result.final_output)
        print("Finished writing report")

        end_time = time.perf_counter()
        elapsed_time = end_time - start_time
        print(f"Execution time: {elapsed_time:.4f} seconds")
        
        return report
    
    async def send_email(self, report: ReportData) -> None:
        print("Writing email...")
        start_time = time.perf_counter()
        result = await Runner.run(
            getEmailAgent(),
            report.markdown_report,
        )
        print("Email sent")
        end_time = time.perf_counter()
        elapsed_time = end_time - start_time
        print(f"Execution time: {elapsed_time:.4f} seconds")
        return report