from __future__ import annotations

import unittest

import refined_agents
from refined_agents.create_prompts import (
    build_agent_prompt,
    build_agents_md,
    build_cursor_rule,
    build_system_prompt,
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
        self.assertNotIn("C# & .NET Engineering Rules", prompt)
        self.assertNotIn("Vue.js & Frontend Engineering Rules", prompt)

    def test_csharp_prompt_includes_csharp_rules_only(self) -> None:
        prompt = build_agent_prompt(
            agent="codex",
            language="csharp",
            task="backend",
            objective="Implement appointment booking module.",
        )

        self.assertIn("C# & .NET Engineering Rules", prompt)
        self.assertIn("Rich Domain Model & Encapsulation", prompt)
        self.assertNotIn("Python Engineering Rules", prompt)
        self.assertNotIn("Rust Engineering Rules", prompt)
        self.assertNotIn("Vue.js & Frontend Engineering Rules", prompt)

    def test_vue_prompt_includes_vue_rules_only(self) -> None:
        prompt = build_agent_prompt(
            agent="codex",
            language="vue",
            task="fullstack",
            objective="Create customer dashboard with Composition API.",
        )

        self.assertIn("Vue.js & Frontend Engineering Rules", prompt)
        self.assertIn("Separation of Concerns & Component Purity", prompt)
        self.assertNotIn("Python Engineering Rules", prompt)
        self.assertNotIn("Rust Engineering Rules", prompt)
        self.assertNotIn("C# & .NET Engineering Rules", prompt)

    def test_vuejs_alias_supported(self) -> None:
        prompt = build_agent_prompt(
            agent="cursor",
            language="vuejs",
            task="fullstack",
            objective="Create user profile view.",
        )

        self.assertIn("Vue.js & Frontend Engineering Rules", prompt)
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

    def test_tiered_prompt_emits_priority_headings(self) -> None:
        prompt = build_system_prompt(
            include_tags=("always", "python", "backend"), mode="backend"
        )

        self.assertIn("## Non-Negotiable Rules", prompt)
        self.assertIn("## Core Guidelines", prompt)
        # Non-negotiable section must come before core guidelines.
        self.assertLess(
            prompt.index("## Non-Negotiable Rules"),
            prompt.index("## Core Guidelines"),
        )

    def test_tiered_can_be_disabled(self) -> None:
        prompt = build_system_prompt(
            include_tags=("always", "python", "backend"),
            mode="backend",
            tiered=False,
        )

        # The tier section heading + blurb must be gone...
        self.assertNotIn("These rules take precedence", prompt)
        self.assertNotIn("## Core Guidelines", prompt)

    def test_critical_recap_appears_in_end_zone(self) -> None:
        prompt = build_agent_prompt(
            agent="claude-code",
            language="python",
            task="backend",
            objective="Add a service layer.",
        )

        self.assertIn("## Non-Negotiable Rules — Final Reminder", prompt)
        # Recap must sit after the rules themselves but before the objective.
        self.assertLess(
            prompt.index("## Non-Negotiable Rules\n"),
            prompt.index("Final Reminder"),
        )
        self.assertLess(
            prompt.index("Final Reminder"),
            prompt.index("## Objective"),
        )
        # Recap is a compact checklist, not a duplicate of the full rules.
        self.assertIn("- Security — Hard Rules", prompt)

    def test_critical_recap_can_be_disabled(self) -> None:
        prompt = build_system_prompt(
            include_tags=("always", "python", "backend"),
            mode="backend",
            reinforce_critical=False,
        )

        self.assertNotIn("Final Reminder", prompt)

    def test_agents_md_output_is_plain_markdown(self) -> None:
        output = build_agents_md("# Prompt\n\nDo the work.")

        self.assertTrue(output.startswith("# Project Agent Instructions\n\n"))
        self.assertNotIn("alwaysApply:", output)
        self.assertTrue(output.endswith("\n"))


if __name__ == "__main__":
    unittest.main()
