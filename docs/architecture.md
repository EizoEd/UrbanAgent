# Architecture

This public snapshot keeps the structure of the private prototype while removing
runtime-specific wiring and private data.

## Package Layout

```text
urban_agent/
  core.py
  schemas/
  agent/
  tools/
    spatial/
  governance/
  evaluation/
```

## Layers

- `schemas/`: request, route, planning, evidence, synthesis, verification, and workflow contracts.
- `agent/`: routing, planning, synthesis, and verification decisions.
- `tools/`: public-safe retrieval and spatial adapters.
- `governance/`: review and memory-write policies.
- `evaluation/`: small scenario definitions for smoke tests and demos.
- `core.py`: the route-plan-retrieve-spatial-synthesize-verify orchestration loop.

## Private Implementation Boundary

The private prototype can connect these modules to model providers, RAG services,
GIS stores, MCP servers, skills, and audit persistence. This public snapshot
keeps those boundaries visible but does not include the private adapters.
