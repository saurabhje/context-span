# Context-Span

> imagine all your agents sharing the context of whats happening in your project and who did what, yes this solves that.

## Memory Layer for LLM Agents

The library provides a **global memory layer** that allows multiple LLM agents to read and write shared context. It abstracts the underlying storage so agents can seamlessly switch between models such as Claude, Codex, or any future LLM without changing their code. The memory API supports atomic updates, retrieval by keys, and expiration policies, enabling coordinated workflows in distributed multi‑agent environments.

### Key Features
- Model‑agnostic interface – works with Claude, Codex, GPT, or custom-agents(MCP compliant) etc.
- Real‑time context propagation across nodes.
