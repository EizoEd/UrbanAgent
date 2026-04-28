# Workflow

UrbanAgent follows an explicit workflow so that each decision can be tested and
reviewed independently.

```text
query
  -> route
  -> plan
  -> retrieve evidence
  -> optional spatial action
  -> synthesize
  -> verify
  -> review or writeback decision
```

## Route

`agent/router.py` classifies a request into one of the public task families:

- `qa`
- `spatial_qa`
- `gis_task`
- `comprehensive`
- `data_ops`

## Plan

`agent/planner.py` converts the route into a hierarchical plan with a top goal,
subgoals, and executable steps. This mirrors the private project design without
including private prompts or runtime settings.

## Retrieve And Tools

`tools/retrieval.py` provides an in-memory adapter for public examples. The
private project can replace it with a real evidence service. `tools/spatial/`
provides public-safe point, bounding-box, distance, and ID comparison helpers.

## Verify And Governance

`agent/verifier.py` returns `answer`, `cannot_solve`, or `needs_clarification`.
`governance/` then decides whether a result can be written to memory or needs a
human review path.
