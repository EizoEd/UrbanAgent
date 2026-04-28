from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class EvidenceItem:
    source_id: str
    title: str
    text: str
    score: float = 0.0
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class SynthesisResult:
    summary: str
    key_findings: list[str] = field(default_factory=list)
    citations: list[dict[str, Any]] = field(default_factory=list)
    map_layers: list[dict[str, Any]] = field(default_factory=list)
    follow_up_actions: list[str] = field(default_factory=list)
