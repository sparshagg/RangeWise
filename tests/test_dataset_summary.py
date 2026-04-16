import pandas as pd

from src.analysis.dataset_range_model import build_efficiency_lookup_table
from src.analysis.dataset_summary import build_dataset_summary, build_energy_by_speed


def test_build_dataset_summary_includes_speed_and_labels() -> None:
    df = pd.DataFrame(
        {
            "speed": [25, 60, 95],
            "temperature_c": [24, 34, 40],
            "energy_consumption_kwh": [6.1, 8.4, 10.8],
            "distance_travelled_km": [18.3, 25.2, 25.9],
            "driving_mode": [1, 2, 3],
            "traffic_level": [1, 2, 3],
        }
    )

    summary = build_dataset_summary(df)
    assert summary["avg_speed_kmh"] == 60.0
    assert summary["top_driving_mode"] == "Eco"
    assert summary["top_traffic_condition"] == "No Traffic"
    assert "avg_efficiency_km_per_kwh" in summary


def test_build_energy_by_speed_returns_speed_bands() -> None:
    df = pd.DataFrame(
        {
            "speed": [20, 45, 75, 105],
            "distance_travelled_km": [12, 24, 30, 31],
            "energy_consumption_kwh": [5.5, 7.2, 9.1, 11.8],
        }
    )

    result = build_energy_by_speed(df)
    assert not result.empty
    assert "speed_level" in result.columns
    assert "km_per_kwh" in result.columns


def test_build_efficiency_lookup_table_returns_grouped_rows(range_model_dataset: pd.DataFrame) -> None:
    result = build_efficiency_lookup_table(range_model_dataset)

    assert not result.empty
    assert "median_km_per_kwh" in result.columns
