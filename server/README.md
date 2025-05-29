# Model Context Protocol (MCP)

The Model Context Protocol (MCP) is a powerful framework that enables developers to build AI applications with large language models (LLMs) by providing a standardized way to connect models with external data sources and tools.

MCP is nothing but a protocol to connect LLMs with external data sources and tools (functions).

## MCP Server

This repository contains the code for setting up a demo MCP server. It contains:

- A simple MCP server with Server Side Events (SSE) that can be used to test the MCP protocol.
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

## Run the server locally

```bash
uv run -m server.main --port 8888
```

## Run server with MCP inspector (Testing)

- Install npm and npx
- Run the server with MCP inspector in stdio mode
- Keep `LOG_LEVEL` in `.env` file as `ERROR` as MCP inspector does not support other log levels.

```bash
npx @modelcontextprotocol/inspector uv run -m server.main --port 8888 --transport stdio
```

## Run the server in docker

- Build the docker image

```bash
docker build -t mcp-server -f Dockerfile.server .
```

- Run the docker container

```bash
docker run -p 8888:8888 mcp-server
```
