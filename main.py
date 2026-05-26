import json
import os
from mcp.server.fastmcp import FastMCP

from core.context import ContextEngine
from core.memory import MemoryManager
from models import Logs, init_db

mcp = FastMCP("context-span")

project_name = os.environ.get("PROJECT_NAME")
project_goal = os.environ.get("PROJECT_GOAL")

memory = None
context = None

if project_name  and project_goal:
    memory = MemoryManager(goal=project_goal, project_name=project_name)
    context = ContextEngine(memory)


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
        return "Error: Please initialize the project first."

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
        return "Error: Please initialize the project first."
    return context.global_context()


if __name__ == "__main__":
    mcp.run()
