import json

from mcp.server.fastmcp import FastMCP

from core.context import ContextEngine
from core.memory import MemoryManager
from models import Logs, init_db

mcp = FastMCP("context-span")

memory: MemoryManager | None = None
context: ContextEngine | None = None


@mcp.tool()
def initalize_project(goal: str) -> str:
    global memory, context
    init_db()
    memory = MemoryManager(goal=goal)
    context = ContextEngine(memory)
    add_log(
        agent="System",
        type="INITIALIZATION",
        action="Project Started",
        reason="User initialized project",
        summary=f"Goal: {goal}"
    )

    return f"Project initialized with goal: {goal}"


@mcp.tool()
def add_log(
    agent: str,
    type: str,
    action: str,
    reason: str,
    summary: str,
    artifacts: list[str] | None = None,
) -> str:
    if memory is None or context is None:
        return "Please initialize the project first."

    entry = Logs(
        agent=agent,
        type=type,
        action=action,
        reason=reason,
        summary=summary,
        artifacts=(json.dumps(artifacts) if artifacts else None),
    )
    memory.writeLog(entry)
    return "log written"

@mcp.tool()
def read_log():
    if memory is None or context is None:
        return "initialize a project"
    return context.global_context()


if __name__ == "__main__":
    mcp.run()
