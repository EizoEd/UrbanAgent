from __future__ import annotations

from urban_agent.schemas import VerificationResult


class MemoryWritePolicy:
    """Prevents unsafe responses from being written to durable memory."""

    def can_write(self, verification: VerificationResult) -> bool:
        return (
            verification.response_type == "answer"
            and verification.passed
            and not verification.requires_review
            and verification.risk_level == "low"
        )
