import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

np.random.seed(42)
dates = pd.date_range(start="2020-12-01", end="2021-12-31", freq="D")

PRODUCTS = [
    "WHITE HANGING HEART T-LIGHT HOLDER",
    "REGENCY CAKESTAND 3 TIER",
    "JUMBO BAG RED RETROSPOT",
    "PARTY BUNTING",
    "LUNCH BAG RED RETROSPOT",
    "SET OF 3 CAKE TINS PANTRY DESIGN",
    "GLASS STAR FROSTED T-LIGHT HOLDER",
    "ASSORTED COLOUR BIRD ORNAMENT",
    "PINK CHERRY LIGHTS",
    "HAND WARMER UNION JACK",
    "WOODEN PICTURE FRAME WHITE FINISH",
    "SMALL POPCORN HOLDER",
    "VINTAGE HEADS AND TAILS CARD GAME",
    "RED RETROSPOT ROUND CAKE TINS",
    "ALARM CLOCK BAKELIKE GREEN",
]

COUNTRIES = [
    "UNITED KINGDOM",
    "ROMANIA",
    "AUSTRIA",
    "FRANCE",
    "BULGARIA",
    "GERMANY",
    "SPAIN",
    "PORTUGAL",
    "DENMARK",
    "ICELAND",
    "GREECE"
]

N_CUSTOMERS = 400
customer_ids = [f"C{str(i).zfill(5)}" for i in range(1, N_CUSTOMERS + 1)]
orders_per_customer = np.random.exponential(scale=4, size=N_CUSTOMERS).astype(int) + 1
orders_per_customer = np.clip(orders_per_customer, 1, 60)

rows = []
invoice_counter = 1
for cid, n_orders in zip(customer_ids, orders_per_customer):
    for _ in range(n_orders):
        invoice_no = f"INV{str(invoice_counter).zfill(6)}"
        invoice_counter += 1
        date = np.random.choice(dates)
        for _ in range(np.random.randint(1, 6)):
            rows.append({
                "InvoiceDate": date,
                "InvoicesNo":  invoice_no,
                "CustomerID":  cid,
                "Description": np.random.choice(PRODUCTS),
                "Country": np.random.choice(COUNTRIES),
                "TotalPrice":  round(np.random.exponential(scale=50), 2)
            })

df = pd.DataFrame(rows)

def plot_monthly_revenue(df: pd.DataFrame) -> None:
    """Line plot: total revenue aggregated by month."""
    monthly = (
        df.groupby(df["InvoiceDate"].dt.to_period("M"))["TotalPrice"]
        .sum()
        .reset_index()
    )
    monthly["InvoiceDate"] = monthly["InvoiceDate"].dt.to_timestamp()
    print(monthly[:20])

    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(monthly["InvoiceDate"], monthly["TotalPrice"], marker="o", linewidth=2)
    ax.set_title("Monthly Revenue", fontsize=14)
    ax.set_xlabel("Month")
    ax.set_ylabel("Revenue (£)")
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"£{x:,.0f}"))
    fig.tight_layout()
    plt.show()

def plot_top10_products(df: pd.DataFrame) -> None:
    """Horizontal bar chart: top 10 products by total revenue."""
    top10 = (
        df.groupby("Description")["TotalPrice"]
        .sum()
        .nlargest(10)
        .sort_values()
    )
    print(top10)

    fig, ax = plt.subplots(figsize=(9, 5))
    top10.plot(kind="barh", ax=ax, color=sns.color_palette("muted")[0])
    ax.set_title("Top 10 Products by Revenue", fontsize=14)
    ax.set_xlabel("Revenue (£)")
    ax.set_ylabel("")
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"£{x:,.0f}"))
    fig.tight_layout()
    plt.show()

def plot_top10_countries(df: pd.DataFrame) -> None:
    """Horizontal bar chart: top 10 countries by total revenue, excluding UK."""
    top10 = (
        df[df["Country"] != "UNITED KINGDOM"]
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
    plt.show()

def orders_by_customer(df: pd.DataFrame) -> None:
    """Histogram: how many distinct invoices does each customer have?"""
    orders = df.groupby("CustomerID")["InvoicesNo"].nunique()
    print(type(orders))

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.hist(orders, bins=50, color=sns.color_palette("muted")[2], edgecolor="white")
    ax.set_title("Distribution of Orders per Customer", fontsize=14)
    ax.set_xlabel("Number of Orders")
    ax.set_ylabel("Number of Customers")
    ax.set_xlim(0, orders.quantile(0.99))   # zoom in: cut top 1% outliers visually
    fig.tight_layout()
    # plt.show()

# plot_monthly_revenue(df)
# plot_top10_products(df)
# plot_top10_countries(df)
orders_by_customer(df)