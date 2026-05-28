from pathlib import Path

from minicodeagent import FakeModelClient, MiniAgent, SessionStore, WorkspaceContext
from minicodeagent.skills import discover_skills, render_skill_summaries


def build_agent(tmp_path, outputs=None):
    (tmp_path / "README.md").write_text("demo\n", encoding="utf-8")
    return MiniAgent(
        model_client=FakeModelClient(outputs or []),
        workspace=WorkspaceContext.build(tmp_path),
        session_store=SessionStore(tmp_path / ".minicodeagent" / "sessions"),
        approval_policy="auto",
    )


def write_skill(root, slug, text):
    path = root / "skills" / slug / "SKILL.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


def test_discovers_skill_frontmatter_and_ignores_invalid_entries(tmp_path):
    write_skill(
        tmp_path,
        "code-review",
        """---
name: code-review
description: Review code for bugs, regressions, and missing tests.
---

# Code Review
""",
    )
    write_skill(
        tmp_path,
        "broken",
        """---
name:
description:
---
""",
    )

    skills = discover_skills(tmp_path)

    assert [skill.name for skill in skills] == ["code-review"]
    assert skills[0].slug == "code-review"
    assert skills[0].description == "Review code for bugs, regressions, and missing tests."
    assert skills[0].path == Path(tmp_path / "skills" / "code-review" / "SKILL.md")


def test_renders_skill_summaries_for_prompt(tmp_path):
    write_skill(
        tmp_path,
        "repo-summary",
        """---
name: repo-summary
description: Summarize the repository architecture and entry points.
---
""",
    )

    text = render_skill_summaries(discover_skills(tmp_path))

    assert text == "Skills:\n- repo-summary: Summarize the repository architecture and entry points."


def test_agent_prompt_includes_local_skill_summaries(tmp_path):
    write_skill(
        tmp_path,
        "test-fix",
        """---
name: test-fix
description: Diagnose failing tests before changing implementation.
---
""",
    )
    agent = build_agent(tmp_path)

    prompt = agent.prompt("Fix the failing test")

    assert "Skills:" in prompt
    assert "- test-fix: Diagnose failing tests before changing implementation." in prompt
    assert agent.last_prompt_metadata["skill_count"] == 1
    assert agent.last_prompt_metadata["skill_names"] == ["test-fix"]
