import hashlib
from fastmcp import FastMCP
from fastmcp.server.dependencies import get_http_headers

EMAIL = "23f3002008@ds.study.iitm.ac.in"

mcp = FastMCP(name="Exam MCP Server")


@mcp.tool
def solve_challenge() -> str:
    """Return the first 16 hex characters of SHA-256(challenge:email)."""
    headers = get_http_headers()

    challenge = headers.get("x-exam-challenge", "")

    if not challenge:
        raise ValueError("Missing X-Exam-Challenge header")

    digest = hashlib.sha256(
        f"{challenge}:{EMAIL}".encode("utf-8")
    ).hexdigest()

    return digest[:16]


# Expose the ASGI application for Vercel.
app = mcp.http_app(path="/mcp")


if __name__ == "__main__":
    mcp.run(
        transport="http",
        host="0.0.0.0",
        port=8000,
        path="/mcp",
    )
