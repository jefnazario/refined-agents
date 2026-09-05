---
id: csharp_hard_rules
priority: 50
tags: [always, csharp]
---

# C# & .NET Engineering Rules — Hard Constraints

These rules are **non-negotiable** and apply to all C#/.NET production code.

---

# Rich Domain Model & Encapsulation

Entities are not passive data bags. They must encapsulate behavior, guard invariants, and express business rules directly in code.

The following domain rules are **mandatory and inviolable**:

- **No public property setters**: Entity properties must never have public setters. Use `private set` or `init`.
- **Intention-revealing state changes**: State transitions must only occur through explicit methods that carry business meaning (e.g., `appointment.Cancel(reason)`, never `appointment.Status = ...`).
- **Objects are born valid or do not exist**: All creation validation lives in the constructor. If arguments are invalid, the entity cannot be instantiated.
- **Single owner for business logic**: Business logic lives inside the entity that originates it, never scattered across Controllers or Services. Services orchestrate; entities decide.
- **No infrastructure dependencies in domain**: Domain entities and value objects must never depend on infrastructure concerns (databases, Entity Framework contexts, HTTP clients, file systems, or loggers).
- **Isolated domain testability**: Domain objects must be testable in complete isolation — without mocks, without databases, and without framework containers.
- **State in enums, not loose booleans**: Represent entity states with explicit enums, never loose boolean flags (e.g., use `AppointmentStatus.Cancelled` instead of `IsCancelled` and `IsCompleted`).
- **Value Objects for identity-less concepts**: Concepts with their own validation rules and no identity must be modeled as Value Objects (e.g., `Email`, `Money`, `Cpf`), never raw primitive types.

---

# Error Handling & Failures

- Never use exceptions for standard control flow.
- Never swallow exceptions with empty or broad `catch` blocks:
  ```csharp
  // FORBIDDEN
  catch (Exception)
  {
  }
  ```
- Any caught exception must be logged with rich contextual information or intentionally translated.
- **DomainException vs. Result Pattern**:
  - `DomainException` is thrown only by entities/value objects when an unrecoverable domain invariant is violated.
  - Controllers/middleware translate `DomainException` into appropriate client errors (e.g., HTTP 400 or 422).
  - For expected and recoverable business failures, always prefer the **Result Pattern** (`Result<T>` / `Result`) over throwing exceptions.

---

# Asynchronous & Concurrency Invariants

- **Never use `async void`** except for top-level event handlers. Always return `Task` or `Task<T>`.
- **Never block on asynchronous code**: Never call `.Result`, `.Wait()`, or `.GetAwaiter().GetResult()` on tasks in synchronous paths. This introduces thread-pool starvation and deadlocks.
- Keep the call chain asynchronous all the way down: `async` and `await` from the controller/handler down to I/O boundaries.
- Always propagate `CancellationToken` through all asynchronous APIs.

---

# Security & Data Integrity

- Never use string interpolation or concatenation to build raw SQL commands. Always use parameterized queries or LINQ with EF Core.
- Never expose internal domain entities in API request or response models. Use dedicated DTOs.
- Never log secrets, passwords, connection strings, authorization tokens, or sensitive customer PII.

---

# Forbidden Patterns

The following are strictly forbidden in production code:

- Public setters on entity properties (`public string Title { get; set; }`).
- Direct property mutations of domain entities by services.
- `async void` methods.
- `.Result`, `.Wait()`, and `.GetAwaiter().GetResult()` on asynchronous operations.
- Empty `catch` blocks or bare `catch (Exception) { }` without logging.
- `throw new NotImplementedException()` in production execution paths.
- String-concatenated SQL queries.
- Leaking domain entities through API responses.
- Commented-out code used as historical reference (rely on version control).
