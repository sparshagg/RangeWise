from __future__ import annotations

from dataclasses import dataclass

import streamlit as st

from src.config import (
    AC_LEVEL_GUIDE,
    AC_LEVEL_VALUES,
    DRIVING_MODE_GUIDE,
    DRIVING_MODE_LEVEL_VALUES,
    SPEED_LEVEL_RANGES,
    SPEED_LEVEL_VALUES,
    TEMPERATURE_LEVEL_RANGES,
    TEMPERATURE_LEVEL_VALUES,
    TRAFFIC_LEVEL_GUIDE,
    TRAFFIC_LEVEL_VALUES,
)


@dataclass
class UserInputs:
    manufacturer_range_km: float
    battery_pct: float
    temperature_level: str
    ac_level: str
    speed_level: str
    driving_mode: str
    traffic_level: str


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
    temperature_level = st.sidebar.select_slider(
        "Temperature",
        options=list(TEMPERATURE_LEVEL_VALUES.keys()),
        value="Hot",
    )
    ac_level = st.sidebar.select_slider(
        "AC Intensity",
        options=list(AC_LEVEL_VALUES.keys()),
        value="Medium",
    )
    speed_level = st.sidebar.select_slider(
        "Speed",
        options=list(SPEED_LEVEL_VALUES.keys()),
        value="City",
    )
    driving_mode = st.sidebar.select_slider(
        "Driving Mode",
        options=list(DRIVING_MODE_LEVEL_VALUES.keys()),
        value="Comfort",
    )
    traffic_level = st.sidebar.select_slider(
        "Traffic Condition",
        options=list(TRAFFIC_LEVEL_VALUES.keys()),
        value="Moderate",
    )

    st.sidebar.caption(f"Representative temperature: {TEMPERATURE_LEVEL_VALUES[temperature_level]}C")
    st.sidebar.caption(f"Representative AC load: {AC_LEVEL_VALUES[ac_level]}/10")
    st.sidebar.caption(f"Representative speed: {SPEED_LEVEL_VALUES[speed_level]} km/h")

    with st.sidebar.expander("Input Band Reference"):
        st.write("Temperature bands")
        for label, band in TEMPERATURE_LEVEL_RANGES.items():
            st.write(f"- {label}: {band}")
        st.write("AC levels")
        for label, guide in AC_LEVEL_GUIDE.items():
            st.write(f"- {label}: {guide}")
        st.write("Speed bands")
        for label, band in SPEED_LEVEL_RANGES.items():
            st.write(f"- {label}: {band}")
        st.write("Driving modes")
        for label, guide in DRIVING_MODE_GUIDE.items():
            st.write(f"- {label}: {guide}")
        st.write("Traffic levels")
        for label, guide in TRAFFIC_LEVEL_GUIDE.items():
            st.write(f"- {label}: {guide}")

    return UserInputs(
        manufacturer_range_km=manufacturer_range_km,
        battery_pct=float(battery_pct),
        temperature_level=temperature_level,
        ac_level=ac_level,
        speed_level=speed_level,
        driving_mode=driving_mode,
        traffic_level=traffic_level,
    )
