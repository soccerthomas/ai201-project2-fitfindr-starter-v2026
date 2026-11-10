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
---

## Capstone criteria (Unit 9)

All five are scored over 3 trials. A trial is one run of `python capstone_trials.py`
with the cache off. A criterion is MET only if its target holds in all 3 trials.
C1–C3 are about this unit's extension; C2 is the bad path.

### C1. A single model failure is recovered, not shown to the user

With `FITFINDR_FAULT=flaky` (the first model call of the run fails), each of 5 runs
on matching queries ends with a fit card, no error, and `outfit_attempts` = 2.
**Target: 5 of 5 per trial.**

**Why:** the simulated fault fails exactly once and the retry is plain code, so one
miss means the retry path is broken or something after it fails. Anything under
5/5 lets a user see an error the extension exists to absorb.

### C2. A model outage ends the run cleanly, fast, and names what was found

With `FITFINDR_FAULT=down`, each of 5 runs on matching queries returns without an
exception escaping `run_agent`, with an error message containing the found item's
title and price, `outfit_attempts` = 2, in under 5 seconds wall time.
**Target: 5 of 5 per trial.**

**Why:** when the model is down the user should still learn what search found and
that the problem is the model, not their query. Under 5 s because no real model
call happens. The only costs are MCP startup (about 1.5 s in M2) and one 1 s retry
wait, so anything slower means the run is waiting on something it shouldn't.

### C3. Every run leaves exactly one log line, and it tells the truth

For a batch of 7 runs (3 normal, 2 impossible queries, 2 with `FITFINDR_FAULT=down`),
`logs/runs.jsonl` gains exactly one line per run, and each line's `outcome` matches
what the caller actually got (fit card = `ok`, empty search = `no_results`, handled
stop = `model_error`, exception = `crash`). **Target: 7 of 7 per trial.**

**Why:** the log is the only way to diagnose a run afterwards. One missing or
mislabeled line means a failure can disappear, which defeats the instrumentation.

### C4. Normal runs stay fast enough to use

Of 5 normal runs (no fault), at least 4 finish with a fit card in under 10 seconds,
by the logged `duration_s`. **Target: at least 4 of 5 per trial.**

**Why:** the measured average in M3 was 8.33 s including two rate-limit pauses, so
10 s leaves a little room. 4 of 5 lets one run land on a rate-limit pause (15
requests/minute, 2 per run) without calling it a miss. Two slow runs means waiting
has become the normal experience.

### C5. The original happy path still works

Of 5 normal runs (no fault, five different matching queries), all 5 end with
`outcome` = `ok` and a non-empty fit card. **Target: 5 of 5 per trial.**

**Why:** this is the system as it worked before the extension, and the extension
must not break it. It is not a free pass. A real `503 UNAVAILABLE` already crashed
one run in M3, and the `create_fit_card` call is not retried, so this can fail on
a bad day. C4 and C5 are scored on the same 5 normal runs.
