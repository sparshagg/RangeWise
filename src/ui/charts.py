from __future__ import annotations

import pandas as pd
import plotly.graph_objects as go


def build_range_comparison_figure(*, baseline_remaining_km: float, adjusted_range_km: float) -> go.Figure:
    figure = go.Figure(
        data=[
            go.Bar(
                x=["Baseline Remaining Range", "Adjusted Range"],
                y=[baseline_remaining_km, adjusted_range_km],
                marker_color=["#5f6caf", "#d95d39"],
            )
        ]
    )
    figure.update_layout(
        title="Baseline vs Adjusted EV Range",
        yaxis_title="Range (km)",
        template="plotly_white",
    )
    return figure


def build_energy_profile_figure(df: pd.DataFrame) -> go.Figure:
    figure = go.Figure()
    if df.empty:
        figure.update_layout(
            title="Dataset insight unavailable",
            template="plotly_white",
        )
        return figure

    figure.add_trace(
        go.Bar(
            x=df["speed_band"],
            y=df["energy_consumption_kwh"],
            marker_color="#d95d39",
        )
    )
    figure.update_layout(
        title="Average Energy Consumption by Speed Band",
        xaxis_title="Speed Band (km/h)",
        yaxis_title="Energy Consumption (kWh)",
        template="plotly_white",
    )
    return figure
