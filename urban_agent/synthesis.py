from __future__ import annotations

from typing import Any, Optional

from urban_agent.schemas import EvidenceItem, SynthesisResult


class EvidenceSynthesizer:
    """Turns evidence and tool outputs into a stable response shape."""

    def synthesize(
        self,
        query: str,
        evidence: list[EvidenceItem],
        spatial_payload: Optional[dict[str, Any]] = None,
        tool_outputs: Optional[list[dict[str, Any]]] = None,
    ) -> SynthesisResult:
        top_evidence = sorted(evidence, key=lambda item: item.score, reverse=True)[:5]
        citations = [
            {"source_id": item.source_id, "title": item.title, "score": round(float(item.score), 3)}
            for item in top_evidence
        ]
        findings = [item.text.strip() for item in top_evidence if item.text.strip()]
        map_layers = []
        if spatial_payload:
            map_layers.append(
                {
                    "name": spatial_payload.get("name", "spatial_result"),
                    "feature_count": len(spatial_payload.get("features", [])),
                    "payload_type": spatial_payload.get("type", "FeatureCollection"),
                }
            )

        tool_count = len(tool_outputs or [])
        summary = _build_summary(query=query, findings=findings, tool_count=tool_count, has_map=bool(map_layers))
        follow_up = []
        if not citations:
            follow_up.append("Add public evidence sources before using this result for decisions.")
        if map_layers:
            follow_up.append("Review map payload geometry and layer metadata before publication.")

        return SynthesisResult(
            summary=summary,
            key_findings=findings[:3],
            citations=citations,
            map_layers=map_layers,
            follow_up_actions=follow_up,
        )


def _build_summary(query: str, findings: list[str], tool_count: int, has_map: bool) -> str:
    if not findings:
        return f"No grounded answer can be produced for: {query}"
    parts = [f"Found {len(findings)} evidence-backed point(s) for: {query}"]
    if has_map:
        parts.append("Spatial output is available for downstream map rendering.")
    if tool_count:
        parts.append(f"{tool_count} governed tool output(s) were incorporated.")
    return " ".join(parts)
