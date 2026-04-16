from __future__ import annotations

from dataclasses import dataclass

import streamlit as st

from src.config import DRIVING_MODE_LABELS, TRAFFIC_CONDITION_LABELS


@dataclass
class UserInputs:
    manufacturer_range_km: float
    battery_pct: float
    temperature_c: float
    ac_intensity: float
    speed_kmh: float
    driving_mode: float
    traffic_condition: float


def render_sidebar_controls() -> UserInputs:
    st.sidebar.header("Range Inputs")
    manufacturer_range_km = st.sidebar.number_input(
        "Manufacturer Rated Range (km)",
        min_value=100.0,
        max_value=1000.0,
        value=450.0,
        step=10.0,
    )
    battery_pct = st.sidebar.slider("Battery Percentage", 0, 100, 80)
    temperature_c = st.sidebar.slider("Ambient Temperature (C)", 10, 55, 35)
    ac_intensity = st.sidebar.slider("AC Intensity", 0, 10, 6)
    speed_kmh = st.sidebar.slider("Vehicle Speed (km/h)", 0, 120, 60)
    driving_mode = st.sidebar.select_slider(
        "Driving Mode",
        options=list(DRIVING_MODE_LABELS.keys()),
        value=2,
        format_func=lambda value: DRIVING_MODE_LABELS[value],
    )
    traffic_condition = st.sidebar.select_slider(
        "Traffic Condition",
        options=list(TRAFFIC_CONDITION_LABELS.keys()),
        value=2,
        format_func=lambda value: TRAFFIC_CONDITION_LABELS[value],
    )

    return UserInputs(
        manufacturer_range_km=manufacturer_range_km,
        battery_pct=float(battery_pct),
        temperature_c=float(temperature_c),
        ac_intensity=float(ac_intensity),
        speed_kmh=float(speed_kmh),
        driving_mode=float(driving_mode),
        traffic_condition=float(traffic_condition),
    )
