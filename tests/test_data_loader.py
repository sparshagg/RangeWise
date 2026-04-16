from pathlib import Path

import pandas as pd
import pytest

from src.data.loader import DatasetValidationError, load_dataset, normalize_columns


def test_normalize_columns_maps_expected_aliases() -> None:
    df = pd.DataFrame(
        columns=[
            "Speed",
            "Acceleration",
            "Temperature",
            "Battery State",
            "Energy Consumption (kWh)",
        ]
    )

    normalized = normalize_columns(df)
    assert "speed" in normalized.columns
    assert "battery_state_pct" in normalized.columns
    assert "energy_consumption_kwh" in normalized.columns


def test_load_dataset_raises_for_missing_file(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError):
        load_dataset(tmp_path / "missing.csv")


def test_load_dataset_validates_required_columns(tmp_path: Path) -> None:
    dataset_path = tmp_path / "ev.csv"
    pd.DataFrame({"Speed": [10], "Acceleration": [1]}).to_csv(dataset_path, index=False)

    with pytest.raises(DatasetValidationError):
        load_dataset(dataset_path)


def test_load_dataset_accepts_valid_dataset(tmp_path: Path) -> None:
    dataset_path = tmp_path / "ev.csv"
    pd.DataFrame(
        {
            "Speed": [10],
            "Acceleration": [1.2],
            "Temperature": [38],
            "Battery State": [75],
            "Energy Consumption (kWh)": [15.4],
        }
    ).to_csv(dataset_path, index=False)

    loaded = load_dataset(dataset_path)
    assert list(loaded.columns) == [
        "speed",
        "acceleration",
        "temperature_c",
        "battery_state_pct",
        "energy_consumption_kwh",
    ]

