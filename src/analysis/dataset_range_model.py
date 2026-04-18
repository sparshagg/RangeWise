from __future__ import annotations

from dataclasses import dataclass

import pandas as pd

from src.config import (
    EXACT_GROUP_MIN_COUNT,
    REFERENCE_RANGE_BUCKET,
    SPEED_LEVEL_EXTRAPOLATION,
    SPEED_LEVEL_PROXY,
    SPEED_MIN_COUNT,
    SPEED_MODE_MIN_COUNT,
)
from src.data.preprocessing import add_range_model_labels


@dataclass(frozen=True)
class DatasetRangeEstimate:
    multiplier: float
    selected_efficiency: float
    reference_efficiency: float
    fallback_level: str
    proxy_speed_level: str
    sample_count: int


def _prepare_lookup_frame(df: pd.DataFrame) -> pd.DataFrame:
    enriched = add_range_model_labels(df)
    required_columns = [
        "km_per_kwh",
        "speed_level",
        "driving_mode_label",
        "traffic_level_label",
    ]
    available = enriched.dropna(subset=required_columns).copy()
    return available[available["km_per_kwh"] > 0]


def _build_reference_efficiency(df: pd.DataFrame) -> float:
    speed_level, driving_mode, traffic_level = REFERENCE_RANGE_BUCKET
    exact_reference = df[
        (df["speed_level"] == speed_level)
        & (df["driving_mode_label"] == driving_mode)
        & (df["traffic_level_label"] == traffic_level)
    ]
    if not exact_reference.empty:
        return float(exact_reference["km_per_kwh"].median())
    return float(df["km_per_kwh"].median())


def build_dataset_multiplier(
    df: pd.DataFrame,
    *,
    speed_level: str,
    driving_mode: str,
    traffic_level: str,
) -> DatasetRangeEstimate:
    lookup_df = _prepare_lookup_frame(df)
    if lookup_df.empty:
        return DatasetRangeEstimate(
            multiplier=1.0,
            selected_efficiency=1.0,
            reference_efficiency=1.0,
            fallback_level="unavailable",
            proxy_speed_level=speed_level,
            sample_count=0,
        )

    reference_efficiency = _build_reference_efficiency(lookup_df)
    proxy_speed_level = SPEED_LEVEL_PROXY[speed_level]

    exact_group = lookup_df[
        (lookup_df["speed_level"] == proxy_speed_level)
        & (lookup_df["driving_mode_label"] == driving_mode)
        & (lookup_df["traffic_level_label"] == traffic_level)
    ]
    if len(exact_group) >= EXACT_GROUP_MIN_COUNT:
        selected_efficiency = float(exact_group["km_per_kwh"].median())
        fallback_level = "exact"
        sample_count = int(len(exact_group))
    else:
        speed_mode_group = lookup_df[
            (lookup_df["speed_level"] == proxy_speed_level)
            & (lookup_df["driving_mode_label"] == driving_mode)
        ]
        if len(speed_mode_group) >= SPEED_MODE_MIN_COUNT:
            selected_efficiency = float(speed_mode_group["km_per_kwh"].median())
            fallback_level = "speed_mode"
            sample_count = int(len(speed_mode_group))
        else:
            speed_group = lookup_df[lookup_df["speed_level"] == proxy_speed_level]
            if len(speed_group) >= SPEED_MIN_COUNT:
                selected_efficiency = float(speed_group["km_per_kwh"].median())
                fallback_level = "speed_only"
                sample_count = int(len(speed_group))
            else:
                selected_efficiency = float(lookup_df["km_per_kwh"].median())
                fallback_level = "global"
                sample_count = int(len(lookup_df))

    selected_efficiency *= SPEED_LEVEL_EXTRAPOLATION[speed_level]
    multiplier = selected_efficiency / reference_efficiency if reference_efficiency else 1.0

    return DatasetRangeEstimate(
        multiplier=multiplier,
        selected_efficiency=selected_efficiency,
        reference_efficiency=reference_efficiency,
        fallback_level=fallback_level,
        proxy_speed_level=proxy_speed_level,
        sample_count=sample_count,
    )


def build_efficiency_lookup_table(df: pd.DataFrame) -> pd.DataFrame:
    lookup_df = _prepare_lookup_frame(df)
    if lookup_df.empty:
        return pd.DataFrame(
            columns=[
                "speed_level",
                "driving_mode",
                "traffic_level",
                "sample_count",
                "median_km_per_kwh",
            ]
        )

    grouped = (
        lookup_df.groupby(
            ["speed_level", "driving_mode_label", "traffic_level_label"], observed=False
        )["km_per_kwh"]
        .agg(["count", "median"])
        .reset_index()
        .rename(
            columns={
                "driving_mode_label": "driving_mode",
                "traffic_level_label": "traffic_level",
                "count": "sample_count",
                "median": "median_km_per_kwh",
            }
        )
    )
    grouped["median_km_per_kwh"] = grouped["median_km_per_kwh"].round(2)
    grouped = grouped[grouped["sample_count"] > 0]
    return grouped
