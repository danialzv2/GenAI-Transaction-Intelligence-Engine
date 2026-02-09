from fastapi import FastAPI
import pandas as pd
import json
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="GenAI Transaction Intelligence API")

TRANSACTION_FILE = "../data/transactions_patterns.csv"
EXPLANATION_FILE = "../data/transaction_explanations.json"

df = pd.read_csv(TRANSACTION_FILE)
with open(EXPLANATION_FILE) as f:
    explanations = json.load(f)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # allow all origins (dev mode)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/transactions")
def get_transactions(limit: int = 20):
    return df.head(limit).to_dict(orient="records")

@app.get("/transaction/{txn_id}/explain")
def explain_transaction(txn_id: str):
    explanation = next(
        (e for e in explanations if e["transaction_id"] == txn_id),
        None
    )

    txn = df[df["transaction_id"] == txn_id]
    if txn.empty:
        return {"error": "Transaction not found"}

    return {
        "transaction": txn.iloc[0].to_dict(),
        "explanation": explanation
    }
