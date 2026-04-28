from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal

from urban_agent.schemas.evidence import SynthesisResult
from urban_agent.schemas.planning import Plan
from urban_agent.schemas.request import ResponseType, RouteDecision


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
