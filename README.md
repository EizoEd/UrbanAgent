# UrbanAgent

UrbanAgent is a privacy-clean public overview of a city-scale remote-sensing task agent. It is designed as an orchestration layer for urban analysis workflows: routing a request, planning the work, retrieving supporting evidence, calling spatial and external tools, synthesizing results, verifying risk, and routing high-risk outputs through review.

This public repository publishes a sanitized project introduction and a compact public source snapshot. Raw documents, generated datasets, logs, memory artifacts, local runtime files, credentials, and environment-specific configuration are intentionally excluded.

## What It Does

- Supports evidence-grounded urban and remote-sensing question answering.
- Routes tasks across short answer flows, spatial analysis flows, **GIS-oriented tasks**, and broader multi-step analysis.
- Uses a **graph-based workflow** to keep routing, retrieval, tool execution, verification, review, and writeback explicit.
- Connects retrieval, spatial actions, local tools, MCP-style tools, and skill-style extensions behind consistent tool contracts.
- Produces structured outputs such as summaries, key findings, citations, object references, map payloads, follow-up actions, and review state.
- Handles cannot-solve and needs-clarification cases as first-class response types instead of forcing low-confidence answers.
- Provides governance features for human review, permission checks, audit events, memory write policies, and strict runtime checks.
- Includes an evaluation and metrics layer for regression checks, workflow comparison, latency tracking, and experiment reports.

## Architecture

UrbanAgent is organized around five main layers:

- **Interface layer**: API endpoints and a lightweight workbench for query, task, review, upload, metrics, and spatial interactions.
- **Orchestration layer**: a LangGraph-style state graph that controls node order, conditional branches, retry handling, asynchronous tasks, and streamable task events.
- **Decision layer**: intent routing, workflow selection, hierarchical planning, evidence synthesis, solvability checks, and guardrail verification.
- **Tool layer**: retrieval adapters, spatial action adapters, local tool governance, MCP-style execution, skill routing, and tool-worker result summarization.
- **Governance layer**: session state, context management, review access control, audit trails, memory write decisions, observability, and evaluation.

The core workflow can be summarized as:

```text
memory -> rewrite -> context management -> route and plan -> retrieve
  -> optional spatial / local / MCP / skill tools
  -> synthesize -> verify -> optional human review -> writeback
```

## Key Components

- **Router and workflow selector**: classify task intent and choose short or agentic execution.
- **Hierarchical planner**: decomposes requests into goals, subgoals, and executable steps while keeping compatibility with flat step plans.
- **RAG adapter**: treats retrieval, evidence lookup, validation, and memory access as tool capabilities rather than rebuilding a retrieval system inside the agent.
- **Spatial action service**: supports region filtering, distance-based search, temporal layer comparison, and map-ready payload generation through pluggable GIS backends.
- **Tool execution layer**: isolates external tool calls, normalizes errors, summarizes large outputs, and prevents tool results from polluting the main reasoning context.
- **Verifier**: checks citation grounding, spatial risk, solvability, missing inputs, and whether a result should be answered, clarified, blocked, or reviewed.
- **Human review loop**: supports pending review, approval, rejection, edits, permission checks, and auditable decisions.
- **Context governance**: manages compact task context, rollover behavior for long sessions, and clean memory write policies.
- **Evaluation layer**: supports scenario datasets, experiment matrices, workflow metrics, and open-source style benchmark construction.

## Typical Use Cases

- Urban planning and policy Q&A with evidence references.
- Spatial filtering by administrative region, distance, layer, or time range.
- Change comparison between urban or remote-sensing layers.
- Multi-document analysis where uploaded materials are parsed, indexed, and used as query context.
- High-risk answer review before memory writeback or user-facing completion.
- Regression evaluation across prompt, memory, routing, and tool-use strategies.

## Technology Stack

- Python 3.9+ for the public source snapshot
- FastAPI for service interfaces
- Pydantic for request and response contracts
- LangChain-compatible tools for retrieval and tool abstraction
- LangGraph-style workflow orchestration
- HTTP adapters for external services
- Pytest-based unit, integration, and end-to-end validation

## Source Snapshot

The `urban_agent/` package is a sanitized, dependency-light subset of the private prototype. It keeps the core ideas visible without exposing private service wiring:

- `router.py`: deterministic route selection for QA, spatial, GIS, data-operation, and comprehensive tasks.
- `planner.py`: hierarchical plan generation with goals, subgoals, and executable steps.
- `synthesis.py`: evidence and tool-output normalization into a stable response shape.
- `verifier.py`: grounding, missing-input, review, cannot-solve, and clarification checks.
- `spatial.py`: public-safe point and bounding-box spatial helpers.
- `workflow.py`: a compact route-plan-retrieve-synthesize-verify orchestration loop.

Run the public snapshot tests with:

```bash
python -m pytest -q
```

## Public Release Scope

The following items were deliberately removed from the public material:

- Personal or local machine paths
- Private repository names, branch names, and commit identifiers
- Raw source documents and extracted document text
- Generated evaluation datasets and sampled records
- Logs, audit files, memory files, cache files, and runtime artifacts
- API credentials, model credentials, service URLs, and environment-specific settings
- Internal reports that include operational details not needed for public understanding

The included source keeps only public-safe orchestration logic and minimal tests.

## Current Status

UrbanAgent has reached a runnable engineering prototype stage in the private workspace. The public repository now includes a sanitized source snapshot; full implementation packages, examples, and datasets remain excluded until each part is reviewed separately for open-source release.
