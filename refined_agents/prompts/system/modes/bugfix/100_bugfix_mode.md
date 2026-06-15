---
id: bugfix_mode
priority: 90
tags: [bugfix]
---

# Bugfix Mode

When fixing bugs, prioritize minimal and safe changes.

Rules:

- identify the root cause before modifying code
- do not rewrite unrelated components
- preserve existing behavior outside the bug scope
- add or update regression tests
- explain the cause of the bug briefly when relevant
- avoid broad refactors during bug fixes unless required for correctness.
