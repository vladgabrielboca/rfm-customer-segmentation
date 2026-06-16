import pandas as pd


from config import (
    DATA_FILE,
    EXPECTED_COLUMNS,
    MAX_QUANTITY,
    MAX_UNITPRICE,
)


def load_raw() -> pd.DataFrame:
    """Read the raw Excel file from disk."""
    print(f"  Reading: {DATA_FILE}")
    df = pd.read_excel(DATA_FILE, engine="openpyxl")
    print(f"  Raw shape: {df.shape[0]:,} rows × {df.shape[1]} columns")
    return df


def validate_columns(df: pd.DataFrame) -> None:
    """Raise an error early if the file doesn't have the columns we expect."""
    missing = set(EXPECTED_COLUMNS) - set(df.columns)
    if missing:
        raise ValueError(f"Missing expected columns: {missing}")


def clean(df: pd.DataFrame) -> pd.DataFrame:
    """Apply all cleaning steps and return a clean DataFrame."""

    initial_rows_num = len(df)

    # Drop Missing CustomerID
    before = len(df)
    df = df.dropna(subset=["CustomerID"])
    print(f"  Drop missing CustomerID:  -{before - len(df):>7,} rows")

    # Drop Missing Description
    before = len(df)
    df = df.dropna(subset=["Description"])
    print(f"  Drop missing Description: -{before - len(df):>7,} rows")

    # Drop duplicates
    before = len(df)
    df = df.drop_duplicates()
    print(f"  Drop duplicates:          -{before - len(df):>7,} rows")

    # Drop returns (Quantity <= 0)
    before = len(df)
    df = df[df["Quantity"] > 0]
    print(f"  Drop returns (Qty <= 0):  -{before - len(df):>7,} rows")

    # Drop zero/negative UnitPrice
    before = len(df)
    df = df[df["UnitPrice"] > 0]
    print(f"  Drop zero price:          -{before - len(df):>7,} rows")

    # Apply limits to filter out extreme outliers in Quantity and UnitPrice
    before = len(df)
    df = df[(df["Quantity"] <= MAX_QUANTITY) & (df["UnitPrice"] <= MAX_UNITPRICE)]
    print(f"  Apply value limits:       -{before - len(df):>7,} rows")

    # Final cleanup: convert CustomerID to int and calculate TotalPrice
    df["CustomerID"] = df["CustomerID"].astype(int)
    df["TotalPrice"] = df["Quantity"] * df["UnitPrice"]

    # Sumarize the cleaning steps
    removed = initial_rows_num - len(df)
    percentage = removed / initial_rows_num * 100
    print(f"\n Final shape: {len(df):,} rows × {df.shape[1]} columns")
    print(f"  Total removed: {removed:,} rows ({percentage:.1f}% of raw data)")
    print(f"  Unique customers: {df['CustomerID'].nunique():,}")
    print(f" Date range: {df['InvoiceDate'].min().date()} to {df['InvoiceDate'].max().date()}")

    return df


def get_clean_data() -> pd.DataFrame:
    """Load, validate, and clean the data, returning a clean DataFrame."""
    df = load_raw()
    validate_columns(df)
    df = clean(df)
    return df

if __name__ == "__main__":
    df = get_clean_data()
    print(df[:1])