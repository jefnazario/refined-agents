# Coding Agent Evidence Matrix

## Purpose

This document records what is explicitly documented by official sources for Codex, Claude Code, and Cursor, and how those facts should influence prompt-generation strategy in this repository.

Goals:

- avoid opinion-only guidance
- separate verified facts from implementation choices
- provide auditable references for agent-specific prompt tuning
- support both plain prompt output and agent-native instruction artifacts

Last updated: 2026-06-15

## Scope and Confidence

Confidence levels used in this document:

- **High**: directly stated in official product documentation.
- **Medium**: inferred from official CLI, rule, or feature behavior, but not stated as a direct prompting rule.
- **Low**: hypothesis to test in our own benchmark loop.

## What Is Explicitly Documented

### Product and Surface Model

- **Codex** is documented as OpenAI's coding agent, available in app, CLI, IDE, and cloud surfaces.
  - Source: <https://developers.openai.com/codex/>
  - Source: <https://developers.openai.com/codex/quickstart>
  - Source: <https://github.com/openai/codex>
- **Claude Code** is documented as an agentic coding tool available in terminal, IDE, desktop app, and browser.
  - Source: <https://code.claude.com/docs/en/overview>
- **Cursor** documents Agent as a coding assistant that can complete coding tasks, run terminal commands, edit code, search code, use browser control, and operate with model-specific tooling.
  - Source: <https://cursor.com/docs/agent/overview.md>

**Confidence:** High

### Persistent Instruction Surfaces

- **Codex** supports repository instructions and prompt customization through Codex product surfaces and CLI workflows.
  - Source: <https://developers.openai.com/codex/>
  - Source: <https://developers.openai.com/codex/cli/reference>
- **Claude Code** documents project-level instruction placement such as `CLAUDE.md`, settings scopes, and system-prompt customization flags.
  - Source: <https://code.claude.com/docs/en/settings>
  - Source: <https://code.claude.com/docs/en/cli-reference>
- **Cursor** documents `.cursor/rules/*.mdc`, User Rules, Team Rules, and `AGENTS.md`. Cursor rules are included at the start of model context when applied.
  - Source: <https://cursor.com/docs/rules.md>

**Confidence:** High

### Non-Interactive and Automation Workflows

- **Codex** explicitly documents `codex exec` for scripts/CI, JSON output, schema output, and automation safety guidance.
  - Source: <https://developers.openai.com/codex/noninteractive>
  - Source: <https://developers.openai.com/codex/cli/reference>
- **Claude Code** explicitly documents `claude -p`, piping, non-interactive usage, and command/flag reference.
  - Source: <https://code.claude.com/docs/en/cli-reference>
  - Source: <https://code.claude.com/docs/en/common-workflows>
- **Cursor** documents headless/CLI surfaces separately from the interactive Agent product.
  - Source: <https://cursor.com/docs/cli/headless.md>
  - Source: <https://cursor.com/docs/cli/reference/parameters.md>

**Confidence:** High

### Permission, Sandbox, and Safety Controls

- **Codex** documents sandbox modes and approval policies (`read-only`, `workspace-write`, `danger-full-access`), plus security defaults.
  - Source: <https://developers.openai.com/codex/agent-approvals-security>
  - Source: <https://developers.openai.com/codex/permissions>
- **Claude Code** documents permission modes and policy controls (`--permission-mode`, deny/allow/ask rules, managed settings precedence).
  - Source: <https://code.claude.com/docs/en/settings>
  - Source: <https://code.claude.com/docs/en/cli-reference>
- **Cursor** documents Agent security behavior, approval requirements for sensitive actions, terminal run modes, MCP approval controls, and network restrictions.
  - Source: <https://cursor.com/docs/agent/security.md>

**Confidence:** High

### Prompting and Context Guidance Framing

- **Codex** best-practices documentation recommends structuring prompts with:
  - Goal
  - Context
  - Constraints
  - Done criteria
  - Source: <https://developers.openai.com/codex/learn/best-practices>
- **Claude Code** documentation emphasizes operational workflows and mode/tool controls, including plan mode, permission modes, subagents, settings layers, and system-prompt customization flags.
  - Source: <https://code.claude.com/docs/en/common-workflows>
  - Source: <https://code.claude.com/docs/en/cli-reference>
  - Source: <https://code.claude.com/docs/en/settings>
- **Cursor** rules documentation recommends focused, actionable, scoped rules, and warns against copying entire style guides or documenting every possible command.
  - Source: <https://cursor.com/docs/rules.md>

**Confidence:** High

## What This Means for Our Prompt Generator

### Confirmed Design Implications

1. We should keep a **shared core prompt** across agents.

Reason: all three products are coding agents with overlapping coding-task surfaces.

