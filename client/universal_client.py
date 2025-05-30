import argparse
import asyncio
import json
from typing import Any, Dict

from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client


class UniversalMCPClient:
    """
    Simple universal MCP client for connecting to MCP servers
    """

    def __init__(self, server_url: str):
        self.server_url = server_url
        self.session = None
        self.client_context = None

    async def connect(self):
        """Establish connection to MCP server"""
        print(f"🔗 Connecting to: {self.server_url}")

        try:
            # Create and enter the streamable HTTP client context
            self.client_context = streamablehttp_client(self.server_url)
            read_stream, write_stream, _ = await self.client_context.__aenter__()

            # Create and enter the client session context
            self.session = ClientSession(read_stream, write_stream)
            await self.session.__aenter__()

            # Initialize the connection
            await self.session.initialize()
            print("✅ Connected successfully!")

        except Exception as e:
            print(f"❌ Connection failed: {e}")
            await self._cleanup()
            raise

    async def disconnect(self):
        """Close connection to MCP server"""
        await self._cleanup()
        print("🔌 Disconnected")

    async def _cleanup(self):
        """Clean up connections properly"""
        try:
            if self.session:
                await self.session.__aexit__(None, None, None)
                self.session = None
        except Exception as e:
            print(f"Warning: Error closing session: {e}")

        try:
            if self.client_context:
                await self.client_context.__aexit__(None, None, None)
                self.client_context = None
        except Exception as e:
            print(f"Warning: Error closing client: {e}")

    async def list_tools(self):
        """List available tools"""
        if not self.session:
            raise RuntimeError("Not connected to server")

        try:
            tools_result = await self.session.list_tools()
            tools = [(tool.name, tool.description) for tool in tools_result.tools]

            print(f"\n🛠️  Available Tools ({len(tools)}):")
            for name, desc in tools:
                print(f"  • {name}: {desc}")

            return tools
        except Exception as e:
            print(f"❌ Error listing tools: {e}")
            return []

    async def list_resources(self):
        """List available resources"""
        if not self.session:
            raise RuntimeError("Not connected to server")

        try:
            resources_result = await self.session.list_resources()
            resources = [
                (res.uri, res.description) for res in resources_result.resources
            ]

            print(f"\n📦 Available Resources ({len(resources)}):")
            for uri, desc in resources:
                print(f"  • {uri}: {desc}")

            return resources
        except Exception as e:
            print(f"❌ Error listing resources: {e}")
            return []

    async def call_tool(
        self, tool_name: str, arguments: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """Call a tool on the server"""
        if not self.session:
            raise RuntimeError("Not connected to server")

        arguments = arguments or {}
        print(f"\n🔧 Calling: {tool_name}")
        if arguments:
            print(f"📝 Args: {arguments}")

        try:
            result = await self.session.call_tool(tool_name, arguments)

            if result.content and len(result.content) > 0:
                content = result.content[0]
                if hasattr(content, "text"):
                    try:
                        parsed_result = json.loads(content.text)
                        print(f"✅ Result: {json.dumps(parsed_result, indent=2)}")
                        return parsed_result
                    except json.JSONDecodeError:
                        print(f"✅ Result: {content.text}")
                        return {"result": content.text}
                else:
                    print(f"✅ Result: {content}")
                    return {"result": str(content)}
            else:
                print("✅ Tool executed successfully")
                return {"status": "success"}

        except Exception as e:
            print(f"❌ Error: {e}")
            return {"error": str(e)}

    async def read_resource(self, resource_uri: str) -> str:
        """Read a resource from the server"""
        if not self.session:
            raise RuntimeError("Not connected to server")

        print(f"\n📖 Reading: {resource_uri}")

        try:
            result = await self.session.read_resource(resource_uri)

            # Handle the response format properly
            if hasattr(result, "contents") and result.contents:
                content = result.contents[0]
                if hasattr(content, "text"):
                    content_text = content.text
                    mime_type = getattr(content, "mimeType", "text/plain")
                elif hasattr(content, "blob"):
                    content_text = content.blob
                    mime_type = getattr(content, "mimeType", "application/octet-stream")
                else:
                    content_text = str(content)
                    mime_type = "text/plain"
            else:
                content_text = str(result)
                mime_type = "text/plain"

            print(f"✅ Content ({mime_type}):")

            try:
                parsed = json.loads(content_text)
                print(json.dumps(parsed, indent=2))
            except json.JSONDecodeError:
                print(content_text)

            return content_text

        except Exception as e:
            print(f"❌ Error: {e}")
            return ""


async def main():
    parser = argparse.ArgumentParser(description="Universal MCP Client")
    parser.add_argument("url", help="MCP server URL (e.g., http://localhost:8001/mcp)")
    parser.add_argument("--tool", help="Tool name to call")
    parser.add_argument("--args", help="Tool arguments as JSON string")
    parser.add_argument("--resource", help="Resource URI to read")
    parser.add_argument(
        "--list-tools", action="store_true", help="List available tools"
    )
    parser.add_argument(
        "--list-resources", action="store_true", help="List available resources"
    )

    args = parser.parse_args()

    client = UniversalMCPClient(args.url)

    try:
        await client.connect()

        if args.list_tools:
            await client.list_tools()

        elif args.list_resources:
            await client.list_resources()

        elif args.tool:
            tool_args = {}
            if args.args:
                try:
                    tool_args = json.loads(args.args)
                except json.JSONDecodeError:
                    print("❌ Invalid JSON in --args")
                    return
            await client.call_tool(args.tool, tool_args)

        elif args.resource:
            await client.read_resource(args.resource)

        else:
            # Show quick usage
            print("\n💡 Quick usage examples:")
            print("  • --list-tools                    : List all available tools")
            print("  • --list-resources                : List all available resources")
            print("  • --tool calculate_fibonacci --args '{\"n\": 10}'")
            print("  • --resource status://server")

    except KeyboardInterrupt:
        print("\n👋 Interrupted")
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        await client.disconnect()


if __name__ == "__main__":
    asyncio.run(main())
