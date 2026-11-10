# FitFindr

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first** — setup, every
> command, and what to do when something breaks.
>
> Once `python test.py` passes:
>
> ```bash
> python app.py listings --full -n 6      # read the data (Milestone 1)
> python app.py fields                    # what you can filter on
> python app.py ask 'vintage graphic tee under $30'
> ```
>
> All three tools are stubs, so that last command will do nothing useful yet.
> That's the starting position.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     HOW TO USE THIS FILE

     This is your submission. Fill each section in as you finish the milestone
     it belongs to — don't leave it all to the end.

     Unit 3 asks for the first five sections. Unit 4 adds the five below them.
     Leave the unit 4 sections alone until then; they're here so you know
     what's coming.

     Everything is pasted as TEXT. No screenshots, no images, no video links.
     A typed block of output gets full credit; a picture of the same output
     gets none.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 3 — THE BUILD ═══════════════════════ -->

## What This Does

<!-- Three or four sentences: what a user asks for, and what they get back. -->
## Notes — Milestone 1
Listing fields: id, title, description, category, style_tags, size, condition, price, colors, brand, platform
Wardrobe fields: id, name, category, colors, style_tags, notes


---

## Tool Inventory

<!-- Four lines per tool. This is worth 2 points and it's the single most
     common place students lose them.

     "Returns a list" earns NOTHING. The description has to say what is IN
     the list.

     The empty case isn't optional either — it's the thing your loop branches
     on, and if you don't decide it here you'll discover it as a crash in
     Milestone 5. -->

### `search_listings`

- **What it does:**
- **Inputs:** <!-- name and type each: `max_price` (float), not "a price" -->
- **Returns:**
- **When it has nothing:**

### `suggest_outfit`

- **What it does:**
- **Inputs:**
- **Returns:**
- **When it has nothing:**

### `create_fit_card`

- **What it does:**
- **Inputs:**
- **Returns:**
- **When it has nothing:**

---

## Planning Loop

<!-- Your branch rule, stated as a rule — the condition AND both paths — plus
     the file and function that holds it.

     Like this:
       "If search_listings returns an empty list, put a message in the session
        and stop. Otherwise take the first result and go to suggest_outfit."
        — agent.py::run_agent

     The grader checks your code against what you claim here, so the file and
     function have to be real. -->

**Branch rule:**

**Where it lives:** `agent.py::run_agent`

**How the query is parsed:** <!-- regex, string splitting, or asking the model — say which -->

**What moves through the session:** <!-- which fields, in what order -->

---

## Sample Run

<!-- Two things go here.

     1. One FULL query and its output, pasted as text.
     2. Your three per-tool terminal tests — the command and what it printed. -->

**One full query**

```
$ python app.py ask '...'

```

**The three tools, tested one at a time**

```
$ python -c "from tools import search_listings; print(search_listings('graphic tee', max_price=30))"

```

```
$ python -c "from tools import suggest_outfit; ..."

```

```
$ python -c "from tools import create_fit_card; ..."

```

---

## How I Used AI

<!-- Two specific moments. What you asked, what came back, what you changed.

     "I used Claude to help me code" is not enough.

     "I gave Claude my search_listings spec. It returned None on no match
     instead of an empty list, so I changed it" is the level we want. -->

**Moment 1**

- *What I asked for:*
- *What came back:*
- *What I changed:*

**Moment 2**

- *What I asked for:*
- *What came back:*
- *What I changed:*

<!-- ═══════════════════════ UNIT 4 — THE TEST ═══════════════════════

     Don't fill these in during unit 3.
     ═══════════════════════════════════════════════════════════════════ -->

---

## Run Log — Before

<!-- Five criteria, five tries each, in this exact format.

     Five, because your criteria are written out of five. Mark each try PASS
     or FAIL, count the passes, and read that count against your target — a
     row targeting 4 of 5 with three PASS cells is MISSED (3/5).

     `python run_eval.py --label before` runs everything and writes the table
     into results/. Paste it here and fill in the verdicts. -->

| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
|---|---|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |  |  |
| 2.  |  |  |  |  |  |  |  |
| 3.  |  |  |  |  |  |  |  |
| 4.  |  |  |  |  |  |  |  |
| 5.  |  |  |  |  |  |  |  |

