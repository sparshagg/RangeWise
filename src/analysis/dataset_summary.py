from __future__ import annotations

import pandas as pd

from src.analysis.dataset_range_model import build_efficiency_lookup_table
from src.config import DATASET_DRIVING_MODE_LABELS, DATASET_TRAFFIC_CONDITION_LABELS, REFERENCE_RANGE_BUCKET
from src.data.preprocessing import add_range_model_labels, add_uae_condition_labels, dataset_overview


def build_dataset_summary(df: pd.DataFrame) -> dict[str, object]:
    enriched = add_uae_condition_labels(add_range_model_labels(df))
    summary = dataset_overview(enriched)

    if "uae_heat_band" in enriched.columns:
        heat_counts = enriched["uae_heat_band"].value_counts(dropna=False)
        summary["heat_band_counts"] = {
            str(index): int(value) for index, value in heat_counts.items() if str(index) != "nan"
        }

    if "speed" in enriched.columns:
        summary["avg_speed_kmh"] = round(float(enriched["speed"].mean()), 2)

    if "driving_mode" in enriched.columns:
        mode = enriched["driving_mode"].mode(dropna=True)
        if not mode.empty:
            summary["top_driving_mode"] = DATASET_DRIVING_MODE_LABELS.get(
                int(mode.iloc[0]), str(mode.iloc[0])
            )

    if "traffic_level" in enriched.columns:
        mode = enriched["traffic_level"].mode(dropna=True)
        if not mode.empty:
            summary["top_traffic_condition"] = DATASET_TRAFFIC_CONDITION_LABELS.get(
                int(mode.iloc[0]), str(mode.iloc[0])
            )

    lookup_table = build_efficiency_lookup_table(df)
    if not lookup_table.empty:
        summary["lookup_rows"] = int(len(lookup_table))
        summary["reference_bucket"] = " / ".join(REFERENCE_RANGE_BUCKET)
        summary["best_lookup_bucket"] = lookup_table.sort_values(
            "median_km_per_kwh", ascending=False
        ).iloc[0].to_dict()
        summary["worst_lookup_bucket"] = lookup_table.sort_values(
            "median_km_per_kwh", ascending=True
        ).iloc[0].to_dict()

    return summary


def build_energy_by_speed(df: pd.DataFrame) -> pd.DataFrame:
    enriched = add_range_model_labels(df)
    if "speed_level" not in enriched.columns or "km_per_kwh" not in enriched.columns:
        return pd.DataFrame(columns=["speed_level", "km_per_kwh"])

    grouped = (
        enriched.groupby("speed_level", observed=False)["km_per_kwh"]
        .mean()
        .reset_index()
    )
    grouped["km_per_kwh"] = grouped["km_per_kwh"].round(2)
    grouped = grouped.dropna(subset=["speed_level"])
    return grouped
