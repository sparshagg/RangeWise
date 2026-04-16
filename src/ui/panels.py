from __future__ import annotations

import streamlit as st


def render_range_metrics(payload: dict[str, object]) -> None:
    col1, col2, col3 = st.columns(3)
    col1.metric("Baseline Remaining Range", f"{payload['baseline_remaining_km']} km")
    col2.metric("Adjusted Range", f"{payload['adjusted_range_km']} km")
    col3.metric("Range Difference", f"{payload['range_delta_km']} km")

    st.caption(f"Adjustment factor: {payload['adjustment_factor']}")


def render_explanation_panel(payload: dict[str, object]) -> None:
    st.subheader("Why The Range Changed")
    st.write(payload["summary"])
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
    if "temp_min_c" in summary and "temp_max_c" in summary:
        st.write(f"Temperature Range: {summary['temp_min_c']}C to {summary['temp_max_c']}C")
    if "top_road_type" in summary:
        st.write(f"Most Common Road Type: {summary['top_road_type']}")
    if "top_weather_type" in summary:
        st.write(f"Most Common Weather Type: {summary['top_weather_type']}")

