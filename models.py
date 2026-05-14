from time import time
from uuid import UUID, uuid4

from sqlmodel import Field, SQLModel, create_engine


class Logs(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    agent: str = Field(index=True)
    type: str
    action: str
    reason: str
    summary: str
    artifacts: str | None = None
    timestamp: float = Field(default_factory=time, index=True)

engine = create_engine("sqlite:///database.db")

def init_db():
    SQLModel.metadata.create_all(engine)
