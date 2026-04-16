from __future__ import annotations

from pathlib import Path

import pandas as pd

from src.config import (
    DATASET_PATH,
    EXPECTED_COLUMNS,
    PROCESSED_DATASET_PATH,
    REQUIRED_CANONICAL_COLUMNS,
)
from src.data.preprocessing import build_processed_dataset


class DatasetValidationError(ValueError):
    """Raised when the EV dataset is missing or structurally incompatible."""


def _column_lookup(columns: list[str]) -> dict[str, str]:
    lookup: dict[str, str] = {}
    for canonical, aliases in EXPECTED_COLUMNS.items():
        for alias in aliases:
            if alias in columns:
                lookup[alias] = canonical
                break
    return lookup


def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    rename_map = _column_lookup(df.columns.tolist())
    return df.rename(columns=rename_map)


def validate_dataset(df: pd.DataFrame) -> None:
    missing = [column for column in REQUIRED_CANONICAL_COLUMNS if column not in df.columns]
    if missing:
        raise DatasetValidationError(
            "Dataset is missing required canonical columns: "
            + ", ".join(sorted(missing))
            + ". Check the Kaggle CSV and column aliases in src/config.py."
        )


def load_dataset(path: str | Path = DATASET_PATH) -> pd.DataFrame:
    dataset_path = Path(path)
    if not dataset_path.exists():
        raise FileNotFoundError(
            f"Dataset not found at {dataset_path}. Add the committed Kaggle CSV there to enable analysis."
        )

    df = pd.read_csv(dataset_path)
    normalized = normalize_columns(df)
    validate_dataset(normalized)
    return normalized


def build_processed_dataset_frame(path: str | Path = DATASET_PATH) -> pd.DataFrame:
    raw_dataset = load_dataset(path)
    return build_processed_dataset(raw_dataset)


def load_processed_dataset(path: str | Path = PROCESSED_DATASET_PATH) -> pd.DataFrame:
    dataset_path = Path(path)
    if not dataset_path.exists():
        raise FileNotFoundError(
            f"Processed dataset not found at {dataset_path}. Generate it with scripts/build_processed_dataset.py."
        )
    return pd.read_csv(dataset_path)
