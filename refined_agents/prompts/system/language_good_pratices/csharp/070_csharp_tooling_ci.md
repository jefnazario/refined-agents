---
id: csharp_tooling_ci
priority: 70
tags: [csharp, ci]
---

# C# & .NET Tooling, Testing & CI Rules

All C#/.NET projects must maintain a consistent, automated tooling and verification pipeline.

---

# Static Analysis & Formatting

- **Roslyn Analyzers**: Enable .NET code analysis in project files:
  ```xml
  <PropertyGroup>
    <AnalysisLevel>latest-recommended</AnalysisLevel>
    <EnforceCodeStyleInBuild>true</EnforceCodeStyleInBuild>
  </PropertyGroup>
  ```
- **Treat Warnings as Errors**: In CI and Release builds, treat all compiler warnings as errors:
  ```xml
  <PropertyGroup Condition="'$(Configuration)' == 'Release'">
    <TreatWarningsAsErrors>true</TreatWarningsAsErrors>
  </PropertyGroup>
  ```
- **Formatting**: Maintain consistent coding styles via a shared `.editorconfig` file.
- Verify formatting in CI via:
  ```bash
  dotnet format --verify-no-changes
  ```

---

# Testing Stack & Guidelines

Standard testing tools for C#/.NET:

- **Test Framework**: **xUnit** (preferred default) or **NUnit**.
- **Assertions**: **FluentAssertions** for human-readable, expressive test assertions.
- **Mocking**: **Moq** or **NSubstitute** for mocking service interfaces in unit tests.
- **Integration Tests**: Use `Microsoft.AspNetCore.Mvc.Testing` (`WebApplicationFactory<Program>`) with an isolated test database (or Testcontainers) to test complete HTTP request/response pipelines.

### Test Rules

- Tests must be deterministic and isolated; no shared mutable test state between test runs.
- Do not mock domain entities or value objects; instantiate them directly using their constructors and intention-revealing methods.
- Integration tests must verify response status codes, payload shapes, and database state transitions.

---

# Dependency Management & Security

- **Careful Dependency Policy**: Keep dependencies lean, well-maintained, and modern. Avoid unmaintained third-party libraries.
- **Vulnerability Auditing**: CI must check for known package vulnerabilities:
  ```bash
  dotnet list package --vulnerable --include-transitive
  ```
- Any high or critical vulnerability blocks build merges.

---

# Continuous Integration Pipeline

Every pull request and build must execute the following validation steps:

1. **Restore**:
   ```bash
   dotnet restore
   ```
2. **Build with strict warnings**:
   ```bash
   dotnet build --no-restore -c Release /p:TreatWarningsAsErrors=true
   ```
3. **Format verification**:
   ```bash
   dotnet format --verify-no-changes
   ```
4. **Test execution**:
   ```bash
   dotnet test --no-build -c Release --logger "console;verbosity=normal"
   ```
5. **Security scan**:
   ```bash
   dotnet list package --vulnerable --include-transitive
   ```

Pull requests must never merge if any of these checks fail.
