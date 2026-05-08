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

    def readLog(self, limit: int | None = None):
        with Session(engine) as session:
            statement = select(Logs).where(Logs.project_id == self.project.id)
            if limit:
                statement = statement.limit(limit)
            logs = session.exec(statement).all()
            return logs


class ContextEngine:
    def __init__(self, memory: MemoryManager):
        self.memory = memory

    def global_context(self):
        entries = self.memory.readLog()
        last_entry = entries[-1]
        if last_entry.handoff_message:
            pass
        context_summary = entries
        return context_summary

    def specified_context(
        self,
        agent: str | None = None,
        action: str | None = None,
        files_changed: str | None = None,
    ):
        with Session(engine) as session:
            statement = select(Logs).where(Logs.project_id == self.memory.project_id)
            if agent:
                statement = statement.where(Logs.agent == agent)
            if action:
                statement = statement.where(Logs.action == action)
            if files_changed:
                statement = statement.where(Logs.files_changed == files_changed)
            logs = session.exec(statement).all()
            return logs


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
    action: str,
    reason: str,
    summary: str,
    files_changed: str | None = None,
    handoff_message: str | None = None,
) -> str:
    if memory is None or context is None:
        return "initialize a project"

    entry = Logs(
        project_id=memory.project_id,
        agent=agent,
        action=action,
        reason=reason,
        summary=summary,
        files_changed=files_changed,
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
