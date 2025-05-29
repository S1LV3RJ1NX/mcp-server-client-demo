import argparse
import asyncio

from mcp import ClientSession
from mcp.client.sse import sse_client


async def main(args):
    # Connect to the server using SSE
    async with sse_client(args.server_url) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            # Initialize the connection
            await session.initialize()

            # List available tools
            tools_result = await session.list_tools()
            print("Available tools:")
            for tool in tools_result.tools:
                print(f"  - {tool.name}: {tool.description}")

            # Call our add tool
            result = await session.call_tool("add", arguments={"a": 2, "b": 3})
            print(f"2 + 3 = {result.content[0].text}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--server-url", type=str, default="http://localhost:8888/sse")
    args = parser.parse_args()
    asyncio.run(main(args))
