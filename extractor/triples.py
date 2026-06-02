"""Simple regex/keyword claim extractor.

Fully implemented. You can use this as a black box to turn a RAG-style
natural-language answer into a list of (subject, predicate, object) claims
to feed into the critic. You are free to improve it (better tokenization,
spaCy parsing, etc.) but you do not have to — the autograder grades the
critic, not the extractor.
"""

import re
from typing import List, Tuple

PREFIX = "http://aispire.example.org/recipes/"

# Surface-form → URI mappings, derived from the recipes KG's skos:prefLabel
# and skos:altLabel. Lowercased on lookup.
_INGREDIENT_TERMS = {
    "eggplant": "eggplant", "aubergine": "eggplant",
    "basil": "basil", "sweet basil": "basil",
    "salt": "salt",
    "parmesan": "parmesan", "parmigiano": "parmesan",
    "tomato": "tomato",
    "garlic": "garlic",
    "orange": "orangeFruit", "naranja": "orangeFruit",
    "turkey": "turkeyMeat", "tom": "turkeyMeat",
}
_CUISINE_TERMS = {
    "italian": "Italian", "french": "French", "greek": "Greek",
    "thai": "Thai", "japanese": "Japanese", "mexican": "Mexican",
    "european": "European", "asian": "Asian",
    "turkish": "turkeyCuisine",
}
_AUTHOR_TERMS = {
    "anna": "annaAuthor", "sarah": "sarahAuthor", "marco": "marcoAuthor",
    "yuki": "yukiAuthor", "raj": "rajAuthor",
}

Claim = Tuple[str, str, str]


def _uri(local: str) -> str:
    return PREFIX + local


def extract_triples_from_text(text: str) -> List[Claim]:
    """Return candidate (subject, predicate, object) triples found in ``text``.

    Heuristic: scan for "X is a Y" / "X has Y" / "by Y" patterns and emit
    rdf:type or property triples. Returns an empty list when no patterns match.
    """
    text_l = text.lower()
    out: List[Claim] = []

    # "<term> is a <type>" → (term_uri, rdf:type, type_uri)
    for m in re.finditer(r"\b([a-z]+)\s+is\s+(?:an?\s+)?([a-z]+)\b", text_l):
        subj, obj = m.group(1), m.group(2)
        if subj in _INGREDIENT_TERMS and obj in {"ingredient", "vegetable"}:
            out.append(
                (_uri(_INGREDIENT_TERMS[subj]),
                 "http://www.w3.org/1999/02/22-rdf-syntax-ns#type",
                 _uri("Ingredient") if obj == "ingredient" else _uri("Vegetable"))
            )
        if subj in _CUISINE_TERMS and obj == "cuisine":
            out.append(
                (_uri(_CUISINE_TERMS[subj]),
                 "http://www.w3.org/1999/02/22-rdf-syntax-ns#type",
                 _uri("Cuisine"))
            )

    # "by <author>" → recipe :authoredBy author (subject left as a placeholder)
    for m in re.finditer(r"\bby\s+([a-z]+)\b", text_l):
        name = m.group(1)
        if name in _AUTHOR_TERMS:
            out.append(("?recipe", _uri("authoredBy"), _uri(_AUTHOR_TERMS[name])))

    return out
