from mcp.server.fastmcp import FastMCP
from sqlmodel import Session, select

from models import Logs, Projects, engine

mcp = FastMCP("context-span")


class MemoryManager:
    def __init__(self, goal: str):
        self.project = Projects(goal=goal)
        with Session(engine) as session:
            session.add(self.project)
            session.commit()
            session.refresh(self.project)
            self.project_id = self.project.id

    def writeLog(self, data: Logs):
        with Session(engine) as session:
            session.add(data)
            session.commit()

    def readLog(self):
        with Session(engine) as session:
            statement = select(Logs).where(Logs.project_id == self.project.id)
            logs = session.exec(statement).all()
            return logs


class ContextEngine:
    def __init__(self, memory: MemoryManager):
        self.memory = memory

    def global_context(self):
        entries = self.memory.readLog()[-5:]
        last_entry = entries[-1]
        if last_entry.handoff_message:
            pass
        context_summary = entries
        return context_summary

    def specified_context(self, field: str, value: str):
        """
        get specific context by agent, actions, files_changed
        """
        entries = self.memory.readLog()
        res = []
        for e in entries:
            if getattr(e, field) == value:
                res.append(e)
        return res


memory: MemoryManager | None = None
context: ContextEngine | None = None


@mcp.tool()
def initalizeProject(goal: str):
    global memory, context
    memory = MemoryManager(goal=goal)
    context = ContextEngine(memory)


@mcp.tool()
def add_log(
    agent: str,
    action: str,
    type: str,
    reason: str,
    summary: str,
    files_changed: str | None = None,
    handoff_message: str | None = None,
) -> str:
    if memory is None or context is None:
        return f"initialize a project"

    entry = Logs(
        project_id=memory.project_id,
        agent=agent,
        action=action,
        type=type,
        reason=reason,
        summary=summary,
        files_changed=files_changed,
        handoff_message=handoff_message,
    )
    memory.writeLog(entry)
    return "log written"


@mcp.tool()
def read_log() -> list:
    if memory is None or context is None:
        return f"initialize a project"
    return context.global_context()


if __name__ == "__main__":
    mcp.run(transport="stdio")
