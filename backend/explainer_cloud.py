import os
import requests
from prompts import SYSTEM_PROMPT, USER_PROMPT_TEMPLATE

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL_NAME = "deepseek/deepseek-r1-0528:free"

def explain_insight(insight: dict) -> str:

    """
    Generate GenAI explanation for ONE transaction insight
    """

    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        return "AI explanation service not configured."
    
    facts_text = "\n".join(
        [f"- {k}: {v}" for k, v in insight["facts"].items()]
    )

    user_prompt = USER_PROMPT_TEMPLATE.format(
        insight_type=insight["insight_type"],
        severity=insight["severity"],
        facts=facts_text
    )

    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": 0.2,
        "max_tokens": 120
    }

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        # Optional but recommended
        "HTTP-Referer": "http://localhost",
        "X-Title": "Transaction Insight Explainer"
    }

    response = requests.post(
        OPENROUTER_URL,
        json=payload,
        headers=headers,
        timeout=30
    )
    response.raise_for_status()

    return response.json()["choices"][0]["message"]["content"].strip()
