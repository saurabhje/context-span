from sqlmodel import Session, select

from models import Logs, engine


class MemoryManager:
    def __init__(self, goal: str):
        self.goal = goal

    def writeLog(self, data: Logs):
        with Session(engine) as session:
            session.add(data)
            session.commit()

    def readLog(self, limit: int | None = None):
        with Session(engine) as session:
            statement = (select(Logs).order_by(Logs.timestamp.desc()))
            if limit:
                statement = statement.limit(limit)
            logs = session.exec(statement).all()
            return logs
