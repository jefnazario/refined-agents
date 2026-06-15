---
id: python_async_data
priority: 80
tags: [python, async, data]
---

# Python Async, Concurrency, and Data Handling Rules

## Async Code

- Use async only when it provides real benefit.
- Do not mix sync and async styles carelessly.
- Blocking work must not run on the event loop.
- Use thread or process offloading when blocking or CPU-heavy work is required.

## Structured Concurrency

- Fire-and-forget background tasks are discouraged.
- Created tasks must be tracked, awaited, or supervised.
- Cancellation behavior must be considered explicitly.

## Shared State

- Avoid shared mutable state across tasks or threads.
- Prefer message passing, queues, or clearly owned state.
- Synchronization primitives must be used intentionally and minimally.

## Database and I/O Boundaries

- Keep transaction boundaries explicit.
- Do not mix business logic with raw SQL or persistence details unless that is the repository’s explicit pattern.
- Batch I/O where it improves performance and clarity.
- Retries must be bounded and used only for retryable failures.

## Data Processing

- Prefer vectorized or batch operations when processing large datasets.
- Avoid row-by-row logic in pandas unless unavoidable.
- Be explicit about timezone handling for all datetime values.
- Avoid silently coercing invalid values in data pipelines.

## Time and Datetime

- All datetime handling must be timezone-aware unless the project explicitly uses naive UTC internally.
- Time assumptions must be explicit.
- Never mix local time and UTC carelessly.
- Serialization format for datetime values must be consistent across the project.

## Resource Management

- Files, connections, sessions, and streams must be closed deterministically.
- Use context managers for all resource lifecycles where possible.
