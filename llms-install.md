# AILegal MCP — install

Remote server, no local process, no API key, no account.

## Cline / Claude Desktop / Cursor / Continue

```json
{
  "mcpServers": {
    "ailegal": {
      "url": "https://ailegal.legal/api/mcp/",
      "transport": "streamable-http"
    }
  }
}
```

Equivalent endpoint: `https://ailegal.legal/api/mcp/` (POST, streamable HTTP).
Local stdio variant: run `python ailegal_server.py` from this repository (requires `pip install "mcp>=2"`).

## Tools

- `legal_breakdown(text, jurisdiction, locale)` — provisions that apply, with official-source links;
  returns an explicit refusal when the verified corpus has no norm.
- `oracle_lookup(q, jurisdiction, limit)` — which verified provisions relate to a query.
- `verify_citation(code, article, jurisdiction)` — does this citation exist in the verified corpus.

Jurisdictions: `ru`, `in`, `us`, `uk`, `ca`, `hk`. Free tier: 120 calls/hour.
Paid per-call rail for volume: `https://ailegal.legal/api/v2/x402/counsel` ($0.05 USDC on Base).

## Test

```bash
curl -s -X POST https://ailegal.legal/api/mcp/ \
  -H 'content-type: application/json' \
  -H 'accept: application/json, text/event-stream' \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-06-18","capabilities":{},"clientInfo":{"name":"probe","version":"1"}}}'
```

Legal information, not legal advice.
