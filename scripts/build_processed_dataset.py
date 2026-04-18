from __future__ import annotations

from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.config import PROCESSED_DATASET_PATH
from src.data.loader import build_processed_dataset_frame


def main() -> None:
    processed_df = build_processed_dataset_frame()
    output_path = Path(PROCESSED_DATASET_PATH)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    processed_df.to_csv(output_path, index=False)


if __name__ == "__main__":
    main()
