"""Shared types for the KG critic.

Fully implemented — do not modify. Import these from ``critic.verify`` to
construct verdicts.
"""

from dataclasses import dataclass, field
from typing import Literal

VerdictLabel = Literal["supported", "entailed", "contradicted", "unsupported"]


@dataclass(frozen=True)
class Verdict:
    """One critic decision over a single (subject, predicate, object) claim.

    Attributes
    ----------
    verdict : VerdictLabel
        One of ``"supported"``, ``"entailed"``, ``"contradicted"``, ``"unsupported"``.
    evidence_triples : list[tuple]
        Triples the critic relied on to reach this verdict. May be empty
        for ``unsupported``. For ``supported`` / ``entailed`` this should
        contain the triple(s) the critic queried. For ``contradicted``
        this should contain the conflicting type and domain/range
        constraints.
    confidence : float
        Calibrated confidence in [0.0, 1.0]. Use higher values when the
        evidence is direct (``ASK`` hit) and lower values when the
        evidence rests on a long entailment chain or abstention.
    """

    verdict: VerdictLabel
    evidence_triples: list[tuple] = field(default_factory=list)
    confidence: float = 0.0
