---
id: rust_defaults
priority: 60
tags: [rust]
---

# 🦀 Rust Engineering Rules — Default Practices

These are **strong defaults** but may be adjusted when justified.

## Ownership and Borrowing

- Prefer borrowing (`&T`, `&mut T`) over ownership transfer.
- Avoid `Rc<RefCell<T>>` and `Arc<Mutex<T>>` unless necessary.
- Prefer simpler alternatives when possible:
  - immutable data structures
  - cloning `Arc<T>` instead of locking
  - message passing via channels.

## API Design

- Public APIs should be **minimal and intentional**.
- Default visibility should be `pub(crate)`.
- Avoid glob re-exports (`pub use module::*`).

## Lifetimes

- Let the compiler infer lifetimes whenever possible.
- Explicit lifetimes should only appear when:
  - necessary for correctness
  - improving API readability.

Avoid complex lifetime relationships in public APIs.

Prefer owned types if they simplify usage.

## Traits and Generics

- Prefer generics for zero-cost abstraction.
- Use trait objects (`dyn Trait`) when runtime polymorphism is required.
- Prefer `impl Trait` in function signatures when the concrete type is irrelevant.

## Performance

Default priorities:

1. Correctness
2. Clarity
3. Performance

Optimization must be **evidence-based**.

Use:

- `criterion` for benchmarking
- `cargo flamegraph` for profiling

Speculative optimization is discouraged.

## Project Structure

Typical crate layout:
src/
├── lib.rs
├── error.rs
├── config.rs
└── domain/

Guidelines:

- One module per file.
- Modules mirror directory structure.
- `lib.rs` exposes the public API.

Integration tests belong in `/tests`.
