# AILegal MCP server

MCP tool for agents that need an answer grounded in law, not in a model's memory.

`legal_breakdown` sends a situation to the public AILegal API and returns the provisions
that apply, each with a link to the official text. When the verified corpus has no provision
for the question, the tool returns an honest refusal (`no_norms`) instead of inventing an
article number.

Jurisdictions: Russia (`ru`), India (`in`), the US (`us`), the UK (`uk`), Canada (`ca`),
Hong Kong (`hk`). 20 India situation pages are available in Hindi in the web product.

## Install

```bash
pip install "mcp>=2"
```

## Claude Desktop / Cursor / Continue

```json
{
  "mcpServers": {
    "ailegal": {
      "command": "python",
      "args": ["/absolute/path/ailegal_server.py"]
    }
  }
}
```

## Tool

```json
{"text": "My employer has not paid my salary in India", "jurisdiction": "in", "locale": "en"}
```

Response: `{answer, norms: [{code, article, title, source_url, verified}], jurisdiction, refused, coverage}`.

## Why it refuses

A citation that does not exist is worse than no answer: the reader stops looking for the right
provision. The server is deliberately limited to the verified corpus.

## Links

- Product: https://ailegal.legal
- Example report: https://ailegal.legal/sample
- Legal information, not legal advice.
