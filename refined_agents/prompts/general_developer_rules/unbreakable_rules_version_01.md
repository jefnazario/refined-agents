# 🔒 UNBREAKABLE RULES
> These apply in every context, no exceptions. No agent may override these.

---

## Code Quality

- Never write duplicated code — extract, abstract, reuse.
- Every function/module does ONE thing (Single Responsibility).
- Names must be descriptive and self-documenting — no abbreviations like `tmp`, `x`, `data2`.
- Never leave dead code, commented-out blocks, or TODO without a ticket reference.
- No unimplemented functions or partially implemented features in production code.
- **Readability over cleverness** — avoid dense one-liners, overly clever abstractions, or hidden control flow. Code must be understandable by another engineer reading it later.

---

## Correctness & Priority Order

All code must follow this priority order — no exceptions:

1. **Correctness** — it must work as intended
2. **Maintainability** — it must be easy to change
3. **Simplicity** — it must be easy to understand
4. **Performance** — only after the above are satisfied

---

## Deterministic Behavior

- Avoid hidden global state.
- Avoid non-deterministic logic without explicit justification.
- Side effects must have clear, documented boundaries.
- Functions must be **pure when possible**.

---

## Error Handling

- All errors must be explicitly handled — no silent failures or empty catch blocks.
- External dependencies (APIs, DBs, files) must always have failure handling.
- Do not convert errors into vague or generic messages.
- Avoid panic-style failure unless the program truly cannot recover.
- Error messages must: explain what failed, include useful context, and help debugging.
- **Failures must always be observable** — systems must expose useful errors, logs, or metrics.

---

## Security

- Never hardcode secrets, credentials, or tokens — ever.
- Never trust external input — always validate and sanitize at system boundaries.
- Never expose secrets in logs.
- Never deserialize untrusted data without validation.
- Principle of Least Privilege: code, services, and users get only the access they need.

---

## Dependency Management

- Never add a dependency without evaluating: maintenance status, security history, compile/bundle size, and ecosystem reputation.
- Avoid dependencies when a small amount of internal code solves the problem.
- All production dependencies must be **actively maintained**.

---

## Project Structure

- Projects must follow clear separation of concerns with defined layers: `application → domain logic → infrastructure → interfaces`.
- Business logic must never depend on infrastructure.
- Domain code must remain independently testable.
- Interfaces should be stable.

---

## Versioning

- Every change gets a commit with a clear, descriptive message.
- Never commit directly to `main`/`master` — always via PR/MR.
- Breaking changes must be documented before merging.
- **No code merges without review** — reviewers must verify correctness, clarity, test coverage, dependency safety, and security implications.

---

## SOLID Principles
> Applies to all paradigms, not just OOP.

- **S** — Single Responsibility: one reason to change
- **O** — Open/Closed: extend behavior, don't modify existing
- **L** — Liskov Substitution: subtypes must honor contracts of their base
- **I** — Interface Segregation: small, focused interfaces over fat ones
- **D** — Dependency Inversion: depend on abstractions, not concretions
