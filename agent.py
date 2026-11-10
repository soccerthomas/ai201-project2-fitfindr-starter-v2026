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
from mcp_client import call_tool
from tools import suggest_outfit, create_fit_card
from generate import ModelUnavailable

import datetime
import json
import os
import time
from pathlib import Path

import generate as _gen

# Capstone (unit 9): retry the suggest_outfit model call once, then stop cleanly.
OUTFIT_MAX_ATTEMPTS = 2
OUTFIT_RETRY_WAIT_S = 1.0
# Capstone M6 improvement: same treatment for create_fit_card.
FIT_CARD_MAX_ATTEMPTS = 2
LOG_PATH = Path(__file__).parent / "logs" / "runs.jsonl"


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

def _run_agent_core(query: str, wardrobe: dict) -> dict:
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

    results = call_tool("search_listings", {
        "description": session["parsed"]["description"],
        "size": session["parsed"]["size"],
        "max_price": session["parsed"]["max_price"],
    })
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

    outfit, last_error = None, None
    for attempt in range(1, OUTFIT_MAX_ATTEMPTS + 1):
        session["outfit_attempts"] = attempt
        try:
            outfit = suggest_outfit(session["selected_item"], wardrobe)
            break
        except ModelUnavailable as exc:
            last_error = exc
            if attempt < OUTFIT_MAX_ATTEMPTS:
                time.sleep(OUTFIT_RETRY_WAIT_S)

    if outfit is None:
        item = session["selected_item"]
        session["error"] = (
            f"Found {item['title']} (${item['price']} on {item['platform']}), "
            f"but couldn't get an outfit suggestion after {OUTFIT_MAX_ATTEMPTS} tries. "
            f"{last_error}"
        )
        return session

    session["outfit_suggestion"] = outfit

    count += 1
    trace.check_iterations(count)

    card = None
    for attempt in range(1, FIT_CARD_MAX_ATTEMPTS + 1):
        session["fit_card_attempts"] = attempt
        try:
            card = create_fit_card(session["outfit_suggestion"], session["selected_item"])
            break
        except ModelUnavailable:
            if attempt < FIT_CARD_MAX_ATTEMPTS:
                time.sleep(OUTFIT_RETRY_WAIT_S)

    if card is None:
        # Model failed twice: build a plain card from data we already have, rather than crash.
        item = session["selected_item"]
        session["fit_card_fallback"] = True
        card = (
            f"{item['title']} — ${item['price']:.0f} on {item['platform']}. "
            f"{session['outfit_suggestion']}"
        )

    session["fit_card"] = card

    return session


# ── running it directly ───────────────────────────────────────────────────────

def run_agent(query: str, wardrobe: dict) -> dict:
    """Run the loop once, and append one structured record to logs/runs.jsonl."""
    start = time.perf_counter()
    calls_before = _gen.call_count()
    tokens_before = _gen.token_counts()
    session, crash = None, None
    try:
        session = _run_agent_core(query, wardrobe)
        return session
    except Exception as exc:
        crash = f"{type(exc).__name__}: {exc}"
        raise
    finally:
        _log_run(query, wardrobe, session, crash, start, calls_before, tokens_before)


def _log_run(query, wardrobe, session, crash, start, calls_before, tokens_before):
    tokens_after = _gen.token_counts()
    s = session or {}
    item = s.get("selected_item") or {}
    fit_card = s.get("fit_card") or ""
    error = crash or s.get("error")
    if crash:
        outcome = "crash"
    elif error and not item:
        outcome = "no_results"
    elif error:
        outcome = "model_error"
    else:
        outcome = "ok"
    record = {
        "ts": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
        "query": query,
        "wardrobe_items": len((wardrobe or {}).get("items", [])),
        "outcome": outcome,
        "selected_item": item.get("title"),
        "selected_price": item.get("price"),
        "outfit_attempts": s.get("outfit_attempts", 0),
        "fit_card_words": len(fit_card.split()),
        "fit_card_attempts": s.get("fit_card_attempts", 0),
        "fit_card_fallback": bool(s.get("fit_card_fallback")),
        "error": error,
        "duration_s": round(time.perf_counter() - start, 3),
        "model_calls": _gen.call_count() - calls_before,
        "prompt_tokens": tokens_after["prompt"] - tokens_before["prompt"],
        "output_tokens": tokens_after["output"] - tokens_before["output"],
        "cache_enabled": bool(config.CACHE_ENABLED),
        "fault": os.getenv("FITFINDR_FAULT") or None,
    }
    try:
        LOG_PATH.parent.mkdir(exist_ok=True)
        with LOG_PATH.open("a", encoding="utf-8") as f:
            f.write(json.dumps(record) + "\n")
    except OSError:
        pass  # logging must never break a run


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