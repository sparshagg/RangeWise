from __future__ import annotations

import pandas as pd

from src.config import DATASET_DRIVING_MODE_LABELS, DATASET_TRAFFIC_CONDITION_LABELS
from src.data.preprocessing import add_uae_condition_labels, dataset_overview


def build_dataset_summary(df: pd.DataFrame) -> dict[str, object]:
    enriched = add_uae_condition_labels(df)
    summary = dataset_overview(df)

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

    return summary


def build_energy_by_speed(df: pd.DataFrame) -> pd.DataFrame:
    if "speed" not in df.columns or "energy_consumption_kwh" not in df.columns:
        return pd.DataFrame(columns=["speed_band", "energy_consumption_kwh"])

    binned = df.copy()
    binned["speed_band"] = pd.cut(
        binned["speed"],
        bins=[0, 30, 60, 90, 120],
        labels=["0-30", "31-60", "61-90", "91-120"],
        include_lowest=True,
    )

    grouped = (
        binned.groupby("speed_band", observed=False)["energy_consumption_kwh"]
        .mean()
        .reset_index()
    )
    grouped["energy_consumption_kwh"] = grouped["energy_consumption_kwh"].round(2)
    return grouped
