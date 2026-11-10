"""Capstone M5: score the five capstone criteria over 3 trials.

    python capstone_trials.py --label before
    python capstone_trials.py --label after
"""
import argparse
import json
import os
import time
from pathlib import Path

import config
config.CACHE_ENABLED = False

import generate
from agent import run_agent, LOG_PATH
from utils.data_loader import get_example_wardrobe

MATCHING = [
    "vintage graphic tee under $30",
    "90s track jacket in size M",
    "silk slip dress in midi length under $40",
    "platform sneakers size 8",
    "denim jacket under $50",
]
IMPOSSIBLE = "designer ballgown size XXS under $5"
TRIALS = 3
CRITERIA = [
    ("C1", "Flaky model call is recovered (attempts=2, fit card)", 5, 5),
    ("C2", "Model down: clean stop, names item+price, <5s", 5, 5),
    ("C3", "One truthful log line per run", 7, 7),
    ("C4", "Normal runs finish OK in <10s", 4, 5),
    ("C5", "Original happy path still ends ok", 5, 5),
]

details = []


def log_lines():
    return LOG_PATH.read_text(encoding="utf-8").splitlines() if LOG_PATH.exists() else []


def one(query, fault=None):
    if fault:
        os.environ["FITFINDR_FAULT"] = fault
    else:
        os.environ.pop("FITFINDR_FAULT", None)
    generate.reset_fault()
    before = len(log_lines())
    t0 = time.perf_counter()
    session, exc = None, None
    try:
        session = run_agent(query, get_example_wardrobe())
    except Exception as e:  # noqa: BLE001 — a crash is a result, not a reason to stop
        exc = e
    wall = time.perf_counter() - t0
    os.environ.pop("FITFINDR_FAULT", None)
    new = log_lines()[before:]
    if exc:
        actual = "crash"
    elif session["error"] and not session["selected_item"]:
        actual = "no_results"
    elif session["error"]:
        actual = "model_error"
    else:
        actual = "ok"
    tag = f"[{fault}]" if fault else ""
    print(f"  {tag:<8} {query[:40]:<40} -> {actual} ({wall:.1f}s)", flush=True)
    return {"query": query, "fault": fault, "session": session, "exc": exc,
            "wall": wall, "new_lines": new, "actual": actual}


def logged(r, key, default=None):
    if len(r["new_lines"]) != 1:
        return default
    return json.loads(r["new_lines"][0]).get(key, default)


def score(crit, trial, r, ok):
    s = r["session"] or {}
    details.append({
        "criterion": crit, "trial": trial, "query": r["query"], "fault": r["fault"],
        "actual": r["actual"], "outfit_attempts": s.get("outfit_attempts", 0),
        "wall_s": round(r["wall"], 3),
        "error": f"{type(r['exc']).__name__}: {r['exc']}" if r["exc"] else s.get("error"),
        "fit_card": s.get("fit_card"),
        "log": [json.loads(l) for l in r["new_lines"]],
        "pass": bool(ok),
    })
    return bool(ok)


def c2_ok(r):
    s = r["session"]
    if r["exc"] or not s or not s["error"] or not s["selected_item"]:
        return False
    item = s["selected_item"]
    return (item["title"] in s["error"] and str(item["price"]) in s["error"]
            and s.get("outfit_attempts") == 2 and r["wall"] < 5)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--label", required=True)
    label = ap.parse_args().label

    scores = {c[0]: [] for c in CRITERIA}
    for trial in range(1, TRIALS + 1):
        print(f"\n=== trial {trial} of {TRIALS} ===")

        normal = [one(q) for q in MATCHING]
        scores["C5"].append(sum(score("C5", trial, r,
            r["actual"] == "ok" and (r["session"] or {}).get("fit_card")) for r in normal))
        scores["C4"].append(sum(score("C4", trial, r,
            r["actual"] == "ok" and logged(r, "duration_s", r["wall"]) < 10) for r in normal))

        flaky = [one(q, "flaky") for q in MATCHING]
        scores["C1"].append(sum(score("C1", trial, r,
            r["actual"] == "ok" and (r["session"] or {}).get("outfit_attempts") == 2) for r in flaky))

        down = [one(q, "down") for q in MATCHING]
        scores["C2"].append(sum(score("C2", trial, r, c2_ok(r)) for r in down))

        batch = [one(MATCHING[0]), one(MATCHING[1]), one(MATCHING[2]),
                 one(IMPOSSIBLE), one(IMPOSSIBLE),
                 one(MATCHING[3], "down"), one(MATCHING[4], "down")]
        scores["C3"].append(sum(score("C3", trial, r,
            len(r["new_lines"]) == 1 and logged(r, "outcome") == r["actual"]) for r in batch))

        print("  scores:", {k: v[-1] for k, v in scores.items()})

    out = Path("results") / f"capstone_{label}.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps({"label": label, "scores": scores, "runs": details},
                              indent=2, default=str), encoding="utf-8")

    print(f"\n## Run Log — {label}\n")
    print("| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |")
    print("|---|---|---|---|---|---|")
    for cid, name, need, of in CRITERIA:
        runs = scores[cid]
        verdict = "MET" if all(k >= need for k in runs) else "MISSED"
        cells = " | ".join(f"{k}/{of}" for k in runs)
        target = f"{need} of {of}" if need == of else f">= {need} of {of}"
        print(f"| {cid}. {name} | {target} | {cells} | {verdict} |")

    print("\nFailing runs:")
    fails = [d for d in details if not d["pass"]]
    for d in fails:
        print(f"  {d['criterion']} t{d['trial']} [{d['fault'] or '-'}] {d['query']}: "
              f"actual={d['actual']} attempts={d['outfit_attempts']} wall={d['wall_s']}s "
              f"err={str(d['error'])[:110]}")
    if not fails:
        print("  none")
    print(f"\nsaved {out}")


if __name__ == "__main__":
    main()
