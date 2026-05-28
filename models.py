from pathlib import Path
import lancedb
import ollama 


def get_db(project_name):
    db_dir = Path.home() / ".context-span" / project_name
    db_dir.mkdir(parents=True, exist_ok=True)
    return lancedb.connect(str(db_dir))

def get_embedding(text):
    response = ollama.embeddings(
        model="nomic-embed-text",
        prompt=text
    )
    return response['embedding']
