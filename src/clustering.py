import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score


from config import (
    K_MIN, K_MAX, K_OPTIMAL,
    KMEANS_RANDOM_STATE, KMEANS_N_INIT,
    FIGURES_DIR, FIGURE_DPI, FIGURE_FORMAT,
)

def scale_rfm(rfm: pd.DataFrame) -> np.ndarray:
    """Standardize the three RFM columns to mean 0, std 1."""
    scaler = StandardScaler()
    scaled = scaler.fit_transform(rfm[["Recency", "Frequency", "Monetary"]])
    return scaled


def find_optimal_k(scaled: np.ndarray) -> None:
    """Run K-Means for a range of K, plot inertia (Elbow) and silhouette."""
    print("[clustering] Searching for optimal K...")
 
    inertias = []
    silhouettes = []
    k_range = range(K_MIN, K_MAX + 1)

    for k in k_range:
        km = KMeans(n_clusters=k, random_state=KMEANS_RANDOM_STATE, n_init=KMEANS_N_INIT)
        labels = km.fit_predict(scaled)
        inertias.append(km.inertia_)
        sil = silhouette_score(scaled, labels)
        silhouettes.append(sil)
        print(f"  K={k}:  inertia={km.inertia_:>12,.0f}   silhouette={sil:.3f}")

    # Comapre both metrics side by side
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))
 
    ax1.plot(list(k_range), inertias, marker="o", linewidth=2)
    ax1.set_title("Elbow Method (Inertia)")
    ax1.set_xlabel("Number of clusters (K)")
    ax1.set_ylabel("Inertia (within-cluster sum of squares)")
 
    ax2.plot(list(k_range), silhouettes, marker="o", linewidth=2, color="darkorange")
    ax2.set_title("Silhouette Score")
    ax2.set_xlabel("Number of clusters (K)")
    ax2.set_ylabel("Silhouette score (higher = better)")
 
    fig.tight_layout()
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    path = FIGURES_DIR / f"optimal_k.{FIGURE_FORMAT}"
    fig.savefig(path, dpi=FIGURE_DPI, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved: {path.name}")


def run_kmeans(rfm: pd.DataFrame, scaled: np.ndarray) -> pd.DataFrame:
    """Fit final K-Means with K_OPTIMAL and attach a Cluster column"""
    print(f"[clustering] Fitting final K-Means with K={K_OPTIMAL}...")

    km = KMeans(
        n_clusters=K_OPTIMAL,
        random_state=KMEANS_RANDOM_STATE,
        n_init=KMEANS_N_INIT
    )
    labels = km.fit_predict(scaled)

    rfm = rfm.copy()
    rfm["Cluster"] = labels
    
    # Report cluster sizes
    sizes = rfm["Cluster"].value_counts().sort_index()
    print("  Cluster sizes:")
    for cluster_id, count in sizes.items():
        pct = count / len(rfm) * 100
        print(f"    Cluster {cluster_id}: {count:>5,} customers ({pct:4.1f}%)")
 
    print("[clustering] Done.\n")
    return rfm