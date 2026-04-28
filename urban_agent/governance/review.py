from __future__ import annotations

from dataclasses import dataclass

from urban_agent.schemas import RouteDecision, SynthesisResult


@dataclass
class ReviewDecision:
    action: str
    reviewer: str = "public-reviewer"
    reason: str = ""


class ReviewPolicy:
    """Minimal review policy for public examples."""

    def requires_review(self, route: RouteDecision, synthesis: SynthesisResult) -> bool:
        if route.requires_review:
            return True
        if not synthesis.citations and route.workflow_mode == "agent":
            return True
        return False

    def apply(self, decision: ReviewDecision, current_status: str) -> str:
        if decision.action == "approve":
            return "completed"
        if decision.action == "reject":
            return "rejected"
        if decision.action == "edit":
            return "needs_revision"
        return current_status
