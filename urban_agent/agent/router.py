from __future__ import annotations

from typing import Any, Optional

from urban_agent.schemas import QueryType, RouteDecision, WorkflowMode


_SPATIAL_TERMS = {
    "area",
    "bbox",
    "buffer",
    "distance",
    "district",
    "intersect",
    "layer",
    "near",
    "polygon",
    "region",
    "within",
}
_TEMPORAL_TERMS = {"change", "compare", "trend", "time", "timeseries", "year"}
_DATA_TERMS = {"clean", "export", "import", "ingest", "merge", "parse", "upload"}
_COMPREHENSIVE_TERMS = {"first", "then", "finally", "workflow", "multi-step", "synthesize"}
_HIGH_RISK_TERMS = {"approve", "compliance", "guarantee", "legal", "liability", "permit"}


class IntentRouter:
    """Public-safe deterministic router for urban analysis requests."""

    def route(self, query: str, metadata: Optional[dict[str, Any]] = None, mode: str = "auto") -> RouteDecision:
        meta = metadata or {}
        text = query.lower()
        terms = _token_hits(text)

        has_spatial = bool(terms & _SPATIAL_TERMS or meta.get("bbox") or meta.get("polygon") or meta.get("center"))
        has_temporal = bool(terms & _TEMPORAL_TERMS)
        has_data_ops = bool(terms & _DATA_TERMS)
        has_comprehensive = bool(terms & _COMPREHENSIVE_TERMS or mode == "analysis")
        has_high_risk = bool(terms & _HIGH_RISK_TERMS or meta.get("requires_review"))

        query_type: QueryType = "qa"
        workflow_mode: WorkflowMode = "short"
        reason = "default evidence question"
        confidence = 0.72

        if has_temporal and has_spatial:
            query_type = "gis_task"
            workflow_mode = "agent"
            reason = "spatial temporal comparison"
            confidence = 0.9
        elif has_data_ops:
            query_type = "data_ops"
            workflow_mode = "agent"
            reason = "data operation request"
            confidence = 0.86
        elif has_comprehensive:
            query_type = "comprehensive"
            workflow_mode = "agent"
            reason = "multi-step analysis request"
            confidence = 0.84
        elif has_spatial:
            query_type = "spatial_qa"
            workflow_mode = "short"
            reason = "spatial constraint request"
            confidence = 0.86

        if has_high_risk:
            workflow_mode = "agent"
            confidence = min(confidence, 0.62)
            reason = f"{reason}; review-sensitive wording"

        return RouteDecision(
            query_type=query_type,
            workflow_mode=workflow_mode,
            confidence=confidence,
            reason=reason,
            requires_review=has_high_risk,
        )


def _token_hits(text: str) -> set[str]:
    normalized = text.replace("_", " ").replace("-", " ")
    return {part.strip(".,:;!?()[]{}") for part in normalized.split() if part.strip()}
