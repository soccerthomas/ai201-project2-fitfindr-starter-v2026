# Acceptance criteria — FitFindr

Five criteria that say what "working" means for this agent, written before
any results existed.

## 1. A matching query completes all three tools

Given a query that matches at least one listing, the agent completes all three
tool calls and returns a fit card — in at least 4 of 5 tries.

**Why this target:** I chose 4 of 5 instead of 5 of 5 because `search_listings`
uses keyword matching, so some valid ways of wording a query may not match the
available listing data.

## 2. An impossible query stops before the second tool

Given a query that matches no listings, the agent stops before calling
`suggest_outfit` and returns a message naming what to change — 5 of 5 tries.

**Why this target:** I chose 5 of 5 because once `search_listings` returns no
results, the agent can directly check that result and stop. This path does
not depend on model-generated output.

## 3. The selected item stays the same between tools

For 5 matching queries, the item stored in `session["selected_item"]` must
exactly match the item passed into `suggest_outfit` in 5 of 5 runs.

**Why this target:** I chose 5 of 5 because the selected item should be stored
in session state and passed directly to the next tool. There is no randomness
that should cause the item to change.

## 4. The fit card contains the important listing information

Across 5 matching runs, the fit card must mention the selected item's name
and price and stay under 100 words in at least 4 of 5 runs.

**Why this target:** I chose 4 of 5 because `suggest_outfit` uses a model, so
the wording can change between runs. The important part is that the main
listing information is still included and the card stays short enough to be
useful.

## 5. The search respects the user's price limit

For 5 queries that include a maximum price, the selected item must be at or
below the requested price limit in 5 of 5 runs.

**Why this target:** I chose 5 of 5 because price is structured listing data,
so the agent can directly compare it with the user's maximum price. This
should not depend on model wording.