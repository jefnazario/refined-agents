# black_cube_agents

A repository for building and evolving **agent instruction sets** as composable Markdown prompt chunks.

The project currently contains:

- A Rust crate scaffold (`src/main.rs`) that is still a placeholder.
- A Python utility (`refined_agents/create_prompts.py`) for loading and assembling prompt chunks.
- A Python package/CLI (`refined-agents`) for generating prompts after installation.
- A curated prompt catalog under `refined_agents/prompts/system/...` organized by:
  - general engineering rules
  - agent-specific overlays (Codex, Claude Code, Cursor)
  - language-specific rules (Python, Rust)
  - task modes (API, backend, bugfix, etc.)

## Why This Repo Exists

The intent is to treat prompt engineering like software engineering:

- break guidance into small, versioned modules
- assign metadata (`priority`, `tags`)
- compose final system prompts deterministically
- support different contexts (language, mode) without duplicating everything

## Repository Layout

```text
.
├── Cargo.toml
├── src/
│   └── main.rs
└── refined_agents/
    ├── create_prompts.py
    ├── test.sql
    └── prompts/
        ├── specific_specialist_rules/      # currently empty
        └── system/
            ├── general_developer_rules/
            ├── agents/
            │   ├── claude_code/
            │   ├── codex/
            │   └── cursor/
            ├── language_good_pratices/
            │   ├── python/
            │   └── rust/
            └── modes/
                ├── api/
                ├── backend/
                ├── bugfix/
                ├── data_pipeline/
                ├── refactor/
                └── test_generation/
```

## Prompt Model

Each prompt chunk is a Markdown file with optional front matter:

```yaml
---
id: python_defaults
priority: 60
tags: [python]
---
```

Then regular Markdown body content follows.

### Metadata Semantics

- `priority`: lower values are loaded first.
- `tags`: used for include/exclude filtering.
- `id`: identifier for humans and traceability.

If `priority` is missing, `create_prompts.py` tries to infer it from filename prefix (`010_...`).

## How Composition Works (Current Script)

`refined_agents/create_prompts.py` provides:

- `PromptChunk` dataclass
- `AgentProfile` dataclass
- `_parse_front_matter(md_text)`
- `load_chunks(*folders, root="agents/prompts")`
- `build_system_prompt(include_tags=("always",), exclude_tags=(), mode=None)`
- `build_agent_prompt(...)`
- `build_cursor_rule(...)`
- `build_agents_md(...)`

### Composition Flow

```mermaid
flowchart TD
    A[Markdown prompt files] --> B[Parse front matter]
    B --> C[Create PromptChunk objects]
    C --> D[Sort by priority then filename]
    D --> E[Filter by tags include/exclude]
    E --> F[Optional mode filter]
    F --> G[Concatenate content]
    G --> H[Final system prompt string]
```

### Rule Layering Model

```mermaid
flowchart LR
    A[General Rules<br/>always-on] --> D[Composed Prompt]
    B[Agent Overlay<br/>codex, claude-code, cursor] --> D
    C[Language Rules<br/>python or rust] --> D
    E[Mode Rules<br/>api/backend/bugfix/etc.] --> D
```

## Important Current Status (Read This First)

The prompt files are deeply nested (`system/general_developer_rules`, `system/language_good_pratices/python`, etc.) and the generator now supports this layout using recursive Markdown discovery.

By default, prompts are loaded from `refined_agents/prompts` (via `DEFAULT_PROMPTS_ROOT`).

### Practical Impact

`build_system_prompt()` and the CLI now assemble the current catalog directly. Mode-specific files are filtered by selected task mode, and task presets apply include/exclude tags to keep generated prompts focused.

## Quick Start For Engineers

### 1) Install locally as a development library

From the repository root:

```bash
python3 -m pip install -e .
```

After installation, use the CLI:

```bash
refined-agents \
    --agent codex \
    --language python \
    --task api \
    --framework fastapi \
    --objective "Create a FastAPI API for customer CRUD with validation and tests" \
    --output data/fastapi_api_prompt.md
```

You can also run it as a module without relying on the console script:

```bash
python3 -m refined_agents \
    --agent cursor \
    --language python \
    --task backend \
    --objective "Standardize service-layer changes"
```

Library usage:

```python
from refined_agents import build_agent_prompt

prompt = build_agent_prompt(
    agent="cursor",
    language="python",
    task="backend",
    objective="Standardize service-layer changes",
)
print(prompt)
```

### 2) Understand the catalog

Start with these folders:

- `refined_agents/prompts/system/general_developer_rules`
- `refined_agents/prompts/system/agents`
- `refined_agents/prompts/system/language_good_pratices/python`
- `refined_agents/prompts/system/language_good_pratices/rust`
- `refined_agents/prompts/system/modes`

