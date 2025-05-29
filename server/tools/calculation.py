from server.tools import mcp_tool


@mcp_tool
async def add(a: float, b: float) -> float:
    """Add two numbers"""
    return a + b


@mcp_tool
async def subtract(a: float, b: float) -> float:
    """Subtract two numbers"""
    return a - b


@mcp_tool
async def multiply(a: float, b: float) -> float:
    """Multiply two numbers"""
    return a * b


@mcp_tool
async def divide(a: float, b: float) -> float:
    """Divide two numbers"""
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b
