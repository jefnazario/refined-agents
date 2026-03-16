---
id: flexible_rules
priority: 40
tags: [always]
---

# Flexible Rules

These are **strong defaults** that should be followed in most cases. They can be adjusted per context, agent, or project — but **deviations must be explicit and justified**.

---

# Testing Standards

- **Default: write tests before code (TDD).** Can be relaxed for prototyping or spike branches — never for production paths.
- Minimum coverage threshold must be defined per project (recommended: **80%+**).
- Integration tests are preferred over mocking everything.
- Tests must be **deterministic, isolated, and fast**.
- Tests that depend on external services must be explicitly marked as integration tests.

---

# Documentation Standards

- **Default: public APIs and all non-trivial functions must have docstrings/comments.**
- Documentation must explain: *why* the code exists, *how* it should be used, and *important invariants*.
- Internal helpers can skip documentation only if they are genuinely self-documenting.
- Complex algorithms must include explanatory comments inline.
- Architecture decisions should be recorded (ADR format recommended).

---

# Logging and Observability

- Prefer **structured logging** (e.g., JSON, key-value pairs) over plain text.
- Log meaningful context — not just "error occurred."
- Avoid excessive logging that creates noise.
- Never log secrets, tokens, or sensitive user data.
- Systems should expose metrics where applicable (request counts, error rates, latency).

---

# Code Style

- Follow the ecosystem's standard formatter:
  - Python → `Ruff` (formatting and linting)
  - Rust → `rustfmt`
  - Infra configs → `Prettier` or `yamlfmt`
- Custom style rules are allowed only if team-agreed and enforced by CI.
- Max function length guideline: **40 lines** — flexible for complex algorithms, but prefer breaking them apart.

---

# Dependencies — Flexible Guidance

- Prefer standard library over third-party when capability is equivalent.
- Can be relaxed when a library is the de facto standard (e.g., `serde` in Rust, `requests` or `pydantic` in Python).
- **Pin dependency versions in production.**
- Loose version pinning is acceptable in dev/tooling environments.

---

# Performance Optimization Workflow

- **Don't optimize prematurely** — profile first, then optimize.
- Required optimization workflow:
  1. Measure current performance
  2. Identify the bottleneck
  3. Optimize the specific issue
  4. Measure again to confirm improvement
- Do not optimize speculative paths.
- Rust agents have more latitude here — performance is often a primary design goal.

---

# Engineering Culture and Standards

- Code should reflect **professional, long-term engineering standards** — not just "make it work today."
- Aim for reliability, clarity, maintainability, and long-term sustainability in every decision.
- Code review is a quality gate — **reviewers are responsible for the code too**, not just the author.
- Engineers should ask: *"Would a future engineer understand and safely modify this?"*
