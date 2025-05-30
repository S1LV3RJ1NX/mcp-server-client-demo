import importlib
import os
from typing import Any, Callable, Dict, List

from streaming_server.logger import logger

# Global registry to store all streaming mcp tools
_streaming_mcp_tools: List[Dict[str, Any]] = []


def mcp_tool(
    func: Callable = None,
    *,
    name: str = None,
    description: str = None,
    stream_enabled: bool = True,
):
    """
    Decorator to mark a function as a streaming MCP tool.
    Auto-registers the function for discovery by FastMCP.

    Args:
        func: The function to decorate
        name: Optional custom name for the tool (defaults to function name)
        description: Optional description (defaults to function docstring)
        stream_enabled: Whether this tool supports streaming responses

    Usage:
        @streaming_mcp_tool
        def my_function(x: int) -> str:
            \"\"\"Does something with x\"\"\"
            return str(x)

        @streaming_mcp_tool(name="custom_name", description="Custom description", stream_enabled=True)
        async def another_function(y: float) -> float:
            return y * 2
    """

    def decorator(f: Callable) -> Callable:
        # Extract function metadata
        tool_name = name or f.__name__
        tool_description = description or (f.__doc__ or "").strip()

        # Register the tool
        _streaming_mcp_tools.append(
            {
                "function": f,
                "name": tool_name,
                "description": tool_description,
                "module": f.__module__,
                "stream_enabled": stream_enabled,
                "is_async": True,  # Streaming tools should be async
            }
        )

        # Return the original function unchanged
        return f

    # Handle both @streaming_mcp_tool and @streaming_mcp_tool() usage
    if func is None:
        return decorator
    else:
        return decorator(func)


def discover_tools() -> List[Dict[str, Any]]:
    """
    Auto-discover all tools with @streaming_mcp_tool decorator from the tools folder.

    Returns:
        List of tool dictionaries containing function, name, description, module, and streaming info
    """
    # Clear existing tools to avoid duplicates on reimport
    global _streaming_mcp_tools
    _streaming_mcp_tools.clear()

    # Get the directory containing this __init__.py file
    tools_dir = os.path.dirname(__file__)

    # Find all Python files in the tools directory (excluding __init__.py)
    for filename in os.listdir(tools_dir):
        if filename.endswith(".py") and filename != "__init__.py":
            module_name = f"streaming_server.tools.{filename[:-3]}"

            try:
                # Import the module to trigger decorator execution
                importlib.import_module(module_name)
                logger.info(f"✓ Discovered streaming tools from {module_name}")
            except Exception as e:
                logger.error(f"✗ Failed to import {module_name}: {e}")

    streaming_tools = [
        tool["name"]
        for tool in _streaming_mcp_tools
        if tool.get("stream_enabled", False)
    ]
    logger.info(
        f"Found {len(_streaming_mcp_tools)} total tools: {[tool['name'] for tool in _streaming_mcp_tools]}"
    )
    logger.info(f"Streaming-enabled tools: {streaming_tools}")
    return _streaming_mcp_tools.copy()


def get_discovered_tools() -> List[Dict[str, Any]]:
    """
    Get the list of discovered streaming tools without re-importing.

    Returns:
        List of tool dictionaries
    """
    return _streaming_mcp_tools.copy()
