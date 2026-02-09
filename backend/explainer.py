import requests
from prompts import SYSTEM_PROMPT, USER_PROMPT_TEMPLATE

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3.1:8b"

def explain_insight(insight: dict) -> str:
    """
    Generate GenAI explanation for ONE transaction insight
    """

    facts_text = "\n".join(
        [f"- {k}: {v}" for k, v in insight["facts"].items()]
    )

    prompt = USER_PROMPT_TEMPLATE.format(
        insight_type=insight["insight_type"],
        severity=insight["severity"],
        facts=facts_text
    )

    payload = {
        "model": MODEL_NAME,
        "prompt": f"{SYSTEM_PROMPT}\n{prompt}",
        "stream": False,
        "options": {
            "temperature": 0.2,
            "num_predict": 120
        }
    }

    response = requests.post(OLLAMA_URL, json=payload)
    response.raise_for_status()

    return response.json()["response"].strip()
