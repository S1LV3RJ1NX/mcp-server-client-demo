import argparse

from mcp.server.fastmcp import FastMCP

from server.logger import logger
from server.tools import discover_tools


def run_server(args):
    """
    Initialize and run the MCP server with discovered tools.

    Args:
        args (argparse.Namespace): Command line arguments containing:
            - transport: Transport protocol to use (default: 'sse')
            - host: Server host address (default: '0.0.0.0')
            - port: Server port number (default: 8888)
    """
    # Auto-discover tools from the tools folder
    logger.info("🔍 Discovering MCP tools...")
    discovered_tools = discover_tools()

    # Initialize FastMCP server with basic configuration
    mcp = FastMCP(
        name="mcp-server",
        version="0.1.0",
        description="A demo MCP server for weather information",
        host=args.host,
        port=args.port,
        tools=[],  # Tools will be added dynamically
    )

    # Register all discovered tools with the server
    logger.info("📝 Registering tools with FastMCP...")
    for tool_info in discovered_tools:
        mcp.add_tool(
            fn=tool_info["function"],  # The actual tool function
            name=tool_info["name"],  # Tool identifier
            description=tool_info["description"],  # Tool documentation
        )
        logger.info(f"✓ Registered tool: {tool_info['name']}")

    # Start the server with the specified transport protocol
    logger.info(f"🚀 Starting server with {len(discovered_tools)} tools")
    mcp.run(transport=args.transport)


if __name__ == "__main__":
    # Configure command line argument parser
    parser = argparse.ArgumentParser(
        description="Run the MCP server with configurable options"
    )
    parser.add_argument(
        "--transport",
        type=str,
        default="sse",
        help="Transport protocol to use (default: sse)",
    )
    parser.add_argument(
        "--host",
        type=str,
        default="0.0.0.0",
        help="Server host address (default: 0.0.0.0)",
    )
    parser.add_argument(
        "--port", type=int, default=8888, help="Server port number (default: 8888)"
    )
    args = parser.parse_args()
    run_server(args)
