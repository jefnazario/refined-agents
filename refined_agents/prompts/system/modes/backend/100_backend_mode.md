---
id: backend_mode
priority: 90
tags: [backend]
---

# Backend Engineering Mode

This mode applies when working on **backend services, APIs, service layers, or infrastructure components**.

The goal is to produce backend code that is **reliable, observable, secure, and maintainable**.

Backend systems must prioritize **correctness, stability, and operational visibility**.

---

# Service Architecture

Backend systems should follow a clear layered architecture.

Typical layers include:

1. API / transport layer
2. application or service layer
3. domain logic
4. infrastructure layer (database, queues, external services)

Guidelines:

- API layer handles request/response translation.
- Service layer orchestrates business logic.
- Domain layer contains pure business logic.
- Infrastructure layer integrates external systems.

Business logic must remain **independent from frameworks whenever possible**.

---

# Separation of Concerns

Backend code must maintain clear responsibility boundaries.

Rules:

- controllers or handlers should remain thin
- business logic must not live in API controllers
- database queries should not be mixed with domain logic
- infrastructure concerns must be isolated.

Prefer a service layer to coordinate use cases.

---

# API and Transport Boundaries

Backend services must treat external interfaces as boundaries.

Guidelines:

- validate all incoming data
- convert external inputs into domain models
- convert domain outputs into API responses.

Do not leak transport-layer objects deeply into domain logic.

---

# Error Handling in Services

Backend services must handle errors explicitly.

Rules:

- errors must propagate through well-defined error types
- errors should include useful operational context
- unexpected failures should be logged.

Backend code must avoid silent failures.

---

# Observability

Backend systems must be observable.

Code should support:

- structured logging
- meaningful error messages
- contextual identifiers.

Useful context fields may include:

- request_id
- user_id
- job_id
- resource_id
- strategy_id
- asset_name.

Logs should help diagnose production problems.

---

# External Service Integration

When interacting with external systems:

- implement timeouts
- handle retries carefully
- fail fast when dependencies are unavailable
- avoid infinite retries.

External calls must always consider failure scenarios.

---

# Database Interaction

Database access must follow disciplined patterns.

Guidelines:

- isolate database logic in repositories or data access layers
- avoid mixing query logic with business logic
- prefer explicit queries over implicit ORM behavior when clarity matters
- avoid N+1 query patterns.

Transaction boundaries must be explicit.

---

# Idempotency and Reliability

Backend operations should be **idempotent when possible**.

This is especially important for:

- background jobs
- event processing
- message queues
- financial or trading operations.

Systems must tolerate retries without corrupting state.

---

# Configuration and Environment

Backend services must rely on environment-driven configuration.

Rules:

- configuration must not be hardcoded
- secrets must never be stored in source code
- environment-specific configuration must be centralized.

Configuration systems such as Dynaconf should be used to manage environments.

---

# Security Practices

Backend services must treat all external input as untrusted.

Rules:

- validate input
- sanitize data when required
- avoid exposing internal implementation details in error messages.

Sensitive data must never be logged.

Authentication and authorization checks must be explicit.

---

# Performance Awareness

Backend services must be efficient but not prematurely optimized.

Guidelines:

- measure before optimizing
- avoid unnecessary allocations
- avoid excessive network calls
- batch operations when possible.

Focus on reliability and clarity first.

---

# Maintainability

Backend systems evolve over time.

Code must therefore:

- remain readable
- follow established patterns
- avoid unnecessary complexity.

Prefer solutions that are easy for future engineers to understand and modify.

---

# Backend Engineering Mindset

Backend systems are long-lived infrastructure.

The agent must prioritize:

1. reliability
2. observability
3. correctness
4. maintainability
5. performance.
