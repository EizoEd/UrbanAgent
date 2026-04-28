"""Sanitized public source snapshot for UrbanAgent.

The package contains a compact, dependency-light implementation of the core
orchestration ideas: route, plan, retrieve, synthesize, verify, and optionally
gate high-risk results for review.
"""

from urban_agent.core import UrbanAgentCore

__all__ = ["UrbanAgentCore"]
