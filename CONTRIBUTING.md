# Contributing

Thanks for helping improve `black_cube_agents`.

This repository is a shared prompt catalog plus tooling for generating coding-agent prompts for Codex, Claude Code, Cursor, and future coding agents.

## Development Setup

Python workflow:

```bash
python3 -m pip install -e .
python3 -m unittest discover -s tests
```

Rust workflow:

```bash
cargo fmt --check
cargo check
```

## Adding Prompt Chunks

Prompt chunks live under `refined_agents/prompts/system`.

Each chunk should:

- use front matter with `id`, `priority`, and `tags`
- cover one focused concern
- avoid duplicating existing rules
- be source-backed when making agent-specific claims

Example:

```markdown
---
id: cursor_backend_overlay
priority: 35
tags: [cursor, backend]
---

# Cursor Backend Overlay

...
```

## Adding Agent Guidance

Agent-specific guidance belongs under:

- `refined_agents/prompts/system/agents/codex`
- `refined_agents/prompts/system/agents/claude_code`
- `refined_agents/prompts/system/agents/cursor`

Before adding strong claims about an agent, update `refined_agents/docs/coding_agent_evidence.md` with official sources or mark the claim as a hypothesis to test.

## Pull Request Checklist

- Tests pass with `python3 -m unittest discover -s tests`.
- Rust checks pass with `cargo fmt --check` and `cargo check`.
- New prompt chunks have clear metadata.
- Public docs are updated when behavior changes.
- Generated files, caches, and local virtualenv files are not committed.
