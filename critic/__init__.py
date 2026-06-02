"""KG critic — verify (subject, predicate, object) claims against the recipes KG."""

from critic.types import Verdict
from critic.verify import verify_claim

__all__ = ["Verdict", "verify_claim"]
