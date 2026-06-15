---
id: python_api_backend
priority: 90
tags: [python, backend, api]
---

# Python API and Backend Rules

These are defaults for backend services, APIs, and application code.

## Framework Boundaries

- Framework code must stay at the edges of the system.
- Domain and business logic must remain framework-independent where practical.
- Request and response objects should not leak deeply into domain code.

## API Design

- APIs must be explicit and stable.
- Input schemas and output schemas must be validated.
- Error responses must be structured and predictable.
- Pagination, filtering, and sorting behavior must be explicit.

## Validation

Preferred pattern:

- validate at the boundary
- transform into domain types
- process in the service/domain layer
- serialize at the boundary again.

## Persistence

- Repositories or data access layers should isolate persistence details.
- ORM models should not automatically become domain models.
- Query logic should remain readable and testable.
- N+1 query patterns should be avoided.

## Logging and Observability

- Use structured logging.
- Include request identifiers, trace identifiers, and useful operational context when available.
- Never log secrets, tokens, passwords, or sensitive payloads.
- Important failures must be observable through logs and metrics.

## Background Jobs

- Background jobs must be idempotent when possible.
- Retries must be bounded and safe.
- Job inputs and outputs should be validated.
- Long-running jobs should emit useful progress or state information when operationally relevant.

## Security

- Authentication and authorization must be explicit.
- Never trust client-provided authorization state.
- Rate limits, input size limits, and timeouts should be considered for exposed endpoints.
- File uploads must be validated carefully.

## Migrations and Schema Changes

- Schema changes must be versioned.
- Destructive migrations require explicit review.
- Backward compatibility should be considered for rolling deployments.

## Caching

- Cached data must have a clear invalidation strategy.
- Do not introduce caching until there is a demonstrated need.
- Cache semantics must be explicit: TTL, ownership, and staleness expectations.
