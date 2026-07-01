import pandas as pd


def compute_rfm(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate transaction-level data into one RFM row per customer"""

    print("[rfm] Computing scores...")

    reference_date = df["InvoiceDate"].max() + pd.Timedelta(days=1)
    print(f"  Reference date: {reference_date.date()}")

    rfm = df.groupby("CustomerID").agg(
        Recency = ("InvoiceDate", lambda x: (reference_date - x.max()).days),
        Frequency = ("InvoiceNo", "nunique"),
        Monetary = ("TotalPrice", "sum"),
    )

    print(f"  Computed RFM for {len(rfm):,} customers")

    assert (rfm["Frequency"] > 0).all(), "Found customer with Frequency <= 0"
    assert (rfm["Monetary"] > 0).all(),  "Found customer with Monetary <= 0"

    print ("[rfm] Done.\n")
    return rfm


def describe_rfm(rfm: pd.DataFrame) -> None:
    """Print descriptive statistics."""
    stats = rfm.describe().round(2)
    print(stats.to_string())