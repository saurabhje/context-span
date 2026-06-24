import json
from mcp.server.fastmcp import FastMCP

from core.context import ContextEngine
from core.memory import MemoryManager

mcp = FastMCP("context-span")

memory: MemoryManager | None = None
context: ContextEngine | None = None


@mcp.tool()
def initialize_project(project_name: str):
    """
    Intializing a new project with project_name and creating the vector db file, or connecting to it if already exists
    """
    global memory, context
    memory = MemoryManager(project_name=project_name)
    context = ContextEngine(memory)
    return f"Project {project_name} initialized"


@mcp.tool()
def add_log(
    agent: str,
    type: str,
    action: str,
    reason: str,
    summary: str,
    artifacts: list[str] | None = None,
) -> str:
    """
    Used to log the action of an agent with proper formating
    """
    if memory is None or context is None:
        return "Error: Please initialize the project first."

    try:
        memory.writeLog(
            {
                "agent": agent,
                "type": type,
                "action": action,
                "reason": reason,
                "summary": summary,
                "artifacts": json.dumps(artifacts) if artifacts else "[]",
            }
        )
        return "Log added successfully."
    except Exception as e:
        return f"Error writing log: {str(e)}"


@mcp.tool()
def global_context(limit: int | None = None):
    """
    use this tool when entire global context needs to be retrieved, like in case of generating
    a summary, or agent swapping, starting a new fresh session
    """
    if memory is None or context is None:
        return "Error: Please initialize the project first."
    return context.global_context(limit)


@mcp.tool()
def task_context(query: str, limit: int = 10):
    """
    use this tool when the context for any specific task/query has been asked
    """
    if memory is None or context is None:
        return "Error: Please initialize the project first."
    return context.task_context(query, limit)


if __name__ == "__main__":
    mcp.run(transport="streamable-http")
