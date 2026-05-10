import json

from mcp.server.fastmcp import FastMCP

from core.context import ContextEngine
from core.memory import MemoryManager
from models import Logs, Projects, engine

mcp = FastMCP("context-span")

memory: MemoryManager | None = None
context: ContextEngine | None = None


@mcp.tool()
def initalize_project(goal: str):
    global memory, context
    memory = MemoryManager(goal=goal)
    context = ContextEngine(memory)


@mcp.tool()
def add_log(
    agent: str,
    type: str,
    action: str,
    reason: str,
    summary: str,
    files_changed: list[str] | None = None,
    handoff_message: str | None = None,
) -> str:
    if memory is None or context is None:
        return "initialize a project"

    entry = Logs(
        project_id=memory.project_id,
        agent=agent,
        type=type,
        action=action,
        reason=reason,
        summary=summary,
        files_changed=(json.dumps(files_changed) if files_changed else None),
        handoff_message=handoff_message,
    )
    memory.writeLog(entry)
    return "log written"


@mcp.tool()
def read_log():
    if memory is None or context is None:
        return "initialize a project"
    return context.global_context()


if __name__ == "__main__":
    mcp.run(transport="streamable-http")
