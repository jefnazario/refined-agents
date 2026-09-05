from __future__ import annotations

import argparse
from dataclasses import dataclass
import os
from pathlib import Path
from typing import Iterable
import re
from urllib.request import urlopen

try:
    from dynaconf import Dynaconf
except ModuleNotFoundError:  # pragma: no cover - fallback path for non-project execution
    Dynaconf = None  # type: ignore[assignment]

FRONT_MATTER_RE = re.compile(r"^\s*---\s*\n(.*?)\n---\s*\n", re.DOTALL)
APP_DIR = Path(__file__).resolve().parent


class FallbackSettings:
    """Small fallback settings reader when dynaconf is unavailable.

    Reads [default] keys from settings.toml and allows env var overrides
    using the REFINED_AGENTS_<KEY> convention.
    """

    def __init__(self, file_path: Path, env_prefix: str = "REFINED_AGENTS") -> None:
        self._values: dict[str, str] = {}
        self._env_prefix = env_prefix
        self._load_file(file_path)

    def _load_file(self, file_path: Path) -> None:
        if not file_path.exists():
            return
        try:
            import tomllib

            raw = tomllib.loads(file_path.read_text(encoding="utf-8"))
            default_section = raw.get("default", {})
            if isinstance(default_section, dict):
                for key, value in default_section.items():
                    self._values[str(key)] = str(value)
        except Exception:
            return

    def get(self, key: str, default: object | None = None) -> object | None:
        env_key = f"{self._env_prefix}_{key}".upper()
        if env_key in os.environ:
            return os.environ[env_key]
        return self._values.get(key, default)

if Dynaconf is not None:
    settings = Dynaconf(
        envvar_prefix="REFINED_AGENTS",
        settings_files=[APP_DIR / "settings.toml", APP_DIR / ".secrets.toml"],
        environments=True,
        load_dotenv=True,
    )
else:
    settings = FallbackSettings(APP_DIR / "settings.toml")


def _default_prompts_root() -> Path:
    configured_root = settings.get("prompts_root", "prompts")
    root_path = Path(str(configured_root))
    if root_path.is_absolute():
        return root_path
    return APP_DIR / root_path


DEFAULT_PROMPTS_ROOT = _default_prompts_root()
PROJECT_CONTEXT_FILE = "000_project_context.md"


@dataclass(frozen=True)
class TaskPreset:
    name: str
    mode: str | None
    tags: set[str]
    exclude_tags: set[str]
    description: str


TASK_PRESETS: dict[str, TaskPreset] = {
    "api": TaskPreset(
        name="api",
        mode="api",
        tags={"api", "backend"},
        exclude_tags={"data_pipeline", "refactor", "bugfix", "test"},
        description="Design and implement an API service or endpoint.",
    ),
    "backend": TaskPreset(
        name="backend",
        mode="backend",
        tags={"backend"},
        exclude_tags={"data_pipeline", "refactor", "bugfix", "test"},
        description="Implement backend/service layer logic.",
    ),
    "data_pipeline": TaskPreset(
        name="data_pipeline",
        mode="data_pipeline",
        tags={"data_pipeline"},
        exclude_tags={"api", "backend", "refactor", "bugfix", "test"},
        description="Build or update a deterministic data pipeline.",
    ),
    "bugfix": TaskPreset(
        name="bugfix",
        mode="bugfix",
        tags={"bugfix"},
        exclude_tags={"api", "backend", "data_pipeline", "refactor", "test"},
        description="Fix an existing bug with minimal, safe changes.",
    ),
    "refactor": TaskPreset(
        name="refactor",
        mode="refactor",
        tags={"refactor"},
        exclude_tags={"api", "backend", "data_pipeline", "bugfix", "test"},
        description="Refactor code without changing behavior.",
    ),
    "test_generation": TaskPreset(
        name="test_generation",
        mode="test_generation",
        tags={"test"},
        exclude_tags={"api", "backend", "data_pipeline", "refactor", "bugfix"},
        description="Generate or extend tests for behavior coverage.",
    ),
    "fullstack": TaskPreset(
        name="fullstack",
        mode="fullstack",
        tags={"api", "backend"},
        exclude_tags={"data_pipeline", "refactor", "bugfix", "test"},
        description="Design and implement a complete full-stack web application (frontend + backend + UI + real-time/database).",
    ),
}


@dataclass(frozen=True)
class AgentProfile:
    name: str
    tag: str
    display_name: str
    aliases: tuple[str, ...]
    description: str


