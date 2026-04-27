from __future__ import annotations

from urban_agent.schemas import EvidenceItem, RouteDecision, SynthesisResult, VerificationResult


class Verifier:
    """Checks whether a synthesized result is grounded and safe to answer."""

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

        if route.requires_review:
            reason_codes.append("review_required")
            suggested_actions.append("Route this result to a human reviewer before final use.")

        if "no_evidence" in reason_codes:
            return VerificationResult(
                passed=False,
                response_type="cannot_solve",
                risk_level="medium",
                reason_codes=reason_codes,
                missing_inputs=missing_inputs,
                suggested_actions=suggested_actions,
                requires_review=False,
            )

        if "missing_spatial_payload" in reason_codes:
            return VerificationResult(
                passed=False,
                response_type="needs_clarification",
                risk_level="medium",
                reason_codes=reason_codes,
                missing_inputs=missing_inputs,
                suggested_actions=suggested_actions,
                requires_review=False,
            )

        return VerificationResult(
            passed=not route.requires_review,
            response_type="answer",
            risk_level="high" if route.requires_review else "low",
            reason_codes=reason_codes,
            missing_inputs=missing_inputs,
            suggested_actions=suggested_actions,
            requires_review=route.requires_review,
        )
