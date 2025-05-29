from server.tools import mcp_tool


@mcp_tool(name="get_weather", description="Get the weather for a given city")
def get_weather(city: str) -> str:
    """Get the weather for a given city"""
    return f"The weather in {city} is sunny"


def not_to_be_discovered():
    """This function is not to be discovered"""
    return "This function is not to be discovered"
