from __future__ import annotations

from dataclasses import dataclass, field


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
