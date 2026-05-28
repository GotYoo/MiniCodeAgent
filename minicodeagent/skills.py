"""Lightweight local skill discovery.

Skills are repository-local markdown files at ``skills/*/SKILL.md``.  The
runtime only needs a compact index for prompt guidance; the full skill body can
stay on disk until a user or future tool chooses to inspect it.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class LocalSkill:
    name: str
    description: str
    slug: str
    path: Path


def _parse_frontmatter(text):
    lines = str(text or "").splitlines()
    if not lines or lines[0].strip() != "---":
        return {}
    values = {}
    for line in lines[1:]:
        stripped = line.strip()
        if stripped == "---":
            return values
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        values[key.strip()] = value.strip().strip('"').strip("'")
    return {}


def discover_skills(root):
    root = Path(root)
    skills_root = root / "skills"
    if not skills_root.exists():
        return []

    skills = []
    for path in sorted(skills_root.glob("*/SKILL.md")):
        metadata = _parse_frontmatter(path.read_text(encoding="utf-8", errors="replace"))
        name = str(metadata.get("name", "")).strip()
        description = str(metadata.get("description", "")).strip()
        if not name or not description:
            continue
        skills.append(
            LocalSkill(
                name=name,
                description=description,
                slug=path.parent.name,
                path=path,
            )
        )
    return skills


def render_skill_summaries(skills):
    skills = list(skills or [])
    if not skills:
        return "Skills:\n- none"
    lines = ["Skills:"]
    for skill in skills:
        lines.append(f"- {skill.name}: {skill.description}")
    return "\n".join(lines)
