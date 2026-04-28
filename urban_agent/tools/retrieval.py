from __future__ import annotations

from urban_agent.schemas import EvidenceItem, QueryRequest


class InMemoryRetrievalAdapter:
    """Tiny retrieval adapter for examples and tests.

    It stands in for a private RAG service without exposing service endpoints or
    runtime configuration.
    """

    def __init__(self, evidence: list[EvidenceItem] | None = None) -> None:
        self.evidence = list(evidence or [])

    def search(self, request: QueryRequest) -> list[EvidenceItem]:
        terms = {part.lower() for part in request.query.split() if len(part) > 2}
        if not terms:
            return self.evidence[:5]
        scored = []
        for item in self.evidence:
            body = f"{item.title} {item.text}".lower()
            overlap = sum(1 for term in terms if term in body)
            if overlap:
                scored.append(EvidenceItem(item.source_id, item.title, item.text, item.score + overlap, item.metadata))
        return sorted(scored, key=lambda item: item.score, reverse=True)[:5]
