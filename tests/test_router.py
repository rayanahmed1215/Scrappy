# SPDX-License-Identifier: AGPL-3.0-only
"""Unit tests for the router. A fake embedder keeps them offline and fast.

Run from the repo root:  python -m pytest
The real-model accuracy check is skipped unless SCRAPPY_SLOW=1.
"""

import inspect
import json
import os
from pathlib import Path

import numpy as np
import pytest

from models.local import HANDLERS, run_refine
from router.embed import make_embedder, normalize
from router.router import EXAMPLES, Router, load_examples

CASES = Path(__file__).with_name("route_cases.json")


class FakeEmbedder:
    """Looks each text up in a fixed table of vectors, so scores are known in advance."""

    def __init__(self, table: dict[str, list[float]]):
        self.table = table
        self.dim = len(next(iter(table.values())))

    def embed_batch(self, texts):
        return normalize([self.table[t] for t in texts])

    def embed(self, text):
        return self.embed_batch([text])[0]


# 3 axes: code, talk, refine. Seeds sit on an axis; queries sit between them.
TABLE = {
    "seed code": [1, 0, 0],
    "seed talk": [0, 1, 0],
    "seed refine": [0, 0, 1],
    "clearly code": [0.9, 0.1, 0],         # far ahead of talk
    "near tie": [0.5, 0.48, 0],            # code barely ahead of talk
    "clearly refine": [0, 0.2, 0.9],
}


def make_router(**kwargs):
    r = Router(embedder=FakeEmbedder(TABLE), **kwargs)
    r.add_rules([("seed code", "code"), ("seed talk", "talk"), ("seed refine", "refine")])
    return r


# --- decisions ---------------------------------------------------------------

def test_clear_winner_takes_its_route():
    d = make_router().decide("clearly code")
    assert d["route"] == "code"
    assert d["runner_up"] == "talk"
    assert d["margin"] >= make_router().min_margin
    assert d["match"] == "seed code"


def test_near_tie_falls_back_with_reason():
    d = make_router().decide("near tie")
    assert d["route"] == "talk"
    assert d["margin"] < make_router().min_margin
    assert "near tie" in d["reason"]


def test_default_fallback_is_local_talk_never_remote():
    r = make_router()
    assert r.fallback == "talk"
    assert r.decide("near tie")["route"] != "remote"


def test_custom_margin_and_fallback():
    # with no margin required, the near tie is decided by the top route
    assert make_router(min_margin=0.0).route("near tie") == "code"
    assert make_router(fallback="refine").route("near tie") == "refine"


def test_margin_is_top_minus_runner_up():
    d = make_router().decide("clearly refine")
    q = normalize(TABLE["clearly refine"])[0]
    assert d["route"] == "refine"
    assert d["margin"] == pytest.approx(q[2] - q[1])


def test_no_examples_falls_back():
    r = Router(embedder=FakeEmbedder(TABLE))
    d = r.decide("clearly code")
    assert d["route"] == "talk"
    assert d["reason"] == "no examples"


def test_single_route_uses_score_as_margin():
    r = Router(embedder=FakeEmbedder(TABLE))
    r.add_rule("seed code", "code")
    d = r.decide("clearly code")
    assert d["runner_up"] is None
    assert d["margin"] == pytest.approx(d["score"])


def test_best_example_per_route_counts():
    # a second, worse code example must not lower code's score
    r = make_router()
    r.add_rule("seed talk", "code")
    assert r.decide("clearly code")["match"] == "seed code"


def test_decide_returns_every_field():
    d = make_router().decide("clearly code")
    assert set(d) == {"route", "score", "margin", "match", "runner_up", "reason"}


def test_add_rule_matches_add_rules():
    a, b = Router(embedder=FakeEmbedder(TABLE)), Router(embedder=FakeEmbedder(TABLE))
    a.add_rules([("seed code", "code"), ("seed talk", "talk")])
    b.add_rule("seed code", "code")
    b.add_rule("seed talk", "talk")
    assert np.allclose(a.vectors, b.vectors)
    assert a.examples == b.examples


# --- embeddings --------------------------------------------------------------

def test_normalize_gives_unit_length_and_handles_zero():
    v = normalize([[3, 4], [0, 0]])
    assert np.allclose(v[0], [0.6, 0.8])
    assert np.allclose(v[1], [0, 0])  # no divide-by-zero


def test_unknown_backend_raises():
    with pytest.raises(ValueError):
        make_embedder("nope")


# --- data files and handlers -------------------------------------------------

def test_load_examples_reads_pairs():
    pairs = load_examples()
    assert pairs and all(isinstance(q, str) and isinstance(r, str) for q, r in pairs)
    assert {r for _, r in pairs} == {"code", "talk", "refine"}


def test_every_route_has_a_handler():
    routes = set(json.loads(EXAMPLES.read_text()))
    assert routes <= set(HANDLERS)
    assert inspect.signature(Router).parameters["fallback"].default in HANDLERS  # default fallback too


def test_refine_runs_two_steps():
    out = run_refine("q")
    assert "[DRAFT]" in out and "[REFINED]" in out


def test_cases_cover_the_same_routes_as_seeds():
    cases = json.loads(CASES.read_text())["cases"]
    assert set(cases) == set(json.loads(EXAMPLES.read_text()))


def test_cases_do_not_repeat_seeds():
    seeds = {q.lower() for q, _ in load_examples()}
    data = json.loads(CASES.read_text())
    queries = [q for qs in data["cases"].values() for q in qs] + data["vague"]
    assert not seeds & {q.lower() for q in queries}
    assert len(queries) == len(set(queries))


# --- real model (slow, opt-in) -----------------------------------------------

@pytest.mark.skipif(os.getenv("SCRAPPY_SLOW") != "1", reason="set SCRAPPY_SLOW=1 to run the real model")
def test_real_model_accuracy_floor():
    """Guards against regressions with the real embedder. Floors sit a bit under current results."""
    r = Router()
    r.add_rules(load_examples())
    data = json.loads(CASES.read_text())
    labeled = [(q, route) for route, qs in data["cases"].items() for q in qs]
    acc = sum(r.route(q) == route for q, route in labeled) / len(labeled)
    vague = sum(r.route(q) == r.fallback for q in data["vague"]) / len(data["vague"])
    assert acc >= 0.80, f"accuracy {acc:.0%}"
    assert vague >= 0.80, f"vague fallback {vague:.0%}"
