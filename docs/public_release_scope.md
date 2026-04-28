# Public Release Scope

The public repository includes a cleaned source snapshot and project-level
documentation. It intentionally excludes materials that can reveal private
implementation details or operational context.

## Included

- Public-safe orchestration code.
- Minimal retrieval and spatial adapters.
- Review and memory-write policy examples.
- Small smoke-test scenarios and examples.
- High-level architecture and workflow documentation.

## Excluded

- Raw project documents and extracted text.
- Runtime logs, audit files, caches, and generated evaluation records.
- Local machine paths, private branch names, and internal commit references.
- Credentials, service endpoints, model configuration, and environment files.
- Private datasets, memory artifacts, and non-public prompts.

## Sanitization Rule

Only stable architecture, module responsibilities, public-safe examples, and
small synthetic test data are included. Anything tied to a private environment
or real operational record is removed or replaced with a neutral placeholder.
