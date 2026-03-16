---
id: python_tooling_ci
priority: 60
tags: [python, ci]
---

# Python Tooling and CI Rules

All Python projects must follow a consistent tooling stack.

The standard tooling for Python projects is:

- Ruff
- basedpyright
- pytest

These tools provide linting, formatting, static type checking, and testing.

---

# Linting and Formatting

Linting and formatting must be automated.

Default tool:

- **Ruff**

Ruff replaces several older tools including:

- flake8
- isort
- pylint (partially)
- black (optional formatting mode)

CI must run:
ruff check .
ruff format --check .


Code must pass linting and formatting before merge.

Developers should run Ruff locally through **pre-commit hooks**.

---

# Static Type Checking

Static type checking is mandatory.

Default tool:

- **basedpyright**

All production modules must pass static type checking.

Rules:

- public APIs must be typed
- important internal functions should also be typed
- avoid `Any` unless explicitly justified
- suppressions must include a comment explaining why.

CI must run:
basedpyright


Configuration must be committed to the repository.

---

# Testing

All production code must have automated tests.

Default testing framework:

- **pytest**

Guidelines:

- unit tests for business logic
- integration tests for system boundaries
- regression tests for fixed bugs.

Recommended pytest plugins:

- pytest-cov
- pytest-xdist
- hypothesis (when property-based testing is valuable)

CI must run:
pytest


Tests must fail the build if failures occur.

---

# Pre-commit Hooks

Repositories should use **pre-commit** to enforce checks locally.

Typical hooks include:

- Ruff linting
- Ruff formatting
- whitespace cleanup
- file consistency checks.

Example tools enforced in pre-commit:

- Ruff
- basedpyright
- pytest (optional lightweight checks)

---

# Dependency and Security Checks

CI should also include:

- dependency vulnerability scanning
- lockfile validation
- optional unused dependency detection.

---

# Continuous Integration Expectations

Every pull request must run:

1. Ruff lint + formatting checks
2. basedpyright type checking
3. pytest test suite

Pull requests must not merge if any of these checks fail.

These checks ensure:

- consistent code style
- static type safety
- reliable test coverage.
