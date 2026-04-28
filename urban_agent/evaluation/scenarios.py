from __future__ import annotations

from dataclasses import dataclass


@dataclass
class EvaluationScenario:
    scenario_id: str
    query: str
    expected_route: str
    notes: str


def default_scenarios() -> list[EvaluationScenario]:
    return [
        EvaluationScenario("qa_policy", "What evidence supports urban growth monitoring?", "qa", "Evidence QA"),
        EvaluationScenario("spatial_bbox", "Find parcels within this region", "spatial_qa", "Spatial filtering"),
        EvaluationScenario("gis_change", "Compare layer change by year", "gis_task", "Temporal GIS task"),
        EvaluationScenario("data_ingest", "Upload and parse this planning file", "data_ops", "Data operation"),
    ]
