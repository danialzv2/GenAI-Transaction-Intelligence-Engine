from fastapi import FastAPI
import pandas as pd
import json
from fastapi.middleware.cors import CORSMiddleware
from explainer import explain_insight
import os
import subprocess
import sys

app = FastAPI(title="GenAI Transaction Intelligence API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # allow all origins (dev mode)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PIPELINE_SCRIPT = os.path.join(BASE_DIR, "../src/main.py")
TXN_FILE = os.path.join(BASE_DIR, "../data/transactions_patterns.csv")
INSIGHT_FILE = os.path.join(BASE_DIR, "../data/transaction_insights.json")

df = pd.read_csv(TXN_FILE)

with open(INSIGHT_FILE) as f:
    all_insights = json.load(f)

# -----------------------------
@app.get("/transactions")
def get_transactions(limit: int = 50):
    return df.head(limit).to_dict(orient="records")

# -----------------------------
@app.get("/transaction/{txn_id}/explain")
def explain_transaction(txn_id: str):
    txn = df[df["transaction_id"] == txn_id]
    if txn.empty:
        return {"error": "Transaction not found"}

    txn_insights = [
        i for i in all_insights
        if i["transaction_id"] == txn_id
    ]

    explanations = []

    for insight in txn_insights:
        text = explain_insight(insight)
        explanations.append({
            "insight_type": insight["insight_type"],
            "explanation": text
        })

    return {
        "transaction": txn.iloc[0].to_dict(),
        "explanations": explanations
    }

@app.post("/generate-transaction")
def generate_transaction():
    """
    Trigger backend pipeline to generate a new transaction
    and refresh processed data.
    """
    global df, all_insights

    try:
        # 1. Run pipeline script safely
        result = subprocess.run(
            [sys.executable, PIPELINE_SCRIPT],
            check=True,
            capture_output=True,
            text=True
        )

        # 2. Reload updated transaction CSV
        df = pd.read_csv(TXN_FILE)

        # 3. Reload updated insight JSON
        with open(INSIGHT_FILE, "r") as f:
            all_insights = json.load(f)

        return {
            "status": "OK",
            "message": "New transaction generated successfully",
            "pipeline_output": result.stdout
        }

    except subprocess.CalledProcessError as e:
        return {
            "status": "ERROR",
            "message": "Pipeline execution failed",
            "error": e.stderr
        }