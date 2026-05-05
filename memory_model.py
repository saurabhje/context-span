from time import time

from pydantic import BaseModel, Field


class MemoryEntry(BaseModel):
    id: str
    agent: str
    type: str
    action: str
    reason: str
    files_changed: list[str] | None = None
    summary: str
    handoff_message: str | None = None
    timestamp: float = Field(default_factory=time)


class GlobalMemory(BaseModel):
    goal: str
    log: list[MemoryEntry] = Field(default_factory=list)
