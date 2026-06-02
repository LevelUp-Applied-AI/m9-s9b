# Optional warm-up — plug the critic into your M8 query-router stretch

> **This section is OPTIONAL and is NOT autograder-gated.** It is rubric-relevant only (see the stretch assignment page rubric, dimension "README + optional warm-up"). If you did not complete the M8 stretch (Query Router), leave this directory untouched — the autograder ignores it.

## What this is

The M8 stretch shipped a **query router** — a classifier that decides whether an incoming question routes to:
- a vector retriever (RAG over `recipes_kg.ttl` chunks),
- a SPARQL query against the KG,
- or a fallback "I don't know" response.

The M9B critic gives you a fourth branch: **claim verification**. A learner question like *"Is eggplant a vegetable?"* is not a retrieval question — it is a claim. The router can dispatch claim-shaped questions to `verify_claim(...)` and surface the verdict.

## How to wire it in

See `kg_branch.py` for the stub. The pattern, in words:

1. In your M8 router, detect claim-shaped inputs (e.g., yes/no questions, "is X a Y" phrasing). The included `extractor.triples.extract_triples_from_text` is a starting point.
2. For each extracted claim, call `verify_claim(claim, FUSEKI_ENDPOINT)`.
3. Convert the `Verdict` to a router-shaped response (supported / entailed → confirm; contradicted → refute with evidence; unsupported → "the KG does not address this").

## Why it lives here, not in the M8 repo

The M9B critic is the **new capability** introduced this week. The warm-up shows you where it plugs in, but does not require you to maintain your M8 repo here. Write up your integration approach in the main README and (optionally) commit a working wire-up in your M8 stretch repo on its own branch.
