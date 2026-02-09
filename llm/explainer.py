import json
import requests
from llm.prompts import SYSTEM_PROMPT, USER_PROMPT_TEMPLATE

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3.1:8b"

INSIGHT_FILE = "../data/transaction_insights.json"
OUTPUT_FILE = "../data/transaction_explanations.json"

def generate_explanation(insight):
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

def main():
    with open(INSIGHT_FILE) as f:
        insights = json.load(f)

    explanations = []

    for insight in insights:
        explanation = generate_explanation(insight)

        explanations.append({
            "transaction_id": insight["transaction_id"],
            "insight_type": insight["insight_type"],
            "explanation": explanation
        })

    with open(OUTPUT_FILE, "w") as f:
        json.dump(explanations, f, indent=2)

    print(f"Local LLaMA explanations generated → {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
