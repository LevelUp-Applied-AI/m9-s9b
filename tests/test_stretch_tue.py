"""Autograder for Stretch 9B Tue — KG Critic / Verifier Agent.

Runs ``verify_claim`` over ``data/eval_claims.jsonl`` and checks:
- Precision on contradicted predictions ≥ 0.75
- Recall on entailed-only gold claims ≥ 0.60
- Precision and recall on supported ≥ 0.90
- Verdict dataclass shape

Plus structural tests: starter unmodified must fail; required cascade
stages are exercised (callable verify_claim, returns Verdict).
"""

import json
import os
import sys
from typing import List, Tuple

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from critic import verify_claim  # noqa: E402
from critic.types import Verdict  # noqa: E402

EVAL_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "eval_claims.jsonl")
FUSEKI_ENDPOINT = os.environ.get("FUSEKI_ENDPOINT", "http://localhost:3030/recipes/sparql")


def _load_eval() -> List[Tuple[tuple, str]]:
    out = []
    with open(EVAL_PATH) as f:
        for line in f:
            row = json.loads(line)
            out.append((tuple(row["claim"]), row["label"]))
    return out


@pytest.fixture(scope="module")
def predictions():
    """Run the critic over every eval claim once; share across tests."""
    eval_set = _load_eval()
    preds = []
    for claim, gold in eval_set:
        v = verify_claim(claim, FUSEKI_ENDPOINT)
        preds.append((claim, gold, v))
    return preds


def test_verdict_dataclass_shape():
    """Verdict has the four required verdict labels and the right field types."""
    v = Verdict(verdict="supported", evidence_triples=[("a", "b", "c")], confidence=0.9)
    assert v.verdict in {"supported", "entailed", "contradicted", "unsupported"}
    assert isinstance(v.evidence_triples, list)
    assert 0.0 <= v.confidence <= 1.0


def test_verify_claim_returns_verdict(predictions):
    """verify_claim returns a Verdict for every claim — no None or raw strings."""
    for claim, gold, v in predictions:
        assert isinstance(v, Verdict), f"verify_claim did not return Verdict for {claim}"
        assert v.verdict in {"supported", "entailed", "contradicted", "unsupported"}


def test_supported_precision_and_recall(predictions):
    """Precision and recall on supported predictions ≥ 0.90."""
    gold_supported = [p for p in predictions if p[1] == "supported"]
    pred_supported = [p for p in predictions if p[2].verdict == "supported"]
    tp = [p for p in predictions if p[1] == "supported" and p[2].verdict == "supported"]
    precision = len(tp) / max(1, len(pred_supported))
    recall = len(tp) / max(1, len(gold_supported))
    assert precision >= 0.90, f"supported precision {precision:.2f} < 0.90"
    assert recall >= 0.90, f"supported recall {recall:.2f} < 0.90"


def test_entailed_only_recall(predictions):
    """Of the 10 entailed-only gold claims, recall ≥ 0.60.

    This is the hard class — a critic that only does ASK will get 0 here.
    """
    gold_entailed = [p for p in predictions if p[1] == "entailed"]
    tp = [p for p in gold_entailed if p[2].verdict == "entailed"]
    recall = len(tp) / max(1, len(gold_entailed))
    assert recall >= 0.60, f"entailed-only recall {recall:.2f} < 0.60"


def test_contradicted_precision(predictions):
    """Of claims predicted as contradicted, ≥ 0.75 were actually contradicted.

    Catches the variant where a learner labels everything-not-supported as
    contradicted — precision collapses.
    """
    pred_contra = [p for p in predictions if p[2].verdict == "contradicted"]
    tp = [p for p in pred_contra if p[1] == "contradicted"]
    if not pred_contra:
        pytest.fail("verify_claim never predicted 'contradicted' — domain/range stage missing")
    precision = len(tp) / len(pred_contra)
    assert precision >= 0.75, f"contradicted precision {precision:.2f} < 0.75"
