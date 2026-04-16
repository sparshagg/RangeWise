from __future__ import annotations

import streamlit as st


def _format_delta(value: float, label: str) -> str:
    return f"{value:+.2f} km {label}"


def render_range_metrics(payload: dict[str, object]) -> None:
    col1, col2, col3 = st.columns(3)
    col1.metric("Claimed Remaining", f"{payload['claimed_remaining_km']} km")
    col2.metric(
        "Shown Range",
        f"{payload['shown_range_km']} km",
        _format_delta(float(payload["shown_range_km"]) - float(payload["claimed_remaining_km"]), "vs claimed"),
    )
    col3.metric(
        "Adjusted Range",
        f"{payload['adjusted_range_km']} km",
        _format_delta(float(payload["range_delta_vs_shown_km"]), "vs shown"),
    )

    st.caption(
        f"Dataset multiplier: {payload['dataset_multiplier']} | UAE fuzzy factor: {payload['fuzzy_adjustment_factor']}"
    )


def render_explanation_panel(payload: dict[str, object]) -> None:
    st.subheader("How The Estimate Was Built")
    st.write(payload["summary"])
    st.write(f"Dataset effect: {payload['dataset_summary_driver']}")
    st.write(f"Fuzzy UAE effect: {payload['fuzzy_summary_driver']}")
    st.write(
        "Lookup bucket: "
        f"{payload['dataset_bucket_used']} | proxy speed bucket: {payload['dataset_proxy_speed_level']} | "
        f"fallback: {payload['dataset_fallback_level']} | supporting rows: {payload['dataset_sample_count']}"
    )
    for driver in payload["drivers"]:
        st.write(f"- {driver}")


def render_dataset_summary(summary: dict[str, object]) -> None:
    st.subheader("Dataset Summary")
    if not summary:
        st.info("Dataset summary is unavailable until the Kaggle CSV is added.")
        return

    st.write(f"Rows: {summary.get('rows', 'n/a')}")
    st.write(f"Columns: {summary.get('columns', 'n/a')}")

    if "avg_energy_kwh" in summary:
        st.write(f"Average Energy Consumption: {summary['avg_energy_kwh']} kWh")
    if "avg_efficiency_km_per_kwh" in summary:
        st.write(f"Average Efficiency: {summary['avg_efficiency_km_per_kwh']} km/kWh")
    if "avg_speed_kmh" in summary:
        st.write(f"Average Speed: {summary['avg_speed_kmh']} km/h")
    if "temp_min_c" in summary and "temp_max_c" in summary:
        st.write(f"Temperature Range: {summary['temp_min_c']}C to {summary['temp_max_c']}C")
    if "top_driving_mode" in summary:
        st.write(f"Most Common Driving Mode: {summary['top_driving_mode']}")
    if "top_traffic_condition" in summary:
        st.write(f"Most Common Traffic Condition: {summary['top_traffic_condition']}")
    if "reference_bucket" in summary:
        st.write(f"Reference Bucket For Shown Range: {summary['reference_bucket']}")
    if "best_lookup_bucket" in summary:
        best = summary["best_lookup_bucket"]
        st.write(
            "Most efficient dataset bucket: "
            f"{best['speed_level']} / {best['driving_mode']} / {best['traffic_level']} "
            f"({best['median_km_per_kwh']} km/kWh)"
        )
    if "worst_lookup_bucket" in summary:
        worst = summary["worst_lookup_bucket"]
        st.write(
            "Least efficient dataset bucket: "
            f"{worst['speed_level']} / {worst['driving_mode']} / {worst['traffic_level']} "
            f"({worst['median_km_per_kwh']} km/kWh)"
        )


def render_dataset_lookup_table(lookup_table: object) -> None:
    st.subheader("Dataset Lookup Table")
    if getattr(lookup_table, "empty", True):
        st.info("Lookup table is unavailable until the dataset is loaded.")
        return
    st.dataframe(lookup_table, hide_index=True, use_container_width=True)
