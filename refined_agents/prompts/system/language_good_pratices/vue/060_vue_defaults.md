---
id: vue_defaults
priority: 60
tags: [vue, vuejs]
---

# Vue.js & Frontend Engineering Rules — Default Practices

These are **strong defaults** for modern Vue 3 applications, to be applied unless a clear, documented project constraint requires otherwise.

---

# Architecture & Module Structure

Structure large applications **by feature / module** rather than flat technical categories.

### Modular Architecture Layout

```text
src/
├── app/
│   ├── router/
│   ├── layouts/
│   ├── providers/
│   └── App.vue
├── modules/
│   ├── auth/
│   │   ├── components/
│   │   ├── composables/
│   │   ├── services/
│   │   ├── stores/
│   │   ├── types/
│   │   └── views/
│   └── users/
│       ├── components/
│       ├── composables/
│       ├── services/
│       ├── stores/
│       ├── types/
│       └── views/
├── components/
│   ├── ui/        # Atomic, generic design system components (Button, Input, Modal)
│   └── shared/    # Cross-module domain widgets
├── composables/   # Cross-cutting composables (useWindowSize, useDark)
├── services/      # Core HTTP clients and interceptors
├── types/         # Global domain contracts
├── utils/         # Pure helper functions
└── main.ts
```

### Module Responsibilities

- **`views/`**: Orchestrate screen composition and layout; do not contain low-level business logic.
- **`components/`**: Feature-specific presentation and UI components.
- **`composables/`**: Encapsulate stateful, reusable business logic specific to the feature.
- **`services/`**: Encapsulate API communication and external integration endpoints.
- **`stores/`**: Manage shared global state via Pinia when state must survive across routes.
- **`types/`**: Interfaces, types, and DTO contracts.
- **`index.ts`**: Public API boundary for the module; export only what other modules need.

---

# Component Design & Composition API

- **`<script setup lang="ts">`**: Use for all new components.
- **Props and Emits Definition**:
  - Always use type-based declarations:
    ```vue
    <script setup lang="ts">
    interface Props {
      userId: string;
      disabled?: boolean;
    }

    const props = withDefaults(defineProps<Props>(), {
      disabled: false,
    });

    const emit = defineEmits<{
      (e: 'select', id: string): void;
      (e: 'cancel'): void;
    }>();
    </script>
    ```
- **Composition over Configuration**:
  - Prefer slots (`<slot name="header" />`, scoped slots) for flexible component customization over boolean flags and complex configuration props.
- **Single Responsibility**:
  - Components should do one thing well. If a component grows large, extract smaller child components and move state orchestration into a composable.

---

# Clean Code & Idiomatic Naming

- **Boolean State**: Prefix booleans with descriptive qualifiers: `isLoading`, `isSubmitting`, `hasError`, `canEdit`.
- **Event Handlers**:
  - Functions handling user actions: `handleSubmit`, `handleRowClick`, `handleDelete`.
  - Service/composable triggers: `loadUsers()`, `createUser()`, `resetForm()`.
- **File Naming Conventions**:
  - Components: `PascalCase.vue` (e.g., `UserCard.vue`, `AppointmentModal.vue`).
  - Composables: `camelCase.ts` starting with `use` (e.g., `useUserList.ts`, `useAuth.ts`).
  - Services: `camelCase.ts` or `kebab-case.service.ts` (e.g., `userService.ts`).
  - Pinia Stores: `use{Name}Store.ts` (e.g., `useAuthStore.ts`).

---

# Testing Philosophy & TDD

- Follow **TDD** (Red → Green → Refactor) whenever the project permits.
- Write tests that verify observable user behavior and component outputs rather than internal implementation details.
- **Test Naming Convention**:
  Use the format: `UnitOfWork_Scenario_ExpectedResult`
  - Example: `LoginForm_WhenCredentialsInvalid_ShouldDisplayErrorMessage`
  - Example: `useUserList_WhenFetchFails_ShouldSetErrorState`

---

# Feature Implementation Workflow

When building a new frontend feature:

1. **Understand requirements**: Review user flows, acceptance criteria, and edge cases.
2. **Define contracts**: Establish TypeScript types for models, API payloads, and component props.
3. **API Integration**: Build or update the typed service layer and HTTP clients.
4. **Composables**: Implement business logic, reactive state, and error handling in composables.
5. **UI & Components**: Compose views, reusable components, and form validation.
6. **Async States**: Wire `loading`, `empty`, and `error` visual states.
7. **Accessibility & Responsive Testing**: Ensure keyboard navigation and responsive breakpoints work cleanly.
8. **Automated Tests**: Write unit and component tests covering critical paths.
9. **Verification**: Run lint, type-checking (`vue-tsc`), and build.

---

# Definition of Done

A task is complete only when:
- Functionality is verified against acceptance criteria.
- TypeScript compiles cleanly with zero warnings or `any` casts.
- Visual loading, empty, and error feedback states are functional.
- Responsive design and keyboard accessibility are verified.
- Unit and component tests pass.
- Code passes linting and formatting.
