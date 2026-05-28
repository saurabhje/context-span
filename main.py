import json
import os
from mcp.server.fastmcp import FastMCP

from core.context import ContextEngine
from core.memory import MemoryManager
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

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

    try:
        memory.writeLog({
        "agent": agent,
        "type": type,
        "action": action,
        "reason": reason,
        "summary": summary,
        "artifacts": json.dumps(artifacts) if artifacts else "[]",
    })
        return "Log added successfully."
    except Exception as e:
        return f"Error writing log: {str(e)}"

@mcp.tool()
def read_log(query: str | None = None, limit: int | None = None):
    if memory is None or context is None:
        return "Error: Please initialize the project first."
    if query:
        return context.task_context(query, limit)
    return context.global_context()


if __name__ == "__main__":
    mcp.run()
