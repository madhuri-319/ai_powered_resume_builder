from google.adk import Agent
from mcp_tools.mcp_server  import search_employees, get_resume_paths, create_talent_excel
from instructions.search_instruction import SEARCH_INSTRUCTION

root_agent = Agent(
    name="query_agent",
    model="gemini-2.5-flash",
    instruction=SEARCH_INSTRUCTION,
    tools=[search_employees, get_resume_paths, create_talent_excel]
)