import pandas as pd
import numpy as np
from generate_daily_transaction import generate_transaction

def feature_eng():
    # LOAD DATA
    df = generate_transaction()

    # TIME FEATURES
    df["hour"] = df["datetime"].dt.hour
    df["day_of_week"] = df["datetime"].dt.weekday  # Monday=0
    df["is_weekend"] = df["day_of_week"] >= 5

    def time_bucket(hour):
        if 6 <= hour < 12:
            return "MORNING"
        elif 12 <= hour < 18:
            return "AFTERNOON"
        elif 18 <= hour < 22:
            return "EVENING"
        else:
            return "LATE_NIGHT"

    df["time_bucket"] = df["hour"].apply(time_bucket)

    # CATEGORY BASELINES
    category_stats = (
        df.groupby("category")["amount"]
        .agg(["mean", "std", "count"])
        .reset_index()
        .rename(columns={
            "mean": "category_avg_amount",
            "std": "category_std_amount",
            "count": "category_txn_count"
        })
    )

    df = df.merge(category_stats, on="category", how="left")

    # Avoid divide-by-zero
    df["category_std_amount"] = df["category_std_amount"].fillna(1)

    # MERCHANT BASELINES
    merchant_stats = (
        df.groupby("merchant")["amount"]
        .agg(["mean", "count"])
        .reset_index()
        .rename(columns={
            "mean": "merchant_avg_amount",
            "count": "merchant_txn_count"
        })
    )

    df = df.merge(merchant_stats, on="merchant", how="left")

    # Z-SCORE CALCULATION
    df["amount_zscore"] = (
        (df["amount"] - df["category_avg_amount"]) /
        df["category_std_amount"]
    )

    # ROUND & CLEAN
    df["category_avg_amount"] = df["category_avg_amount"].round(2)
    df["category_std_amount"] = df["category_std_amount"].round(2)
    df["merchant_avg_amount"] = df["merchant_avg_amount"].round(2)
    df["amount_zscore"] = df["amount_zscore"].round(2)

    # SAVE
    df = df.sort_values("datetime")
    return df