import pandas as pd
from insight_generator import insight
from generate_daily_transaction import generate_transaction
import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "..", "data", "transactions.csv")
OUTPUT_PATTERN = os.path.join(BASE_DIR, "..", "data", "transactions_patterns.csv")
OUTPUT_INSIGHTS = os.path.join(BASE_DIR, "..", "data", "transaction_insights.json")

def main():

    insights, df = insight()

    # SAVE JSON
    with open(OUTPUT_INSIGHTS, "w") as f:
        json.dump(insights, f, indent=2)
    print(f"Generated {len(insights)} insight signals {OUTPUT_INSIGHTS}")

    df.to_csv(OUTPUT_PATTERN, index=False)

if __name__ == "__main__":
    main()
    print("Data Successfully Retrieved")