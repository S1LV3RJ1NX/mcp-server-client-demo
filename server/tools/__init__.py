import importlib
import os
from typing import Any, Callable, Dict, List

from server.logger import logger

# Global registry to store all mcp tools
_mcp_tools: List[Dict[str, Any]] = []


def mcp_tool(func: Callable = None, *, name: str = None, description: str = None):
    """
    Decorator to mark a function as an MCP tool.
    Auto-registers the function for discovery by FastMCP.

    Args:
        func: The function to decorate
        name: Optional custom name for the tool (defaults to function name)
        description: Optional description (defaults to function docstring)

    Usage:
        @mcp_tool
        def my_function(x: int) -> str:
            \"\"\"Does something with x\"\"\"
            return str(x)

        @mcp_tool(name="custom_name", description="Custom description")
        def another_function(y: float) -> float:
            return y * 2
    """

    def decorator(f: Callable) -> Callable:
        # Extract function metadata
        tool_name = name or f.__name__
        tool_description = description or (f.__doc__ or "").strip()

        # Register the tool
        _mcp_tools.append(
            {
                "function": f,
                "name": tool_name,
                "description": tool_description,
                "module": f.__module__,
            }
        )

        # Return the original function unchanged
        return f

    # Handle both @mcp_tool and @mcp_tool() usage
    if func is None:
        return decorator
    else:
        return decorator(func)


def discover_tools() -> List[Dict[str, Any]]:
    """
    Auto-discover all tools with @mcp_tool decorator from the tools folder.

    Returns:
        List of tool dictionaries containing function, name, description, and module
    """
    # Clear existing tools to avoid duplicates on reimport
    global _mcp_tools
    _mcp_tools.clear()

    # Get the directory containing this __init__.py file
    tools_dir = os.path.dirname(__file__)

    # Find all Python files in the tools directory (excluding __init__.py)
    for filename in os.listdir(tools_dir):
        if filename.endswith(".py") and filename != "__init__.py":
            module_name = f"server.tools.{filename[:-3]}"

            try:
                # Import the module to trigger decorator execution
                importlib.import_module(module_name)
                logger.info(f"✓ Discovered tools from {module_name}")
            except Exception as e:
                logger.error(f"✗ Failed to import {module_name}: {e}")

    logger.info(
        f"Found {len(_mcp_tools)} total tools: {[tool['name'] for tool in _mcp_tools]}"
    )
    return _mcp_tools.copy()


def get_discovered_tools() -> List[Dict[str, Any]]:
    """
    Get the list of discovered tools without re-importing.

    Returns:
        List of tool dictionaries
    """
    return _mcp_tools.copy()
