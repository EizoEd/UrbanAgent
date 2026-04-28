from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class Feature:
    feature_id: str
    lon: float
    lat: float
    properties: dict[str, Any] = field(default_factory=dict)
