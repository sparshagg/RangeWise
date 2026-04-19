from __future__ import annotations

import pandas as pd
import plotly.graph_objects as go


def build_range_comparison_figure(
    *,
    claimed_remaining_km: float,
    shown_range_km: float,
    adjusted_range_km: float,
    hybrid_range_km: float | None = None,
) -> go.Figure:
    labels = ["Claimed Remaining", "Shown Range", "Fuzzy-Only Range"]
    values = [claimed_remaining_km, shown_range_km, adjusted_range_km]
    colors = ["#5f6caf", "#f0a202", "#d95d39"]

    if hybrid_range_km is not None:
        labels.append("Hybrid Range")
        values.append(hybrid_range_km)
        colors.append("#2ec4b6")

    title = (
        "Claimed vs Shown vs Fuzzy vs Hybrid EV Range"
        if hybrid_range_km is not None
        else "Claimed vs Shown vs Fuzzy-Only EV Range"
    )

    figure = go.Figure(
        data=[go.Bar(x=labels, y=values, marker_color=colors)]
    )
    figure.update_layout(
        title=title,
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
            x=df["speed_level"],
            y=df["km_per_kwh"],
            marker_color="#d95d39",
        )
    )
    figure.update_layout(
        title="Average Dataset Efficiency by Speed Band",
        xaxis_title="Speed Band (km/h)",
        yaxis_title="Efficiency (km/kWh)",
        template="plotly_white",
    )
    return figure
