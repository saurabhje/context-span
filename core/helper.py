import json
import ollama


def extract_information_from_query(query: str) -> dict:
    response = ollama.chat(
        model="qwen2.5:0.5b",
        messages=[
            {
                "role": "system",
                "content": """
                            You extract retrieval signals from tasks.
                            Return ONLY valid JSON.
                            RULES:
                            -keyword = important technical terms
                            -artifact = important files, code snippets, or data, url
                            -concept = broader engineering concepts related to the task
                            Schema:
                            {
                            "keywords": [],
                            "artifacts": [],
                            "concepts": []
                            }
                            """
                        },
                            {
                                "role": "user",
                                "content": f"""Task:{query}"""
                            }
        ]
    )

    data = response.message.content.strip()

    return json.loads(data)


print(
    extract_information_from_query(
        "implement a function to call the ollama api"
    )
)