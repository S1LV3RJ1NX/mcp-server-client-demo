import argparse
import json
from datetime import datetime

from mcp.server.fastmcp import FastMCP

from streaming_server.logger import logger
from streaming_server.tools import discover_tools


def run_streaming_server(args):
    """
    Initialize and run the streaming MCP server with discovered tools.

    Args:
        args (argparse.Namespace): Command line arguments containing:
            - transport: Transport protocol to use (default: 'streamable-http')
            - host: Server host address (default: '0.0.0.0')
            - port: Server port number (default: 8001)
    """
    # Auto-discover streaming tools from the tools folder
    logger.info("🔍 Discovering streaming MCP tools...")
    discovered_tools = discover_tools()

    # Initialize FastMCP server with streaming configuration
    mcp = FastMCP(
        name="streaming-mcp-server",
        version="1.0.0",
        description="A stateless streaming MCP server for real-time data processing",
        host=args.host,
        port=args.port,
        stateless_http=True,  # Enable stateless mode
        # json_response=False   # Default: enables streaming
    )

    # Add server status resource
    @mcp.resource("status://server")
    def get_server_status() -> str:
        """Get streaming server status information"""
        return json.dumps(
            {
                "server_type": "stateless_streaming",
                "server_name": "streaming-mcp-server",
                "status": "healthy",
                "timestamp": datetime.now().isoformat(),
                "features": ["streaming", "stateless", "async_processing", "real_time"],
                "transport": args.transport,
                "host": args.host,
                "port": args.port,
                "tools_count": len(discovered_tools),
            }
        )

    @mcp.resource("config://streaming")
    def get_streaming_config() -> str:
        """Get streaming server configuration"""
        return json.dumps(
            {
                "max_concurrent_streams": 100,
                "stream_timeout": 300,
                "chunk_size": 1024,
                "compression_enabled": True,
                "async_processing": True,
                "stateless_mode": True,
            }
        )

    # Register all discovered tools with the server
    logger.info("📝 Registering streaming tools with FastMCP...")
    for tool_info in discovered_tools:
        mcp.add_tool(
            fn=tool_info["function"],  # The actual tool function
            name=tool_info["name"],  # Tool identifier
            description=tool_info["description"],  # Tool documentation
        )

        stream_status = (
            "✓ STREAMING" if tool_info.get("stream_enabled", False) else "• STANDARD"
        )
        logger.info(f"{stream_status} Registered tool: {tool_info['name']}")

    # Start the server with the specified transport protocol
    logger.info(f"🚀 Starting streaming server with {len(discovered_tools)} tools")
    logger.info(f"📡 Transport: {args.transport}")
    logger.info(f"🔄 Mode: stateless streaming")
    logger.info(f"🌐 URL: http://{args.host}:{args.port}/mcp")

    mcp.run(transport=args.transport)


if __name__ == "__main__":
    # Configure command line argument parser
    parser = argparse.ArgumentParser(
        description="Run the streaming MCP server with configurable options"
    )
    parser.add_argument(
        "--transport",
        type=str,
        default="streamable-http",
        help="Transport protocol to use (default: streamable-http)",
    )
    parser.add_argument(
        "--host",
        type=str,
        default="127.0.0.1",
        help="Server host address (default: 127.0.0.1)",
    )
    parser.add_argument(
        "--port", type=int, default=8001, help="Server port number (default: 8001)"
    )
    args = parser.parse_args()
    run_streaming_server(args)
