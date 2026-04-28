from urban_agent import UrbanAgentCore
from urban_agent.governance import MemoryWritePolicy
from urban_agent.schemas import EvidenceItem, QueryRequest
from urban_agent.evaluation import default_scenarios
from urban_agent.tools.spatial import Feature, SpatialActionService


def test_short_qa_flow_answers_with_evidence() -> None:
    agent = UrbanAgentCore(
        evidence_provider=lambda _request: [
            EvidenceItem(source_id="public-doc-1", title="Public Note", text="Urban growth should be evidence-led.", score=0.9)
        ]
    )

    result = agent.run(QueryRequest(query="What evidence supports urban growth monitoring?"))

    assert result.route.query_type == "qa"
    assert result.verification.response_type == "answer"
    assert "retrieve" in result.trace


def test_spatial_flow_needs_payload_when_missing_features() -> None:
    agent = UrbanAgentCore(
        evidence_provider=lambda _request: [
            EvidenceItem(source_id="public-doc-1", title="Public Note", text="Spatial filtering requires geometry.", score=0.8)
        ]
    )

    result = agent.run(QueryRequest(query="Find parcels within this region", metadata={"bbox": [0, 0, 1, 1]}))

    assert result.route.query_type == "spatial_qa"
    assert result.verification.response_type == "needs_clarification"


def test_spatial_bbox_query() -> None:
    service = SpatialActionService()
    features = [
        Feature(feature_id="a", lon=0.5, lat=0.5),
        Feature(feature_id="b", lon=5.0, lat=5.0),
    ]

    payload = service.query_by_bbox(features, (0, 0, 1, 1))

    assert [item["id"] for item in payload["features"]] == ["a"]


def test_memory_policy_blocks_review_required_result() -> None:
    agent = UrbanAgentCore(
        evidence_provider=lambda _request: [
            EvidenceItem(source_id="public-doc-1", title="Public Note", text="Evidence exists.", score=0.8)
        ]
    )

    result = agent.run(QueryRequest(query="Guarantee this legal approval", metadata={"requires_review": True}))

    assert result.verification.requires_review is True
    assert MemoryWritePolicy().can_write(result.verification) is False


def test_default_eval_scenarios_are_public_safe() -> None:
    scenarios = default_scenarios()

    assert {item.expected_route for item in scenarios} >= {"qa", "spatial_qa", "gis_task", "data_ops"}
    assert all("public" not in item.scenario_id.lower() for item in scenarios)
