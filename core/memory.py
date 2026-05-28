from sqlmodel import Session, select
from models import get_db, get_embedding
from uuid import uuid4
from time import time

class MemoryManager:
    def __init__(self, goal: str, project_name: str):
        self.goal = goal
        self.project_name = project_name
        self.db = get_db(project_name)

        if "logs" not in self.db.table_names():
            self.table = self.db.create_table("logs", data = [{
                "id": str(uuid4()),
                "agent": "system",
                "type": "INITIALIZATION",
                "action": "Project created",
                "reason": "First run",
                "summary": f"Goal: {goal}",
                "artifacts": "[]",
                "timestamp": time(),
                "vector": get_embedding(f"Goal: {goal}"),
            }])
        else:
            self.table = self.db.open_table("logs")
            
    @property
    def project_goal(self):
        return self.goal
    
    def writeLog(self, data: dict):
        text = f"{data['action']} {data['reason']} {data['summary']}"
        data['vector'] = get_embedding(text)
        data['id'] = str(uuid4())
        data['timestamp'] = time()
        self.table.add([data])

    def readLog(self, limit: int | None = None):
        logs = self.table.search().select(["action", "reason", "summary", "artifacts", "timestamp"]).limit(limit).to_list()
        logs.sort(key=lambda x: x["timestamp"], reverse=True)
        return logs
    
    def queryLog(self, query: str, limit: int | None = None):
        query_vector = get_embedding(query)
        results = self.table.search(query_vector).limit(limit).to_list()
        return results