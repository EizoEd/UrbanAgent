from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal


QueryType = Literal["qa", "spatial_qa", "gis_task", "comprehensive", "data_ops"]
WorkflowMode = Literal["short", "agent"]
ResponseType = Literal["answer", "cannot_solve", "needs_clarification"]


@dataclass
class QueryRequest:
    query: str
    mode: str = "auto"
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class RouteDecision:
    query_type: QueryType
    workflow_mode: WorkflowMode
    confidence: float
    reason: str
    requires_review: bool = False
