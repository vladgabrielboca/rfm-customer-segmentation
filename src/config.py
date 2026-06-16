from pathlib import Path
 
# ── Paths ──────────────────────────────────────────────────────────────────────
 
ROOT = Path(__file__).resolve().parent.parent  # project root
 
DATA_RAW       = ROOT / "data" / "raw"
DATA_FILE      = DATA_RAW / "Online_Retail.xlsx"
 
OUTPUTS        = ROOT / "outputs"
FIGURES_DIR    = OUTPUTS / "figures"
SEGMENTS_FILE  = OUTPUTS / "rfm_segments.csv"
 
# ── Data cleaning ──────────────────────────────────────────────────────────────
 
# Coloanele pe care le asteptam in dataset
EXPECTED_COLUMNS = [
    "InvoiceNo", "StockCode", "Description", "Quantity",
    "InvoiceDate", "UnitPrice", "CustomerID", "Country"
]
 
# Filtrare outlieri: comenzi cu cantitate sau pret prea mari
MAX_QUANTITY  = 10_000
MAX_UNITPRICE = 5_000
 
# ── Clustering ─────────────────────────────────────────────────────────────────
 
# Range de K pentru Elbow Method
K_MIN = 2
K_MAX = 10
 
# K-ul ales final (actualizat dupa ce vedem graficul Elbow)
K_OPTIMAL = 4
 
KMEANS_RANDOM_STATE = 42
KMEANS_N_INIT       = 10   # cate initializari face K-Means (ia cel mai bun)
 
# ── Classifier ─────────────────────────────────────────────────────────────────
 
TEST_SIZE          = 0.20
CLASSIFIER_RANDOM_STATE = 42
 
# ── Plotting ───────────────────────────────────────────────────────────────────
 
FIGURE_DPI = 150
FIGURE_FORMAT = "png"