import typer
from core.memory import MemoryManager
import json

app = typer.Typer()
import typer
from core.memory import MemoryManager
import json

app = typer.Typer()

@app.command()
def log(
    project: str,
    agent: str = "human",
    action: str = typer.Option(...),
    reason: str = typer.Option(...),
    summary: str = typer.Option(...),
    artifacts: list[str] = typer.Option(default=[]),
):
    memory = MemoryManager(project_name=project)
    memory.writeLog({
        "agent": agent,
        "action": action,
        "reason": reason,
        "summary": summary,
        "artifacts": json.dumps(artifacts),
        "type": "manual",
    })
    typer.echo("Log added.")

if __name__ == "__main__":
    app()