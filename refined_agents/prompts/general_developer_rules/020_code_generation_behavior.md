---
id: code_generation_behavior
priority: 20
tags: [always]
---

# Code Generation Behavior

These rules define **how the agent must behave when generating or modifying code**.

They apply to all languages and repositories.

The goal is to produce **correct, maintainable, production-ready code**.

---

# Generate Complete Solutions

The agent must generate **complete working code** whenever possible.

Avoid returning:

- partial snippets
- incomplete implementations
- pseudo-code
- placeholder logic.

If the request requires multiple files or modules, the response should clearly show the structure.

Example:
src/
services/order_service.py
models/order.py
api/order_routes.py


All required imports must be included.

---

# Respect Existing Project Structure

The agent must **adapt to the project's existing architecture**.

Do not introduce a completely different structure unless explicitly requested.

Before generating code, the agent must consider:

- current project layout
- naming conventions
- framework usage
- existing abstractions.

Prefer extending existing components instead of creating parallel systems.

---

# Prefer Existing Libraries and Patterns

When writing new code:

- reuse existing utilities
- follow the repository’s patterns
- avoid introducing unnecessary dependencies.

If a dependency is suggested, the agent must ensure it is:

- widely adopted
- actively maintained
- appropriate for the use case.

Avoid niche or experimental libraries unless explicitly requested.

---

# Avoid Hallucinated APIs

The agent must **not invent functions, modules, or APIs** that do not exist.

If unsure about an API:

- prefer standard library solutions
- explicitly state assumptions
- avoid fabricating interfaces.

Generated code must compile or run using known APIs.

---

# Code Must Be Production Ready

Generated code must follow professional engineering standards.

Code must include:

- proper error handling
- clear function signatures
- appropriate logging
- correct imports
- type hints where applicable.

Avoid quick prototypes unless explicitly requested.

---

# Follow Language-Specific Rules

Language-specific rules override general preferences.

For example:

- Rust safety rules must be followed.
- Python typing and linting rules must be respected.

Generated code must comply with the language-specific policies defined elsewhere.

---

# Do Not Break Existing Behavior

When modifying code:

- preserve existing functionality
- avoid changing unrelated logic
- maintain backward compatibility unless the task requires breaking changes.

Changes must be **minimal and focused**.

---

# Tests Must Be Included When Appropriate

When generating new logic:

- include unit tests when possible
- update existing tests if behavior changes.

Tests should validate behavior, not just increase coverage.

Example:

tests/test_order_service.py


---

# Explain Non-Obvious Design Decisions

When the implementation includes non-obvious choices:

- briefly explain the reasoning
- mention tradeoffs if relevant.

Avoid long explanations unless requested.

---

# Avoid Overengineering

Prefer simple solutions first.

Avoid:

- unnecessary abstraction layers
- premature optimization
- complex patterns without clear benefit.

Complexity must be justified.

---

# Prefer Deterministic Code

Generated code should avoid:

- hidden side effects
- unpredictable state changes
- reliance on global mutable state.

Behavior should be clear and deterministic.

---

# Respect Tooling Rules

Generated code must pass repository tooling.

Examples:

Python code must pass:

- Ruff
- basedpyright
- pytest

Rust code must pass:

- rustfmt
- clippy
- cargo test

The agent should write code that would reasonably pass these checks.

---

# Security Awareness

The agent must avoid introducing security risks.

Never generate code that:

- exposes secrets
- trusts unvalidated input
- disables security checks.

Security-sensitive code must be explicit and defensive.

---

# Prefer Maintainable Code

The agent must prefer code that is easy to maintain.

Priorities:

1. clarity
2. correctness
3. maintainability
4. performance.

Short clever code is worse than clear code.

---

# When Requirements Are Ambiguous

If a request is ambiguous:

- choose the safest reasonable implementation
- document assumptions briefly
- avoid risky design decisions.


