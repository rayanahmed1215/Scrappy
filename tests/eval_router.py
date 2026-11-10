# SPDX-License-Identifier: AGPL-3.0-only
"""Measure router accuracy and speed on tests/route_cases.json.

Run from the repo root:
    python -m tests.eval_router
    python -m tests.eval_router --model BAAI/bge-small-en-v1.5 --margin 0.08
"""

import argparse
import json
import statistics
import time
from pathlib import Path

from router.embed import make_embedder
from router.router import Router, load_examples

CASES = Path(__file__).with_name("route_cases.json")


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--backend", default=None, help="embedder backend (default: SCRAPPY_EMBED_BACKEND or fastembed)")
    p.add_argument("--model", default=None, help="embedding model name for the backend")
    p.add_argument("--margin", type=float, default=0.10, help="min lead of the best route over the runner-up")
    p.add_argument("--fallback", default="talk", help="route used when the margin is too small")
    p.add_argument("--cases", default=str(CASES))
    args = p.parse_args()

    data = json.loads(Path(args.cases).read_text())
    kwargs = {"model": args.model} if args.model else {}

    t0 = time.perf_counter()
    embedder = make_embedder(args.backend, **kwargs)
    load_s = time.perf_counter() - t0

    # min_margin=-1 so decide() always returns the top route; margins are applied below
    router = Router(embedder=embedder, min_margin=-1.0, fallback=args.fallback)
    router.add_rules(load_examples())  # same seeds main.py uses

    labeled = [(q, r) for r, qs in data["cases"].items() for q in qs]
    vague = data.get("vague", [])

    router.decide("warm up")  # first call is slower; don't count it
    results, times = [], []
    for q in [q for q, _ in labeled] + vague:
        t = time.perf_counter()
        results.append(router.decide(q))
        times.append((time.perf_counter() - t) * 1000)

    def pick(res, m):
        return res["route"] if res["margin"] >= m else args.fallback

    name = getattr(embedder, "model_name", type(embedder).__name__)
    print(f"model      {name} (dim {embedder.dim}, loaded in {load_s:.1f}s)")
    print(f"speed      {statistics.mean(times):.1f} ms/query avg, "
          f"{sorted(times)[int(len(times) * 0.95) - 1]:.1f} ms p95")
    print(f"settings   margin {args.margin}, fallback '{args.fallback}'\n")

    # accuracy at the chosen margin
    lab_res = results[: len(labeled)]
    vag_res = results[len(labeled):]
    print("route      correct")
    for route in data["cases"]:
        rows = [(q, res) for (q, r), res in zip(labeled, lab_res) if r == route]
        ok = sum(pick(res, args.margin) == route for _, res in rows)
        print(f"{route:<10} {ok}/{len(rows)}")
    total_ok = sum(pick(res, args.margin) == r for (_, r), res in zip(labeled, lab_res))
    print(f"{'overall':<10} {total_ok}/{len(labeled)} ({100 * total_ok / len(labeled):.0f}%)")
    if vague:
        fb = sum(res["margin"] < args.margin for res in vag_res)
        print(f"{'vague':<10} {fb}/{len(vague)} fell back (higher is better)")

    # margin spread: misroutes and vague queries should be near ties (small margins)
    right = [res["margin"] for (_, r), res in zip(labeled, lab_res) if res["route"] == r]
    wrong = [res["margin"] for (_, r), res in zip(labeled, lab_res) if res["route"] != r]
    vs = [res["margin"] for res in vag_res]
    print("\nmargins             min / median / max")
    for label, xs in [("right top route", right), ("wrong top route", wrong), ("vague", vs)]:
        if xs:
            print(f"{label:<19} {min(xs):.2f} / {statistics.median(xs):.2f} / {max(xs):.2f}  (n={len(xs)})")

    print("\nmisroutes")
    any_miss = False
    for (q, r), res in zip(labeled, lab_res):
        got = pick(res, args.margin)
        if got != r:
            any_miss = True
            why = (f"near tie with {res['runner_up']}" if res["margin"] < args.margin
                   else f"matched '{res['match']}'")
            print(f"  want {r:<7} got {got:<7} margin {res['margin']:.2f}  {why}  <- {q}")
    if not any_miss:
        print("  none")

    # how accuracy moves with the margin cutoff, to help pick one
    print("\nmargin  accuracy  vague fell back")
    for m in [x / 50 for x in range(0, 16)]:  # 0.00 .. 0.30
        acc = sum(pick(res, m) == r for (_, r), res in zip(labeled, lab_res)) / len(labeled)
        fb = sum(res["margin"] < m for res in vag_res)
        mark = "  <- current" if abs(m - args.margin) < 1e-9 else ""
        print(f"  {m:.2f}  {100 * acc:5.1f}%   {fb}/{len(vague)}{mark}")

if __name__ == "__main__":
    main()
