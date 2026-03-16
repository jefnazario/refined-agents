---
id: project_context
priority: 0
tags: [always]
---

# Project Context

This document provides **high-level knowledge about the repository** so the agent can generate code that integrates correctly with the project.

This file is **project-specific** and should be updated when the system architecture evolves.

---

# Project Overview

Describe the purpose of the system.

Example:

This repository contains services and infrastructure used to power the trading platform.

The system includes:

- data ingestion pipelines
- market data processing
- trading strategies
- API services
- analytics tools.

---

# Architecture Principles

The system follows a layered architecture.

Typical layers include:

1. API layer
2. application/service layer
3. domain logic
4. infrastructure layer.

Business logic must remain independent of infrastructure concerns.

Framework code should remain at the boundaries of the system.

---

# Primary Languages

This project uses multiple languages:

Python is used for:

- services
- data pipelines
- backend APIs
- machine learning and analytics.

Rust is used for:

- performance-critical modules
- low-latency systems
- memory-safe infrastructure components.

Language-specific rules must be respected.

---

# Python Stack

Python services follow these standards:

Core tooling:

- Ruff for linting and formatting
- basedpyright for static typing
- pytest for testing.

Configuration management:

- Dynaconf
- environment-driven configuration following the 12-factor methodology.

Logging:

- centralized logging using Python's `logging` module
- structured logging encouraged.

Typical service structure:

src/
app/
api/
services/
domain/
repositories/
models/
config/
logging/
tests/


---

# Rust Stack

Rust components follow these standards:

Core tooling:

- rustfmt
- clippy
- cargo test.

Typical crates follow a structure such as:


Rust code must respect strict safety and ownership rules defined in Rust-specific rule files.

---

# Configuration Management

Configuration must follow **12-factor principles**.

All configuration is environment-driven.

Preferred configuration tool:

- Dynaconf.

Typical configuration files:
config/
settings.toml
.secrets.toml


Secrets must never be committed to version control.

---

# Logging and Observability

Logging must be centralized and structured.

Logs should include contextual fields when available:

- request_id
- job_id
- asset_name
- strategy_id.

Sensitive information must never appear in logs.

---

# Testing Strategy

The project uses automated testing.

Testing tools include:

- pytest for Python
- cargo test for Rust.

Testing types:

- unit tests for core logic
- integration tests for system behavior
- regression tests for previously fixed bugs.

Tests should be deterministic and fast.

---

# Dependency Philosophy

Dependencies must be carefully chosen.

Before adding a dependency evaluate:

- maintenance status
- ecosystem adoption
- security history
- build size impact.

Avoid introducing unnecessary libraries.

---

# Repository Conventions

The repository prioritizes:

- clear module boundaries
- explicit naming
- minimal public APIs
- deterministic behavior.

Avoid introducing new architectural patterns unless necessary.

Prefer extending existing abstractions.

---

# Development Workflow

All changes must pass CI checks before merge.

Typical CI checks include:

- linting
- type checking
- test execution.

Pull requests must be reviewed before merging.

---

# Agent Responsibilities

When generating code inside this repository, the agent must:

- respect the existing architecture
- follow the defined language rules
- use approved tooling
- avoid introducing conflicting patterns.

New code must integrate naturally with the existing system.
