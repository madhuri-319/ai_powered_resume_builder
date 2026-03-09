import asyncio
import os
import sys
import json
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# --- CONFIGURATION & PATHS ---

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

# Path to MCP Server
SERVER_PATH = os.path.abspath(os.path.join(CURRENT_DIR, "..", "server.py"))

# Add project root for imports if needed
ROOT_DIR = os.path.abspath(os.path.join(CURRENT_DIR, "..", ".."))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)


# --- MCP BRIDGE TOOLS ---

async def search_employees(skills: list[str], min_experience: int) -> dict:
    """
    Calls the MCP server to search employees based on skills and experience.
    Returns employee_ids.
    """
    server_params = StdioServerParameters(command="python", args=[SERVER_PATH])

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            response = await session.call_tool(
                "search_employees",
                {"skills": skills, "min_experience": min_experience}
            )

            return json.loads(response.content[0].text)


async def get_resume_paths(employee_ids: list[str]) -> list:
    """
    Calls MCP server to fetch resume paths for employee IDs.
    """
    server_params = StdioServerParameters(command="python", args=[SERVER_PATH])

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            response = await session.call_tool(
                "get_resume_paths",
                {"employee_ids": employee_ids}
            )

            return json.loads(response.content[0].text)