---
id: vue_tooling_ci
priority: 70
tags: [vue, vuejs, ci]
---

# Vue.js Tooling, Quality & CI Rules

All Vue.js and frontend projects must maintain a consistent, automated tooling and verification pipeline.

---

# Build & Development Tooling

- **Vite**: The standard build tool and development server for Vue 3 applications.
- **Fast HMR & Optimized Bundles**:
  - Keep plugins lean and avoid heavy build-time transformations.
  - Ensure paths and module aliases (e.g., `@/` pointing to `src/`) are aligned between `vite.config.ts`, `tsconfig.json`, and test runners.

---

# Static Type Checking

- **Template & Script Validation**:
  - CI must run `vue-tsc --noEmit` to validate TypeScript types inside both `<script>` and `<template>` blocks.
  - Do not rely solely on editor linting; `vue-tsc` catches broken prop types and missing template bindings that standard `tsc` overlooks.
- Configuration must enforce:
  - `"strict": true`
  - `"noImplicitAny": true`
  - `"skipLibCheck": true`

---

# Linting & Formatting

- **ESLint**:
  - Enforce official rules using `eslint-plugin-vue` (essential/recommended rules) and `@vue/eslint-config-typescript`.
  - Prohibit unused variables, broken component tags, and formatting violations.
- **Prettier**:
  - Centralize code formatting rules in `.prettierrc`.
  - CI must verify formatting consistency:
    ```bash
    npx prettier --check "src/**/*.{ts,vue,css,html}"
    ```

---

# Testing Stack & Guidelines

Standard testing tools for Vue applications:

- **Vitest**: Preferred unit test runner.
  - Use for testing composables, utility functions, validation schemas, and Pinia stores.
  - Fast execution and native Vite configuration sharing.
- **Vue Test Utils**: Component testing library.
  - Use for testing component interactions, prop passing, custom event emissions (`wrapper.emitted()`), and conditional DOM rendering.
  - Test observable user behavior rather than internal component implementation details.
- **Playwright**: End-to-end (E2E) testing framework.
  - Use for critical business journeys: authentication flows, multi-step checkout/registration forms, and core navigation.

---

# Dependency Management & Security

- **Strict Dependency Discipline**:
  - Evaluate bundle size impact before adding third-party packages (use tools like `bundlephobia`).
  - Prefer native web APIs or Vue built-in utilities over micro-libraries.
- **Vulnerability Auditing**:
  - CI must audit for known dependency vulnerabilities:
    ```bash
    npm audit --audit-level=high
    ```
  - Unresolved high or critical vulnerabilities block pull request merges.

---

# Continuous Integration Pipeline

Every pull request and build must execute the following automated stages:

1. **Lint Check**:
   ```bash
   npm run lint
   ```
2. **Type Check**:
   ```bash
   npx vue-tsc --noEmit
   ```
3. **Automated Unit & Component Tests**:
   ```bash
   npm run test:unit -- --run
   ```
4. **Production Build**:
   ```bash
   npm run build
   ```
5. **Security Audit**:
   ```bash
   npm audit --audit-level=high
   ```

Pull requests must never merge if any of these checks fail.
