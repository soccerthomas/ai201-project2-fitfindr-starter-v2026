"""
The three FitFindr tools.

Each one is a standalone function you can call and test on its own, before any
of them are wired into the loop. Build and test them one at a time — three
untested tools joined by a loop is one problem that looks like six, because you
can't tell which layer is lying to you.

    search_listings(description, size, max_price)  → list[dict]
    suggest_outfit(new_item, wardrobe)             → str
    create_fit_card(outfit, new_item)              → str

All three are stubs right now. They run and they do nothing — that's the
starting position and it's deliberate.

⚠️ Before you write any of them, fill in the **Tool Inventory** section of your
README (Milestone 2). Four lines per tool: what it does, each input with its
type, exactly what it returns, and what it returns when it has nothing to give.
That last line is what your loop branches on. "Returns a list" earns nothing —
the description has to say what is *in* the list.
"""

import re

import config  # noqa: F401 — you'll use this in search_listings
from generate import generate
from utils.data_loader import load_listings


def _tokenize(text: str) -> set[str]:
    """Lowercase and split into word/number tokens, so 'S/M' -> {'s', 'm'}."""
    return set(re.findall(r"[a-z0-9]+", text.lower()))


# ── Tool 1: search_listings ───────────────────────────────────────────────────

def search_listings(
    description: str,
    size: str | None = None,
    max_price: float | None = None,
) -> list[dict]:
    """
    Search the listings data for items matching a description, and optionally a
    size and a price ceiling.

    This is the tool that doesn't call the model, which makes it the easiest one
    to test and the one to move onto MCP in unit 4.

    Args:
        description: keywords describing what the user wants
                     (e.g. "vintage graphic tee").
        size:        a size string to filter by, or None to skip size filtering.
                     Match case-insensitively — "M" should match "S/M".
        max_price:   maximum price, inclusive, or None to skip price filtering.

    Returns:
        A list of matching listing dicts, best match first.
        Returns an empty list when nothing matches — an empty list, not None,
        and not an exception. Your loop branches on this.

    Each listing dict has these fields:
        id, title, description, category, style_tags (list), size,
        condition, price (float), colors (list), brand (str or None), platform

    Test it from a terminal before you move on:
        python -c "from tools import search_listings; print(search_listings('graphic tee', max_price=30))"
    """
    listings = load_listings()
    query_words = _tokenize(description)

    scored = []
    for listing in listings:
        if max_price is not None and listing["price"] > max_price:
            continue

        if size is not None:
            size_tokens = _tokenize(listing["size"])
            if size.strip().lower() not in size_tokens:
                continue

        searchable = " ".join([
            listing["title"],
            listing["description"],
            " ".join(listing["style_tags"]),
        ])
        listing_words = _tokenize(searchable)

        score = len(query_words & listing_words)
        if score == 0:
            continue

        scored.append((score, listing))

    scored.sort(key=lambda pair: pair[0], reverse=True)
    return [listing for _score, listing in scored[: config.SEARCH_RESULT_LIMIT]]


# ── Tool 2: suggest_outfit ────────────────────────────────────────────────────

def suggest_outfit(new_item: dict, wardrobe: dict) -> str:
    items = wardrobe.get("items", [])

    item_description = (
        f"{new_item['title']} ({new_item['category']}, "
        f"{', '.join(new_item['colors'])}, size {new_item['size']}, "
        f"style: {', '.join(new_item['style_tags'])})"
    )

    if not items:
        prompt = (
            f"Someone is considering buying this secondhand item:\n"
            f"{item_description}\n\n"
            f"They don't have any wardrobe items on file yet. Suggest general "
            f"styling ideas for this item — what kinds of pieces would pair "
            f"well with it, in terms of color, fit, and vibe."
        )
    else:
        wardrobe_lines = "\n".join(
            f"- {i['name']} ({i['category']}, {', '.join(i['colors'])})"
            for i in items
        )
        prompt = (
            f"Someone is considering buying this secondhand item:\n"
            f"{item_description}\n\n"
            f"Here is their current wardrobe:\n{wardrobe_lines}\n\n"
            f"Suggest one or two specific outfits that combine the new item "
            f"with pieces they already own. Name the wardrobe pieces directly."
        )

    system = (
        "You are a thrifting and styling assistant. Give concrete, concise "
        "outfit suggestions in a friendly tone. Keep it to a few sentences."
    )

    return generate(prompt, system=system)


# ── Tool 3: create_fit_card ───────────────────────────────────────────────────

def create_fit_card(outfit: str, new_item: dict) -> str:
    if not outfit or not outfit.strip():
        return (
            f"{new_item['title']} — ${new_item['price']:.0f} on "
            f"{new_item['platform']}. No outfit suggestion available yet."
        )

    prompt = (
        f"Write a short caption (2-4 sentences) someone would actually post "
        f"when reselling or sharing this thrifted find:\n\n"
        f"Item: {new_item['title']}\n"
        f"Price: ${new_item['price']:.0f}\n"
        f"Platform: {new_item['platform']}\n"
        f"Condition: {new_item['condition']}\n\n"
        f"Outfit idea to reference: {outfit}\n\n"
        f"Mention the item, its price, and its platform once each. Write it "
        f"like a real social post, not a product listing — specific about "
        f"the vibe, not generic."
    )

    system = (
        "You write short, casual social captions for secondhand fashion "
        "finds. Sound like a real person posting, not an ad."
    )

    return generate(prompt, system=system)