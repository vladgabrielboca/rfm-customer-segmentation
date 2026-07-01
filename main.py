import sys
from pathlib import Path
 
sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))
 
from load_data import get_clean_data
from eda import run_eda
from rfm import compute_rfm, describe_rfm
from clustering import scale_rfm, find_optimal_k, run_kmeans
from interpret import interpret_segments
from config import SEGMENTS_FILE

def main():
    print("=" * 60)
    print("  RFM CUSTOMER SEGMENTATION - PIPELINE START")
    print("=" * 60 + "\n")

    df = get_clean_data()
    run_eda(df)
    rfm = compute_rfm(df)
    describe_rfm(rfm)

    scaled = scale_rfm(rfm)
    find_optimal_k(scaled)
    rfm = run_kmeans(rfm, scaled)
    rfm = interpret_segments(rfm)

    SEGMENTS_FILE.parent.mkdir(parents=True, exist_ok=True)
    rfm.to_csv(SEGMENTS_FILE)
    print(f"[main] Final segments saved to: {SEGMENTS_FILE}")
 
    print("\n" + "=" * 60)
    print("  PIPELINE COMPLETE")
    print("=" * 60)
 
 
if __name__ == "__main__":
    main()