from time import time
from uuid import uuid4

from models import get_db, get_embedding


class MemoryManager:
    def __init__(self, project_name: str):
        self.project_name = project_name
        self.db = get_db(project_name)

        if "logs" not in self.db.table_names():
            self.table = self.db.create_table(
                "logs",
                data=[
                    {
                        "id": str(uuid4()),
                        "agent": "system",
                        "type": "INITIALIZATION",
                        "action": "Project created",
                        "reason": "First run",
                        "summary": f"Goal: {project_name}",
                        "artifacts": "[]",
                        "timestamp": time(),
                        "vector": get_embedding(f"Project_name: {project_name}"),
                    }
                ],
            )
        else:
            self.table = self.db.open_table("logs")

    def writeLog(self, data: dict):
        text = f"{data['action']} {data['reason']} {data['summary']}"
        data["vector"] = get_embedding(text)
        data["id"] = str(uuid4())
        data["timestamp"] = time()
        self.table.add([data])

    def readLog(self, limit: int):
        logs = (
            self.table.search()
            .select(
                ["agent", "type", "action", "reason", "summary", "artifacts", "timestamp"]
            )
            .limit(limit)
            .to_list()
        )
        logs.sort(key=lambda x: x["timestamp"], reverse=True)
        return logs

    def queryLog(self, query: str, limit: int = 10):
        query_vector = get_embedding(query)
        results = self.table.search(query_vector).limit(limit).to_list()
        return [r for r in results if r["_distance"] < 0.6]
