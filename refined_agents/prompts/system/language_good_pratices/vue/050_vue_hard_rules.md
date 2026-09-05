---
id: vue_hard_rules
priority: 50
tags: [always, vue, vuejs]
---

# Vue.js & Frontend Engineering Rules — Hard Constraints

These rules are **non-negotiable** and apply to all Vue 3 / TypeScript frontend production code.

---

# Separation of Concerns & Component Purity

Components must remain focused on presentation and user interaction.

- **No Direct HTTP in Presentation Components**:
  - Components must never make direct `fetch()`, `axios`, or client HTTP calls.
  - All external network communication must be encapsulated inside dedicated API services or composables (`useUser()`, `userService.ts`).
- **No Giant Monolithic Components**:
  - A component must never combine business logic from multiple unrelated domains or grow into hundreds of lines of mixed template, styles, and state.
  - Divide large screens into cohesive child components and extract reusable logic into composables.
- **Composition API Exclusivity**:
  - Always use **Composition API** with `<script setup lang="ts">` in new code.
  - Options API is strictly forbidden in new features unless maintaining legacy components that explicitly mandate it.
- **No Unjustified Watchers**:
  - Never use `watch` or `watchEffect` to derive state that can be expressed naturally with `computed`.
  - Use `watch` only when reacting to state changes with an intentional, non-derivable side effect (e.g., triggering network requests or synchronizing third-party libraries).

---

# Type Safety & TypeScript Discipline

- **Strictly Prohibit `any`**:
  - Never use `any` as a shortcut or workaround for typing challenges.
  - Use `unknown`, proper generics, narrowing type guards, or discriminated unions.
- **No Unsafe Type Assertions**:
  - Do not use `as SomeType` merely to silence TypeScript compiler warnings. Fix the underlying type contract or use runtime type validation.
- **Typed Contracts**:
  - Component props (`defineProps<{ ... }>()`) and emitted events (`defineEmits<{ ... }>()`) must be strictly and explicitly typed.
  - All API requests, responses, and error structures must have explicit TypeScript interface/type contracts.

---

# Security & Secrets

- **Zero Secrets on Frontend**:
  - Never store private API keys, database credentials, encryption secrets, or sensitive tokens in client-side code.
  - Any environment variable prefixed with `VITE_` is compiled into the public client bundle and must be treated as completely public.
- **Strict `v-html` Sanitization**:
  - Never render dynamic, user-provided, or external HTML using `v-html` without prior sanitization using an approved library (e.g., DOMPurify).
  - Unsanitized `v-html` is an immediate XSS vulnerability.
- **No Client-Side Authorization Assumptions**:
  - Hiding buttons, links, or navigation menus based on user roles is an interface enhancement (UX), **never** a security boundary.
  - The frontend must assume any action can be called maliciously; backend APIs must independently authenticate and authorize every request.

---

# State & Reactivity Invariants

- **No Gratuitous Global State**:
  - Never place purely local or ephemeral component state into Pinia.
  - Pinia stores are reserved exclusively for state that survives route navigation, is shared across disparate features, or represents global session/auth.
  - Modals, temporary form fields, and dropdown visibility must remain local component state (`ref`).

---

# Asynchronous States & UX Correctness

- **Never Ignore Asynchronous States**:
  - Every meaningful asynchronous operation must explicitly account for all five lifecycle states:
    ```text
    idle → loading → success → empty → error
    ```
  - Never leave users with an unhandled loading spinner, frozen UI, or blank view on API errors.
  - Disable submit buttons during pending requests to prevent duplicate form submissions.

---

# Forbidden Patterns

The following patterns are strictly forbidden in production code:

- `any` in TypeScript declarations.
- Direct `fetch`/`axios` calls inside `.vue` component templates or scripts.
- Unsanitized `v-html`.
- Exposing private backend secrets in `VITE_*` environment variables.
- Modifying props directly inside child components (violating one-way data flow).
- Incomplete placeholder stubs (`// TODO`, unfinished methods) in production paths.
- Commented-out code preserved as historical reference (rely on Git history).
- Global mutable objects outside Vue's reactivity system.
