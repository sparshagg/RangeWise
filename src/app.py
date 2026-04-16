from __future__ import annotations

from pathlib import Path

import pandas as pd
import streamlit as st

from src.analysis.dataset_summary import build_dataset_summary, build_energy_by_speed
from src.config import DATASET_PATH
from src.data.loader import DatasetValidationError, load_dataset
from src.fuzzy.inference import predict_adjusted_range
from src.ui.charts import build_energy_profile_figure, build_range_comparison_figure
from src.ui.controls import UserInputs, render_sidebar_controls
from src.ui.panels import render_dataset_summary, render_explanation_panel, render_range_metrics


def build_dashboard_payload(user_inputs: UserInputs) -> dict[str, object]:
    return predict_adjusted_range(
        manufacturer_range_km=user_inputs.manufacturer_range_km,
        battery_pct=user_inputs.battery_pct,
        temperature_c=user_inputs.temperature_c,
        ac_intensity=user_inputs.ac_intensity,
        speed_kmh=user_inputs.speed_kmh,
        driving_mode=user_inputs.driving_mode,
        traffic_condition=user_inputs.traffic_condition,
    )


def load_dashboard_dataset(dataset_path: str | Path = DATASET_PATH) -> tuple[pd.DataFrame | None, str | None]:
    try:
        return load_dataset(dataset_path), None
    except (FileNotFoundError, DatasetValidationError) as exc:
        return None, str(exc)


def main() -> None:
    st.set_page_config(page_title="Smart EV Range Predictor", layout="wide")
    st.title("Smart EV Range Predictor")
    st.write(
        "Estimate realistic EV range for UAE driving conditions using heat, AC, speed, driving mode, and traffic-aware fuzzy logic."
    )

    user_inputs = render_sidebar_controls()
    payload = build_dashboard_payload(user_inputs)

    render_range_metrics(payload)
    st.plotly_chart(
        build_range_comparison_figure(
            baseline_remaining_km=float(payload["baseline_remaining_km"]),
            adjusted_range_km=float(payload["adjusted_range_km"]),
        ),
        use_container_width=True,
    )
    render_explanation_panel(payload)

    st.divider()
    st.header("Dataset-Backed Insights")
    dataset, error_message = load_dashboard_dataset()
    if error_message:
        st.warning(error_message)
        render_dataset_summary({})
        return

    assert dataset is not None
    summary = build_dataset_summary(dataset)
    render_dataset_summary(summary)
    st.plotly_chart(
        build_energy_profile_figure(build_energy_by_speed(dataset)),
        use_container_width=True,
    )


if __name__ == "__main__":
    main()
