"""Interview demo task templates."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class DemoTask:
    name: str
    title: str
    skill: str
    prompt: str
    talking_points: tuple[str, ...]


DEMO_TASKS = (
    DemoTask(
        name="code-review",
        title="Review a focused code change",
        skill="code-review",
        prompt="Review the latest local changes for bugs, risky behavior, and missing tests. Return concrete findings first.",
        talking_points=(
            "Shows local skill activation for code review.",
            "Demonstrates safe read/search-first behavior.",
            "Pairs well with `minicodeagent report latest` to explain tools and safety events.",
        ),
    ),
    DemoTask(
        name="test-fix",
        title="Diagnose and fix a failing test",
        skill="test-fix",
        prompt="Run the focused failing test, diagnose the failure from its output, make the smallest fix, and rerun the test.",
        talking_points=(
            "Shows test-first debugging discipline.",
            "Exercises shell execution plus patch/write tools.",
            "Makes the run report useful because files modified and tool statuses are visible.",
        ),
    ),
    DemoTask(
        name="repo-summary",
        title="Explain repository architecture",
        skill="repo-summary",
        prompt="Summarize this repository's architecture, main entry points, runtime flow, and extension points for an interview.",
        talking_points=(
            "Shows the agent can inspect and explain an unfamiliar codebase.",
            "Activates the repo-summary skill without modifying files.",
            "Good first demo when network or provider access is uncertain.",
        ),
    ),
)


def demo_by_name(name):
    for demo in DEMO_TASKS:
        if demo.name == name:
            return demo
    return None


def format_demo_list():
    lines = ["Available demos:"]
    for demo in DEMO_TASKS:
        lines.append(f"- {demo.name}: {demo.title} [{demo.skill}]")
    return "\n".join(lines)


def format_demo_show(demo):
    lines = [
        f"Demo: {demo.name}",
        f"Title: {demo.title}",
        f"Skill: {demo.skill}",
        "",
        "Prompt:",
        demo.prompt,
        "",
        "Interview flow:",
        f"1. Inspect this template with `uv run minicodeagent demo show {demo.name}`.",
        "2. Run the agent command below.",
        "3. Review the latest run with `uv run minicodeagent report latest`.",
        "4. Explain active skills, tools, safety, and files changed from the report.",
        "",
        "Replay:",
        f"uv run minicodeagent demo show {demo.name}",
        f"uv run minicodeagent --approval ask \"{demo.prompt}\"",
        "uv run minicodeagent report latest",
        "",
        "Talking points:",
    ]
    lines.extend(f"- {point}" for point in demo.talking_points)
    return "\n".join(lines)
