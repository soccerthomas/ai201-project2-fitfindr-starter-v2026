"""Capstone M3: run the agent until 10 runs succeed (cache off); measure cost per run from the log."""
import json
import time
from collections import Counter

import config
config.CACHE_ENABLED = False

from agent import run_agent, LOG_PATH
from utils.data_loader import get_example_wardrobe

PRICE_IN_PER_M = 0.30    # USD per 1M input tokens, gemini-3.5-flash-lite
PRICE_OUT_PER_M = 2.50   # USD per 1M output tokens
TARGET_OK, MAX_RUNS = 10, 20

QUERIES = [
    "vintage graphic tee under $30",
    "90s track jacket in size M",
    "silk slip dress in midi length under $40",
    "platform sneakers size 8",
    "denim jacket under $50",
]

start_line = len(LOG_PATH.read_text().splitlines()) if LOG_PATH.exists() else 0
ok = runs = 0
while ok < TARGET_OK and runs < MAX_RUNS:
    q = QUERIES[runs % len(QUERIES)]
    runs += 1
    try:
        s = run_agent(q, get_example_wardrobe())
        status = "error: " + s["error"][:60] if s["error"] else "ok"
        ok += 0 if s["error"] else 1
    except Exception as exc:  # logged by run_agent as outcome=crash
        status = f"CRASH {type(exc).__name__}: {str(exc)[:70]}"
        time.sleep(5)
    print(f"run {runs:>2}: {q!r} -> {status}")

rows = [json.loads(l) for l in LOG_PATH.read_text().splitlines()[start_line:]]
good = [r for r in rows if r["outcome"] == "ok"]
print("\noutcomes:", dict(Counter(r["outcome"] for r in rows)))
n = len(good)
avg = lambda k: sum(r[k] for r in good) / n
cost = (avg("prompt_tokens") * PRICE_IN_PER_M + avg("output_tokens") * PRICE_OUT_PER_M) / 1e6
print(f"successful runs measured: {n}")
print(f"avg duration_s:    {avg('duration_s'):.2f}")
print(f"avg model_calls:   {avg('model_calls'):.2f}")
print(f"avg prompt_tokens: {avg('prompt_tokens'):.1f}")
print(f"avg output_tokens: {avg('output_tokens'):.1f}")
print(f"avg cost per run:  ${cost:.6f}")
print(f"100 runs/day:      ${cost * 100:.4f}/day, ${cost * 100 * 30:.2f}/month")
