---
id: vue_async_state
priority: 80
tags: [vue, vuejs, async, state]
---

# Vue.js Async State Management & API Integration Rules

These rules govern how data is fetched, state is structured, and asynchronous lifecycles are handled in Vue 3 applications.

---

# State Architecture: Local vs. Global

### When to Keep State Local (`ref` / `reactive`)

Always prefer local component state by default:
- Modal or dialog open/close flags.
- Form inputs before submission.
- Accordion or tab active indexes.
- Tooltips, dropdown toggles, and UI-only animations.

### When to Use Pinia Stores

Adopt Pinia stores only when:
- State must persist across route navigation (e.g., current user profile, auth session).
- Multiple unrelated components across the application need real-time synchronization.
- Complex domain state requires centralized actions with shared cache or coordination.

Avoid turning Pinia stores into generic "data dumps" for arbitrary component variables.

---

# Explicit Asynchronous States

Asynchronous operations must never be represented by simple booleans alone.

Explicitly model operations with five states:

```text
idle    → Operation has not yet started.
loading → Request is currently in flight.
success → Data was successfully received and is non-empty.
empty   → Request succeeded, but result list/dataset is empty.
error   → Operation failed; error message or diagnostics available.
```

### Discriminated Union Pattern

When managing complex asynchronous state in composables, represent state using discriminated unions:

```ts
export type AsyncState<T> =
  | { status: 'idle'; data: null; error: null }
  | { status: 'loading'; data: null; error: null }
  | { status: 'success'; data: T; error: null }
  | { status: 'empty'; data: []; error: null }
  | { status: 'error'; data: null; error: Error };
```

This prevents impossible states (such as `isLoading: true` and `error: Error` coexisting).

---

# REST API Integration Layer

Maintain a clean separation of network concerns:

```text
View Component
      ↓
  Composable       (orchestrates UI state, triggers fetch)
      ↓
   Service         (encapsulates API endpoints and DTO transforms)
      ↓
  HTTP Client      (Axios / Fetch with centralized interceptors)
      ↓
  Backend API
```

### Integration Rules

- **Typed Contracts**: Define explicit TypeScript interfaces for all Request and Response payloads.
- **Centralized Interceptors**:
  - Automatically attach JWT Bearer tokens to request headers.
  - Intercept 401 Unauthorized responses to clear stale sessions and redirect to login.
- **Normalized Error Handling**:
  - Translate backend error schemas into user-friendly error objects.
  - Never swallow errors silently in `catch` blocks.
- **Cancellation & Cleanup**:
  - Cancel in-flight requests using `AbortController` when components unmount to prevent memory leaks and race conditions on rapid user navigation.

---

# Vue Router & Navigation Guards

- **Declarative Route Metadata**:
  - Use `meta` tags to declare access requirements:
    ```ts
    {
      path: '/dashboard',
      component: () => import('./views/DashboardView.vue'),
      meta: { requiresAuth: true, roles: ['admin', 'manager'] }
    }
    ```
- **Navigation Guards**:
  - Implement `beforeEach` navigation guards to evaluate authentication tokens before rendering protected routes.
  - Handle session timeouts and unauthorized navigation cleanly with redirect parameters (e.g., `?redirect=/original-target`).