Confidence: High

2. We should add **agent-specific overlays** instead of completely different templates.

Reason: the agents share broad coding capabilities, but expose different controls, persistent instruction surfaces, and operational defaults.

Confidence: Medium

3. We should support **agent-native output artifacts**, not only one pasted prompt.

Reason: Cursor has first-class `.cursor/rules/*.mdc` and `AGENTS.md`; Claude Code has `CLAUDE.md` and settings; Codex has CLI and automation-oriented prompt surfaces.

Confidence: High

4. We should always include **execution contract fields** in generated task prompts.

Fields:

- objective
- constraints
- done criteria
- verification commands

Reason: explicitly aligned with Codex best-practices structure and compatible with Claude/Cursor workflow docs.

Confidence: High

5. We should tune **verbosity and control instructions** per agent via measured outcomes, not assumptions.

Reason: docs describe capabilities and controls, not a universal best prompt length rule.

Confidence: Medium

## Agent-Specific Optimization Checklist (v1)

### Codex-Targeted Additions

- Include explicit Goal/Context/Constraints/Done sections.
  - Source: <https://developers.openai.com/codex/learn/best-practices>
- Include safe execution assumptions for automation contexts.
  - Source: <https://developers.openai.com/codex/agent-approvals-security>
  - Source: <https://developers.openai.com/codex/noninteractive>
- When used in CI-like flows, prefer machine-readable output requirements.
  - Source: <https://developers.openai.com/codex/noninteractive>

### Claude Code-Targeted Additions

- Include explicit permission and mode expectations where relevant.
  - Source: <https://code.claude.com/docs/en/common-workflows>
  - Source: <https://code.claude.com/docs/en/cli-reference>
- Include project-level instruction placement guidance (`CLAUDE.md`, settings scope awareness) when integrating into teams.
  - Source: <https://code.claude.com/docs/en/settings>
- Use append-style system instruction strategy when preserving default coding assistant behavior.
  - Source: <https://code.claude.com/docs/en/cli-reference>

### Cursor-Targeted Additions

- Prefer `.cursor/rules/*.mdc` for reusable project rules that need metadata, globs, or always-apply behavior.
  - Source: <https://cursor.com/docs/rules.md>
- Prefer `AGENTS.md` for simple plain-Markdown project instructions.
  - Source: <https://cursor.com/docs/rules.md>
- Keep Cursor rules focused, actionable, and scoped; reference files instead of copying large guides.
  - Source: <https://cursor.com/docs/rules.md>
- Make approval-sensitive terminal, MCP, network, or configuration actions explicit.
  - Source: <https://cursor.com/docs/agent/security.md>

## Surface Strategy

| Agent | Best default output | Native artifact support to add |
| --- | --- | --- |
| Codex | Markdown task prompt | automation-oriented prompt with explicit verification/output requirements |
| Claude Code | Markdown task prompt | `CLAUDE.md` or append-style instruction guidance |
| Cursor | Markdown task prompt or project rule | `.cursor/rules/*.mdc` and `AGENTS.md` |

## Claims We Should Not State Without Testing

These are common beliefs but not directly guaranteed by the sources above:

- "Codex always needs shorter prompts than Claude Code."
- "Claude Code always benefits from longer reasoning instructions."
- "Cursor is universally better for UI tasks."
- "One agent is universally better for refactor/debug/test tasks."

Status: treat as **hypotheses** and validate empirically.

## Suggested Measurement Plan

To prove optimization quality by target agent, track:

1. first-pass success rate
2. first-pass lint/test pass rate
3. number of follow-up turns to completion
4. diff scope accuracy (requested scope vs changed files)
5. rollback/rework rate after review
6. prompt/artifact size vs task success

This is the evidence loop needed before hard-coding stronger agent-specific assumptions.

## Source Index

### Codex

- <https://developers.openai.com/codex/>
- <https://developers.openai.com/codex/quickstart>
- <https://developers.openai.com/codex/learn/best-practices>
- <https://developers.openai.com/codex/noninteractive>
- <https://developers.openai.com/codex/agent-approvals-security>
- <https://developers.openai.com/codex/permissions>
- <https://developers.openai.com/codex/cli/reference>
- <https://github.com/openai/codex>

### Claude Code

- <https://code.claude.com/docs/en/overview>
- <https://code.claude.com/docs/en/common-workflows>
- <https://code.claude.com/docs/en/settings>
- <https://code.claude.com/docs/en/cli-reference>

### Cursor

- <https://cursor.com/docs/agent/overview.md>
- <https://cursor.com/docs/rules.md>
- <https://cursor.com/docs/agent/security.md>
- <https://cursor.com/docs/cli/headless.md>
- <https://cursor.com/docs/cli/reference/parameters.md>
