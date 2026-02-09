import pandas as pd
from feature_engineering import feature_eng

OUTPUT_FILE = "../GenAI-Transaction-Intelligence-Engine/data/transactions_patterns.csv"

def pattern():

    # LOAD DATA
    df = feature_eng()

    # INITIALIZE FLAGS & REASONS
    df["flags"] = ""
    df["reasons"] = ""

    def add_flag_reason(row, flag, reason):
        if row["flags"]:
            row["flags"] += f"|{flag}"
            row["reasons"] += f" | {reason}"
        else:
            row["flags"] = flag
            row["reasons"] = reason
        return row

    # APPLY RULES
    for idx, row in df.iterrows():

        # High amount anomaly
        if row["amount_zscore"] >= 2.0:
            df.loc[idx] = add_flag_reason(
                row,
                "HIGH_AMOUNT",
                "Transaction amount is significantly higher than your usual category spending"
            )

        # Low amount anomaly
        if row["amount_zscore"] <= -2.0:
            df.loc[idx] = add_flag_reason(
                row,
                "LOW_AMOUNT",
                "Transaction amount is significantly lower than your usual category spending"
            )

        # Late night weekday
        if row["time_bucket"] == "LATE_NIGHT" and not row["is_weekend"]:
            df.loc[idx] = add_flag_reason(
                row,
                "LATE_NIGHT_WEEKDAY",
                "Transaction occurred late at night on a weekday"
            )

        # New or rare merchant
        if row["merchant_txn_count"] <= 2:
            df.loc[idx] = add_flag_reason(
                row,
                "RARE_MERCHANT",
                "This merchant is new or rarely used in your transaction history"
            )

    # CLEAN EMPTY VALUES
    df["flags"] = df["flags"].replace("", "NORMAL")
    df["reasons"] = df["reasons"].replace("", "No unusual spending behavior detected")

    # SAVE
    df = df.sort_values("datetime")
    return df
