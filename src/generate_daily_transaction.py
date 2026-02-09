import random
import pandas as pd
from datetime import datetime, timedelta
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "..", "data", "transactions.csv")

def generate_transaction():
    # CONFIG
    USER_ID = "U001"
    MAX_HISTORY_DAYS = 365

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

    # HELPERS
    def generate_amount(category, is_weekend):
        low, high = CATEGORY_RANGES[category]
        if is_weekend and category in ["Food", "Shopping"]:
            high *= 1.3
        return round(random.uniform(low, high), 2)

    def generate_transaction_id(existing_df):
        """
        Generate a new transaction_id that is guaranteed
        to not duplicate existing IDs in the CSV.
        """
        if existing_df.empty or "transaction_id" not in existing_df.columns:
            return "TXN000001"

        # Extract numeric part safely
        existing_ids = (
            existing_df["transaction_id"]
            .astype(str)
            .str.replace("TXN", "", regex=False)
            .astype(int)
        )

        next_id = existing_ids.max() + 1
        return f"TXN{next_id:06d}"


    # LOAD EXISTING DATA
    if os.path.exists(DATA_FILE):
        df = pd.read_csv(DATA_FILE, parse_dates=["datetime"])
    else:
        df = pd.DataFrame()

    # CLEAN OLD DATA (> 1 YEAR)
    cutoff_date = datetime.now() - timedelta(days=MAX_HISTORY_DAYS)

    if not df.empty:
        df = df[df["datetime"] >= cutoff_date]

    # GENERATE TODAY'S TRANSACTION
    now = datetime.now()
    is_weekend = now.weekday() >= 5

    category = random.choices(
        population=list(MERCHANTS.keys()),
        weights=[30, 15, 20, 15, 20],
        k=1
    )[0]

    merchant = random.choice(MERCHANTS[category])
    amount = generate_amount(category, is_weekend)

    transaction = {
        "transaction_id": generate_transaction_id(df),
        "user_id": USER_ID,
        "datetime": now,
        "amount": amount,
        "merchant": merchant,
        "category": category,
        "channel": random.choice(CHANNELS),
        "payment_type": "DEBIT",
        "location": random.choice(LOCATIONS)
    }

    # APPEND & SAVE
    df = pd.concat([df, pd.DataFrame([transaction])], ignore_index=True)
    df = df.sort_values("datetime")
    df.to_csv(DATA_FILE, index=False)

    print(transaction)
    return df