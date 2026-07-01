import asyncio
import logging
from mcp.server import Server
from mcp.types import Tool, TextContent
from mcp.server.stdio import stdio_server

from mcp_server.tools import (
    execute_get_problem,
    execute_submit_attempt,
    execute_get_progress,
    execute_get_review_queue,
    get_problem_schema,
    submit_attempt_schema
)

# Configure logging to write to a file to prevent stdout corruption (which breaks MCP)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    filename="mcp_server.log",
    filemode="a"
)
logger = logging.getLogger(__name__)

# Initialize the MCP Server
app = Server("preppal-mcp")

@app.list_tools()
async def list_tools() -> list[Tool]:
    """Exposes available tools to the LLM client."""
    return [
        Tool(
            name="get_problem",
            description="Returns one practice problem from the PrepPal SQLite database.",
            inputSchema=get_problem_schema()
        ),
        Tool(
            name="submit_attempt",
            description="Stores a user's practice attempt for a specific problem.",
            inputSchema=submit_attempt_schema()
        ),
        Tool(
            name="get_progress",
            description="Returns the user's dashboard metrics including accuracy and weak topics.",
            inputSchema={"type": "object", "properties": {}}
        ),
        Tool(
            name="get_review_queue",
            description="Returns a list of problems that are due for spaced repetition review.",
            inputSchema={"type": "object", "properties": {}}
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Routes tool execution requests to the appropriate handler."""
    logger.info(f"Executing tool: {name} with args: {arguments}")
    
    try:
        if name == "get_problem":
            result = execute_get_problem(arguments)
        elif name == "submit_attempt":
            result = execute_submit_attempt(arguments)
        elif name == "get_progress":
            result = execute_get_progress(arguments)
        elif name == "get_review_queue":
            result = execute_get_review_queue(arguments)
        else:
            raise ValueError(f"Unknown tool: {name}")

        return [TextContent(type="text", text=result)]
        
    except Exception as e:
        logger.error(f"Tool execution failed: {e}")
        return [TextContent(type="text", text=f"Error executing tool: {e}")]

async def main():
    """Runs the MCP server over standard IO."""
    logger.info("Starting PrepPal MCP Server...")
    # Initialize the stdio transport layer
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )

if __name__ == "__main__":
    asyncio.run(main())