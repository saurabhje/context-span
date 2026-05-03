from pydantic import BaseModel, Field
from time import time

class MemoryEntry(BaseModel):
    id: str
    agent: str
    type: str
    action: str
    reason: str
    files_changed: list[str]
    change_summary: str | None = None
    handoff_message: str | None = None
    timestamp: float = Field(default_factory=time)

class GlobalMemory(BaseModel):
    goal: str
    log: list[MemoryLog] = Field(default_factory=list)
