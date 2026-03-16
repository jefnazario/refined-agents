---
id: rust_tooling_ci
priority: 60
tags: [rust, ci]
---

# 🦀 Rust Tooling & CI Rules

These rules define the required development tooling.

## Formatting

Rust formatting must be enforced with `rustfmt`.

CI blocks merges if formatting fails.

Developers must run:
cargo fmt

before committing.

## Linting

Static analysis is enforced using **Clippy**.

CI runs:
cargo clippy -- -D warnings


All warnings must be resolved unless explicitly justified.

Suppressions using `#[allow(...)]` must include a comment explaining why.

## Testing

Testing standards:

- Unit tests live beside the code under test.
- Integration tests belong in `/tests`.

Preferred tools:

- `cargo nextest` for running tests
- `proptest` or `quickcheck` for property testing.

## Documentation

Public APIs must include rustdoc comments.

Documentation should include:

- purpose
- usage
- examples when appropriate.

Example:

```rust
/// Parses the configuration file.
///
/// Returns an error if the file is invalid.

MSRV Policy
Projects must define a Minimum Supported Rust Version (MSRV).
Dependencies must respect the defined MSRV.
Nightly features are not allowed unless explicitly documented.
