from pathlib import Path
 
# ── Paths ──────────────────────────────────────────────────────────────────────
 
ROOT = Path(__file__).resolve().parent.parent  # project root
 
DATA_RAW       = ROOT / "data" / "raw"
DATA_FILE      = DATA_RAW / "Online_Retail.xlsx"
 
OUTPUTS        = ROOT / "outputs"
FIGURES_DIR    = OUTPUTS / "figures"
SEGMENTS_FILE  = OUTPUTS / "rfm_segments.csv"
 
# ── Data cleaning ──────────────────────────────────────────────────────────────
 
EXPECTED_COLUMNS = [
    "InvoiceNo", "StockCode", "Description", "Quantity",
    "InvoiceDate", "UnitPrice", "CustomerID", "Country"
]
 
# ── Filtering ─────────────────────────────────────────────────────────────────
MAX_QUANTITY  = 10_000
MAX_UNITPRICE = 5_000
 
# ── Clustering ─────────────────────────────────────────────────────────────────
 
K_MIN = 2
K_MAX = 10
 
K_OPTIMAL = 4
 
KMEANS_RANDOM_STATE = 42
KMEANS_N_INIT       = 10
 
# ── Classifier ─────────────────────────────────────────────────────────────────
 
TEST_SIZE          = 0.20
CLASSIFIER_RANDOM_STATE = 42
 
# ── Plotting ───────────────────────────────────────────────────────────────────
 
FIGURE_DPI = 150
FIGURE_FORMAT = "png"