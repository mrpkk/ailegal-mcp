#!/usr/bin/env python3
"""AILegal MCP server — verified legal breakdowns for agents (28.10.2026).

Tool `legal_breakdown` calls the public AILegal API and returns the answer with
the provisions it relies on. The server itself stores nothing: no account, no
key, no history.

Run (stdio):
    python ailegal_server.py
Config for Claude Desktop / Cursor / Continue:
    {"mcpServers": {"ailegal": {"command": "python", "args": ["/path/ailegal_server.py"]}}}
"""
from __future__ import annotations

import json
import urllib.error
import urllib.request

from mcp.server.mcpserver import MCPServer

API = "https://ailegal.legal/api/v2/ask"
TIMEOUT = 60

mcp = MCPServer(
    name="ailegal",
    instructions=(
        "Verified legal breakdowns for Russia, India, the US, the UK, Canada and Hong Kong. "
        "Answers are assembled from provisions read in official sources; when the corpus has "
        "no provision, the tool returns no_norms instead of inventing a citation."
    ),
)


def _ask(text: str, jurisdiction: str, locale: str) -> dict:
    body = json.dumps({"text": text, "jurisdiction": jurisdiction, "locale": locale}).encode()
    req = urllib.request.Request(
        API, data=body, headers={"content-type": "application/json", "User-Agent": "ailegal-mcp/1.0"}
    )
    with urllib.request.urlopen(req, timeout=TIMEOUT) as res:
        data = json.loads(res.read())
    result = data.get("result") or {}
    norms = [
        {
            "code": n.get("code"),
            "article": n.get("article"),
            "title": n.get("title") or n.get("summary_en") or "",
            "source_url": n.get("source_url"),
            "verified": bool(n.get("verified")),
        }
        for n in (result.get("norms") or [])
    ]
    return {
        "answer": result.get("answer") or data.get("partial_text") or "",
        "norms": norms,
        "jurisdiction": data.get("jurisdiction"),
        "refused": bool(data.get("refuse")),
        "coverage": data.get("coverage"),
        "note": "Legal information, not legal advice. Verify the current wording in the official source.",
    }


@mcp.tool(
    name="legal_breakdown",
    description=(
        "Describe a legal situation and get the provisions that apply, with official-source links. "
        "jurisdiction: ru | in | us | uk | ca | hk. Returns an honest no_norms refusal when the "
        "verified corpus has no provision for the question."
    ),
)
async def legal_breakdown(text: str, jurisdiction: str = "ru", locale: str = "en") -> str:
    try:
        return json.dumps(_ask(text, jurisdiction, locale), ensure_ascii=False)
    except urllib.error.HTTPError as exc:
        return json.dumps({"error": {"code": "HTTP_%s" % exc.code,
                                     "message": "AILegal API rejected the request",
                                     "retryable": exc.code >= 500}}, ensure_ascii=False)
    except Exception as exc:  # noqa: BLE001 — агент должен получить причину, а не пустоту
        return json.dumps({"error": {"code": "UNAVAILABLE", "message": str(exc)[:200],
                                     "retryable": True}}, ensure_ascii=False)


if __name__ == "__main__":
    mcp.run()
