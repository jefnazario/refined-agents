🔒 UNBREAKABLE RULES
These apply in every context, no exceptions.
Code Quality

Never write duplicated code — extract, abstract, reuse.
Every function/module does ONE thing (Single Responsibility).
Names must be descriptive and self-documenting — no abbreviations like tmp, x, data2.
Never leave dead code, commented-out blocks, or TODO without a ticket reference.

Security

Never hardcode secrets, credentials, or tokens — ever.
Never trust external input — always validate and sanitize at system boundaries.
Principle of Least Privilege: code, services, and users get only the access they need.

Reliability

All errors must be explicitly handled — no silent failures or empty catch blocks.
External dependencies (APIs, DBs, files) must always have failure handling.

Versioning

Every change gets a commit with a clear, descriptive message.
Never commit directly to main/master — always via PR/MR.
Breaking changes must be documented before merging.

SOLID (applies to all, not just OOP)

S — Single Responsibility
O — Open/Closed (extend, don't modify)
L — Liskov Substitution
I — Interface Segregation (small, focused interfaces)
D — Dependency Inversion (depend on abstractions)


🔧 FLEXIBLE RULES
Strong defaults, but can be adjusted per context or agent.
Testing

Default: write tests before code (TDD). Can be relaxed for prototyping/spike branches.
Minimum coverage threshold should be defined per project (e.g. 80%).
Integration tests are preferred over mocking everything.

Documentation

Default: public APIs and functions must have docstrings/comments. Internal helpers can be skipped if self-documenting.
Architecture decisions should be recorded (ADR format recommended).

Code Style

Follow the ecosystem's standard formatter (Black for Python, rustfmt for Rust, Prettier for infra configs). Custom rules allowed if team-agreed and enforced by CI.
Max function length guideline (e.g. 40 lines) — flexible for complex algorithms.

Dependencies

Prefer standard library over third-party when capability is equivalent. Can be relaxed when a library is the de facto standard (e.g. serde in Rust, requests in Python).
Pin dependency versions in production. Loose in dev/tooling.

Performance

Don't optimize prematurely — profile first, then optimize. Rust agent gets more latitude here since performance is often a primary goal.


