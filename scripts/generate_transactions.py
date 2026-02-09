import random
import pandas as pd
from datetime import datetime, timedelta

# -----------------------------
# CONFIG
# -----------------------------
USER_ID = "U001"
START_DATE = datetime(2025, 1, 1)
END_DATE = datetime(2025, 12, 31)
OUTPUT_FILE = "../data/transactions.csv"

MERCHANTS = {
    "Food": ["GRAB*FOOD", "MCDONALDS", "KFC", "TEXAS CHICKEN", "LOCAL CAFE"],
    "Fuel": ["SETEL", "PETRONAS", "SHELL"],
    "Grocery": ["LOTUS", "GIANT", "AEON", "VILLAGE GROCER"],
    "Transport": ["GRAB", "RAPIDKL", "TNG TRANSIT"],
    "Shopping": ["SHOPEE", "LAZADA", "UNIQLO", "IKEA"]
}

CHANNELS = ["E-WALLET", "DEBIT CARD"]
LOCATIONS = ["Kuala Lumpur", "Petaling Jaya", "Shah Alam"]

CATEGORY_RANGES = {
    "Food": (10, 120),
    "Fuel": (40, 120),
    "Grocery": (30, 250),
    "Transport": (5, 50),
    "Shopping": (50, 500)
}

# -----------------------------
# HELPERS
# -----------------------------
def random_datetime(day):
    hour = random.choice(
        list(range(8, 22)) +  # normal hours
        ([22, 23] if random.random() < 0.2 else [])
    )
    minute = random.randint(0, 59)
    return day.replace(hour=hour, minute=minute)

def generate_amount(category, is_weekend):
    low, high = CATEGORY_RANGES[category]
    if is_weekend and category in ["Food", "Shopping"]:
        high *= 1.3
    return round(random.uniform(low, high), 2)

# -----------------------------
# GENERATE DATA
# -----------------------------
transactions = []
txn_id = 1
current_date = START_DATE

while current_date <= END_DATE:
    is_weekend = current_date.weekday() >= 5

    daily_txn_count = random.randint(1, 4)
    for _ in range(daily_txn_count):
        category = random.choices(
            population=list(MERCHANTS.keys()),
            weights=[30, 15, 20, 15, 20],
            k=1
        )[0]

        merchant = random.choice(MERCHANTS[category])
        amount = generate_amount(category, is_weekend)

        transactions.append({
            "transaction_id": f"TXN{txn_id:06d}",
            "user_id": USER_ID,
            "datetime": random_datetime(current_date),
            "amount": amount,
            "merchant": merchant,
            "category": category,
            "channel": random.choice(CHANNELS),
            "payment_type": "DEBIT",
            "location": random.choice(LOCATIONS)
        })
        txn_id += 1

    current_date += timedelta(days=1)

# -----------------------------
# SAVE
# -----------------------------
df = pd.DataFrame(transactions)
df = df.sort_values("datetime")
df.to_csv(OUTPUT_FILE, index=False)

print(f"Generated {len(df)} transactions → {OUTPUT_FILE}")
