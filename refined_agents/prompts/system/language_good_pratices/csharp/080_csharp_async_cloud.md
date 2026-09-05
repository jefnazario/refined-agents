---
id: csharp_async_cloud
priority: 80
tags: [csharp, async, cloud]
---

# C# & .NET Async, Concurrency & Cloud Scalability Rules

These rules govern asynchronous operations, concurrency discipline, and cloud-native scalability in C# and .NET applications.

---

# Asynchronous Programming & Concurrency

- **Pure Async**: Always use `async` and `await` end-to-end. Do not mix synchronous and asynchronous calls.
- **No Thread Starvation**:
  - Never call `.Result`, `.Wait()`, or `.GetAwaiter().GetResult()`.
  - Never use `Thread.Sleep()`; use `await Task.Delay(...)`.
  - Never instantiate raw `Thread` objects; rely on the .NET thread pool and `Task` abstractions.
- **Cancellation Propagation**:
  - Accept a `CancellationToken` on all public asynchronous methods (`CancellationToken cancellationToken = default`).
  - Pass the token down to all I/O operations (EF Core queries, HTTP requests, stream reads).
- **Parallel Independent I/O**:
  - When multiple independent asynchronous tasks can run concurrently, dispatch them together and await with `Task.WhenAll(...)`.
- **CPU-Bound Work**:
  - For CPU-heavy processing inside web services, offload to background threads with `Task.Run(...)` only when necessary, or delegate to dedicated background worker services.
- **In-Memory Concurrency**:
  - Use `System.Threading.Channels` for producer-consumer workflows.
  - Prefer immutable data structures or message passing over explicit lock primitives (`Monitor`, `lock`).

---

# Scalability & Cloud Architecture (Azure)

- **Stateless Services for Auto-Scaling**:
  - Web APIs and services must be completely stateless to support automated scaling based on real-time traffic and resource consumption.
  - Store session and temporary state in external distributed caches (e.g., Redis or Azure Cache for Redis), never in local memory.
- **Event-Driven Decoupling with Queues**:
  - Use **Azure Queues** or **Azure Service Bus** for asynchronous, background, or resource-intensive processing.
  - Decouple time-consuming operations from the HTTP request/response loop by publishing messages to queues and processing them in worker services.
- **Database-Backed Queues**:
  - When transactional consistency requires keeping jobs in the relational database, manage queue items using status flags, explicit transitions, and optimistic or pessimistic concurrency controls.
- **Resilience & Fault Tolerance**:
  - Implement bounded retries with exponential backoff and jitter using **Polly** for transient network or cloud service failures.
  - Use circuit breakers and fallback policies to protect downstream services from cascading degradation.

---

# Resource Lifecycle Management

- Always dispose of managed resources deterministically.
- Prefer `await using` for types implementing `IAsyncDisposable` (e.g., `DbConnection`, `FileStream`, `HttpResponseMessage`).
- Avoid creating manual `HttpClient` instances inside request scopes; always register and inject `IHttpClientFactory`.
