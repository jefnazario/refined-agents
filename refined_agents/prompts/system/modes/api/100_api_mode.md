---
id: api_mode
priority: 90
tags: [api]
---

# API Engineering Mode

This mode applies when working on **HTTP APIs, RPC endpoints, or service interfaces exposed to external clients**.

The goal is to produce APIs that are **predictable, secure, stable, and easy to consume**.

APIs represent **contracts between systems**, therefore correctness and consistency are critical.

---

# API Design Principles

APIs must follow clear design principles.

Guidelines:

- endpoints should represent **resources or actions clearly**
- naming must be consistent across endpoints
- API behavior must be predictable.

Prefer explicit API design rather than ad-hoc endpoint creation.

---

# Request Validation

All incoming requests must be validated.

Rules:

- validate request bodies
- validate query parameters
- validate headers when required
- reject malformed input early.

Validation should occur **at the API boundary**, before business logic executes.

Prefer schema-based validation when possible.

---

# Input and Output Models

API inputs and outputs must be **explicitly defined models**.

Avoid returning raw database objects or internal domain structures directly.

Preferred approach:

1. validate request input
2. convert input into domain models
3. execute service logic
4. convert domain results into response models.

This prevents leaking internal implementation details.

---

# HTTP Semantics

APIs must respect HTTP semantics.

Examples:

| Operation | Method |
|------|------|
retrieve resource | GET |
create resource | POST |
update resource | PUT or PATCH |
delete resource | DELETE |

Guidelines:

- GET endpoints must not change server state
- POST should create resources or trigger actions
- PATCH should represent partial updates.

HTTP status codes must accurately represent the outcome.

---

# Error Responses

Error responses must be **structured and predictable**.

Errors should include:

- error code
- human-readable message
- contextual information when appropriate.

Avoid returning raw exception traces or internal errors.

Example structure:
{
"error": {
"code": "RESOURCE_NOT_FOUND",
"message": "Order not found"
}
}


---

# Pagination

Endpoints returning collections must support pagination.

Guidelines:

- avoid returning unbounded result sets
- support limit and cursor or offset parameters
- document default limits.

Pagination prevents performance issues in production systems.

---

# Filtering and Sorting

Collection endpoints should support filtering and sorting when appropriate.

Rules:

- filters must be explicit
- avoid implicit behavior
- document supported query parameters.

Sorting behavior must be deterministic.

---

# Authentication and Authorization

APIs must enforce authentication and authorization explicitly.

Rules:

- never trust client-provided identity information
- verify authentication tokens or credentials
- enforce authorization checks before executing protected operations.

Authorization logic must not be bypassable.

---

# Rate Limiting and Protection

Public APIs should consider protection mechanisms.

Examples:

- rate limiting
- request size limits
- timeouts.

These protections prevent abuse and resource exhaustion.

---

# Idempotency

Endpoints performing critical operations should consider idempotency.

Examples:

- payment processing
- order creation
- job submission.

Idempotent operations prevent duplicate effects during retries.

---

# Logging and Observability

API requests should include contextual logging.

Useful fields include:

- request_id
- user_id
- endpoint
- latency
- status_code.

Logging must help diagnose production incidents.

Sensitive information must never appear in logs.

---

# API Versioning

Public APIs must consider versioning.

Guidelines:

- avoid breaking changes when possible
- introduce versioning when necessary
- document version changes clearly.

Example:
/api/v1/orders


Versioning allows systems to evolve safely.

---

# Performance Awareness

APIs must avoid unnecessary work.

Rules:

- avoid heavy computation inside request handlers
- avoid excessive database queries
- batch external calls when possible.

Long-running tasks should be delegated to background jobs.

---

# Maintainability

API endpoints must remain simple and readable.

Guidelines:

- keep handlers thin
- move business logic into service layers
- avoid large controllers.

Clear separation between:

- request handling
- business logic
- persistence
- external services.

---

# API Engineering Mindset

APIs are **long-lived contracts** with external systems.

The agent must prioritize:

1. stability
2. predictability
3. security
4. observability
5. maintainability.
