"""KG critic — verify a (subject, predicate, object) claim against the recipes KG.

You implement ``verify_claim(claim, fuseki_endpoint) -> Verdict``. The
``Verdict`` dataclass in ``critic/types.py`` is fully defined; construct
and return it from your cascade.
"""

from typing import Tuple

from critic.types import Verdict

DEFAULT_ENDPOINT = "http://localhost:3030/recipes/sparql"

# Triple is (subject_uri_or_curie, predicate_uri_or_curie, object_uri_or_curie_or_literal).
Claim = Tuple[str, str, str]


def verify_claim(claim: Claim, fuseki_endpoint: str = DEFAULT_ENDPOINT) -> Verdict:
    """Decide whether the KG supports, entails, contradicts, or fails to address ``claim``.

    Returns a Verdict whose ``verdict`` label is one of
    ``"supported" | "entailed" | "contradicted" | "unsupported"`` and whose
    ``evidence_triples`` and ``confidence`` reflect what your cascade found.

    See the assignment page for the full cascade specification (ASK,
    entailment via ``rdfs:subClassOf*`` / ``skos:broader*``, domain/range
    check, abstain).
    """
    # TODO: Stage 1 — ASK against the Fuseki endpoint for the literal triple.
    # If the KG asserts the triple directly, return a supported Verdict
    # with the queried triple as evidence and high confidence.

    # TODO: Stage 2 — query whether the claim is entailed via an
    # rdfs:subClassOf* or skos:broader* chain (this is the hard class —
    # without this stage, entailed-only recall stays at 0).
    # If the chain holds, return an entailed Verdict.

    # TODO: Stage 3 — domain/range check. Inspect the predicate's
    # rdfs:domain and rdfs:range; if the subject's rdf:type is incompatible
    # with the domain (no rdfs:subClassOf* path) or the object's type with
    # the range, return a contradicted Verdict.

    # TODO: Stage 4 — abstain. Return an unsupported Verdict with low
    # confidence and no evidence triples.
    raise NotImplementedError(
        "Implement verify_claim() — see the stretch assignment page for the cascade."
    )