AGENT_PROFILES: dict[str, AgentProfile] = {
    "codex": AgentProfile(
        name="codex",
        tag="codex",
        display_name="Codex",
        aliases=("codex", "openai-codex", "openai codex"),
        description="OpenAI Codex coding agent surfaces, including app, CLI, IDE, and automation use.",
    ),
    "claude-code": AgentProfile(
        name="claude-code",
        tag="claude_code",
        display_name="Claude Code",
        aliases=("claude-code", "claude_code", "claude", "anthropic-claude-code"),
        description="Claude Code terminal, IDE, desktop, and browser coding workflows.",
    ),
    "cursor": AgentProfile(
        name="cursor",
        tag="cursor",
        display_name="Cursor",
        aliases=("cursor", "cursor-agent", "cursor agent"),
        description="Cursor Agent and Cursor-native rules such as .cursor/rules/*.mdc and AGENTS.md.",
    ),
}

AGENT_ALIASES: dict[str, str] = {
    alias: name for name, profile in AGENT_PROFILES.items() for alias in profile.aliases
}
AGENT_TAGS = {profile.tag for profile in AGENT_PROFILES.values()}
LANGUAGE_TAGS = {"python", "rust"}


def _normalize_agent(agent: str) -> AgentProfile:
    normalized = agent.strip().lower()
    profile_name = AGENT_ALIASES.get(normalized, normalized)
    if profile_name not in AGENT_PROFILES:
        known = ", ".join(sorted(AGENT_PROFILES))
        raise ValueError(f"Unknown agent '{agent}'. Expected one of: {known}")
    return AGENT_PROFILES[profile_name]


@dataclass(frozen=True)
class PromptChunk:
    path: Path
    priority: int
    tags: set[str]
    content: str


@dataclass(frozen=True)
class PriorityTier:
    """A band of priorities rendered under a shared heading.

    Chunks are placed in the first tier whose ``max_priority`` is >= the
    chunk priority. The heading and blurb make importance an explicit signal
    the receiving agent can read, instead of being implied only by ordering.
    """

    max_priority: int
    heading: str
    blurb: str


# Ordered from highest importance (lowest priority numbers) to lowest.
# The final tier uses a very large bound to catch everything remaining.
PRIORITY_TIERS: tuple[PriorityTier, ...] = (
    PriorityTier(
        max_priority=34,
        heading="Non-Negotiable Rules",
        blurb="These rules take precedence. Follow them exactly; do not override them with anything below.",
    ),
    PriorityTier(
        max_priority=69,
        heading="Core Guidelines",
        blurb="Strong defaults for how to carry out the work. Apply unless a non-negotiable rule above conflicts.",
    ),
    PriorityTier(
        max_priority=10**9,
        heading="Supplementary Guidance",
        blurb="Context-specific and stylistic guidance. Use where it applies.",
    ),
)


def _tier_for_priority(priority: int) -> PriorityTier:
    for tier in PRIORITY_TIERS:
        if priority <= tier.max_priority:
            return tier
    return PRIORITY_TIERS[-1]


# Chunks carrying this tag are recapped at the very end of the prompt so the
# most critical rules get recency weight in addition to their primacy position,
# countering the "lost in the middle" effect in long prompts.
RECAP_TAG = "critical"


def _section_headings(content: str) -> list[str]:
    """Top-level (`# `) section titles of a chunk, minus its own title."""
    headings = [
        line[2:].strip() for line in content.splitlines() if line.startswith("# ")
    ]
    return headings[1:] if headings else []


def _build_critical_recap(chunks: list[PromptChunk]) -> str:
    items: list[str] = []
    for c in chunks:
        for heading in _section_headings(c.content):
            if heading not in items:
                items.append(heading)

    if not items:
        return ""

    checklist = "\n".join(f"- {item}" for item in items)
    return (
        "## Non-Negotiable Rules — Final Reminder\n\n"
        "_Before finalizing, re-verify the work against the non-negotiable rules "
        "stated earlier. They override everything below them. At minimum, confirm "
        "each of these holds:_\n\n"
        f"{checklist}"
    )

