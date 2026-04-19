from __future__ import annotations

from pathlib import Path
import sys

import pandas as pd
import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.analysis.dataset_range_model import build_efficiency_lookup_table
from src.analysis.dataset_summary import build_dataset_summary, build_energy_by_speed
from src.config import ANFIS_WEIGHTS_PATH, DATASET_PATH, PROCESSED_DATASET_PATH
from src.data.loader import (
    DatasetValidationError,
    build_processed_dataset_frame,
    load_dataset,
    load_processed_dataset,
)
from src.fuzzy.inference import predict_adjusted_range
from src.ui.charts import build_energy_profile_figure, build_range_comparison_figure
from src.ui.controls import UserInputs, render_sidebar_controls
from src.ui.panels import (
    render_dataset_lookup_table,
    render_processed_dataset_preview,
    render_processing_flow,
    render_dataset_summary,
    render_explanation_panel,
    render_range_metrics,
)


@st.cache_resource
def load_anfis_model():
    """Load trained ANFIS weights once per session. Returns None if not trained yet."""
    if not ANFIS_WEIGHTS_PATH.exists():
        return None
    try:
        from src.neuro_fuzzy.anfis import ANFIS
        return ANFIS.load(ANFIS_WEIGHTS_PATH)
    except Exception:
        return None


def build_dashboard_payload(
    user_inputs: UserInputs,
    dataset: pd.DataFrame | None = None,
    anfis=None,
) -> dict[str, object]:
    return predict_adjusted_range(
        manufacturer_range_km=user_inputs.manufacturer_range_km,
        battery_pct=user_inputs.battery_pct,
        temperature_level=user_inputs.temperature_level,
        ac_level=user_inputs.ac_level,
        speed_level=user_inputs.speed_level,
        driving_mode=user_inputs.driving_mode,
        traffic_level=user_inputs.traffic_level,
        dataset=dataset,
        anfis=anfis,
    )


def load_dashboard_dataset(dataset_path: str | Path = DATASET_PATH) -> tuple[pd.DataFrame | None, str | None]:
    try:
        return load_dataset(dataset_path), None
    except (FileNotFoundError, DatasetValidationError) as exc:
        return None, str(exc)


def load_dashboard_processed_dataset(
    dataset_path: str | Path = PROCESSED_DATASET_PATH,
) -> tuple[pd.DataFrame | None, str | None]:
    try:
        return load_processed_dataset(dataset_path), None
    except FileNotFoundError:
        try:
            return build_processed_dataset_frame(), None
        except (FileNotFoundError, DatasetValidationError) as exc:
            return None, str(exc)


def main() -> None:
    st.set_page_config(page_title="Smart EV Range Predictor", layout="wide")
    st.title("Smart EV Range Predictor")
    st.write(
        "Estimate realistic EV range for UAE driving conditions using a dataset-backed shown-range stage plus a fuzzy UAE correction for heat and AC."
    )

    user_inputs = render_sidebar_controls()
    dataset, error_message = load_dashboard_dataset()
    anfis_model = load_anfis_model()
    payload = build_dashboard_payload(user_inputs, dataset, anfis_model)

    render_range_metrics(payload)
    hybrid_km = payload.get("hybrid_range_km")
    st.plotly_chart(
        build_range_comparison_figure(
            claimed_remaining_km=float(payload["claimed_remaining_km"]),
            shown_range_km=float(payload["shown_range_km"]),
            adjusted_range_km=float(payload["adjusted_range_km"]),
            hybrid_range_km=float(hybrid_km) if hybrid_km is not None else None,
        ),
        use_container_width=True,
    )
    render_explanation_panel(payload)

    st.divider()
    st.header("Dataset-Backed Insights")
    if error_message:
        st.warning(error_message)
        render_dataset_summary({})
        render_dataset_lookup_table(pd.DataFrame())
        render_processed_dataset_preview(pd.DataFrame())
        return

    assert dataset is not None
    processed_dataset, processed_error_message = load_dashboard_processed_dataset()
    summary = build_dataset_summary(dataset)
    render_dataset_summary(summary)
    render_processing_flow()
    if processed_error_message:
        st.warning(processed_error_message)
        render_processed_dataset_preview(pd.DataFrame())
    else:
        assert processed_dataset is not None
        render_processed_dataset_preview(processed_dataset)
    render_dataset_lookup_table(build_efficiency_lookup_table(dataset))
    st.plotly_chart(
        build_energy_profile_figure(build_energy_by_speed(dataset)),
        use_container_width=True,
    )


if __name__ == "__main__":
    main()
