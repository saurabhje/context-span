import json

from sqlmodel import Session, select

from core.memory import MemoryManager
from models import Logs, engine


class ContextEngine:
    def __init__(self, memory: MemoryManager):
        self.memory = memory

    def serialize_log(self, log: Logs):
        return {
            "agent": log.agent,
            "type": log.type,
            "action": log.action,
            "reason": log.reason,
            "summary": log.summary,
            "files_changed": [f for f in json.loads(log.files_changed) if f]
            if log.files_changed
            else [],
            "handoff_message": log.handoff_message,
            "timestamp": log.timestamp,
        }

    def global_context(self, limit: int | None = None):
        entries = self.memory.readLog(limit)
        if not entries:
            return []
        last_entry = entries[0]

        return {
            "project_goal": self.memory.project_goal,
            "handoff_message": last_entry.handoff_message if last_entry else None,
            "logs": [self.serialize_log(entry) for entry in entries],
        }

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
                statement = statement.where(Logs.files_changed.contains(files_changed))
            logs = session.exec(statement).all()
            return [self.serialize_log(log) for log in logs]
