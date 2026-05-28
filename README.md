# MiniCodeAgent

MiniCodeAgent is a lightweight local coding agent runtime for repository-oriented tasks. It runs in the terminal, inspects the current workspace, calls a bounded set of tools, and stores session state and run artifacts locally under `.minicodeagent/`.

The project focuses on the runtime layer behind coding agents: workspace context, model adapters, tool execution, approval control, memory, checkpointed resume, trace logging, and reproducible run reports.

## Why MiniCodeAgent

MiniCodeAgent is built as an interview-ready agent engineering project rather than a thin API wrapper. The goal is to show how a coding agent can be controlled, observed, extended, and explained.

- **Runtime control loop:** turns a user request into repeated model decisions, validated tool calls, observations, checkpoints, and a final answer.
- **Bounded tool system:** exposes file read/search/write/patch/shell/delegation through explicit schemas instead of free-form hidden actions.
- **Unified tool protocol:** normalizes tool outputs into success, partial, and error envelopes while still giving the model concise observations.
- **Safety approval layer:** separates safe read/search tools from risky shell and file-write tools, with `ask`, `auto`, `never`, and read-only modes.
- **Observable run artifacts:** records `task_state.json`, `trace.jsonl`, and structured `report.json` for post-run debugging and review.
- **Local skills extension:** loads repository-local `skills/*/SKILL.md`, activates relevant skills per request, and records active skills in reports.
- **Demo replay path:** provides built-in interview demo templates and report review commands so the project can be demonstrated consistently.

## What It Does

- Inspects repository structure and important project documents before acting.
- Reads files, searches code, writes patches, and runs shell commands through explicit tools.
- Keeps conversation history, compact working memory, and checkpoint metadata across turns.
- Supports local run artifacts for debugging and review: `task_state.json`, `trace.jsonl`, and `report.json`.
- Works with Ollama, OpenAI-compatible Responses API, Anthropic-compatible Messages API, and DeepSeek's Anthropic-compatible endpoint.
- Supports risky-tool approval modes: `ask`, `auto`, and `never`.

## Runtime Flow

```mermaid
flowchart TD
    User["User request"] --> CLI["CLI / one-shot command"]
    CLI --> Workspace["Workspace snapshot"]
    CLI --> Session["Session store"]
    Workspace --> Runtime["MiniCodeAgent runtime"]
    Session --> Runtime
    Runtime --> Context["Context manager"]
    Context --> Prompt["Prompt: rules + workspace + memory + history + request"]
    Prompt --> Model["Model adapter"]
    Model --> Decision{"Tool call or final answer?"}
    Decision -->|Tool call| Validate["Validate tool and arguments"]
    Validate --> Approval{"Risky tool?"}
    Approval -->|No| Execute["Execute tool"]
    Approval -->|Yes| Policy["Approval policy"]
    Policy -->|Allowed| Execute
    Policy -->|Denied| Observation["Denied observation"]
    Execute --> Observation["Tool observation"]
    Observation --> Memory["Update memory and checkpoint"]
    Memory --> Trace["Write trace and task state"]
    Trace --> Context
    Decision -->|Final answer| Report["Write report.json"]
    Report --> Answer["Return answer"]
```

## Project Layout

```text
minicodeagent/
  cli.py              CLI assembly and interactive loop
  runtime.py          Agent control loop, approval, trace, checkpoints
  tools.py            Built-in workspace tools
  context_manager.py  Prompt section budgeting and history reduction
  memory.py           Working memory and durable topic notes
  models.py           Provider adapters
  run_store.py        Local run artifacts
  skills.py           Repository-local skill discovery
  task_state.py       Per-run task status model
tests/                Regression tests for runtime, tools, memory, safety, metrics
skills/               Local task workflow summaries injected into the prompt
benchmarks/           Scripted benchmark tasks
docs/                 Public architecture and review notes
```

## Install

MiniCodeAgent requires Python 3.10+.

With `uv`:

```bash
uv sync
```

With pip:

```bash
pip install -e .
```

## Quick Start

Run in the current repository:

```bash
uv run minicodeagent --provider deepseek
```

Run against another workspace:

```bash
uv run minicodeagent --cwd /path/to/repo --provider deepseek
```

Run a one-shot task:

```bash
uv run minicodeagent --provider deepseek "inspect the test failures and propose a fix"
```

List interview demo templates:

