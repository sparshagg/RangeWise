from __future__ import annotations

import pandas as pd

from src.config import (
    DATASET_DRIVING_MODE_LABELS,
    DATASET_TRAFFIC_CONDITION_LABELS,
    SPEED_LEVEL_BINS,
    SPEED_LEVEL_LABELS,
)


def add_uae_condition_labels(df: pd.DataFrame) -> pd.DataFrame:
    enriched = df.copy()

    if "temperature_c" in enriched.columns:
        enriched["uae_heat_band"] = pd.cut(
            enriched["temperature_c"],
            bins=[-100, 28, 40, 100],
            labels=["Mild", "Warm", "Hot"],
        )

    if "traffic_level" in enriched.columns:
        numeric = pd.to_numeric(enriched["traffic_level"], errors="coerce")
        if numeric.notna().any():
            enriched["traffic_band"] = pd.cut(
                numeric,
                bins=[-1, 3.5, 6.5, 10.5],
                labels=["Light", "Moderate", "Heavy"],
            )

    return enriched


def add_range_model_labels(df: pd.DataFrame) -> pd.DataFrame:
    enriched = df.copy()

    if {"distance_travelled_km", "energy_consumption_kwh"}.issubset(enriched.columns):
        distance = pd.to_numeric(enriched["distance_travelled_km"], errors="coerce")
        energy = pd.to_numeric(enriched["energy_consumption_kwh"], errors="coerce")
        valid_energy = energy.where(energy > 0)
        enriched["km_per_kwh"] = distance / valid_energy

    if "speed" in enriched.columns:
        speed = pd.to_numeric(enriched["speed"], errors="coerce")
        enriched["speed_level"] = pd.cut(
            speed,
            bins=SPEED_LEVEL_BINS,
            labels=SPEED_LEVEL_LABELS,
            include_lowest=True,
        )

    if "driving_mode" in enriched.columns:
        driving_mode = pd.to_numeric(enriched["driving_mode"], errors="coerce")
        enriched["driving_mode_label"] = driving_mode.map(DATASET_DRIVING_MODE_LABELS)

    if "traffic_level" in enriched.columns:
        traffic_level = pd.to_numeric(enriched["traffic_level"], errors="coerce")
        enriched["traffic_level_label"] = traffic_level.map(DATASET_TRAFFIC_CONDITION_LABELS)

    return enriched


def build_processed_dataset(df: pd.DataFrame) -> pd.DataFrame:
    enriched = add_uae_condition_labels(add_range_model_labels(df))

    preferred_columns = [
        "vehicle_id",
        "timestamp",
        "speed",
        "speed_level",
        "acceleration",
        "driving_mode",
        "driving_mode_label",
        "traffic_level",
        "traffic_level_label",
        "temperature_c",
        "uae_heat_band",
        "battery_state_pct",
        "distance_travelled_km",
        "energy_consumption_kwh",
        "km_per_kwh",
    ]
    selected_columns = [column for column in preferred_columns if column in enriched.columns]
    processed = enriched[selected_columns].copy()

    if "km_per_kwh" in processed.columns:
        processed["km_per_kwh"] = processed["km_per_kwh"].round(3)

    return processed


def dataset_overview(df: pd.DataFrame) -> dict[str, object]:
    overview: dict[str, object] = {
        "rows": int(len(df)),
        "columns": int(len(df.columns)),
    }

    if "energy_consumption_kwh" in df.columns:
        overview["avg_energy_kwh"] = round(float(df["energy_consumption_kwh"].mean()), 2)

    if "temperature_c" in df.columns:
        overview["temp_min_c"] = round(float(df["temperature_c"].min()), 1)
        overview["temp_max_c"] = round(float(df["temperature_c"].max()), 1)

    if "km_per_kwh" in df.columns:
        overview["avg_efficiency_km_per_kwh"] = round(float(df["km_per_kwh"].mean()), 2)

    return overview
