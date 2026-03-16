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
