import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
 
from config import FIGURES_DIR, FIGURE_DPI, FIGURE_FORMAT

sns.set_theme(style="whitegrid", palette="muted")

def profile_clusters(rfm: pd.DataFrame) -> pd.DataFrame:
    """Compute the mean R/F/M and customer count for each cluster using original units (days, counts, £) for human interpretation"""
    profile = rfm.groupby("Cluster").agg(
        Recency=("Recency", "mean"),
        Frequency=("Frequency", "mean"),
        Monetary=("Monetary", "mean"),
        Count=("Recency", "size"),
    ).round(1)

    print("  ── Cluster profiles (original units) ─────────────────")
    print(profile.to_string())
    print("  ──────────────────────────────────────────────────────\n")
    return profile

def label_clusters(rfm: pd.DataFrame, profile: pd.DataFrame) -> pd.DataFrame:
    """Assign a business label to each cluster using rank-based scoring"""
    p = profile.copy()

    p["R_rank"] = p["Recency"].rank(ascending=False)
    p["F_rank"] = p["Frequency"].rank(ascending=True)
    p["M_rank"] = p["Monetary"].rank(ascending=True)
    p["Score"] = p["R_rank"] + p["F_rank"] + p["M_rank"]

    ordered = p.sort_values("Score", ascending=False).index.to_list()

    # Choose granularity based on K
    name_pools = {
        2: ["Champions", "At Risk"],
        3: ["Champions", "Loyal", "At Risk"],
        4: ["Champions", "Loyal", "Potential", "Lost"],
        5: ["Champions", "Loyal", "Potential", "Needs Attention", "Lost"],
    }

    names = name_pools.get(len(ordered),
                          [f"Segment {i + 1}" for i in range(ordered)])
    
    cluster_to_label = {cluster: name for cluster, name in zip(ordered, names)}
    print(f"  Cluster -> label mapping:")
    for cluster, label in cluster_to_label.items():
        print(f"    Cluster {cluster} -> {label}")
    print()

    rfm = rfm.copy()
    rfm["Label"] = rfm["Cluster"].map(cluster_to_label)
    return rfm

def _save(fig, name):
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    path = FIGURE_DPI / f"{name}.{FIGURE_FORMAT}"
    fig.savefig(path, dpi=FIGURE_DPI, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved: {path.name}")