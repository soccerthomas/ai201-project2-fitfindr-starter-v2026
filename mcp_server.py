"""
Your MCP server. ← UNIT 4, MILESTONE 1

search_listings is registered below and exposed over MCP.

    python mcp_server.py        starts the server (it will just sit there — that's right)
    python mcp_client.py        asks the server what it offers
"""

from mcp.server.fastmcp import FastMCP

from tools import search_listings as _search_listings_impl

# log_level="WARNING" keeps the server from printing an INFO line for every
# request. Without it your terminal fills with "Processing request of type
# CallToolRequest" and the output you actually care about scrolls away.
mcp = FastMCP("fitfindr", log_level="WARNING")


@mcp.tool()
def search_listings(
    description: str,
    size: str | None = None,
    max_price: float | None = None,
) -> list[dict]:
    """
    Search secondhand clothing listings for items matching free-text keywords,
    optionally narrowed by size and a maximum price in whole dollars.

    description is required keywords (e.g. "vintage graphic tee"); size and
    max_price are optional filters -- omit either to search without it, and
    size is matched case-insensitively against each listing's size field.
    Returns a list of matching listing dicts, best match first, each with
    id, title, description, category, style_tags, size, condition, price,
    colors, brand, and platform. Returns an empty list, never an error and
    never null, when nothing matches.
    """
    return _search_listings_impl(description, size, max_price)


if __name__ == "__main__":
    mcp.run()
