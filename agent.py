"""
The FitFindr planning loop.

This is the file that makes FitFindr an agent rather than a script. It decides
which tool to run next based on what the last one returned.

If your loop calls all three tools no matter what comes back, you have a list
of function calls. A loop looks at the last result before it picks the next
step. **That branch is the graded part of this unit.**

Build and test your three tools in `tools.py` first. Then come here.

    python agent.py          runs both example paths below
"""

import re

import config
import trace
from tools import search_listings, suggest_outfit, create_fit_card
from generate import ModelUnavailable


# ── query parsing ──────────────────────────────────────────────────────────────

_SIZE_TOKENS = {"xs", "s", "m", "l", "xl", "xxl"}


def _parse_query(query: str) -> dict:
    """Pull description, size, and max_price out of a plain-language query."""
    text = query.lower()

    max_price = None
    price_match = re.search(r"under\s*\$?(\d+(?:\.\d+)?)", text)
    if price_match:
        max_price = float(price_match.group(1))

    size = None
    size_match = re.search(r"\bsize\s+([a-z0-9/]+)\b", text)
    if size_match:
        size = size_match.group(1)
    else:
        for token in re.findall(r"[a-z]+", text):
            if token in _SIZE_TOKENS:
                size = token
                break

    description = text
    if price_match:
        description = description[: price_match.start()] + description[price_match.end():]
    if size_match:
        description = description.replace(size_match.group(0), "", 1)
    description = re.sub(r"\s+", " ", description).strip(" ,.")

    return {"description": description, "size": size, "max_price": max_price}


# ── session state ─────────────────────────────────────────────────────────────

def new_session(query: str, wardrobe: dict) -> dict:
    """
    A fresh session for one user interaction.

    The session is the single source of truth for a run. Every tool result goes
    in here, and the next tool reads it back out.
    """
    return {
        "query": query,              # what the user typed
        "parsed": {},                # description / size / max_price you pulled out of it
        "search_results": [],        # everything search_listings returned
        "selected_item": None,       # the one you chose — goes into suggest_outfit
        "wardrobe": wardrobe,        # the user's wardrobe
        "outfit_suggestion": None,   # what suggest_outfit returned
        "fit_card": None,            # what create_fit_card returned
        "error": None,               # set when the run ended early
    }


# ── planning loop ─────────────────────────────────────────────────────────────

def run_agent(query: str, wardrobe: dict) -> dict:
    """
    Run the loop once and return the finished session.

    Branch rule: if search_listings returns an empty list, put a message in
    session["error"] and stop — suggest_outfit is never called. Otherwise,
    take the first result and continue through suggest_outfit and
    create_fit_card, writing every result into the session.
    """
    session = new_session(query, wardrobe)

    count = 1
    trace.check_iterations(count)

    session["parsed"] = _parse_query(query)

    results = search_listings(
        description=session["parsed"]["description"],
        size=session["parsed"]["size"],
        max_price=session["parsed"]["max_price"],
    )
    session["search_results"] = results

    if not results:
        session["error"] = (
            "No listings matched your search. Try raising your price limit, "
            "trying a different size, or using fewer specific keywords."
        )
        return session

    session["selected_item"] = results[0]

    count += 1
    trace.check_iterations(count)

    session["outfit_suggestion"] = suggest_outfit(session["selected_item"], wardrobe)

    count += 1
    trace.check_iterations(count)

    session["fit_card"] = create_fit_card(session["outfit_suggestion"], session["selected_item"])

    return session


# ── running it directly ───────────────────────────────────────────────────────

def _show(session: dict) -> None:
    if session["error"]:
        print(f"  stopped: {session['error']}")
        print(f"  fit_card is {session['fit_card']!r} — it should still be None here")
        return

    item = session["selected_item"] or {}
    print(f"  found:    {item.get('title')} — ${item.get('price')} on {item.get('platform')}")
    print(f"  outfit:   {session['outfit_suggestion']}")
    print(f"  fit card: {session['fit_card']}")


if __name__ == "__main__":
    from utils.data_loader import get_example_wardrobe

    print("=== A query the data can match ===")
    _show(run_agent(
        query="looking for a vintage graphic tee under $30",
        wardrobe=get_example_wardrobe(),
    ))

    print("\n=== A query it can't ===")
    _show(run_agent(
        query="designer ballgown size XXS under $5",
        wardrobe=get_example_wardrobe(),
    ))

    print(
        "\nThe second one should stop before the fit card. If both paths look "
        "the same,\nthe branch isn't doing anything yet."
    )