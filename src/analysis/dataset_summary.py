from __future__ import annotations

import pandas as pd

from src.data.preprocessing import add_uae_condition_labels, dataset_overview


def build_dataset_summary(df: pd.DataFrame) -> dict[str, object]:
    enriched = add_uae_condition_labels(df)
    summary = dataset_overview(enriched)

    if "uae_heat_band" in enriched.columns:
        heat_counts = enriched["uae_heat_band"].value_counts(dropna=False)
        summary["heat_band_counts"] = {
            str(index): int(value) for index, value in heat_counts.items() if str(index) != "nan"
        }

    for column in ("road_type", "weather_type", "driving_mode"):
        if column in enriched.columns:
            mode = enriched[column].mode(dropna=True)
            if not mode.empty:
                summary[f"top_{column}"] = str(mode.iloc[0])

    return summary


def build_energy_by_temperature(df: pd.DataFrame) -> pd.DataFrame:
    if "temperature_c" not in df.columns or "energy_consumption_kwh" not in df.columns:
        return pd.DataFrame(columns=["temperature_c", "energy_consumption_kwh"])

    binned = df.copy()
    binned["temp_bucket"] = pd.cut(
        binned["temperature_c"],
        bins=[-20, 20, 28, 36, 44, 60],
        labels=["-20-20", "21-28", "29-36", "37-44", "45-60"],
    )

    grouped = (
        binned.groupby("temp_bucket", observed=False)["energy_consumption_kwh"]
        .mean()
        .reset_index()
        .rename(columns={"temp_bucket": "temperature_c"})
    )
    grouped["energy_consumption_kwh"] = grouped["energy_consumption_kwh"].round(2)
    return grouped
