import pandas as pd

def feature_engineering(data):

    df = data.copy()

    df["balance_diff_org"] = df["oldbalanceOrg"] - df["newbalanceOrig"]
    df["balance_diff_dest"] = df["newbalanceDest"] - df["oldbalanceDest"]

    df["amount_ratio"] = df["amount"] / (df["oldbalanceOrg"] + 1)

    df["account_drained"] = (df["newbalanceOrig"] == 0).astype(int)

    df["hour"] = df["step"] % 24

    df["is_night"] = ((df["hour"] < 6) | (df["hour"] > 22)).astype(int)

    df["suspicious_balance"] = (
        (df["oldbalanceOrg"] > 0) &
        (df["newbalanceOrig"] == 0)
    ).astype(int)

    df["high_risk_type"] = df["type"].isin(
        ["TRANSFER","CASH_OUT"]
    ).astype(int)

    df = df.drop(columns=["nameOrig","nameDest"], errors="ignore")

    return df