### 3) Run and iterate locally

Use Python 3.11+ (script uses modern typing syntax).

Generate a prompt directly from the terminal with the installed CLI:

```bash
refined-agents \
    --agent codex \
    --language python \
    --task api \
    --framework fastapi \
    --objective "Create a FastAPI API for customer CRUD with validation and tests" \
    --output data/fastapi_api_prompt.md
```

The direct script command also works from the repository root:

```bash
python3 refined_agents/create_prompts.py \
    --agent codex \
    --language python \
    --task api \
    --framework fastapi \
    --objective "Create a FastAPI API for customer CRUD with validation and tests" \
    --output data/fastapi_api_prompt.md
```

Data pipeline example:

```bash
python3 refined_agents/create_prompts.py \
    --agent claude-code \
    --language python \
    --task data_pipeline \
    --objective "Build an idempotent pipeline to ingest CSV, validate schema, and publish curated parquet" \
    --output prompts/data_pipeline_prompt.md
```

Cursor project rule example:

```bash
python3 refined_agents/create_prompts.py \
    --agent cursor \
    --language python \
    --task backend \
    --objective "Standardize service-layer changes around explicit validation, tests, and minimal diffs" \
    --format cursor-rule \
    --cursor-rule-type files \
    --cursor-globs "src/**/*.py,tests/**/*.py" \
    --cursor-description "Python backend service conventions" \
    --output .cursor/rules/python-backend-service.mdc
```

Cursor `AGENTS.md` example:

```bash
python3 refined_agents/create_prompts.py \
    --agent cursor \
    --language python \
    --task refactor \
    --objective "Refactor safely while preserving behavior and verifying with the existing test suite" \
    --format agents-md \
    --output AGENTS.md
```

Interactive mode (asks questions in terminal):

```bash
python3 refined_agents/create_prompts.py --interactive
```

If you prefer to print to stdout instead of writing a file, omit `--output`.

Project context is now optional and externalized:

- If you do not pass a project context source, prompts are generated without project context.
- Use `--project-context-path` to load project context from a local markdown file.
- Use `--project-context-url` to download project context from a URL.

Example with local project context:

```bash
refined-agents \
    --agent codex \
    --language python \
    --task backend \
    --objective "Implement service layer for order lifecycle" \
    --project-context-path refined_agents/prompts/system/general_developer_rules/000_project_context.md \
    --output data/backend_prompt.md
```

### 3.1) Configure defaults via environment variables (Dynaconf)

The generator now uses Dynaconf and loads defaults from:

- `refined_agents/settings.toml`
- `refined_agents/.secrets.toml` (optional, gitignored)
- environment variables with prefix `REFINED_AGENTS_`

Example:

```bash
REFINED_AGENTS_AGENT=cursor \
REFINED_AGENTS_LANGUAGE=python \
REFINED_AGENTS_TASK=data_pipeline \
refined-agents --objective "Create an ingestion pipeline with schema validation"
```

Minimal local experimentation from repository root using the library API:

```bash
python3 - <<'PY'
from refined_agents.create_prompts import build_system_prompt

# This call reflects current defaults; see caveat section in README.
result = build_system_prompt(include_tags=("always", "python", "backend"), mode="backend")
print(result[:1000])
PY
```

### 4) Extend rules safely

When adding a new prompt chunk:

- place it in the correct domain folder
- add front matter (`id`, `priority`, `tags`)
- keep one focused concern per file
- avoid duplicating existing rules

## Prompt Domains In This Repo

- **General developer rules**: reasoning strategy, code generation behavior, non-negotiables.
- **Agent overlays**: Codex, Claude Code, and Cursor-specific execution guidance.
- **Python rules**: lint/type/test expectations, async/data guidance, backend/API defaults.
- **Rust rules**: safety/error/tooling/async defaults.
- **Modes**: overlays for specific tasks (bugfix, refactor, test generation, backend, API, data pipeline).

## Suggested Next Engineering Steps

1. Expand automated tests for front matter parsing, mode detection, tag filtering, and output formats.
2. Add real examples under `specific_specialist_rules/`.
3. Add task presets for more frameworks/stacks (e.g., Django, Axum, Actix).
4. Add Claude Code native artifact output (`CLAUDE.md`) if project-level Claude workflows become a target.
5. Replace placeholder Rust `main.rs` or document Rust role if intentionally reserved.

## Notes

- `test.sql` is currently empty.
- `specific_specialist_rules/` is currently empty.
- Rust crate is currently scaffold-only (`Hello, world!`).

## Evidence Docs

- `refined_agents/docs/coding_agent_evidence.md`: documented differences and source-backed rationale for Codex, Claude Code, and Cursor prompt optimization.
