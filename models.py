from time import time
from uuid import UUID, uuid4
import os
from sqlmodel import Field, SQLModel, create_engine
from pathlib import Path

class Logs(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    agent: str = Field(index=True)
    type: str
    action: str
    reason: str
    summary: str
    artifacts: str | None = None
    timestamp: float = Field(default_factory=time, index=True)


def get_engine(project_name):
    db_dir = Path.home() / ".context-span"
    db_dir.mkdir(parents=True, exist_ok=True)
    db_path = db_dir / f"{project_name}.db"
    db_exists = db_path.exists()
    engine = create_engine(f"sqlite:///{db_path}")
    return engine, db_exists

def init_db(engine):
    SQLModel.metadata.create_all(engine)