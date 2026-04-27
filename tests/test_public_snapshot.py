from urban_agent import UrbanAgentCore
from urban_agent.schemas import EvidenceItem, QueryRequest
from urban_agent.spatial import Feature, SpatialActionService


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
