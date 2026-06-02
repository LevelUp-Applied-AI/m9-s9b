# Module 9 Week B — Stretch (Honors Track): KG Critic / Verifier Agent

> **Honors Track.** This stretch is for learners who have completed the required Week B work (Reading, Drill, Lab, Integration) and are On Track or Advanced. Stretch is not required for program completion but is required for Honors distinction. See the Honors track policy for eligibility.

For the full task description, see the assignment page: **Module 9 Week B — Stretch: KG Critic / Verifier Agent**.

## What you are building

A **KG critic** — an agent that takes a claim `(subject, predicate, object)` and decides whether the recipes KG **supports**, **entails**, **contradicts**, or fails to address (**unsupported**) the claim. The critic operationalizes the open-world assumption: it abstains explicitly when the KG is silent, rather than guessing.

You implement the cascade in `critic/verify.py`. The starter ships:

- `critic/types.py` — `Verdict` dataclass (fully implemented; do not modify).
- `critic/verify.py` — `verify_claim(claim, fuseki_endpoint)` — **your work**.
- `extractor/triples.py` — a small regex-based claim extractor (fully implemented; you may improve it, but you do not have to).
- `data/recipes_kg.ttl` — the same KG as Lab 9B.
- `data/eval_claims.jsonl` — 40 labeled claims (20 supported, 10 entailed-only, 10 contradicted). The autograder runs against this set.
- `router_warmup/` — **optional** stub for composing the critic with the M8 query-router stretch. Not autograder-gated; rubric points only.

## Setup

```bash
# Start Fuseki
docker compose up -d

# Install dependencies (cached from the lab — should be fast)
pip install -r requirements.txt

# Load the KG
python load_dataset.py

# Run the autograder
pytest tests/ -v
```

## The verdict cascade

`verify_claim` should resolve a claim through these stages, in order:

1. **`ASK`** the literal triple. If the KG asserts it directly → `supported`.
2. **Entailment** — query whether the claim is entailed by an `rdfs:subClassOf*` or `skos:broader*` chain. If the chain holds → `entailed`.
3. **Domain/range check** — if the predicate has `rdfs:domain D` and the subject's `rdf:type` is incompatible with `D` (no subclass path from the subject's type to `D`), or the same situation for `rdfs:range` and the object → `contradicted`.
4. Otherwise → `unsupported`.

The order matters. A claim that is literally present is `supported`, not `entailed`. A claim where the entailment chain holds AND the domain/range is satisfied is `entailed`, not `contradicted`.

## Autograder gates

The autograder runs `verify_claim` over `data/eval_claims.jsonl` and checks:

| Class | Metric | Threshold |
|---|---|---|
| `supported` | precision and recall | ≥ 0.90 |
| `entailed-only` | recall | ≥ 0.60 |
| `contradicted` | precision | ≥ 0.75 |

If you only implement step 1 (`ASK`), `entailed-only` recall will be 0. If you label everything-not-supported as `contradicted`, your `contradicted` precision will tank.

## Optional warm-up — M8 router integration

`router_warmup/` shows where `verify_claim` plugs into the M8 query-router stretch as a **KG branch**. If you completed the M8 stretch, wire your router to call the critic; if not, leave the file untouched (the autograder does not gate on it).

---

## License

This repository is provided for educational use only. See [LICENSE](LICENSE) for terms.

You may clone and modify this repository for personal learning and practice, and reference code you wrote here in your professional portfolio. Redistribution outside this course is not permitted.
