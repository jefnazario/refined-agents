from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable
import re

FRONT_MATTER_RE = re.compile(r"^\s*---\s*\n(.*?)\n---\s*\n", re.DOTALL)

@dataclass(frozen=True)
class PromptChunk:
    path: Path
    priority: int
    tags: set[str]
    content: str

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

def load_chunks(*folders: str, root: str = "agents/prompts") -> list[PromptChunk]:
    root_path = Path(root)
    chunks: list[PromptChunk] = []

    for folder in folders:
        p = root_path / folder
        for file in sorted(p.glob("*.md")):
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

def build_system_prompt(
    include_tags: Iterable[str] = ("always",),
    exclude_tags: Iterable[str] = (),
    mode: str | None = None,
) -> str:
    include = set(include_tags)
    exclude = set(exclude_tags)

    folders = ["system", "tools"]
    if mode:
        folders.append("modes")

    chunks = load_chunks(*folders)

    selected: list[str] = []
    for c in chunks:
        # Modes: only include mode file if it matches requested mode
        if c.path.parent.name == "modes" and mode and c.path.stem != mode:
            continue

        # Tag rules:
        # - if a chunk has no tags, include it by default (optional; you can change this)
        if c.tags:
            if c.tags & exclude:
                continue
            if include and not (c.tags & include):
                continue

        selected.append(f"<!-- {c.path.parent.name}/{c.path.name} -->\n{c.content}")

    return "\n\n".join(selected).strip()
