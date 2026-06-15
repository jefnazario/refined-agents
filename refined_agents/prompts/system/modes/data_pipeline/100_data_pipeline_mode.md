---
id: data_pipeline_mode
priority: 90
tags: [data_pipeline]
---

# Data Pipeline Mode

When working on data pipelines, prioritize correctness, observability, and reproducibility.

Rules:

- make data transformations explicit
- validate schema assumptions
- handle missing and invalid values intentionally
- avoid silent coercion
- log pipeline stage boundaries and failures
- keep transformations testable and deterministic
- make time and timezone handling explicit.
