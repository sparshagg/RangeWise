from __future__ import annotations


def build_explanation(
    *,
    battery_pct: float,
    temperature_level: str,
    ac_level: str,
    speed_level: str,
    driving_mode: str,
    traffic_level: str,
    adjustment_factor: float,
) -> dict[str, str | list[str]]:
    drivers: list[str] = []

    if battery_pct <= 25:
        drivers.append("Low battery state is already limiting the remaining baseline range.")
    if temperature_level == "Extremely Hot":
        drivers.append("Extremely hot UAE weather is creating the harshest thermal penalty.")
    elif temperature_level == "Very Hot":
        drivers.append("Very hot weather is adding a strong heat penalty.")
    elif temperature_level == "Hot":
        drivers.append("Hot weather is slightly reducing the expected range.")
    else:
        drivers.append("Pleasant weather keeps thermal stress on the vehicle lower.")

    if ac_level == "High":
        drivers.append("High AC demand is reducing range to maintain cabin comfort.")
    elif ac_level == "Medium":
        drivers.append("Medium AC usage adds a moderate auxiliary load.")
    else:
        drivers.append("Low AC usage helps preserve battery range.")

    if speed_level == "Extreme Highway":
        drivers.append("Extreme highway speed is one of the strongest range penalties in the model.")
    elif speed_level == "Fast Highway":
        drivers.append("Fast highway speed creates a major energy penalty.")
    elif speed_level == "Highway":
        drivers.append("Highway speed noticeably increases energy demand.")
    elif speed_level == "City":
        drivers.append("City-speed driving creates a moderate speed penalty.")
    else:
        drivers.append("Local-road speed helps keep energy demand comparatively low.")

    if driving_mode == "Sport":
        drivers.append("Sport driving mode increases power demand and reduces range.")
    elif driving_mode == "Comfort":
        drivers.append("Comfort mode balances performance and efficiency.")
    elif driving_mode == "Eco":
        drivers.append("Eco driving mode helps preserve range under the same conditions.")

    if traffic_level == "High":
        drivers.append("High traffic adds stop-and-go inefficiency.")
    elif traffic_level == "Moderate":
        drivers.append("Moderate traffic creates some additional drag on efficiency.")
    else:
        drivers.append("No traffic supports smoother, more efficient travel.")

    if not drivers:
        drivers.append("Conditions are balanced, so the estimated range remains near the baseline.")

    if adjustment_factor < 0.7:
        summary = "Harsh UAE driving conditions are causing a strong range reduction."
    elif adjustment_factor < 0.86:
        summary = "Current conditions are causing a noticeable range reduction."
    elif adjustment_factor < 0.95:
        summary = "Conditions are only slightly below ideal for EV range."
    else:
        summary = "Conditions are favorable and the EV stays close to its nominal range."

    return {
        "summary": summary,
        "drivers": drivers,
    }
