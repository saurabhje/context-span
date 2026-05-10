from sqlmodel import Session, select

from models import Logs, Projects, engine


class MemoryManager:
    def __init__(self, goal: str):
        self.project = Projects(goal=goal)
        with Session(engine) as session:
            session.add(self.project)
            session.commit()
            session.refresh(self.project)
            self.project_id = self.project.id
            self.project_goal = self.project.goal

    def writeLog(self, data: Logs):
        with Session(engine) as session:
            session.add(data)
            session.commit()

    def readLog(self, limit: int | None = None):
        with Session(engine) as session:
            statement = (
                select(Logs)
                .where(Logs.project_id == self.project_id)
                .order_by(Logs.timestamp.desc())
            )
            if limit:
                statement = statement.limit(limit)
            logs = session.exec(statement).all()
            return logs