**Real output from one try**, pasted as text, naming the file and function
that produced it:

```

```

---

## Verdicts and Diagnoses

<!-- MET or MISSED per criterion against LAST UNIT's target, plus a sentence on
     how you decided.

     Then, for every miss: which of the four places it happened — a tool, the
     loop's branch, the session, or the model's output — AND the mechanism.

     Not a diagnosis:  "The fit card was bad."
     A diagnosis:      "The fit card criterion missed on 2 of 5 items. Both had
                        an empty brand field. My prompt puts the brand in the
                        first sentence, so the card opened with a blank and read
                        like a fragment. The tool worked; the prompt assumed a
                        field that isn't always there."

     Look for a pattern. Three misses on the same tool is one problem, not
     three. -->

| # | Criterion | Target | Verdict | How I decided |
|---|---|---|---|---|
| 1 |  |  |  |  |
| 2 |  |  |  |  |
| 3 |  |  |  |  |
| 4 |  |  |  |  |
| 5 |  |  |  |  |

**Diagnoses**



---

## Loop Trace

<!-- One full run, printed step by step, with the MCP call visible in it.

     `python app.py ask '...' --trace` once you've added the trace.step()
     calls in Milestone 2.

     Worth pasting BOTH the happy path and the empty-search path. The empty
     one should be visibly shorter, because it stops. If your two traces are
     the same length, your branch isn't working — and this is the fastest way
     anyone will ever find that out. -->

**Happy path**

```

```

**Empty search**

```

```

**On the MCP move:** <!-- what changed in your code, and whether anything
behaved differently afterwards. If the rewire didn't work, say exactly where it
broke — the error text and the last thing that worked. That earns the point in
full. -->



---

## The Improvement

<!-- What you changed, why your diagnosis pointed at it, and the after-run in
     the same table format. One change, measured properly.

     `python run_eval.py --label after` -->

**What I changed:**

**Which failure it was meant to fix:**

### Run Log — After

| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
|---|---|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |  |  |
| 2.  |  |  |  |  |  |  |  |
| 3.  |  |  |  |  |  |  |  |
| 4.  |  |  |  |  |  |  |  |
| 5.  |  |  |  |  |  |  |  |

**Did it help, and how do I know:**

<!-- If it made things worse, say that. Honestly reported, that earns full
     credit and is more interesting than one that worked. -->



---

## What's Still Broken

<!-- For each criterion still missed: what you'd do, and why you stopped where
     you did. "I ran out of time" is fine if it's true. Pretending nothing is
     left is not. -->



<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 3

       [ ] criteria.md has five numbered criteria, each with a target
       [ ] Each criterion has a reason underneath it
       [ ] All five unit 3 sections above have real content
       [ ] Tool Inventory: all three tools, inputs WITH TYPES, a specific
           return value, and the empty case
       [ ] Planning Loop names the branch rule and agent.py::run_agent
       [ ] Sample Run: one full query plus the three per-tool tests, as text
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN, you submit the same one
           next unit

     SUBMISSION CHECKLIST — unit 4

       [ ] mcp_server.py exists with one tool registered
           (or a written record of exactly where the rewire broke)
       [ ] Run Log — Before, five criteria, five tries each
       [ ] Real output pasted underneath, naming file and function
       [ ] A verdict on every criterion
       [ ] A diagnosis for every miss, naming a place AND a mechanism
       [ ] Loop Trace, with the MCP call visible in it
       [ ] All three failure modes triggered and handled
       [ ] One improvement, with Run Log — After in the same format
       [ ] What's Still Broken
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository. Your commit history is what
     shows your criteria existed before your results did.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**

---

# Capstone (Unit 9)

## What This Extends

FitFindr, the three-tool thrift agent (search_listings over MCP, then
suggest_outfit, then create_fit_card). New this unit: the suggest_outfit
model call has a hard timeout and one retry, and every run writes a
structured log record to logs/runs.jsonl.

## The Shape

