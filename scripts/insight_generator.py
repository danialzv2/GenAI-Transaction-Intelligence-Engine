import pandas as pd
import json

INPUT_FILE = "../data/transactions_patterns.csv"
OUTPUT_FILE = "../data/transaction_insights.json"

# LOAD DATA
df = pd.read_csv(INPUT_FILE, parse_dates=["datetime"])

insights = []

# INSIGHT BUILDERS
def build_spending_anomaly(row):
    return {
        "transaction_id": row["transaction_id"],
        "insight_type": "SPENDING_ANOMALY",
        "severity": "HIGH" if abs(row["amount_zscore"]) >= 3 else "MEDIUM",
        "facts": {
            "category": row["category"],
            "amount": row["amount"],
            "usual_category_avg": row["category_avg_amount"],
            "zscore": row["amount_zscore"],
            "merchant": row["merchant"]
        }
    }

def build_time_behavior(row):
    return {
        "transaction_id": row["transaction_id"],
        "insight_type": "TIME_BEHAVIOR_SHIFT",
        "severity": "MEDIUM",
        "facts": {
            "time_bucket": row["time_bucket"],
            "is_weekend": bool(row["is_weekend"]),
            "hour": row["hour"]
        }
    }

def build_merchant_change(row):
    return {
        "transaction_id": row["transaction_id"],
        "insight_type": "MERCHANT_RARITY",
        "severity": "LOW",
        "facts": {
            "merchant": row["merchant"],
            "merchant_txn_count": row["merchant_txn_count"],
            "merchant_avg_amount": row["merchant_avg_amount"]
        }
    }

# GENERATE INSIGHTS
for _, row in df.iterrows():
    flags = row["flags"].split("|")

    if "HIGH_AMOUNT" in flags or "LOW_AMOUNT" in flags:
        insights.append(build_spending_anomaly(row))

    if "LATE_NIGHT_WEEKDAY" in flags:
        insights.append(build_time_behavior(row))

    if "RARE_MERCHANT" in flags:
        insights.append(build_merchant_change(row))

# SAVE JSON
with open(OUTPUT_FILE, "w") as f:
    json.dump(insights, f, indent=2)

print(f"Generated {len(insights)} insight signals → {OUTPUT_FILE}")
