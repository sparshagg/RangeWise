"""
One-time ANFIS training script.

Run from the project root:
    python scripts/train_anfis.py

Generates models/anfis_weights.json.
Re-run whenever the dataset changes or you want to retrain.
"""

import sys
from pathlib import Path

# Allow running from project root without installing the package
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.config import ANFIS_WEIGHTS_PATH, DATASET_PATH
from src.data.loader import load_dataset
from src.neuro_fuzzy.training import save_weights, train_anfis


def main() -> None:
    print("=" * 60)
    print("RangeWise ANFIS Training")
    print("=" * 60)

    print(f"\nLoading dataset: {DATASET_PATH}")
    df = load_dataset(DATASET_PATH)
    print(f"Dataset loaded: {len(df):,} rows, {len(df.columns)} columns")

    print(f"\nTraining ANFIS (20 epochs, hybrid learning)...")
    anfis, metrics = train_anfis(df)

    final_train = metrics["train_mse"][-1]
    final_test = metrics["test_mse"][-1]
    print(f"\nTraining complete.")
    print(f"  Final train MSE : {final_train:.6f}")
    print(f"  Final test  MSE : {final_test:.6f}")

    save_weights(anfis, metrics, ANFIS_WEIGHTS_PATH)
    print("\nDone. You can now run: streamlit run src/app.py")


if __name__ == "__main__":
    main()