**B — Harden against failure.** Before this unit, a model timeout or outage
during suggest_outfit escaped run_agent as an exception: the command ended
with an error line and no result, even though search had already found an
item. Now each model request has a 20 second ceiling (FITFINDR_TIMEOUT_MS),
suggest_outfit is retried once after a failure, and if the retry also fails
the run stops cleanly with a message naming the item it found and what went
wrong. Failures can be triggered on purpose: FITFINDR_FAULT=flaky fails the
first model call of a run, FITFINDR_FAULT=down fails every one.

**Out of scope:** create_fit_card's model call is not retried (one tool call,
not two). Transient errors and permanent ones like a bad key are not told
apart, so both get the same single retry. No hosting (Path B). No changes to
search scoring or prompts.


## Running It

Path B, local with logs. The start command, environment, clean-checkout steps and
fault switches are in [RUNNING.md](RUNNING.md) under "Capstone run path".

## Instrumentation

`agent.run_agent()` appends one JSON record per run to `logs/runs.jsonl`, including
runs that error or crash (it logs in a `finally`). Fields:

| Field | Meaning |
|---|---|
| `ts` | UTC timestamp at the end of the run |
| `query` | what came in |
| `wardrobe_items` | how many wardrobe items the run had |
| `outcome` | `ok`, `no_results`, `model_error` (handled stop) or `crash` (exception escaped) |
| `selected_item`, `selected_price` | what search picked |
| `outfit_attempts` | how many tries suggest_outfit took (0 = never reached) |
| `fit_card_words` | length of the output |
| `error` | the message the user saw, or the exception text for a crash |
| `duration_s` | wall time for the whole run, including MCP startup and rate-limit waits |
| `model_calls`, `prompt_tokens`, `output_tokens` | real model calls and tokens (cache hits and simulated faults cost 0) |
| `cache_enabled`, `fault` | the conditions the run happened under |

All 15 entries recorded so far, unedited. Note the `crash` line: a real
`503 UNAVAILABLE` from the model during `create_fit_card`, the call this unit
did not harden.

