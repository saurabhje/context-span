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

    def global_context(self):
        entries = self.memory.readLog()[-5:]
        last_entry = entries[-1]
        if last_entry.handoff_message:
            pass
        context_summary = entries
        return context_summary

    def specified_context(self, field: str, value: str):
        """
        get specific context by agent, actions, files_changed
        """
        entries = self.memory.readLog()
        res = []
        for e in entries:
            if getattr(e, field) == value:
                res.append(e)
        return res


s1 = MemoryManager(goal="testing")
c1 = ContextEngine(s1)
new_entry = MemoryEntry(
    id="1",
    agent="claude",
    type="nigga",
    action="nigga",
    reason="nigga",
    files_changed=["nigga", "nigga2"],
    summary="did nigga",
    handoff_message="nigga",
)
s1.writeLog(new_entry)
print(c1.specified_context("agent", "claude"))
