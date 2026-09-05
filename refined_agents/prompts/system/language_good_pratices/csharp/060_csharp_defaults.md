---
id: csharp_defaults
priority: 60
tags: [csharp]
---

# C# & .NET Engineering Rules — Default Practices

These are **strong defaults** for C#/.NET architecture and design, to be followed unless a compelling, documented justification exists.

---

# Architecture & Module Conventions

Structure code around cohesion and clean boundaries using **Vertical Slice Architecture** or **Clean Architecture** conventions.

When organizing code by modules, place each module in `Modules/{ModuleName}/` with dedicated files per responsibility:

- `{Module}Controller.cs`: Receives and responds to HTTP requests. Contains zero business logic and delegates directly to the service interface.
- `I{Module}Service.cs`: Public contract of the module. This is the **only** dependency the controller is permitted to know.
- `{Module}Service.cs`: Concrete service implementation. Implements business orchestration, coordinates repositories, and enforces workflow rules.
- `{Module}Models.cs`: Request, Response, and internal DTOs. Strongly-typed models that never leak domain entities to callers.

### Golden Rules of Modules

1. **Decoupled modules**: Modules never reference each other's internal concrete implementations — only public interfaces or domain abstractions.
2. **Interface before implementation**: Design and establish the contract (`I{Module}Service.cs`) before coding the implementation.
3. **Restricted controller scope**: Controllers only know their module's service interface.
4. **Strict DTO isolation**: Models must never expose internal domain entities; always use dedicated, typed DTOs.
5. **One file per responsibility**: Keep files focused and separated, even if small.
6. **Consistent naming**: Use the module name as a prefix for all files inside its directory.

### Module Setup Sequence

When creating a new module:
1. Create the directory under `Modules/{ModuleName}/`.
2. Create `I{Module}Service.cs` defining the contractual operations.
3. Create `{Module}Models.cs` with the necessary DTOs.
4. Create `{Module}Service.cs` implementing the contract and business orchestration.
5. Create `{Module}Controller.cs` delegating to the interface.
6. Register the module via an extension method (e.g., `Add{Module}Module(this IServiceCollection services)`) and invoke it in `Program.cs`.

---

# Design Principles & Patterns

Apply these principles consistently:

- **SOLID & DRY**: Uphold Single Responsibility strictly; if a class takes on multiple concerns, refactor it immediately. Eliminate duplicate logic or configurations.
- **KISS & YAGNI**: Keep solutions straightforward. Avoid premature abstractions until a real need emerges.
- **Dependency Injection**: Always use constructor injection. Keep constructors focused; excessive parameters indicate a violation of Single Responsibility.
- **Options Pattern**: Use strongly-typed configuration classes bound with `IOptions<T>` or `IOptionsSnapshot<T>` instead of raw `IConfiguration["key"]`.
- **Result Pattern**: Prefer returning a `Result<T>` or `Result` for expected operational outcomes (e.g., entity not found, validation error, business precondition failed) over throwing domain exceptions.
- **CQRS & MediatR**: When read and write paths benefit from separation or decoupled orchestration, apply CQRS and MediatR handlers.

---

# C# Idiomatic Style & Conventions

- **Nullable Reference Types**: Keep `<Nullable>enable</Nullable>` active. Handle nullable warnings intentionally; never suppress with `!` unless proven safe with a comment.
- **Modern Constructs**:
  - Use file-scoped namespaces (`namespace App.Modules.Orders;`).
  - Use `record` or `record struct` for immutable DTOs and Value Objects.
  - Use pattern matching (`is`, `switch` expressions) over deep `if-else` chains or type casting.
  - Use collection expressions (`[...]`) in modern .NET where appropriate.
- **Naming Conventions**:
  - `PascalCase` for classes, records, interfaces, structs, enums, methods, and properties.
  - `camelCase` for method parameters and local variables.
  - `_camelCase` with leading underscore for `private readonly` dependency fields.
  - Prefix interfaces with `I` (e.g., `IOrderService`).

---

# Testing Philosophy & TDD

- Practice **Test-Driven Development (TDD)** (Red, Green, Refactor) whenever the project allows.
- **Unit Tests**: Cover class logic in isolation. Mocks should only be used for external dependencies, never for domain entities.
- **Integration Tests**: Validate end-to-end communication across real layers and database queries.
- **Test Naming Convention**:
  Use the semantic format: `UnitOfWork_Scenario_ExpectedResult`
  - Example: `LoginService_WhenCredentialsAreInvalid_ShouldReturnUnauthorized`
  - Example: `Appointment_WhenScheduledInThePast_ShouldThrowDomainException`
