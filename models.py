from time import time
from uuid import UUID, uuid4

from sqlmodel import Field, SQLModel, create_engine


class Logs(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    project_id: UUID = Field(foreign_key="projects.id")
    agent: str = Field(index=True)
    action: str
    type: str
    reason: str
    summary: str
    files_changed: str | None = None
    handoff_message: str | None = None
    timestamp: float = Field(default_factory=time)


class Projects(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    goal: str = Field(index=True)


engine = create_engine("sqlite:///database.db")
SQLModel.metadata.create_all(engine)
