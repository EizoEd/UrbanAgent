from __future__ import annotations

from collections.abc import Callable
from typing import Any, Optional

from urban_agent.planner import TaskPlanner
from urban_agent.router import IntentRouter
from urban_agent.schemas import EvidenceItem, QueryRequest, WorkflowResult
from urban_agent.spatial import Feature, SpatialActionService
from urban_agent.synthesis import EvidenceSynthesizer
from urban_agent.verifier import Verifier


EvidenceProvider = Callable[[QueryRequest], list[EvidenceItem]]


class UrbanAgentCore:
    """A compact source snapshot of the UrbanAgent orchestration loop."""

    def __init__(self, evidence_provider: Optional[EvidenceProvider] = None) -> None:
        self.router = IntentRouter()
        self.planner = TaskPlanner()
        self.spatial = SpatialActionService()
        self.synthesizer = EvidenceSynthesizer()
        self.verifier = Verifier()
        self.evidence_provider = evidence_provider or (lambda _request: [])

    def run(self, request: QueryRequest) -> WorkflowResult:
        trace: list[str] = []

        route = self.router.route(request.query, metadata=request.metadata, mode=request.mode)
        trace.append("route")

        plan = self.planner.build(request.query, route)
        trace.append("plan")

        evidence = self.evidence_provider(request)
        trace.append("retrieve")

        spatial_payload = self._maybe_spatial_payload(route_query_type=route.query_type, metadata=request.metadata)
        if spatial_payload:
            trace.append("spatial")

        synthesis = self.synthesizer.synthesize(
            query=request.query,
            evidence=evidence,
            spatial_payload=spatial_payload,
            tool_outputs=[],
        )
        trace.append("synthesize")

        verification = self.verifier.verify(route=route, synthesis=synthesis, evidence=evidence)
        trace.append("verify")

        if verification.requires_review:
            trace.append("human_review")
        elif verification.response_type == "answer":
            trace.append("writeback_allowed")
        else:
            trace.append("writeback_blocked")

        return WorkflowResult(
            route=route,
            plan=plan,
            synthesis=synthesis,
            verification=verification,
            trace=trace,
        )

    def _maybe_spatial_payload(self, route_query_type: str, metadata: dict[str, Any]) -> Optional[dict[str, Any]]:
        if route_query_type not in {"spatial_qa", "gis_task", "comprehensive"}:
            return None

        features = [
            Feature(
                feature_id=str(item.get("id", idx)),
                lon=float(item["lon"]),
                lat=float(item["lat"]),
                properties=dict(item.get("properties", {})),
            )
            for idx, item in enumerate(metadata.get("features", []), start=1)
            if "lon" in item and "lat" in item
        ]
        if not features:
            return None

        bbox = metadata.get("bbox")
        if isinstance(bbox, (list, tuple)) and len(bbox) == 4:
            return self.spatial.query_by_bbox(features, tuple(float(value) for value in bbox))

        center = metadata.get("center")
        distance_km = metadata.get("distance_km")
        if isinstance(center, (list, tuple)) and len(center) == 2 and distance_km is not None:
            return self.spatial.query_by_distance(
                features,
                (float(center[0]), float(center[1])),
                float(distance_km),
            )
        return None
