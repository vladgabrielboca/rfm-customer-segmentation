import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import pandas as pd

from config import FIGURES_DIR, FIGURE_DPI, FIGURE_FORMAT

# Styling for plots

sns.set_theme(style="whitegrid", palette="muted")
FIGURES_DIR.mkdir(parents=True, exist_ok=True)

def _save(fig: plt.Figure, name: str) -> None:
    """Save a figure to the figures directory."""
    path = FIGURES_DIR / f"{name}.{FIGURE_FORMAT}"
    fig.savefig(path, dpi=FIGURE_DPI, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved: {path.name}")

# Individual plots

def plot_monthly_revenue(df: pd.DataFrame) -> None:
    """Line plot: total revenue aggregated by month."""
    monthly = (
        df.groupby(df["InvoiceDate"].dt.to_period("M"))["TotalPrice"]
        .sum()
        .reset_index()
    )
    monthly["InvoiceDate"] = monthly["InvoiceDate"].dt.to_timestamp()

    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(monthly["InvoiceDate"], monthly["TotalPrice"], marker="o", linewidth=2)
    ax.set_title("Monthly Revenue", fontsize=14)
    ax.set_xlabel("Month")
    ax.set_ylabel("Revenue (£)")
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"£{x:,.0f}"))
    fig.tight_layout()
    _save(fig, "monthly_revenue")

def plot_top10_products(df: pd.DataFrame) -> None:
    """Horizontal bar chart: top 10 products by total revenue."""
    top10 = (
        df.groupby("Description")["TotalPrice"]
        .sum()
        .nlargest(10)
        .sort_values()
    )

    fig, ax = plt.subplots(figsize=(9, 5))
    top10.plot(kind="barh", ax=ax, color=sns.color_palette("muted")[0])
    ax.set_title("Top 10 Products by Revenue", fontsize=14)
    ax.set_xlabel("Revenue (£)")
    ax.set_ylabel("")
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"£{x:,.0f}"))
    fig.tight_layout()
    _save(fig, "top10_products")

def plot_top10_countries(df: pd.DataFrame) -> None:
    """Horizontal bar chart: top 10 countries by total revenue, excluding UK."""
    top10 = (
        df[df["Country"] != "United Kingdom"]
        .groupby("Country")["TotalPrice"]
        .sum()
        .nlargest(10)
        .sort_values()
    )

    fig, ax = plt.subplots(figsize=(9, 5))
    top10.plot(kind="barh", ax=ax, color=sns.color_palette("muted")[0])
    ax.set_title("Top 10 Countries by Revenue", fontsize=14)
    ax.set_xlabel("Revenue (£)")
    ax.set_ylabel("")
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"£{x:,.0f}"))
    fig.tight_layout()
    _save(fig, "top10_countries")

def plot_orders_per_customer(df: pd.DataFrame) -> None:
    """Histogram: how many distinct invoices does each customer have?"""
    orders = df.groupby("CustomerID")["InvoicesNo"].nunique()

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.hist(orders, bins=50, color=sns.color_palette("muted")[2], edgecolor="white")
    ax.set_title("Distribution of Orders per Customer", fontsize=14)
    ax.set_xlabel("Number of Orders")
    ax.set_ylabel("Number of Customers")
    ax.set_xlim(0, orders.quantile(0.99))   # zoom in: cut top 1% outliers visually
    fig.tight_layout()
    _save(fig, "orders_per_customer")

def plot_revenue_per_customer(df: pd.DataFrame) -> None:
    """Histogram: total spend distribution across customers."""
    revenue = df.groupby("CustomerID")["TotalPrice"].sum()

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.hist(revenue, bins=50, color=sns.color_palette("muted")[3], edgecolor="white")
    ax.set_title("Distribution of Total Revenue per Customer", fontsize=14)
    ax.set_xlabel("Total Spend (£)")
    ax.set_ylabel("Number of Customers")
    ax.set_xlim(0, revenue.quantile(0.99))  # zoom in: cut top 1% outliers visually
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"£{x:,.0f}"))
    fig.tight_layout()
    _save(fig, "revenue_per_customer")

def print_summary(df: pd.DataFrame) -> None:
    """Print high-level summary statistics to the console."""
    print("  ── Dataset overview ──────────────────────────────────")
    print(f"  Transactions:      {len(df):>10,}")
    print(f"  Unique customers:  {df['CustomerID'].nunique():>10,}")
    print(f"  Unique products:   {df['Description'].nunique():>10,}")
    print(f"  Unique countries:  {df['Country'].nunique():>10,}")
    print(f"  Date range:        {df['InvoiceDate'].min().date()} → {df['InvoiceDate'].max().date()}")
    print(f"  Total revenue:     £{df['TotalPrice'].sum():>12,.2f}")
    print(f"  Avg order value:   £{df.groupby('InvoiceNo')['TotalPrice'].sum().mean():>12,.2f}")
    print("  ──────────────────────────────────────────────────────")


# ── Main entry point ───────────────────────────────────────────────────────────

def run_eda(df: pd.DataFrame) -> None:
    """Run all EDA steps."""
    print("[eda] Running exploratory data analysis...")
    print_summary(df)
    plot_monthly_revenue(df)
    plot_top10_products(df)
    plot_top10_countries(df)
    plot_orders_per_customer(df)
    plot_revenue_per_customer(df)
    print("[eda] Done.\n")