{"ts": "2026-11-10T08:06:08+00:00", "query": "denim jacket under $50", "wardrobe_items": 10, "outcome": "ok", "selected_item": "Denim Jacket \u2014 Light Wash, Cropped", "selected_price": 42.0, "outfit_attempts": 1, "fit_card_words": 56, "error": null, "duration_s": 8.103, "model_calls": 2, "prompt_tokens": 439, "output_tokens": 172, "cache_enabled": false, "fault": null}
{"ts": "2026-11-10T08:06:21+00:00", "query": "denim jacket under $50", "wardrobe_items": 10, "outcome": "ok", "selected_item": "Denim Jacket \u2014 Light Wash, Cropped", "selected_price": 42.0, "outfit_attempts": 2, "fit_card_words": 51, "error": null, "duration_s": 12.467, "model_calls": 2, "prompt_tokens": 445, "output_tokens": 172, "cache_enabled": false, "fault": "flaky"}
{"ts": "2026-11-10T08:06:23+00:00", "query": "denim jacket under $50", "wardrobe_items": 10, "outcome": "model_error", "selected_item": "Denim Jacket \u2014 Light Wash, Cropped", "selected_price": 42.0, "outfit_attempts": 2, "fit_card_words": 0, "error": "Found Denim Jacket \u2014 Light Wash, Cropped ($42.0 on poshmark), but couldn't get an outfit suggestion after 2 tries. Couldn't reach the model. Check your internet connection and try again.", "duration_s": 1.696, "model_calls": 0, "prompt_tokens": 0, "output_tokens": 0, "cache_enabled": false, "fault": "down"}
{"ts": "2026-11-10T08:07:40+00:00", "query": "vintage graphic tee under $30", "wardrobe_items": 10, "outcome": "ok", "selected_item": "Y2K Baby Tee \u2014 Butterfly Print", "selected_price": 18.0, "outfit_attempts": 1, "fit_card_words": 55, "error": null, "duration_s": 9.452, "model_calls": 2, "prompt_tokens": 446, "output_tokens": 168, "cache_enabled": false, "fault": null}
{"ts": "2026-11-10T08:07:50+00:00", "query": "90s track jacket in size M", "wardrobe_items": 10, "outcome": "crash", "selected_item": null, "selected_price": null, "outfit_attempts": 0, "fit_card_words": 0, "error": "ModelUnavailable: Couldn't reach the model: 503 UNAVAILABLE. {'error': {'code': 503, 'message': 'This model is currently experiencing high demand. Spikes in demand are usually temporary. Please try again later.', 'status': 'UNAVAILABLE'}}", "duration_s": 10.002, "model_calls": 2, "prompt_tokens": 228, "output_tokens": 80, "cache_enabled": false, "fault": null}
{"ts": "2026-11-10T08:08:33+00:00", "query": "vintage graphic tee under $30", "wardrobe_items": 10, "outcome": "ok", "selected_item": "Y2K Baby Tee \u2014 Butterfly Print", "selected_price": 18.0, "outfit_attempts": 1, "fit_card_words": 47, "error": null, "duration_s": 9.181, "model_calls": 2, "prompt_tokens": 450, "output_tokens": 157, "cache_enabled": false, "fault": null}
{"ts": "2026-11-10T08:08:36+00:00", "query": "90s track jacket in size M", "wardrobe_items": 10, "outcome": "ok", "selected_item": "90s Track Jacket \u2014 Navy/White Stripe", "selected_price": 45.0, "outfit_attempts": 1, "fit_card_words": 48, "error": null, "duration_s": 3.387, "model_calls": 2, "prompt_tokens": 451, "output_tokens": 167, "cache_enabled": false, "fault": null}
{"ts": "2026-11-10T08:08:44+00:00", "query": "silk slip dress in midi length under $40", "wardrobe_items": 10, "outcome": "ok", "selected_item": "90s Silk Slip Dress \u2014 Floral, Midi Length", "selected_price": 30.0, "outfit_attempts": 1, "fit_card_words": 56, "error": null, "duration_s": 7.648, "model_calls": 2, "prompt_tokens": 444, "output_tokens": 158, "cache_enabled": false, "fault": null}
{"ts": "2026-11-10T08:08:52+00:00", "query": "platform sneakers size 8", "wardrobe_items": 10, "outcome": "ok", "selected_item": "Platform Sneakers \u2014 White Chunky Sole", "selected_price": 48.0, "outfit_attempts": 1, "fit_card_words": 39, "error": null, "duration_s": 7.871, "model_calls": 2, "prompt_tokens": 403, "output_tokens": 115, "cache_enabled": false, "fault": null}
{"ts": "2026-11-10T08:08:54+00:00", "query": "denim jacket under $50", "wardrobe_items": 10, "outcome": "ok", "selected_item": "Denim Jacket \u2014 Light Wash, Cropped", "selected_price": 42.0, "outfit_attempts": 1, "fit_card_words": 42, "error": null, "duration_s": 2.263, "model_calls": 2, "prompt_tokens": 419, "output_tokens": 134, "cache_enabled": false, "fault": null}
{"ts": "2026-11-10T08:09:05+00:00", "query": "vintage graphic tee under $30", "wardrobe_items": 10, "outcome": "ok", "selected_item": "Y2K Baby Tee \u2014 Butterfly Print", "selected_price": 18.0, "outfit_attempts": 1, "fit_card_words": 54, "error": null, "duration_s": 10.834, "model_calls": 2, "prompt_tokens": 425, "output_tokens": 148, "cache_enabled": false, "fault": null}
{"ts": "2026-11-10T08:09:08+00:00", "query": "90s track jacket in size M", "wardrobe_items": 10, "outcome": "ok", "selected_item": "90s Track Jacket \u2014 Navy/White Stripe", "selected_price": 45.0, "outfit_attempts": 1, "fit_card_words": 51, "error": null, "duration_s": 3.687, "model_calls": 2, "prompt_tokens": 429, "output_tokens": 149, "cache_enabled": false, "fault": null}
{"ts": "2026-11-10T08:09:26+00:00", "query": "silk slip dress in midi length under $40", "wardrobe_items": 10, "outcome": "ok", "selected_item": "90s Silk Slip Dress \u2014 Floral, Midi Length", "selected_price": 30.0, "outfit_attempts": 1, "fit_card_words": 47, "error": null, "duration_s": 17.994, "model_calls": 2, "prompt_tokens": 430, "output_tokens": 139, "cache_enabled": false, "fault": null}
{"ts": "2026-11-10T08:09:38+00:00", "query": "platform sneakers size 8", "wardrobe_items": 10, "outcome": "ok", "selected_item": "Platform Sneakers \u2014 White Chunky Sole", "selected_price": 48.0, "outfit_attempts": 1, "fit_card_words": 38, "error": null, "duration_s": 11.462, "model_calls": 2, "prompt_tokens": 427, "output_tokens": 133, "cache_enabled": false, "fault": null}
{"ts": "2026-11-10T08:09:47+00:00", "query": "denim jacket under $50", "wardrobe_items": 10, "outcome": "ok", "selected_item": "Denim Jacket \u2014 Light Wash, Cropped", "selected_price": 42.0, "outfit_attempts": 1, "fit_card_words": 54, "error": null, "duration_s": 8.988, "model_calls": 2, "prompt_tokens": 453, "output_tokens": 185, "cache_enabled": false, "fault": null}


