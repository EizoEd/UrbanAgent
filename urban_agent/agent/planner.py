from __future__ import annotations

from urban_agent.schemas import Plan, PlanStep, RouteDecision, SubGoal


class TaskPlanner:
    """Builds a public-safe hierarchical plan from a route decision."""

    def build(self, query: str, route: RouteDecision) -> Plan:
        steps: list[PlanStep] = [
            PlanStep("s1", "load_context", "memory_context", "Load short task context and safe session summary."),
            PlanStep("s2", "retrieve_evidence", "retrieval_adapter", "Retrieve public-safe supporting evidence."),
        ]
        subgoals: list[SubGoal] = [
            SubGoal("sg1", "evidence_collection", "Collect context and evidence for a grounded answer.", ["s1", "s2"])
        ]

        if route.query_type in {"spatial_qa", "gis_task", "comprehensive"}:
            steps.append(
                PlanStep("s3", "run_spatial_action", "spatial_adapter", "Apply region, distance, or layer constraints.")
            )
            subgoals.append(SubGoal("sg2", "spatial_reasoning", "Generate map-ready spatial output.", ["s3"]))

        if route.workflow_mode == "agent":
            steps.append(
                PlanStep("s4", "optional_tool_enrichment", "tool_registry", "Call approved tools when required.")
            )
            subgoals.append(SubGoal("sg3", "tool_enrichment", "Use governed tool outputs to enrich analysis.", ["s4"]))

        steps.append(
            PlanStep(
                "s5",
                "synthesize_and_verify",
                "synthesizer_verifier",
                "Create final response and check grounding, solvability, and review requirements.",
                route.requires_review,
            )
        )
        subgoals.append(SubGoal("sg4", "answer_governance", "Synthesize findings and decide review path.", ["s5"]))

        return Plan(
            objective=query,
            top_goal=f"Resolve {route.query_type} request with evidence and governance.",
            subgoals=subgoals,
            steps=steps,
        )
