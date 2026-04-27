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


@dataclass
class PlanStep:
    step_id: str
    name: str
    tool_name: str
    description: str
    requires_review: bool = False


@dataclass
class SubGoal:
    subgoal_id: str
    name: str
    objective: str
    step_ids: list[str] = field(default_factory=list)


@dataclass
class Plan:
    objective: str
    top_goal: str
    subgoals: list[SubGoal]
    steps: list[PlanStep]


@dataclass
class EvidenceItem:
    source_id: str
    title: str
    text: str
    score: float = 0.0
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class SynthesisResult:
    summary: str
    key_findings: list[str] = field(default_factory=list)
    citations: list[dict[str, Any]] = field(default_factory=list)
    map_layers: list[dict[str, Any]] = field(default_factory=list)
    follow_up_actions: list[str] = field(default_factory=list)


@dataclass
class VerificationResult:
    passed: bool
    response_type: ResponseType
    risk_level: Literal["low", "medium", "high"]
    reason_codes: list[str] = field(default_factory=list)
    missing_inputs: list[str] = field(default_factory=list)
    suggested_actions: list[str] = field(default_factory=list)
    requires_review: bool = False


@dataclass
class WorkflowResult:
    route: RouteDecision
    plan: Plan
    synthesis: SynthesisResult
    verification: VerificationResult
    trace: list[str] = field(default_factory=list)
