# Model Context Protocol (MCP)

The Model Context Protocol (MCP) is a powerful framework that enables developers to build AI applications with large language models (LLMs) by providing a standardized way to connect models with external data sources and tools.

MCP is nothing but a protocol to connect LLMs with external data sources and tools (functions).

## MCP Server

This repository contains the code for setting up a demo MCP server. It contains:

- A stateless MCP server with streamable HTTP transport for scalable production deployment.
- Auto tool registry with `@mcp_tool` decorator.
- Docker file to containerize the server.
- Server can be run locally or in docker and deployed to any cloud provider.

## Setup

- Install uv

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

- Install dependencies

```bash
uv sync
```

## MCP Client

This repository contains the code for setting up a demo MCP client with OpenAI SDK. Refer to the [client](client/README.md) for more details.

> Note: For ease of understanding, both server and client are in the same repository, you can easily keep them in separate repositories / projects.
