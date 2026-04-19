import pandas as pd

from src.analysis.dataset_range_model import build_dataset_multiplier


def test_exact_group_lookup_uses_exact_fallback(range_model_dataset: pd.DataFrame) -> None:
    result = build_dataset_multiplier(
        range_model_dataset,
        speed_level="City",
        driving_mode="Comfort",
        traffic_level="Moderate",
    )

    assert result.fallback_level == "exact"
    assert result.sample_count >= 20
    assert result.multiplier == 1.0


def test_sparse_group_falls_back_to_speed_mode(range_model_dataset: pd.DataFrame) -> None:
    result = build_dataset_multiplier(
        range_model_dataset,
        speed_level="Highway",
        driving_mode="Sport",
        traffic_level="High",
    )

    assert result.fallback_level == "speed_mode"
    assert result.sample_count >= 40


def test_sparse_group_can_fall_back_to_speed_only(range_model_dataset: pd.DataFrame) -> None:
    result = build_dataset_multiplier(
        range_model_dataset,
        speed_level="Local",
        driving_mode="Comfort",
        traffic_level="High",
    )

    assert result.fallback_level == "speed_only"
    assert result.sample_count >= 80


def test_eco_multiplier_exceeds_sport_for_same_band(range_model_dataset: pd.DataFrame) -> None:
    eco = build_dataset_multiplier(
        range_model_dataset,
        speed_level="City",
        driving_mode="Eco",
        traffic_level="No Traffic",
    )
    sport = build_dataset_multiplier(
        range_model_dataset,
        speed_level="City",
        driving_mode="Sport",
        traffic_level="High",
    )

    assert eco.multiplier > sport.multiplier
