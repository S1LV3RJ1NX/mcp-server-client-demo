# Model Context Protocol (MCP)

The Model Context Protocol (MCP) is a powerful framework that enables developers to build AI applications with large language models (LLMs) by providing a standardized way to connect models with external data sources and tools.

MCP is nothing but a protocol to connect LLMs with external data sources and tools (functions).

## MCP Client

This repository contains the code for setting up a demo MCP client. It contains:

- A simple MCP client with Server Side Events (SSE) that can be used to test the MCP protocol.
- An OpenAI client that can be used to test the MCP server showcasing simple Agentic tool calling capablities.

## Setup

- Install uv

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

- Install dependencies

```bash
uv sync
```

## ENV Variables

Make sure to set the following ENV variables in `.env` file:

- `OPENAI_API_KEY`
- `OPENAI_BASE`

## Run simple client

- The url should be the MCP server url.

```bash
uv run -m client.client_simple --server-url http://localhost:8888/sse
```

## Run the client locally

- The url should be the MCP server url.
- The model should be the OpenAI model to use.
- If using any opensrc model, make sure to set the `OPENAI_BASE` to the base url of the model.

```bash
uv run -m client.openai_client --server-url http://localhost:8888/sse --model gpt-4.1-nano
```
