import argparse
import asyncio
import json
from contextlib import AsyncExitStack
from typing import Any, Dict, List, Optional

from mcp import ClientSession
from mcp.client.sse import sse_client
from openai import AsyncOpenAI

from client.config import settings
from client.logger import logger


class MCPClient:
    """Client for interacting with OpenAI models using MCP tools."""

    def __init__(self, server_url: str, model: str = "gpt-4.1-nano"):
        """Initialize the OpenAI MCP client.

        Args:
            model: The OpenAI model to use.
        """
        # Initialize session and client objects
        self.session: Optional[ClientSession] = None
        self.exit_stack = AsyncExitStack()
        self.openai_client = AsyncOpenAI(
            base_url=settings.OPENAI_BASE,
            api_key=settings.OPENAI_API_KEY,
        )
        self.model = model
        self.server_url = server_url
        self.stdio: Optional[Any] = None
        self.write: Optional[Any] = None

    async def connect_to_server(self):
        """Connect to an MCP server using SSE transport."""
        # Connect to the server using SSE
        sse_transport = await self.exit_stack.enter_async_context(
            sse_client(self.server_url)
        )
        read_stream, write_stream = sse_transport

        # Create session with SSE transport
        self.session = await self.exit_stack.enter_async_context(
            ClientSession(read_stream, write_stream)
        )

        # Initialize the connection
        await self.session.initialize()

        # List available tools
        tools_result = await self.session.list_tools()
        logger.info("\nConnected to server with tools:")
        for tool in tools_result.tools:
            logger.info(f"  - {tool.name}: {tool.description}")

    async def get_mcp_tools(self) -> List[Dict[str, Any]]:
        """Get available tools from the MCP server in OpenAI format.

        Returns:
            A list of tools in OpenAI format.
        """
        tools_result = await self.session.list_tools()
        return [
            {
                "type": "function",
                "function": {
                    "name": tool.name,
                    "description": tool.description,
                    "parameters": tool.inputSchema,
                },
            }
            for tool in tools_result.tools
        ]

    async def process_query(self, query: str) -> str:
        """Process a query using OpenAI and available MCP tools.
        This can be later switch with a workflow engine like Langgraph.

        Args:
            query: The user query.

        Returns:
            The response from OpenAI.
        """
        # Get available tools
        tools = await self.get_mcp_tools()

        # Initial OpenAI API call
        response = await self.openai_client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": query}],
            tools=tools,
            tool_choice="auto",
        )

        # Get assistant's response
        assistant_message = response.choices[0].message

        # Initialize conversation with user query and assistant response
        messages = [
            {"role": "user", "content": query},
            assistant_message,
        ]

        # Handle tool calls if present
        if assistant_message.tool_calls:
            # Process each tool call
            for tool_call in assistant_message.tool_calls:
                # Execute tool call
                result = await self.session.call_tool(
                    tool_call.function.name,
                    arguments=json.loads(tool_call.function.arguments),
                )

                # Add tool response to conversation
                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": result.content[0].text,
                    }
                )

            # Get final response from OpenAI with tool results
            final_response = await self.openai_client.chat.completions.create(
                model=self.model,
                messages=messages,
                tools=tools,
                tool_choice="none",  # Don't allow more tool calls
            )

            return final_response.choices[0].message.content

        # No tool calls, just return the direct response
        return assistant_message.content

    async def cleanup(self):
        """Clean up resources."""
        await self.exit_stack.aclose()


async def main(args):
    """Main entry point for the client."""
    client = MCPClient(args.server_url, args.model)
    await client.connect_to_server()

    try:
        while True:
            print("--------------------------------\n")
            query = input("Enter a query: ")
            response = await client.process_query(query)
            print(f"Response: {response}")
            print("--------------------------------\n")
    except KeyboardInterrupt:
        logger.info("Keyboard interrupt detected, exiting...")
    finally:
        await client.cleanup()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--server-url", type=str, default="http://localhost:8888/sse")
    parser.add_argument("--model", type=str, default="gpt-4.1-nano")
    args = parser.parse_args()
    asyncio.run(main(args))
