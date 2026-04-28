from urban_agent import UrbanAgentCore
from urban_agent.schemas import EvidenceItem, QueryRequest
from urban_agent.tools import InMemoryRetrievalAdapter


adapter = InMemoryRetrievalAdapter(
    [
        EvidenceItem(
            source_id="public-doc-1",
            title="Public Urban Monitoring Note",
            text="Urban growth monitoring should combine evidence retrieval, spatial checks, and review.",
            score=0.8,
        )
    ]
)

agent = UrbanAgentCore(evidence_provider=adapter.search)
result = agent.run(QueryRequest(query="What evidence supports urban growth monitoring?"))

print(result.synthesis.summary)
print(result.verification.response_type)
