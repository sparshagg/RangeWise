from __future__ import annotations


def build_explanation(
    *,
    battery_pct: float,
    temperature_c: float,
    ac_intensity: float,
    driving_style: float,
    traffic_level: float,
    adjustment_factor: float,
) -> dict[str, str | list[str]]:
    drivers: list[str] = []

    if battery_pct <= 25:
        drivers.append("Low battery state is already limiting the remaining baseline range.")
    if temperature_c >= 40:
        drivers.append("Hot UAE ambient temperature is increasing EV energy demand.")
    elif temperature_c >= 30:
        drivers.append("Warm ambient temperature is creating a moderate heat penalty.")

    if ac_intensity >= 7:
        drivers.append("Strong AC usage is reducing range to maintain cabin comfort.")
    elif ac_intensity <= 3:
        drivers.append("Light AC usage helps preserve range.")

    if driving_style >= 7:
        drivers.append("Aggressive driving behavior increases energy consumption.")
    elif driving_style <= 3:
        drivers.append("Efficient driving helps keep the range close to nominal.")

    if traffic_level >= 7:
        drivers.append("Heavy traffic adds stop-and-go inefficiency.")
    elif traffic_level <= 3:
        drivers.append("Light traffic helps maintain smoother energy usage.")

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

