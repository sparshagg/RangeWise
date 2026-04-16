from pathlib import Path

import pandas as pd
import pytest

from src.data.loader import (
    DatasetValidationError,
    build_processed_dataset_frame,
    load_dataset,
    load_processed_dataset,
    normalize_columns,
)


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
            "Speed_kmh": [10],
            "Acceleration_ms2": [1.2],
            "Temperature_C": [38],
            "Battery_State_%": [75],
            "Energy_Consumption_kWh": [15.4],
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


def test_load_dataset_accepts_real_dataset_header_shape(tmp_path: Path) -> None:
    dataset_path = tmp_path / "ev_real_shape.csv"
    pd.DataFrame(
        {
            "Vehicle_ID": [1102],
            "Timestamp": ["2024-01-01 00:00:00"],
            "Speed_kmh": [111.5],
            "Acceleration_ms2": [-2.7],
            "Battery_State_%": [30.4],
            "Battery_Voltage_V": [378.0],
            "Battery_Temperature_C": [25.3],
            "Driving_Mode": [2],
            "Road_Type": [1],
            "Traffic_Condition": [1],
            "Slope_%": [6.8],
            "Weather_Condition": [4],
            "Temperature_C": [0.7],
            "Humidity_%": [42.1],
            "Wind_Speed_ms": [7.8],
            "Tire_Pressure_psi": [31.1],
            "Vehicle_Weight_kg": [1822.9],
            "Distance_Travelled_km": [20.7],
            "Energy_Consumption_kWh": [12.0],
        }
    ).to_csv(dataset_path, index=False)

    loaded = load_dataset(dataset_path)
    assert "speed" in loaded.columns
    assert "traffic_level" in loaded.columns
    assert "distance_travelled_km" in loaded.columns


def test_build_processed_dataset_frame_adds_derived_columns(tmp_path: Path) -> None:
    dataset_path = tmp_path / "ev_processed.csv"
    pd.DataFrame(
        {
            "Vehicle_ID": [1102],
            "Timestamp": ["2024-01-01 00:00:00"],
            "Speed_kmh": [111.5],
            "Acceleration_ms2": [-2.7],
            "Battery_State_%": [30.4],
            "Driving_Mode": [2],
            "Traffic_Condition": [1],
            "Temperature_C": [34.0],
            "Distance_Travelled_km": [20.7],
            "Energy_Consumption_kWh": [12.0],
        }
    ).to_csv(dataset_path, index=False)

    processed = build_processed_dataset_frame(dataset_path)
    assert "speed_level" in processed.columns
    assert "driving_mode_label" in processed.columns
    assert "traffic_level_label" in processed.columns
    assert "km_per_kwh" in processed.columns


def test_load_processed_dataset_reads_generated_csv(tmp_path: Path) -> None:
    dataset_path = tmp_path / "processed.csv"
    pd.DataFrame(
        {
            "speed": [60],
            "speed_level": ["City"],
            "km_per_kwh": [3.2],
        }
    ).to_csv(dataset_path, index=False)

    loaded = load_processed_dataset(dataset_path)
    assert list(loaded.columns) == ["speed", "speed_level", "km_per_kwh"]
