# MiniCodeAgent Agent Harness v1 Overview

MiniCodeAgent is organized around a compact local runtime:

1. The CLI builds a workspace snapshot, model client, session store, and runtime.
2. The runtime assembles prompt context from workspace facts, memory, relevant notes, history, and the current request.
3. The model emits either a tool call or final answer.
4. Tool calls pass through validation, approval, execution, trace logging, memory updates, task state updates, and report generation.
