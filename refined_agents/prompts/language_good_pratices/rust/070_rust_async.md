
---

# 📄 070_rust_async.md

```markdown
---
id: rust_async
priority: 70
tags: [rust, async]
---

# 🦀 Rust Async & Concurrency Rules

## Async Runtime

Default runtime is **Tokio**.

Exceptions:

- Embedded systems may use `embassy`
- specialized environments may use alternative runtimes.

## Blocking Operations

Blocking operations must not run inside async contexts.

Use:
tokio::task::spawn_blocking


for CPU-bound or blocking tasks.

## Structured Concurrency

Fire-and-forget tasks are discouraged.

Spawned tasks must:

- be awaited
- have cancellation handling
- be managed via task handles.

## Shared State

Minimize shared mutable state.

Preferred patterns:

1. message passing (channels)
2. actor models
3. immutable shared state.

If locks are required:

- `RwLock` for read-heavy workloads
- `Mutex` for simple exclusive access.

If a poisoned mutex is acceptable to ignore:

```rust
let data = mutex.lock().unwrap_or_else(|e| e.into_inner());

This must include a comment explaining why it is safe.
Async Traits
Prefer native async traits when available for the project’s MSRV.
Otherwise use the async_trait crate and document the choice.