## What It Costs

Measured with `python measure_cost.py`: cache off, the agent run until 10 runs
succeeded (10 of 10 did), then token counts averaged from those 10 log records.
Token counts come from the service's own `usage_metadata`, not estimates.

| Measure | Average per run |
|---|---|
| model calls | 2.00 |
| prompt tokens | 433.1 |
| output tokens | 148.5 |
| wall time | 8.33 s (includes two rate-limit pauses) |

Price used: gemini-3.5-flash-lite at $0.30 per 1M input tokens and $2.50 per 1M
output tokens.

Cost per run = 433.1 × $0.30/1M + 148.5 × $2.50/1M = $0.000130 + $0.000371 = **$0.000501**

100 people a day, one run each: 100 × $0.000501 = **$0.050 per day**, about $1.50 per month.
At that volume the real limit is not money but the per-minute rate limit: 2 calls per
run against 15 requests per minute means about 7 runs per minute before people queue.


## Run Log and Verdicts

Three trials, each one full run of `python capstone_trials.py --label before`, cache off.
Raw output: `results/capstone_before.txt` and `results/capstone_before.json`.

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| C1. Flaky model call is recovered | 5 of 5 | 4/5 | 5/5 | 5/5 | MISSED |
| C2. Model down: clean stop, names item and price, under 5 s | 5 of 5 | 5/5 | 5/5 | 5/5 | MET |
| C3. One truthful log line per run | 7 of 7 | 7/7 | 7/7 | 7/7 | MET |
| C4. Normal runs finish ok in under 10 s | at least 4 of 5 | 3/5 | 3/5 | 4/5 | MISSED |
| C5. Original happy path still ends ok | 5 of 5 | 5/5 | 5/5 | 5/5 | MET |

Real output, one log line per criterion. Each record is written by `agent.py::_log_run`
and scored by `capstone_trials.py::main`:

C1 (FAILED, trial 1, 'platform sneakers size 8', fault=flaky):
{"ts": "2026-11-10T08:16:55+00:00", "query": "platform sneakers size 8", "wardrobe_items": 10, "outcome": "crash", "selected_item": null, "selected_price": null, "outfit_attempts": 0, "fit_card_words": 0, "error": "ModelUnavailable: Couldn't reach the model: 503 UNAVAILABLE. {'error': {'code': 503, 'message': 'This model is currently experiencing high demand. Spikes in demand are usually temporary. Please try again later.', 'status': 'UNAVAILABLE'}}", "duration_s": 6.372, "model_calls": 2, "prompt_tokens": 226, "output_tokens": 77, "cache_enabled": false, "fault": "flaky"}

C2 (passed, trial 1, 'vintage graphic tee under $30', fault=down):
{"ts": "2026-11-10T08:17:11+00:00", "query": "vintage graphic tee under $30", "wardrobe_items": 10, "outcome": "model_error", "selected_item": "Y2K Baby Tee \u2014 Butterfly Print", "selected_price": 18.0, "outfit_attempts": 2, "fit_card_words": 0, "error": "Found Y2K Baby Tee \u2014 Butterfly Print ($18.0 on depop), but couldn't get an outfit suggestion after 2 tries. Couldn't reach the model. Check your internet connection and try again.", "duration_s": 1.793, "model_calls": 0, "prompt_tokens": 0, "output_tokens": 0, "cache_enabled": false, "fault": "down"}

