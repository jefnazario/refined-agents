
---

# 📄 050_python_defaults.md (UPDATED)

```markdown
---
id: python_defaults
priority: 50
tags: [python]
---

# Python Engineering Rules — Default Practices

These are **strong defaults** but may be adjusted when justified.

---

# Style and Readability

Prefer clarity over cleverness.

Code must be easy to understand by another engineer reading it later.

Guidelines:

- prefer explicit logic
- avoid dense one-liners
- avoid deeply nested control flow
- choose descriptive variable and function names.

Modules should remain cohesive and focused on one responsibility.

---

# Function Design

Functions should do **one thing well**.

Guidelines:

- keep functions small and composable
- avoid long parameter lists
- prefer keyword arguments when several optional parameters exist
- return values must be predictable and well documented.

---

# Typing

Type hints are required for:

- public functions
- class methods
- important module-level variables.

Use modern typing syntax compatible with the project Python version.

Avoid misleading types such as `Any` unless there is a clear justification.

Prefer structured types when appropriate:

- `dataclass`
- `TypedDict`
- `Protocol`
- Pydantic models.

---

# Data Modeling

Preferred order for structured data:

1. `dataclass` for internal domain models
2. Pydantic models for validated external data
3. `TypedDict` for lightweight structured dictionaries
4. plain dictionaries for simple unstructured cases.

---

# Object-Oriented Design

Use classes only when they model real state or behavior.

Prefer:

- composition over inheritance
- small focused classes.

Inheritance must represent a real **is-a relationship**.

Avoid deep inheritance hierarchies.

---

# Imports and Module Structure

Imports must be explicit and predictable.

Guidelines:

- avoid circular imports
- keep modules lightweight
- avoid heavy initialization during import time.

A module should generally contain **one primary responsibility**.

---

# Configuration Management

Configuration must follow **12-factor application principles**.

Configuration must never be hardcoded inside application logic.

Configuration sources may include:

- environment variables
- configuration files
- secret managers.

Configuration loading must be centralized.

Preferred configuration approach:

Use **Dynaconf** for configuration management.

Dynaconf allows:

- environment-specific settings
- secret management
- layered configuration
- environment variable overrides.

Typical configuration structure:
config/
├── settings.toml
├── .secrets.toml
└── settings.py


Application code should access configuration through a centralized settings module.

---

# Logging Best Practices

Logging configuration must be centralized and environment-driven.

Typical structure:
logging/
└── logger.py


Logging should support:

- environment-based log levels
- consistent formatting
- structured fields
- integration with monitoring systems.

Prefer structured logging for operational observability.

Example contextual fields:

- request_id
- job_id
- user_id
- asset_name
- strategy_id.

---

# Performance

Default priorities:

1. correctness
2. clarity
3. simplicity
4. performance.

Optimization must follow measurement.

Use profiling tools when performance issues arise.

---

# Pythonic Practices

Prefer idiomatic Python constructs when they improve readability.

Examples:

- context managers for resource handling
- comprehensions when they improve clarity
- generators for streaming data
- `pathlib` for file paths.

---

# Project Structure

Typical backend or service layout:

src/
app/
api/
services/
domain/
repositories/
models/
config/
utils/
tests/


Guidelines:

- business logic must not depend directly on frameworks
- persistence logic must be isolated
- service layer coordinates use cases
- API layer handles transport concerns.

---

# Testing Philosophy

All production code must be testable.

Minimum expectations:

- unit tests for business logic
- integration tests for system behavior.

Tests should be:

- deterministic
- isolated
- fast
- easy to understand.
