from sqlmodel import Session, select
from models import Logs, get_engine, init_db


class MemoryManager:
    def __init__(self, goal: str, project_name: str):
        self.goal = goal
        self.engine, db_exists = get_engine(project_name)
        init_db(self.engine)

        if not db_exists:
            self.writeLog(Logs(
                agent="System",
                type="INITIALIZATION",
                action="Project created",
                reason="First run",
                summary=f"Goal: {goal}"
            ))

    def writeLog(self, data: Logs):
        with Session(self.engine) as session:
            session.add(data)
            session.commit()

    def readLog(self, limit: int | None = None):
        with Session(self.engine) as session:
            statement = (select(Logs).order_by(Logs.timestamp.desc()))
            if limit:
                statement = statement.limit(limit)
            logs = session.exec(statement).all()
            return logs
