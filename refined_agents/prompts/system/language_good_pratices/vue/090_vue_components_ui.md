---
id: vue_components_ui
priority: 90
tags: [vue, vuejs, frontend, ui]
---

# Vue.js UI, UX, Styling & Accessibility Rules

These rules govern user interface design, form validation, component styling, accessibility, and frontend performance in Vue applications.

---

# Accessibility (a11y) Standards

Accessibility is not optional and must be considered during initial implementation.

- **Semantic HTML5 Elements**:
  - Use native HTML elements (`<button>`, `<header>`, `<main>`, `<nav>`, `<section>`, `<article>`) instead of generic `<div onclick="...">`.
- **Keyboard Navigation & Focus States**:
  - Interactive elements must be navigable via keyboard (`Tab`, `Enter`, `Space`).
  - Never remove focus outlines (`outline: none` or `outline-none`) without providing an explicit, high-contrast replacement focus indicator.
- **Form Accessibility**:
  - Every `<input>`, `<select>`, and `<textarea>` must have a programmatic label via `<label for="...">` or `aria-label`.
  - Link field validation errors to inputs using `aria-describedby="error-id"` and indicate invalid state with `aria-invalid="true"`.
- **Color Contrast & Dynamic Visuals**:
  - Maintain minimum WCAG AA contrast ratios (4.5:1 for normal text, 3:1 for large text).
  - Do not convey information exclusively through color; include icons or clear text labels.

---

# Forms & Validation

- **Predictable Form State**:
  - Keep complex validation logic inside composables or schema validators (e.g., Zod, VeeValidate), not directly in component templates.
- **Immediate & Adjacent Feedback**:
  - Display validation error messages adjacent to the corresponding input fields, not in distant toast notifications alone.
- **Submission Safeguards**:
  - Disable submit buttons and display a loading indicator while a form submission is in flight (`:disabled="isSubmitting"`).
  - Prevent accidental double submissions and handle rapid duplicate clicks gracefully.

---

# Styling: Tailwind CSS & Scoped Styles

- **Design System Consistency**:
  - Adhere strictly to the project's design tokens (palette colors, typography scales, spacing tokens).
  - Avoid arbitrary utility classes (e.g., `w-[317px]`, `text-[#ff0044]`) when design system tokens exist.
- **Component Extraction**:
  - When a cluster of Tailwind classes repeats frequently across features, extract a reusable UI component (e.g., `AppButton.vue`, `BaseInput.vue`) instead of copying strings of classes.
- **Scoped Styles**:
  - When custom CSS is required, always scope it with `<style scoped>` to prevent styles from leaking into other components.
  - Avoid heavy global style overrides.

---

# Frontend Performance Optimization

- **Route-Level Code Splitting**:
  - Load all Vue Router view components lazily via dynamic imports:
    ```ts
    component: () => import('./views/UsersView.vue')
    ```
- **Asynchronous Component Loading**:
  - Use `defineAsyncComponent()` for heavy, rarely used components (e.g., rich text editors, charting libraries, large modals).
- **List Virtualization**:
  - Never render thousands of DOM nodes simultaneously. Use virtualized scrolling lists for large collections.
- **Debouncing and Throttling**:
  - Debounce search inputs, auto-save triggers, and filter queries to avoid flooding the backend with network requests.
- **Computed Caching**:
  - Use `computed` properties for expensive calculations; Vue caches computed results and only re-evaluates when reactive dependencies change.
