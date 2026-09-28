## What This Does

FitFindr takes a plain-language request like "vintage graphic tee under $30, size M"
and turns it into a full outfit recommendation. It searches secondhand listings for
a match, checks what it would pair with from the user's existing wardrobe, and
writes a short caption someone could actually post alongside the item. If nothing
in the listings matches, it says so instead of guessing.

## Notes — Milestone 1
Listing fields: id, title, description, category, style_tags, size, condition, price, colors, brand, platform
Wardrobe fields: id, name, category, colors, style_tags, notes

---

## Tool Inventory

### `search_listings`

- **What it does:** Searches the listings file for items matching a text description, a size, and a maximum price.
- **Inputs:** `description` (str) — free text matched against `title`, `description`, and `style_tags`; `size` (str) — exact match against the listing's `size` field; `max_price` (float) — upper price bound, inclusive.
- **Returns:** A list of listing dicts, each with the full listing fields (`id, title, description, category, style_tags, size, condition, price, colors, brand, platform`).
- **When it has nothing:** Returns an empty list (`[]`) — never `None`, never a crash.

### `suggest_outfit`

- **What it does:** Given a new item and the user's wardrobe, asks the model for outfit pairing ideas.
- **Inputs:** `new_item` (dict, a listing) — the item being considered; `wardrobe` (list of dicts) — the user's existing wardrobe items.
- **Returns:** A string containing outfit suggestion text (a few sentences on what to pair the item with).
- **When it has nothing:** If `wardrobe` is an empty list, returns general styling advice for the item instead of failing.

### `create_fit_card`

- **What it does:** Writes a short, postable caption for the new item, informed by the suggested outfit.
- **Inputs:** `outfit` (str) — the suggestion text from `suggest_outfit`; `new_item` (dict) — the listing being captioned.
- **Returns:** A string — the caption text.
- **When it has nothing:** If `outfit` is empty or missing, falls back to a generic caption built from `new_item` alone.

---

## Planning Loop

**Branch rule:** If `search_listings` returns an empty list, put a "no results" message in the session and stop — do not call `suggest_outfit`. Otherwise, take the first result from `search_listings`, store it as `session["selected_item"]`, and pass it into `suggest_outfit`.

**Where it lives:** `agent.py::run_agent`

**How the query is parsed:** *(decide once you write this — either a regex/string-splitting approach that pulls out a price ceiling like `under $30` and a size token, or asking the model to extract `description`/`size`/`max_price` as structured fields. Say which one you actually used once it's built.)*

**What moves through the session:** `session["query"]` → `session["search_results"]` → `session["selected_item"]` → `session["outfit"]` → `session["fit_card"]`, written in that order by each tool call, read back out for the next.

---

## Sample Run

*(Fill in after Milestone 4 — needs real tools.py to run against.)*

---

## How I Used AI

**Moment 1**

- *What I asked for:* A spec for `search_listings` — what "description" should match against and what the empty case should return.
- *What came back:* A suggestion to match against `title` + `description` + `style_tags` combined (not just title), and to return `[]` on no match rather than `None`, since the assignment's branch rule assumes an empty list.
- *What I changed:* [say here whether you kept this as-is or adjusted the matching fields once you saw how it performed against your data]

**Moment 2**

- *What I asked for:* Help debugging why `python test.py` kept failing on the API key check.
- *What came back:* It turned out I'd put my real key in `.env.example` instead of `.env`, and later that the placeholder text length (13 characters) confirmed the real key was never saved.
- *What I changed:* Moved the real key into `.env`, restored the placeholder in `.env.example`.