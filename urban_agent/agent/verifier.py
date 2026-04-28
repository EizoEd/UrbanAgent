from __future__ import annotations

from urban_agent.governance.review import ReviewPolicy
from urban_agent.schemas import EvidenceItem, RouteDecision, SynthesisResult, VerificationResult


class Verifier:
    """Checks grounding, missing inputs, solvability, and review requirements."""

    def __init__(self, review_policy: ReviewPolicy | None = None) -> None:
        self.review_policy = review_policy or ReviewPolicy()

    def verify(
        self,
        route: RouteDecision,
        synthesis: SynthesisResult,
        evidence: list[EvidenceItem],
    ) -> VerificationResult:
        reason_codes: list[str] = []
        missing_inputs: list[str] = []
        suggested_actions: list[str] = []

        if not evidence:
            reason_codes.append("no_evidence")
            missing_inputs.append("public evidence")
            suggested_actions.append("Add a source collection or retrieval adapter output.")

        if route.query_type in {"spatial_qa", "gis_task"} and not synthesis.map_layers:
            reason_codes.append("missing_spatial_payload")
            missing_inputs.append("spatial result")
            suggested_actions.append("Provide region, distance, or layer metadata.")

        review_required = self.review_policy.requires_review(route=route, synthesis=synthesis)
        if review_required:
            reason_codes.append("review_required")
            suggested_actions.append("Route this result to a human reviewer before final use.")

        if "no_evidence" in reason_codes:
            return VerificationResult(False, "cannot_solve", "medium", reason_codes, missing_inputs, suggested_actions)

        if "missing_spatial_payload" in reason_codes:
            return VerificationResult(False, "needs_clarification", "medium", reason_codes, missing_inputs, suggested_actions)

        return VerificationResult(
            passed=not review_required,
            response_type="answer",
            risk_level="high" if review_required else "low",
            reason_codes=reason_codes,
            missing_inputs=missing_inputs,
            suggested_actions=suggested_actions,
            requires_review=review_required,
        )
