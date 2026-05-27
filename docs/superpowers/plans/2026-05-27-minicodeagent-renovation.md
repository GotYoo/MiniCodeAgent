# MiniCodeAgent Renovation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Turn the imported codebase into a clean MiniCodeAgent project with interview-ready branding, safety, observability, and extension features.

**Architecture:** Keep the current compact local coding-agent runtime, then rename public surfaces first before adding behavior. Subsequent rounds add structured tool responses, approval policy hardening, run reports, and lightweight skills through focused modules with tests.

**Tech Stack:** Python 3.10+, setuptools, pytest, JSON/JSONL run artifacts, terminal CLI.

---

### Round 1: Brand And Package Rename

**Files:**
- Rename: `MiniCodeAgent/` to `minicodeagent/`
- Rename: `tests/test_MiniCodeAgent.py` to `tests/test_minicodeagent.py`
- Modify: `pyproject.toml`
- Modify: `.env.example`
- Modify: `.gitignore`
- Modify: `README.md`
- Modify: `benchmarks/coding_tasks.json`
- Modify: `scripts/*.py`
- Modify: `tests/*.py`
- Modify: `minicodeagent/*.py`

- [ ] Rename package directory and test file.
- [ ] Replace imports and module paths with `minicodeagent`.
- [ ] Replace CLI entry point with `minicodeagent`.
- [ ] Replace runtime artifact directory `.minicodeagent` with `.minicodeagent`.
- [ ] Replace environment variable prefix `MINICODEAGENT_` with `MINICODEAGENT_`.
- [ ] Run `python -m pytest tests -q`.
- [ ] Commit as `refactor: rename project to MiniCodeAgent`.

### Round 2: Documentation And Interview Materials

**Files:**
- Modify: `README.md`
- Create: `docs/architecture.md`
- Create: `docs/interview_qa.md`
- Create: `demo/interview_demo_script.md`

- [ ] Rewrite README around MiniCodeAgent positioning and quick start.
- [ ] Add architecture walkthrough.
- [ ] Add interview Q&A.
- [ ] Add deterministic demo prompts.
- [ ] Commit as `docs: rewrite README and add interview materials`.

### Round 3: Unified Tool Response Protocol

**Files:**
- Create: `minicodeagent/tool_protocol.py`
- Modify: `minicodeagent/tools.py`
- Modify: `minicodeagent/runtime.py`
- Create: `tests/test_tool_protocol.py`

- [ ] Add `success_response`, `partial_response`, and `error_response`.
- [ ] Convert built-in tools to return protocol envelopes.
- [ ] Ensure runtime still clips and records readable tool observations.
- [ ] Test success and error envelopes.
- [ ] Commit as `feat: add unified tool response protocol`.

### Round 4: Approval Policy Hardening

**Files:**
- Modify: `minicodeagent/tools.py`
- Modify: `minicodeagent/runtime.py`
- Modify: `minicodeagent/cli.py`
- Create: `tests/test_approval_policy.py`

- [ ] Define safe and risky tool groups.
- [ ] Enforce `ask`, `auto`, `never`, and `read-only` behavior.
- [ ] Record denied risky tool attempts in trace metadata.
- [ ] Test `never` and `read-only` denial paths.
- [ ] Commit as `feat: enforce approval policy for risky tools`.

### Round 5: Structured Run Reports

**Files:**
- Modify: `minicodeagent/runtime.py`
- Modify: `minicodeagent/task_state.py`
- Modify: `minicodeagent/run_store.py`
- Create: `tests/test_run_report.py`

- [ ] Add tools used, risky tools used, files read, files modified, denial count, duration, and errors to `report.json`.
- [ ] Keep report deterministic and local-only.
- [ ] Test report fields after a fake-model run.
- [ ] Commit as `feat: add structured run reports`.

### Round 6: Lightweight Skills Extension

**Files:**
- Create: `minicodeagent/skills.py`
- Modify: `minicodeagent/runtime.py`
- Create: `skills/code-review/SKILL.md`
- Create: `skills/test-fix/SKILL.md`
- Create: `skills/repo-summary/SKILL.md`
- Create: `tests/test_skills.py`

- [ ] Scan `skills/*/SKILL.md`.
- [ ] Parse `name` and `description`.
- [ ] Inject skill summaries into the prompt.
- [ ] Test discovery and prompt injection.
- [ ] Commit as `feat: add lightweight skills extension`.


