from __future__ import annotations

from urban_agent.schemas import Plan, PlanStep, RouteDecision, SubGoal


class TaskPlanner:
    """Builds a compact hierarchical plan from a route decision."""

    def build(self, query: str, route: RouteDecision) -> Plan:
        steps: list[PlanStep] = [
            PlanStep(
                step_id="s1",
                name="load_context",
                tool_name="memory_context",
                description="Load short task context and safe session summary.",
            ),
            PlanStep(
                step_id="s2",
                name="retrieve_evidence",
                tool_name="retrieval_adapter",
                description="Retrieve public-safe supporting evidence.",
            ),
        ]
        subgoals: list[SubGoal] = [
            SubGoal(
                subgoal_id="sg1",
                name="evidence_collection",
                objective="Collect context and evidence needed for a grounded answer.",
                step_ids=["s1", "s2"],
            )
        ]

        if route.query_type in {"spatial_qa", "gis_task", "comprehensive"}:
            steps.append(
                PlanStep(
                    step_id="s3",
                    name="run_spatial_action",
                    tool_name="spatial_adapter",
                    description="Apply region, distance, or layer comparison constraints.",
                )
            )
            subgoals.append(
                SubGoal(
                    subgoal_id="sg2",
                    name="spatial_reasoning",
                    objective="Generate structured map-ready spatial output.",
                    step_ids=["s3"],
                )
            )

        if route.workflow_mode == "agent":
            steps.append(
                PlanStep(
                    step_id="s4",
                    name="optional_tool_enrichment",
                    tool_name="tool_registry",
                    description="Call approved external tools or skills when required.",
                )
            )
            subgoals.append(
                SubGoal(
                    subgoal_id="sg3",
                    name="tool_enrichment",
                    objective="Use governed tools to enrich the task result.",
                    step_ids=["s4"],
                )
            )

        steps.append(
            PlanStep(
                step_id="s5",
                name="synthesize_and_verify",
                tool_name="synthesizer_verifier",
                description="Create the final response and check risk, grounding, and solvability.",
                requires_review=route.requires_review,
            )
        )
        subgoals.append(
            SubGoal(
                subgoal_id="sg4",
                name="answer_governance",
                objective="Synthesize findings and decide whether review is needed.",
                step_ids=["s5"],
            )
        )

        return Plan(
            objective=query,
            top_goal=f"Resolve {route.query_type} request with evidence and governance.",
            subgoals=subgoals,
            steps=steps,
        )
