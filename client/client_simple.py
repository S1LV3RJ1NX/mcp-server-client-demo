import argparse
import asyncio

from mcp import ClientSession
from mcp.client.sse import sse_client


async def main(args):
    """
    Main async function that demonstrates MCP client functionality.

    This function:
    1. Establishes an SSE connection to the MCP server
    2. Lists all available tools on the server
    3. Demonstrates calling a simple addition tool

    Args:
        args (argparse.Namespace): Command line arguments containing:
            - server_url: URL of the MCP server (default: http://localhost:8888/sse)
    """
    # Connect to the server using Server-Sent Events (SSE) protocol
    async with sse_client(args.server_url) as (read_stream, write_stream):
        # Create a new client session with the established streams
        async with ClientSession(read_stream, write_stream) as session:
            # Initialize the connection and establish protocol version
            await session.initialize()

            # Query the server for available tools and display them
            tools_result = await session.list_tools()
            print("Available tools:")
            for tool in tools_result.tools:
                print(f"  - {tool.name}: {tool.description}")

            # Demonstrate tool usage by calling the 'add' tool with arguments
            result = await session.call_tool("add", arguments={"a": 2, "b": 3})
            print(f"2 + 3 = {result.content[0].text}")


if __name__ == "__main__":
    # Set up command line argument parsing
    parser = argparse.ArgumentParser(
        description="MCP Client Demo - Connects to an MCP server and demonstrates tool usage"
    )
    parser.add_argument(
        "--server-url",
        type=str,
        default="http://localhost:8888/sse",
        help="URL of the MCP server (default: http://localhost:8888/sse)",
    )
    args = parser.parse_args()

    # Run the async main function
    asyncio.run(main(args))
