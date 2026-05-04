from memory_model import GlobalMemory, MemoryEntry


class MemoryManager:
    def __init__(self, goal: str):
        self.memory = GlobalMemory(goal=goal)

    def writeLog(self, data: MemoryEntry):
        self.memory.log.append(data)

    def readLog(self):
        return self.memory.log


class ContextEngine:
    def __init__(self, memory: MemoryManager):
        self.memory = memory

    def latest_project_context(self):
        context_summary = list()
        entries = self.memory.readLog()[-5:]
        last_entry = entries[-1]
        if last_entry.handoff_message:
            pass
        context_summary.append(entries)
        return context_summary
