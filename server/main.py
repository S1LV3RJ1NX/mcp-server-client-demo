import argparse

from mcp.server.fastmcp import FastMCP

from server.logger import logger
from server.tools import discover_tools


def run_server(args):
    # Auto-discover tools from the tools folder
    logger.info("🔍 Discovering MCP tools...")
    discovered_tools = discover_tools()

    mcp = FastMCP(
        name="mcp-server",
        version="0.1.0",
        description="A demo MCP server for weather information",
        host=args.host,
        port=args.port,
        tools=[],
    )

    # Register all discovered tools
    logger.info("📝 Registering tools with FastMCP...")
    for tool_info in discovered_tools:
        mcp.add_tool(
            fn=tool_info["function"],
            name=tool_info["name"],
            description=tool_info["description"],
        )
        logger.info(f"✓ Registered tool: {tool_info['name']}")

    logger.info(f"🚀 Starting server with {len(discovered_tools)} tools")
    mcp.run(transport=args.transport)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--transport", type=str, default="sse")
    parser.add_argument("--host", type=str, default="0.0.0.0")
    parser.add_argument("--port", type=int, default=8888)
    args = parser.parse_args()
    run_server(args)
