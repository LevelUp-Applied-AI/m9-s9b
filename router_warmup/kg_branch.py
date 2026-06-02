"""Optional warm-up — stub showing where the critic plugs into an M8 query-router.

This file is NOT autograded. It is rubric-relevant only. Delete or modify
freely. See router_warmup/README.md for the integration pattern.
"""

from critic import verify_claim
from extractor import extract_triples_from_text


def kg_branch(user_question: str, fuseki_endpoint: str) -> dict:
    """Route a claim-shaped question to the critic and return a router response.

    The shape of this function mirrors what the M8 stretch router expects:
    a callable that takes a question and returns a dict the router can
    surface to the user.
    """
    # TODO: extract candidate (s, p, o) claims from the user_question.
    claims = extract_triples_from_text(user_question)

    if not claims:
        return {"route": "kg_branch", "response": "No verifiable claim found.", "evidence": []}

    # TODO: in your M8 router, you might verify only the highest-confidence
    # extracted claim, or aggregate verdicts across all extracted claims.
    verdicts = [verify_claim(c, fuseki_endpoint) for c in claims]

    # TODO: convert Verdict objects into the response shape your router uses.
    return {
        "route": "kg_branch",
        "verdicts": [v.verdict for v in verdicts],
        "evidence": [v.evidence_triples for v in verdicts],
    }
