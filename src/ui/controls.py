from __future__ import annotations

from dataclasses import dataclass

import streamlit as st


@dataclass
class UserInputs:
    manufacturer_range_km: float
    battery_pct: float
    temperature_c: float
    ac_intensity: float
    driving_style: float
    traffic_level: float


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
    driving_style = st.sidebar.slider("Driving Style", 0, 10, 5)
    traffic_level = st.sidebar.slider("Traffic Level", 0, 10, 5)

    return UserInputs(
        manufacturer_range_km=manufacturer_range_km,
        battery_pct=float(battery_pct),
        temperature_c=float(temperature_c),
        ac_intensity=float(ac_intensity),
        driving_style=float(driving_style),
        traffic_level=float(traffic_level),
    )

