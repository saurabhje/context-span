import json

from core.memory import MemoryManager


class ContextEngine:
    def __init__(self, memory: MemoryManager):
        self.memory = memory

    def serialize_log(self, log: dict):
        return {
            "agent": log["agent"],
            "type": log["type"],
            "action": log["action"],
            "reason": log["reason"],
            "summary": log["summary"],
            "artifacts": [f for f in json.loads(log["artifacts"]) if f]
            if log["artifacts"]
            else [],
            "timestamp": log["timestamp"],
        }

    def global_context(self, limit: int):
        logs = self.memory.readLog(limit)
        return {
            "project_name": self.memory.project_name,
            "logs": logs,
        }

    def task_context(self, query, limit: int):
        results = self.memory.queryLog(query, limit)
        return {
            "project_goal": self.memory.project_name,
            "query": query,
            "relevant_logs": [self.serialize_log(result) for result in results],
        }
