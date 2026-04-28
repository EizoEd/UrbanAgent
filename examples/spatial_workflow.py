from urban_agent import UrbanAgentCore
from urban_agent.schemas import EvidenceItem, QueryRequest


agent = UrbanAgentCore(
    evidence_provider=lambda _request: [
        EvidenceItem(
            source_id="public-spatial-note",
            title="Public Spatial Note",
            text="Spatial filtering should return structured map payloads for downstream review.",
            score=0.9,
        )
    ]
)

request = QueryRequest(
    query="Find features within this region",
    metadata={
        "bbox": [0.0, 0.0, 1.0, 1.0],
        "features": [
            {"id": "feature-a", "lon": 0.5, "lat": 0.5, "properties": {"kind": "sample"}},
            {"id": "feature-b", "lon": 4.0, "lat": 4.0, "properties": {"kind": "sample"}},
        ],
    },
)

result = agent.run(request)
print(result.synthesis.map_layers)
print(result.trace)