def _parse_front_matter(md_text: str) -> tuple[dict, str]:
    """
    Minimal front-matter parser (YAML-ish without dependencies).
    Supports:
      priority: 10
      tags: [a, b]
    """
    m = FRONT_MATTER_RE.match(md_text)
    if not m:
        return {}, md_text.strip()

    fm_raw = m.group(1)
    body = md_text[m.end():].strip()

    meta: dict = {}
    for line in fm_raw.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" not in line:
            continue
        k, v = [x.strip() for x in line.split(":", 1)]
        if k == "priority":
            meta["priority"] = int(v)
        elif k == "tags":
            # supports tags: [a, b]
            v = v.strip()
            if v.startswith("[") and v.endswith("]"):
                items = [x.strip() for x in v[1:-1].split(",") if x.strip()]
                meta["tags"] = items
            else:
                meta["tags"] = [v]
        else:
            meta[k] = v
    return meta, body

def load_chunks(*folders: str, root: str | Path = DEFAULT_PROMPTS_ROOT) -> list[PromptChunk]:
    root_path = Path(root)
    chunks: list[PromptChunk] = []

    for folder in folders:
        p = root_path / folder
        if not p.exists():
            continue
        for file in sorted(p.rglob("*.md")):
            text = file.read_text(encoding="utf-8")
            meta, body = _parse_front_matter(text)

            priority = meta.get("priority")
            if priority is None:
                # fallback: infer from filename prefix "010_..."
                prefix = file.stem.split("_", 1)[0]
                priority = int(prefix) if prefix.isdigit() else 1000

            tags = set(meta.get("tags", []))
            chunks.append(PromptChunk(path=file, priority=priority, tags=tags, content=body))

    chunks.sort(key=lambda c: (c.priority, c.path.name))
    return chunks


def _extract_mode_from_path(path: Path) -> str | None:
    parts = path.parts
    if "modes" not in parts:
        return None

    idx = parts.index("modes")
    if idx + 1 >= len(parts):
        return None
    return parts[idx + 1]


def _chunk_matches_tags(
    *,
    chunk_tags: set[str],
    include: set[str],
    exclude: set[str],
) -> bool:
    if not chunk_tags:
        return True

    if chunk_tags & exclude:
        return False

    for exclusive_group in (LANGUAGE_TAGS, AGENT_TAGS):
        chunk_group_tags = chunk_tags & exclusive_group
        if chunk_group_tags and not (chunk_group_tags & include):
            return False

    return not include or bool(chunk_tags & include)


def build_system_prompt(
    include_tags: Iterable[str] = ("always",),
    exclude_tags: Iterable[str] = (),
    mode: str | None = None,
    root: str | Path = DEFAULT_PROMPTS_ROOT,
    project_context_content: str | None = None,
    tiered: bool = True,
    reinforce_critical: bool = True,
) -> str:
    include = set(include_tags)
    exclude = set(exclude_tags)

    chunks = load_chunks("system", root=root)

    preamble: list[str] = []

    if project_context_content:
        preamble.append(
            "<!-- external/project_context.md -->\n" + project_context_content.strip()
        )

    # Collect matching chunks, preserving the priority/name sort from load_chunks.
    matched: list[PromptChunk] = []
    for c in chunks:
        # Project context is injected only when explicitly provided by the user.
        if c.path.name == PROJECT_CONTEXT_FILE:
            continue

        chunk_mode = _extract_mode_from_path(c.path)

        # Exclude mode chunks unless a mode was requested.
        if mode is None and chunk_mode is not None:
            continue
        if mode is not None and chunk_mode is not None and chunk_mode != mode:
            continue

        if not _chunk_matches_tags(chunk_tags=c.tags, include=include, exclude=exclude):
            continue

        matched.append(c)

    def render_chunk(c: PromptChunk) -> str:
        rel_path = c.path.relative_to(Path(root))
        return f"<!-- {rel_path.as_posix()} -->\n{c.content}"

    # Recap of critical chunks, appended last so it lands in the high-attention
    # end zone of the prompt (just above the task/objective in build_agent_prompt).
    recap = ""
    if reinforce_critical:
        recap = _build_critical_recap([c for c in matched if RECAP_TAG in c.tags])

    if not tiered:
        selected = preamble + [render_chunk(c) for c in matched]
        if recap:
            selected.append(recap)
        return "\n\n".join(selected).strip()

    # Group matched chunks into priority tiers so importance is an explicit,
    # readable signal rather than just implied by ordering.
    sections: list[str] = list(preamble)
    for tier in PRIORITY_TIERS:
        tier_chunks = [c for c in matched if _tier_for_priority(c.priority) is tier]
        if not tier_chunks:
            continue
        body = "\n\n".join(render_chunk(c) for c in tier_chunks)
        sections.append(f"## {tier.heading}\n\n_{tier.blurb}_\n\n{body}")

    if recap:
        sections.append(recap)

    return "\n\n".join(sections).strip()


