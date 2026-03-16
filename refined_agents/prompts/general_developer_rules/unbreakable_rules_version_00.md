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