```bash
uv run minicodeagent demo list
uv run minicodeagent demo show test-fix
```

Replay a complete interview loop:

```bash
uv run minicodeagent demo show test-fix
uv run minicodeagent --approval ask "Run the focused failing test, diagnose the failure from its output, make the smallest fix, and rerun the test."
uv run minicodeagent report latest
```

## Interview Demo Path

Use this sequence when presenting the project:

1. Show available demo tasks:

   ```bash
   uv run minicodeagent demo list
   ```

2. Inspect one demo template:

   ```bash
   uv run minicodeagent demo show test-fix
   ```

3. Run the generated prompt with an approval policy:

   ```bash
   uv run minicodeagent --approval ask "Run the focused failing test, diagnose the failure from its output, make the smallest fix, and rerun the test."
   ```

4. Review the structured report:

   ```bash
   uv run minicodeagent report latest
   ```

5. Explain the report in terms of active skills, requested tools, risky-tool approvals, files read, files modified, and final status.

Recommended demos:

- `repo-summary`: safest first demo; shows repository understanding and skill activation without requiring file writes.
- `code-review`: best for explaining read/search behavior, findings-first output, and report review.
- `test-fix`: strongest end-to-end demo; shows shell execution, patching, verification, safety approval, and report replay.

If installed in the current environment:

```bash
python -m minicodeagent --provider deepseek
```

## Configuration

MiniCodeAgent loads `.env` from the workspace root. Keep real keys in `.env`; only `.env.example` should be committed.

Configuration priority:

```text
CLI arguments > MINICODEAGENT_* environment variables > legacy provider variables > defaults
```

Example:

```bash
cp .env.example .env
```

### Ollama

```bash
ollama serve
ollama pull qwen3.5:4b
uv run minicodeagent --provider ollama --model qwen3.5:4b
```

### OpenAI-Compatible

```bash
MINICODEAGENT_OPENAI_API_BASE="https://your-api.example/v1"
MINICODEAGENT_OPENAI_API_KEY="your-api-key"
MINICODEAGENT_OPENAI_MODEL="gpt-5.4"
uv run minicodeagent --provider openai
```

### Anthropic-Compatible

```bash
MINICODEAGENT_ANTHROPIC_API_BASE="https://your-api.example/v1"
MINICODEAGENT_ANTHROPIC_API_KEY="your-api-key"
MINICODEAGENT_ANTHROPIC_MODEL="claude-sonnet-4-6"
uv run minicodeagent --provider anthropic
```

### DeepSeek

```bash
MINICODEAGENT_DEEPSEEK_API_KEY="your-api-key"
MINICODEAGENT_DEEPSEEK_MODEL="deepseek-v4-pro"
uv run minicodeagent --provider deepseek
```

## Interactive Commands

- `/help`: show commands
- `/memory`: show distilled working memory
- `/session`: show the current session file path
- `/reset`: clear current session history and memory
- `/exit` or `/quit`: exit the REPL

## Safety And Persistence

MiniCodeAgent treats shell execution and file writes as risky actions. Risky tools are controlled by:

```bash
--approval ask
--approval auto
--approval never
```

Run artifacts are written locally:

```text
.minicodeagent/runs/<run_id>/
  task_state.json
  trace.jsonl
  report.json
```

These artifacts are local debugging and review data; they are ignored by git.

Review recent runs without opening JSON files:

```bash
uv run minicodeagent runs
uv run minicodeagent report latest
```

`runs` lists stored run ids with status and stop reason. `report latest` prints a compact summary of the latest run, including requested tools, risky-tool denials, files read, and files modified.

## Talking Points

- I built the project around the agent runtime, not only model prompting. The runtime owns prompt assembly, tool validation, approval policy, memory, checkpoints, trace, and reports.
- I added a unified tool response protocol so every tool call has a machine-readable status, error code, data payload, and human-readable text.
- I hardened safety by separating safe tools from risky tools and making risky operations visible in both trace and report artifacts.
- I made the agent observable: each run produces trace and report files, and the CLI can summarize them without opening JSON manually.
- I added a lightweight skills mechanism so task-specific workflows are local markdown files instead of hard-coded prompt text.
- I added demo templates and replay commands so the project can be shown consistently in an interview.

## Development

Run tests:

```bash
python -m pytest tests -q
```

Run lint if Ruff is installed:

```bash
uv run ruff check .
```
