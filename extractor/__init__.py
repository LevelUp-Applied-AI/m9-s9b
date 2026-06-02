"""Claim extractor — pulls candidate (s, p, o) triples from a RAG-style answer string."""

from extractor.triples import extract_triples_from_text

__all__ = ["extract_triples_from_text"]
