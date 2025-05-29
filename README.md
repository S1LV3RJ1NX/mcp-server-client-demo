# Model Context Protocol (MCP)

This repository contains the code for setting up a demo MCP server and using it via python backend and OpenAI SDK.

## Setup

- Install uv

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

- Install dependencies

```bash
uv sync
```

## Run the server

```bash
uv run -m server.main --port 8888
```
