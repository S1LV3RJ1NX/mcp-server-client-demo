# Streaming MCP Server

This repository contains the code for setting up a demo MCP server. It contains:

- A stateless MCP server with streamable HTTP transport for scalable production deployment.
- Auto tool registry with `@mcp_tool` decorator.
- Docker file to containerize the server.
- Server can be run locally or in docker and deployed to any cloud provider.

A **stateless** Model Context Protocol (MCP) server designed for scalable async operations.

## Features

- ✅ **Stateless HTTP Transport**: Scalable across multiple workers/pods
- ⚡ **Async Operations**: Non-blocking, concurrent tool execution
- 📊 **Simple Tools**: Clean, straightforward tool implementations
- 🔄 **HTTP Streaming**: Uses streamable-http transport for web deployment

## Server Configuration

- **Transport**: `streamable-http`
- **Mode**: `stateless_http=True`
- **Async**: All tools are async
- **Port**: `8001` (default)
- **URL**: `http://localhost:8001/mcp`

## Available Tools

### Mathematical Tools

- `calculate_fibonacci(n)` - Generate fibonacci sequences
- `fibonacci_stats(max_number)` - Calculate fibonacci statistics

### Data Processing Tools

- `process_large_dataset(size, processing_delay)` - Process datasets async
- `analyze_logs(log_lines, error_rate)` - Analyze log data

### Utility Tools

- `get_current_time()` - Get current timestamp

## Available Resources

- `status://server` - Server status and configuration
- `config://streaming` - Server-specific settings

## Run the server locally

```bash
uv run -m streaming_server.main --port 8001
```

## Run the server in docker

- Build the docker image

```bash
docker build -t mcp-server -f Dockerfile.server .
```

- Run the docker container

```bash
docker run -p 8001:8001 mcp-server
```

## Run server with MCP inspector (Testing)

- Install npm and npx
- Run the server with MCP inspector in stdio mode
- Keep `LOG_LEVEL` in `.env` file as `ERROR` as MCP inspector does not support other log levels.

```bash
npx @modelcontextprotocol/inspector uv run -m streaming_server.main --port 8001 --transport stdio
```

## Key Characteristics

### Stateless Architecture

- **Horizontal Scaling**: Works with load balancers
- **Cloud Native**: Perfect for Kubernetes deployments
- **Multi-Worker**: No session dependencies between requests
- **High Availability**: Fault-tolerant distributed processing

### Simple Async Tools

- **Clean Implementation**: No complex streaming logic
- **Async Processing**: Non-blocking execution
- **Easy Development**: Simple function-based tools
- **Automatic Discovery**: Tools are automatically registered

## Tool Development

Create new tools using the `@streaming_mcp_tool` decorator:

```python
from streaming_server.tools import streaming_mcp_tool

@mcp_tool()
async def my_custom_tool(param: str) -> dict:
    # Simple async processing
    await asyncio.sleep(0.1)  # Simulate work
    return {"result": f"Processed: {param}"}
```

## Configuration

Environment variables (via `.env`):

```env
LOG_LEVEL=INFO
```

The server also has some built-in configuration that can be viewed via the `config://streaming` resource.

## Use Cases

Perfect for:

- **Web APIs**: HTTP-accessible MCP services
- **Microservices**: Stateless, scalable architecture
- **Cloud Deployment**: Container-friendly design
- **Load Balanced**: Multiple instance deployment
- **Simple Async Processing**: Basic async operations
