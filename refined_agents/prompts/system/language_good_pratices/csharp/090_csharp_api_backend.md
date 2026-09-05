---
id: csharp_api_backend
priority: 90
tags: [csharp, backend, api]
---

# C# & .NET API & Backend Rules

These rules define standard practices for designing and implementing RESTful APIs, domain services, and persistence layers in C#/.NET.

---

# RESTful API Design & Conventions

- **Semantic Routing & Versioning**:
  - Version all APIs explicitly in the route (e.g., `/api/v1/appointments`, `/api/v2/appointments`) to maintain backwards compatibility.
  - Use plural nouns for resources (e.g., `/orders`, `/customers`).
  - Controller and action names must be semantically meaningful.
- **Strict HTTP Verb Semantics**:
  - `GET`: Read resource without side effects.
  - `POST`: Create a new resource.
  - `PUT`: Replace or update an existing resource idempotently.
  - `PATCH`: Apply partial updates.
  - `DELETE`: Remove a resource.
- **Semantic Status Codes**:
  - `200 OK`: Successful retrieval or update.
  - `201 Created`: Successful resource creation (include `Location` header via `CreatedAtAction` or `CreatedAtRoute`).
  - `204 No Content`: Successful execution with no response payload.
  - `400 Bad Request`: Malformed syntax or invalid request format.
  - `401 Unauthorized`: Missing or invalid authentication token.
  - `403 Forbidden`: Authenticated caller lacks permissions for the resource.
  - `404 Not Found`: Target resource does not exist.
  - `422 Unprocessable Entity`: Syntactically valid request that violates domain rules.
  - `500 Internal Server Error`: Unexpected internal system failure.
- **RFC 7807 Problem Details**:
  - Standardize error responses using ASP.NET Core `ProblemDetails` for consistency.

---

# Separation of Responsibilities

Strictly enforce clean boundaries between layers:

- **Controller**:
  - Handles transport, extracts route/query/body parameters, validates request schemas.
  - Contains **zero business logic**.
  - Calls the module's service interface (`I{Module}Service`) and maps the result to an HTTP response status code.
- **Service Layer**:
  - Implements application use cases and business orchestration.
  - Interacts with repositories, domain entities, and external gateways.
  - Never leaks domain entities to the controller; maps domain state to DTOs.
- **Domain Layer**:
  - Houses entities, value objects, domain logic, and domain events.
  - Completely framework-agnostic.
- **Repository / Data Access**:
  - Encapsulates database queries, LINQ expressions, and persistence mappings.

---

# Authentication & Authorization

- **JWT Authentication**: Default for stateless RESTful APIs. Validate issuer, audience, lifetime, and signing keys.
- **OAuth / SSO**: Integrate social and enterprise identity providers (Google, Microsoft, Apple, GitHub) when required.
- **Policy-Based Authorization**:
  - Use `[Authorize]` and policy attributes (`[Authorize(Policy = "...")]`) to enforce granular access controls.
  - Never rely solely on client-provided claims for authorization decisions without backend validation.

---

# Data Persistence with Entity Framework Core & SQL

- **LINQ & Projections**:
  - Write expressive LINQ queries.
  - Use `.Select()` projections to load only required fields instead of fetching entire entities for read operations.
- **Performance & Tracking**:
  - Always apply `.AsNoTracking()` for read-only queries to prevent change-tracker overhead.
  - Avoid N+1 queries by proactively using `.Include()` or explicit projections.
- **Transaction Boundaries**:
  - Coordinate multi-entity writes under explicit Unit of Work or database transactions.
- **Domain Events & CQRS**:
  - Propagate entity side effects using Domain Events.
  - Separate read and write paths using CQRS and MediatR when complexity justifies it.

---

# Observability & Structured Logging

- Use `ILogger<T>` for structured logging across controllers, services, and handlers.
- Include operational identifiers (e.g., `CorrelationId`, `UserId`, `OrderId`) in log scopes.
- Never log passwords, tokens, API keys, or personal identifiable information (PII).