C3 (passed, trial 1, 'vintage graphic tee under $30', fault=None):
{"ts": "2026-11-10T08:17:33+00:00", "query": "vintage graphic tee under $30", "wardrobe_items": 10, "outcome": "ok", "selected_item": "Y2K Baby Tee \u2014 Butterfly Print", "selected_price": 18.0, "outfit_attempts": 2, "fit_card_words": 48, "error": null, "duration_s": 15.757, "model_calls": 3, "prompt_tokens": 423, "output_tokens": 144, "cache_enabled": false, "fault": null}

C4 (FAILED, trial 1, 'vintage graphic tee under $30', fault=None):
{"ts": "2026-11-10T08:15:31+00:00", "query": "vintage graphic tee under $30", "wardrobe_items": 10, "outcome": "ok", "selected_item": "Y2K Baby Tee \u2014 Butterfly Print", "selected_price": 18.0, "outfit_attempts": 1, "fit_card_words": 48, "error": null, "duration_s": 11.953, "model_calls": 2, "prompt_tokens": 405, "output_tokens": 125, "cache_enabled": false, "fault": null}

C5 (passed, trial 1, 'vintage graphic tee under $30', fault=None):
{"ts": "2026-11-10T08:15:31+00:00", "query": "vintage graphic tee under $30", "wardrobe_items": 10, "outcome": "ok", "selected_item": "Y2K Baby Tee \u2014 Butterfly Print", "selected_price": 18.0, "outfit_attempts": 1, "fit_card_words": 48, "error": null, "duration_s": 11.953, "model_calls": 2, "prompt_tokens": 405, "output_tokens": 125, "cache_enabled": false, "fault": null}


