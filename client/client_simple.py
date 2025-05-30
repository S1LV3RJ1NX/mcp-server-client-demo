import argparse
import asyncio

from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client


async def main(args):
    """
    Main async function that demonstrates MCP client functionality.

    This function:
    1. Establishes a streamable HTTP connection to the MCP server
    2. Lists all available tools on the server
    3. Demonstrates calling a simple fibonacci tool

    Args:
        args (argparse.Namespace): Command line arguments containing:
            - server_url: URL of the MCP server (default: http://localhost:8001/mcp)
    """
    # Connect to the server using streamable HTTP protocol
    async with streamablehttp_client(args.server_url) as (read_stream, write_stream, _):
        # Create a new client session with the established streams
        async with ClientSession(read_stream, write_stream) as session:
            # Initialize the connection and establish protocol version
            await session.initialize()

            # Query the server for available tools and display them
            tools_result = await session.list_tools()
            print("Available tools:")
            for tool in tools_result.tools:
                print(f"  - {tool.name}: {tool.description}")

            # Demonstrate tool usage by calling the 'calculate_fibonacci' tool
            result = await session.call_tool("calculate_fibonacci", arguments={"n": 10})
            print(f"Fibonacci(10) = {result.content[0].text}")


if __name__ == "__main__":
    # Set up command line argument parsing
    parser = argparse.ArgumentParser(
        description="MCP Client Demo - Connects to an MCP streaming server and demonstrates tool usage"
    )
    parser.add_argument(
        "--server-url",
        type=str,
        default="http://localhost:8001/mcp",
        help="URL of the MCP server (default: http://localhost:8001/mcp)",
    )
    args = parser.parse_args()

    # Run the async main function
    asyncio.run(main(args))
