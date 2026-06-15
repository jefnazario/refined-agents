from __future__ import annotations

import unittest

import refined_agents
from refined_agents.create_prompts import (
    build_agent_prompt,
    build_agents_md,
    build_cursor_rule,
)


class AgentPromptTests(unittest.TestCase):
    def test_public_api_exports_prompt_builder(self) -> None:
        self.assertIs(refined_agents.build_agent_prompt, build_agent_prompt)

    def test_cursor_prompt_includes_cursor_overlay_only(self) -> None:
        prompt = build_agent_prompt(
            agent="cursor",
            language="python",
            task="backend",
            objective="Add a service layer.",
        )

        self.assertIn("# Cursor Agent Overlay", prompt)
        self.assertNotIn("# Codex Agent Overlay", prompt)
        self.assertNotIn("# Claude Code Agent Overlay", prompt)
        self.assertIn("- Target coding agent: Cursor", prompt)

    def test_codex_prompt_includes_codex_overlay_only(self) -> None:
        prompt = build_agent_prompt(
            agent="codex",
            language="python",
            task="api",
            objective="Add a customer API.",
        )

        self.assertIn("# Codex Agent Overlay", prompt)
        self.assertNotIn("# Cursor Agent Overlay", prompt)
        self.assertNotIn("# Claude Code Agent Overlay", prompt)
        self.assertIn("- Target coding agent: Codex", prompt)

    def test_language_tags_do_not_leak_through_always_tag(self) -> None:
        prompt = build_agent_prompt(
            agent="claude-code",
            language="rust",
            task="refactor",
            objective="Refactor parser module safely.",
        )

        self.assertIn("Rust Engineering Rules", prompt)
        self.assertNotIn("Python Engineering Rules", prompt)

    def test_cursor_rule_output_has_mdc_front_matter(self) -> None:
        output = build_cursor_rule(
            prompt="# Prompt\n\nDo the work.",
            description="Python backend service conventions",
            globs="src/**/*.py,tests/**/*.py",
            always_apply=False,
        )

        self.assertTrue(output.startswith("---\n"))
        self.assertIn('description: "Python backend service conventions"', output)
        self.assertIn("globs: src/**/*.py,tests/**/*.py", output)
        self.assertIn("alwaysApply: false", output)
        self.assertTrue(output.endswith("\n"))

    def test_agents_md_output_is_plain_markdown(self) -> None:
        output = build_agents_md("# Prompt\n\nDo the work.")

        self.assertTrue(output.startswith("# Project Agent Instructions\n\n"))
        self.assertNotIn("alwaysApply:", output)
        self.assertTrue(output.endswith("\n"))


if __name__ == "__main__":
    unittest.main()