def _build_execution_brief(
    *,
    agent: AgentProfile,
    language: str,
    task: str,
    objective: str,
    framework: str | None,
    extra_context: str | None,
) -> str:
    lines = [
        "# Execution Brief",
        f"- Target coding agent: {agent.display_name}",
        f"- Primary language: {language}",
        f"- Task type: {task}",
    ]

    if framework:
        lines.append(f"- Framework/stack: {framework}")

    lines.extend(
        [
            "",
            "## Objective",
            objective.strip(),
            "",
        ]
    )

    if extra_context:
        lines.extend(["## Extra Context", extra_context.strip(), ""])

    lines.extend(
        [
            "## Output Requirements",
            "- Produce production-ready code and tests when applicable.",
            "- Keep changes minimal and aligned with existing architecture.",
            "- Explain important tradeoffs and assumptions briefly.",
        ]
    )

    return "\n".join(lines).strip()


def _load_project_context(
    *,
    project_context_path: str | None,
    project_context_url: str | None,
) -> str | None:
    if not project_context_path and not project_context_url:
        return None

    if project_context_path:
        p = Path(project_context_path)
        if not p.is_absolute():
            p = Path.cwd() / p
        if not p.exists():
            raise ValueError(f"Project context file not found: {p}")
        return p.read_text(encoding="utf-8").strip()

    assert project_context_url is not None
    with urlopen(project_context_url, timeout=20) as response:
        charset = response.headers.get_content_charset() or "utf-8"
        return response.read().decode(charset).strip()


def build_agent_prompt(
    *,
    agent: str,
    language: str,
    task: str,
    objective: str,
    framework: str | None = None,
    extra_context: str | None = None,
    root: str | Path = DEFAULT_PROMPTS_ROOT,
    project_context_path: str | None = None,
    project_context_url: str | None = None,
) -> str:
    profile = _normalize_agent(agent)
    if task not in TASK_PRESETS:
        known = ", ".join(sorted(TASK_PRESETS))
        raise ValueError(f"Unknown task '{task}'. Expected one of: {known}")

    preset = TASK_PRESETS[task]
    include_tags = {"always", profile.tag, language, *preset.tags}
    project_context = _load_project_context(
        project_context_path=project_context_path,
        project_context_url=project_context_url,
    )

    system_prompt = build_system_prompt(
        include_tags=include_tags,
        exclude_tags=preset.exclude_tags,
        mode=preset.mode,
        root=root,
        project_context_content=project_context,
    )

    brief = _build_execution_brief(
        agent=profile,
        language=language,
        task=task,
        objective=objective,
        framework=framework,
        extra_context=extra_context,
    )

    header = "\n".join(
        [
            "# Prompt For Coding Agent",
            "",
            f"This prompt is tailored for {profile.display_name}.",
            f"Task preset: {preset.name} ({preset.description})",
            "",
        ]
    )

    parts = [header, system_prompt, brief]
    return "\n\n".join(part for part in parts if part).strip() + "\n"


def build_cursor_rule(
    *,
    prompt: str,
    description: str | None = None,
    globs: str | None = None,
    always_apply: bool = False,
) -> str:
    front_matter = ["---"]
    if description:
        escaped = description.replace('"', '\\"')
        front_matter.append(f'description: "{escaped}"')
    if globs:
        front_matter.append(f"globs: {globs}")
    front_matter.append(f"alwaysApply: {'true' if always_apply else 'false'}")
    front_matter.append("---")

    return "\n".join(front_matter) + "\n\n" + prompt.strip() + "\n"


def build_agents_md(prompt: str) -> str:
    return "# Project Agent Instructions\n\n" + prompt.strip() + "\n"


def _prompt_text(prompt: str, default: str | None = None) -> str:
    if default:
        raw = input(f"{prompt} [{default}]: ").strip()
        return raw or default
    return input(f"{prompt}: ").strip()