**C1: MISSED (4/5, 5/5, 5/5).** Stage: `create_fit_card`. In trial 1 the flaky
"platform sneakers" run recovered the simulated fault in `suggest_outfit` as designed.
The next model call, `create_fit_card`, then got a real `503 UNAVAILABLE` ("model is
currently experiencing high demand"). That call had no retry, because it was out of scope,
so `ModelUnavailable` escaped `run_agent` and the run crashed. The log recorded it as
`outcome: crash`. The retry worked; the miss came from the unhardened call after it.

**C2: MET (5/5 ×3).** Every down-mode run stopped with the item's title and price in
the message, `outfit_attempts: 2`, in 1.4 to 2.2 s.

**C3: MET (7/7 ×3).** Every run left exactly one log line and every `outcome` matched
what the caller got, including `no_results` and `model_error`.

**C4: MISSED (3/5, 3/5, 4/5).** Stage: the two model calls, not search or MCP. Down-mode
runs skip the model and take about 1.5 s, so search plus MCP startup is about 1.5 s and
everything above that is model time. Most slow runs (11 to 15 s) had no printed
rate-limit wait. The 503 traceback shows the google-genai SDK retrying internally
(`tenacity`), so when the service is under load the SDK waits silently inside one call.
One slow run (29.8 s, "90s track jacket", trial 1) had `outfit_attempts: 2` with no
fault switch set: a real failure that the 20 s timeout cut off and the retry recovered.
My criterion assumed slowness would come from my own printed rate limiter. It mostly
came from the service.

**C5: MET (5/5 ×3).** The happy path still ends `ok`.

**Pattern:** both misses trace to one stage, the model service under load. When it
errors, an unhardened call crashes the run (C1). When it's slow, runs cross 10 s (C4).
Before the fix, 3 normal run(s) with no fault switch set needed the
`suggest_outfit` retry; after, 0. The extension caught real failures,
not only simulated ones.

## The Improvement

**What I changed:** gave `create_fit_card` the same treatment as `suggest_outfit`. It
gets one retry, and if both attempts fail the agent builds a plain fit card from data it
already has (title, price, platform and the outfit text) instead of crashing. Two new log
fields record it: `fit_card_attempts` and `fit_card_fallback`.

**Why this one:** the C1 diagnosis named the exact mechanism, an unretried model call
after the retried one, and this closes it. It does not target C4.

Run Log, after (`python capstone_trials.py --label after`):

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| C1. Flaky model call is recovered | 5 of 5 | 5/5 | 5/5 | 5/5 | MET |
| C2. Model down: clean stop, names item and price, under 5 s | 5 of 5 | 5/5 | 5/5 | 5/5 | MET |
| C3. One truthful log line per run | 7 of 7 | 7/7 | 7/7 | 7/7 | MET |
| C4. Normal runs finish ok in under 10 s | at least 4 of 5 | 4/5 | 4/5 | 3/5 | MISSED |
| C5. Original happy path still ends ok | 5 of 5 | 5/5 | 5/5 | 5/5 | MET |

C1 (passed, trial 1, 'vintage graphic tee under $30', fault=flaky):
{"ts": "2026-11-10T19:58:24+00:00", "query": "vintage graphic tee under $30", "wardrobe_items": 10, "outcome": "ok", "selected_item": "Y2K Baby Tee \u2014 Butterfly Print", "selected_price": 18.0, "outfit_attempts": 2, "fit_card_words": 56, "fit_card_attempts": 1, "fit_card_fallback": false, "error": null, "duration_s": 15.767, "model_calls": 2, "prompt_tokens": 444, "output_tokens": 173, "cache_enabled": false, "fault": "flaky"}

C4 (FAILED, trial 1, 'vintage graphic tee under $30', fault=None):
{"ts": "2026-11-10T19:57:56+00:00", "query": "vintage graphic tee under $30", "wardrobe_items": 10, "outcome": "ok", "selected_item": "Y2K Baby Tee \u2014 Butterfly Print", "selected_price": 18.0, "outfit_attempts": 1, "fit_card_words": 51, "fit_card_attempts": 1, "fit_card_fallback": false, "error": null, "duration_s": 10.033, "model_calls": 2, "prompt_tokens": 428, "output_tokens": 154, "cache_enabled": false, "fault": null}


**Did it help?** For C1, yes: it went from 4/5, 5/5, 5/5 to 5/5 ×3. In the after set, 1 logged run(s) needed a second `create_fit_card` attempt and 0 used the fallback card; all of them still ended `ok`. The forced-failure test (create_fit_card replaced with one that always raises) also returned a fallback card instead of a crash.

C2, C3 and C5 held. C4 is still MISSED (4/5, 4/5, 3/5), and the slow runs moved
mechanism. Three of the four after-set misses (10.2 to 12.6 s) ran straight after a
printed rate-limit wait of 6 to 7 s. The trial runner issues about 26 real calls in
roughly 2 minutes against a 15 requests/minute cap, so the test's own load pushes
limiter waits into the runs it measures. The fix didn't cause that, but it didn't help
it either.

## What's Still Broken

**C4 is still missed.** What I'd do: log time per stage (each model call, and seconds
spent waiting on the rate limiter) so one run splits into "my pacing" and "Google's
latency". Then I'd know whether to space test runs to a real user's rate or to cut
calls per run. Why I stopped: the unit allows one measured improvement. C4 needs a
measurement before a fix, and guessing at it would be the "four changes you can't tell
apart" the brief warns against. I am not changing the 10 s target. The runs came out
slower, which is a result, not a broken criterion.

**Also not handled (out of scope, still true):** transient and permanent errors get the
same retry, so a bad API key wastes one retry and about 1 s before failing.

**The one thing I'd do first with another unit:** per-stage timing in the log, because
every remaining miss is a latency question I can't answer from total `duration_s` alone.

## How I Used AI

1. **Finding the gap.** I had Claude read `generate.py` and `agent.py`. It pointed out
   that `ModelUnavailable` is raised immediately for anything that isn't a rate limit,
   and that `run_agent` never catches it, so one bad response ends the whole run. That
   became the extension. I kept the scope to one tool call, not all of `generate.py`.
2. **Reading the 503.** Claude noticed `tenacity` in the 503 traceback, which means the
   SDK retries internally. That changed my C4 diagnosis from "my rate limiter is slow"
   to "service latency is hidden inside single calls". The first cost script it wrote
   crashed on that same 503. I had it rewritten to keep going and to measure only
   successful runs, and the crash became evidence in the log instead of lost data.

Staff note: this capstone was built as TF prep, and its criteria were drafted with
Claude. In a student submission the criteria would have to be the student's own, per
the brief.
