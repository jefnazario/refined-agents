---
id: rust_hard_rules
priority: 50
tags: [always, rust]
---

# 🦀 Rust Engineering Rules — Hard Constraints

These rules are **non-negotiable** and must be followed in all Rust code.

## Memory Safety

- `unsafe` code is **forbidden unless absolutely necessary**.
- Every `unsafe` block must include:
  - a comment explaining **why it is safe**
  - clear boundaries isolating unsafe code
- `std::mem::transmute` must never be used unless there is **no safe alternative and the reasoning is documented**.
- Raw pointer manipulation must be confined to **FFI modules or low-level abstractions**.

## Panic Policy

- Production code must **never rely on panic for control flow**.
- `unwrap()` and `expect()` are **not allowed in production paths**.
- Acceptable locations for `unwrap()`:
  - tests
  - examples
  - prototypes
- Acceptable uses of `panic!`:
  - unrecoverable startup failure in `main`
  - logically impossible states using `unreachable!()` or `debug_assert!`.

## Error Handling

- Fallible operations must represent failure **explicitly** using:
  - `Result<T, E>` for recoverable errors
  - `Option<T>` for absence of a value
- Errors must **never be represented as plain strings**.
- Library crates must define **typed error enums** using `thiserror`.
- Binary crates may use `anyhow` **only at application boundaries**.

## Dependency Policy

- Wildcard dependency versions (`*`) are forbidden.
- Every new dependency must be justified in the PR:
  - compile time impact
  - maintenance status
  - binary size implications
- CI must run `cargo audit`.
- Vulnerable dependencies block merges.

## Incomplete Code

The following macros are **forbidden in production code**:

- `todo!()`
- `unimplemented!()`
- `unreachable!()` without justification

## Ownership Discipline

- Never clone data **only to silence the borrow checker**.
- Cloning is acceptable **only when it is a deliberate design tradeoff and inexpensive**.