def _interactive_args() -> argparse.Namespace:
    task_choices = ", ".join(sorted(TASK_PRESETS))
    agent_choices = ", ".join(sorted(AGENT_PROFILES))
    agent = _prompt_text(
        f"Target agent ({agent_choices})", str(settings.get("agent", "codex"))
    )
    language = _prompt_text(
        "Language (python|rust)", str(settings.get("language", "python"))
    ).lower()
    task = _prompt_text(f"Task ({task_choices})", str(settings.get("task", "api"))).lower()
    framework = _prompt_text("Framework (optional)", "") or None
    objective = _prompt_text("Task objective")
    extra_context = _prompt_text("Extra context (optional)", "") or None
    project_context_path = _prompt_text("Project context file path (optional)", "") or None
    project_context_url = None
    if not project_context_path:
        project_context_url = _prompt_text("Project context URL (optional)", "") or None
    output = _prompt_text("Output file (optional)", "") or None

    return argparse.Namespace(
        agent=agent,
        language=language,
        task=task,
        framework=framework,
        objective=objective,
        extra_context=extra_context,
        project_context_path=project_context_path,
        project_context_url=project_context_url,
        output=output,
        output_format="prompt",
        cursor_rule_type="always",
        cursor_globs=None,
        cursor_description=None,
        root=str(DEFAULT_PROMPTS_ROOT),
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build a prompt for coding agents (Codex, Claude Code, Goose, etc)."
    )
    parser.add_argument(
        "--agent",
        default=str(settings.get("agent", "codex")),
        help=(
            "Target coding agent name. Known agents: "
            + ", ".join(sorted(AGENT_PROFILES.keys()))
        ),
    )
    parser.add_argument(
        "--language",
        choices=["python", "rust"],
        default=str(settings.get("language", "python")),
        help="Primary implementation language.",
    )
    parser.add_argument(
        "--task",
        choices=sorted(TASK_PRESETS.keys()),
        default=str(settings.get("task", "api")),
        help="Type of engineering task.",
    )
    parser.add_argument(
        "--framework",
        default=settings.get("framework"),
        help="Optional framework (e.g., fastapi).",
    )
    parser.add_argument("--objective", help="Natural language task objective.")
    parser.add_argument(
        "--extra-context",
        default=settings.get("extra_context"),
        help="Additional context for the agent.",
    )
    ctx_group = parser.add_mutually_exclusive_group()
    ctx_group.add_argument(
        "--project-context-path",
        default=settings.get("project_context_path") or None,
        help="Path to a project-specific context markdown file.",
    )
    ctx_group.add_argument(
        "--project-context-url",
        default=settings.get("project_context_url") or None,
        help="URL to download a project-specific context markdown file.",
    )
    parser.add_argument("--output", help="Output file path to save the generated prompt.")
    parser.add_argument(
        "--format",
        dest="output_format",
        choices=["prompt", "cursor-rule", "agents-md"],
        default="prompt",
        help="Output artifact format.",
    )
    parser.add_argument(
        "--cursor-rule-type",
        choices=["always", "intelligent", "files", "manual"],
        default="always",
        help="Cursor .mdc rule application style when --format cursor-rule is used.",
    )
    parser.add_argument(
        "--cursor-globs",
        help="Comma-separated Cursor glob patterns for --cursor-rule-type files.",
    )
    parser.add_argument(
        "--cursor-description",
        help="Cursor rule description for intelligent or documented project rules.",
    )
    parser.add_argument(
        "--root",
        default=str(_default_prompts_root()),
        help="Prompts root folder. Defaults to refined_agents/prompts.",
    )
    parser.add_argument(
        "--interactive",
        action="store_true",
        help="Ask questions interactively in the terminal.",
    )

    args = parser.parse_args()
    if args.interactive:
        return _interactive_args()

    try:
        _normalize_agent(args.agent)
    except ValueError as exc:
        parser.error(str(exc))

    missing = [name for name in ("language", "task", "objective") if not getattr(args, name)]
    if missing:
        parser.error(
            "Missing required arguments when not interactive: "
            + ", ".join(f"--{name.replace('_', '-')}" for name in missing)
        )
    return args


def main() -> None:
    args = parse_args()
    prompt = build_agent_prompt(
        agent=args.agent,
        language=args.language,
        task=args.task,
        objective=args.objective,
        framework=args.framework,
        extra_context=args.extra_context,
        root=args.root,
        project_context_path=args.project_context_path,
        project_context_url=args.project_context_url,
    )
    output_text = prompt
    if args.output_format == "cursor-rule":
        if _normalize_agent(args.agent).name != "cursor":
            raise ValueError("--format cursor-rule requires --agent cursor")
        output_text = build_cursor_rule(
            prompt=prompt,
            description=args.cursor_description,
            globs=args.cursor_globs if args.cursor_rule_type == "files" else None,
            always_apply=args.cursor_rule_type == "always",
        )
    elif args.output_format == "agents-md":
        output_text = build_agents_md(prompt)

    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(output_text, encoding="utf-8")
        print(f"Prompt written to {output_path}")
        return

    print(output_text)


if __name__ == "__main__":
    main()
