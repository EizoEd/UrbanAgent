from __future__ import annotations

from math import asin, cos, radians, sin, sqrt
from typing import Any

from urban_agent.tools.spatial.models import Feature


class SpatialActionService:
    """Public-safe spatial adapter using point features only."""

    def query_by_bbox(self, features: list[Feature], bbox: tuple[float, float, float, float]) -> dict[str, Any]:
        min_lon, min_lat, max_lon, max_lat = bbox
        selected = [item for item in features if min_lon <= item.lon <= max_lon and min_lat <= item.lat <= max_lat]
        return _feature_collection("bbox_query", selected)

    def query_by_distance(
        self,
        features: list[Feature],
        center: tuple[float, float],
        distance_km: float,
    ) -> dict[str, Any]:
        center_lon, center_lat = center
        selected = [
            item for item in features if _haversine_km(center_lon, center_lat, item.lon, item.lat) <= distance_km
        ]
        return _feature_collection("distance_query", selected)

    def compare_ids(self, previous_ids: set[str], current_ids: set[str]) -> dict[str, list[str]]:
        return {
            "added": sorted(current_ids - previous_ids),
            "removed": sorted(previous_ids - current_ids),
            "unchanged": sorted(previous_ids & current_ids),
        }


def _feature_collection(name: str, features: list[Feature]) -> dict[str, Any]:
    return {
        "name": name,
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "id": item.feature_id,
                "geometry": {"type": "Point", "coordinates": [item.lon, item.lat]},
                "properties": dict(item.properties),
            }
            for item in features
        ],
    }


def _haversine_km(lon1: float, lat1: float, lon2: float, lat2: float) -> float:
    radius_km = 6371.0088
    dlon = radians(lon2 - lon1)
    dlat = radians(lat2 - lat1)
    a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
    return 2 * radius_km * asin(sqrt(a))
